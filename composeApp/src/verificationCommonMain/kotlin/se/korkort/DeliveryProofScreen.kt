package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.Density
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.unit.dp

/** Build-time-only verification host. No accepted session, score, history or production route. */
@Composable
fun DeliveryProofScreen(initialCode: String = "S1", initialMode: String = "meaning", dark: Boolean = false, fontScale: Float = 1f, onReady: (Boolean) -> Unit = {}) {
    var code by remember {mutableStateOf(initialCode)}
    var mode by remember {mutableStateOf(initialMode)}
    var selected by remember(code,mode) {mutableStateOf(false)}
    val uri=LocalUriHandler.current
    if(initialMode=="learning") {
        Box(Modifier.fillMaxSize().windowInsetsPadding(WindowInsets.safeDrawing)) {
            LearningRoute {reference->runCatching{uri.openUri(reference.url)}.isSuccess}
        }
        return
    }
    val density=LocalDensity.current
    @Composable fun content() {
        Surface(Modifier.fillMaxSize()) {
            Column(Modifier.fillMaxSize().windowInsetsPadding(WindowInsets.safeDrawing)) {
                FlowRow(horizontalArrangement=Arrangement.spacedBy(4.dp)) {
                    Text("Unscored verification fixture",Modifier.padding(8.dp))
                    TextButton(onClick={code=deliveryFixtureCodes[(deliveryFixtureCodes.indexOf(code)+1)%deliveryFixtureCodes.size]}) {Text("Next fixture")}
                    listOf("reference","meaning","recognise").forEach {value->TextButton(onClick={mode=value}) {Text(value)}}
                }
                key(code,mode) {
                    if(mode=="delivery") {
                        val picture=requireNotNull(deliveryCandidate(code,"meaning").image)
                        val asset=navigationAssets.single {it.id==picture.assetId}
                        var first by remember {mutableStateOf<Boolean?>(null)}
                        var second by remember {mutableStateOf<Boolean?>(null)}
                        var viewer by remember {mutableStateOf(false)}
                        var opened by remember {mutableStateOf(false)}
                        val focus=remember {FocusRequester()}
                        Column(Modifier.weight(1f).verticalScroll(rememberScrollState()).padding(16.dp),verticalArrangement=Arrangement.spacedBy(12.dp)) {
                            Text("Question image")
                            ExactAssetImage(asset,picture.description,Modifier.fillMaxWidth().height(180.dp),onLoaded={first=it})
                            Text("Option image")
                            ExactAssetImage(asset,picture.description,Modifier.fillMaxWidth().height(105.dp),onLoaded={second=it})
                            OutlinedButton(onClick={opened=true;viewer=true},modifier=Modifier.heightIn(min=48.dp).focusRequester(focus)) {Text("Enlarge image")}
                        }
                        if(viewer)AccessibleImageViewer(ImageViewerContent.assessment(picture,navigationAssets)) {viewer=false}
                        LaunchedEffect(viewer) {if(opened && !viewer) {withFrameNanos {};focus.requestFocus()}}
                        LaunchedEffect(first,second) {if(first!=null && second!=null) {withFrameNanos {};onReady(first==true && second==true)}}
                    } else if(mode=="reference") {
                        val sign=navigationSigns.single {it.code==code}
                        SignReferenceDetail(sign,navigationAssets.single {it.id==sign.assetId},navigationSources.references,{}, {ref->runCatching {uri.openUri(ref.url)}.isSuccess})
                    } else {
                        Column(Modifier.weight(1f).padding(16.dp)) {
                            Box(Modifier.weight(1f)) {AssessmentWithImageViewer(deliveryCandidate(code,mode),{selected=true},navigationAssets)}
                            if(selected)Text("Selection recorded for this unscored verification fixture.")
                        }
                    }
                }
            }
        }
    }
    CompositionLocalProvider(LocalDensity provides Density(density.density,fontScale)) {
        if(dark)MaterialTheme(colorScheme=darkColorScheme()) {content()} else KorkortTheme {content()}
    }
}
