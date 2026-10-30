package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.*
import se.korkort.progress.*

internal enum class DataPage { OVERVIEW,EXPORT,REVIEW,INVALID,RESET,COMPLETE }
internal class DataUiState(notice:String?=null) {
    var page by mutableStateOf(if(notice==null)DataPage.OVERVIEW else DataPage.COMPLETE)
    var backup by mutableStateOf<ProgressBackup?>(null)
    var busy by mutableStateOf(false)
    var error by mutableStateOf<String?>(null)
    var notice by mutableStateOf(notice)
    var exportReturn by mutableStateOf(DataPage.OVERVIEW)
    fun back():Boolean {if(page==DataPage.OVERVIEW || page==DataPage.COMPLETE)return false;page=DataPage.OVERVIEW;error=null;return true}
}
@Composable internal fun DataControls(environment:StudyEnvironment,records:StudyRecords?,ui:DataUiState,onLearning:()->Unit) {
    val files=rememberProgressFiles()
    fun run(action:suspend ()->Unit) {
        if(ui.busy)return
        ui.busy=true;ui.error=null;ui.notice=null
        environment.scope.launch {
            try{action()}catch(e:CancellationException){throw e}
            catch(e:Exception){ui.error="The operation could not be completed. Your current progress has not been replaced or reset. Try again."}
            finally {ui.busy=false}
        }
    }
    fun choose()=run {
        val text=files.choose() ?: return@run
        try {ui.backup=withContext(Dispatchers.Default){environment.study.validateImport(text)};ui.page=DataPage.REVIEW}
        catch(e:Exception){if(e is CancellationException)throw e;ui.backup=null;ui.page=DataPage.INVALID}
    }
    fun export(returnTo:DataPage){ui.exportReturn=returnTo;ui.page=DataPage.EXPORT}
    Column(Modifier.widthIn(max=800.dp).fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
        StudyHeading(when(ui.page){DataPage.EXPORT->"Save a backup";DataPage.REVIEW->"Review import";DataPage.INVALID->"Import progress";DataPage.RESET->"Reset progress?";else->"Your data"})
        ui.notice?.let{StudyCard(true){Text(it,style=MaterialTheme.typography.titleLarge,modifier=Modifier.semantics{liveRegion=LiveRegionMode.Polite})}}
        ui.error?.let{StudyCard{Text(it,color=MaterialTheme.colorScheme.error,modifier=Modifier.semantics{liveRegion=LiveRegionMode.Assertive})}}
        if(ui.busy){LinearProgressIndicator(Modifier.fillMaxWidth());Text("Please wait…",Modifier.semantics{liveRegion=LiveRegionMode.Polite})}
        when(ui.page) {
            DataPage.OVERVIEW,DataPage.COMPLETE->{
                Text("Keep a copy of your progress or restore a saved file.")
                if(records!=null)StudyCard {
                    Text("${records.summary(environment.study.catalog).lessonsRead} lessons marked as read")
                    Text("${records.sessions.count{it.status!="active"}} completed or ended exercises")
                    Text(if(records.sessions.any{it.status=="active"})"1 unfinished exercise" else "No unfinished exercise")
                }
                if(ui.page==DataPage.COMPLETE)StudyAction("Start learning",!ui.busy,onLearning)
                StudyRow("Export progress","Save a backup file",!ui.busy && records!=null){export(DataPage.OVERVIEW)}
                StudyRow("Import progress","Review a file before replacing progress",!ui.busy){choose()}
                TextButton({ui.page=DataPage.RESET},enabled=!ui.busy){Text("Reset progress",color=MaterialTheme.colorScheme.error)}
                Text("Progress is stored on this device. Keep exported files somewhere safe.")
            }
            DataPage.EXPORT->{
                StudyCard {Text("korkortgo-progress.json",style=MaterialTheme.typography.titleMedium);Text("Includes reading progress and positions, exercise history and confirmed answers, and your unfinished exercise.")}
                Text("Choose where to save the file. Exporting does not change your progress.")
                StudyAction("Save backup file",!ui.busy){run {
                    val text=environment.study.repository.exportProgress(environment.study.token)
                    when(files.save(text)){
                        BackupSaveResult.SAVED->ui.notice="Backup file saved"
                        BackupSaveResult.REQUESTED->ui.notice="Backup download requested. Check your browser's downloads."
                        BackupSaveResult.CANCELLED->Unit
                    }
                    ui.page=ui.exportReturn
                }}
                TextButton({ui.page=ui.exportReturn},enabled=!ui.busy){Text("Cancel")}
            }
            DataPage.REVIEW->{
                val backup=ui.backup
                if(backup==null){Text("Choose a supported progress file.");StudyAction("Choose a file",!ui.busy){choose()}}
                else {
                    StudyCard {Text("korkortgo-progress.json · File checked");Text("${backup.records.lessons.count{it.read}} lessons marked as read");Text("${backup.records.sessions.count{it.status!="active"}} completed or ended exercises");Text(if(backup.records.sessions.any{it.status=="active"})"1 unfinished exercise" else "No unfinished exercise")}
                    Text("Replace current progress?",style=MaterialTheme.typography.titleLarge,color=MaterialTheme.colorScheme.error)
                    Text("This replaces your reading progress, exercise history and unfinished exercise on this device. Earlier content remains historical and may not count toward the current curriculum.")
                    OutlinedButton({export(DataPage.REVIEW)},enabled=!ui.busy,modifier=Modifier.fillMaxWidth()){Text("Export current progress first")}
                    StudyAction("Replace progress",!ui.busy){run {environment.replace(backup.records,"Progress imported")}}
                    TextButton({ui.page=DataPage.OVERVIEW;ui.backup=null},enabled=!ui.busy){Text("Cancel")}
                }
            }
            DataPage.INVALID->{
                Text("This file can't be imported",style=MaterialTheme.typography.titleLarge,color=MaterialTheme.colorScheme.error)
                Text("Choose a supported KörkortGo progress file. Your current progress has not changed.")
                StudyAction("Choose another file",!ui.busy){choose()}
                OutlinedButton({ui.page=DataPage.OVERVIEW},enabled=!ui.busy,modifier=Modifier.fillMaxWidth()){Text("Back to Your data")}
            }
            DataPage.RESET->{
                Text("This clears:",style=MaterialTheme.typography.titleLarge,color=MaterialTheme.colorScheme.error)
                Text("Reading progress and saved positions\nExercise history and answers\nYour unfinished exercise")
                Text("The lessons and question bank stay available. Exported files are not deleted.")
                OutlinedButton({export(DataPage.RESET)},enabled=!ui.busy,modifier=Modifier.fillMaxWidth()){Text("Export progress first")}
                StudyAction("Keep my progress",!ui.busy){ui.page=DataPage.OVERVIEW}
                Button({run {environment.replace(StudyRecords(),"Progress reset. You can start again with chapter 1.")}},enabled=!ui.busy,colors=ButtonDefaults.buttonColors(containerColor=MaterialTheme.colorScheme.error),modifier=Modifier.fillMaxWidth().heightIn(min=52.dp)){Text("Reset progress")}
                Text("You can't undo this without an exported backup.")
            }
        }
    }
}
