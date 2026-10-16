package se.korkort

import kotlin.random.Random
import kotlin.test.*

class ScenarioCorrectionsTest {
    private val ids = listOf("032", "045", "105", "107", "125", "162", "172", "178").map { "situation-$it" }
    @Test fun correctedQuestionsKeepIdentityAndFeedbackThroughShuffling() {
        ids.forEach { id ->
            val legacy = questionBank.single { it.id == id }
            val q = requireNotNull(legacy.assessment)
            assertEquals(id, q.key.questionId.value)
            assertEquals(id, q.conceptId)
            assertEquals(SemanticRevision("scenario-r2"), q.key.revision)
            assertEquals(ScoringEligibility.ACCEPTED, q.acceptance.eligibility)
            assertTrue(legacy.eligibleForScoring())
            assertEquals(legacy.explanation, q.feedback.explanation.assessmentText())
            repeat(40) { seed ->
                val snapshot = q.snapshot(ContentPackageIdentity("test", Sha256("a".repeat(64))), Random(seed))
                assertEquals(1, snapshot.displayedOptionIds.count { snapshot.isCorrect(SnapshotAnswer(q.key, it)) })
                snapshot.displayedOptionIds.forEach { option -> assertEquals(option, snapshot.feedbackFor(option).optionId) }
            }
        }
    }
}
