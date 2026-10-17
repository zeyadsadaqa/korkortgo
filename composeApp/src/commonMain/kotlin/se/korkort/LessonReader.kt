@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class,androidx.compose.foundation.ExperimentalFoundationApi::class)
package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.*
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.*
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.unit.dp

internal fun RichText.annotated(onLink:(TeachingLink)->Unit): AnnotatedString = buildAnnotatedString {
    fun AnnotatedString.Builder.add(nodes: RichText) { nodes.forEach { node -> when(node) {
        is InlineContent.Text -> append(node.text)
        is InlineContent.Emphasis -> withStyle(SpanStyle(fontStyle=FontStyle.Italic)){add(node.children)}
        is InlineContent.Strong -> withStyle(SpanStyle(fontWeight=FontWeight.SemiBold)){add(node.children)}
        is InlineContent.Math -> append(node.expression)
        is InlineContent.Link -> withLink(LinkAnnotation.Clickable(node.target.toString(),linkInteractionListener={onLink(node.target)})){add(node.label)}
    } } }
    add(this@annotated)
}

@Composable internal fun TeachingText(text:RichText,onLink:(TeachingLink)->Unit,modifier:Modifier=Modifier) {
    SelectionContainer { Text(text.annotated(onLink),modifier,style=MaterialTheme.typography.bodyLarge) }
}

internal fun readingNeighbours(id:ContentId): Pair<ContentId?,ContentId?> {
    val i=readerOrder.indexOf(id)
    return if(i<0) null to null else readerOrder.getOrNull(i-1) to readerOrder.getOrNull(i+1)
}

@Composable internal fun LessonReader(
    target: ContentTarget,
    onOpen:(ContentTarget)->Unit,
    onSource:(SourceReferenceId,ReturnContext)->Unit,
    onLibrary:()->Unit,
    notice:String?=null,
    restored:RestoredContext?=null,
    onSources:((ReturnContext)->Unit)?=null,
    state:LazyListState=remember(target.contentId){LazyListState()},
    onReference:((ContentTarget,ReturnContext)->Unit)?=null,
) {
    val found=canonicalResolver.canonical(target) as? Resolution.Found
    val document=readerDocuments.singleOrNull{it.id==found?.target?.contentId}
    if(document==null) { Text("This content is unavailable."); return }
    key(document.id) {
        val answers=document.answerBlocks.associateBy{it.metadata.id}
        val sources=remember(document.id){lessonSources(document)}
        val module=readerModules.singleOrNull{it.id==document.moduleId}
        val neighbours=readingNeighbours(document.id)
        val sourceFocus=remember(document.id){lessonSources(document).associate{it.id to FocusRequester()}}
        val focusSource=restored?.focusId?.takeIf{it.startsWith("source:")}?.removePrefix("source:")?.let{SourceReferenceId(it)}
        var focusRestored by remember(restored){mutableStateOf(false)}
        val sourceVisible=state.layoutInfo.visibleItemsInfo.any{it.key=="source:${focusSource?.value}" && it.size>0 && it.offset<state.layoutInfo.viewportEndOffset && it.offset+it.size>state.layoutInfo.viewportStartOffset}
        LaunchedEffect(focusSource,sourceVisible,focusRestored){
            if(focusSource!=null && !focusRestored && focusSource in sourceFocus){
                if(!sourceVisible) state.requestScrollToItem(document.bodyBlocks.size+2+sources.indexOfFirst{it.id==focusSource})
                else {withFrameNanos{};focusRestored=sourceFocus.getValue(focusSource).requestFocus()}
            }
        }
        fun context(focusId:String?=null)=ReturnContext(ContentTarget(document.id),document.bodyBlocks.getOrNull((state.firstVisibleItemIndex-1).coerceIn(0,document.bodyBlocks.lastIndex))?.let{ReadingPosition(it.metadata.id,state.firstVisibleItemScrollOffset)},focusId)
        val link:(TeachingLink)->Unit={when(it){is TeachingLink.Internal->if(onReference!=null)onReference(it.target,context())else onOpen(it.target);is TeachingLink.ExternalSource->onSource(it.referenceId,context())}}
        LaunchedEffect(found?.target,restored,MaterialTheme.typography.bodyLarge.fontFamily) {
            if(focusSource!=null) return@LaunchedEffect
            val position=restored?.position
            if(position!=null) {
                val i=document.bodyBlocks.indexOfFirst{it.metadata.id==position.blockId}
                if(i>=0)state.scrollToItem(i+1,position.offsetPx)
            } else {
            val index=document.bodyBlocks.indexOfFirst{it.metadata.id==found?.target?.blockId}
            if(index>=0) state.scrollToItem(index+1)
            }

        }
        LazyColumn(Modifier.widthIn(max=800.dp).fillMaxSize(),state,contentPadding=PaddingValues(24.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
            item("opening") {
                Column(verticalArrangement=Arrangement.spacedBy(12.dp)) {
                    TextButton(onLibrary){Text("Learning library")}
                    module?.let{Text("${it.order}. ${it.title}")}
                    (notice ?: found?.notice)?.let{Text(if(it=="The precise passage has moved. Showing its parent.")"This passage has moved. The related lesson is shown below."else it,Modifier.semantics{liveRegion=LiveRegionMode.Polite})}
                    Text(document.title,style=MaterialTheme.typography.headlineLarge,modifier=Modifier.semantics{heading()})
                    document.objectives.filter{objective->document.bodyBlocks.none{it.searchText().contains(objective.assessmentText())}}.forEach{TeachingText(it,link)}
                }
            }
            items(document.bodyBlocks,key={it.metadata.id.value}){block->TeachingBlock(block,answers,link)}
            item("sources") {
                if(onSources!=null) TextButton({onSources(context())}){Text("Sources",style=MaterialTheme.typography.titleLarge)} else Text("Sources",style=MaterialTheme.typography.titleLarge,modifier=Modifier.semantics{heading()})
            }
            items(sources,key={"source:${it.id.value}"}){source->
                TextButton({onSource(source.id,context("source:${source.id.value}"))},modifier=Modifier.focusRequester(sourceFocus.getValue(source.id))){Text(source.title)}
            }
            item("neighbours") {
                FlowRow(horizontalArrangement=Arrangement.spacedBy(12.dp)) {
                    neighbours.first?.let{id->TextButton({onOpen(ContentTarget(id))}){Text("Previous: ${readerDocuments.single{it.id==id}.title}")}}
                    neighbours.second?.let{id->TextButton({onOpen(ContentTarget(id))}){Text("Next: ${readerDocuments.single{it.id==id}.title}")}}
                }
            }
        }
    }
}

@Composable internal fun TeachingBlock(block:ContentBlock,answers:Map<BlockId,AnswerBlock>,onLink:(TeachingLink)->Unit) {
    when(val p=block.payload) {
        is BlockPayload.Heading -> Text(p.text.annotated(onLink),style=if(p.level<=2)MaterialTheme.typography.headlineSmall else MaterialTheme.typography.titleLarge,modifier=Modifier.semantics{heading()})
        is BlockPayload.Paragraph -> TeachingText(p.text,onLink)
        is BlockPayload.ListItems -> Column(verticalArrangement=Arrangement.spacedBy(8.dp)) { p.items.forEachIndexed{index,blocks->
            Row {Text(if(p.ordered)"${index+p.start}. " else "• ");Column(Modifier.weight(1f)){blocks.forEach{TeachingBlock(it,answers,onLink)}}}
        } }
        is BlockPayload.Table -> Column(verticalArrangement=Arrangement.spacedBy(12.dp)) {
            p.caption?.let{TeachingText(it,onLink)}
            // Each row reflows vertically with its column labels; no horizontal clipping at large text.
            p.rows.forEach{row->OutlinedCard(Modifier.fillMaxWidth()) {Column(Modifier.padding(12.dp),verticalArrangement=Arrangement.spacedBy(8.dp)) {
                row.cells.forEachIndexed{i,cell->TeachingText(p.columns[i].heading,onLink);TeachingText(cell,onLink)}
            }}}
        }
        is BlockPayload.Equation -> Column {
            SelectionContainer {Text(p.expression,style=MaterialTheme.typography.bodyLarge,modifier=Modifier.semantics{contentDescription=p.spokenText})}
            TeachingText(p.assumptions,onLink)
        }
        is BlockPayload.Callout -> OutlinedCard(Modifier.fillMaxWidth()) {Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(8.dp)) {
            p.title?.let{TeachingText(it,onLink)};p.blocks.forEach{TeachingBlock(it,answers,onLink)}
        }}
        is BlockPayload.Scenario -> Column(verticalArrangement=Arrangement.spacedBy(8.dp)) {p.title?.let{TeachingText(it,onLink)};p.blocks.forEach{TeachingBlock(it,answers,onLink)}}
        is BlockPayload.KnowledgeCheck -> {
            var expanded by remember(block.metadata.id){mutableStateOf(false)}
            val focus=remember{FocusRequester()}
            OutlinedCard(Modifier.fillMaxWidth()) {Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(8.dp)) {
                p.prompts.forEach{TeachingBlock(it,answers,onLink)}
                TextButton({ if(expanded) focus.requestFocus();expanded=!expanded },modifier=Modifier.focusRequester(focus).semantics{stateDescription=if(expanded)"Expanded" else "Collapsed"}){Text(if(expanded)"Hide answer" else "Show answer")}
                if(expanded) Column(Modifier.semantics{paneTitle="Answer"}) { answers.getValue(p.answerId).blocks.forEach{TeachingBlock(it,answers,onLink)} }
            }}
        }
        is BlockPayload.Image -> TeachingIllustration(p.assetId,null,emptyList(),emptyList(),p.caption,onLink)
        is BlockPayload.CroppedImage -> TeachingIllustration(p.assetId,p.region,emptyList(),emptyList(),p.caption,onLink)
        is BlockPayload.PolygonImage -> TeachingIllustration(p.assetId,p.region,p.polygon,emptyList(),p.caption,onLink)
        is BlockPayload.CompositeImage -> TeachingIllustration(p.assetId,p.region,emptyList(),p.overlays,p.caption,onLink)
        is BlockPayload.RelatedLinks -> Column{p.links.forEach{TeachingText(listOf(it),onLink)}}
        is BlockPayload.SignExamples -> Column{p.entryIds.forEach{id->val sign=navigationSigns.single{it.id==id};val asset=readerAssets.single{it.id==sign.assetId};StudyImage(asset,"Enlarge ${sign.englishLabel} image");TeachingText(sign.caption,onLink)}}
    }
}

@Composable internal fun StudyImage(asset:CurriculumAsset,label:String) {
    var enlarged by remember(asset.id){mutableStateOf(false)}
    var restore by remember(asset.id){mutableStateOf(false)}
    val focus=remember{FocusRequester()}
    ExactAssetImage(asset,asset.studyAltText,Modifier.fillMaxWidth().height(180.dp))
    OutlinedButton({enlarged=true},Modifier.focusRequester(focus)){Text(label)}
    if(enlarged)AccessibleImageViewer(ImageViewerContent(asset,"Road signs and reference",asset.studyAltText)){enlarged=false;restore=true}
    LaunchedEffect(enlarged,restore){if(!enlarged && restore){withFrameNanos{};focus.requestFocus();restore=false}}
}
