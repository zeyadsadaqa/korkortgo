package se.korkort
import android.content.ContextWrapper
import androidx.activity.ComponentActivity
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
@Composable internal actual fun OnStudyBackground(onBackground:()->Unit) {
    val current by rememberUpdatedState(onBackground)
    var context=LocalContext.current
    while(context !is ComponentActivity && context is ContextWrapper)context=context.baseContext
    val activity=context as? ComponentActivity
    DisposableEffect(activity) {
        val observer=LifecycleEventObserver{_,event->if(event==Lifecycle.Event.ON_STOP)current()}
        activity?.lifecycle?.addObserver(observer)
        onDispose{activity?.lifecycle?.removeObserver(observer)}
    }
}
