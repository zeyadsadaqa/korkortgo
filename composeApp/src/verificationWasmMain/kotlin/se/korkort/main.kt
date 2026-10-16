package se.korkort
import androidx.compose.ui.window.ComposeViewport
import kotlinx.browser.document
import kotlinx.browser.window
@OptIn(androidx.compose.ui.ExperimentalComposeUiApi::class)
fun main() {
    // This parser exists only in the explicitly built verification binary.
    val args=window.location.hash.removePrefix("#").split('/')
    ComposeViewport(document.body!!) {DeliveryProofScreen(args.getOrNull(0)?.ifBlank {"S1"} ?: "S1",args.getOrNull(1) ?: "meaning",args.getOrNull(2)=="dark",args.getOrNull(3)?.toFloatOrNull() ?: 1f)}
}
