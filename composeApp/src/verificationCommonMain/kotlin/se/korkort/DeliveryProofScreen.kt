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
import kotlin.random.Random

/** Build-time-only verification host. No accepted session, score, history or production route. */
@Composable
fun DeliveryProofScreen(initialCode: String = "S1", initialMode: String = "meaning", dark: Boolean = false, fontScale: Float = 1f, onReady: (Boolean) -> Unit = {}) {
    var code by remember {mutableStateOf(initialCode)}
    var mode by remember {mutableStateOf(initialMode)}
    var selected by remember(code,mode) {mutableStateOf(false)}
    val uri=LocalUriHandler.current
    if(initialMode.startsWith("learning")) {
        val initial=remember(initialCode,initialMode) {when(initialMode) {
            "learning-question" -> canonicalResolver.lookup(questionId=QuestionId(initialCode))
            "learning-chapter" -> canonicalResolver.legacy(LegacyLookup.Chapter("legacy-app-4768933c3d9a",initialCode))
            "learning-sign" -> canonicalResolver.legacy(LegacyLookup.Sign("legacy-app-4768933c3d9a",initialCode))
            else -> if(initialCode=="S1")null else canonicalResolver.canonical(ContentTarget(ContentId(initialCode)))
        }}
        Box(Modifier.fillMaxSize().windowInsetsPadding(WindowInsets.safeDrawing)) {
            CompositionLocalProvider(LocalDensity provides Density(LocalDensity.current.density,fontScale)) {
                LearningRoute(initial) {reference->runCatching{uri.openUri(reference.url)}.isSuccess}
            }
        }
        return
    }
    val density=LocalDensity.current
    @Composable fun content() {
        Surface(Modifier.fillMaxSize()) {
            Column(Modifier.fillMaxSize().windowInsetsPadding(WindowInsets.safeDrawing)) {
                FlowRow(horizontalArrangement=Arrangement.spacedBy(4.dp)) {
                    Text("Unscored verification fixture",Modifier.padding(8.dp))
                    TextButton(onClick={
                        val ids=if(mode=="candidate") candidateQuestions9J.filter {it.acceptance.eligibility==ScoringEligibility.HELD}.map {it.key.questionId.value} else deliveryFixtureCodes
                        code=ids[(ids.indexOf(code)+1)%ids.size]
                    }) {Text("Next fixture")}
                    listOf("reference","meaning","recognise").forEach {value->TextButton(onClick={
                        if(mode=="candidate") {
                            val target=candidateQuestions9J.single {it.key.questionId.value==code}.feedback.targetSignCode
                            code=deliveryFixtureCodes.firstOrNull {it==target} ?: deliveryFixtureCodes.first()
                        }
                        mode=value
                    }) {Text(value)}}
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
                            ExactAssetImage(asset,picture.description,Modifier.readableArtworkFrame(),onLoaded={first=it})
                            Text("Option image")
                            ExactAssetImage(asset,picture.description,Modifier.readableArtworkFrame(),onLoaded={second=it})
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
                            val presentation = if (mode == "candidate") {
                                candidateQuestions9J.single { it.key.questionId.value == code }
                                    .snapshot(candidateIdentity9J, Random(9)).presentation(null, false, true)
                            } else deliveryCandidate(code,mode)
                            Box(Modifier.weight(1f)) {AssessmentWithImageViewer(presentation,{selected=true},navigationAssets)}
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
