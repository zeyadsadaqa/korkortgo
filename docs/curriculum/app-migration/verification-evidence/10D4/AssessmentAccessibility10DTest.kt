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
class AssessmentAccessibility10DTest {
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
        fun screenshot(name:String) {render();val f=root.resolve("docs/curriculum/app-migration/verification-evidence/10D4/captures/$name.png").toFile();f.parentFile.mkdirs();f.writeBytes(surface.makeImageSnapshot().encodeToData(EncodedImageFormat.PNG)!!.bytes)}
        override fun close() {scene.close();surface.close()}
    }


    @Test fun keyboardAndRevealGatesUseAcceptedQuestionIdentity() {
        val ids=listOf("situation-001","situation-017","situation-103","fuel-saving-150-1.5","sign-meaning-A1","sign-recognise-A1","sign-meaning-M17a","sign-recognise-M17a","sign-recognise-S5","sign-meaning-X8")
        val rows=mutableListOf<Map<String,Any?>>()
        for(width in listOf(390,320))for(dark in listOf(false,true))for(scale in listOf(1f,1.6f))for(mode in Feedback.entries)for(id in ids) {
            val q=acceptedQuestions9J.single{it.key.questionId.value==id}
            val snapshot=q.snapshot(acceptedPracticeBank9J.identity,kotlin.random.Random(10));var session by mutableStateOf(AssessmentSession(listOf(snapshot),mode))
            Harness(width,844).use {h->
                var loaded=mutableSetOf<AssetId>()
                h.scene.setContent { CompositionLocalProvider(androidx.compose.ui.platform.LocalDensity provides androidx.compose.ui.unit.Density(1f,scale)) {
                    LearningTheme { androidx.compose.material3.MaterialTheme(colorScheme=if(dark)androidx.compose.material3.darkColorScheme() else androidx.compose.material3.MaterialTheme.colorScheme,typography=androidx.compose.material3.MaterialTheme.typography) {
                        androidx.compose.material3.Surface(androidx.compose.ui.Modifier.fillMaxSize(),color=androidx.compose.material3.MaterialTheme.colorScheme.background) {
                            AssessmentWithImageViewer(session.presentation(),{session=session.answer(it)},navigationAssets,onImageLoaded={asset,ok->assertTrue(ok);loaded.add(asset)},viewerHost={content,close->ImageViewerSurface(content,close)})
                        }
                    }}
                }}
                val pictures=listOfNotNull(q.image)+q.options.mapNotNull{it.image};h.awaitCondition{pictures.all{it.assetId in loaded}}
                assertNull(session.currentAnswer);assertNull(session.presentation().explanation);assertFalse(h.text().contains("Correct answer"))
                val radios=h.nodes().filter{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton};assertEquals(4,radios.size)
                val first=radios.first();assertTrue(first.config[SemanticsActions.RequestFocus].action!!.invoke());h.render();h.key(Key.Spacebar)
                assertNull(session.currentAnswer);assertEquals(1,h.nodes().count{it.config.getOrNull(SemanticsProperties.Selected)==true})
                val expected=mutableListOf<String>()
                for((index,choice) in session.presentation().choices.withIndex()) {if(index!=0)expected.add(choice.letter);if(choice.image!=null)expected.add("Enlarge option ${choice.letter} image")}
                expected.add("Confirm answer  >")
                val actual=mutableListOf<String>()
                for(label in expected){h.key(Key.Tab);h.awaitCondition{h.nodes().any{it.config.getOrNull(SemanticsProperties.Focused)==true}};val focus=h.nodes().single{it.config.getOrNull(SemanticsProperties.Focused)==true};val texts=focus.config.getOrNull(SemanticsProperties.Text).orEmpty().map{it.text};assertTrue(label in texts,"$id $mode expected Tab to $label, got $texts");actual.add(label)}
                h.key(Key.Enter);h.awaitCondition{session.currentAnswer!=null}
                assertEquals(snapshot.displayedOptionIds.first(),session.currentAnswer!!.selectedOptionId)
                assertTrue(h.nodes().filter{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton}.all{it.config.contains(SemanticsProperties.Disabled)})
                assertTrue(h.nodes().any{it.config.getOrNull(SemanticsProperties.LiveRegion)==LiveRegionMode.Polite})
                val immediate=mode==Feedback.IMMEDIATE
                assertEquals(immediate,session.presentation().explanation!=null);assertEquals(immediate,h.text().contains("Correct answer"))
                if(!immediate){assertTrue(h.text().contains("Answer saved."));session=session.next();h.awaitCondition{h.text().contains("Correct answer")}}
                assertEquals(q.key,session.snapshots.single().question.key);assertEquals(snapshot.displayedOptionIds,session.snapshots.single().displayedOptionIds)
                rows.add(mapOf("viewport_width_logical_px" to width,"viewport_height_logical_px" to 844,"question_id" to id,"revision" to q.key.revision.value,"mode" to mode.name,"theme" to if(dark)"dark" else "light","font_scale" to scale,"tab_order" to actual,"selected_authored_option_id" to session.currentAnswer!!.selectedOptionId.value,"keyboard_selection_confirmation" to "pass","feedback_gate_disabled_radios_polite_region" to "pass","snapshot_identity" to "pass","visual_selection_indicator" to "requires_affected_component_retest_DEF-10D-001","modality_scope" to "Shared desktop keyboard and node observations; no assistive speech or native modal exclusion proof"))
            }
        }
        assertEquals(160,rows.size)
        Files.writeString(root.resolve("docs/curriculum/app-migration/verification-evidence/10D4/shared-accessibility-observations.json"),canonical(mapOf("task" to "10D4","observations" to rows,"package_identity" to acceptedPracticeBank9J.identity)))
    }
}
