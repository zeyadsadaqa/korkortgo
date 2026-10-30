@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.runtime.snapshots.Snapshot
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.asComposeCanvas
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.PlatformContext
import androidx.compose.ui.scene.CanvasLayersComposeScene
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.Density
import androidx.compose.ui.unit.IntSize
import org.jetbrains.skia.Surface
import kotlin.test.*

class NavigationUiTest {
    @Test fun navigationAdaptsAndExposesItsSelectedDestination() {
        for(width in listOf(320,390,840,1280)) for(scale in listOf(1f,1.6f)) {
            var owner: SemanticsOwner?=null
            val listener=object:PlatformContext.SemanticsOwnerListener {
                override fun onSemanticsOwnerAppended(o:SemanticsOwner){owner=o}
                override fun onSemanticsOwnerRemoved(o:SemanticsOwner){owner=null}
                override fun onSemanticsChange(o:SemanticsOwner){}
                override fun onLayoutChange(o:SemanticsOwner,id:Int){}
            }
            val scene=CanvasLayersComposeScene(size=IntSize(width,1000),platformContext=object:PlatformContext by PlatformContext.Empty{override val semanticsOwnerListener=listener})
            val surface=Surface.makeRasterN32Premul(width,1000)
            var frame=0L
            var destination by mutableStateOf<AppDestination>(AppDestination.Library)
            fun render(){Snapshot.sendApplyNotifications();repeat(5){scene.render(surface.canvas.asComposeCanvas(),++frame*16_666_667)}}
            fun nodes():List<SemanticsNode> {
                fun walk(n:SemanticsNode):List<SemanticsNode> = listOf(n)+n.children.flatMap(::walk)
                return owner?.rootSemanticsNode?.let(::walk).orEmpty()
            }
            try {
                scene.setContent {
                    CompositionLocalProvider(LocalDensity provides Density(1f,scale)) {LearningTheme {
                        AppChrome(destination,{destination=when(it){StudyTab.HOME->AppDestination.Home;StudyTab.LEARNING->AppDestination.Library;StudyTab.EXERCISE->AppDestination.QuizSetup}},false,{}) {Box(Modifier.weight(1f)){Text("Content")}}
                    }}
                }
                render()
                for(label in listOf("Home","Learning","Exercise")) {
                    val candidates=nodes().filter { it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text==label}==true }
                    assertTrue(candidates.isNotEmpty(),"$label missing at $width / $scale")
                    val clickable=candidates.first {it.config.getOrNull(SemanticsActions.OnClick)?.action!=null}
                    val box=clickable.boundsInRoot
                    assertTrue(box.width>0 && box.height>0)
                    if(width<840)assertTrue(box.top>700,"Compact navigation must be at the bottom")
                    else assertTrue(box.left<100,"Wide navigation must be in the rail")
                    assertTrue(clickable.config[SemanticsActions.OnClick].action!!.invoke());render()
                    assertEquals(label,tabFor(destination).label)
                }
            } finally {scene.close();surface.close()}
        }
    }
}
