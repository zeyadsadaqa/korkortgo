@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
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
import org.jetbrains.skia.Surface
import java.io.File
import kotlin.random.Random
import kotlin.test.*

/** Actual held records, projected as unscored fixtures. Never changes eligibility. */
class CandidateDelivery9JTest {
    @Test fun everyHeldCandidateLoadsAndReturnsFromEachImageWithoutRevealingOrLosingSelection() {
        val held=candidateQuestions9J.filter {it.acceptance.eligibility==ScoringEligibility.HELD}
        assertEquals(616,held.size)
        val rows=mutableListOf<String>()
        for(dark in listOf(false,true)) for(scale in listOf(1f,1.6f)) {
            var owner:SemanticsOwner?=null
            val listener=object:PlatformContext.SemanticsOwnerListener {
                override fun onSemanticsOwnerAppended(semanticsOwner:SemanticsOwner){owner=semanticsOwner}
                override fun onSemanticsOwnerRemoved(semanticsOwner:SemanticsOwner){owner=null}
                override fun onSemanticsChange(semanticsOwner:SemanticsOwner){}
                override fun onLayoutChange(semanticsOwner:SemanticsOwner,semanticsNodeId:Int){}
            }
            val scene=CanvasLayersComposeScene(size=IntSize(390,844),platformContext=object:PlatformContext by PlatformContext.Empty {override val semanticsOwnerListener=listener})
            val surface=Surface.makeRasterN32Premul(390,844);var frame=0L
            fun render(){Snapshot.sendApplyNotifications();repeat(4){scene.render(surface.canvas.asComposeCanvas(),++frame*16_666_667)}}
            fun nodes():List<SemanticsNode>{
                fun walk(n:SemanticsNode):List<SemanticsNode> = listOf(n)+n.children.flatMap{walk(it)}
                return walk(requireNotNull(owner).rootSemanticsNode)
            }
            fun text()=nodes().flatMap {it.config.getOrNull(SemanticsProperties.Text).orEmpty()}.joinToString(" | "){it.text}
            fun click(label:String){val n=nodes().first{it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text==label}==true && it.config.getOrNull(SemanticsActions.OnClick)!=null};assertTrue(n.config[SemanticsActions.OnClick].action!!.invoke());render()}
            fun key(k:Key){scene.sendKeyEvent(KeyEvent(k,KeyEventType.KeyDown));scene.sendKeyEvent(KeyEvent(k,KeyEventType.KeyUp));render()}
            fun awaitLoaded(condition:()->Boolean){repeat(300){render();if(condition())return;Thread.sleep(2)};error("Exact asset failed to load: see current test row")}
            var current by mutableStateOf(held.first().snapshot(candidateIdentity9J,Random(9)).presentation(null,false,true).copy(key=QuestionRevisionKey(QuestionId("delivery-initial"),SemanticRevision("fixture-r1"))))
            var loaded=mutableSetOf<AssetId>();var confirmed:OptionId?=null
            try {
                scene.setContent {CompositionLocalProvider(LocalDensity provides Density(1f,scale)) {
                    @Composable fun card(){key(current.key){AssessmentWithImageViewer(current,{confirmed=it},navigationAssets,onImageLoaded={id,ok->assertTrue(ok,"$id");loaded.add(id)},viewerHost={content,close->ImageViewerSurface(content,close)})}}
                    if(dark)MaterialTheme(colorScheme=darkColorScheme()){card()} else KorkortTheme {card()}
                }}
                for(q in held){
                    loaded=mutableSetOf();confirmed=null
                    current=q.snapshot(candidateIdentity9J,Random(9)).presentation(null,false,true)
                    val images=listOfNotNull(current.image)+current.choices.mapNotNull{it.image}
                    awaitLoaded {images.all{it.assetId in loaded}}
                    assertNull(current.explanation);assertNull(current.targetCode)
                    assertTrue(current.choices.all{it.correct==null && it.feedback==null})
                    assertFalse(text().contains("Correct answer"));assertFalse(text().contains(q.feedback.explanation.assessmentText()))
                    val radios=nodes().filter{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton}
                    assertEquals(4,radios.size)
                    assertTrue(radios[1].config[SemanticsActions.OnClick].action!!.invoke());render()
                    val labels=listOfNotNull(current.image?.let{"Enlarge question image"})+current.choices.filter{it.image!=null}.map{"Enlarge option ${it.letter} image"}
                    for(label in labels){
                        click(label);awaitLoaded {!text().contains("Loading image")}
                        assertTrue(text().contains("Question illustration"));assertFalse(text().contains("Correct answer"))
                        key(Key.Equals);assertTrue(text().contains("150%"));key(Key.DirectionRight);key(Key.Home);assertTrue(text().contains("100%"));key(Key.Escape)
                        val focused=nodes().single{it.config.getOrNull(SemanticsProperties.Focused)==true}
                        assertTrue(focused.config[SemanticsProperties.Text].any{it.text==label},"${q.key} return to $label")
                        assertEquals(1,nodes().count{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton && it.config.getOrNull(SemanticsProperties.Selected)==true})
                        assertNull(confirmed)
                    }
                    click("Confirm answer  >");assertEquals(current.choices[1].id,confirmed)
                    rows.add("{\"question_id\":\"${q.key.questionId.value}\",\"revision\":\"${q.key.revision.value}\",\"dark\":$dark,\"font_scale\":$scale,\"image_occurrences\":${images.size},\"zoom_returns\":${labels.size}}")
                }
            }finally{scene.close();surface.close()}
        }
        assertEquals(2464,rows.size)
        val file=File("build/verification/9J-followup/desktop-delivery.json");file.parentFile.mkdirs()
        file.writeText("{\"scope\":\"desktop Compose semantics and exact-resource loading; not native reader or visual legibility acceptance\",\"package\":\"${candidateIdentity9J}\",\"rows\":["+rows.joinToString(",\n")+"]}\n")
    }
}
