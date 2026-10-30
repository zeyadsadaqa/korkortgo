package se.korkort
import androidx.compose.runtime.*
import se.korkort.progress.openProgressDatabase
import androidx.compose.ui.platform.LocalContext
import androidx.sqlite.driver.bundled.BundledSQLiteDriver
@Composable internal actual fun progressStoreFactory(): ()->ProgressStore {
    val context=LocalContext.current.applicationContext
    return remember(context) {{
        val file=context.getDatabasePath("learner-progress.db")
        check(file.parentFile!!.let {it.isDirectory || it.mkdirs()})
        ProgressStore(openProgressDatabase(file.absolutePath,BundledSQLiteDriver()))
    }}
}
