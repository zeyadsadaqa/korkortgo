package se.korkort.storageprobe

import kotlinx.coroutines.runBlocking

fun main(args: Array<String>) = runBlocking {
    require(args.size == 1 && args[0] in setOf("write", "verify"))
    val db = iosProbe()
    try {
        if (args[0] == "write") writeProbe(db) else verifyProbe(db)
        println("STORAGE_PROBE_PASS ios ${args[0]}")
    } finally { db.close() }
}
