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
class ReferenceVerification10BTest {
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
        fun key(key:Key) {scene.sendKeyEvent(KeyEvent(key,KeyEventType.KeyDown));scene.sendKeyEvent(KeyEvent(key,KeyEventType.KeyUp));render()}
        fun awaitCondition(condition:()->Boolean) {repeat(200) {render();if(condition())return;Thread.sleep(5)};error("Image decoding did not finish")}
        fun screenshot(name:String) {repeat(20){render();Thread.sleep(5)};val f=root.resolve("docs/curriculum/app-migration/verification-evidence/${System.getProperty("verificationTask")}/captures/$name.png").toFile();f.parentFile.mkdirs();f.writeBytes(surface.makeImageSnapshot().encodeToData(EncodedImageFormat.PNG)!!.bytes)}
        override fun close() {scene.close();surface.close()}
    }

    @Test fun verifyCompleteReferenceContent() {
        val out=root.resolve("docs/curriculum/app-migration/verification-evidence/10B13").toFile().apply{mkdirs()}
        val rows=mutableListOf<Map<String,Any?>>()
        Harness(1280,4096).use{h->
            for(sign in navigationSigns) {
                val asset=readerAssets.single{it.id==sign.assetId}
                h.scene.setContent{LearningTheme{SignReferenceDetail(sign,asset,navigationSources.references,{},{false})}}
                repeat(6){h.render()}
                val required=listOf(sign.code,sign.englishLabel,sign.officialNameSv,sign.caption.assessmentText(),asset.studyAltText,"Editorial English translation; not an official agency translation.")+sign.limitations
                val missing=required.filter{!h.text().contains(it)}
                h.click("Sources and artwork credits")
                val credits=asset.reuse.flatMap{listOf(it.credit,it.conditions)}
                val creditMissing=credits.filter{!h.text().contains(it)}
                rows.add(mapOf("id" to sign.id.value,"type" to "sign","missing" to missing,"missing_credits" to creditMissing,"passed" to (missing.isEmpty() && creditMissing.isEmpty())))
                if(sign.code in listOf("A1","B4","F31a","M1","T8","S1"))h.screenshot(sign.id.value)
            }
            for(group in navigationReferenceGroups) {
                val r=canonicalResolver.canonical(ContentTarget(group.id))
                h.scene.setContent{key(group.id){LearningRoute(initialResolution=r,onExternal={false})}}
                repeat(6){h.render()}
                val captions=group.bodyBlocks.flatMap{segments(it.payload)}
                val required=listOf(group.title)+group.entryIds.map{id->navigationSigns.single{it.id==id}.englishLabel}+captions
                val missing=required.filter{!h.text().contains(it)}
                rows.add(mapOf("id" to group.id.value,"type" to "reference_group","missing" to missing,"passed" to missing.isEmpty()))
            }
        }
        File(out,"reference-runtime.json").writeText(canonical(mapOf("task" to "10B13","target" to "shared desktop 1280x4096, actual SignReferenceDetail and LearningRoute groups","observations" to rows)))
        assertTrue(rows.all{it["passed"]==true},"Reference content omission; see reference-runtime.json")
    }
    private fun segments(p:BlockPayload):List<String> = when(p) {
        is BlockPayload.Paragraph->listOf(p.text.assessmentText())
        is BlockPayload.Heading->listOf(p.text.assessmentText())
        is BlockPayload.SignExamples->p.entryIds.flatMap{id->val sign=navigationSigns.single{it.id==id};listOf(sign.caption.assessmentText(),readerAssets.single{it.id==sign.assetId}.studyAltText)}
        else->emptyList()
    }
}
