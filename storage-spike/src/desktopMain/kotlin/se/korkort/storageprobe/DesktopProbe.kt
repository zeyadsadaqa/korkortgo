package se.korkort.storageprobe

import androidx.room3.Room
import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import java.io.File
import kotlinx.coroutines.runBlocking

fun desktopProbe(path: String): ProbeDatabase {
    File(path).absoluteFile.parentFile.mkdirs()
    return openProbeDatabase(Room.databaseBuilder<ProbeDatabase>(path), BundledSQLiteDriver())
}

fun main(args: Array<String>) = runBlocking {
    require(args.size == 2 && args[0] in setOf("write", "verify"))
    val db = desktopProbe(args[1])
    try {
        if (args[0] == "write") writeProbe(db) else verifyProbe(db)
        println("STORAGE_PROBE_PASS desktop ${args[0]}")
    } finally { db.close() }
}
