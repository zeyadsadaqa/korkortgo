@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort
import androidx.compose.runtime.*
import kotlin.test.*
class RecoveryActions10GTest {
 @Test fun exactPage46ChooserAndUnavailableLibraryActions() {
  val res=canonicalResolver.legacy(LegacyLookup.Page("legacy-app-4768933c3d9a",46)) as Resolution.Choices
  val rows=mutableListOf<Any>()
  for(choice in res.choices){RecoveryHarness10G().use{h->
   val opened=mutableListOf<String>();h.scene.setContent{LearningRoute(res,onExternal={opened.add(it.url);true})}
   h.await("Chooser missing"){h.text().contains("Choose related teaching")}
   assertTrue(res.choices.all{it.entry.title in h.texts()});assertFalse(h.text().contains("Learning objectives"))
   h.capture("10G2","chooser-${choice.target.contentId.value}");h.click(choice.entry.title)
   h.await("Exact selected lesson missing"){choice.entry.title in h.texts() && !h.text().contains("Choose related teaching")}
   h.click("Learning library");h.await("Library recovery missing"){h.text().contains("Search lessons")}
   assertTrue(opened.isEmpty());rows.add(mapOf("case" to "page46-choice","selected_target" to choice.target,"title" to choice.entry.title,"chooser_offered_targets" to res.choices.map{it.target},"returned_to_library" to true,"status" to "pass"))
  }}
  for((name,resolution) in listOf("unknown-canonical" to canonicalResolver.canonical(ContentTarget(ContentId("unknown"))),"unknown-question" to canonicalResolver.lookup(questionId=QuestionId("unknown"),legacy=LegacyLookup.Page("legacy-app-4768933c3d9a",46)),"gap-page" to canonicalResolver.legacy(LegacyLookup.Page("legacy-app-4768933c3d9a",13)))){
   RecoveryHarness10G().use{h->h.scene.setContent{LearningRoute(resolution,onExternal={error("Unexpected external action")})};h.await("Recovery missing"){h.text().contains("Content unavailable")};assertFalse(h.text().contains("Choose related teaching"));assertFalse(h.text().contains("Open official description"));h.capture("10G2",name);h.click("Open learning library");h.await("Library missing"){h.text().contains("Search lessons")};rows.add(mapOf("case" to name,"status" to "pass","recovery" to "explicit library action; no automatic target"))}
  }
  val origin=navigationAliases.aliases.first().origin;val synthetic=mutableListOf<Any>()
  for(count in 0..2){val ids=canonicalEntries.take(count).map{it.id};val resolver=CanonicalResolver(canonicalEntries,canonicalAnchors,LegacyAliasPayload(1,emptyList(),listOf(ContentTombstone(ContentId("fixture-retired-content"),ids,"Reviewed synthetic retirement",ReviewEvidence(origin,null)))));val actual=resolver.canonical(ContentTarget(ContentId("fixture-retired-content")));if(count==0)assertIs<Resolution.Unavailable>(actual) else assertEquals(ids,(actual as Resolution.Choices).choices.map{it.target.contentId});synthetic.add(mapOf("replacement_ids" to ids,"actual" to actual,"scope" to "synthetic only; production tombstones remain empty"))}
  assertFalse(practiceStartCheck("1",candidatePracticeBank9M).allowed)
  assertIs<Resolution.Found>(canonicalResolver.lookup(questionId=QuestionId("sign-meaning-S1")))
  Proof10G.write("10G2","recovery-action-observations.json",mapOf("status" to "pass_shared_scope","actions" to rows,"retirement_fixtures" to synthetic,"historical_unaccepted_candidate_scoring_gate" to "rejected while related teaching remains reachable; current replacements are accepted","limits" to "Real LearningRoute/DestinationRecovery components, injected internal resolver entry; shared semantic actions1000x1800, default production theme. No public deep-link/parser, native/browser or assistive-speech claim."))
 }
}
