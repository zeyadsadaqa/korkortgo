@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)
package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
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

@Composable internal fun LearningLibrary(
    onOpen: (ContentTarget)->Unit,
    onSources: ()->Unit,
    onReferences: ()->Unit,
) {
    var expanded by remember { mutableStateOf(setOf(ContentId("M03"))) }
    var filter by remember { mutableStateOf(LibraryFilter()) }
    val documents=remember {readerDocuments.associateBy{it.id}}
    val filtering=filter.query.isNotBlank() || filter.category!=null
    val visible=readerModules.sortedBy{it.order}.map { module ->
        module to (module.lessonIds + module.reviewId).map{documents.getValue(it)}.filter {
            if(filtering) it.kind==DocumentKind.LESSON && filter.matches(it,readerTags) else true
        }
    }.filter { it.second.isNotEmpty() }
    Column(Modifier.widthIn(max=900.dp).fillMaxWidth().verticalScroll(rememberScrollState()).padding(24.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
        Text("Learning library",style=MaterialTheme.typography.headlineLarge,modifier=Modifier.semantics{heading()})
        Text("${readerModules.size} modules · ${readerModules.sumOf{it.lessonIds.size}} lessons")
        FlowRow(horizontalArrangement=Arrangement.spacedBy(8.dp)) {
            OutlinedButton(onClick=onSources){Text("Sources")}
            OutlinedButton(onClick=onReferences){Text("Road signs and reference")}
        }
        OutlinedTextField(filter.query,{filter=filter.copy(query=it)},label={Text("Search lessons")},modifier=Modifier.fillMaxWidth())
        FlowRow(horizontalArrangement=Arrangement.spacedBy(8.dp)) {
            FilterChip(filter.category==null,{filter=filter.clearCategory()},label={Text("All topics")})
            Category.entries.forEach { category -> FilterChip(filter.category==category,{filter=filter.copy(category=category)},label={Text(category.title)}) }
        }
        FlowRow(horizontalArrangement=Arrangement.spacedBy(8.dp)) {
            TextButton({filter=filter.clearQuery()}){Text("Clear search")}
            TextButton({filter=filter.clearCategory()}){Text("Clear filters")}
        }
        if(visible.isEmpty()) Text("No matching lessons.",Modifier.semantics{liveRegion=LiveRegionMode.Polite})
        visible.forEach { (module,children) ->
            OutlinedCard(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(8.dp)) {
                    Text("${module.order}. ${module.title}",style=MaterialTheme.typography.headlineSmall,modifier=Modifier.fillMaxWidth().background(MaterialTheme.colorScheme.secondaryContainer).clickable{expanded=if(module.id in expanded)expanded-module.id else expanded+module.id}.padding(12.dp).semantics{heading();role=Role.Button;stateDescription=if(module.id in expanded || filtering)"Expanded" else "Collapsed"})
                    if(module.id in expanded || filtering) children.forEach { document ->
                        TextButton({onOpen(ContentTarget(document.id))},modifier=Modifier.fillMaxWidth()) {
                            Column(Modifier.fillMaxWidth()) {
                                Text(document.title,style=MaterialTheme.typography.titleMedium)
                                Text(if(document.kind==DocumentKind.MODULE_REVIEW) "Module review" else "Lesson",style=MaterialTheme.typography.labelMedium)
                            }
                        }
                    }
                }
            }
        }
        readerDocuments.filter{it.kind==DocumentKind.APPENDIX || it.kind==DocumentKind.FRONT_MATTER}.sortedBy{it.order}.forEach { document ->
            TextButton({onOpen(ContentTarget(document.id))}){Text(document.title)}
        }
    }
}
