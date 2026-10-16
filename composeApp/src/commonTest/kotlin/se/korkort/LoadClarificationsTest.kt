package se.korkort

import kotlin.random.Random
import kotlin.test.*

class LoadClarificationsTest {
    @Test fun allThirtyKeysAndFeedbackRemainCorrectAfterShuffle() {
        val rows = questionBank.filter { it.id.startsWith("load-") }
        assertEquals(30, rows.size)
        rows.forEach { legacy ->
            val q = requireNotNull(legacy.assessment)
            assertEquals(SemanticRevision("load-r2"), q.key.revision)
            assertEquals(legacy.id, q.key.questionId.value)
            assertEquals("registered-payload", q.conceptId)
            assertEquals(ScoringEligibility.ACCEPTED, q.acceptance.eligibility)
            assertTrue(legacy.eligibleForScoring())
            val weights = Regex("(\\d+) kg").findAll(legacy.prompt).map { it.groupValues[1].toInt() }.toList()
            val expected = "${weights[0] - weights[1]} kg"
            assertEquals(expected, legacy.options[legacy.correct].text)
            assertEquals(1, legacy.options.count { it.text == expected })
            repeat(40) { seed ->
                val snapshot = q.snapshot(ContentPackageIdentity("test", Sha256("a".repeat(64))), Random(seed))
                assertEquals(1, snapshot.displayedOptionIds.count { snapshot.isCorrect(SnapshotAnswer(q.key, it)) })
                snapshot.displayedOptionIds.forEach { id -> assertEquals(id, snapshot.feedbackFor(id).optionId) }
            }
        }
    }
}
