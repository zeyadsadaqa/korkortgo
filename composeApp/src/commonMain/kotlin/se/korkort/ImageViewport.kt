package se.korkort

import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathFillType
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.clipRect
import androidx.compose.ui.graphics.drawscope.withTransform
import kotlin.math.min

/** Pure geometry: source coordinates remain unchanged; fit and zoom use one uniform scale. */
data class ImageViewport(val zoom: Float = 1f, val pan: Offset = Offset.Zero) {
    init { require(zoom.isFinite() && zoom in 1f..8f); require(pan.x.isFinite() && pan.y.isFinite()) }
    fun fit(imageWidth: Float, imageHeight: Float, width: Float, height: Float): Float {
        require(listOf(imageWidth,imageHeight,width,height).all { it.isFinite() && it > 0f })
        return min(width/imageWidth,height/imageHeight)
    }
    fun bounds(imageWidth: Float, imageHeight: Float, width: Float, height: Float): Offset {
        val scale=fit(imageWidth,imageHeight,width,height)*zoom
        return Offset(((imageWidth*scale-width)/2f).coerceAtLeast(0f),((imageHeight*scale-height)/2f).coerceAtLeast(0f))
    }
    fun clamp(imageWidth: Float, imageHeight: Float, width: Float, height: Float): ImageViewport {
        val b=bounds(imageWidth,imageHeight,width,height)
        return copy(pan=Offset(if(b.x==0f) 0f else pan.x.coerceIn(-b.x,b.x),if(b.y==0f) 0f else pan.y.coerceIn(-b.y,b.y)))
    }
    fun zoomTo(value: Float) = copy(zoom=value.coerceIn(1f,8f))
    fun reset() = ImageViewport()
}

/** Decoded PDF display list, bound to the original PDF hash. No authored replacement artwork. */
internal data class ExactVectorDrawing(val sourceSha256: Sha256, val width: Float, val height: Float, val clip: Rect, val strokeWidth: Float, val colour: Color, val path: Path, val fill: Boolean = false, val evenOdd: Boolean = false) {
    fun draw(scope: DrawScope) = with(scope) {
        clipRect(clip.left,clip.top,clip.right,clip.bottom) {
            if(fill) {path.fillType=if(evenOdd) PathFillType.EvenOdd else PathFillType.NonZero;drawPath(path,colour)}
            else drawPath(path,colour,style=Stroke(width=strokeWidth,cap=StrokeCap.Round,join=StrokeJoin.Round))
        }
    }
}

internal data class ExactVectorPicture(val sourceSha256: Sha256, val width: Float, val height: Float, val layers: List<ExactVectorDrawing>) {
    fun draw(scope: DrawScope) {layers.forEach {it.draw(scope)}}
}
