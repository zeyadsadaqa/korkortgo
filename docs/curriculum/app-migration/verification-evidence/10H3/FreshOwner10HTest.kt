@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.AnnotatedString
import kotlin.test.*
class FreshOwner10HTest {
 @Test fun setupPreferencesSurviveNavigationButFreshAppOwnerRestoresDefaults() {
  val rows=mutableListOf<Any>()
  repeat(2){launch->RecoveryHarness10H().use{h->
   h.scene.setContent{App()};h.await("Home"){h.text().contains("practice questions")};h.click("Start a practice test  >")
   fun count()=h.nodes().first{it.config.getOrNull(SemanticsProperties.EditableText)!=null}.config[SemanticsProperties.EditableText].text
   fun selected(label:String)=h.nodes().any{it.config.getOrNull(SemanticsProperties.Selected)==true && it.config.getOrNull(SemanticsProperties.Text).orEmpty().any{t->t.text==label}}
   assertEquals("70",count());assertTrue(selected("After each question"))
   val field=h.nodes().first{it.config.getOrNull(SemanticsActions.SetText)?.action!=null};field.config[SemanticsActions.SetText].action!!.invoke(AnnotatedString("20"));h.render();h.click("At the end of the test")
   h.click("Overview");h.click("Practice");assertEquals("20",count());assertTrue(selected("At the end of the test"))
   rows.add(mapOf("shared_owner_creation" to launch+1,"fresh_count" to "70","fresh_feedback" to "immediate","same_process_count" to "20","same_process_feedback" to "at_end","session_auto_started" to false))
  }}
  Proof10H.write("10H3","fresh-owner-results.json",mapOf("identity" to acceptedIdentity9J,"status" to "pass_shared_scope","runs" to rows,"scope" to "Dispose shared Compose scene and create new App owner; no OS process kill/relaunch inferred"))
 }
}
