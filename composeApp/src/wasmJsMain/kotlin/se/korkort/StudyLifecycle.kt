@file:OptIn(ExperimentalWasmJsInterop::class)
package se.korkort
import androidx.compose.runtime.*
private fun listenBackground(callback:()->Unit):JsAny=js("""{
 const hidden=()=>{if(document.visibilityState==='hidden')callback();};
 const pagehide=()=>callback();document.addEventListener('visibilitychange',hidden);window.addEventListener('pagehide',pagehide);
 return {hidden,pagehide};
}""")
private fun stopBackground(token:JsAny):Unit=js("""{document.removeEventListener('visibilitychange',token.hidden);window.removeEventListener('pagehide',token.pagehide);}""")
@Composable internal actual fun OnStudyBackground(onBackground:()->Unit) {
    val current by rememberUpdatedState(onBackground)
    DisposableEffect(Unit) {val token=listenBackground{current()};onDispose{stopBackground(token)}}
}
