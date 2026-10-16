package se.korkort

import kotlin.random.Random
import kotlin.test.*

class FuelCorrectionsTest {
    @Test fun exactKeysRejectLegacyRevisionAndSurviveAllShufflePositions() {
        val keys = mapOf("fuel-saving-150-0.5" to "0.75 litres", "fuel-saving-150-1.5" to "2.25 litres", "fuel-saving-250-0.5" to "1.25 litres", "fuel-saving-250-1.5" to "3.75 litres")
        keys.forEach { (id, exact) ->
            val legacy = questionBank.single { it.id == id }
            val q = requireNotNull(legacy.assessment)
            assertEquals(SemanticRevision("fuel-exact-r2"), q.key.revision)
            assertEquals(exact, legacy.options[legacy.correct].text)
            assertTrue(legacy.eligibleForScoring())
            val positions = mutableSetOf<Int>()
            repeat(80) { seed ->
                val snapshot = q.snapshot(ContentPackageIdentity("test", Sha256("a".repeat(64))), Random(seed))
                positions += snapshot.displayedOptionIds.indexOf(q.feedback.correctOptionId)
                assertEquals(1, snapshot.displayedOptionIds.count { snapshot.isCorrect(SnapshotAnswer(q.key, it)) })
                val oldKey = q.key.copy(revision = SemanticRevision("legacy-r1"))
                assertFailsWith<IllegalArgumentException> { snapshot.isCorrect(SnapshotAnswer(oldKey, q.feedback.correctOptionId)) }
            }
            assertEquals(setOf(0, 1, 2, 3), positions)
        }
    }
    @Test fun sixUnitCorrectionsHaveStableAuthoredKeys() {
        val ids = listOf("fuel-40-5", "fuel-saving-100-0.5", "fuel-saving-100-1", "fuel-saving-100-2", "fuel-saving-200-0.5", "fuel-saving-200-1")
        ids.forEach { id ->
            val legacy = questionBank.single { it.id == id }
            val q = requireNotNull(legacy.assessment)
            assertEquals(SemanticRevision("fuel-unit-r2"), q.key.revision)
            assertEquals(q.options[legacy.correct].id, q.feedback.correctOptionId)
            assertEquals(ScoringEligibility.ACCEPTED, q.acceptance.eligibility)
        }
    }
}
