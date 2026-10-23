@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort
import androidx.compose.runtime.*
import androidx.compose.runtime.snapshots.Snapshot
import androidx.compose.ui.graphics.asComposeCanvas
import androidx.compose.ui.platform.PlatformContext
import androidx.compose.ui.scene.CanvasLayersComposeScene
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.IntSize
import org.jetbrains.skia.Surface
import org.jetbrains.skia.EncodedImageFormat
import java.nio.file.Files
import kotlin.test.*
internal class JourneyHarness11(val width:Int=390,val height:Int=844):AutoCloseable {
 private val owners=mutableListOf<SemanticsOwner>()
 private val listener=object:PlatformContext.SemanticsOwnerListener{
  override fun onSemanticsOwnerAppended(semanticsOwner:SemanticsOwner){owners.add(semanticsOwner)}
  override fun onSemanticsOwnerRemoved(semanticsOwner:SemanticsOwner){owners.remove(semanticsOwner)}
  override fun onSemanticsChange(semanticsOwner:SemanticsOwner){}
  override fun onLayoutChange(semanticsOwner:SemanticsOwner,semanticsNodeId:Int){}
 }
 val scene=CanvasLayersComposeScene(size=IntSize(width,height),platformContext=object:PlatformContext by PlatformContext.Empty{override val semanticsOwnerListener=listener})
 private val surface=Surface.makeRasterN32Premul(width,height);private var frame=0L
 fun render(){Snapshot.sendApplyNotifications();repeat(4){surface.canvas.clear(org.jetbrains.skia.Color.TRANSPARENT);scene.render(surface.canvas.asComposeCanvas(),++frame*16_666_667)}}
 fun nodes():List<SemanticsNode>{
  fun walk(n:SemanticsNode):List<SemanticsNode> = listOf(n)+n.children.flatMap(::walk)
  return owners.lastOrNull()?.rootSemanticsNode?.let(::walk).orEmpty()
 }
 fun texts()=nodes().flatMap{it.config.getOrNull(SemanticsProperties.Text).orEmpty()}.map{it.text}
 fun text()=nodes().joinToString(" | "){it.config.getOrNull(SemanticsProperties.Text).orEmpty().joinToString(" "){t->t.text}+it.config.getOrNull(SemanticsProperties.ContentDescription).orEmpty().joinToString(" ")}
 fun await(label:String,f:()->Boolean){repeat(200){render();if(f())return;Thread.sleep(5)};error("$label\n${text()}")}
 fun scroll(delta:Float):Boolean {val action=nodes().firstOrNull{it.config.getOrNull(SemanticsActions.ScrollBy)?.action!=null}?.config?.get(SemanticsActions.ScrollBy)?.action ?: return false;val moved=action.invoke(0f,delta);repeat(8){render()};return moved}
 fun reach(label:String) {
  if(nodes().any{it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text==label}==true && it.config.getOrNull(SemanticsActions.OnClick)?.action!=null})return
  scroll(-100000f)
  repeat(100){render();if(nodes().any{it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text==label}==true && it.config.getOrNull(SemanticsActions.OnClick)?.action!=null})return;scroll(450f)}
  error("Unreachable $label\n${text()}")
 }
 fun click(label:String){reach(label);val n=nodes().first{it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text==label}==true && it.config.getOrNull(SemanticsActions.OnClick)?.action!=null};assertTrue(n.config[SemanticsActions.OnClick].action!!.invoke());render()}
 fun capture(task:String,name:String){render();val p=Proof10J.root.resolve("docs/curriculum/app-migration/verification-evidence/$task/captures/$name.png");Files.createDirectories(p.parent);Files.write(p,surface.makeImageSnapshot().encodeToData(EncodedImageFormat.PNG)!!.bytes)}
 override fun close(){scene.close();surface.close()}
}
