@file:OptIn(ExperimentalWasmJsInterop::class)
package se.korkort

import androidx.compose.runtime.*
import kotlinx.coroutines.CompletableDeferred

private fun selectProgressFile(callback:(String?,String?)->Unit):Unit=js("""{
 const input=document.createElement('input'); input.type='file'; input.accept='.json,application/json';
 input.style.display='none';document.body.appendChild(input);
 let done=false;const finish=(text,error)=>{if(done)return;done=true;input.remove();callback(text,error);};
 input.addEventListener('cancel',()=>finish(null,null));
 input.onchange=async()=>{try{const f=input.files[0];if(!f)return finish(null,null);
 if(f.size>33554432)return finish(null,'File is too large');finish(await f.text(),null);
 }catch(e){finish(null,'Could not read the selected file');}};
 input.click();
}""")
private fun downloadProgress(text:String):Unit=js("""{
 const blob=new Blob([text],{type:'application/json'});const url=URL.createObjectURL(blob);
 const a=document.createElement('a');a.href=url;a.download='korkortgo-progress.json';
 document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),60000);
}""")
@Composable internal actual fun rememberProgressFiles():ProgressFiles=remember {object:ProgressFiles {
    override suspend fun choose():String? {
        val result=CompletableDeferred<String?>()
        selectProgressFile {text,error->if(error!=null)result.completeExceptionally(IllegalArgumentException(error)) else result.complete(text)}
        return result.await()
    }
    override suspend fun save(text:String):BackupSaveResult {downloadProgress(text);return BackupSaveResult.REQUESTED}
}}
