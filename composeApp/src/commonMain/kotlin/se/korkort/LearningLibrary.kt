@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)
package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import se.korkort.progress.LessonProgress
import kotlinx.coroutines.flow.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.Alignment
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.dp

/** Search teaching, never bank capacity. Each clear action changes only its own input. */
data class LibraryFilter(val query: String = "", val category: Category? = null) {
    fun clearQuery() = copy(query = "")
    fun clearCategory() = copy(category = null)
    fun matches(document: CurriculumDocument, tags: Map<ContentId, Set<Category>>): Boolean =
        (category == null || category in tags[document.id].orEmpty()) &&
            (query.isBlank() || document.searchText().contains(query.trim(), ignoreCase = true))
}

internal fun CurriculumDocument.searchText(): String =
    (listOf(title) + objectives.map { it.assessmentText() } + bodyBlocks.map { it.searchText() }).joinToString("\n")

internal fun ContentBlock.searchText(): String = when(val p=payload) {
    is BlockPayload.Heading -> p.text.assessmentText()
    is BlockPayload.Paragraph -> p.text.assessmentText()
    is BlockPayload.ListItems -> p.items.flatten().joinToString("\n") { it.searchText() }
    is BlockPayload.Table -> listOfNotNull(p.caption?.assessmentText(), p.columns.joinToString(" "){it.heading.assessmentText()},p.rows.joinToString(" "){r->r.cells.joinToString(" "){it.assessmentText()}}).joinToString(" ")
    is BlockPayload.Equation -> "${p.expression} ${p.spokenText} ${p.assumptions.assessmentText()}"
    is BlockPayload.Callout -> "${p.title?.assessmentText().orEmpty()} ${p.blocks.joinToString(" "){it.searchText()}}"
    is BlockPayload.Scenario -> "${p.title?.assessmentText().orEmpty()} ${p.blocks.joinToString(" "){it.searchText()}}"
    is BlockPayload.KnowledgeCheck -> p.prompts.joinToString(" "){it.searchText()}
    is BlockPayload.Image -> p.caption.assessmentText()
    is BlockPayload.CroppedImage -> p.caption.assessmentText()
    is BlockPayload.PolygonImage -> p.caption.assessmentText()
    is BlockPayload.CompositeImage -> p.caption.assessmentText()
    is BlockPayload.RelatedLinks -> p.links.joinToString(" "){it.label.assessmentText()}
    is BlockPayload.SignExamples -> p.entryIds.joinToString(" "){id->navigationSigns.single{it.id==id}.englishLabel}
}

/** Retained by the route owner while a lesson, source or reference is open. */
internal class LearningLibraryState {
    var expanded by mutableStateOf(setOf(ContentId("M03")))
    var progressInitialized=false
    var showFilters by mutableStateOf(false)
    var supportingExpanded by mutableStateOf(false)
    var filter by mutableStateOf(LibraryFilter())
    val scroll = androidx.compose.foundation.ScrollState(0)
}

@Composable internal fun LearningLibrary(
    onOpen: (ContentTarget)->Unit,
    onSources: ()->Unit,
    onReferences: ()->Unit,
    state: LearningLibraryState = remember { LearningLibraryState() },
) {
    val environment=LocalStudy.current
    val progress by produceState<List<LessonProgress>?>(null,environment) {
        environment?.study?.let {study->study.repository.observeLessons(study.token).collect {value=it}}
    }
    val read=readLessonIds(progress.orEmpty(),readerDocuments)
    val current=readerModules.sortedBy{it.order}.firstOrNull {module->module.lessonIds.any {it !in read}}
    LaunchedEffect(progress) {
        if(progress!=null && !state.progressInitialized) {
            state.expanded=setOfNotNull(current?.id)
            state.progressInitialized=true
        }
    }
    val expanded=state.expanded
    val filter=state.filter
    val focus=LocalFocusManager.current
    val documents=remember {readerDocuments.associateBy{it.id}}
    val filtering=filter.query.isNotBlank() || filter.category!=null
    var supportingExpanded by state::supportingExpanded
    val visible=readerModules.sortedBy{it.order}.map { module ->
        module to (module.lessonIds + module.reviewId).map{documents.getValue(it)}.filter {
            if(filtering) it.kind==DocumentKind.LESSON && filter.matches(it,readerTags) else true
        }
    }.filter { it.second.isNotEmpty() }
    Column(Modifier.widthIn(max=900.dp).fillMaxWidth().verticalScroll(state.scroll).padding(24.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
        Text(if(environment==null)"Learning library" else "Learning",style=MaterialTheme.typography.headlineLarge,modifier=Modifier.semantics{heading()})
        if(environment==null)Text("${readerModules.size} modules · ${readerModules.sumOf{it.lessonIds.size}} lessons")
        if(environment!=null) {
            Text(if(progress==null)"Loading your progress…" else "${read.size} of ${readerModules.sumOf{it.lessonIds.size}} lessons read")
            LinearProgressIndicator(progress={read.size.toFloat()/readerModules.sumOf{it.lessonIds.size}},modifier=Modifier.fillMaxWidth().semantics{contentDescription="Reading progress"})
        }
        OutlinedTextField(filter.query,{state.filter=filter.copy(query=it)},label={Text("Search lessons")},singleLine=true,
            keyboardOptions=KeyboardOptions(imeAction=ImeAction.Search),keyboardActions=KeyboardActions(onSearch={focus.clearFocus()}),
            modifier=Modifier.fillMaxWidth().semantics{contentDescription="Search lessons";stateDescription=filter.query})
        var showFilters by state::showFilters
        if(environment!=null) TextButton({showFilters=!showFilters}) {Text(if(showFilters)"Hide topic filters" else "Filter by topic")}
        if(environment==null || showFilters) FlowRow(horizontalArrangement=Arrangement.spacedBy(8.dp)) {
            FilterChip(filter.category==null,{state.filter=filter.clearCategory()},label={Text("All topics")})
            Category.entries.forEach { category -> FilterChip(filter.category==category,{state.filter=filter.copy(category=category)},label={Text(category.title)}) }
        }
        if(environment==null || filtering) FlowRow(horizontalArrangement=Arrangement.spacedBy(8.dp)) {
            TextButton({state.filter=filter.clearQuery()}){Text("Clear search")}
            TextButton({state.filter=filter.clearCategory()}){Text("Clear filters")}
        }
        if(visible.isEmpty()) LearningInfoPanel {
            Text("No matching lessons.",style=MaterialTheme.typography.headlineSmall,modifier=Modifier.semantics{liveRegion=LiveRegionMode.Polite})
            Text("Try another search or clear the topic filters.")
        }
        visible.forEach { (module,children) ->
            OutlinedCard(Modifier.fillMaxWidth(),border=androidx.compose.foundation.BorderStroke(1.dp,MaterialTheme.colorScheme.outline.copy(alpha=.3f))) {
                Column {
                    Row(Modifier.fillMaxWidth().background(if(module.id in expanded || filtering)MaterialTheme.colorScheme.secondaryContainer else MaterialTheme.colorScheme.surface).clickable{state.expanded=if(module.id in expanded)expanded-module.id else expanded+module.id}.padding(16.dp).semantics(mergeDescendants=true){text=androidx.compose.ui.text.AnnotatedString("${module.order}. ${module.title}");heading();role=Role.Button;stateDescription=(if(module.id in expanded || filtering)"Expanded" else "Collapsed") + (if(environment!=null)"; ${module.lessonIds.count{it in read}} of ${module.lessonIds.size} lessons read" else "")},verticalAlignment=Alignment.CenterVertically,horizontalArrangement=Arrangement.spacedBy(12.dp)) {
                        Surface(shape=CircleShape,color=MaterialTheme.colorScheme.primary.copy(alpha=.12f)) {Text(module.order.toString(),Modifier.padding(horizontal=12.dp,vertical=6.dp).clearAndSetSemantics {},style=MaterialTheme.typography.titleLarge)}
                        Column(Modifier.weight(1f).clearAndSetSemantics {}) {
                            Text(module.title,style=MaterialTheme.typography.titleMedium)
                            if(environment!=null) {
                                val count=module.lessonIds.count {it in read}
                                val started=progress.orEmpty().any {p->module.lessonIds.any {it.value==p.lessonId && documents[it]?.revision?.value==p.revision}}
                                Text(if(count==module.lessonIds.size)"$count of ${module.lessonIds.size} lessons · Read" else if(count==0 && !started)"Not started" else "$count of ${module.lessonIds.size} lessons read · In progress",style=MaterialTheme.typography.bodyMedium)
                            }
                        }
                        Text(if(module.id in expanded || filtering)"⌄" else "›",Modifier.clearAndSetSemantics {})
                    }
                    if(module.id in expanded || filtering) children.forEach { document ->
                        HorizontalDivider(color=MaterialTheme.colorScheme.outline.copy(alpha=.3f))
                        TextButton({onOpen(ContentTarget(document.id))},modifier=Modifier.fillMaxWidth(),shape=RoundedCornerShape(0.dp),contentPadding=PaddingValues(16.dp)) {
                            if(environment!=null && document.kind==DocumentKind.LESSON)Text(if(document.id in read)"✓" else "○",modifier=Modifier.clearAndSetSemantics {}) else DocumentMark()
                            Spacer(Modifier.width(12.dp))
                            Column(Modifier.weight(1f)) {
                                Text(document.title,style=MaterialTheme.typography.titleMedium)
                                Text(if(document.kind==DocumentKind.MODULE_REVIEW) "Module review" else if(environment==null)"Lesson" else if(document.id in read)"Read" else if(progress.orEmpty().any{it.lessonId==document.id.value && it.revision==document.revision.value})"Continue" else "Not started",style=MaterialTheme.typography.labelMedium)
                            }
                            Text("›",Modifier.clearAndSetSemantics {})
                        }
                    }
                }
            }
        }
        FlowRow(horizontalArrangement=Arrangement.spacedBy(8.dp)) {
            OutlinedButton(onClick=onSources,shape=RoundedCornerShape(8.dp)){DocumentMark();Spacer(Modifier.width(8.dp));Text("Sources")}
            OutlinedButton(onClick=onReferences,shape=RoundedCornerShape(8.dp)){DocumentMark();Spacer(Modifier.width(8.dp));Text("Road signs and reference")}
        }
        if(filtering) OutlinedButton({supportingExpanded=!supportingExpanded},Modifier.fillMaxWidth()) {Text(if(supportingExpanded)"Hide supporting documents" else "Browse supporting documents")}
        if(!filtering || supportingExpanded) readerDocuments.filter{it.kind==DocumentKind.APPENDIX || it.kind==DocumentKind.FRONT_MATTER}.sortedBy{it.order}.forEach { document ->
            LearningAction(document.title,{onOpen(ContentTarget(document.id))})
        }
    }
}

internal fun readLessonIds(progress: List<LessonProgress>,documents: List<CurriculumDocument>): Set<ContentId> {
    val revisions=documents.filter{it.kind==DocumentKind.LESSON}.associate{it.id.value to it.revision.value}
    return progress.filter{it.read && revisions[it.lessonId]==it.revision}.map{ContentId(it.lessonId)}.toSet()
}
