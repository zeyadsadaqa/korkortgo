@file:OptIn(org.jetbrains.compose.resources.ExperimentalResourceApi::class)
package se.korkort

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.clipRect
import androidx.compose.ui.graphics.drawscope.withTransform
import androidx.compose.ui.graphics.painter.BitmapPainter
import androidx.compose.ui.graphics.painter.Painter
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.semantics.*
import org.jetbrains.compose.resources.decodeToImageBitmap
import se.korkort.resources.Res
import kotlin.coroutines.cancellation.CancellationException

internal class ExactVectorPainter(private val drawing: ExactVectorPicture): Painter() {
    override val intrinsicSize=Size(drawing.width,drawing.height)
    override fun androidx.compose.ui.graphics.drawscope.DrawScope.onDraw() { drawing.draw(this) }
}

internal suspend fun loadExactAsset(asset: CurriculumAsset): Painter {
    require(asset.bundled.sha256==asset.original.sha256)
    val prefix="composeApp/src/commonMain/composeResources/"
    require(asset.bundled.path.startsWith(prefix))
    val bytes=Res.readBytes(asset.bundled.path.removePrefix(prefix))
    require(assetSha256(bytes)==asset.bundled.sha256) { "Artwork integrity check failed" }
    return if(asset.bundled.path.endsWith(".pdf")) {
        val vector=requireNotNull(decodedOfficialVector(asset.bundled.sha256)) {"This PDF has no verified shared decoder yet"}
        require(vector.sourceSha256==asset.bundled.sha256) { "This PDF has no verified shared decoder yet" }
        ExactVectorPainter(vector)
    } else BitmapPainter(bytes.decodeToImageBitmap())
}

/** Complete image at fit; zoom clips only the viewport. The source path/colour is never altered. */
@Composable
fun ExactAssetImage(
    asset: CurriculumAsset,
    description: String,
    modifier: Modifier = Modifier,
    viewport: ImageViewport = ImageViewport(),
    onViewportChange: (ImageViewport) -> Unit = {},
    onLoaded: (Boolean) -> Unit = {},
    onGeometry: (Size, Size) -> Unit = { _, _ -> },
) {
    var painter by remember(asset.bundled) { mutableStateOf<Painter?>(null) }
    var failed by remember(asset.bundled) { mutableStateOf(false) }
    var width by remember { mutableStateOf(0f) };var height by remember { mutableStateOf(0f) }
    val loadedCallback by rememberUpdatedState(onLoaded)
    LaunchedEffect(asset.bundled) {
        try { painter=loadExactAsset(asset);loadedCallback(true) }
        catch(cancelled: CancellationException) { throw cancelled }
        catch(_: Exception) { failed=true;loadedCallback(false) }
    }
    val p=painter
    val geometryCallback by rememberUpdatedState(onGeometry)
    LaunchedEffect(p,width,height) { if(p!=null && width>0 && height>0) geometryCallback(p.intrinsicSize,Size(width,height)) }
    val liveViewport by rememberUpdatedState(viewport)
    val liveViewportChange by rememberUpdatedState(onViewportChange)
    BoxWithConstraints(modifier.background(Color.White).onSizeChanged { width=it.width.toFloat();height=it.height.toFloat() }
        .semantics { contentDescription=description;role=Role.Image }
        .pointerInput(p,viewport.zoom>1f,width,height) {
            if(p!=null && width>0 && height>0 && viewport.zoom>1f) detectDragGestures { change,delta ->
                change.consume()
                liveViewportChange(liveViewport.copy(pan=liveViewport.pan+delta).clamp(p.intrinsicSize.width,p.intrinsicSize.height,width,height))
            }
        }, propagateMinConstraints = true) {
        // Canvas uses Spacer measurement: an unbounded max height must become a fixed
        // height, otherwise its drawing size can be zero despite the parent's minimum.
        if(p!=null) Canvas(if(constraints.hasBoundedHeight) Modifier.fillMaxSize() else Modifier.fillMaxWidth().height(minHeight)) {
            if(size.width>0 && size.height>0) {
                val source=p.intrinsicSize
                val v=viewport.clamp(source.width,source.height,size.width,size.height)
                val scale=v.fit(source.width,source.height,size.width,size.height)*v.zoom
                clipRect {
                    withTransform({
                        translate((size.width-source.width*scale)/2f+v.pan.x,(size.height-source.height*scale)/2f+v.pan.y)
                        scale(scale,scale,pivot=Offset.Zero)
                    }) { with(p) { draw(source) } }
                }
            }
        }
        else Text(if(failed) "Image unavailable. Return and try again." else "Loading image…",color=Color(0xFF172C29))
    }
}
