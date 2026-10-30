package se.korkort

import androidx.compose.runtime.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.*
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import se.korkort.progress.*

internal class ProgressStore(val database: ProgressDatabase, val close: ()->Unit = { database.close() })
@Composable internal expect fun progressStoreFactory(): ()->ProgressStore
internal class StudyEnvironment(val study: DurableStudy, val scope: CoroutineScope, val notice:String?=null, private val onReplace:(WriteToken,String)->Unit={_,_->}) {
    suspend fun replace(records:StudyRecords,message:String) {
        check(!busy);busy=true
        try {writes.withLock {val token=study.repository.replaceProgress(study.token,study.catalog,records);onReplace(token,message)}} finally {busy=false}
    }
    suspend fun refreshGeneration() {
        val current=study.repository.createProfile()
        if(current!=study.token)onReplace(current,"Progress changed in another window")
    }
    var busy by mutableStateOf(false)
    var failure by mutableStateOf<String?>(null)
    var conflict by mutableStateOf(false)
    fun acknowledgeConflict(){if(conflict){conflict=false;failure=null;retry=null}}
    private val writes=Mutex()
    private val positionFlushes=mutableSetOf<()->Unit>()
    fun registerPositionFlush(flush:()->Unit):()->Unit {positionFlushes.add(flush);return {positionFlushes.remove(flush)}}
    fun flushPositions(){positionFlushes.toList().forEach{it()}}
    fun background(action:suspend ()->Unit) {
        flushPositions()
        scope.launch {try{writes.withLock {action()}}catch(e:CancellationException){throw e}catch(e:StaleSessionWrite){conflict=true}catch(e:Exception){failure="Your progress could not be saved. Try again.";retry={save(action)}}}
    }
    private var retry: (() -> Unit)? = null
    fun save(action: suspend ()->Unit) {
        if(busy)return
        retry={save(action)}; busy=true; failure=null
        scope.launch {
            try { writes.withLock { action() }; retry=null }
            catch(e: CancellationException) { throw e }
            catch(e: Exception) { if(e is StaleSessionWrite){conflict=true;retry=null;failure="This exercise changed in another window. Refreshing the saved question…"} else failure="Your progress could not be saved. Your selection is still here. Try again." }
            finally { busy=false }
        }
    }
    fun position(action: suspend ()->Unit) {
        scope.launch {
            try { writes.withLock {action()} }
            catch(e:CancellationException){throw e}
            catch(e:Exception){ if(failure==null) {failure="Your reading position could not be saved. Try again.";retry={save(action)}} }
        }
    }
    fun retry() { retry?.invoke() }
}
internal val LocalStudy = staticCompositionLocalOf<StudyEnvironment?> { null }
@Composable internal fun ProgressHost(previewFailure:Boolean?=null) {
    if(previewFailure!=null){ProgressRecoveryScreen(previewFailure,false,{},{},{});return}
    val factory=progressStoreFactory()
    var attempt by remember { mutableIntStateOf(0) }
    var store by remember { mutableStateOf<ProgressStore?>(null) }
    var study by remember { mutableStateOf<DurableStudy?>(null) }
    var failure by remember { mutableStateOf(false) }
    var notice by remember { mutableStateOf<String?>(null) }
    var recoveryConfirm by remember {mutableStateOf(false)}
    var requestedReset by remember {mutableStateOf(false)}
    val scope=rememberCoroutineScope()
    LaunchedEffect(attempt) {
        failure=false
        val resetting=requestedReset;requestedReset=false
        try {
            withTimeout(30_000) {
            val opened=factory();store=opened
            val repo=ProgressRepository(opened.database)
            var connected=DurableStudy(repo,repo.createProfile(),acceptedPracticeBank9J)
            if(resetting) {
                val token=repo.replaceProgress(connected.token,connected.catalog)
                connected=DurableStudy(repo,token,acceptedPracticeBank9J)
                notice="Progress reset. You can start again with chapter 1.";recoveryConfirm=false
            }
            if(!resetting)connected.initialize();study=connected
            }
        } catch(e:Exception){
            if(e is CancellationException && e !is TimeoutCancellationException)throw e
            store?.close?.invoke();store=null;failure=true
        }
    }
    DisposableEffect(Unit) { onDispose { store?.close?.invoke() } }
    val connected=study
    if(connected==null) ProgressRecoveryScreen(failure,recoveryConfirm,{attempt++},{recoveryConfirm=!recoveryConfirm},{requestedReset=true;attempt++}) else {
        val environment=remember(connected){StudyEnvironment(connected,scope,notice){token,message->
            if(study?.token==connected.token){notice=message;study=DurableStudy(connected.repository,token,acceptedPracticeBank9J)}
        }}
        CompositionLocalProvider(LocalStudy provides environment) { key(connected.token.generation) {CurriculumApp(acceptedPracticeBank9J,acceptedCurriculumSummary9J)} }
    }
}

@Composable internal fun ProgressRecoveryScreen(failure:Boolean,recoveryConfirm:Boolean,onRetry:()->Unit,onReviewReset:()->Unit,onReset:()->Unit) {
LearningTheme {
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(24.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
            Text(if(failure)"Could not open your saved progress" else "Opening your saved progress…",style=MaterialTheme.typography.headlineSmall)
            if(failure) {
                Text("Your saved data has not been reset. Try opening it again.")
                Button(onRetry){Text("Retry")}
                if(!recoveryConfirm)TextButton(onReviewReset){Text("Your data")}
                else {
                    StudyHeading("Reset progress?")
                    Text("This clears reading progress and saved positions, exercise history and answers, and your unfinished exercise. The lessons and question bank stay available. Exported files are not deleted.")
                    Text("A backup cannot be exported while saved progress cannot be opened. Reset only succeeds if the store can complete the operation safely; no damaged database file is silently deleted.")
                    Button(onReviewReset){Text("Keep my progress")}
                    Button(onReset,colors=ButtonDefaults.buttonColors(containerColor=MaterialTheme.colorScheme.error)){Text("Reset progress")}
                }
            }
        }
    }
}
