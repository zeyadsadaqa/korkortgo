package se.korkort

import androidx.compose.runtime.*
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.*
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import se.korkort.progress.*

internal class ProgressStore(val database: ProgressDatabase, val close: ()->Unit = { database.close() })
@Composable internal expect fun progressStoreFactory(): ()->ProgressStore
internal class StudyEnvironment(val study: DurableStudy, val scope: CoroutineScope) {
    var busy by mutableStateOf(false)
    var failure by mutableStateOf<String?>(null)
    private val writes=Mutex()
    private var retry: (() -> Unit)? = null
    fun save(action: suspend ()->Unit) {
        if(busy)return
        retry={save(action)}; busy=true; failure=null
        scope.launch {
            try { writes.withLock { action() }; retry=null }
            catch(e: CancellationException) { throw e }
            catch(e: Exception) { failure="Your progress could not be saved. Your selection is still here. Try again." }
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
@Composable internal fun ProgressHost() {
    val factory=progressStoreFactory()
    var attempt by remember { mutableIntStateOf(0) }
    var store by remember { mutableStateOf<ProgressStore?>(null) }
    var study by remember { mutableStateOf<DurableStudy?>(null) }
    var failure by remember { mutableStateOf(false) }
    val scope=rememberCoroutineScope()
    LaunchedEffect(attempt) {
        failure=false
        try {
            withTimeout(30_000) {
            val opened=factory();store=opened
            val repo=ProgressRepository(opened.database)
            val connected=DurableStudy(repo,repo.createProfile(),acceptedPracticeBank9J)
            connected.initialize();study=connected
            }
        } catch(e:Exception){
            if(e is CancellationException && e !is TimeoutCancellationException)throw e
            store?.close?.invoke();store=null;failure=true
        }
    }
    DisposableEffect(Unit) { onDispose { store?.close?.invoke() } }
    val connected=study
    if(connected==null) LearningTheme {
        Column(Modifier.fillMaxSize().padding(24.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
            Text(if(failure)"Could not open your saved progress" else "Opening your saved progress…",style=MaterialTheme.typography.headlineSmall)
            if(failure) {Text("Your saved data has not been reset. Try opening it again.");Button({attempt++}){Text("Retry")}}
        }
    } else {
        val environment=remember(connected){StudyEnvironment(connected,scope)}
        CompositionLocalProvider(LocalStudy provides environment) { CurriculumApp(acceptedPracticeBank9J,acceptedCurriculumSummary9J) }
    }
}
