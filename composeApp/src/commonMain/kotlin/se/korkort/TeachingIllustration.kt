@file:OptIn(org.jetbrains.compose.resources.ExperimentalResourceApi::class)
package se.korkort

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.Alignment
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.*
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import org.jetbrains.compose.resources.decodeToImageBitmap
import se.korkort.resources.Res
import kotlin.coroutines.cancellation.CancellationException

/** Only authored contextual windows/masks are applied; official art uses ExactAssetImage. */
@Composable internal fun TeachingIllustration(id:AssetId,region:ApprovedImageRegion?,polygon:List<SourcePixelPoint>,overlays:List<IllustrationOverlay>,caption:RichText,onLink:(TeachingLink)->Unit) {
    val asset=readerAssets.single{it.id==id}
    if(asset.kind==AssetKind.OFFICIAL_SIGN) {
        require(region==null && polygon.isEmpty() && overlays.isEmpty())
        StudyImage(asset,"Enlarge image")
        TeachingText(caption,onLink);return
    }
    var bitmap by remember(id){mutableStateOf<ImageBitmap?>(null)}
    var error by remember(id){mutableStateOf(false)}
    LaunchedEffect(id){try {
        val bytes=Res.readBytes(asset.bundled.path.removePrefix("composeApp/src/commonMain/composeResources/"))
        require(assetSha256(bytes)==asset.bundled.sha256)
        bitmap=bytes.decodeToImageBitmap()
    }catch(e:CancellationException){throw e}catch(_:Exception){error=true}}
    Column(verticalArrangement=Arrangement.spacedBy(8.dp)) {
        val b=bitmap
        if(b!=null) {
            val left=region?.left?:0;val top=region?.top?:0
            val w=(region?.let{it.right-it.left}?:b.width).toFloat();val h=(region?.let{it.bottom-it.top}?:b.height).toFloat()
            BoxWithConstraints(Modifier.fillMaxWidth().aspectRatio(w/h)) {
                Canvas(Modifier.fillMaxSize()) {
                    val scale=size.width/w
                    val path=Path().apply {polygon.forEachIndexed{i,p->if(i==0)moveTo((p.x-left)*scale,(p.y-top)*scale)else lineTo((p.x-left)*scale,(p.y-top)*scale)};close()}
                    fun DrawScope.paint(){withTransform({scale(scale,scale,Offset.Zero);translate(-left.toFloat(),-top.toFloat())}){drawImage(b);overlays.forEach{drawRect(Color.White,Offset(it.left.toFloat(),it.top.toFloat()),Size((it.right-it.left).toFloat(),(it.bottom-it.top).toFloat()))}}}
                    clipRect {if(polygon.isEmpty()) paint() else clipPath(path){paint()}}
                }
                overlays.forEach { overlay ->
                    val x=(overlay.left+overlay.insetPixels-left)/w;val y=(overlay.top+overlay.insetPixels-top)/h
                    val ow=(overlay.right-overlay.left-2*overlay.insetPixels)/w;val oh=(overlay.bottom-overlay.top-2*overlay.insetPixels)/h
                    Box(Modifier.offset(maxWidth*x,maxHeight*y).width(maxWidth*ow).height(maxHeight*oh)) {
                        overlay.assetId?.let { overlayId -> ExactAssetImage(readerAssets.single{it.id==overlayId},readerAssets.single{it.id==overlayId}.studyAltText,Modifier.fillMaxSize()) }
                        if(overlay.label.isNotEmpty()) Text(overlay.label.annotated(onLink),fontSize=12.sp)
                    }
                }
            }
            // An equivalent selectable description remains available at the user's actual text scale.
        } else {
            val dimensions=readerImageDimensions.getValue(id)
            val ratio=region?.let{(it.right-it.left).toFloat()/(it.bottom-it.top)} ?: (dimensions.first.toFloat()/dimensions.second)
            Box(Modifier.fillMaxWidth().aspectRatio(ratio),contentAlignment=Alignment.Center){Text(if(error)"Illustration unavailable." else "Loading illustration…")}
        }
        Text(asset.studyAltText)
        overlays.filter{it.label.isNotEmpty()}.forEach{TeachingText(it.label,onLink)}
        TeachingText(caption,onLink)
        asset.reuse.map{it.credit}.distinct().forEach{Text(it)}
    }
}
