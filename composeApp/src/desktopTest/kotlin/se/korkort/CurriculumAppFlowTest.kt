@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort

import androidx.compose.runtime.*
import androidx.compose.runtime.snapshots.Snapshot
import androidx.compose.ui.graphics.asComposeCanvas
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.platform.PlatformContext
import androidx.compose.ui.platform.UriHandler
import androidx.compose.ui.scene.CanvasLayersComposeScene
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.unit.IntSize
import org.jetbrains.skia.Surface
import org.jetbrains.skia.EncodedImageFormat
import java.io.File
import kotlin.test.*

/** Actual production owner; a single already-accepted text question makes UI assertions deterministic. */
class CurriculumAppFlowTest {
    private fun flow(mode:Feedback) {
        val question=candidateQuestions9J.single{it.key.questionId.value=="situation-001"}
        assertEquals(ScoringEligibility.ACCEPTED,question.acceptance.eligibility)
        val bank=PracticeBank(ContentPackageIdentity("root-route-fixture",Sha256("c".repeat(64))),listOf(question),true)
        val owners=mutableListOf<SemanticsOwner>()
        val listener=object:PlatformContext.SemanticsOwnerListener {
            override fun onSemanticsOwnerAppended(semanticsOwner:SemanticsOwner){owners.add(semanticsOwner)}
            override fun onSemanticsOwnerRemoved(semanticsOwner:SemanticsOwner){owners.remove(semanticsOwner)}
            override fun onSemanticsChange(semanticsOwner:SemanticsOwner){}
            override fun onLayoutChange(semanticsOwner:SemanticsOwner,semanticsNodeId:Int){}
        }
        val scene=CanvasLayersComposeScene(size=IntSize(1000,1800),platformContext=object:PlatformContext by PlatformContext.Empty{override val semanticsOwnerListener=listener})
        val surface=Surface.makeRasterN32Premul(1000,1800);var frame=0L
        val opened=mutableListOf<String>()
        fun render(){Snapshot.sendApplyNotifications();repeat(5){scene.render(surface.canvas.asComposeCanvas(),++frame*16_666_667)}}
        fun nodes():List<SemanticsNode>{
            fun walk(n:SemanticsNode):List<SemanticsNode> = listOf(n)+n.children.flatMap(::walk)
            return owners.lastOrNull()?.rootSemanticsNode?.let(::walk).orEmpty()
        }
        fun text()=nodes().flatMap{it.config.getOrNull(SemanticsProperties.Text).orEmpty()}.joinToString(" | "){it.text}
        fun await(message:String,condition:()->Boolean){repeat(300){render();if(condition())return;Thread.sleep(5)};error(message+"\n"+text())}
        fun click(label:String){await("Missing $label"){nodes().any{it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text==label}==true && it.config.getOrNull(SemanticsActions.OnClick)?.action!=null}};val n=nodes().first{it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text==label}==true && it.config.getOrNull(SemanticsActions.OnClick)?.action!=null};assertTrue(n.config[SemanticsActions.OnClick].action!!.invoke());render()}
        fun screenshot(name:String){render();val file=File("build/verification/9L14/${mode.name.lowercase()}-$name.png");file.parentFile.mkdirs();file.writeBytes(surface.makeImageSnapshot().encodeToData(EncodedImageFormat.PNG)!!.bytes)}
        try {
            scene.setContent{CompositionLocalProvider(LocalUriHandler provides object:UriHandler{override fun openUri(uri:String){opened.add(uri)}}){CurriculumApp(bank)}}
            await("Home missing"){text().contains("KörkortGo")};screenshot("home")
            click("Learning library")
            val query="Combine the instructions"
            await("No library query"){nodes().any{it.config.getOrNull(SemanticsActions.SetText)?.action!=null}}
            val search=nodes().first{it.config.getOrNull(SemanticsActions.SetText)?.action!=null}
            assertTrue(search.config[SemanticsActions.SetText].action!!.invoke(AnnotatedString(query)));render()
            click(query)
            // Header tab must reset a reader even when its route began inside Library.
            click("Learning library")
            await("Header library tab left the reader open"){nodes().any{it.config.getOrNull(SemanticsProperties.EditableText)?.text==query}}
            click("Overview")
            click("Start a practice test  >")
            val field=nodes().first{it.config.getOrNull(SemanticsActions.SetText)?.action!=null}
            assertTrue(field.config[SemanticsActions.SetText].action!!.invoke(AnnotatedString("1")));render()
            if(mode==Feedback.AT_END)click("At the end of the test")
            screenshot("setup");click("Start test  >")
            await("Quiz missing"){text().contains(question.prompt.assessmentText())}
            assertFalse(text().contains("Correct answer"))
            val wrong=question.options.first{it.id!=question.feedback.correctOptionId}.text.assessmentText()
            click(wrong)
            click("Learning library")
            await("No discard guard"){text().contains("Leave this test?")}
            click("Keep practising")
            assertEquals(1,nodes().count{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton && it.config.getOrNull(SemanticsProperties.Selected)==true})
            click("Confirm answer  >")
            assertEquals(mode==Feedback.IMMEDIATE,text().contains("Correct answer"))
            screenshot("confirmed");click("Finish test  >")
            await("Result missing"){text().contains("0 / 1")}
            screenshot("results");click("Review answers  >");click("Incorrect")
            click("Review all four options ↓")
            assertTrue(text().contains("Correct answer"));assertTrue(text().contains(question.feedback.explanation.assessmentText()))
            screenshot("expanded-review")
            val lesson=readerDocuments.single{it.id==question.relationship.primaryLessonId}
            click(lesson.title)
            await("Related lesson missing"){text().contains("Return to answer review")}
            screenshot("related-teaching");click("Return to answer review")
            assertTrue(text().contains("Hide explanation ↑"));assertTrue(text().contains("Correct answer"))
            val source=navigationSources.references.single{it.id==question.relationship.sourceUses.first().referenceId}
            click(source.title);await("Source detail missing"){text().contains("Back to answer review")}
            click("Open source");await("Registered URL was not delivered"){opened==listOf(source.url)}
            click("Back to answer review");assertTrue(text().contains("Hide explanation ↑"))
            await("Review source trigger did not regain focus"){nodes().any{it.config.getOrNull(SemanticsProperties.Focused)==true && it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text==source.title}==true}}
            click("Correct");assertTrue(text().contains("No answers in this filter."))
            click("All");assertTrue(text().contains(question.prompt.assessmentText()))
            click("Take another test  >")
            assertEquals("1",nodes().first{it.config.getOrNull(SemanticsProperties.EditableText)!=null}.config[SemanticsProperties.EditableText].text)
            click("Start test  >")
            assertEquals(0,nodes().count{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton && it.config.getOrNull(SemanticsProperties.Selected)==true})
            assertFalse(text().contains("Correct answer"))
            click("Learning library");click("Leave test")
            await("Discard destination missing"){text().contains("Search lessons")}
            assertFalse(text().contains(question.prompt.assessmentText()))
            screenshot("discarded-library")
        } finally {scene.close();surface.close()}
    }
    @Test fun immediateFeedbackProductionOwnerCompletesGuardReviewTeachingAndSourceFlow()=flow(Feedback.IMMEDIATE)
    @Test fun deferredFeedbackProductionOwnerCompletesGuardReviewTeachingAndSourceFlow()=flow(Feedback.AT_END)
}
