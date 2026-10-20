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
class FaintComparison10DTest {
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
        fun screenshot(name:String) {repeat(20){render();Thread.sleep(5)};val f=root.resolve("docs/curriculum/app-migration/verification-evidence/10D2/comparisons/$name.png").toFile();f.parentFile.mkdirs();f.writeBytes(surface.makeImageSnapshot().encodeToData(EncodedImageFormat.PNG)!!.bytes)}
        override fun close() {scene.close();surface.close()}
    }


    @Test fun renderUnchangedFaintAssetsAtFrameAndViewerScale() {
        val ids=listOf("S5","S6","S7","S11","S12","S13","T1","T2","T6","T8","T22","X8")
        val rows=mutableListOf<Map<String,Any?>>()
        for(code in ids) {
            val q=acceptedQuestions9J.single{it.key.questionId.value=="sign-meaning-$code"}
            val image=q.snapshot(acceptedPracticeBank9J.identity,kotlin.random.Random(10)).presentation(null,false,true).image!!
            val asset=navigationAssets.single{it.id==image.assetId};var loaded=false
            Harness(354,236).use{h->
                h.scene.setContent { LearningTheme { ExactAssetImage(asset,image.description,androidx.compose.ui.Modifier.readableArtworkFrame(),onLoaded={loaded=it}) } }
                h.awaitCondition{loaded};h.screenshot("$code-frame")
            }
            Harness(390,844).use{h->
                h.scene.setContent { LearningTheme { ImageViewerSurface(ImageViewerContent.assessment(image,navigationAssets),{}) } }
                h.awaitCondition{!h.text().contains("Loading image")};h.key(Key.Equals);h.awaitCondition{h.text().contains("150%")};h.screenshot("$code-viewer150")
                h.key(Key.Home);assertTrue(h.text().contains("100%"))
            }
            rows.add(mapOf("asset_id" to image.assetId.value,"original_sha256" to asset.original.sha256.value,"bundled_sha256" to asset.bundled.sha256.value,"frame" to mapOf("width_dp" to 354,"height_dp" to 236,"density" to 1),"viewer" to mapOf("width_dp" to 390,"height_dp" to 844,"zoom_percent" to 150),"frame_capture" to "comparisons/$code-frame.png","viewer_capture" to "comparisons/$code-viewer150.png","status" to "rendered_shared_comparison_only"))
        }
        Files.writeString(root.resolve("docs/curriculum/app-migration/verification-evidence/10D2/comparison-observations.json"),canonical(mapOf("task" to "10D2","observations" to rows,"scope" to "Unchanged exact artwork; stand-alone 354x236 frame and 390x844 shared viewer, not a full-question or platform acceptance")))
    }
}
