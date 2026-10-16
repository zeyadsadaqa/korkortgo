package se.korkort
import kotlin.random.Random
import kotlin.test.*

class SignRewriteBatchTest {
    private val rewritten get() = questionBank.filter { it.assessment != null }
    @Test fun exactBatchHasStableIdsRevisionsAndBindings() {
        assertEquals(578,rewritten.size)
        assertEquals(578,rewritten.map { it.id }.toSet().size)
        assertEquals(289,rewritten.map { it.concept }.toSet().size)
        rewritten.forEach { legacy ->
            val q=requireNotNull(legacy.assessment)
            assertEquals(legacy.id,q.key.questionId.value)
            assertEquals(legacy.concept,q.conceptId)
            assertEquals(SemanticRevision("rewrite-r2"),q.key.revision)
            assertEquals(q.options[legacy.correct].id,q.feedback.correctOptionId)
            assertEquals(ScoringEligibility.HELD,q.acceptance.eligibility)
            assertTrue(q.acceptance.openHolds.isNotEmpty())
            assertTrue(q.acceptance.deliveryProof.isEmpty())
            assertNotNull(q.acceptance.contentReview)
            listOfNotNull(q.image).plus(q.options.mapNotNull { it.image }).forEach { assertTrue(it.neutralDescription!!.text.isNotBlank()) }
        }
    }
    @Test fun heldRewritesCannotEnterLegacyOrNewScoredSessions() {
        repeat(100) { seed -> assertTrue(QuizEngine.select(questionBank,70,Random(seed)).none { it.assessment != null }) }
        assertFailsWith<IllegalArgumentException> { QuizEngine.select(rewritten,1) }
        assertFailsWith<IllegalArgumentException> { QuizSession(listOf(rewritten.first()),Feedback.IMMEDIATE) }
        assertFailsWith<IllegalArgumentException> { AssessmentEngine.select(rewritten.map { it.assessment!! },1,ContentPackageIdentity("test",Sha256("a".repeat(64)))) }
    }
    @Test fun recognitionLabelsHaveNoCodeAndEveryPermutationKeepsOptionFeedback() {
        rewritten.forEach { legacy ->
            val q=legacy.assessment!!
            assertFalse(q.prompt.assessmentText().contains("(${q.feedback.targetSignCode})"))
            if(legacy.id.startsWith("sign-recognise-")) {
                assertTrue(q.options.all { it.text.isEmpty() && it.image != null })
                assertTrue(legacy.options.all { it.text.isEmpty() })
            }
            val positions=mutableSetOf<Int>()
            repeat(100) { seed ->
                val snapshot=q.snapshot(ContentPackageIdentity("test",Sha256("a".repeat(64))),Random(seed))
                positions.add(snapshot.displayedOptionIds.indexOf(q.feedback.correctOptionId))
                snapshot.displayedOptionIds.forEach { id ->
                    assertEquals(id,snapshot.feedbackFor(id).optionId)
                    assertEquals(id==q.feedback.correctOptionId,snapshot.isCorrect(SnapshotAnswer(q.key,id)))
                }
            }
            assertEquals(setOf(0,1,2,3),positions)
        }
    }
}
