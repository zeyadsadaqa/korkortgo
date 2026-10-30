package se.korkort
import androidx.compose.runtime.Composable
import androidx.activity.compose.BackHandler
@Composable internal actual fun PlatformStudyBack(enabled:Boolean,onBack:()->Unit) {BackHandler(enabled,onBack)}
