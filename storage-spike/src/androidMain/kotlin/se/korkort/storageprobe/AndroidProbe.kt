package se.korkort.storageprobe

import android.content.Context
import androidx.room3.Room
import androidx.sqlite.driver.bundled.BundledSQLiteDriver

fun androidProbe(context: Context): ProbeDatabase {
    val app = context.applicationContext
    return openProbeDatabase(
        Room.databaseBuilder<ProbeDatabase>(app, app.getDatabasePath("storage-proof.db").absolutePath),
        BundledSQLiteDriver(),
    )
}
