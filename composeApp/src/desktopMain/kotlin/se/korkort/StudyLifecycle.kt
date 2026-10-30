package se.korkort
import androidx.compose.runtime.*
import java.awt.Toolkit
import java.awt.AWTEvent
import java.awt.event.AWTEventListener
import java.awt.event.WindowEvent
@Composable internal actual fun OnStudyBackground(onBackground:()->Unit) {
    val current by rememberUpdatedState(onBackground)
    DisposableEffect(Unit) {
        val listener=AWTEventListener{event->if(event is WindowEvent && event.id in setOf(WindowEvent.WINDOW_DEACTIVATED,WindowEvent.WINDOW_CLOSING))current()}
        Toolkit.getDefaultToolkit().addAWTEventListener(listener,AWTEvent.WINDOW_EVENT_MASK)
        onDispose{Toolkit.getDefaultToolkit().removeAWTEventListener(listener)}
    }
}
