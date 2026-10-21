package se.korkort

import androidx.compose.runtime.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.ui.unit.dp
import androidx.compose.material3.*
import androidx.compose.foundation.layout.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.Alignment

/** Canonical teaching route; library state may be retained by the application owner. */
@Composable internal fun LearningRoute(initialResolution:Resolution?=null,libraryState:LearningLibraryState=remember {LearningLibraryState()},initialReferences:Boolean=false,onExternal:(SourceReference)->Boolean) {
    var target by remember{mutableStateOf((initialResolution as? Resolution.Found)?.target)}
    var resolution by remember{mutableStateOf(initialResolution)}
    var directory by remember{mutableStateOf(false)}
    var source by remember{mutableStateOf<SourceReferenceId?>(null)}
    var origin by remember{mutableStateOf<ReturnContext?>(null)}
    var restored by remember{mutableStateOf<RestoredContext?>(null)}
    var directoryFocus by remember{mutableStateOf<SourceReferenceId?>(null)}
    val directoryScroll=rememberScrollState()
    var references by remember{mutableStateOf(initialReferences)}
    fun open(t:ContentTarget){
        val r=canonicalResolver.canonical(t)
        if(r is Resolution.Found){target=r.target;resolution=if(r.notice!=null)r else null}else resolution=r
        directory=false;source=null;references=false
    }
    fun library(){target=null;resolution=null;directory=false;source=null;origin=null;restored=null;references=false}
    fun returnToReading(){
        source=null;directory=false
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
            source!=null -> SourceDetail(source!!,{directoryFocus=source;source=null;directory=true},::returnToReading,onExternal,returnLabel=if(origin==null)"Learning library" else "Return to reading")
            directory -> SourceDirectory(origin,{source=it},::returnToReading,directoryScroll,directoryFocus)
            resolution!=null && resolution !is Resolution.Found -> DestinationRecovery(resolution!!,::open,::library,onExternal)
            references -> Column(Modifier.widthIn(max=800.dp).fillMaxSize().verticalScroll(rememberScrollState()).padding(24.dp)) {TextButton(::library){Text("Learning library")};if(origin!=null)TextButton(::returnToReading){Text("Return to reading")};Text("Road signs and signals",style=MaterialTheme.typography.headlineLarge);Text("${navigationSigns.size} entries · Verified official artwork with editorial English teaching.");navigationReferenceGroups.sortedBy{it.order}.forEach{group->TextButton({open(ContentTarget(group.id))}){Text(group.title)}}}
            target!=null -> {
                val t=target!!
                val group=navigationReferenceGroups.singleOrNull{it.id==t.contentId}
                val sign=navigationSigns.singleOrNull{it.id==t.contentId}
                val sourceDestination=navigationSources.destinations.singleOrNull{it.id==t.contentId}
                when {
                    sourceDestination!=null -> Column(Modifier.widthIn(max=800.dp).fillMaxSize().verticalScroll(rememberScrollState()).padding(24.dp)) {
                        TextButton(::library){Text("Learning library")}
                        Text(sourceDestination.title,style=MaterialTheme.typography.headlineLarge)
                        sourceDestination.scopedUrls.map{it.referenceId}.distinct().forEach{id->
                            val reference=navigationSources.references.single{it.id==id}
                            TextButton({source=id}){Text(reference.title)}
                            Text(reference.publisher);Text(reference.classificationNote)
                        }
                    }
                    sign!=null -> SignReferenceDetail(sign,readerAssets.single{it.id==sign.assetId},navigationSources.references,{target=null;resolution=null;references=true},onExternal,referenceGroups=navigationReferenceGroups.filter{sign.id in it.entryIds}.map{it.title to {open(ContentTarget(it.id))}})
                    group!=null -> Column(Modifier.widthIn(max=800.dp).fillMaxSize().verticalScroll(rememberScrollState()).padding(24.dp)) {TextButton(::library){Text("Learning library")};if(origin!=null)TextButton(::returnToReading){Text("Return to reading")};Text(group.title);group.bodyBlocks.forEach{TeachingBlock(it,emptyMap()){link->when(link){is TeachingLink.Internal->open(link.target);is TeachingLink.ExternalSource->{source=link.referenceId}}}};group.entryIds.forEach{id->TextButton({open(ContentTarget(id))}){Text(navigationSigns.single{it.id==id}.englishLabel)}}}
                    else -> LessonReader(t,::open,{id,context->origin=context;source=id;restored=null},::library,(resolution as? Resolution.Found)?.notice,restored,{context->origin=context;directory=true;restored=null},onReference={reference,context->origin=context;restored=null;open(reference)})
                }
            }
            else -> LearningLibrary(::open,{directory=true},{references=true},libraryState)
        }
    }}
}
