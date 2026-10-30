package se.korkort

import androidx.compose.runtime.*
import androidx.compose.foundation.ScrollState
import androidx.compose.foundation.lazy.LazyListState

/** UI-only state survives Android recreation; committed learner state always comes from the store. */
internal class CurriculumWorkspace(notice:String?=null) {
    val state=mutableStateOf(TransientQuizState())
    val learningRoute=mutableStateOf(LearningRouteState())
    val lastLearning=mutableStateOf<AppDestination>(AppDestination.Library)
    val lastExercise=mutableStateOf<AppDestination>(AppDestination.QuizSetup)
    val questionViews=mutableMapOf<PracticeQuestionToken,QuestionUiState>()
    val homeScroll=LazyListState();val setupScroll=LazyListState();val resultsScroll=LazyListState();val reviewScroll=LazyListState()
    val reviewSourceScrolls=mutableMapOf<SourceReferenceId,ScrollState>()
    val exerciseUi=ExerciseUiState();val dataUi=DataUiState(notice)
    val showData=mutableStateOf(notice!=null)
    val library=LearningLibraryState()
    val sourceFailure=mutableStateOf(false)
    val sourceOrigin=mutableStateOf<QuestionRevisionKey?>(null)
    val restoreReviewSource=mutableStateOf<Pair<QuestionRevisionKey,SourceReferenceId>?>(null)
    val reviewSource=mutableStateOf<SourceReferenceId?>(null)
}
@Composable internal expect fun rememberStudyWorkspace(generation:String,notice:String?):CurriculumWorkspace
