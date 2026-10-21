@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.platform.UriHandler
import kotlin.test.*
class UnavailableSignals10GTest {
 @Test fun allExactUnavailableSignalsUseOfficialActionsAndSafeRecovery() {
  val rows=mutableListOf<Any>();val ns="legacy-app-4768933c3d9a"
  for(code in listOf("SIG16","SIG17","SIG18")){
   val resolution=canonicalResolver.legacy(LegacyLookup.Sign(ns,code)) as Resolution.Unavailable
   assertEquals(listOf(ContentTarget(ContentId("M03-L02"))),resolution.related)
   assertIs<Resolution.Unavailable>(canonicalResolver.canonical(ContentTarget(ContentId("sign-$code"))))
   assertFalse(navigationSigns.any{it.code==code});assertFalse(navigationAssets.any{it.codeOrIllustrationId==code})
   val reference=navigationSources.references.single{it.id==resolution.officialReferenceId};val related=readerDocuments.single{it.id==ContentId("M03-L02")}
   val opened=mutableListOf<String>();var fail=true
   RecoveryHarness10G().use{h->
    h.scene.setContent{CompositionLocalProvider(LocalUriHandler provides object:UriHandler{override fun openUri(uri:String){opened.add(uri);if(fail)error("Injected host URI failure")}}){val uri=LocalUriHandler.current;LearningRoute(resolution,onExternal={r->runCatching{uri.openUri(r.url)}.isSuccess})}}
    h.await("Unavailable action missing"){h.text().contains("Content unavailable") && h.text().contains("Open official description")}
    assertTrue(h.text().contains(resolution.message));assertTrue(related.title in h.texts());h.capture("10G3","$code-unavailable")
    h.click("Open official description");assertEquals(listOf(reference.url),opened)
    assertTrue(h.text().contains("The official description could not be opened."));assertTrue(h.text().contains("Content unavailable"));h.capture("10G3","$code-open-failed")
    fail=false;h.click("Open official description");assertEquals(listOf(reference.url,reference.url),opened);assertFalse(h.text().contains("The official description could not be opened."));assertTrue(h.text().contains("Content unavailable"))
    h.click(related.title);h.await("Wrong related teaching"){related.title in h.texts() && !h.text().contains("Content unavailable")};h.capture("10G3","$code-related")
    h.click("Learning library");h.await("Library missing"){h.text().contains("Search lessons")}
    rows.add(mapOf("code" to code,"policy" to "unavailable_exact_entry","actual_resolution" to resolution,"official_reference" to reference,"attempted_urls" to opened,"first_open" to "injected_host_failure_retains_route_and_actions","retry" to "registered_URI_callback_success_retains_route","related_action" to ContentTarget(related.id),"library_recovery" to "explicit_action","status" to "pass_shared_scope"))
   }
  }
  Proof10G.write("10G3","shared-unavailable-signal-observations.json",mapOf("identity" to acceptedIdentity9J,"status" to "pass_shared_scope","signals" to rows,"limits" to "Real LearningRoute/DestinationRecovery and URI abstraction; internal injected entry, shared semantic actions. URI callbacks do not establish OS/browser dispatch, network availability, fresh source validity or assistive speech."))
 }
}
