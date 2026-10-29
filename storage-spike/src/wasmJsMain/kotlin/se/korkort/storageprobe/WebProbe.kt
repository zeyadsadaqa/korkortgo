package se.korkort.storageprobe

import androidx.room3.Room
import androidx.sqlite.driver.web.WebWorkerSQLiteDriver
import kotlinx.browser.document
import kotlinx.coroutines.MainScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.withTimeout
import org.w3c.dom.Worker

@OptIn(ExperimentalWasmJsInterop::class)
private fun createProbeWorker(): Worker =
    js("new Worker(new URL('worker.js', document.baseURI), {type: 'module'})")

@OptIn(ExperimentalWasmJsInterop::class)
private fun action(): String =
    js("new URLSearchParams(window.location.search).get('action') || 'verify'")

@OptIn(ExperimentalWasmJsInterop::class)
private fun supportsPersistentStorage(): Boolean =
    js("globalThis.isSecureContext && globalThis.crossOriginIsolated && !!navigator.storage?.getDirectory")

fun main() {
    MainScope().launch {
        var worker: Worker? = null
        var db: ProbeDatabase? = null
        try {
            withTimeout(30_000) {
                val requested = action()
                require(requested in setOf("write", "verify"))
                check(supportsPersistentStorage()) {
                    "Persistent SQLite requires a secure context, OPFS and COOP/COEP headers"
                }
                worker = createProbeWorker()
                db = openProbeDatabase(
                    Room.databaseBuilder<ProbeDatabase>("korkort-storage-proof.db"),
                    WebWorkerSQLiteDriver(checkNotNull(worker)),
                )
                if (requested == "write") writeProbe(checkNotNull(db)) else verifyProbe(checkNotNull(db))
                document.body?.textContent = "STORAGE_PROBE_PASS web $requested"
                document.body?.setAttribute("data-probe-result", "pass")
            }
        } catch (error: Throwable) {
            document.body?.textContent = "STORAGE_PROBE_FAIL ${error.message}"
            document.body?.setAttribute("data-probe-result", "fail")
            println(error.toString())
        } finally {
            db?.close()
            worker?.terminate()
        }
    }
}
