package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusProperties
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp

/** Approved 8J detail. The caller owns canonical routing and validates its return context. */
@Composable
fun SignReferenceDetail(
    entry: SignEntry,
    asset: CurriculumAsset,
    references: List<SourceReference>,
    onBack: () -> Unit,
    onExternal: (SourceReference) -> Boolean,
    modifier: Modifier = Modifier,
    referenceGroups: List<Pair<String, () -> Unit>> = emptyList(),
    viewerHost: @Composable (ImageViewerContent, () -> Unit) -> Unit = { content,close -> AccessibleImageViewer(content,close) },
) {
    require(entry.assetId==asset.id)
    val scroll=rememberScrollState()
    var viewer by remember(entry.id) { mutableStateOf(false) }
    var credits by remember(entry.id) { mutableStateOf(false) }
    var openedViewer by remember(entry.id) { mutableStateOf(false) }
    var error by remember(entry.id) { mutableStateOf<String?>(null) }
    val enlargeFocus=remember(entry.id) { FocusRequester() }
    val titleStyle=MaterialTheme.typography.headlineLarge.copy(fontFamily=FontFamily.Serif)
    val bound=entry.sourceUses.map { use->references.single { it.id==use.referenceId } }.distinctBy { it.id }
    val official=bound.firstOrNull { it.publisher=="Transportstyrelsen" && "transportstyrelsen.se" in it.url }
    fun open(reference: SourceReference) { if(!onExternal(reference))error="Could not open the official page. You can still use this reference and its saved sources." }
    LaunchedEffect(viewer) { if(openedViewer && !viewer) {withFrameNanos {};enlargeFocus.requestFocus()} }
    if(viewer) {
        viewerHost(ImageViewerContent(asset,"${entry.code} · ${entry.englishLabel}",asset.studyAltText)) {viewer=false}
        return
    }
    Surface(Modifier.fillMaxSize(),color=MaterialTheme.colorScheme.background,contentColor=MaterialTheme.colorScheme.onBackground) {
    Column(modifier.fillMaxSize().verticalScroll(scroll).padding(24.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
        referenceGroups.forEach { (title,action) -> TextButton(onClick=action) {Text(title)} }
        TextButton(onClick=onBack) {Text("‹ Road signs and reference")}
        BoxWithConstraints(Modifier.fillMaxWidth()) {
            val wide=maxWidth>=720.dp
            @Composable fun identity() {
                Text(entry.code,style=MaterialTheme.typography.labelLarge)
                Text(entry.englishLabel,style=titleStyle)
                Text(entry.officialNameSv,style=MaterialTheme.typography.headlineSmall)
            }
            @Composable fun artwork() {
                ExactAssetImage(asset,asset.studyAltText,Modifier.fillMaxWidth().heightIn(min=180.dp).height(if(wide) 380.dp else 220.dp))
                OutlinedButton(shape=RoundedCornerShape(6.dp), onClick={openedViewer=true;viewer=true},modifier=Modifier.fillMaxWidth().heightIn(min=48.dp).focusRequester(enlargeFocus).focusProperties{canFocus=true}) {Text("Enlarge image")}
            }
            @Composable fun description() {
                Text(entry.caption.assessmentText(),style=MaterialTheme.typography.bodyLarge)
                if(entry.translationStatus==TranslationStatus.EDITORIAL_ENGLISH) Text("Editorial English translation; not an official agency translation.",style=MaterialTheme.typography.bodySmall)
                entry.limitations.forEach { Text(it,style=MaterialTheme.typography.bodySmall) }
                official?.let { reference -> OutlinedButton(shape=RoundedCornerShape(6.dp), onClick={open(reference)},modifier=Modifier.fillMaxWidth().heightIn(min=48.dp)) {Text("Official description")}}
                OutlinedButton(shape=RoundedCornerShape(6.dp), onClick={credits=!credits},modifier=Modifier.fillMaxWidth().heightIn(min=48.dp)) {Text("Sources and artwork credits")}
            }
            if(wide) Row(horizontalArrangement=Arrangement.spacedBy(28.dp)) {
                Column(Modifier.weight(1f),verticalArrangement=Arrangement.spacedBy(12.dp)) {artwork()}
                Column(Modifier.weight(1f),verticalArrangement=Arrangement.spacedBy(16.dp)) {identity();description()}
            } else Column(verticalArrangement=Arrangement.spacedBy(16.dp)) {identity();artwork();description()}
        }
        error?.let { Text(it) }
        if(credits) {
            HorizontalDivider()
            bound.forEach { reference ->
                Text(reference.title,style=MaterialTheme.typography.titleMedium)
                Text(reference.publisher)
                Text(reference.classificationNote)
                reference.evidence.forEach { evidence ->
                    Text(evidence.scope)
                    evidence.dates.checkedOn?.let {Text("Checked: $it")}
                    evidence.dates.retrievedOn?.let {Text("Retrieved: $it")}
                    evidence.dates.publishedOn?.let {Text("Published: $it")}
                    evidence.limitations.forEach {Text(it)}
                }
                TextButton(onClick={open(reference)}) {Text("Open ${reference.publisher} page")}
            }
            asset.reuse.forEach { Text(it.credit);Text(it.conditions) }
        }
    }
    }
}
