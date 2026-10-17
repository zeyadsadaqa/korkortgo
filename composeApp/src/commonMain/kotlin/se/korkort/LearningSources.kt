package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.ScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusProperties
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.dp

/** Exact source uses include nested blocks and answer evidence, not unrelated directory examples. */
internal fun lessonSources(document:CurriculumDocument): List<SourceReference> {
    fun uses(block:ContentBlock):List<SourceReferenceId> = block.metadata.sourceUses.map{it.referenceId}+when(val p=block.payload){
        is BlockPayload.ListItems->p.items.flatten().flatMap{uses(it)}
        is BlockPayload.Callout->p.blocks.flatMap{uses(it)}
        is BlockPayload.Scenario->p.blocks.flatMap{uses(it)}
        is BlockPayload.KnowledgeCheck->p.prompts.flatMap{uses(it)}
        else->emptyList()
    }
    val ids=(document.bodyBlocks.flatMap{uses(it)}+document.answerBlocks.flatMap{it.metadata.sourceUses.map{it.referenceId}+it.blocks.flatMap{b->uses(b)}}).toSet()
    return navigationSources.references.filter{it.id in ids}
}

@Composable internal fun SourceDirectory(origin:ReturnContext?,onOpen:(SourceReferenceId)->Unit,onReturn:()->Unit, scroll:ScrollState=rememberScrollState(), restoreFocus:SourceReferenceId?=null) {
    val document=readerDocuments.singleOrNull{it.id==origin?.origin?.contentId}
    val references=if(document!=null)lessonSources(document)else navigationSources.references.filter{reference->navigationSources.destinations.any{destination->destination.scopedUrls.any{it.referenceId==reference.id}}}
    val focus=remember(references){references.associate{it.id to FocusRequester()}}
    LaunchedEffect(restoreFocus){restoreFocus?.let{withFrameNanos{};focus[it]?.requestFocus()}}
    Column(Modifier.widthIn(max=800.dp).fillMaxSize().verticalScroll(scroll).padding(24.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
        Text("Sources",style=MaterialTheme.typography.headlineLarge,modifier=Modifier.semantics{heading()})
        TextButton(onReturn){Text(if(document==null)"Learning library" else "Return to ${document.title}")}
        references.forEach{reference->OutlinedCard(Modifier.fillMaxWidth()) {Column(Modifier.padding(16.dp)){
            TextButton({onOpen(reference.id)},Modifier.focusRequester(focus.getValue(reference.id)).focusProperties{canFocus=true}){Text(reference.title)}
            Text(reference.publisher);Text(reference.classificationNote)
        }}}
    }
}

@Composable internal fun SourceDetail(id:SourceReferenceId,onBack:()->Unit,onReturn:()->Unit,onExternal:(SourceReference)->Boolean) {
    val source=navigationSources.references.singleOrNull{it.id==id}
    if(source==null){Text("This source is unavailable.");TextButton(onBack){Text("Sources")};return}
    var failed by remember(id){mutableStateOf(false)}
    Column(Modifier.widthIn(max=800.dp).fillMaxSize().verticalScroll(rememberScrollState()).padding(24.dp),verticalArrangement=Arrangement.spacedBy(12.dp)) {
        TextButton(onBack){Text("Back to Sources")}
        Text(source.title,style=MaterialTheme.typography.headlineLarge,modifier=Modifier.semantics{heading()})
        Text(source.publisher)
        Text(source.classifications.joinToString(" · "){it.name.lowercase().replace('_',' ')})
        Text(source.classificationNote)
        source.evidence.forEach { evidence ->
            Text("Checked: ${evidence.dates.checkedOn ?: "Not recorded"}")
            Text("Retrieved: ${evidence.dates.retrievedOn ?: "Not recorded"}")
            Text("Published: ${evidence.dates.publishedOn ?: "Not recorded"}")
            Text(evidence.scope);Text(evidence.finding)
            evidence.limitations.forEach{Text(it)}
        }
        Button({failed=!onExternal(source)}){Text("Open source")}
        if(failed)Text("The source could not be opened. You can return to Sources or your reading.",Modifier.semantics{liveRegion=LiveRegionMode.Polite})
        TextButton(onReturn){Text("Return to reading")}
    }
}
