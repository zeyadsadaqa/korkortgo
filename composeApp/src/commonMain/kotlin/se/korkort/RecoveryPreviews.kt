package se.korkort

import androidx.compose.runtime.Composable
import androidx.compose.material3.Text
import org.jetbrains.compose.ui.tooling.preview.Preview
import se.korkort.progress.*

/** All previews are immutable fixtures; none opens or modifies learner storage. */
private fun previewDashboard():Dashboard {
    val summary=ProgressSummary(0,readerModules.size,0,readerModules.sumOf{it.lessonIds.size},0,acceptedQuestions9J.size,0,0)
    return Dashboard(StudyRecords(),summary,NextStudyStep("Start chapter 1","Your route into driving","Start learning",lesson=readerModules.first().lessonIds.first()))
}
private fun previewCatalog()=ContentCatalog("preview",readerModules.associate{it.id.value to it.lessonIds.map{l->l.value}},readerDocuments.filter{it.kind==DocumentKind.LESSON}.associate{it.id.value to it.revision.value},acceptedQuestions9J.associate{it.key.questionId.value to it.key.revision.value})
@Preview(name="Curriculum · Home",widthDp=390,heightDp=844)
@Composable internal fun CurriculumAppPreview() {CurriculumApp(acceptedPracticeBank9J,previewDashboard=previewDashboard())}

@Preview(name="Reader · position recovery",widthDp=390,heightDp=844)
@Composable internal fun LessonReaderRecoveryPreview() {
    LearningTheme {RootModalHost {LessonReader(ContentTarget(readerModules.first().lessonIds.first()),{},{_,_->},{},notice="Your saved position has moved. Showing the start of this lesson.")}}
}
@Preview(name="Progress host · loading",widthDp=390,heightDp=844)
@Composable internal fun ProgressHostPreview() {ProgressHost(previewFailure=false)}

@Preview(name="Progress recovery · unavailable store",widthDp=390,heightDp=844)
@Composable internal fun ProgressRecoveryScreenPreview() {ProgressRecoveryScreen(true,false,{},{},{})}

@Preview(name="Progress recovery · confirmed reset",widthDp=390,heightDp=844)
@Composable internal fun ProgressResetRecoveryPreview() {ProgressRecoveryScreen(true,true,{},{},{})}

@Preview(name="Exercise · empty review pool",widthDp=390,heightDp=844)
@Composable internal fun ExerciseScreensPreview() {
    val ui=ExerciseUiState().apply{page=ExercisePage.SETUP;request=ExerciseRequest(ExerciseMode.REVIEW)}
    LearningTheme {ExerciseScreens(acceptedPracticeBank9J,previewCatalog(),StudyRecords(),false,{},ui,false,{},{},{},{})}
}
@Preview(name="Exercise · unavailable history",widthDp=390,heightDp=844)
@Composable internal fun ExerciseUnavailablePreview() {
    val session=Session("preview","preview","earlier-package",true,"[]",status="abandoned")
    val records=StudyRecords(sessions=listOf(session),metadata=listOf(StoreMetadata("unavailable:preview","1")))
    val ui=ExerciseUiState().apply{page=ExercisePage.DETAIL;detail=session.id}
    LearningTheme {ExerciseScreens(acceptedPracticeBank9J,previewCatalog(),records,false,{},ui,false,{},{},{},{})}
}
@Preview(name="Lifecycle-aware content",widthDp=390,heightDp=100)
@Composable internal fun OnStudyBackgroundPreview() {OnStudyBackground {};LearningTheme{Text("Study progress is saved when the app moves to the background.")}}
