package se.korkort
import androidx.compose.ui.geometry.Offset
import kotlin.test.*

class ImageViewportTest {
    @Test fun fitContainsWholeImageWithOneScale() {
        val v=ImageViewport()
        assertEquals(2f,v.fit(100f,50f,200f,200f))
        assertEquals(1f,v.fit(100f,50f,300f,50f))
        assertEquals(Offset.Zero,v.bounds(100f,50f,200f,200f))
        assertFailsWith<IllegalArgumentException> {v.fit(0f,50f,200f,200f)}
    }
    @Test fun panCannotLoseTheImageAndResetReturnsToFit() {
        val zoom=ImageViewport(4f,Offset(10000f,-10000f)).clamp(100f,50f,200f,200f)
        assertEquals(Offset(300f,-100f),zoom.pan)
        assertEquals(ImageViewport(),zoom.reset())
        assertEquals(Offset.Zero,zoom.copy(zoom=1f).clamp(100f,50f,200f,200f).pan)
        assertEquals(8f,zoom.zoomTo(50f).zoom);assertEquals(1f,zoom.zoomTo(.1f).zoom)
    }
    @Test fun resourceHashMatchesStandardSha256Vectors() {
        assertEquals("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",assetSha256(byteArrayOf()).value)
        assertEquals("ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",assetSha256("abc".encodeToByteArray()).value)
        assertEquals("248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1",assetSha256("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq".encodeToByteArray()).value)
    }
    @Test fun assessmentViewerDoesNotUseStudyMeaningOrCode() {
        val asset=navigationAssets.single {it.id==AssetId("official/S1")}
        val viewer=ImageViewerContent.assessment(AssessmentImagePresentation(asset.id,"Thin dark outline of a rectangular body with three circles beneath it."),navigationAssets)
        assertEquals("Question illustration",viewer.title)
        assertFalse(viewer.description.contains("S1"));assertFalse(viewer.description.contains("Heavy goods"))
        assertEquals(asset,viewer.asset)
    }
}
