@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.AnnotatedString
import kotlin.test.*
class ProductionGuard10HTest {
 @Test fun acceptedProductionOwnerCancelDiscardAndModalTree() {
  val rows=mutableListOf<Any>()
  for(mode in Feedback.entries)RecoveryHarness10H().use{h->
   h.scene.setContent{App()};h.await("Home"){h.text().contains("practice questions")};h.click("Start a practice test  >")
   val field=h.nodes().first{it.config.getOrNull(SemanticsActions.SetText)?.action!=null};field.config[SemanticsActions.SetText].action!!.invoke(AnnotatedString("1"));h.render()
   if(mode==Feedback.AT_END)h.click("At the end of the test")
   h.click("Start test  >");h.await("Quiz"){h.text().contains("Question 1 of 1")}
   val prompt=h.text();val radio=h.nodes().first{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton}
   assertTrue(radio.config[SemanticsActions.OnClick].action!!.invoke());h.render();assertFalse(h.text().contains("Correct answer"))
   h.click("Learning library");h.await("Guard"){h.text().contains("Leave this test?")}
   // Latest semantics owner is the platform dialog, not the background tree.
   assertFalse(h.nodes().any{it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton})
   h.capture("10H2","${mode.name.lowercase()}-guard")
   h.click("Keep practising");h.await("Selected draft"){h.nodes().count{it.config.getOrNull(SemanticsProperties.Selected)==true && it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton}==1}
   assertEquals(prompt,h.text());assertFalse(h.text().contains("Correct answer"))
   h.click("Learning library");h.click("Leave test");h.await("Library"){h.text().contains("Search lessons")}
   h.click("Practice");h.await("Setup"){h.text().contains("Make every question count.")};assertEquals("1",h.nodes().first{it.config.getOrNull(SemanticsProperties.EditableText)!=null}.config[SemanticsProperties.EditableText].text)
   h.click("Start test  >");h.await("Fresh quiz"){h.text().contains("Question 1 of 1")};assertFalse(h.nodes().any{it.config.getOrNull(SemanticsProperties.Selected)==true&&it.config.getOrNull(SemanticsProperties.Role)==Role.RadioButton})
   rows.add(mapOf("mode" to mode,"cancel_preserves_prompt_and_selected_draft" to true,"discard_library_then_deliberate_new_attempt" to true,"latest_modal_owner_excludes_background_radios" to true,"native_pointer_focus_and_browser_background" to "pending10K"))
  }
  Proof10H.write("10H2","shared-production-guard-results.json",mapOf("identity" to acceptedIdentity9J,"cases" to rows,"status" to "pass_shared_scope"))
 }
}
