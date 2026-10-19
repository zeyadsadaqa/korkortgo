package se.korkort

import androidx.compose.runtime.Composable
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.ui.graphics.Color

private val Forest=Color(0xFF173E32)
private val Paper=Color(0xFFF7F8F3)
private val Sage=Color(0xFFE7EEE5)
private val Ink=Color(0xFF172C29)
private val Muted=Color(0xFF61706B)
private val Line=Color(0xFFD5DED5)
private val Ochre=Color(0xFFE7BD4A)
private val Wrong=Color(0xFF9A332F)
private val WrongBg=Color(0xFFFFEDEA)

@Composable internal fun KorkortTheme(content: @Composable () -> Unit) {
    MaterialTheme(colorScheme=lightColorScheme(primary=Forest, onPrimary=Color.White, background=Paper, surface=Color.White, onSurface=Ink, secondary=Forest, secondaryContainer=Sage, onSecondaryContainer=Forest, surfaceVariant=Sage, outline=Line)) {content()}
}


/** Only the validated accepted release enters normal learner routes. */
@Composable fun App() { CurriculumApp(acceptedPracticeBank9J,acceptedCurriculumSummary9J) }
