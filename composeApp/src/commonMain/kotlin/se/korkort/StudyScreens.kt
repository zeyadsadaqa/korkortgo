@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class,kotlin.time.ExperimentalTime::class)
package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.unit.dp
import se.korkort.progress.*
import kotlin.time.Instant

@Composable internal fun StudyCard(sage:Boolean=false,content:@Composable ColumnScope.()->Unit) {
    OutlinedCard(Modifier.fillMaxWidth(),colors=CardDefaults.outlinedCardColors(containerColor=if(sage)MaterialTheme.colorScheme.secondaryContainer else MaterialTheme.colorScheme.surface)) {
        Column(Modifier.padding(20.dp),verticalArrangement=Arrangement.spacedBy(12.dp),content=content)
    }
}
@Composable internal fun StudyHeading(text:String) {Text(text,style=MaterialTheme.typography.headlineLarge,modifier=Modifier.semantics{heading()})}
@Composable internal fun StudyAction(label:String,enabled:Boolean=true,onClick:()->Unit) {Button(onClick,enabled=enabled,modifier=Modifier.fillMaxWidth().heightIn(min=52.dp),shape=RoundedCornerShape(12.dp)){Text(label)}}
@Composable internal fun StudyRow(title:String,detail:String?=null,enabled:Boolean=true,onClick:()->Unit) {
    OutlinedButton(onClick,enabled=enabled,modifier=Modifier.fillMaxWidth().heightIn(min=64.dp),contentPadding=PaddingValues(16.dp),shape=RoundedCornerShape(16.dp)) {
        Column(Modifier.weight(1f)){Text(title,style=MaterialTheme.typography.titleMedium);detail?.let{Text(it,style=MaterialTheme.typography.bodyMedium)}}
        Text("›",Modifier.clearAndSetSemantics{})
    }
}
@Composable internal fun ProgressUnavailable(failed:Boolean,retry:()->Unit) {
    Column(Modifier.fillMaxWidth().padding(24.dp),verticalArrangement=Arrangement.spacedBy(20.dp)) {
        if(failed) {StudyCard {Text("Couldn't load your progress",style=MaterialTheme.typography.titleLarge);Text("Try again to see your saved learning and next step.");StudyAction("Try again",onClick=retry)}}
        else {LinearProgressIndicator(Modifier.fillMaxWidth());Text("Loading your progress…",Modifier.semantics{liveRegion=LiveRegionMode.Polite})}
    }
}
@Composable internal fun HomeDashboard(data:Dashboard?,failed:Boolean,retry:()->Unit,scroll:LazyListState,onLearning:()->Unit,onExercise:()->Unit,onStep:(NextStudyStep)->Unit,onChapter:(CurriculumModule)->Unit,onData:()->Unit) {
    LazyColumn(state=scroll,modifier=Modifier.widthIn(max=1100.dp).fillMaxSize(),contentPadding=PaddingValues(20.dp),verticalArrangement=Arrangement.spacedBy(20.dp)) {
        item{StudyHeading("Your progress");Text(if(data?.summary?.lessonsRead==0 && data.summary.answered==0 && data.next.resume==null)"Your learning starts here." else "Every step brings you closer.")}
        if(data==null) item {ProgressUnavailable(failed,retry);if(failed){TextButton(onLearning){Text("Browse learning")};TextButton(onExercise){Text("Open Exercise")}}}
        else {
            val s=data.summary
            item {
                BoxWithConstraints {
                    val stacked=maxWidth<360.dp || LocalDensity.current.fontScale>1.3f
                    @Composable fun chapters(){CoverageCard(s.chaptersRead,s.chaptersTotal,"Chapters read",onLearning)}
                    @Composable fun questions(){CoverageCard(s.answered,s.questionTotal,"Questions answered",onExercise)}
                    if(stacked)Column(verticalArrangement=Arrangement.spacedBy(12.dp)){chapters();questions()}
                    else Row(horizontalArrangement=Arrangement.spacedBy(12.dp)){Box(Modifier.weight(1f)){chapters()};Box(Modifier.weight(1f)){questions()}}
                }
            }
            item {StudyCard(true){Text("YOUR NEXT STEP",style=MaterialTheme.typography.labelLarge);Text(data.next.title,style=MaterialTheme.typography.headlineSmall);Text(data.next.reason)
                data.next.resume?.let{id->Text(ExerciseRequest.decode(data.records.value("mode:$id")).label);Text(if(data.records.sessions.singleOrNull{it.id==id}?.deferred==true)"Answers will be shown at the end." else "Answers are explained after each question.")}
                StudyAction(data.next.action){onStep(data.next)}
            }}
            item {Text("Learning overview",style=MaterialTheme.typography.headlineSmall,modifier=Modifier.semantics{heading()})}
            if(data.lastChapter!=null)item {StudyRow("Last completed",data.lastChapter.title){onChapter(data.lastChapter)}}
            if(s.lessonsRead==s.lessonsTotal)item {StudyRow("All ${s.lessonsTotal} lessons read","Browse learning",onClick=onLearning)}
            else item {StudyRow("Browse all ${s.chaptersTotal} chapters","${s.lessonsRead} of ${s.lessonsTotal} lessons read",onClick=onLearning)}
            if(s.revisit>0)item{StudyRow("${s.revisit} ${if(s.revisit==1)"question" else "questions"} to revisit","Based on your latest published answers"){onStep(NextStudyStep("","","",request=ExerciseRequest(ExerciseMode.REVIEW)))}}
            item {Text("Progress saved on this device",style=MaterialTheme.typography.bodySmall);TextButton(onData){Text("Your data")}}
        }
    }
}
@Composable private fun CoverageCard(count:Int,total:Int,label:String,onClick:()->Unit) {
    OutlinedCard(onClick,modifier=Modifier.fillMaxWidth(),colors=CardDefaults.outlinedCardColors(containerColor=MaterialTheme.colorScheme.surface)) {Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(8.dp)) {
        Text("$count / $total",style=MaterialTheme.typography.headlineSmall);Text(label)
        LinearProgressIndicator(progress={if(total==0)0f else count.toFloat()/total},modifier=Modifier.fillMaxWidth().semantics{contentDescription=label})
    }}
}
internal enum class ExercisePage { HUB,SETUP,HISTORY,DETAIL }
internal class ExerciseUiState {
    var page by mutableStateOf(ExercisePage.HUB)
    var request by mutableStateOf(ExerciseRequest())
    var count by mutableStateOf("20")
    var feedback by mutableStateOf(Feedback.IMMEDIATE)
    var detail by mutableStateOf<String?>(null)
    var error by mutableStateOf<String?>(null)
    var visible by mutableIntStateOf(20)
    val scrolls=ExercisePage.entries.associateWith{androidx.compose.foundation.ScrollState(0)}
    fun setup(request:ExerciseRequest){this.request=request;page=ExercisePage.SETUP;error=null}
    fun back(){error=null;page=if(page==ExercisePage.DETAIL)ExercisePage.HISTORY else ExercisePage.HUB}
}
@Composable internal fun ExerciseScreens(bank:PracticeBank,catalog:ContentCatalog,records:StudyRecords?,failed:Boolean,retry:()->Unit,ui:ExerciseUiState,busy:Boolean,onStart:()->Unit,onResume:(String)->Unit,onEnd:()->Unit,onResult:(String)->Unit) {
    val r=records
    Column(Modifier.widthIn(max=1000.dp).fillMaxSize().verticalScroll(ui.scrolls.getValue(ui.page)).padding(20.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
        StudyHeading(when(ui.page){ExercisePage.HUB->"Exercise";ExercisePage.SETUP->if(ui.request.mode==ExerciseMode.MIXED)"Set up an exercise" else ui.request.mode.label;ExercisePage.HISTORY->"Exercise history";ExercisePage.DETAIL->"Exercise details"})
        if(r==null){ProgressUnavailable(failed,retry);return@Column}
        ui.error?.let {StudyCard{Text(it,color=MaterialTheme.colorScheme.error,modifier=Modifier.semantics{liveRegion=LiveRegionMode.Polite});TextButton({ui.error=null}){Text("Dismiss")}}}
        val summary=r.summary(catalog)
        val active=r.sessions.singleOrNull{it.status=="active"}
        when(ui.page) {
            ExercisePage.HUB->{
                Text("Put your knowledge into practice.")
                StudyCard {
                    Text("${summary.answered} / ${summary.questionTotal}",style=MaterialTheme.typography.headlineLarge);Text("Unique questions answered")
                    LinearProgressIndicator(progress={if(summary.questionTotal==0)0f else summary.answered.toFloat()/summary.questionTotal},modifier=Modifier.fillMaxWidth())
                    Text("${summary.correct} correct on latest attempt · ${summary.revisit} to revisit")
                    if(active==null)StudyAction("Start an exercise",!busy){ui.setup(ExerciseRequest())}
                }
                if(active!=null)StudyCard(true){
                    Text("EXERCISE IN PROGRESS",style=MaterialTheme.typography.labelLarge)
                    Text(ExerciseRequest.decode(r.value("mode:${active.id}")).label,style=MaterialTheme.typography.headlineSmall)
                    Text("${r.attempts.count{it.sessionId==active.id}} of ${r.questions.count{it.sessionId==active.id}} questions answered")
                    Text(if(active.deferred)"Answers will be shown at the end." else "Answers are explained after each question.")
                    StudyAction("Resume exercise",!busy){onResume(active.id)}
                    OutlinedButton(onEnd,enabled=!busy,modifier=Modifier.fillMaxWidth()){Text("End this exercise")}
                }
                StudyRow("Practise unanswered",if(summary.answered==summary.questionTotal)"All current questions answered" else "${summary.questionTotal-summary.answered} questions remaining",active==null && !busy && summary.answered<summary.questionTotal){ui.setup(ExerciseRequest(ExerciseMode.UNANSWERED))}
                StudyRow("Review mistakes",if(summary.revisit==0)"No mistakes to review yet" else "${summary.revisit} ${if(summary.revisit==1)"question" else "questions"} to revisit",active==null && !busy && summary.revisit>0){ui.setup(ExerciseRequest(ExerciseMode.REVIEW))}
                Text("Recent exercises",style=MaterialTheme.typography.headlineSmall,modifier=Modifier.semantics{heading()})
                val recent=r.sessions.filter{it.status!="active"}.take(3)
                if(recent.isEmpty())Text("Your completed and ended exercises will appear here.")
                recent.forEach{s->HistoryRow(s,r,!busy){if(s.status=="completed")onResult(s.id) else {ui.detail=s.id;ui.page=ExercisePage.DETAIL}}}
                TextButton({ui.page=ExercisePage.HISTORY}){Text("View exercise history")}
                Text("Choose 1–70 questions per exercise, subject to the available learning points.",style=MaterialTheme.typography.bodySmall)
            }
            ExercisePage.SETUP->{
                if(active!=null){Text("Finish or end your current exercise before starting another.");StudyAction("Resume exercise",!busy){onResume(active.id)};OutlinedButton(onEnd,enabled=!busy){Text("End this exercise")};return@Column}
                ChoiceMenu("Practice type",ui.request.mode.label,ExerciseMode.entries.map{it.label to {
                    ui.request=ExerciseRequest(it,if(it==ExerciseMode.CHAPTER)readerModules.first().id.value else null,if(it==ExerciseMode.CATEGORY)Category.entries.first() else null)
                }})
                if(ui.request.mode==ExerciseMode.CHAPTER)ChoiceMenu("Chapter",readerModules.single{it.id.value==ui.request.chapter}.title,readerModules.map{m->m.title to {ui.request=ui.request.copy(chapter=m.id.value)}})
                if(ui.request.mode!=ExerciseMode.MIXED && ui.request.mode!=ExerciseMode.CHAPTER)ChoiceMenu("Category",ui.request.category?.title ?: "All categories",listOf("All categories" to {ui.request=ui.request.copy(category=null)})+Category.entries.map{c->c.title to {ui.request=ui.request.copy(category=c)}})
                val pool=exercisePool(bank,ui.request,r,catalog);val capacity=pool.map{it.conceptId}.distinct().size.coerceAtMost(70)
                if(capacity==0){StudyCard(true){Text(if(ui.request.mode==ExerciseMode.REVIEW)"No mistakes to review" else "No questions in this pool",style=MaterialTheme.typography.headlineSmall);Text("Choose another mode or category to keep practising.");StudyAction("Choose another mode"){ui.request=ExerciseRequest()}};return@Column}
                val targeted=ui.request.mode!=ExerciseMode.MIXED
                if(targeted)StudyCard(true){Text("${pool.size} eligible ${if(pool.size==1)"question covers" else "questions cover"} ${pool.map{it.conceptId}.distinct().size} distinct ${if(pool.map{it.conceptId}.distinct().size==1)"learning point" else "learning points"}. ${if(capacity==1)"This exercise has 1 question." else "Choose 1–$capacity questions."}");Text("One question per learning point in this exercise.",style=MaterialTheme.typography.bodySmall)}
                LaunchedEffect(ui.request,capacity){if((ui.count.toIntOrNull() ?: 0)>capacity)ui.count=capacity.toString()}
                Text("How many questions?",style=MaterialTheme.typography.titleLarge)
                OutlinedTextField(ui.count,{ui.count=it},label={Text("Questions (1–$capacity)")},singleLine=true,keyboardOptions=KeyboardOptions(keyboardType=KeyboardType.Number),modifier=Modifier.fillMaxWidth())
                FlowRow(horizontalArrangement=Arrangement.spacedBy(8.dp)){listOf(1,10,20,40,70,capacity).distinct().sorted().filter{it<=capacity}.forEach{n->FilterChip(ui.count==n.toString(),{ui.count=n.toString()},label={Text(n.toString())})}}
                Text("Show answers",style=MaterialTheme.typography.titleLarge)
                Feedback.entries.forEach{f->OutlinedCard({ui.feedback=f},modifier=Modifier.fillMaxWidth().semantics{role=Role.RadioButton;selected=ui.feedback==f},colors=CardDefaults.outlinedCardColors(containerColor=if(ui.feedback==f)MaterialTheme.colorScheme.secondaryContainer else MaterialTheme.colorScheme.surface)) {
                    Row(Modifier.padding(12.dp).heightIn(min=48.dp),verticalAlignment=androidx.compose.ui.Alignment.CenterVertically){RadioButton(ui.feedback==f,null);Spacer(Modifier.width(8.dp));Text(if(f==Feedback.IMMEDIATE)"After each question" else "At the end")}
                }}
                if(ui.feedback==Feedback.AT_END)Text("At the end: coverage and results update only when you finish.")
                if(targeted)Text("Targeted practice uses this pool, not the mixed question distribution.",style=MaterialTheme.typography.bodySmall)
                else {
                    var mix by remember{mutableStateOf(false)}
                    TextButton({mix=!mix}){Text(if(mix)"Hide question mix" else "View question mix")}
                    if(mix){val allocation=QuizEngine.allocation((ui.count.toIntOrNull() ?: 1).coerceIn(1,70));allocation.categories.forEach{(c,n)->Text("${c.title}: $n")};Text("Random from any category: ${allocation.random}")}
                }
                val size=ui.count.toIntOrNull();val allowed=size!=null && size in 1..capacity && (targeted || practiceStartCheck(ui.count,bank).allowed)
                if(!allowed)Text("Choose a valid number from 1 to $capacity.",color=MaterialTheme.colorScheme.error)
                StudyAction("Start ${ui.count} ${if(ui.count=="1")"question" else "questions"}",allowed && !busy,onStart)
            }
            ExercisePage.HISTORY->{
                val history=r.sessions.filter{it.status!="active"}
                if(history.isEmpty())Text("Your completed and ended exercises will appear here.")
                history.take(ui.visible).forEach{s->HistoryRow(s,r,!busy){if(s.status=="completed")onResult(s.id) else {ui.detail=s.id;ui.page=ExercisePage.DETAIL}}}
                if(history.size>ui.visible)OutlinedButton({ui.visible+=20}){Text("Load more")}
            }
            ExercisePage.DETAIL->{
                val s=r.sessions.singleOrNull{it.id==ui.detail}
                if(s==null)Text("This exercise is unavailable.") else StudyCard {
                    Text(ExerciseRequest.decode(r.value("mode:${s.id}")).label,style=MaterialTheme.typography.headlineSmall)
                    Text(if(r.value("unavailable:${s.id}")=="1")"Unavailable content · History kept" else "Ended early · ${r.attempts.count{it.sessionId==s.id}} of ${r.questions.count{it.sessionId==s.id}} answered")
                    Text("This partial exercise has no completed score.")
                    if(s.deferred)Text("Its deferred answers were not added to coverage or review progress.")
                }
                TextButton({ui.page=ExercisePage.HISTORY}){Text("Back to exercise history")}
            }
        }
    }
}
@Composable private fun ChoiceMenu(label:String,value:String,choices:List<Pair<String,()->Unit>>) {
    var expanded by remember {mutableStateOf(false)}
    Box {StudyRow(label,value){expanded=true};DropdownMenu(expanded,{expanded=false},modifier=Modifier.heightIn(max=420.dp)){choices.forEach{(text,action)->DropdownMenuItem(text={Text(text)},onClick={action();expanded=false})}}}
}
@Composable private fun HistoryRow(s:Session,r:StudyRecords,enabled:Boolean,onClick:()->Unit) {
    val answers=r.attempts.filter{it.sessionId==s.id};val questions=r.questions.filter{it.sessionId==s.id}
    // Only authenticated current snapshots can expose a score. Older content remains historical.
    val current=questions.all{q->acceptedQuestions9J.any{it.key.questionId.value==q.questionId && it.key.revision.value==q.revision && it.feedback.correctOptionId.value==q.correctOption}}
    val detail=if(r.value("unavailable:${s.id}")=="1")"Unavailable content · History kept" else if(s.status=="completed" && current)"Completed · ${answers.count{a->questions.single{it.position==a.position}.correctOption==a.selectedOption}} / ${questions.size} correct"
        else if(s.status=="completed")"Completed · Earlier content; results unavailable" else "Ended early · ${answers.size} of ${questions.size} answered"
    val date=if(s.createdAt==0L)"Date unavailable" else Instant.fromEpochMilliseconds(s.createdAt).toString().take(10)+" UTC"
    StudyRow(ExerciseRequest.decode(r.value("mode:${s.id}")).label,"$detail\n$date",enabled,onClick)
}

@org.jetbrains.compose.ui.tooling.preview.Preview(name="History · unavailable exercise",widthDp=390,heightDp=140)
@Composable private fun HistoryRowPreview() {
    val session=Session("preview","preview","earlier-package",true,"[]",status="abandoned")
    val records=StudyRecords(sessions=listOf(session),metadata=listOf(StoreMetadata("unavailable:preview","1")))
    LearningTheme {HistoryRow(session,records,true){}}
}
