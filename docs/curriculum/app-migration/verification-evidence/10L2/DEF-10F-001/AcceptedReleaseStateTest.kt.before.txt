package se.korkort

import kotlin.random.Random
import kotlin.test.*

/** Repeats scored/transient checks on the release bank, never the candidate subset. */
class AcceptedReleaseStateTest {
    @Test fun acceptedPackagePreservesEverySizeBothFeedbackModesAndExactSnapshotScores() {
        val bank=acceptedPracticeBank9J
        assertTrue(bank.releaseAccepted)
        assertEquals(1000,bank.questions.size)
        assertEquals(500,bank.questions.map{it.conceptId}.toSet().size)
        assertTrue(bank.questions.all{it.acceptance.eligibility==ScoringEligibility.ACCEPTED && it.acceptance.openHolds.isEmpty()})
        for(mode in Feedback.entries)for(size in 1..70)for(seed in 0..19) {
            var state=TransientQuizState(countText=size.toString(),feedback=mode).showSetup().startPractice(bank,Random(seed))
            val pinned=state.pinned!!
            assertEquals(size,pinned.assessment.snapshots.size)
            assertEquals(size,pinned.assessment.snapshots.map{it.question.conceptId}.toSet().size)
            val mix=QuizEngine.allocation(size)
            mix.categories.forEach{(category,quota)->assertTrue(pinned.assessment.snapshots.count{it.question.category==category}>=quota)}
            repeat(size){
                val p=state.pinned!!;val token=p.token
                assertEquals(bank.identity,token.packageIdentity)
                assertNull(p.assessment.presentation().explanation)
                val option=p.assessment.current.question.feedback.correctOptionId
                state=state.select(token,option).confirm(token)
                assertEquals(mode==Feedback.IMMEDIATE,state.pinned!!.assessment.presentation().explanation!=null)
                state=state.nextQuestion()
            }
            assertEquals(size,state.pinned!!.assessment.score)
            assertEquals(AppDestination.Results(pinned.id),state.navigation.current)
            state=state.openReview()
            assertEquals((0 until size).toList(),state.reviewPositions())
            assertEquals(0,state.filterReview(PracticeReviewFilter.INCORRECT).reviewPositions().size)
            assertNull(state.filterReview(PracticeReviewFilter.INCORRECT).reviewPresentation())
            state=state.filterReview(PracticeReviewFilter.CORRECT).moveReview(size-1)
            assertEquals(size-1,state.reviewSnapshotPosition())
            val snapshot=state.reviewPresentation()!!
            assertTrue(snapshot.choices.single{it.selected}.correct!!)
            assertEquals(bank.identity,state.pinned!!.assessment.current.packageIdentity)
        }
    }

    @Test fun acceptedPackageGuardsDraftReviewSourcesPreferencesAndProcessReset() {
        val bank=acceptedPracticeBank9J
        var state=TransientQuizState(countText="2",feedback=Feedback.IMMEDIATE).showSetup().startPractice(bank,Random(41))
        val initial=state.pinned!!
        val token=initial.token
        val option=token.displayedOptionIds[1]
        state=state.select(token,option)
        val pending=state.request(NavigationRequest(AppDestination.Library)).first
        assertNotNull(pending.navigation.pending)
        state=pending.cancelExit()
        assertEquals(initial,state.pinned);assertEquals(option,state.draft!!.optionId)
        state=state.confirm(token).nextQuestion()
        val second=state.pinned!!.token
        state=state.select(second,second.displayedOptionIds[0]).confirm(second).nextQuestion().openReview()
        val key=state.pinned!!.assessment.snapshots[1].question.key
        state=state.moveReview(1).expandReview(key)
        val cursor=state.review
        val score=state.pinned!!.assessment.score
        val question=state.pinned!!.assessment.snapshots[1].question
        state=state.request(NavigationRequest(AppDestination.Content(ContentTarget(question.relationship.primaryLessonId)),NavigationIntent.RELATED_READING)).first
        assertEquals(cursor,state.review);assertEquals(score,state.pinned!!.assessment.score)
        state=state.openReview()
        assertEquals(cursor,state.review)
        val id=question.relationship.sourceUses.first().referenceId
        state=state.request(NavigationRequest(state.navigation.current,NavigationIntent.SOURCE,sourceReferenceId=id)).first
        val (effect,consumed)=state.takeSourceToOpen();assertEquals(id,effect)
        state=consumed;assertNull(state.takeSourceToOpen().first);assertEquals(cursor,state.review)
        state=state.showSetup();assertEquals("2",state.countText);assertEquals(Feedback.IMMEDIATE,state.feedback)
        state=state.startPractice(bank,Random(41))
        assertNotEquals(initial.id,state.pinned!!.id)
        assertFailsWith<IllegalArgumentException>{state.select(token,option)}
        val restarted=state.restartPracticeProcess()
        assertEquals("70",restarted.countText);assertEquals(Feedback.IMMEDIATE,restarted.feedback)
        assertNull(restarted.pinned);assertNull(restarted.review);assertNull(restarted.draft)
        val missing=restarted.request(NavigationRequest(AppDestination.Results("missing"))).first
        assertEquals(PracticeRecovery.MISSING_RESULT,missing.recovery)
        assertEquals(AppDestination.QuizSetup,missing.navigation.current)
        assertNull(missing.pinned)
        for(raw in listOf("0","71","1.5",""))assertFalse(practiceStartCheck(raw,bank).allowed)
    }
}
