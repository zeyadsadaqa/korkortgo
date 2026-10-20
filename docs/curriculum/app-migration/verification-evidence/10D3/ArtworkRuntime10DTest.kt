@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort

import androidx.compose.runtime.*
import androidx.compose.foundation.layout.fillMaxSize
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
class ArtworkRuntime10DTest {
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
        fun focusVisible(label:String) {
            val n=nodes().first {it.config.getOrNull(SemanticsProperties.Text)?.any{it.text==label}==true && it.config.getOrNull(SemanticsActions.OnClick)!=null}
            val request=n.config.getOrNull(SemanticsActions.RequestFocus)?.action
            if(request!=null) {assertTrue(request());awaitCondition{nodes().any{it.id==n.id && it.boundsInRoot.height>=47f && it.boundsInRoot.top>=0f && it.boundsInRoot.bottom<=844.5f}}}
        }
        fun scrollTo(index:Int) { val action=nodes().mapNotNull{it.config.getOrNull(SemanticsActions.ScrollToIndex)}.first().action!!;assertTrue(action(index));render() }
        fun key(key:Key) {scene.sendKeyEvent(KeyEvent(key,KeyEventType.KeyDown));scene.sendKeyEvent(KeyEvent(key,KeyEventType.KeyUp));render()}
        fun awaitCondition(condition:()->Boolean) {repeat(200) {render();if(condition())return;Thread.sleep(5)};error("Image decoding did not finish")}
        fun screenshot(name:String) {render();val f=root.resolve("docs/curriculum/app-migration/verification-evidence/10D3/captures/$name.png").toFile();f.parentFile.mkdirs();f.writeBytes(surface.makeImageSnapshot().encodeToData(EncodedImageFormat.PNG)!!.bytes)}
        override fun close() {scene.close();surface.close()}
    }


    @Test fun verifyAcceptedArtworkAcrossAllSharedContexts() {
        val questions=acceptedQuestions9J.filter{it.key.questionId.value.startsWith("sign-") && it.relationship.disposition!=QuestionDisposition.RETAIN}
        assertEquals(616,questions.size)
        val rows=mutableListOf<Map<String,Any?>>()
        val faint=setOf("S5","S6","S7","S11","S12","S13","T1","T2","T6","T8","T22","X8").map{"official/$it"}.toSet()
        for(dark in listOf(false,true))for(scale in listOf(1f,1.6f)) {
            val setting="${if(dark) "dark" else "light"}-${if(scale==1f) "100" else "160"}"
            Harness(390,844).use{h->
                var current by mutableStateOf(questions.first().snapshot(acceptedPracticeBank9J.identity,kotlin.random.Random(10)).presentation(null,false,true).copy(key=QuestionRevisionKey(QuestionId("10D-start"),SemanticRevision("fixture"))))
                var loaded=mutableSetOf<AssetId>();var confirmed:OptionId?=null
                h.scene.setContent { androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalDensity provides androidx.compose.ui.unit.Density(1f,scale)) {
                    LearningTheme { if(dark) androidx.compose.material3.MaterialTheme(colorScheme=androidx.compose.material3.darkColorScheme(),typography=androidx.compose.material3.MaterialTheme.typography) { androidx.compose.material3.Surface(androidx.compose.ui.Modifier.fillMaxSize(),color=androidx.compose.material3.MaterialTheme.colorScheme.background) {key(current.key){AssessmentWithImageViewer(current,{confirmed=it},navigationAssets,onImageLoaded={id,ok->assertTrue(ok,"$id");loaded.add(id)},viewerHost={content,close->ImageViewerSurface(content,close)})}} }
                    else key(current.key){AssessmentWithImageViewer(current,{confirmed=it},navigationAssets,onImageLoaded={id,ok->assertTrue(ok,"$id");loaded.add(id)},viewerHost={content,close->ImageViewerSurface(content,close)})}
                    }
                }}
                for(q in questions) {
                    loaded=mutableSetOf();confirmed=null
                    current=q.snapshot(acceptedPracticeBank9J.identity,kotlin.random.Random(10)).presentation(null,false,true)
                    val images=listOfNotNull(current.image)+current.choices.mapNotNull{it.image}
                    h.awaitCondition{images.all{it.assetId in loaded}}
                    val capture=q.relationship.disposition==QuestionDisposition.REPLACE
                    val prefix="${q.key.questionId.value}-$setting"
                    val allowed=(listOf(current.prompt,"A","B","C","D","Confirm answer  >","Enlarge question image")+current.choices.flatMap{listOf(it.text,"Enlarge option ${it.letter} image")}+images.map{it.description}).toSet()
                    val atoms=h.nodes().flatMap{n->n.config.getOrNull(SemanticsProperties.Text).orEmpty().map{it.text}+n.config.getOrNull(SemanticsProperties.ContentDescription).orEmpty()}.filter{it.isNotBlank()}
                    assertTrue(atoms.all{it in allowed},"Unexpected pre-answer semantics ${q.key}: ${atoms.filter{it !in allowed}}")
                    assertFalse(h.text().contains("official/"));assertFalse(h.text().contains("sign-recognise-"));assertFalse(h.text().contains("sign-meaning-"))
                    val radios=h.nodes().filter{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton}
                    assertEquals(4,radios.size);assertEquals(listOf("A","B","C","D"),radios.map{it.config[SemanticsProperties.Text].first().text})
                    if(capture)h.screenshot("$prefix-pre")
                    val chosen=radios[1];assertTrue(chosen.config[SemanticsActions.OnClick].action!!.invoke());h.render();assertNull(confirmed)
                    if(capture)h.screenshot("$prefix-pending")
                    val imageRows=mutableListOf<Map<String,Any?>>()
                    for((i,picture) in images.withIndex()) {
                        val label=if(current.image!=null && i==0)"Enlarge question image" else "Enlarge option ${current.choices.single{it.image==picture}.letter} image"
                        h.focusVisible(label)
                        val imageNode=h.nodes(true).first{it.config.getOrNull(SemanticsProperties.ContentDescription)?.contains(picture.description)==true && it.config.getOrNull(SemanticsProperties.Role)!=Role.RadioButton}
                        assertTrue(imageNode.size.height>=220,"Minimum artwork frame: ${q.key} ${picture.assetId} ${imageNode.size}")
                        val frame=mapOf("width_px" to imageNode.size.width,"height_px" to imageNode.size.height)
                        h.click(label);h.awaitCondition{!h.text().contains("Loading image")}
                        assertTrue(h.text().contains("Question illustration"));assertFalse(h.text().contains("Correct answer"))
                        val faintCapture=picture.assetId.value in faint
                        if(faintCapture)h.screenshot("$prefix-slot$i-fit")
                        h.key(Key.Equals);assertTrue(h.text().contains("150%"))
                        if(faintCapture)h.screenshot("$prefix-slot$i-zoom150")
                        h.key(Key.DirectionRight);h.key(Key.Home);assertTrue(h.text().contains("100%"));h.key(Key.Escape)
                        h.awaitCondition { h.nodes().any{it.config.getOrNull(SemanticsProperties.Focused)==true && it.config.getOrNull(SemanticsProperties.Text)?.any{it.text==label}==true} }
                        assertEquals(1,h.nodes().count{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton && it.config.getOrNull(SemanticsProperties.Selected)==true});assertNull(confirmed)
                        imageRows.add(mapOf("asset_id" to picture.assetId.value,"frame" to frame,"trigger" to label,"resource_loaded" to true,"zoom150_reset_close_focus_selection" to "pass","faint_captures" to if(faintCapture)listOf("captures/$prefix-slot$i-fit.png","captures/$prefix-slot$i-zoom150.png") else emptyList<String>()))
                    }
                    h.focusVisible("Confirm answer  >");h.click("Confirm answer  >");assertEquals(current.choices[1].id,confirmed)
                    rows.add(mapOf("case_id" to "T03-ART-desktop-${q.key.questionId.value}-$setting","question_id" to q.key.questionId.value,"revision" to q.key.revision.value,"setting" to setting,"displayed_option_ids" to current.choices.map{it.id.value},"selected_option_id" to confirmed!!.value,"pre_answer_semantic_projection" to "pass","radio_order" to listOf("A","B","C","D"),"images" to imageRows,"captures" to if(capture)listOf("captures/$prefix-pre.png","captures/$prefix-pending.png") else emptyList<String>(),"shared_runtime_status" to "pass","visual_signoff" to "pending_review_and_10K","modal_exclusion" to "not_proven_by_single_scene_viewer_seam"))
                    if(rows.size%100==0){File(root.resolve("docs/curriculum/app-migration/verification-evidence/10D3/runtime-progress.txt").toString()).writeText("${rows.size}/2464 contexts checked; $prefix\n")}
                }
            }
        }
        assertEquals(2464,rows.size)
        Files.writeString(root.resolve("docs/curriculum/app-migration/verification-evidence/10D3/shared-artwork-observations.json"),canonical(mapOf("task" to "10D3","surface" to "actual accepted question snapshots in shared Compose/Skia, 390x844 logical pixels, density 1; both themes, 1.0/1.6 text","package_identity" to acceptedPracticeBank9J.identity,"rows" to rows,"scope_limit" to "ViewerSurface seam; not native modal exclusion, assistive speech, production-owner journeys or independent visual signoff")))
    }
}
