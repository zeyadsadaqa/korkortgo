package se.korkort

import kotlin.random.Random
import kotlin.test.*

/** Runtime guards and selection behaviour for non-release candidate content. */
class QuestionPackage9JTest {
    @Test fun allCanonicalRelationshipsResolveAndHeldProposalsStayOutOfLiveBank() {
        assertFalse(candidateReleaseAccepted9J)
        assertEquals(1000, questionRelationships9J.size)
        questionBank.forEach { row ->
            val r = row.canonicalRelationship
            (listOf(r.primaryLessonId) + r.relatedLessonIds + r.referenceIds + r.sourceIds).forEach { id -> assertIs<Resolution.Found>(canonicalResolver.canonical(ContentTarget(id))) }
            if (row.id.startsWith("sign-") && row.assessment == null) assertTrue(QuestionId(row.id) in replacementDeliveryHolds)
        }
        assertEquals(384, candidateQuestions9J.count { it.acceptance.eligibility == ScoringEligibility.ACCEPTED })
        assertEquals(616, candidateQuestions9J.count { it.acceptance.eligibility == ScoringEligibility.HELD })
    }
    @Test fun everyLengthAndSeedPreserveQuotasConceptUniquenessAndResidualPicks() {
        val accepted = candidateQuestions9J.filter { it.acceptance.eligibility == ScoringEligibility.ACCEPTED }
        val counts = Category.entries.associateWith { category -> accepted.filter { it.category == category }.map { it.conceptId }.distinct().size }
        assertEquals(listOf(45, 26, 45, 47, 29), Category.entries.map { counts[it] })
        assertEquals(listOf(7,5,16,32,5), Category.entries.map { QuizEngine.allocation(70).categories[it] })
        assertEquals(5, QuizEngine.allocation(70).random)
        for (size in 1..70) for (seed in 0..19) {
            val selected = AssessmentEngine.select(candidateQuestions9J, size, candidateIdentity9J, Random(seed))
            val allocation = QuizEngine.allocation(size)
            assertEquals(size, selected.size)
            assertEquals(size, selected.map { it.question.conceptId }.distinct().size)
            assertTrue(selected.all { it.question.acceptance.eligibility == ScoringEligibility.ACCEPTED })
            allocation.categories.forEach { (category, quota) -> assertTrue(selected.count { it.question.category == category } >= quota) }
            assertEquals(allocation.random, size-allocation.categories.values.sum())
            // Largest-remainder allocation, independently reconstructed from integer remainders.
            val weights = Category.entries.map { it.quota } + 5
            val independent = weights.map { size * it / 70 }.toMutableList()
            val order = weights.indices.sortedWith(compareByDescending<Int> { size * weights[it] % 70 }.thenBy { it })
            repeat(size-independent.sum()) { independent[order[it]]++ }
            assertEquals(independent, Category.entries.map { allocation.categories.getValue(it) } + allocation.random)
        }
    }
    @Test fun allKeysVisitEveryPositionAndBothFeedbackModesStayGuarded() {
        candidateQuestions9J.forEach { q ->
            val positions=mutableSetOf<Int>()
            repeat(80) { seed ->
                val snapshot=q.snapshot(candidateIdentity9J,Random(seed))
                positions+=snapshot.displayedOptionIds.indexOf(q.feedback.correctOptionId)
                assertEquals(1,snapshot.displayedOptionIds.count { snapshot.isCorrect(SnapshotAnswer(q.key,it)) })
                snapshot.displayedOptionIds.forEach { id -> assertEquals(id,snapshot.feedbackFor(id).optionId) }
            }
            assertEquals(setOf(0,1,2,3),positions,q.key.questionId.value)
            if (q.acceptance.eligibility==ScoringEligibility.ACCEPTED) {
                Feedback.entries.forEach { mode ->
                    var session=AssessmentSession(listOf(q.snapshot(candidateIdentity9J,Random(9))),mode)
                    assertNull(session.presentation().explanation)
                    session=session.answer(q.feedback.correctOptionId)
                    assertEquals(mode==Feedback.IMMEDIATE,session.presentation().explanation!=null)
                    session=session.next()
                    assertEquals(1,session.score)
                    assertNotNull(session.presentation().explanation)
                }
            } else assertFailsWith<IllegalArgumentException> { AssessmentSession(listOf(q.snapshot(candidateIdentity9J)),Feedback.IMMEDIATE) }
        }
    }
}
