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

class ReferenceViewerSemanticsTest {
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
        fun awaitLoaded() {repeat(100) {render();if(!text().contains("Loading image"))return;Thread.sleep(5)};error("Image did not finish loading")}
        fun recordImageBounds(description:String,name:String) {
            val node=nodes(true).first {it.config.getOrNull(SemanticsProperties.ContentDescription)?.contains(description)==true && it.config.getOrNull(SemanticsProperties.Role)!=Role.RadioButton}
            val b=node.boundsInRoot
            val f=File("build/verification/9L10/$name-bounds.json");f.parentFile.mkdirs()
            f.writeText("{\"left\":${b.left},\"top\":${b.top},\"right\":${b.right},\"bottom\":${b.bottom}}")
            screenshot(name)
            val bitmap=javax.imageio.ImageIO.read(File("build/verification/9L10/$name.png"))
            var painted=0
            for(y in b.top.toInt() until b.bottom.toInt())for(x in b.left.toInt() until b.right.toInt()) {
                val pixel=bitmap.getRGB(x,y)
                if((pixel ushr 24)>0 && (pixel and 255)<220)painted++
            }
            assertEquals(105f,b.height)
            assertTrue(painted>100,"The image has semantics but no painted artwork: $painted pixels")
            File("build/verification/9L10/$name-pixels.json").writeText("{\"painted_pixels\":$painted,\"height_px\":${b.height}}")
        }
        fun screenshot(name:String) {val f=File("build/verification/9L10/$name.png");f.parentFile.mkdirs();f.writeBytes(surface.makeImageSnapshot().encodeToData(EncodedImageFormat.PNG)!!.bytes)}
        override fun close() {scene.close();surface.close()}
    }
    @Test fun b1DetailUsesExactCaptionSourceAndReturnsFocusAfterZoom() {
        Harness(1000,1000).use {h->
            val sign=navigationSigns.single {it.code=="B1"};val asset=navigationAssets.single {it.id==sign.assetId}
            var back=false
            h.scene.setContent {KorkortTheme {SignReferenceDetail(sign,asset,navigationSources.references,{back=true},{false},viewerHost={content,close->ImageViewerSurface(content,close)})}}
            h.awaitLoaded()
            assertTrue(h.text().contains("Väjningsplikt"));assertTrue(h.text().contains("With a distance or stop-ahead panel"))
            assertTrue(h.text().contains("not an official agency translation"))
            h.screenshot("b1-detail-wide")
            h.click("Official description");assertTrue(h.text().contains("Could not open"))
            h.click("Enlarge image");h.awaitLoaded()
            assertTrue(h.text().contains("100%"));assertFalse(h.text().contains("With a distance or stop-ahead panel"))
            h.key(Key.Equals);assertTrue(h.text().contains("150%"))
            h.click("Reset");assertTrue(h.text().contains("100%"))
            h.key(Key.Escape);assertTrue(h.text().contains("With a distance or stop-ahead panel"))
            val focused=h.nodes().single {it.config.getOrNull(SemanticsProperties.Focused)==true}
            assertTrue(focused.config[SemanticsProperties.Text].any {it.text=="Enlarge image"})
            assertFalse(back)
        }
    }
    @Test fun neutralS1ViewerSupportsKeyboardAndLargeTextOnLightAndDarkSurfaces() {
        for(dark in listOf(false,true)) Harness(360,780).use {h->
            val picture=AssessmentImagePresentation(AssetId("official/S1"),"A thin dark outline of a rectangular vehicle body with a cab and three circular wheels.")
            val content=ImageViewerContent.assessment(picture,navigationAssets)
            var closed=false
            h.scene.setContent {CompositionLocalProvider(LocalDensity provides Density(1f,1.6f)) {MaterialTheme(colorScheme=if(dark) darkColorScheme() else lightColorScheme()) {ImageViewerSurface(content) {closed=true}}}}
            h.awaitLoaded()
            assertTrue(h.text().contains(picture.description));assertFalse(h.text().contains("Heavy goods"));assertFalse(h.text().contains("S1"))
            assertTrue(h.text().contains("100%"));h.screenshot(if(dark) "s1-viewer-dark-fit" else "s1-viewer-light-fit");h.key(Key.Equals);assertTrue(h.text().contains("150%"))
            h.key(Key.DirectionRight);h.key(Key.DirectionDown)
            h.screenshot(if(dark) "s1-viewer-dark-large-text" else "s1-viewer-light-large-text")
            h.key(Key.Home);assertTrue(h.text().contains("100%"))
            for(label in listOf("Close","Zoom in","Zoom out","Reset")) {
                val n=h.nodes().first {it.config.getOrNull(SemanticsProperties.Text)?.any {it.text==label}==true && it.config.getOrNull(SemanticsActions.OnClick)!=null}
                assertTrue(n.boundsInRoot.height>=48f)
                assertTrue(n.boundsInRoot.bottom<=780f && n.boundsInRoot.top>=0f)
            }
            h.key(Key.Escape);assertTrue(closed)
        }
    }
    @Test fun assessmentZoomPreservesPendingChoiceAndDoesNotRevealMeaning() {
        Harness(800,1500).use {h->
            val picture=AssessmentImagePresentation(AssetId("official/S1"),"A thin rectangular outline with circular wheels.")
            val choices=(1..4).map {n->AssessmentChoicePresentation(OptionId("fixture-$n"),('A'+n-1).toString(),"",picture,false,null,null)}
            val p=AssessmentPresentation(QuestionRevisionKey(QuestionId("unscored-fixture"),SemanticRevision("test")),"Which picture?",null,choices,true,null,null,null)
            var confirmed:OptionId?=null
            var decoded=0
            h.scene.setContent {KorkortTheme {AssessmentWithImageViewer(p,{confirmed=it},navigationAssets,onImageLoaded={_,ok->assertTrue(ok);decoded++},viewerHost={content,close->ImageViewerSurface(content,close)})}}
            h.awaitCondition {decoded==4}
            h.render()
            h.recordImageBounds(picture.description,"assessment-min-height")
            val radio=h.nodes().first {it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton}
            assertTrue(radio.config[SemanticsActions.OnClick].action!!.invoke());h.render()
            h.click("Enlarge option B image");h.awaitLoaded()
            assertFalse(h.text().contains("Heavy goods"));assertFalse(h.text().contains("S1"))
            h.key(Key.Escape)
            assertTrue(h.nodes().first {it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton}.config[SemanticsProperties.Selected])
            assertNull(confirmed)
            h.click("Confirm answer  >");assertEquals(OptionId("fixture-1"),confirmed)
        }
    }

}
