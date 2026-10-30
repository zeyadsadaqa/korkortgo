package se.korkort

import androidx.compose.runtime.*
import kotlinx.coroutines.*
import javax.swing.JFileChooser
import javax.swing.SwingUtilities
import se.korkort.progress.MAX_BACKUP_BYTES

@Composable internal actual fun rememberProgressFiles():ProgressFiles=remember {object:ProgressFiles {
    private suspend fun pick(save:Boolean):java.io.File? {
        val result=CompletableDeferred<java.io.File?>()
        SwingUtilities.invokeLater {
            try {val chooser=JFileChooser().apply{selectedFile=java.io.File("korkortgo-progress.json")}
                var answer=if(save)chooser.showSaveDialog(null) else chooser.showOpenDialog(null)
                if(save && answer==JFileChooser.APPROVE_OPTION && chooser.selectedFile.exists() && javax.swing.JOptionPane.showConfirmDialog(null,"Replace this backup file?","Save backup",javax.swing.JOptionPane.YES_NO_OPTION)!=javax.swing.JOptionPane.YES_OPTION)answer=JFileChooser.CANCEL_OPTION
                result.complete(if(answer==JFileChooser.APPROVE_OPTION)chooser.selectedFile else null)
            }catch(e:Exception){result.completeExceptionally(e)}
        }
        return result.await()
    }
    override suspend fun choose():String? {
        val file=pick(false) ?: return null
        return withContext(Dispatchers.IO){file.inputStream().use {input->
            val out=java.io.ByteArrayOutputStream();val buffer=ByteArray(8192)
            while(true){val n=input.read(buffer);if(n<0)break;require(out.size()+n<=MAX_BACKUP_BYTES);out.write(buffer,0,n)}
            out.toByteArray().decodeToString(throwOnInvalidSequence=true)
        }}
    }
    override suspend fun save(text:String):BackupSaveResult {
        val file=pick(true) ?: return BackupSaveResult.CANCELLED
        withContext(Dispatchers.IO){file.writeText(text)}
        return BackupSaveResult.SAVED
    }
}}
