@file:OptIn(androidx.compose.ui.ExperimentalComposeUiApi::class)
package se.korkort

import androidx.compose.foundation.background
import androidx.compose.foundation.focusGroup
import androidx.compose.foundation.focusable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.*
import androidx.compose.ui.input.key.*
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties

internal expect val singleLayerBrowserModals: Boolean
internal expect fun setBrowserModalAccessibility(active:Boolean)
private class RootModal(val token:Any,val dismiss:()->Unit,val fullWidth:Boolean,val content:@Composable ()->Unit)
private class RootModalState {var modal by mutableStateOf<RootModal?>(null)}
private val LocalRootModal = staticCompositionLocalOf<RootModalState?> {null}

/** Browser 1.9.3 tracks only the latest scene semantics owner. Keep production
 * modals in the root scene so closing one restores the real accessibility tree. */
@Composable internal fun RootModalHost(content:@Composable ()->Unit) {
    if(!singleLayerBrowserModals){content();return}
    val host=remember {RootModalState()}
    val modal=host.modal
    val focus=remember {FocusRequester()}
    SideEffect {setBrowserModalAccessibility(modal!=null)}
    val manager=LocalFocusManager.current
    CompositionLocalProvider(LocalRootModal provides host) {
        Box(Modifier.fillMaxSize()) {
            Box(Modifier.fillMaxSize().semantics{contentDescription="Application content"}){content()}
            if(modal!=null) {
                Box(Modifier.fillMaxSize().background(MaterialTheme.colorScheme.scrim.copy(alpha=0.32f))
                    .pointerInput(modal.token){detectTapGestures {modal.dismiss()}}
                    .focusProperties{exit={FocusRequester.Cancel}}.focusGroup()
                    .onPreviewKeyEvent{event->
                        if(event.type==KeyEventType.KeyDown && event.key==Key.Escape){modal.dismiss();true}
                        else if(event.type==KeyEventType.KeyDown && event.key==Key.Tab){
                            val moved=manager.moveFocus(if(event.isShiftPressed)FocusDirection.Previous else FocusDirection.Next)
                            if(!moved){focus.requestFocus();manager.moveFocus(if(event.isShiftPressed)FocusDirection.Previous else FocusDirection.Next)}
                            true
                        }else false
                    }.focusRequester(focus).focusable().semantics{isTraversalGroup=true},contentAlignment=Alignment.Center) {
                    Box((if(modal.fullWidth)Modifier.fillMaxSize() else Modifier.widthIn(max=560.dp).fillMaxWidth().padding(24.dp))
                        .pointerInput(Unit){detectTapGestures{}},contentAlignment=Alignment.Center){modal.content()}
                }
                LaunchedEffect(modal.token){withFrameNanos{};focus.requestFocus()}
            }
        }
    }
}

@Composable internal fun RootPlatformDialog(onDismissRequest:()->Unit,fullWidth:Boolean=false,content:@Composable ()->Unit) {
    val host=LocalRootModal.current
    if(!singleLayerBrowserModals || host==null){Dialog(onDismissRequest,properties=DialogProperties(usePlatformDefaultWidth=!fullWidth),content=content);return}
    val token=remember {Any()}
    val body by rememberUpdatedState(content)
    val dismiss by rememberUpdatedState(onDismissRequest)
    DisposableEffect(host,token){host.modal=RootModal(token,{dismiss()},fullWidth){body()};onDispose{if(host.modal?.token===token)host.modal=null}}
}

@Composable internal fun RootAlertDialog(title:String,message:String,dismiss:String?,confirm:String,onDismiss:()->Unit,onConfirm:()->Unit) {
    if(!singleLayerBrowserModals){
        AlertDialog(onDismissRequest=onDismiss,title={Text(title)},text={Text(message)},confirmButton={TextButton(onConfirm){Text(confirm)}},dismissButton=dismiss?.let{{TextButton(onDismiss){Text(it)}}})
    }else RootPlatformDialog(onDismiss){
        Surface(shape=MaterialTheme.shapes.extraLarge,color=MaterialTheme.colorScheme.surfaceContainerHigh,tonalElevation=6.dp) {
            Column(Modifier.padding(24.dp).verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(24.dp)) {
                Text(title,style=MaterialTheme.typography.headlineSmall,modifier=Modifier.semantics{heading()})
                Text(message,style=MaterialTheme.typography.bodyMedium)
                Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.End){
                    if(dismiss!=null)TextButton(onDismiss){Text(dismiss)}
                    TextButton(onConfirm){Text(confirm)}
                }
            }
        }
    }
}
