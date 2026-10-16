package se.korkort

import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asComposeCanvas
import androidx.compose.ui.graphics.drawscope.CanvasDrawScope
import androidx.compose.ui.graphics.drawscope.withTransform
import androidx.compose.ui.unit.Density
import androidx.compose.ui.unit.LayoutDirection
import kotlinx.coroutines.runBlocking
import org.jetbrains.skia.EncodedImageFormat
import org.jetbrains.skia.Surface
import java.io.File
import kotlin.test.*

class ExactVectorRenderingTest {
    @Test fun exactPdfDisplayListRendersWithoutStrokeOrGeometryChanges() {
        val assets=navigationAssets.filter {it.bundled.path.endsWith(".pdf")}
        assertEquals(18,assets.size)
        for(asset in assets) {
            val vector=requireNotNull(decodedOfficialVector(asset.bundled.sha256))
            val width=kotlin.math.ceil(vector.width*4f).toInt();val height=kotlin.math.ceil(vector.height*4f).toInt()
            val surface=Surface.makeRasterN32Premul(width,height)
            try {
                CanvasDrawScope().draw(Density(1f),LayoutDirection.Ltr,surface.canvas.asComposeCanvas(),Size(width.toFloat(),height.toFloat())) {
                    drawRect(Color.White)
                    withTransform({scale(4f,4f,pivot=Offset.Zero)}) {vector.draw(this)}
                }
                val file=File("build/verification/9L10/${asset.codeOrIllustrationId.lowercase()}-compose-4x.png");file.parentFile.mkdirs()
                file.writeBytes(surface.makeImageSnapshot().encodeToData(EncodedImageFormat.PNG)!!.bytes)
                assertEquals(asset.original.sha256,vector.sourceSha256)
            } finally {surface.close()}
        }
        assertEquals(.90459114f,decodedS1Vector().strokeWidth,.000001f)
    }
    @Test fun runtimeResourcesMatchExactApprovedB1AndS1Bindings() = runBlocking {
        for(code in listOf("B1")+(1..13).map {"S$it"}+listOf("T1","T2","T6","T8","T22","X8")) {
            val asset=navigationAssets.single {it.id==AssetId("official/$code")}
            assertTrue(loadExactAsset(asset).intrinsicSize.width>0f)
            assertFailsWith<IllegalArgumentException> {loadExactAsset(asset.copy(original=asset.original.copy(sha256=Sha256("0".repeat(64))),bundled=asset.bundled.copy(sha256=Sha256("0".repeat(64)))))}
        }
    }
}
