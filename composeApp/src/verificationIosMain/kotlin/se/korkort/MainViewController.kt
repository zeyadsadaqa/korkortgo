package se.korkort
import androidx.compose.ui.window.ComposeUIViewController
import platform.Foundation.NSProcessInfo
fun MainViewController() = ComposeUIViewController {
    val env=NSProcessInfo.processInfo.environment
    DeliveryProofScreen(env["PROOF_CODE"] as? String ?: "S1",env["PROOF_MODE"] as? String ?: "meaning",env["PROOF_DARK"]=="true",(env["PROOF_FONT_SCALE"] as? String)?.toFloatOrNull() ?: 1f)
}
