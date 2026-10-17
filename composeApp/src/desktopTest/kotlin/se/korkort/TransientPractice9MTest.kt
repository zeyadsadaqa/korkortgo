@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort

import androidx.compose.runtime.*
import androidx.compose.runtime.snapshots.Snapshot
import androidx.compose.ui.graphics.asComposeCanvas
import androidx.compose.ui.platform.PlatformContext
import androidx.compose.ui.scene.CanvasLayersComposeScene
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.IntSize
import org.jetbrains.skia.Surface
import kotlin.random.Random
import kotlin.test.*

class TransientPractice9MTest {
    @Test fun heldCandidateCannotStartProductionAndAllSupportedFixtureSizesPreserveIdentity() {
        val bank=candidatePracticeBank9M
        assertFalse(bank.releaseAccepted)
        assertEquals(616,bank.questions.count{it.acceptance.eligibility==ScoringEligibility.HELD})
        assertFalse(practiceStartCheck("70",bank).allowed)
        assertFailsWith<IllegalArgumentException>{TransientQuizState().showSetup().startPractice(bank)}
        for(size in 1..70){
            val initial=TransientQuizState(countText=size.toString()).showSetup()
            val state=initial.startPracticeFixture(bank,Random(size))
            val a=state.pinned!!.assessment
            assertEquals(size,a.snapshots.size)
            assertEquals(size,a.snapshots.map{it.question.conceptId}.distinct().size)
            assertTrue(a.snapshots.all{it.packageIdentity==bank.identity && it.question.acceptance.eligibility==ScoringEligibility.ACCEPTED})
            var answered=state
            repeat(size){val pin=answered.pinned!!;answered=answered.select(pin.token,pin.assessment.current.question.feedback.correctOptionId).confirm(pin.token).nextQuestion()}
            assertEquals(size,answered.pinned!!.assessment.score)
            assertEquals(a.snapshots,answered.pinned!!.assessment.snapshots)
            val reviewed=answered.openReview().filterReview(PracticeReviewFilter.INCORRECT)
            assertTrue(reviewed.reviewPositions().isEmpty());assertNull(reviewed.reviewSnapshotPosition());assertNull(reviewed.reviewPresentation());assertNull((reviewed.navigation.current as AppDestination.Review).questionId)
        }
    }
    @Test fun reusedQuestionAndOrderCannotCarryUnconfirmedRadioSelectionIntoAnotherAttempt() {
        val q=AssessmentTest().question("shared").let{it.copy(options=it.options.map{option->option.copy(image=null)})}
        val identity=ContentPackageIdentity("ui-session-fixture",Sha256("e".repeat(64)))
        val snapshot=SessionQuestionSnapshot(q,identity,q.options.map{it.id})
        var practice by mutableStateOf(PinnedPractice("ui-1",AssessmentSession(listOf(snapshot),Feedback.IMMEDIATE)))
        var confirmed:Pair<PracticeQuestionToken,OptionId>?=null
        var owner:SemanticsOwner?=null
        val listener=object:PlatformContext.SemanticsOwnerListener{
            override fun onSemanticsOwnerAppended(semanticsOwner:SemanticsOwner){owner=semanticsOwner}
            override fun onSemanticsOwnerRemoved(semanticsOwner:SemanticsOwner){owner=null}
            override fun onSemanticsChange(semanticsOwner:SemanticsOwner){}
            override fun onLayoutChange(semanticsOwner:SemanticsOwner,semanticsNodeId:Int){}
        }
        val scene=CanvasLayersComposeScene(size=IntSize(800,1600),platformContext=object:PlatformContext by PlatformContext.Empty{override val semanticsOwnerListener=listener})
        val surface=Surface.makeRasterN32Premul(800,1600);var frame=0L
        fun render(){Snapshot.sendApplyNotifications();repeat(4){scene.render(surface.canvas.asComposeCanvas(),++frame*16_666_667)}}
        fun nodes():List<SemanticsNode>{
            fun walk(n:SemanticsNode):List<SemanticsNode> = listOf(n)+n.children.flatMap{walk(it)}
            return walk(owner!!.rootSemanticsNode)
        }
        try{
            scene.setContent{KorkortTheme{PinnedAssessmentCard(practice){token,id->confirmed=token to id}}};render()
            val radio=nodes().first{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton}
            assertTrue(radio.config[SemanticsActions.OnClick].action!!.invoke());render()
            assertEquals(1,nodes().count{it.config.getOrNull(SemanticsProperties.Selected)==true})
            practice=practice.copy(id="ui-2");render()
            assertEquals(0,nodes().count{it.config.getOrNull(SemanticsProperties.Selected)==true})
            assertNull(confirmed)
            val second=nodes().filter{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton}[1]
            assertTrue(second.config[SemanticsActions.OnClick].action!!.invoke());render()
            val button=nodes().first{it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text=="Confirm answer  >"}==true}
            assertTrue(button.config[SemanticsActions.OnClick].action!!.invoke());render()
            assertEquals(practice.token to q.options[1].id,confirmed)
        }finally{scene.close();surface.close()}
    }
}
