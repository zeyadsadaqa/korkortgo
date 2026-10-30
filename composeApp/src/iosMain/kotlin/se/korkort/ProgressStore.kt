package se.korkort
import androidx.compose.runtime.*
import se.korkort.progress.openProgressDatabase
import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import kotlinx.cinterop.ExperimentalForeignApi
import platform.Foundation.*
@OptIn(ExperimentalForeignApi::class)
@Composable internal actual fun progressStoreFactory(): ()->ProgressStore = remember {{
    val directory=checkNotNull(NSFileManager.defaultManager.URLForDirectory(NSApplicationSupportDirectory,NSUserDomainMask,null,true,null)?.path)
    ProgressStore(openProgressDatabase("$directory/learner-progress.db",BundledSQLiteDriver()))
}}
