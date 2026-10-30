package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.focusable
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.selection.selectableGroup
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusProperties
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.semantics.*
import androidx.compose.ui.state.ToggleableState
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
    onEnlargeImage: ((AssessmentImagePresentation, FocusRequester) -> Unit)? = null,
) {
    val canInteract=LocalStudy.current?.let { !it.busy && it.failure==null } ?: true
    var pending by remember(presentation.key, presentation.choices.map { it.id }) { mutableStateOf<OptionId?>(null) }
    val feedbackFocus = remember(presentation.key) { FocusRequester() }
    LaunchedEffect(presentation.key, presentation.canConfirm, presentation.explanation) {
        if (!presentation.canConfirm) feedbackFocus.requestFocus()
    }
    val selection = presentation.choices.singleOrNull { it.selected }?.id ?: pending
    DisposableEffect(presentation.key) { onDispose { clearBrowserAssessmentChoices() } }
    SideEffect { updateBrowserAssessmentChoices(presentation.choices.singleOrNull{it.id==selection}?.letter,presentation.canConfirm && canInteract) }
    Column(Modifier.semantics { isTraversalGroup = true }, verticalArrangement = Arrangement.spacedBy(14.dp)) {
        Text(presentation.prompt, style = MaterialTheme.typography.headlineSmall)
        presentation.image?.let { picture ->
            val focus=remember(presentation.key) {FocusRequester()}
            AssessmentPicture(picture, Modifier.readableArtworkFrame(), image)
            if(onEnlargeImage!=null) OutlinedButton(onClick={onEnlargeImage(picture,focus)},modifier=Modifier.heightIn(min=48.dp).focusRequester(focus).focusProperties{canFocus=true}) {Text("Enlarge question image")}
        }
        Column(Modifier.selectableGroup().then(if(singleLayerBrowserModals)Modifier.semantics{contentDescription="Answer choices"}else Modifier), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            presentation.choices.forEach { choice ->
                key(choice.id) {
                    // Foundation selectable supplies Space/Enter, focus and radio semantics as one target.
                    val isSelected = choice.id == selection
                    Surface(shape = MaterialTheme.shapes.medium,
                        border = BorderStroke(if(isSelected)2.dp else 1.dp,if(isSelected)MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant),
                        color = if(isSelected && presentation.canConfirm)MaterialTheme.colorScheme.secondaryContainer else MaterialTheme.colorScheme.surface) {
                        Column(Modifier.fillMaxWidth().selectable(
                            selected = choice.id == selection,
                            enabled = presentation.canConfirm && canInteract,
                            role = Role.RadioButton,
                            onClick = { pending = choice.id },
                        ).semantics(mergeDescendants = true) {
                            toggleableState = if(isSelected)ToggleableState.On else ToggleableState.Off
                            stateDescription = if(isSelected)"Selected" else "Not selected"
                        }.padding(18.dp)) {
                            Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.SpaceBetween) {
                                Text(choice.letter)
                                // The radio's checked state/stateDescription supplies this to AT once.
                                if(isSelected && presentation.canConfirm)Text("Selected",modifier=Modifier.clearAndSetSemantics {},style=MaterialTheme.typography.labelMedium)
                            }
                            if (choice.text.isNotEmpty()) Text(choice.text)
                            choice.image?.let { AssessmentPicture(it, Modifier.readableArtworkFrame(), image) }
                            choice.correct?.let { correct ->
                                Text(if (correct) "Correct answer" else if (choice.selected) "Your answer · Incorrect" else "Incorrect option")
                            }
                            choice.feedback?.let { Text(it) }
                        }
                    }
                    choice.image?.let { picture ->
                        val focus=remember(choice.id) {FocusRequester()}
                        if(onEnlargeImage!=null) OutlinedButton(onClick={onEnlargeImage(picture,focus)},modifier=Modifier.heightIn(min=48.dp).focusRequester(focus).focusProperties{canFocus=true}) {Text("Enlarge option ${choice.letter} image")}
                    }
                }
            }
        }
        if (presentation.canConfirm) {
            Button(onClick = { selection?.let(onConfirm) }, enabled = selection != null && canInteract,
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
    Box(modifier.clearAndSetSemantics { contentDescription = picture.description }, propagateMinConstraints = true) {
        image(picture, Modifier.fillMaxWidth())
    }
}
