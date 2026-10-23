package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.Density
import androidx.compose.ui.unit.dp
import kotlin.random.Random

/** Unscored changed-record fixtures. Never a normal route or accepted package activation. */
@Composable internal fun Step10CorrectionProof(initialCode:String,mode:String,dark:Boolean,fontScale:Float,questions:List<AssessmentQuestion> = step10CandidateQuestions,identity:ContentPackageIdentity=step10CandidateIdentity,fixtureLabel:String="Unscored correction fixture") {
    val ids=when(mode) {
        "corrected-source" -> step10CorrectedSources.map{it.id.value}
        "corrected-sign" -> step10CorrectedSigns.map{it.code}
        else -> questions.map{it.key.questionId.value}
    }
    var code by remember { mutableStateOf(initialCode.takeIf{it in ids} ?: ids.first()) }
    val density=LocalDensity.current
    LearningTheme { RootModalHost { CompositionLocalProvider(LocalDensity provides Density(density.density,fontScale)) {
        @Composable fun body() {
            Column(Modifier.fillMaxSize().windowInsetsPadding(WindowInsets.safeDrawing)) {
                Text(fixtureLabel,Modifier.padding(8.dp))
                Text("Fixture: $code")
                TextButton({code=ids[(ids.indexOf(code)+1)%ids.size]}) {Text("Next fixture")}
                key(code) {
                    when(mode) {
                        "corrected-source" -> SourceDetail(SourceReferenceId(code),{},{},{false},references=step10CorrectedSources)
                        "corrected-sign" -> {
                            val sign=step10CorrectedSigns.single{it.code==code}
                            SignReferenceDetail(sign,step10CorrectedAssets.single{it.id==sign.assetId},navigationSources.references,{},{false})
                        }
                        else -> {
                            val q=questions.single{it.key.questionId.value==code}
                            val expected=(listOfNotNull(q.image)+q.options.mapNotNull{it.image}).map{it.assetId}.toSet()
                            var loaded by remember { mutableStateOf(emptySet<AssetId>()) }
                            var confirmed by remember { mutableStateOf(false) }
                            Text(if(loaded.containsAll(expected))"Exact question images ready" else "Question images loading")
                            Box(Modifier.weight(1f).padding(16.dp)) {
                                AssessmentWithImageViewer(q.snapshot(identity,Random(9)).presentation(null,false,true),{confirmed=true},navigationAssets,onImageLoaded={id,ok->if(ok)loaded=loaded+id})
                            }
                            if(confirmed)Text("Selection recorded for this unscored verification fixture.")
                        }
                    }
                }
            }
        }
        if(dark)MaterialTheme(colorScheme=darkColorScheme()){Surface(Modifier.fillMaxSize()){body()}}else body()
    }}}
}
