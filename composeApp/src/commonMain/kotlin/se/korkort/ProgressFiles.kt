package se.korkort
import androidx.compose.runtime.Composable

internal enum class BackupSaveResult { SAVED, REQUESTED, CANCELLED }
internal interface ProgressFiles {
    suspend fun choose():String?
    suspend fun save(text:String):BackupSaveResult
}
@Composable internal expect fun rememberProgressFiles():ProgressFiles
