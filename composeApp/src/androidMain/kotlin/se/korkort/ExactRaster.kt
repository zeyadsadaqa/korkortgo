@file:OptIn(org.jetbrains.compose.resources.ExperimentalResourceApi::class)
package se.korkort

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.BitmapRegionDecoder
import android.graphics.Paint
import android.graphics.Rect
import android.graphics.RectF
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.drawIntoCanvas
import androidx.compose.ui.graphics.nativeCanvas
import androidx.compose.ui.graphics.painter.BitmapPainter
import androidx.compose.ui.graphics.painter.Painter
import org.jetbrains.compose.resources.decodeToImageBitmap
import kotlin.math.max

internal actual fun decodeExactRaster(bytes: ByteArray): Painter {
    val bounds=BitmapFactory.Options().apply{inJustDecodeBounds=true}
    BitmapFactory.decodeByteArray(bytes,0,bytes.size,bounds)
    require(bounds.outWidth>0 && bounds.outHeight>0)
    // Hardware Canvas rejects a single bitmap above its allocation limit, even
    // when it would be scaled down. Keep ordinary assets on the existing path.
    return if(bounds.outWidth.toLong()*bounds.outHeight>16_000_000L || max(bounds.outWidth,bounds.outHeight)>8192)
        ExactRegionPainter(bytes,bounds.outWidth,bounds.outHeight)
    else BitmapPainter(bytes.decodeToImageBitmap())
}

/** Original pixels at native zoom; bounded decoded regions at fit. No derived asset file. */
@Suppress("DEPRECATION")
private class ExactRegionPainter(bytes: ByteArray,width: Int,height: Int): Painter(), RasterResolutionAwarePainter {
    private val sourceWidth=width
    private val sourceHeight=height
    private val decoder=requireNotNull(BitmapRegionDecoder.newInstance(bytes,0,bytes.size,false))
    private data class Tile(val sample: Int,val x: Int,val y: Int)
    private val cache=linkedMapOf<Tile,Bitmap>()
    private val paint=Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG)
    override val intrinsicSize=Size(width.toFloat(),height.toFloat())
    private var rasterScale=1f
    override fun setRasterScale(scale: Float) { require(scale.isFinite() && scale>0f);rasterScale=scale }
    override fun DrawScope.onDraw() = drawIntoCanvas {canvas->
        val native=canvas.nativeCanvas
        var sample=1
        while(sample<32 && sample*2*rasterScale<=1f)sample*=2
        val span=1024*sample
        var y=0
        while(y<sourceHeight) {
            var x=0
            while(x<sourceWidth) {
                val region=Rect(x,y,(x+span).coerceAtMost(sourceWidth),(y+span).coerceAtMost(sourceHeight))
                val target=RectF(region)
                if(!native.quickReject(target,android.graphics.Canvas.EdgeType.BW)) {
                    val key=Tile(sample,x,y)
                    val bitmap=cache.remove(key) ?: requireNotNull(decoder.decodeRegion(region,BitmapFactory.Options().apply{inSampleSize=sample;inPreferredConfig=Bitmap.Config.ARGB_8888}))
                    cache[key]=bitmap
                    while(cache.size>8)cache.remove(cache.keys.first())
                    // Do not recycle evicted tiles: a hardware display list can
                    // still own them until its frame has been submitted.
                    native.drawBitmap(bitmap,null,target,paint)
                }
                x+=span
            }
            y+=span
        }
    }
}
