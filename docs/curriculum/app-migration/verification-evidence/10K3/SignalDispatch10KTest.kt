@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort
import kotlin.test.*
class SignalDispatch10KTest {
 @Test fun exactUnavailableSignalCallbacksAndRecovery() {
  val rows=mutableListOf<Any>()
  for(code in listOf("SIG16","SIG17","SIG18"))for(accepted in listOf(false,true))LibraryHarness10J(390,1800).use{h->
   val resolution=canonicalResolver.legacy(LegacyLookup.Sign("legacy-app-4768933c3d9a",code)) as Resolution.Unavailable
   val expected=navigationSources.references.single{it.id==resolution.officialReferenceId};var actual:String?=null
   h.scene.setContent{LearningRoute(resolution,onExternal={actual=it.url;accepted})};h.await("unavailable"){h.text().contains("Content unavailable")};h.click("Open official description");assertEquals(expected.url,actual)
   assertEquals(!accepted,h.text().contains("The official description could not be opened."))
   h.capture("10K3","signal-$code-$accepted");h.click("Open learning library");h.await("recovery"){h.text().contains("Search lessons")}
   rows.add(mapOf("signal" to code,"callback_accepted" to accepted,"url" to actual,"recovery" to true))
  }
  Proof10J.write("10K3","signal-dispatch-observations.json",mapOf("cases" to rows,"scope" to "Fresh configuredJVM callback/failure/recovery; not an OS browser or remote website assertion"))
 }
}
