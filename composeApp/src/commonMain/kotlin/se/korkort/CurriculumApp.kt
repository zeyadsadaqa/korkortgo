@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)
package se.korkort

import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.roundToInt
import kotlinx.coroutines.*
import se.korkort.progress.*

private val Forest=Color(0xFF173E32)
private val Paper=Color(0xFFF7F8F3)
private val Sage=Color(0xFFE7EEE5)
private val Muted=Color(0xFF61706B)
private val Line=Color(0xFFD5DED5)
/** UI projection; production learner writes pass through the durable study adapter. */
@Composable internal fun CurriculumApp(bank: PracticeBank, summary: CurriculumSummary = CurriculumSummary("2026 curriculum",readerModules.size,readerModules.sumOf{it.lessonIds.size},bank.questions.count{it.acceptance.eligibility==ScoringEligibility.ACCEPTED},navigationSigns.size), fixtureBank: Boolean = false) {
    require(summary.questions==bank.questions.count{it.acceptance.eligibility==ScoringEligibility.ACCEPTED})
    require(summary.modules==readerModules.size && summary.lessons==readerModules.sumOf{it.lessonIds.size} && summary.signEntries==navigationSigns.size)
    val environment=LocalStudy.current
    val workspace=rememberStudyWorkspace(environment?.study?.token?.generation ?: "fixture",environment?.notice)
    var state by workspace.state
    var learningRoute by workspace.learningRoute
    var lastLearning by workspace.lastLearning
    var lastExercise by workspace.lastExercise
    val questionViews=workspace.questionViews
    val homeScroll=workspace.homeScroll
    val setupScroll=workspace.setupScroll
    val resultsScroll=workspace.resultsScroll
    val reviewSourceScrolls=workspace.reviewSourceScrolls
    val exerciseUi=workspace.exerciseUi
    val dataUi=workspace.dataUi
    var showData by workspace.showData
    var records by remember {mutableStateOf<StudyRecords?>(null)}
    var recordsFailed by remember {mutableStateOf(false)}
    var refresh by remember {mutableIntStateOf(0)}
    LaunchedEffect(environment,refresh) {
        if(environment!=null)while(isActive) {
            try {records=environment.study.repository.records(environment.study.token);recordsFailed=false}
            catch(e:CancellationException){throw e}
            catch(e:Exception){records=null;recordsFailed=true;try{environment.refreshGeneration()}catch(refreshError:Exception){if(refreshError is CancellationException)throw refreshError}}
            delay(1500)
        }
    }
    val homeData=remember(records,environment){if(records!=null && environment!=null)dashboard(records!!,environment.study) else null}
    var initializing by remember { mutableStateOf(environment!=null) }
    var savedUnavailable by remember { mutableStateOf(false) }
    LaunchedEffect(environment) {
        environment?.save {
            try {
                val saved=environment.study.active()
                if(saved!=null && state.pinned==null) state=state.copy(pinned=saved,navigation=GuardedNavigation(state.navigation.current,saved.navigation))
                else if(saved!=null && state.pinned?.id==saved.id)state=state.copy(pinned=saved)
            } catch(e:IllegalArgumentException) {savedUnavailable=true}
            initializing=false
        }
    }
    fun resumeId(id:String) {environment?.save {state=environment.study.quizState(id)}}
    fun resumeSaved() { val id=records?.sessions?.singleOrNull{it.status=="active"}?.id ?: state.pinned?.id; if(id!=null)resumeId(id) }
    fun endSaved() { environment?.save {
        environment.study.endActive(); savedUnavailable=false;exerciseUi.page=ExercisePage.HUB
        state=TransientQuizState(navigation=GuardedNavigation(AppDestination.QuizSetup,null))
    } }
    val library = workspace.library
    var sourceFailure by workspace.sourceFailure
    var sourceOrigin by workspace.sourceOrigin
    var restoreReviewSource by workspace.restoreReviewSource
    var reviewSource by workspace.reviewSource
    val uri = LocalUriHandler.current
    val destination = state.navigation.current
    val practice = state.pinned
    LaunchedEffect(practice?.id){questionViews.keys.removeAll{it.sessionId!=practice?.id}}
    val reviewScroll = workspace.reviewScroll
    LaunchedEffect(practice?.id,state.review?.filter) { reviewScroll.scrollToItem((state.review?.row ?: 0).let{if(it==0)0 else it+1}) }
    SideEffect {
        when(tabFor(destination)) { StudyTab.LEARNING->lastLearning=destination;StudyTab.EXERCISE->lastExercise=destination;else->Unit }
    }
    fun navigate(target: AppDestination, intent: NavigationIntent = NavigationIntent.GENERAL, restoreTab: Boolean=false) {
        if(environment?.busy==true || initializing)return
        state = if(environment!=null) state.copy(navigation=GuardedNavigation(target,state.pinned?.navigation))
            else state.request(NavigationRequest(target,intent)).first
        if(state.navigation.pending==null) {
            if(!restoreTab){reviewSource=null;restoreReviewSource=null;sourceOrigin=null}
            if(!restoreTab && state.navigation.current==target) {
                if(target==AppDestination.Library || target is AppDestination.Content || target==AppDestination.SignCatalogue)
                    learningRoute=LearningRouteState((target as? AppDestination.Content)?.let{canonicalResolver.canonical(it.target)},target==AppDestination.SignCatalogue)
            }
        }
    }
    fun setup() {
        exerciseUi.page=ExercisePage.HUB
        if(environment?.busy==true || initializing)return
        state=if(environment!=null)state.copy(navigation=GuardedNavigation(AppDestination.QuizSetup,state.pinned?.navigation)) else state.showSetup()
        if(state.navigation.pending==null){reviewSource=null;restoreReviewSource=null;sourceOrigin=null}
    }
    fun returnToReviewSource() {
        restoreReviewSource=sourceOrigin?.let{key->reviewSource?.let{id->key to id}}
        reviewSource=null
    }
    fun source(id: SourceReferenceId) {
        if(environment!=null) sourceFailure=runCatching{uri.openUri(navigationSources.references.single{it.id==id}.url)}.isFailure
        else state=state.request(NavigationRequest(state.navigation.current,NavigationIntent.SOURCE,sourceReferenceId=id)).first
    }
    LaunchedEffect(state.navigation.sourceToOpen) {
        val (id, consumed) = state.takeSourceToOpen()
        if(id!=null) {
            state=consumed
            val reference=navigationSources.references.single {it.id==id}
            sourceFailure=runCatching {uri.openUri(reference.url)}.isFailure
        }
    }
    LearningTheme { RootModalHost {
        AppChrome(destination,{tab->navigate(when(tab){StudyTab.HOME->AppDestination.Home;StudyTab.LEARNING->lastLearning;StudyTab.EXERCISE->lastExercise},restoreTab=true)},destination!=AppDestination.Home || showData,{
            if(destination==AppDestination.Home && showData) {if(!dataUi.back())showData=false}
            else if(environment!=null && destination==AppDestination.QuizSetup && exerciseUi.page!=ExercisePage.HUB)exerciseUi.back()
            else if(reviewSource!=null && tabFor(destination)==StudyTab.EXERCISE)returnToReviewSource()
            else if(tabFor(destination)==StudyTab.LEARNING && learningRoute.canBack)learningRoute.back()
            else if(destination is AppDestination.Quiz || destination is AppDestination.Results)setup()
            else if(destination is AppDestination.Review && practice!=null)navigate(AppDestination.Results(practice.id))
            else navigate(AppDestination.Home,restoreTab=true)
        },showBack=(destination==AppDestination.Home && showData) || (tabFor(destination)==StudyTab.LEARNING && learningRoute.canBack) || (tabFor(destination)==StudyTab.EXERCISE && (destination!=AppDestination.QuizSetup || environment!=null && exerciseUi.page!=ExercisePage.HUB))) {
            if(environment?.failure!=null) {
                Surface(color=MaterialTheme.colorScheme.errorContainer) { Column(Modifier.fillMaxWidth().padding(16.dp)) {
                    Text(if(destination is AppDestination.Quiz)"Answer not saved" else "Progress not saved",style=MaterialTheme.typography.titleMedium)
                    Text(environment.failure!!)
                    Button({environment.retry()},enabled=!environment.busy){Text("Retry saving")}
                } }
            }
            if(savedUnavailable) Column(Modifier.padding(16.dp)) {
                Text("Your saved exercise uses content that is no longer available. End it to start a new one.")
                Button(::endSaved,enabled=environment?.busy!=true){Text("End this exercise")}
            }
            Box(Modifier.weight(1f).fillMaxWidth(),contentAlignment=Alignment.TopCenter) {
                if(state.recovery==PracticeRecovery.MISSING_RESULT) {
                    MissingResults {setup()}
                } else if(state.recovery==PracticeRecovery.MISSING_QUIZ) {
                    Column(Modifier.padding(24.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
                        Text("No active test is available.")
                        Primary("Set up a practice test"){setup()}
                    }
                } else if(reviewSource!=null && tabFor(destination)==StudyTab.EXERCISE) {
                    SourceDetail(reviewSource!!,::returnToReviewSource,::returnToReviewSource,{reference->source(reference.id);true},backLabel="Back to answer review",returnLabel="Return to answer review",scroll=reviewSourceScrolls.getOrPut(reviewSource!!){androidx.compose.foundation.ScrollState(0)})
                } else when(val page=destination) {
                    AppDestination.Home -> if(environment!=null) {
                        if(showData)DataControls(environment,records,dataUi){showData=false;navigate(AppDestination.Library)}
                        else HomeDashboard(homeData,recordsFailed,{refresh++},homeScroll,{navigate(AppDestination.Library)},{exerciseUi.page=ExercisePage.HUB;navigate(AppDestination.QuizSetup)},{step->
                            when {
                                step.resume!=null->resumeId(step.resume)
                                step.lesson!=null->navigate(AppDestination.Content(ContentTarget(step.lesson)))
                                step.request!=null->{exerciseUi.setup(step.request);navigate(AppDestination.QuizSetup)}
                            }
                        },{chapter->library.expanded=setOf(chapter.id);library.progressInitialized=true;navigate(AppDestination.Library)},{showData=true})
                    } else LazyColumn(state=homeScroll,modifier=Modifier.widthIn(max=1160.dp).fillMaxSize(),contentPadding=PaddingValues(24.dp),verticalArrangement=Arrangement.spacedBy(20.dp)) {
                        if(environment!=null && practice?.assessment?.finished==false) item { SavedExercise(practice,environment.busy,::resumeSaved,::endSaved) }
                        item {AdaptiveColumns({
                            Eyebrow("YOUR SWEDISH DRIVING JOURNEY");Heading("Your road to\nconfidence.",true)
                            Text("Learn the rules. Understand the why. Practise at your pace.",color=Muted,fontSize=18.sp)
                            Spacer(Modifier.height(24.dp));Primary("Start a practice test  >"){setup()}
                            TextButton({navigate(AppDestination.Library)}){Text("Explore the theory  >")}
                        },{RoadIllustration()})}
                        item {Panel(Sage){FlowRow(horizontalArrangement=Arrangement.spacedBy(32.dp),verticalArrangement=Arrangement.spacedBy(16.dp)){
                            Stat(summary.questions.toString(),"practice questions")
                            Stat(summary.modules.toString(),"modules")
                            Stat(summary.lessons.toString(),"lessons")
                        }}}
                        item {Heading("A little learning. A safer journey.")}
                        item {FlowRow(horizontalArrangement=Arrangement.spacedBy(12.dp),verticalArrangement=Arrangement.spacedBy(12.dp)){
                            Category.entries.forEach {category->Surface(onClick={library.filter=LibraryFilter(category=category);navigate(AppDestination.Library)},shape=RoundedCornerShape(14.dp),border=BorderStroke(1.dp,Line),modifier=Modifier.widthIn(min=175.dp,max=210.dp).heightIn(min=125.dp)){
                                Column(Modifier.padding(20.dp)){Text(categoryIcon(category));Spacer(Modifier.height(12.dp));Text(category.title,fontWeight=FontWeight.SemiBold);Text("Explore  >")}
                            }}
                        }}
                        item {Text(summary.releaseLabel,color=Muted)}
                        item {Text("KörkortGo original curriculum and explained practice. This is a learning aid, not an official examination.",color=Muted)}
                    }
                    AppDestination.Library, AppDestination.SignCatalogue, is AppDestination.Content -> Column(Modifier.fillMaxSize()) {
                        if(practice?.assessment?.finished==true && state.review!=null) TextButton({state=state.openReview()}){Text("Return to answer review")}
                        Box(Modifier.weight(1f)) {LearningRoute((page as? AppDestination.Content)?.let{canonicalResolver.canonical(it.target)},libraryState=library,initialReferences=page==AppDestination.SignCatalogue,retainedState=learningRoute){reference->runCatching{uri.openUri(reference.url)}.isSuccess}}
                    }
                    AppDestination.QuizSetup -> if(environment!=null)ExerciseScreens(environment.study,records,recordsFailed,{refresh++},exerciseUi,environment.busy,{
                        environment.save {
                            state=environment.study.start(state.copy(countText=exerciseUi.count,feedback=exerciseUi.feedback),exerciseUi.request)
                        }
                    },::resumeId,::endSaved,{id->
                        environment.scope.launch {
                            try {state=environment.study.quizState(id)}
                            catch(e:CancellationException){throw e}
                            catch(e:Exception){exerciseUi.error="This exercise uses earlier or unavailable content. Its history is retained, but results cannot be opened."}
                        }
                    }) else LazyColumn(state=setupScroll,modifier=Modifier.widthIn(max=1160.dp).fillMaxSize(),contentPadding=PaddingValues(24.dp),verticalArrangement=Arrangement.spacedBy(20.dp)) {
                        if(environment!=null && practice?.assessment?.finished==false) item { SavedExercise(practice,environment.busy,::resumeSaved,::endSaved) }
                        item {Eyebrow("PRACTICE TEST");Heading("Make every question count.")}
                        item {AdaptiveColumns({
                            Panel {Text("1. How many questions?",fontSize=20.sp,fontWeight=FontWeight.Bold)
                                OutlinedTextField(state.countText,{state=state.copy(countText=it)},label={Text("Number of questions (1–70)")},singleLine=true,modifier=Modifier.fillMaxWidth())
                                FlowRow(horizontalArrangement=Arrangement.spacedBy(8.dp)){listOf(10,20,40,70).forEach{n->FilterChip(state.countText==n.toString(),{state=state.copy(countText=n.toString())},label={Text(n.toString())})}}
                            }
                            Spacer(Modifier.height(16.dp));Panel {Text("2. Reveal the answers",fontSize=20.sp,fontWeight=FontWeight.Bold)
                                ModeCard("After each question","See the answer and all four explanations as you go.",state.feedback==Feedback.IMMEDIATE){state=state.copy(feedback=Feedback.IMMEDIATE)}
                                ModeCard("At the end of the test","Finish the test first, then review every answer.",state.feedback==Feedback.AT_END){state=state.copy(feedback=Feedback.AT_END)}
                            }
                        },{
                            Panel(Sage){Text("Your question mix",fontFamily=MaterialTheme.typography.headlineLarge.fontFamily,fontSize=26.sp,fontWeight=FontWeight.Bold)
                                val check=practiceStartCheck(state.countText,bank,fixture=fixtureBank)
                                val mix=QuizEngine.allocation((check.size?:1).coerceIn(1,70))
                                Category.entries.forEach{category->Row(Modifier.fillMaxWidth()){Text(category.title,Modifier.weight(1f));Text(mix.categories.getValue(category).toString())}}
                                Row(Modifier.fillMaxWidth()){Text("Random from any category",Modifier.weight(1f));Text(mix.random.toString())}
                                Text("The extra random questions can belong to any category. No repeated learning point within a test.",fontSize=12.sp)
                                check.errors.forEach{Text(it,color=MaterialTheme.colorScheme.error)}
                                Primary("Start test  >",check.allowed && state.recovery==PracticeRecovery.NONE && !initializing && environment?.busy!=true && !savedUnavailable && (environment==null || practice?.assessment?.finished!=false)){
                                    if(environment==null)state=if(fixtureBank)state.startPracticeFixture(bank)else state.startPractice(bank)
                                    else environment.save { state=environment.study.start(state) }
                                }
                                Text("No time pressure. All questions count towards your practice score.",fontSize=12.sp)
                            }
                        })}
                    }
                    is AppDestination.Quiz -> {
                        if(practice==null || practice.id!=page.sessionId) MissingPractice {setup()}
                        else Column(Modifier.widthIn(max=900.dp).fillMaxSize().padding(horizontal=16.dp,vertical=24.dp),verticalArrangement=Arrangement.spacedBy(12.dp)) {
                            val assessment=practice.assessment
                            Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.SpaceBetween){Eyebrow("PRACTICE TEST");TextButton({setup()}){Text(if(environment==null)"End test" else "Pause exercise")}}
                            LinearProgressIndicator(progress={assessment.index.toFloat()/assessment.snapshots.size},modifier=Modifier.fillMaxWidth())
                            Text("Question ${assessment.index+1} of ${assessment.snapshots.size}")
                            Box(Modifier.weight(1f)){CompositionLocalProvider(LocalQuestionUi provides questionViews.getOrPut(practice.token){QuestionUiState()}) {PinnedAssessmentCard(practice,trailingContent={
                                if(assessment.presentation().explanation!=null) {
                                    val question=assessment.current.question
                                    TextButton({navigate(AppDestination.Content(ContentTarget(question.relationship.primaryLessonId)),NavigationIntent.RELATED_READING)}){Text("Read the related lesson")}
                                    question.relationship.sourceUses.map{it.referenceId}.distinct().forEach{id->TextButton({source(id)}){Text(navigationSources.references.single{it.id==id}.title)}}
                                }
                            }){token,option->
                                if(environment==null)state=state.select(token,option).confirm(token)
                                else environment.save { state=environment.study.confirm(practice,option) }}}}
                            if(assessment.currentAnswer!=null)Primary(if(assessment.index==assessment.snapshots.lastIndex)"Finish test  >" else "Next question  >"){if(environment==null)state=state.nextQuestion() else environment.save { state=environment.study.next(practice) }}
                            else Text(if(assessment.feedbackMode==Feedback.AT_END)"Answers revealed at the end" else "Answers explained after each question",fontSize=12.sp,color=Muted)
                        }
                    }
                    is AppDestination.Results -> {
                        if(practice==null || practice.id!=page.sessionId || !practice.assessment.finished)MissingResults {setup()}
                        else LazyColumn(Modifier.widthIn(max=1160.dp).fillMaxSize(),state=resultsScroll,contentPadding=PaddingValues(24.dp),verticalArrangement=Arrangement.spacedBy(20.dp)){
                            val assessment=practice.assessment;val score=requireNotNull(assessment.score)
                            item {Eyebrow("TEST COMPLETE");Heading("Every question is\na step forward.");Text("Take a moment to understand what you missed.")}
                            item {AdaptiveColumns({Panel(Sage){Text("$score / ${assessment.snapshots.size}",fontFamily=MaterialTheme.typography.headlineLarge.fontFamily,fontSize=64.sp,fontWeight=FontWeight.Bold);Text("${(100.0*score/assessment.snapshots.size).roundToInt()}% correct",fontSize=22.sp);Text("$score correct · ${assessment.snapshots.size-score} to revisit");Primary("Review answers  >"){state=state.openReview()};OutlinedButton({setup()}){Text("Take another test")};Text("Practice score · not an official exam result",fontSize=12.sp)}},{Panel{
                                Text("Results by category",fontFamily=MaterialTheme.typography.headlineLarge.fontFamily,fontSize=25.sp)
                                Category.entries.forEach{category->val positions=assessment.snapshots.indices.filter{assessment.snapshots[it].question.category==category};val correct=positions.count{assessment.snapshots[it].isCorrect(assessment.answers[it])};Row(Modifier.fillMaxWidth()){Text(category.title,Modifier.weight(1f));Text("$correct / ${positions.size}")};LinearProgressIndicator(progress={if(positions.isEmpty())0f else correct.toFloat()/positions.size},modifier=Modifier.fillMaxWidth())}
                            }})}
                        }
                    }
                    is AppDestination.Review -> {
                        if(practice==null || practice.id!=page.sessionId || !practice.assessment.finished)MissingResults {setup()}
                        else Column(Modifier.widthIn(max=900.dp).fillMaxSize().padding(horizontal=16.dp,vertical=24.dp),verticalArrangement=Arrangement.spacedBy(12.dp)) {
                            val positions=state.reviewPositions()
                            LazyColumn(Modifier.weight(1f),state=reviewScroll,verticalArrangement=Arrangement.spacedBy(12.dp)) {
                                item(key="review-heading") {
                                    Column(verticalArrangement=Arrangement.spacedBy(12.dp)) {
                                        Heading("Understand every answer.")
                                        TextButton({navigate(AppDestination.Results(practice.id))}){Text("Back to results")}
                                        FlowRow(horizontalArrangement=Arrangement.spacedBy(8.dp)){PracticeReviewFilter.entries.forEach{filter->FilterChip(state.review?.filter==filter,{restoreReviewSource=null;state=state.filterReview(filter)},label={Text(filter.name.lowercase().replaceFirstChar{it.uppercase()})})}}
                                        if(positions.isEmpty())Text("No answers in this filter.")
                                    }
                                }
                                items(positions,key={practice.assessment.snapshots[it].question.key.let{key->"${key.questionId.value}/${key.revision.value}"}}){position->val snapshot=practice.assessment.snapshots[position];val key=snapshot.question.key
                                    OutlinedCard(Modifier.fillMaxWidth()){Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(8.dp)){
                                        Text(snapshot.question.prompt.assessmentText(),style=MaterialTheme.typography.titleMedium,modifier=Modifier.semantics{heading()})
                                        val expanded=key in state.review!!.expanded
                                        TextButton({restoreReviewSource=null;state=state.moveReview(positions.indexOf(position)).expandReview(key)}){Text(if(expanded)"Hide explanation ↑" else "Review all four options ↓")}
                                        if(expanded)LearningAnswerReview(practice.assessment,position,{target->state=state.moveReview(positions.indexOf(position));navigate(AppDestination.Content(target),NavigationIntent.RELATED_READING)},{id->state=state.moveReview(positions.indexOf(position));restoreReviewSource=null;sourceOrigin=key;reviewSource=id},scrollable=false,showPrompt=false,restoreSourceFocus=restoreReviewSource?.takeIf{it.first==key}?.second)
                                    }}
                                }
                            }
                            Primary("Take another test  >"){setup()}
                        }
                    }
                }
            }
        }
        if(state.navigation.pending!=null)RootAlertDialog("Leave this test?","Your unfinished answers will be discarded. You can start a fresh test whenever you are ready.","Keep practising","Leave test",{state=state.cancelExit()},{state=state.discardExit()})
        if(sourceFailure)RootAlertDialog("Could not open the source","Your current page is still available. Return and try the link again.",null,"Return",{sourceFailure=false},{sourceFailure=false})
    }}
}

@Composable private fun MissingPractice(onSetup:()->Unit) {Column(Modifier.padding(24.dp)){Text("No active test is available.");TextButton(onSetup){Text("Set up a practice test")}}}

@Composable private fun Nav(label:String,active:Boolean,onClick:()->Unit) {
    Column(Modifier.width(IntrinsicSize.Min)) {
        TextButton(onClick=onClick) { Text(label,color=Forest,fontWeight=if(active)FontWeight.Bold else FontWeight.Normal) }
        if(active) HorizontalDivider(color=Forest,thickness=3.dp)
    }
}
@Composable private fun Eyebrow(text:String) { Text(text.uppercase(),fontSize=11.sp,letterSpacing=1.3.sp,color=Muted,fontWeight=FontWeight.SemiBold,modifier=Modifier.padding(bottom=10.dp)) }
@Composable private fun Heading(text:String,large:Boolean=false) { Text(text,fontFamily=MaterialTheme.typography.headlineLarge.fontFamily,fontWeight=FontWeight.Bold,fontSize=if(large)48.sp else 36.sp,lineHeight=if(large)54.sp else 43.sp,color=Forest,modifier=Modifier.padding(bottom=16.dp).semantics{heading()}) }
@Composable private fun Primary(text:String,enabled:Boolean=true,onClick:()->Unit) { Button(onClick=onClick,enabled=enabled,shape=RoundedCornerShape(9.dp),contentPadding=PaddingValues(horizontal=24.dp,vertical=16.dp),modifier=Modifier.heightIn(min=52.dp)) {Text(text,fontWeight=FontWeight.SemiBold)} }
@Composable private fun Panel(color:Color=Color.White,content:@Composable ColumnScope.()->Unit) { Surface(color=color,shape=RoundedCornerShape(16.dp),border=BorderStroke(1.dp,Line),modifier=Modifier.fillMaxWidth()) { Column(Modifier.padding(24.dp),verticalArrangement=Arrangement.spacedBy(14.dp),content=content) } }
@Composable private fun Stat(value:String,label:String) { Column {Text(value,fontFamily=MaterialTheme.typography.headlineLarge.fontFamily,fontWeight=FontWeight.Bold,fontSize=30.sp,color=Forest);Text(label,color=MaterialTheme.colorScheme.onSurfaceVariant,fontSize=13.sp)} }
@Composable private fun AdaptiveColumns(left:@Composable ColumnScope.()->Unit,right:@Composable ColumnScope.()->Unit) { BoxWithConstraints(Modifier.fillMaxWidth()) { if(maxWidth>760.dp) Row(horizontalArrangement=Arrangement.spacedBy(28.dp)) {Column(Modifier.weight(1.2f),content=left);Column(Modifier.weight(1f),content=right)} else Column(verticalArrangement=Arrangement.spacedBy(24.dp)) {Column(content=left);Column(content=right)} } }
@Composable private fun ModeCard(title:String,description:String,selected:Boolean,onClick:()->Unit) { Surface(onClick=onClick,color=if(selected)Sage else Color.White,border=BorderStroke(1.dp,if(selected)Forest else MaterialTheme.colorScheme.outline),shape=RoundedCornerShape(10.dp),modifier=Modifier.fillMaxWidth().semantics {role=Role.RadioButton;this.selected=selected}) {Row(Modifier.padding(16.dp),verticalAlignment=Alignment.CenterVertically) {RadioButton(selected=selected,onClick=null);Column(Modifier.padding(start=8.dp)) {Text(title,fontWeight=FontWeight.SemiBold);Text(description,fontSize=13.sp,lineHeight=19.sp,color=MaterialTheme.colorScheme.onSurfaceVariant)}}} }
private fun categoryIcon(c:Category)=when(c){Category.VEHICLE->"01";Category.ENVIRONMENT->"02";Category.SAFETY->"03";Category.RULES->"04";Category.PERSONAL->"05"}
@Composable private fun RoadIllustration() {Canvas(Modifier.fillMaxWidth().height(300.dp).background(Sage,RoundedCornerShape(24.dp)).semantics {contentDescription="Illustration of a winding road through a quiet landscape"}) {
    val w=size.width;val h=size.height
    drawCircle(Color(0xFFF3D77F),radius=h*.12f,center=Offset(w*.77f,h*.2f))
    val hill=Path().apply {moveTo(0f,h*.65f);cubicTo(w*.25f,h*.2f,w*.65f,h*.8f,w,h*.4f);lineTo(w,h);lineTo(0f,h);close()};drawPath(hill,Color(0xFFB9CBB6))
    val road=Path().apply {moveTo(w*.55f,h*1.1f);cubicTo(w*.03f,h*.58f,w*.95f,h*.6f,w*.5f,h*.16f)}
    drawPath(road,Color(0xFFF9FAF4),style=Stroke(width=w*.15f,cap=StrokeCap.Round));drawPath(road,Color(0xFF7A8A80),style=Stroke(width=w*.12f,cap=StrokeCap.Round));drawPath(road,Color(0xFFF6E7A0),style=Stroke(width=2.dp.toPx()))
    listOf(.13f to .63f,.22f to .38f,.82f to .68f,.89f to .49f,.71f to .37f).forEach { (x,y)->val tree=Path().apply {moveTo(w*x,h*(y-.17f));lineTo(w*(x-.055f),h*y);lineTo(w*(x+.055f),h*y);close()};drawPath(tree,Forest);drawLine(Forest,Offset(w*x,h*y),Offset(w*x,h*(y+.05f)),3.dp.toPx())}
} }

@Composable private fun SavedExercise(practice: PinnedPractice,busy: Boolean,onResume:()->Unit,onEnd:()->Unit) {
    Panel(Sage) {
        Text("Exercise in progress",style=MaterialTheme.typography.headlineSmall)
        Text("Mixed practice",style=MaterialTheme.typography.titleLarge)
        Text("${practice.assessment.answers.size} of ${practice.assessment.snapshots.size} questions answered")
        LinearProgressIndicator(progress={practice.assessment.answers.size.toFloat()/practice.assessment.snapshots.size},modifier=Modifier.fillMaxWidth())
        Text(if(practice.assessment.feedbackMode==Feedback.AT_END)"Answers will be shown at the end." else "Continue where you left off.")
        Primary("Resume exercise",!busy,onResume)
        OutlinedButton(onEnd,enabled=!busy){Text("End this exercise")}
        Text("Your confirmed answers are saved on this device.")
    }
}
