package se.korkort.storageprobe

import androidx.test.platform.app.InstrumentationRegistry
import kotlinx.coroutines.runBlocking
import org.junit.Test

class AndroidPersistenceTest {
    @Test fun persistsAcrossInstrumentationProcesses() = runBlocking {
        val action = InstrumentationRegistry.getArguments().getString("probeAction") ?: "roundtrip"
        require(action in setOf("write", "verify", "roundtrip"))
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val db = androidProbe(context)
        try {
            if (action != "verify") writeProbe(db) else verifyProbe(db)
        } finally { db.close() }
        val reopened = androidProbe(context)
        try { verifyProbe(reopened) } finally { reopened.close() }
        println("STORAGE_PROBE_PASS android $action")
    }
}
