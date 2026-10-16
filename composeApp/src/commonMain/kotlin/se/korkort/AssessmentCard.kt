package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.focusable
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.selection.selectableGroup
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.dp

/** Uses the existing question card's vertical reading order. Wiring into routes is 9L7.
 * Only the session's gated projection enters composition, including the accessibility tree.
 * Image delivery is injected so assessment code cannot fall back to study captions or file names.
 */
@Composable
fun AssessmentCard(
    presentation: AssessmentPresentation,
    onConfirm: (OptionId) -> Unit,
    image: @Composable (AssessmentImagePresentation, Modifier) -> Unit = { picture, modifier ->
        // Equivalent text remains available if a platform cannot yet deliver an exact image.
        Text(picture.description, modifier)
    },
) {
    var pending by remember(presentation.key, presentation.choices.map { it.id }) { mutableStateOf<OptionId?>(null) }
    val feedbackFocus = remember(presentation.key) { FocusRequester() }
    LaunchedEffect(presentation.key, presentation.canConfirm, presentation.explanation) {
        if (!presentation.canConfirm) feedbackFocus.requestFocus()
    }
    val selection = presentation.choices.singleOrNull { it.selected }?.id ?: pending
    Column(Modifier.semantics { isTraversalGroup = true }, verticalArrangement = Arrangement.spacedBy(14.dp)) {
        Text(presentation.prompt, style = MaterialTheme.typography.headlineSmall)
        presentation.image?.let { AssessmentPicture(it, Modifier.fillMaxWidth().heightIn(min = 180.dp), image) }
        Column(Modifier.selectableGroup(), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            presentation.choices.forEach { choice ->
                key(choice.id) {
                    // Foundation selectable supplies Space/Enter, focus and radio semantics as one target.
                    Surface(shape = MaterialTheme.shapes.medium) {
                        Column(Modifier.fillMaxWidth().selectable(
                            selected = choice.id == selection,
                            enabled = presentation.canConfirm,
                            role = Role.RadioButton,
                            onClick = { pending = choice.id },
                        ).semantics(mergeDescendants = true) {}.padding(18.dp)) {
                            Text(choice.letter)
                            if (choice.text.isNotEmpty()) Text(choice.text)
                            choice.image?.let { AssessmentPicture(it, Modifier.fillMaxWidth().heightIn(min = 105.dp), image) }
                            choice.correct?.let { correct ->
                                Text(if (correct) "Correct answer" else if (choice.selected) "Your answer · Incorrect" else "Incorrect option")
                            }
                            choice.feedback?.let { Text(it) }
                        }
                    }
                }
            }
        }
        if (presentation.canConfirm) {
            Button(onClick = { selection?.let(onConfirm) }, enabled = selection != null,
                modifier = Modifier.fillMaxWidth().heightIn(min = 52.dp)) {
                Text("Confirm answer  >")
            }
        }
        presentation.explanation?.let { explanation ->
            Column(Modifier.focusRequester(feedbackFocus).focusable().semantics(mergeDescendants = true) {
                liveRegion = LiveRegionMode.Polite
            }) {
                listOfNotNull(presentation.targetCode, presentation.targetLabel).takeIf { it.isNotEmpty() }?.let {
                    Text(it.joinToString(" · "))
                }
                Text(explanation)
            }
        }
        if (!presentation.canConfirm && presentation.explanation == null) {
            Text("Answer saved.", Modifier.focusRequester(feedbackFocus).focusable().semantics {
                liveRegion = LiveRegionMode.Polite
            })
        }
    }
}

@Composable
private fun AssessmentPicture(
    picture: AssessmentImagePresentation,
    modifier: Modifier,
    image: @Composable (AssessmentImagePresentation, Modifier) -> Unit,
) {
    // Enforce the assessment description even if the platform renderer supplies its own semantics.
    Box(modifier.clearAndSetSemantics { contentDescription = picture.description }) {
        image(picture, Modifier.fillMaxWidth())
    }
}
