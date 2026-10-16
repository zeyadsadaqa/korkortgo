package se.korkort

import androidx.compose.foundation.focusable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.input.key.*
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties

/** Assessment callers construct this only from the gated presentation, never SignEntry captions. */
data class ImageViewerContent(val asset: CurriculumAsset, val title: String, val description: String) {
    companion object {
        fun assessment(picture: AssessmentImagePresentation, assets: List<CurriculumAsset>): ImageViewerContent =
            ImageViewerContent(assets.single { it.id==picture.assetId },"Question illustration",picture.description)
    }
}

@Composable
internal fun ImageViewerSurface(content: ImageViewerContent, onClose: () -> Unit) {
    var viewport by remember(content.asset.id) { mutableStateOf(ImageViewport()) }
    var loaded by remember(content.asset.id) { mutableStateOf(false) }
    var sourceSize by remember { mutableStateOf(Size.Zero) }
    var viewportSize by remember { mutableStateOf(Size.Zero) }
    val focus=remember { FocusRequester() }
    fun set(value: ImageViewport) {
        viewport=if(sourceSize.width>0 && viewportSize.width>0 && viewportSize.height>0)
            value.clamp(sourceSize.width,sourceSize.height,viewportSize.width,viewportSize.height) else value
    }
    fun pan(delta: Offset) { set(viewport.copy(pan=viewport.pan+delta)) }
        Surface(Modifier.fillMaxSize()) {
            Column(Modifier.fillMaxSize().windowInsetsPadding(WindowInsets.safeDrawing).padding(20.dp)
                .onPreviewKeyEvent { event ->
                    if(event.type==KeyEventType.KeyDown && event.key==Key.Escape) {onClose();true}
                    else if(event.type!=KeyEventType.KeyDown || !loaded) false else when(event.key) {
                        Key.DirectionLeft -> {pan(Offset(48f,0f));true}
                        Key.DirectionRight -> {pan(Offset(-48f,0f));true}
                        Key.DirectionUp -> {pan(Offset(0f,48f));true}
                        Key.DirectionDown -> {pan(Offset(0f,-48f));true}
                        Key.Plus,Key.Equals,Key.NumPadAdd -> {set(viewport.zoomTo(viewport.zoom*1.5f));true}
                        Key.Minus,Key.NumPadSubtract -> {set(viewport.zoomTo(viewport.zoom/1.5f));true}
                        Key.Home -> {viewport=viewport.reset();true}
                        Key.Escape -> {onClose();true}
                        else -> false
                    }
                },verticalArrangement=Arrangement.spacedBy(12.dp)) {
                // Scrollable controls remain reachable at large text; the image can shrink before controls clip.
                Column(Modifier.heightIn(max=180.dp).verticalScroll(rememberScrollState())) {
                    Text(content.title,style=MaterialTheme.typography.titleLarge)
                    OutlinedButton(shape=RoundedCornerShape(6.dp), onClick=onClose,modifier=Modifier.heightIn(min=48.dp)) {Text("Close")}
                }
                Box(Modifier.weight(1f).fillMaxWidth().focusRequester(focus).focusable()
                    .semantics { contentDescription="Image viewport. Arrow keys pan when enlarged." }) {
                    ExactAssetImage(content.asset,content.description,Modifier.fillMaxSize(),viewport,{set(it)},
                        onLoaded={loaded=it},onGeometry={source,window->sourceSize=source;viewportSize=window;set(viewport)})
                }
                Column(Modifier.heightIn(max=220.dp).verticalScroll(rememberScrollState())) {
                    FlowRow(horizontalArrangement=Arrangement.spacedBy(8.dp),verticalArrangement=Arrangement.spacedBy(4.dp)) {
                        OutlinedButton(shape=RoundedCornerShape(6.dp), onClick={set(viewport.zoomTo(viewport.zoom*1.5f))},enabled=loaded && viewport.zoom<8f,modifier=Modifier.heightIn(min=48.dp)) {Text("Zoom in")}
                        OutlinedButton(shape=RoundedCornerShape(6.dp), onClick={set(viewport.zoomTo(viewport.zoom/1.5f))},enabled=loaded && viewport.zoom>1f,modifier=Modifier.heightIn(min=48.dp)) {Text("Zoom out")}
                        OutlinedButton(shape=RoundedCornerShape(6.dp), onClick={viewport=viewport.reset()},enabled=loaded,modifier=Modifier.heightIn(min=48.dp)) {Text("Reset")}
                    }
                    Text("${(viewport.zoom*100).toInt()}% · Original artwork proportions preserved.",Modifier.semantics { liveRegion=LiveRegionMode.Polite },style=MaterialTheme.typography.bodySmall)
                }
            }
            LaunchedEffect(Unit) { focus.requestFocus() }
        }
}

@Composable
fun AccessibleImageViewer(content: ImageViewerContent, onClose: () -> Unit) {
    Dialog(onDismissRequest=onClose,properties=DialogProperties(usePlatformDefaultWidth=false)) {
        ImageViewerSurface(content,onClose)
    }
}
