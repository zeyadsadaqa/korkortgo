package se.korkort
import android.os.Bundle
import android.graphics.Bitmap
import android.os.Handler
import android.os.Looper
import android.view.PixelCopy
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.*
import kotlinx.coroutines.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.File

/** Only compiled/declared with -PreferenceProof; never present in normal debug/release builds. */
class DeliveryProofActivity: ComponentActivity() {
    private data class Spec(val code:String,val mode:String,val dark:Boolean,val scale:Float,val ready:CompletableDeferred<Boolean> = CompletableDeferred())
    private val scope=MainScope()
    private var spec by mutableStateOf(Spec("S1","meaning",false,1f))
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState);enableEdgeToEdge()
        spec=Spec(intent.getStringExtra("code") ?: "S1",intent.getStringExtra("mode") ?: "meaning",intent.getBooleanExtra("dark",false),intent.getFloatExtra("fontScale",1f))
        setContent {val current=spec;key(current) {DeliveryProofScreen(current.code,current.mode,current.dark,current.scale) {current.ready.complete(it)}}}
        if(intent.getBooleanExtra("captureAll",false))scope.launch {captureAll()}
    }
    private suspend fun captureAll() {
        val folder=File(filesDir,"delivery-proof");folder.mkdirs();File(folder,"complete.json").delete();val results=JSONArray()
        for(code in deliveryFixtureCodes)for(dark in listOf(false,true))for(scale in listOf(1f,1.6f)) {
            val current=Spec(code,"delivery",dark,scale);spec=current
            val loaded=withTimeoutOrNull(10000) {current.ready.await()}==true
            delay(200)
            val bitmap=Bitmap.createBitmap(window.decorView.width,window.decorView.height,Bitmap.Config.ARGB_8888)
            val copied=CompletableDeferred<Int>()
            PixelCopy.request(window,bitmap,{copied.complete(it)},Handler(Looper.getMainLooper()))
            val status=withTimeoutOrNull(5000) {copied.await()}
            val name="$code-${if(dark) "dark" else "light"}-$scale.png"
            if(status==PixelCopy.SUCCESS)File(folder,name).outputStream().use {bitmap.compress(Bitmap.CompressFormat.PNG,100,it)}
            bitmap.recycle()
            results.put(JSONObject().put("code",code).put("mode","approved equal full-width artwork frames, minimum 220dp").put("dark",dark).put("font_scale",scale).put("exact_assets_loaded",loaded).put("pixel_copy_result",status).put("screenshot",name))
            File(folder,"progress.json").writeText(results.toString(2))
        }
        File(folder,"complete.json").writeText(JSONObject().put("status","captures complete; no legibility or scoring acceptance").put("captures",results).toString(2))
    }
    override fun onDestroy() {scope.cancel();super.onDestroy()}
}
