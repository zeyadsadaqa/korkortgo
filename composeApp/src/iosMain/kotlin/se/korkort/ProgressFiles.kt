@file:OptIn(kotlinx.cinterop.ExperimentalForeignApi::class)
package se.korkort

import androidx.compose.runtime.*
import kotlinx.coroutines.*
import kotlinx.cinterop.usePinned
import kotlinx.cinterop.addressOf
import platform.Foundation.*
import platform.UIKit.*
import platform.UniformTypeIdentifiers.UTTypeJSON
import platform.darwin.NSObject
import se.korkort.progress.MAX_BACKUP_BYTES

private class DocumentChoice: NSObject(),UIDocumentPickerDelegateProtocol {
    val result=CompletableDeferred<NSURL?>()
    override fun documentPicker(controller:UIDocumentPickerViewController,didPickDocumentsAtURLs:List<*>) {result.complete(didPickDocumentsAtURLs.firstOrNull() as? NSURL)}
    override fun documentPickerWasCancelled(controller:UIDocumentPickerViewController){result.complete(null)}
}
@Composable internal actual fun rememberProgressFiles():ProgressFiles=remember {object:ProgressFiles {
    private suspend fun present(picker:UIDocumentPickerViewController):NSURL? {
        val delegate=DocumentChoice();picker.delegate=delegate
        return withContext(Dispatchers.Main) {
            val scene=UIApplication.sharedApplication.connectedScenes.firstOrNull{it is UIWindowScene} as? UIWindowScene
            var controller=scene?.windows?.filterIsInstance<UIWindow>()?.firstOrNull{it.isKeyWindow()}?.rootViewController
            while(controller?.presentedViewController!=null)controller=controller.presentedViewController
            checkNotNull(controller){"No window available"}.presentViewController(picker,true,null)
            try {delegate.result.await()}finally {picker.delegate=null}
        }
    }
    override suspend fun choose():String? {
        val url=present(UIDocumentPickerViewController(forOpeningContentTypes=listOf(UTTypeJSON),asCopy=true)) ?: return null
        return withContext(Dispatchers.Default){
            val scoped=url.startAccessingSecurityScopedResource()
            try {
                val attrs=NSFileManager.defaultManager.attributesOfItemAtPath(checkNotNull(url.path),null)
                require((attrs?.get(NSFileSize) as? NSNumber)?.longLongValue?.let{it<=MAX_BACKUP_BYTES}==true){"File is too large"}
                checkNotNull(NSString.stringWithContentsOfURL(url,NSUTF8StringEncoding,null))
            } finally {if(scoped)url.stopAccessingSecurityScopedResource()}
        }
    }
    override suspend fun save(text:String):BackupSaveResult {
        val url=checkNotNull(NSURL.fileURLWithPath(NSTemporaryDirectory()+"korkortgo-progress.json"))
        withContext(Dispatchers.Default){
            val bytes=text.encodeToByteArray()
            val data=bytes.usePinned{NSData.create(bytes=it.addressOf(0),length=bytes.size.toULong())}
            check(data.writeToURL(url,true))
        }
        return try {if(present(UIDocumentPickerViewController(forExportingURLs=listOf(url),asCopy=true))==null)BackupSaveResult.CANCELLED else BackupSaveResult.SAVED}
        finally {NSFileManager.defaultManager.removeItemAtURL(url,null)}
    }
}}
