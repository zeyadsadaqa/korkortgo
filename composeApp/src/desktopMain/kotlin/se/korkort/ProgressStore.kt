package se.korkort
import androidx.compose.runtime.*
import se.korkort.progress.openProgressDatabase
import java.io.File
import androidx.sqlite.driver.bundled.BundledSQLiteDriver
@Composable internal actual fun progressStoreFactory(): ()->ProgressStore = remember {{
    val directory=File(System.getProperty("user.home"),".korkortgo").apply{mkdirs()}
    ProgressStore(openProgressDatabase(File(directory,"learner-progress.db").absolutePath,BundledSQLiteDriver()))
}}
