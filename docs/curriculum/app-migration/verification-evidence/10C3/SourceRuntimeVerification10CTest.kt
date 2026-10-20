@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort

import androidx.compose.runtime.*
import androidx.compose.runtime.snapshots.Snapshot
import androidx.compose.ui.graphics.asComposeCanvas
import androidx.compose.ui.input.key.*
import androidx.compose.ui.platform.PlatformContext
import androidx.compose.ui.scene.CanvasLayersComposeScene
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.IntSize
import org.jetbrains.skia.EncodedImageFormat
import org.jetbrains.skia.Surface
import java.io.File
import java.lang.reflect.Modifier
import java.nio.file.Files
import java.nio.file.Path
import kotlin.test.*

/** Fresh compiled-object export and actual reader semantics. Expected data is checked independently by verify_10b.py. */
class SourceRuntimeVerification10CTest {
    private val root: Path get() = generateSequence(Path.of(System.getProperty("user.dir"))) { it.parent }.first { Files.exists(it.resolve("content/curriculum.json")) }
    private fun quote(text: String): String = buildString {
        append('"')
        text.forEach { c -> when (c) {
            '"' -> append("\\\""); '\\' -> append("\\\\"); '\n' -> append("\\n"); '\r' -> append("\\r"); '\t' -> append("\\t")
            else -> if (c.code < 32) append("\\u%04x".format(c.code)) else append(c)
        } }
        append('"')
    }
    private fun canonical(value: Any?): String = when (value) {
        null -> "null"
        is String -> quote(value)
        is Number, is Boolean -> value.toString()
        is Enum<*> -> quote(value.name.lowercase())
        is Iterable<*> -> value.joinToString(",", "[", "]") { canonical(it) }
        is Map<*, *> -> value.entries.sortedBy { it.key.toString() }.joinToString(",", "{", "}") { canonical(it.key) + ":" + canonical(it.value) }
        else -> {
            val fields = value.javaClass.declaredFields.filter { !Modifier.isStatic(it.modifiers) && !it.isSynthetic }.associate { field ->
                field.isAccessible = true
                field.name.replace(Regex("([A-Z])")) { "_" + it.value.lowercase() } to field.get(value)
            }.toMutableMap()
            if (fields.keys == setOf("value")) canonical(fields.getValue("value")) else {
                if(value is BlockPayload.RelatedLinks) fields["links"]=value.links.map{mapOf("label" to it.label,"target" to it.target)}
                if (value is InlineContent || value is BlockPayload || value is TeachingLink)
                    fields["type"] = value.javaClass.simpleName.replace(Regex("([a-z])([A-Z])"),"$1_$2").lowercase()
                canonical(fields)
            }
        }
    }
    private inner class Harness(width: Int, height: Int): AutoCloseable {
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
        fun scrollTo(index:Int) { val action=nodes().mapNotNull{it.config.getOrNull(SemanticsActions.ScrollToIndex)}.first().action!!;assertTrue(action(index));render() }
        fun key(key:Key) {scene.sendKeyEvent(KeyEvent(key,KeyEventType.KeyDown));scene.sendKeyEvent(KeyEvent(key,KeyEventType.KeyUp));render()}
        fun awaitCondition(condition:()->Boolean) {repeat(200) {render();if(condition())return;Thread.sleep(5)};error("Image decoding did not finish")}
        fun screenshot(name:String) {repeat(20){render();Thread.sleep(5)};val f=root.resolve("docs/curriculum/app-migration/verification-evidence/10C3/captures/$name.png").toFile();f.parentFile.mkdirs();f.writeBytes(surface.makeImageSnapshot().encodeToData(EncodedImageFormat.PNG)!!.bytes)}
        override fun close() {scene.close();surface.close()}
    }


    @Test fun executeSourceFlows() {
        val out=root.resolve("docs/curriculum/app-migration/verification-evidence/10C3").toFile().apply{mkdirs()}
        val examples=listOf(
            "swedish_legislation" to "REF-9f4b74a976fa03fb",
            "foreign_guidance" to "REF-4c8313a9f060c341",
            "research" to "REF-642e8e5d8ee346e2",
            "commercial_shortcut" to "REF-0f011d29fdd9c97f",
            "manufacturer_caution" to "REF-8994a6a11921a063",
            "editorial_arithmetic" to "REF-642e8e5d8ee346e2")
        val rows=mutableListOf<Map<String,Any?>>()
        Harness(1280,2048).use { h ->
            for((kind,rid) in examples) {
                val source=navigationSources.references.single{it.id.value==rid}
                var returned=0;var backed=0;val dispatched=mutableListOf<String>();var accept=true
                h.scene.setContent { key(kind) { LearningTheme { SourceDetail(source.id,{backed++},{returned++},{dispatched.add(it.url);accept}) } } }
                h.awaitCondition{h.text().contains(source.title)}
                val required=listOf(source.title,source.publisher,source.classifications.joinToString(" · "){it.name.lowercase().replace('_',' ')},source.classificationNote)+source.evidence.flatMap{e->listOf("Checked: ${e.dates.checkedOn ?: "Not recorded"}","Retrieved: ${e.dates.retrievedOn ?: "Not recorded"}","Published: ${e.dates.publishedOn ?: "Not recorded"}",e.scope,e.finding)+e.limitations}
                assertTrue(required.all{h.text().contains(it)},"Source detail omissions for $kind")
                h.click("Back to Sources");assertEquals(1,backed)
                h.click("Return to reading");assertEquals(1,returned)
                rows.add(mapOf("case_class" to kind,"state" to "details_return","reference_id" to rid,"status" to "pass","detail_fields_checked" to required.size,"back_callbacks" to backed,"return_callbacks" to returned))
                h.click("Open source");assertEquals(listOf(source.url),dispatched)
                assertFalse(h.text().contains("could not be opened"))
                rows.add(mapOf("case_class" to kind,"state" to "external_dispatch","reference_id" to rid,"status" to "pass","dispatched_url" to dispatched.single(),"mechanism" to "injected callback; no OS/browser launch or HTTP claim"))
                accept=false;h.click("Open source")
                assertTrue(h.text().contains("The source could not be opened."))
                assertTrue(h.nodes().any{it.config.getOrNull(SemanticsProperties.LiveRegion)==LiveRegionMode.Polite})
                h.screenshot("$kind-failure")
                h.click("Return to reading");assertEquals(2,returned)
                accept=true;h.click("Open source");assertFalse(h.text().contains("could not be opened"))
                rows.add(mapOf("case_class" to kind,"state" to "unreachable_return","reference_id" to rid,"status" to "pass","mechanism" to "injected dispatch rejection; polite recovery, return and retry clear failure; not remote HTTP/offline measurement"))
            }
            var recovered=false
            h.scene.setContent { LearningTheme { SourceDetail(SourceReferenceId("REF-missing-10C"),{recovered=true},{},{false}) } }
            h.awaitCondition{h.text().contains("This source is unavailable.")};h.click("Sources");assertTrue(recovered)
            h.screenshot("missing-source-recovery")
            rows.add(mapOf("case_id" to "10C3-SUPPLEMENT-01","state" to "missing_source","status" to "pass","observed" to "Unavailable message and Sources recovery callback"))

            val document=readerDocuments.single{it.id.value=="M01-L01"}
            val firstSource=lessonSources(document).first()
            val route=canonicalResolver.canonical(ContentTarget(document.id))
            h.scene.setContent { LearningRoute(initialResolution=route,onExternal={false}) }
            h.awaitCondition{h.text().contains(document.title)}
            h.scrollTo(document.bodyBlocks.size+2)
            h.awaitCondition{h.text().contains(firstSource.title)}
            h.click(firstSource.title)
            h.awaitCondition{h.text().contains("Open source")}
            h.click("Open source");assertTrue(h.text().contains("could not be opened"))
            h.click("Return to reading")
            h.awaitCondition { h.nodes().any{n->n.config.getOrNull(SemanticsProperties.Text)?.any{it.text==firstSource.title}==true && n.config.getOrNull(SemanticsProperties.Focused)==true} }
            h.screenshot("reader-source-return-focus")
            rows.add(mapOf("case_id" to "10C3-SUPPLEMENT-02","state" to "reader_return","status" to "pass","origin" to document.id.value,"reference_id" to firstSource.id.value,"observed" to "Actual LearningRoute returns from rejected dispatch to the source row in original lesson with focus restored"))

            val question=acceptedQuestions9J.single{it.key.questionId.value=="reaction-20-0.5"}
            val snapshot=question.snapshot(ContentPackageIdentity("10C-review",Sha256("a".repeat(64))),kotlin.random.Random(10))
            val session=AssessmentSession(listOf(snapshot),Feedback.IMMEDIATE).answer(question.feedback.correctOptionId).next()
            var reviewSource by mutableStateOf<SourceReferenceId?>(null)
            var restoreSource by mutableStateOf<SourceReferenceId?>(null)
            val sourceId=question.relationship.sourceUses.first().referenceId
            val sourceTitle=navigationSources.references.single{it.id==sourceId}.title
            h.scene.setContent { LearningTheme { if(reviewSource==null) LearningAnswerReview(session,0,{}, {reviewSource=it},restoreSourceFocus=restoreSource) else SourceDetail(reviewSource!!,{restoreSource=reviewSource;reviewSource=null},{restoreSource=reviewSource;reviewSource=null},{false},backLabel="Back to answer review",returnLabel="Return to answer review") } }
            h.awaitCondition{h.text().contains(sourceTitle)};val before=h.text()
            h.click(sourceTitle);h.click("Open source");assertTrue(h.text().contains("could not be opened"));h.click("Return to answer review")
            h.awaitCondition{h.text().contains("Answer review") && h.nodes().any{n->n.config.getOrNull(SemanticsProperties.Text)?.any{it.text==sourceTitle}==true && n.config.getOrNull(SemanticsProperties.Focused)==true}}
            assertEquals(before,h.text());assertEquals(question.key,session.snapshots.single().question.key);assertEquals(1,session.score)
            h.screenshot("review-source-return-focus")
            rows.add(mapOf("case_id" to "10C3-SUPPLEMENT-03","state" to "review_component_return","status" to "pass","question_id" to question.key.questionId.value,"observed" to "Actual LearningAnswerReview and SourceDetail in verification owner preserve prompt/options/explanation, snapshot/score and restore source focus","limit" to "Component integration; production CurriculumApp navigation owner and native URI failures still require 10K"))
        }
        File(out,"desktop-source-observations.json").writeText(canonical(mapOf("task" to "10C3","target" to "desktop","surface" to "shared Compose/Skia JVM 1280x2048; injected dispatch","observations" to rows)))
    }
}
