package se.korkort
import kotlin.random.Random
import kotlin.test.*

class GeneratedAssessmentIdentityTest {
    @Test fun authoredIdentityAndRevisionSurviveGenerationAndEveryShufflePosition() {
        val pack = identityFixture9D1
        val question = pack.questions.questions.single()
        assertEquals("situation-001", question.key.questionId.value)
        val ids = (1..4).map { OptionId("situation-001-option-$it") }
        assertEquals(ids, question.options.map { it.id })
        assertEquals(ids[0], question.feedback.correctOptionId)
        assertEquals(ScoringEligibility.UNREVIEWED, question.acceptance.eligibility)
        val positions = mutableSetOf<Int>()
        repeat(100) { seed ->
            val snapshot = question.snapshot(pack.manifest.identity, Random(seed))
            assertEquals(question.key, snapshot.question.key)
            positions.add(snapshot.displayedOptionIds.indexOf(ids[0]))
            snapshot.displayedOptionIds.forEach { id ->
                assertEquals(question.feedback.optionFeedback.single { it.optionId == id }, snapshot.feedbackFor(id))
                assertEquals(id == ids[0], snapshot.isCorrect(SnapshotAnswer(question.key, id)))
            }
        }
        assertEquals(setOf(0, 1, 2, 3), positions)
    }
}
