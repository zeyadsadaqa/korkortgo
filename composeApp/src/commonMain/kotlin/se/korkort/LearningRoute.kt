package se.korkort

import androidx.compose.runtime.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.ui.unit.dp
import androidx.compose.material3.*
import androidx.compose.foundation.layout.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.Alignment

internal class LearningRouteState(initialResolution: Resolution?=null, initialReferences: Boolean=false) {
    val target=mutableStateOf((initialResolution as? Resolution.Found)?.target)
    val resolution=mutableStateOf(initialResolution)
    val directory=mutableStateOf(false)
    val source=mutableStateOf<SourceReferenceId?>(null)
    val origin=mutableStateOf<ReturnContext?>(null)
    val restored=mutableStateOf<RestoredContext?>(null)
    val directoryFocus=mutableStateOf<SourceReferenceId?>(null)
    val references=mutableStateOf(initialReferences)
    val directoryScroll=androidx.compose.foundation.ScrollState(0)
    val lessonHistory=mutableStateListOf<ContentTarget>()
    val scrolls=mutableMapOf<String,androidx.compose.foundation.ScrollState>()
    fun scroll(key:String)=scrolls.getOrPut(key){androidx.compose.foundation.ScrollState(0)}
    val canBack get() = target.value!=null || source.value!=null || directory.value || references.value || resolution.value!=null
    fun back() {
        when {
            source.value!=null -> {directoryFocus.value=source.value;source.value=null;directory.value=true}
            directory.value || references.value && origin.value!=null -> {
                source.value=null;directory.value=false;references.value=false
                origin.value?.let { context->
                    restored.value=canonicalResolver.restore(context,readerDocuments.singleOrNull{it.id==context.origin.contentId}?.let{lessonSources(it).map {s->"source:${s.id.value}"}.toSet()}.orEmpty())
                    target.value=(restored.value?.resolution as? Resolution.Found)?.target
                }
            }
            target.value!=null && lessonHistory.isNotEmpty() -> {
                target.value=lessonHistory.removeAt(lessonHistory.lastIndex);resolution.value=null;restored.value=null
            }
            target.value!=null -> {
                val id=target.value!!.contentId
                target.value=null;resolution.value=null
                references.value=navigationSigns.any{it.id==id} || navigationReferenceGroups.any{it.id==id}
                if(!references.value){origin.value=null;restored.value=null;lessonHistory.clear()}
            }
            else -> {target.value=null;resolution.value=null;references.value=false}
        }
    }
    val readers=mutableMapOf<ContentId,androidx.compose.foundation.lazy.LazyListState>()
}
/** Route state belongs to the tab owner so switching tabs does not discard reading/navigation. */
@Composable internal fun LearningRoute(initialResolution:Resolution?=null,libraryState:LearningLibraryState=remember {LearningLibraryState()},initialReferences:Boolean=false,retainedState:LearningRouteState=remember {LearningRouteState(initialResolution,initialReferences)},onExternal:(SourceReference)->Boolean) {
    var target by retainedState.target
    var resolution by retainedState.resolution
    var directory by retainedState.directory
    var source by retainedState.source
    var origin by retainedState.origin
    var restored by retainedState.restored
    var directoryFocus by retainedState.directoryFocus
    val directoryScroll=retainedState.directoryScroll
    var references by retainedState.references
    fun open(t:ContentTarget){
        val previous=target
        if(previous!=null && previous!=t && readerDocuments.any{it.id==previous.contentId} && readerDocuments.any{it.id==t.contentId})retainedState.lessonHistory.add(previous)
        restored=null
        val r=canonicalResolver.canonical(t)
        if(r is Resolution.Found){target=r.target;resolution=if(r.notice!=null)r else null}else resolution=r
        directory=false;source=null;references=false
    }
    fun library(){retainedState.lessonHistory.clear();target=null;resolution=null;directory=false;source=null;origin=null;restored=null;references=false}
    fun returnToReading(){
        source=null;directory=false;references=false
        val o=origin
        if(o==null)library() else {
            val document=readerDocuments.singleOrNull{it.id==o.origin.contentId}
            val valid=document?.let{lessonSources(it).map{"source:${it.id.value}"}.toSet()}.orEmpty()
            restored=canonicalResolver.restore(o,valid)
            val r=restored!!.resolution
            if(r is Resolution.Found)target=r.target else resolution=r
        }
    }
    LearningTheme { Box(Modifier.fillMaxSize(),contentAlignment=Alignment.TopCenter) {
        when {
            source!=null -> SourceDetail(source!!,{directoryFocus=source;source=null;directory=true},::returnToReading,onExternal,returnLabel=if(origin==null)"Learning library" else "Return to reading",scroll=retainedState.scroll("source:${source!!.value}"))
            directory -> SourceDirectory(origin,{source=it},::returnToReading,directoryScroll,directoryFocus)
            resolution!=null && resolution !is Resolution.Found -> DestinationRecovery(resolution!!,::open,::library,onExternal)
            references -> Column(Modifier.widthIn(max=800.dp).fillMaxSize().verticalScroll(retainedState.scroll("references")).padding(24.dp)) {TextButton(::library){Text("Learning library")};if(origin!=null)TextButton(::returnToReading){Text("Return to reading")};Text("Road signs and signals",style=MaterialTheme.typography.headlineLarge);Text("${navigationSigns.size} entries · Verified official artwork with editorial English teaching.");navigationReferenceGroups.sortedBy{it.order}.forEach{group->TextButton({open(ContentTarget(group.id))}){Text(group.title)}}}
            target!=null -> {
                val t=target!!
                val group=navigationReferenceGroups.singleOrNull{it.id==t.contentId}
                val sign=navigationSigns.singleOrNull{it.id==t.contentId}
                val sourceDestination=navigationSources.destinations.singleOrNull{it.id==t.contentId}
                when {
                    sourceDestination!=null -> Column(Modifier.widthIn(max=800.dp).fillMaxSize().verticalScroll(retainedState.scroll("source-destination:${t.contentId.value}")).padding(24.dp)) {
                        TextButton(::library){Text("Learning library")}
                        Text(sourceDestination.title,style=MaterialTheme.typography.headlineLarge)
                        sourceDestination.scopedUrls.map{it.referenceId}.distinct().forEach{id->
                            val reference=navigationSources.references.single{it.id==id}
                            TextButton({source=id}){Text(reference.title)}
                            Text(reference.publisher);Text(reference.classificationNote)
                        }
                    }
                    sign!=null -> SignReferenceDetail(sign,readerAssets.single{it.id==sign.assetId},navigationSources.references,{target=null;resolution=null;references=true},onExternal,scrollState=retainedState.scroll("sign:${sign.id.value}"),referenceGroups=navigationReferenceGroups.filter{sign.id in it.entryIds}.map{it.title to {open(ContentTarget(it.id))}})
                    group!=null -> Column(Modifier.widthIn(max=800.dp).fillMaxSize().verticalScroll(retainedState.scroll("group:${t.contentId.value}")).padding(24.dp)) {TextButton(::library){Text("Learning library")};if(origin!=null)TextButton(::returnToReading){Text("Return to reading")};Text(group.title);group.bodyBlocks.forEach{TeachingBlock(it,emptyMap()){link->when(link){is TeachingLink.Internal->open(link.target);is TeachingLink.ExternalSource->{source=link.referenceId}}}};group.entryIds.forEach{id->TextButton({open(ContentTarget(id))}){Text(navigationSigns.single{it.id==id}.englishLabel)}}}
                    else -> LessonReader(t,::open,{id,context->origin=context;source=id;restored=null},::library,(resolution as? Resolution.Found)?.notice,restored,{context->origin=context;directory=true;restored=null},onReference={reference,context->origin=context;restored=null;open(reference)},state=retainedState.readers.getOrPut(t.contentId){androidx.compose.foundation.lazy.LazyListState()})
                }
            }
            else -> LearningLibrary(::open,{directory=true},{references=true},libraryState)
        }
    }}
}
