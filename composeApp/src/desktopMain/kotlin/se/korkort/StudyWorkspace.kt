package se.korkort
import androidx.compose.runtime.*
@Composable internal actual fun rememberStudyWorkspace(generation:String,notice:String?):CurriculumWorkspace=remember(generation){CurriculumWorkspace(notice)}
