package se.korkort

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import android.net.Uri
import kotlinx.coroutines.*
import se.korkort.progress.MAX_BACKUP_BYTES

@Composable internal actual fun rememberProgressFiles():ProgressFiles {
    val resolver=LocalContext.current.contentResolver
    var opening by remember {mutableStateOf<CompletableDeferred<Uri?>?>(null)}
    var saving by remember {mutableStateOf<CompletableDeferred<Uri?>?>(null)}
    val open=rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()){opening?.complete(it);opening=null}
    val save=rememberLauncherForActivityResult(ActivityResultContracts.CreateDocument("application/json")){saving?.complete(it);saving=null}
    DisposableEffect(Unit){onDispose{opening?.cancel();saving?.cancel()}}
    return remember(resolver) {object:ProgressFiles {
        override suspend fun choose():String? {
            val result=CompletableDeferred<Uri?>();opening=result;open.launch(arrayOf("application/json","text/plain","application/octet-stream"))
            val uri=result.await() ?: return null
            return withContext(Dispatchers.IO) {checkNotNull(resolver.openInputStream(uri)).use {input->
                val output=java.io.ByteArrayOutputStream();val buffer=ByteArray(8192)
                while(true){val count=input.read(buffer);if(count<0)break;require(output.size()+count<=MAX_BACKUP_BYTES){"File is too large"};output.write(buffer,0,count)}
                output.toByteArray().decodeToString(throwOnInvalidSequence=true)
            }}
        }
        override suspend fun save(text:String):BackupSaveResult {
            val result=CompletableDeferred<Uri?>();saving=result;save.launch("korkortgo-progress.json")
            val uri=result.await() ?: return BackupSaveResult.CANCELLED
            withContext(Dispatchers.IO){checkNotNull(resolver.openOutputStream(uri,"wt")).use{it.write(text.encodeToByteArray());it.flush()}}
            return BackupSaveResult.SAVED
        }
    }}
}
