@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort

import androidx.compose.runtime.*
import androidx.compose.material3.*
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.Density
import kotlin.test.*

/** Exact corrected records through production views; unscored opt-in fixtures. */
class CorrectedMetadataStep10Test {
 @Test fun classificationsDatesScopeLimitsAndSignCaptionMatchReviewedRecords() {
  val rows=mutableListOf<Any>()
  val expectedClasses=mapOf("REF-496b85361fc1b2c5" to setOf(SourceClassification.SWEDISH_PUBLIC_SERVICE), "REF-2816f9478f49eea3" to setOf(SourceClassification.SWEDISH_PUBLIC_SERVICE), "REF-56e38aa92cb10d3e" to setOf(SourceClassification.SWEDISH_AUTHORITY_GUIDANCE), "REF-6ca8f251127184be" to setOf(SourceClassification.SWEDISH_AUTHORITY_GUIDANCE), "REF-b3162b40db29d9bd" to setOf(SourceClassification.SWEDISH_AUTHORITY_GUIDANCE), "REF-52a2a9e7d845ad8f" to setOf(SourceClassification.MANUFACTURER))
  assertEquals(6,step10CorrectedSources.size)
  assertEquals(setOf("C18","M8"),step10CorrectedSigns.map{it.code}.toSet())
  for(width in listOf(390,1280))for(scale in listOf(1f,1.6f))LibraryHarness10J(width,1800).use{h->
   for(source in step10CorrectedSources){
    val original=navigationSources.references.single{it.id==source.id}
    assertEquals(expectedClasses.getValue(source.id.value),source.classifications)
    assertEquals(original.url,source.url);assertEquals(original.publisher,source.publisher)
    assertEquals(original.evidence,source.evidence)
    h.scene.setContent{key(source.id){CompositionLocalProvider(LocalDensity provides Density(1f,scale)){LearningTheme{SourceDetail(source.id,{},{},{false},references=step10CorrectedSources)}}}}
    h.await("source title"){h.texts().contains(source.title)}
    assertTrue(h.texts().contains(source.classifications.joinToString(" · "){it.name.lowercase().replace('_',' ')}))
    assertTrue(h.texts().contains(source.classificationNote));assertTrue(h.texts().contains("Scope"));assertTrue(h.texts().contains("Limits"))
    source.evidence.forEach{e->assertTrue(h.texts().contains(e.scope));assertTrue(h.texts().contains(e.finding));e.limitations.forEach{assertTrue(h.texts().contains(it))}}
    h.click("View source evidence records")
    source.evidence.forEach{e->assertTrue(h.texts().contains("Checked: ${e.dates.checkedOn ?: "Not recorded"}"));assertTrue(h.texts().contains("Retrieved: ${e.dates.retrievedOn ?: "Not recorded"}"));assertTrue(h.texts().contains("Published: ${e.dates.publishedOn ?: "Not recorded"}"))}
    h.capture("10L3/content-corrections/metadata-active-r2","${source.id.value}-$width-$scale")
    rows.add(mapOf("source_id" to source.id.value,"width" to width,"font_scale" to scale,"exact_evidence_dates_scope_limits" to "pass"))
   }
   for(sign in step10CorrectedSigns){
    val asset=step10CorrectedAssets.single{it.id==sign.assetId}
    val oldAsset=navigationAssets.single{it.id==asset.id}
    assertEquals(oldAsset.original,asset.original);assertEquals(oldAsset.bundled,asset.bundled)
    h.scene.setContent{key(sign.id){CompositionLocalProvider(LocalDensity provides Density(1f,scale)){LearningTheme{SignReferenceDetail(sign,asset,navigationSources.references,{},{false})}}}}
    h.await("corrected caption"){h.texts().contains(sign.caption.assessmentText())}
    assertFalse(h.text().contains("Loading image"))
    h.capture("10L3/content-corrections/metadata-active-r2","${sign.code}-$width-$scale")
    rows.add(mapOf("sign_code" to sign.code,"width" to width,"font_scale" to scale,"caption" to sign.caption.assessmentText(),"official_bytes_unchanged" to true))
   }
  }
  Proof10J.write("10L3/content-corrections/metadata-active-r2","results.json",mapOf("scope" to "corrected shared component text/metadata; native visual acceptance separate","cases" to rows))
 }
}
