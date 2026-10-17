@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.*
import androidx.compose.runtime.snapshots.Snapshot
import androidx.compose.ui.graphics.asComposeCanvas
import androidx.compose.ui.input.key.*
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.PlatformContext
import androidx.compose.ui.scene.CanvasLayersComposeScene
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.Density
import androidx.compose.ui.unit.IntSize
import org.jetbrains.skia.EncodedImageFormat
import org.jetbrains.skia.Surface
import java.io.File
import kotlin.test.*

class LearningViewsSemanticsTest {
    private class Harness(width: Int, height: Int): AutoCloseable {
        private var owner: SemanticsOwner?=null
        private val listener=object: PlatformContext.SemanticsOwnerListener {
            override fun onSemanticsOwnerAppended(semanticsOwner: SemanticsOwner) {owner=semanticsOwner}
            override fun onSemanticsOwnerRemoved(semanticsOwner: SemanticsOwner) {owner=null}
            override fun onSemanticsChange(semanticsOwner: SemanticsOwner) {}
            override fun onLayoutChange(semanticsOwner: SemanticsOwner,semanticsNodeId:Int) {}
        }
        val scene=CanvasLayersComposeScene(size=IntSize(width,height),platformContext=object:PlatformContext by PlatformContext.Empty {override val semanticsOwnerListener=listener})
        private val surface=Surface.makeRasterN32Premul(width,height)
        private var frame=0L
        fun render() {Snapshot.sendApplyNotifications();repeat(4) {scene.render(surface.canvas.asComposeCanvas(),++frame*16_666_667)}}
        fun nodes(unmerged:Boolean=false):List<SemanticsNode> {
            fun walk(n:SemanticsNode):List<SemanticsNode> = listOf(n)+n.children.flatMap {walk(it)}
            val o=requireNotNull(owner)
            return walk(if(unmerged)o.unmergedRootSemanticsNode else o.rootSemanticsNode)
        }
        fun text()=nodes().joinToString(" | ") {n->n.config.getOrNull(SemanticsProperties.Text)?.joinToString {it.text}.orEmpty()+n.config.getOrNull(SemanticsProperties.ContentDescription)?.joinToString().orEmpty()}
        fun click(label:String) {
            val node=nodes().first {n->n.config.getOrNull(SemanticsProperties.Text)?.any {it.text==label}==true && n.config.getOrNull(SemanticsActions.OnClick)!=null}
            assertTrue(node.config[SemanticsActions.OnClick].action!!.invoke());render()
        }
        fun key(key:Key) {scene.sendKeyEvent(KeyEvent(key,KeyEventType.KeyDown));scene.sendKeyEvent(KeyEvent(key,KeyEventType.KeyUp));render()}
        fun awaitCondition(condition:()->Boolean) {repeat(200) {render();if(condition())return;Thread.sleep(5)};error("Image decoding did not finish")}
        fun screenshot(name:String) {repeat(20){render();Thread.sleep(5)};val f=File("build/verification/9L/$name.png");f.parentFile.mkdirs();f.writeBytes(surface.makeImageSnapshot().encodeToData(EncodedImageFormat.PNG)!!.bytes)}
        override fun close() {scene.close();surface.close()}
    }
    @Test fun deliberateRevealRemovesHiddenAnswerAndRestoresToggleFocus() {
        val doc=readerDocuments.single{it.id==ContentId("M03-L02")}
        val block=doc.bodyBlocks.single{(it.payload as? BlockPayload.KnowledgeCheck)?.prompts?.any{p->p.searchText().contains("amber")}==true}
        Harness(390,1500).use{h->
            h.scene.setContent{LearningTheme{TeachingBlock(block,doc.answerBlocks.associateBy{it.metadata.id},{})}}
            h.render()
            assertFalse(h.text().contains("unsafe stop"))
            val toggle=h.nodes().first{it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text=="Show answer"}==true && it.config.getOrNull(SemanticsActions.RequestFocus)!=null}
            assertTrue(toggle.config[SemanticsActions.RequestFocus].action!!.invoke());h.key(Key.Enter)
            assertTrue(h.text().contains("unsafe stop"))
            assertTrue(h.nodes().any{it.config.getOrNull(SemanticsProperties.StateDescription)=="Expanded"})
            h.screenshot("knowledge-revealed-phone")
            h.key(Key.Enter)
            assertFalse(h.text().contains("unsafe stop"))
            assertTrue(h.nodes().any{it.config.getOrNull(SemanticsProperties.Focused)==true && it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text=="Show answer"}==true})
        }
    }
    @Test fun libraryAndReaderRenderAtPhoneWideAndActualLargeText() {
        for(width in listOf(390,1280)) for(scale in listOf(1f,1.5f)) Harness(width,1800).use{h->
            h.scene.setContent{CompositionLocalProvider(LocalDensity provides Density(1f,scale)){LearningTheme{LearningLibrary({},{},{})}}}
            h.render()
            assertTrue(h.text().contains("Learning library"))
            h.screenshot("library-${width}-${scale}")
            h.scene.setContent{CompositionLocalProvider(LocalDensity provides Density(1f,scale)){LearningTheme{LessonReader(ContentTarget(ContentId("M03-L02")),{},{_,_->},{})}}}
            h.render()
            assertTrue(h.text().contains("Combine the instructions"))
            assertTrue(h.text().contains("Follow the traffic instructions"))
            if(width>800){val title=h.nodes().first{it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text=="Combine the instructions"}==true};assertTrue(title.boundsInRoot.width<=752f);assertTrue(title.boundsInRoot.left>=264f)}
            h.screenshot("reader-${width}-${scale}")
        }
    }
    @Test fun reviewUsesShuffledSnapshotAndWithholdsFeedbackUntilAllowed() {
        for(mode in Feedback.entries) Harness(800,2400).use{h->
            val q=candidateQuestions9J.single{it.key.questionId==QuestionId("situation-001")}
            val snapshot=SessionQuestionSnapshot(q,candidateIdentity9J,listOf(1,0,3,2).map{q.options[it].id})
            var session by mutableStateOf(AssessmentSession(listOf(snapshot),mode).answer(q.options[1].id))
            h.scene.setContent{LearningTheme{LearningAnswerReview(session,onRelated={},onSource={})}}
            h.render()
            assertTrue(h.text().contains("A. Follow the green light"))
            assertEquals(mode==Feedback.IMMEDIATE,h.text().contains("Correct answer"))
            if(mode==Feedback.AT_END){session=session.next();h.render()}
            assertTrue(h.text().contains("Correct answer"))
            assertTrue(h.text().contains("B. Stop as directed by the officer."))
            h.screenshot("review-${mode}")
        }
    }
    @Test fun exactFuelReviewUsesASelectedBCorrectAndSelectableUnroundedExplanation() {
        Harness(390,2400).use{h->
            val q=candidateQuestions9J.single{it.key.questionId==QuestionId("fuel-saving-150-0.5")}
            val snapshot=SessionQuestionSnapshot(q,candidateIdentity9J,listOf(1,0,3,2).map{q.options[it].id})
            val session=AssessmentSession(listOf(snapshot),Feedback.IMMEDIATE).answer(q.options[1].id)
            h.scene.setContent{LearningTheme{LearningAnswerReview(session,onRelated={},onSource={})}};h.render()
            assertTrue(h.text().contains("A. 0.375 litres"));assertTrue(h.text().contains("B. 0.75 litres"))
            assertTrue(h.text().contains("150 × 0.5 ÷ 100 = 0.75 litres exactly"))
            assertFalse(session.finished);assertNull(session.score)
            h.screenshot("fuel-review-phone")
        }
    }
    @Test fun calculationAndTableRetainFullTextAtSameViewportAndLargeScale() {
        val doc=readerDocuments.single{it.id==ContentId("M03-L04")}
        val blocks=doc.bodyBlocks.filter{it.searchText().contains("40.6") || it.searchText().contains("guarantee")}
        assertTrue(blocks.isNotEmpty())
        for(scale in listOf(1f,1.5f)) Harness(390,2600).use{h->
            h.scene.setContent{CompositionLocalProvider(LocalDensity provides Density(1f,scale)){LearningTheme{androidx.compose.foundation.layout.Column{blocks.forEach{TeachingBlock(it,emptyMap(),{})}}}}}
            h.render();assertTrue(h.text().contains("40.6"));h.screenshot("long-calculation-390-${scale}")
        }
        val table=readerDocuments.flatMap{it.bodyBlocks}.first{it.payload is BlockPayload.Table}
        Harness(390,2600).use{h->
            h.scene.setContent{CompositionLocalProvider(LocalDensity provides Density(1f,1.5f)){LearningTheme{TeachingBlock(table,emptyMap(),{})}}}
            h.render()
            val p=table.payload as BlockPayload.Table
            p.columns.forEach{assertTrue(h.text().contains(it.heading.assessmentText()))}
            p.rows.flatMap{it.cells}.forEach{assertTrue(h.text().contains(it.assessmentText()))}
            h.screenshot("table-390-1.5")
        }
    }
    @Test fun unavailableExternalFailureKeepsAllRecoveryActions() {
        Harness(390,1500).use{h->
            val r=canonicalResolver.legacy(LegacyLookup.Sign("legacy-app-4768933c3d9a","SIG16"))
            var library=false;var opened:ContentTarget?=null
            h.scene.setContent{LearningTheme{DestinationRecovery(r,{opened=it},{library=true},{false})}};h.render()
            h.click("Open official description")
            assertTrue(h.text().contains("could not be opened"))
            h.screenshot("signal-unavailable")
            h.click("Combine the instructions");assertEquals(ContentTarget(ContentId("M03-L02")),opened)
            h.click("Open learning library");assertTrue(library)
        }
    }
    @Test fun sourceReturnRestoresTheExactTriggerWithoutFabricatedPosition() {
        Harness(800,1600).use{h->
            val doc=readerDocuments.single{it.id==ContentId("M03-L02")}
            val state=androidx.compose.foundation.lazy.LazyListState(doc.bodyBlocks.size+2)
            var context:ReturnContext?=null
            var restored by mutableStateOf<RestoredContext?>(null)
            var source by mutableStateOf<SourceReferenceId?>(null)
            h.scene.setContent{LearningTheme{
                if(source==null)LessonReader(ContentTarget(doc.id),{},{id,c->context=c;source=id},{},restored=restored,state=state)
                else SourceDetail(source!!,{},{
                    restored=canonicalResolver.restore(context!!,lessonSources(doc).map{"source:${it.id.value}"}.toSet());source=null
                },{false})
            }}
            h.render()
            val ref=lessonSources(doc).first()
            // Resource fonts resolve asynchronously in the headless scene; scroll after their first layout.
            repeat(20){h.render();Thread.sleep(10)}
            val scroll=h.nodes().first{it.config.getOrNull(SemanticsActions.ScrollToIndex)!=null}
            assertTrue(scroll.config[SemanticsActions.ScrollToIndex].action!!.invoke(doc.bodyBlocks.size+2))
            h.awaitCondition{h.text().contains(ref.title)}
            val trigger=h.nodes().first{it.config.getOrNull(SemanticsProperties.Role)==Role.Button && it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text==ref.title}==true}
            assertTrue(trigger.config[SemanticsActions.OnClick].action!!.invoke());h.render()
            assertNotNull(context);assertEquals(doc.id,context!!.origin.contentId)
            assertEquals("source:${ref.id.value}",context!!.focusId)
            assertTrue(h.scene.focusManager.takeFocus(androidx.compose.ui.focus.FocusDirection.Next))
            h.click("Open source");assertTrue(h.text().contains("could not be opened"));h.screenshot("source-detail-failure")
            h.click("Return to reading");h.render()
            assertNotNull(restored!!.position)
            h.awaitCondition{h.nodes().any{it.config.getOrNull(SemanticsProperties.Focused)==true && it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text==ref.title}==true}}
            h.screenshot("source-return-focus")
            val focused=h.nodes().single{it.config.getOrNull(SemanticsProperties.Focused)==true}
            assertTrue(focused.boundsInRoot.top>=0f && focused.boundsInRoot.bottom<=1600f,"Focused source escaped the viewport after artwork decoding")
            h.scene.setContent{LearningTheme{SourceDirectory(context,{},{})}};h.render();h.screenshot("source-directory")
        }
    }
    @Test fun libraryClearActionsPreserveTheOtherInput() {
        Harness(1280,1600).use{h->
            h.scene.setContent{LearningTheme{LearningLibrary({},{},{})}};h.render()
            h.click("Traffic safety")
            val field=h.nodes().first{it.config.getOrNull(SemanticsActions.SetText)!=null}
            assertTrue(field.config[SemanticsActions.SetText].action!!.invoke(androidx.compose.ui.text.AnnotatedString("zzzxq")));h.render()
            assertTrue(h.text().contains("No matching lessons."))
            h.click("Clear filters");assertTrue(h.text().contains("No matching lessons."))
            h.screenshot("library-empty-wide")
            h.click("Traffic safety");h.click("Clear search")
            assertFalse(h.text().contains("No matching lessons."))
            assertTrue(h.nodes().any{it.config.getOrNull(SemanticsProperties.Selected)==true && it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text=="Traffic safety"}==true})
            h.screenshot("library-filtered-wide")
        }
    }
    @Test fun chooserRequiresDeliberateChoiceAndMovedPassageShowsParentNotice() {
        Harness(390,1600).use{h->
            val choices=canonicalResolver.legacy(LegacyLookup.Page("legacy-app-4768933c3d9a",46))
            var opened:ContentTarget?=null
            h.scene.setContent{LearningTheme{DestinationRecovery(choices,{opened=it},{},{false})}};h.render()
            assertNull(opened);h.screenshot("page-46-chooser")
            val choice=(choices as Resolution.Choices).choices[2]
            h.click(choice.entry.title);assertEquals(choice.target,opened)
            h.scene.setContent{LearningTheme{LessonReader(ContentTarget(ContentId("M03-L04"),BlockId("missing")),{},{_,_->},{})}};h.render()
            assertTrue(h.text().contains("This passage has moved. The related lesson is shown below."))
            h.screenshot("moved-passage")
        }
    }
    @Test fun approvedContextualCropCannotPaintIntoFollowingContent() {
        Harness(800,2000).use{h->
            val block=readerDocuments.single{it.id==ContentId("M03-L02")}.bodyBlocks.first{it.payload is BlockPayload.CroppedImage}
            h.scene.setContent{LearningTheme{androidx.compose.foundation.layout.Column{TeachingBlock(block,emptyMap(),{})}}};h.render()
            h.awaitCondition{!h.text().contains("Loading illustration")}
            assertFalse(h.text().contains("Illustration unavailable"))
            h.screenshot("contextual-crop-bounds")
            val bottom=h.nodes().mapNotNull{node->if(node.config.getOrNull(SemanticsProperties.Text)!=null)node.boundsInRoot.bottom else null}.max().toInt()
            assertTrue(bottom+120<2000)
            val bitmap=javax.imageio.ImageIO.read(File("build/verification/9L/contextual-crop-bounds.png"))
            for(y in bottom+20 until bottom+120) for(x in 24 until 776)
                assertEquals(0xfff7f8f3.toInt(),bitmap.getRGB(x,y),"Source sheet escaped its approved crop at $x,$y")
        }
    }
    @Test fun missingResultRequiresDeliberateSetupAction() {
        Harness(390,780).use{h->var setup=false
            h.scene.setContent{LearningTheme{MissingResults{setup=true}}};h.render()
            assertFalse(setup);assertTrue(h.text().contains("No saved result is available."))
            h.screenshot("missing-results")
            h.click("Set up a practice test");assertTrue(setup)
        }
    }
    @Test fun routeRetainsLibrarySearchExpansionAndAccessibleFieldState(){
        Harness(800,1800).use{h->
            h.scene.setContent{LearningRoute{false}};h.render()
            h.click("1. Choose to drive responsibly")
            val title="Your route into driving"
            val edit=h.nodes().single{it.config.getOrNull(SemanticsActions.SetText)!=null}
            assertTrue(edit.config[SemanticsActions.SetText].action!!.invoke(androidx.compose.ui.text.AnnotatedString(title)))
            h.render();h.click(title)
            h.awaitCondition{h.nodes().any{it.config.getOrNull(SemanticsProperties.Heading)!=null && it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text==title}==true}}
            h.click("Learning library")
            val restored=h.nodes().single{it.config.getOrNull(SemanticsActions.SetText)!=null}
            assertEquals(title,restored.config[SemanticsProperties.EditableText].text)
            assertEquals(listOf("Search lessons"),restored.config[SemanticsProperties.ContentDescription])
            assertEquals(title,restored.config[SemanticsProperties.StateDescription])
            h.click("Clear search")
            assertTrue(h.nodes().any{it.config.getOrNull(SemanticsProperties.StateDescription)=="Expanded" && it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text=="1. Choose to drive responsibly"}==true})
        }
    }
    @Test fun referenceBackUsesCatalogueRatherThanLibrary(){
        Harness(800,1800).use{h->
            val target=canonicalResolver.canonical(ContentTarget(navigationSigns.single{it.code=="B1"}.id))
            h.scene.setContent{LearningRoute(target){false}};h.render()
            h.click("‹ Road signs and reference")
            assertFalse(h.nodes().any{it.config.getOrNull(SemanticsActions.SetText)!=null})
            assertTrue(h.text().contains(navigationReferenceGroups.first().title))
        }
    }

}
