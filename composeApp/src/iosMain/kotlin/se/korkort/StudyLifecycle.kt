package se.korkort
import androidx.compose.runtime.*
import platform.Foundation.*
import platform.UIKit.UIApplicationWillResignActiveNotification
@Composable internal actual fun OnStudyBackground(onBackground:()->Unit) {
    val current by rememberUpdatedState(onBackground)
    DisposableEffect(Unit) {
        val observer=NSNotificationCenter.defaultCenter.addObserverForName(UIApplicationWillResignActiveNotification,null,NSOperationQueue.mainQueue){current()}
        onDispose{NSNotificationCenter.defaultCenter.removeObserver(observer)}
    }
}
