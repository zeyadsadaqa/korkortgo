@file:OptIn(ExperimentalWasmJsInterop::class)
package se.korkort
import androidx.compose.runtime.*
import se.korkort.progress.openProgressDatabase
import androidx.sqlite.driver.web.WebWorkerSQLiteDriver
import org.w3c.dom.Worker
private fun canPersist(): Boolean = js("globalThis.isSecureContext && globalThis.crossOriginIsolated && !!navigator.storage?.getDirectory")
private fun worker(): Worker = js("new Worker(new URL('worker.js',document.baseURI),{type:'module'})")
@Composable internal actual fun progressStoreFactory(): ()->ProgressStore = remember {{
    check(canPersist()) { "Persistent browser storage requires HTTPS and isolation headers" }
    val worker=worker()
    try {
        val db=openProgressDatabase("learner-progress.db",WebWorkerSQLiteDriver(worker))
        ProgressStore(db) {db.close();worker.terminate()}
    } catch(e:Exception){worker.terminate();throw e}
}}
