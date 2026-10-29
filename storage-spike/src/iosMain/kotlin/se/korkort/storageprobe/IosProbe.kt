package se.korkort.storageprobe

import androidx.room3.Room
import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import kotlinx.cinterop.ExperimentalForeignApi
import platform.Foundation.NSApplicationSupportDirectory
import platform.Foundation.NSFileManager
import platform.Foundation.NSUserDomainMask

@OptIn(ExperimentalForeignApi::class)
fun iosProbe(): ProbeDatabase {
    val directory = checkNotNull(NSFileManager.defaultManager.URLForDirectory(
        NSApplicationSupportDirectory, NSUserDomainMask, null, true, null,
    )?.path)
    return openProbeDatabase(
        Room.databaseBuilder<ProbeDatabase>("$directory/korkort-storage-proof.db"),
        BundledSQLiteDriver(),
    )
}
