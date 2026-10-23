package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusProperties
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.dp

/** Callbacks go to the shared navigation owner; the view cannot bypass its unfinished-test guard. */
@Composable internal fun LearningAnswerReview(session:AssessmentSession,position:Int=session.index,onRelated:(ContentTarget)->Unit,onSource:(SourceReferenceId)->Unit,scrollable:Boolean=true,showPrompt:Boolean=true,restoreSourceFocus:SourceReferenceId?=null) {
    val presentation=session.presentation(position)
    val question=session.snapshots[position].question
    val sourceFocus=remember(question.key){question.relationship.sourceUses.map{it.referenceId}.distinct().associateWith{FocusRequester()}}
    LaunchedEffect(restoreSourceFocus){restoreSourceFocus?.let{id->withFrameNanos{};sourceFocus[id]?.requestFocus()}}
    Column(Modifier.widthIn(max=800.dp).then(if(scrollable)Modifier.fillMaxSize().verticalScroll(rememberScrollState()) else Modifier.fillMaxWidth()).padding(if(scrollable)24.dp else 0.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
        if(showPrompt) {
        Text("Answer review",style=MaterialTheme.typography.headlineLarge,modifier=Modifier.semantics{heading()})
        Text(presentation.prompt,style=MaterialTheme.typography.bodyLarge)
        }
        presentation.image?.let{image->ReviewImage(image,"Enlarge question image")}
        presentation.choices.forEach { choice ->
            OutlinedCard(Modifier.fillMaxWidth(),colors=CardDefaults.outlinedCardColors(containerColor=when{choice.correct==true->MaterialTheme.colorScheme.secondaryContainer;choice.selected && choice.correct==false->MaterialTheme.colorScheme.errorContainer;else->MaterialTheme.colorScheme.surface})) {Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(8.dp)) {
                Text("${choice.letter}. ${choice.text}")
                choice.image?.let{image->ReviewImage(image,"Enlarge option ${choice.letter} image")}
                if(choice.selected)Text("Your answer")
                if(choice.correct==true)Text("Correct answer")
                if(choice.selected && choice.correct==false)Text("Incorrect")
                choice.feedback?.let{Text(it)}
            }}
        }
        presentation.explanation?.let { explanation ->
            LearningInfoPanel {
                Text("Explanation",style=MaterialTheme.typography.headlineSmall,modifier=Modifier.semantics{heading()})
                Text(explanation,style=MaterialTheme.typography.bodyLarge)
            }
            (listOf(question.relationship.primaryLessonId)+question.relationship.relatedLessonIds).distinct().forEach{id->
                LearningAction(readerDocuments.single{it.id==id}.title,{onRelated(ContentTarget(id))},detail="Related lesson")
            }
            question.relationship.sourceUses.map{it.referenceId}.distinct().forEach{id->
                LearningAction(navigationSources.references.single{it.id==id}.title,{onSource(id)},Modifier.focusRequester(sourceFocus.getValue(id)).focusProperties{canFocus=true},detail="Sources")
            }
        }
    }
}

@Composable private fun ReviewImage(image:AssessmentImagePresentation,label:String) {
    var enlarged by remember(image){mutableStateOf(false)}
    var restore by remember(image){mutableStateOf(false)}
    val focus=remember{FocusRequester()}
    ExactAssetImage(readerAssets.single{it.id==image.assetId},image.description,Modifier.readableArtworkFrame())
    OutlinedButton({enlarged=true},Modifier.focusRequester(focus).focusProperties{canFocus=true}){Text(label)}
    if(enlarged) AccessibleImageViewer(ImageViewerContent.assessment(image,readerAssets)){enlarged=false;restore=true}
    LaunchedEffect(enlarged,restore){if(!enlarged && restore){withFrameNanos{};focus.requestFocus();restore=false}}
}
