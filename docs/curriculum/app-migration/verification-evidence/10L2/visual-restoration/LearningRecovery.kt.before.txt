package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.dp

@Composable internal fun DestinationRecovery(resolution:Resolution,onOpen:(ContentTarget)->Unit,onLibrary:()->Unit,onExternal:(SourceReference)->Boolean) {
    var failed by remember(resolution){mutableStateOf(false)}
    Column(Modifier.widthIn(max=800.dp).fillMaxWidth().padding(24.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
        when(resolution) {
            is Resolution.Found -> {resolution.notice?.let{Text(it,Modifier.semantics{liveRegion=LiveRegionMode.Polite})};TextButton({onOpen(resolution.target)}){Text(resolution.entry.title)}}
            is Resolution.Choices -> {
                Text("Choose related teaching",style=MaterialTheme.typography.headlineSmall,modifier=Modifier.semantics{heading()})
                Text(resolution.notice)
                resolution.choices.forEach { choice -> OutlinedButton({onOpen(choice.target)},Modifier.fillMaxWidth()){Text(choice.entry.title)} }
            }
            is Resolution.Unavailable -> {
                Text("Content unavailable",style=MaterialTheme.typography.headlineSmall,modifier=Modifier.semantics{heading()})
                Text(resolution.message)
                resolution.officialReferenceId?.let{id->navigationSources.references.singleOrNull{it.id==id}?.let{reference->
                    Button({failed=!onExternal(reference)}){Text("Open official description")}
                }}
                resolution.related.forEach{target->val found=canonicalResolver.canonical(target) as? Resolution.Found
                    found?.let{TextButton({onOpen(it.target)}){Text(it.entry.title)}}
                }
            }
        }
        if(failed)Text("The official description could not be opened. You can still use the actions below.",Modifier.semantics{liveRegion=LiveRegionMode.Polite})
        TextButton(onLibrary){Text("Open learning library")}
    }
}

/** A missing session never constructs results or starts a test. Preferences belong to setup. */
@Composable internal fun MissingResults(onSetup:()->Unit) {
    Column(Modifier.padding(24.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
        Card(colors=CardDefaults.cardColors(containerColor=MaterialTheme.colorScheme.secondaryContainer)){Text("No saved result is available.",style=MaterialTheme.typography.headlineSmall,modifier=Modifier.padding(16.dp).semantics{heading()})}
        Button(onSetup){Text("Set up a practice test")}
    }
}
