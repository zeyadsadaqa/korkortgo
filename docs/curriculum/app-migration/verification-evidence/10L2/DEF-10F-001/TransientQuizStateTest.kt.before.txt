package se.korkort

import kotlin.random.Random
import kotlin.test.*

class TransientQuizStateTest {
    private val identity=ContentPackageIdentity("state-fixture",Sha256("d".repeat(64)))
    private fun question(id:String,category:Category=Category.RULES)=AssessmentTest().question(id,category)
    private fun practice(mode:Feedback=Feedback.IMMEDIATE): TransientQuizState {
        val snapshots=(0..2).map{i->question("state-$i").snapshot(identity,Random(i))}
        val p=PinnedPractice("attempt-1",AssessmentSession(snapshots,mode))
        return TransientQuizState(pinned=p,navigation=GuardedNavigation(AppDestination.Quiz(p.id),p.navigation))
    }
    private fun finish(mode:Feedback=Feedback.IMMEDIATE):TransientQuizState {
        var s=practice(mode)
        repeat(3){i->val p=s.pinned!!;val option=if(i==1)p.assessment.current.displayedOptionIds.first{it!=p.assessment.current.question.feedback.correctOptionId}else p.assessment.current.question.feedback.correctOptionId
            s=s.select(p.token,option).confirm(p.token).nextQuestion()}
        return s
    }
    @Test fun draftConfirmationAndBothFeedbackModesPinAuthoredIdentity() {
        Feedback.entries.forEach{mode->
            val s=practice(mode);val token=s.pinned!!.token;val option=token.displayedOptionIds[0]
            val selected=s.select(token,option)
            assertNull(selected.pinned!!.assessment.currentAnswer);assertNull(selected.pinned.assessment.presentation().explanation)
            val confirmed=selected.confirm(token)
            assertEquals(option,confirmed.pinned!!.assessment.currentAnswer!!.selectedOptionId)
            assertEquals(mode==Feedback.IMMEDIATE,confirmed.pinned.assessment.presentation().explanation!=null)
            assertNull(confirmed.pinned.assessment.score)
            assertFailsWith<IllegalArgumentException>{confirmed.confirm(token)}
            assertFailsWith<IllegalArgumentException>{s.select(token.copy(sessionId="other"),option)}
            assertFailsWith<IllegalArgumentException>{s.select(token.copy(key=token.key.copy(revision=SemanticRevision("r2"))),option)}
            assertFailsWith<IllegalArgumentException>{s.select(token.copy(packageIdentity=identity.copy(contentVersion="new")),option)}
            assertFailsWith<IllegalArgumentException>{s.select(token.copy(displayedOptionIds=token.displayedOptionIds.reversed()),option)}
            assertFailsWith<IllegalArgumentException>{s.select(token,OptionId("foreign"))}
            val next=confirmed.nextQuestion();assertNull(next.draft)
            assertFailsWith<IllegalArgumentException>{next.select(token,option)}
        }
    }
    @Test fun reviewFilterPositionExpansionAndScoreSurviveTeachingAndSourceVisits() {
        var s=finish().openReview().filterReview(PracticeReviewFilter.CORRECT).moveReview(1)
        assertEquals(2,s.pinned!!.assessment.score)
        val key=s.pinned!!.assessment.snapshots[2].question.key
        s=s.expandReview(key)
        assertEquals(2,s.reviewSnapshotPosition());assertEquals(key,s.reviewPresentation()!!.key)
        val pinned=s.pinned;val cursor=s.review
        val request=NavigationRequest(AppDestination.Content(ContentTarget(ContentId("M03-L02"))),NavigationIntent.RELATED_READING)
        s=s.request(request).first
        assertEquals(cursor,s.review);assertEquals(pinned,s.pinned)
        s=s.openReview();assertEquals(cursor,s.review);assertEquals(pinned,s.pinned)
        assertEquals(key.questionId,(s.navigation.current as AppDestination.Review).questionId)
        val source=navigationSources.references.first().id
        s=s.request(NavigationRequest(s.navigation.current,NavigationIntent.SOURCE,sourceReferenceId=source)).first
        assertEquals(source,s.navigation.sourceToOpen);assertEquals(cursor,s.review);assertEquals(2,s.pinned!!.assessment.score)
        val (effect,consumed)=s.takeSourceToOpen();assertEquals(source,effect);assertNull(consumed.navigation.sourceToOpen);assertEquals(s.pinned,consumed.pinned)
        val empty=s.filterReview(PracticeReviewFilter.INCORRECT).filterReview(PracticeReviewFilter.CORRECT)
        assertEquals(0,empty.review!!.row)
        assertFailsWith<IllegalArgumentException>{s.moveReview(2)}
        assertEquals(s,s.request(NavigationRequest(AppDestination.Review(pinned!!.id,QuestionId("unknown")))).first)
    }
    @Test fun unfinishedGuardsPreserveDraftAndBindTheExactPendingAttempt() {
        var s=practice();val token=s.pinned!!.token;s=s.select(token,token.displayedOptionIds.first())
        val target=NavigationRequest(AppDestination.Content(ContentTarget(ContentId("M03-L02"))),NavigationIntent.RELATED_READING)
        assertIs<NavigationDecision.Denied>(s.request(target).second)
        val exit=NavigationRequest(AppDestination.Library)
        val (pending,decision)=s.request(exit);assertEquals(NavigationDecision.ConfirmDiscard,decision)
        assertEquals(s,pending.cancelExit())
        assertFailsWith<IllegalArgumentException>{pending.confirm(token)}
        val altered=pending.copy(pinned=pending.pinned!!.copy(assessment=pending.pinned.assessment.answer(token.displayedOptionIds.first())))
        assertFailsWith<IllegalArgumentException>{altered.discardExit()}
        val discarded=pending.discardExit();assertNull(discarded.pinned);assertNull(discarded.draft);assertNull(discarded.review);assertEquals(AppDestination.Library,discarded.navigation.current)
        assertIs<NavigationDecision.Denied>(s.request(NavigationRequest(AppDestination.Results("stale"))).second)
        assertNotNull(s.showSetup().navigation.pending)
        val answered=s.confirm(token)
        assertEquals(NavigationDecision.ConfirmDiscard,answered.request(target).second)
        val source=navigationSources.references.first().id
        val sourceExit=answered.request(NavigationRequest(answered.navigation.current,NavigationIntent.SOURCE,sourceReferenceId=source)).first
        assertNull(sourceExit.navigation.sourceToOpen)
        val left=sourceExit.discardExit();assertEquals(source,left.navigation.sourceToOpen);assertEquals(AppDestination.QuizSetup,left.navigation.current)
    }
    @Test fun missingContextsNeverFabricateResultsAndSetupDoesNotAutoStart() {
        val initial=TransientQuizState(countText="20",feedback=Feedback.AT_END,review=PracticeReviewCursor("gone"))
        val (missing,decision)=initial.request(NavigationRequest(AppDestination.Results("gone")))
        assertIs<NavigationDecision.MissingSession>(decision);assertEquals(PracticeRecovery.MISSING_RESULT,missing.recovery)
        assertNull(missing.pinned);assertNull(missing.review);assertEquals("20",missing.countText);assertEquals(Feedback.AT_END,missing.feedback)
        assertEquals(PracticeRecovery.NONE,missing.showSetup().recovery);assertNull(missing.showSetup().pinned)
        assertEquals("70",initial.copy(countText="invalid").recoverMissing(PracticeRecovery.MISSING_RESULT).countText)
        val restarted=finish().copy(countText="10",feedback=Feedback.AT_END,library=LibraryFilter("query",Category.RULES)).restartPracticeProcess()
        assertEquals(TransientQuizState(),restarted)
        assertEquals(PracticeRecovery.MISSING_QUIZ,restarted.request(NavigationRequest(AppDestination.Quiz("gone"))).first.recovery)
        val library=initial.copy(library=LibraryFilter("query",Category.SAFETY))
        assertNull(library.libraryCategory("unknown").library.category)
        assertEquals("query",library.libraryCategory("unknown").library.query)
        assertEquals(library.library,library.request(NavigationRequest(AppDestination.Library)).first.library)
        assertEquals(library.library,library.request(NavigationRequest(AppDestination.Content(ContentTarget(ContentId("M03-L02"))))).first.library)
    }
    @Test fun setupPreflightsEveryQuotaAndRandomSlotWithoutWeakeningReleaseGate() {
        val questions=Category.entries.flatMap{category->(0 until category.quota+5).map{question("${category.name}-$it",category)}}
        val bank=PracticeBank(identity,questions,true)
        for(size in 1..70)assertTrue(practiceStartCheck(size.toString(),bank).allowed)
        listOf("","0","71","abc","1.5","999999999999999").forEach{assertFalse(practiceStartCheck(it,bank).allowed)}
        val setup=TransientQuizState(countText="70",feedback=Feedback.AT_END).showSetup()
        val started=setup.startPractice(bank,Random(3));assertEquals(70,started.pinned!!.assessment.snapshots.size)
        assertEquals(Feedback.AT_END,started.copy(feedback=Feedback.IMMEDIATE).pinned!!.assessment.feedbackMode)
        assertFailsWith<IllegalArgumentException>{setup.startPractice(bank.copy(releaseAccepted=false))}
        assertFailsWith<IllegalArgumentException>{started.startPractice(bank)}
        assertFalse(practiceStartCheck("70",bank.copy(questions=questions.filter{it.category!=Category.RULES})).allowed)
        assertFalse(practiceStartCheck("70",bank.copy(questions=questions+questions.first())).allowed)
        val cross=questions.last().copy(conceptId=questions.first().conceptId)
        assertFalse(practiceStartCheck("70",bank.copy(questions=questions.dropLast(1)+cross)).allowed)
        val held=questions.map{it.copy(acceptance=it.acceptance.copy(eligibility=ScoringEligibility.HELD))}
        assertFalse(practiceStartCheck("1",bank.copy(questions=held)).allowed)
    }
    @Test fun staleRoutesCannotAbandonAnExistingAttemptAndZoomDoesNotChangeIt() {
        val original=practice()
        assertFailsWith<IllegalArgumentException>{original.recoverMissing(PracticeRecovery.MISSING_RESULT)}
        val broken=original.copy(navigation=original.navigation.copy(current=AppDestination.Results("missing")))
        val (repaired,decision)=broken.request(NavigationRequest(AppDestination.Library))
        assertIs<NavigationDecision.Denied>(decision)
        assertEquals(original.pinned,repaired.pinned)
        assertEquals(AppDestination.Quiz(original.pinned!!.id),repaired.navigation.current)
        val (zoom,allowed)=original.request(NavigationRequest(original.navigation.current,NavigationIntent.IMAGE_VIEWER))
        assertEquals(NavigationDecision.Allow,allowed);assertEquals(original,zoom)
        val invalid=original.request(NavigationRequest(original.navigation.current,NavigationIntent.SOURCE,sourceReferenceId=SourceReferenceId("unknown")))
        assertIs<NavigationDecision.Denied>(invalid.second);assertEquals(original,invalid.first)
    }
    @Test fun newSessionResetsReviewAndSnapshotScoresNeverConsultRevisedBank() {
        val old=finish().openReview().filterReview(PracticeReviewFilter.INCORRECT)
        val oldPin=old.pinned!!
        val revised=oldPin.assessment.snapshots.map{it.question.copy(key=it.question.key.copy(revision=SemanticRevision("r2")),feedback=it.question.feedback.copy(correctOptionId=it.question.options.first{option->option.id!=it.question.feedback.correctOptionId}.id))}
        assertEquals(2,old.pinned!!.assessment.score)
        assertEquals(1,old.reviewPositions().size)
        val bank=PracticeBank(identity.copy(contentVersion="new"),revised,true)
        val setup=old.copy(countText="1").showSetup()
        val next=setup.startPractice(bank,Random(1))
        assertNotEquals(oldPin.id,next.pinned!!.id)
        assertNull(next.review);assertNull(next.draft);assertEquals("new",next.pinned!!.token.packageIdentity.contentVersion)
        assertEquals(2,oldPin.assessment.score)
        val token=next.pinned!!.token
        val discarded=next.request(NavigationRequest(AppDestination.QuizSetup)).first.discardExit()
        val again=discarded.startPractice(bank,Random(1))
        assertNotEquals(token.sessionId,again.pinned!!.token.sessionId)
        assertFailsWith<IllegalArgumentException>{again.select(token,token.displayedOptionIds.first())}
    }
}
