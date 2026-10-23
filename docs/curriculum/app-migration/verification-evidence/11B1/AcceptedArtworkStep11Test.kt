@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.Surface
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.ui.Modifier
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
import org.jetbrains.skia.Surface as SkiaSurface
import java.io.File
import kotlin.random.Random
import kotlin.test.*

/** Current accepted records for the exact616 artwork IDs; unscored renderer contexts, not normal production journeys. */
class AcceptedArtworkStep11Test {
    @Test fun everyHeldCandidateLoadsAndReturnsFromEachImageWithoutRevealingOrLosingSelection() {
        val oldIds=candidateQuestions9J.filter{it.acceptance.eligibility==ScoringEligibility.HELD}.map{it.key.questionId}.toSet()
        val held=acceptedQuestions9J.filter{it.key.questionId in oldIds}
        assertEquals(616,held.size)
        val runRoot=Proof10J.root.resolve("docs/curriculum/app-migration/verification-evidence/11D1").toFile().apply{mkdirs()}
        val fingerprint=requireNotNull(System.getenv("STEP11_INPUT_FINGERPRINT")) {"Run through the checkpoint-aware step11 runner"}
        val identityFile=File(runRoot,"checkpoint-input.txt")
        if(identityFile.exists())assertEquals(fingerprint,identityFile.readText(),"Never reuse artwork checkpoints after changed inputs") else identityFile.writeText(fingerprint)
        val checkpoint=File(runRoot,"checkpoint.jsonl")
        val rows=if(checkpoint.exists())checkpoint.readLines().filter{it.isNotBlank()}.toMutableList() else mutableListOf<String>()
        for(width in listOf(390)) for(dark in listOf(false,true)) for(scale in listOf(1f,1.6f)) {
            var owner:SemanticsOwner?=null
            val listener=object:PlatformContext.SemanticsOwnerListener {
                override fun onSemanticsOwnerAppended(semanticsOwner:SemanticsOwner){owner=semanticsOwner}
                override fun onSemanticsOwnerRemoved(semanticsOwner:SemanticsOwner){owner=null}
                override fun onSemanticsChange(semanticsOwner:SemanticsOwner){}
                override fun onLayoutChange(semanticsOwner:SemanticsOwner,semanticsNodeId:Int){}
            }
            val scene=CanvasLayersComposeScene(size=IntSize(width,844),platformContext=object:PlatformContext by PlatformContext.Empty {override val semanticsOwnerListener=listener})
            val surface=SkiaSurface.makeRasterN32Premul(width,844);var frame=0L
            fun render(){Snapshot.sendApplyNotifications();repeat(4){surface.canvas.clear(org.jetbrains.skia.Color.TRANSPARENT);scene.render(surface.canvas.asComposeCanvas(),++frame*16_666_667)}}
            fun nodes():List<SemanticsNode>{
                fun walk(n:SemanticsNode):List<SemanticsNode> = listOf(n)+n.children.flatMap{walk(it)}
                return walk(requireNotNull(owner).rootSemanticsNode)
            }
            fun text()=nodes().flatMap {it.config.getOrNull(SemanticsProperties.Text).orEmpty()}.joinToString(" | "){it.text}
            fun click(label:String){val n=nodes().first{it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text==label}==true && it.config.getOrNull(SemanticsActions.OnClick)!=null};assertTrue(n.config[SemanticsActions.OnClick].action!!.invoke());render()}
            fun key(k:Key){scene.sendKeyEvent(KeyEvent(k,KeyEventType.KeyDown));scene.sendKeyEvent(KeyEvent(k,KeyEventType.KeyUp));render()}
            fun awaitLoaded(condition:()->Boolean){repeat(300){render();if(condition())return;Thread.sleep(2)};error("Exact asset failed to load: see current test row")}
            var current by mutableStateOf(held.first().snapshot(acceptedIdentity9J,Random(9)).presentation(null,false,true).copy(key=QuestionRevisionKey(QuestionId("delivery-initial"),SemanticRevision("fixture-r1"))))
            var loaded=mutableSetOf<AssetId>();var confirmed:OptionId?=null
            val captureRoot=Proof10J.root.resolve("docs/curriculum/app-migration/verification-evidence/11D1/captures").toFile().apply{mkdirs()}
            fun capture(name:String){render();File(captureRoot,name+".png").writeBytes(surface.makeImageSnapshot().encodeToData(org.jetbrains.skia.EncodedImageFormat.PNG)!!.bytes)}
            try {
                scene.setContent {CompositionLocalProvider(LocalDensity provides Density(1f,scale)) {
                    @Composable fun card(){key(current.key){AssessmentWithImageViewer(current,{confirmed=it},navigationAssets,onImageLoaded={id,ok->assertTrue(ok,"$id");loaded.add(id)},viewerHost={content,close->ImageViewerSurface(content,close)})}}
                    LearningTheme {if(dark)MaterialTheme(colorScheme=darkColorScheme()){Surface(Modifier.fillMaxSize()){card()}} else card()}
                }}
                for(q in held){
                    if(rows.any {it.contains("\"question_id\":\"${q.key.questionId.value}\"") && it.contains("\"width\":$width,") && it.contains("\"dark\":$dark,") && it.contains("\"font_scale\":$scale,")})continue
                    loaded=mutableSetOf();confirmed=null
                    current=q.snapshot(acceptedIdentity9J,Random(9)).presentation(null,false,true)
                    val images=listOfNotNull(current.image)+current.choices.mapNotNull{it.image}
                    awaitLoaded {images.all{it.assetId in loaded}}
                    assertNull(current.explanation);assertNull(current.targetCode)
                    assertTrue(current.choices.all{it.correct==null && it.feedback==null})
                    assertFalse(text().contains("Correct answer"));assertFalse(text().contains(q.feedback.explanation.assessmentText()))
                    capture("${q.key.questionId.value}-$width-$dark-$scale-pre-answer")
                    val radios=nodes().filter{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton}
                    assertEquals(4,radios.size)
                    assertTrue(radios[1].config[SemanticsActions.RequestFocus].action!!.invoke());render()
                    assertTrue(radios[1].config[SemanticsActions.OnClick].action!!.invoke());render()
                    awaitLoaded {nodes().any{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton && it.config.getOrNull(SemanticsProperties.Selected)==true && it.boundsInRoot.height>0}}
                    assertEquals(1,nodes().count{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton && it.config.getOrNull(SemanticsProperties.Selected)==true})
                    capture("${q.key.questionId.value}-$width-$dark-$scale-pending")
                    val labels=listOfNotNull(current.image?.let{"Enlarge question image"})+current.choices.filter{it.image!=null}.map{"Enlarge option ${it.letter} image"}
                    for(label in labels){
                        click(label);awaitLoaded {!text().contains("Loading image")}
                        assertTrue(text().contains("Question illustration"));assertFalse(text().contains("Correct answer"))
                        key(Key.Equals);assertTrue(text().contains("150%"));capture("${q.key.questionId.value}-$width-$dark-$scale-${label.replace(' ','_')}-zoom");key(Key.DirectionRight);key(Key.Home);assertTrue(text().contains("100%"));key(Key.Escape)
                        val focused=nodes().single{it.config.getOrNull(SemanticsProperties.Focused)==true}
                        assertTrue(focused.config[SemanticsProperties.Text].any{it.text==label},"${q.key} return to $label")
                        assertEquals(1,nodes().count{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton && it.config.getOrNull(SemanticsProperties.Selected)==true})
                        assertNull(confirmed)
                    }
                    click("Confirm answer  >");assertEquals(current.choices[1].id,confirmed)
                    rows.add("{\"question_id\":\"${q.key.questionId.value}\",\"revision\":\"${q.key.revision.value}\",\"width\":$width,\"height\":844,\"dark\":$dark,\"font_scale\":$scale,\"image_occurrences\":${images.size},\"zoom_returns\":${labels.size}}")
                    checkpoint.appendText(rows.last()+"\n")
                }
            }finally{scene.close();surface.close()}
        }
        assertEquals(2464,rows.size)
        val file=File("../docs/curriculum/app-migration/verification-evidence/11D1/result.json");file.parentFile.mkdirs()
        file.writeText("{\"scope\":\"Current accepted artwork contexts;390x844 logical viewport, neutral selection, exact resources, focus-return and captures. Visual review is separately recorded; no native bridge/normal-journey claim.\",\"package\":\"${acceptedIdentity9J}\",\"rows\":["+rows.joinToString(",\n")+"]}\n")
    }
}
