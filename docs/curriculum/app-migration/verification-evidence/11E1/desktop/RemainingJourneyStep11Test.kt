@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort
import androidx.compose.runtime.*
import androidx.compose.ui.platform.*
import androidx.compose.ui.unit.Density
import androidx.compose.ui.input.key.*
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.AnnotatedString
import kotlin.test.*

class RemainingJourneyStep11Test {
 private fun JourneyHarness11.key(k:Key,shift:Boolean=false){scene.sendKeyEvent(KeyEvent(k,KeyEventType.KeyDown,isShiftPressed=shift));scene.sendKeyEvent(KeyEvent(k,KeyEventType.KeyUp,isShiftPressed=shift));render()}
 private fun JourneyHarness11.start(scale:Float){scene.setContent{CompositionLocalProvider(LocalDensity provides Density(1f,scale)){App()}};await("Normal home"){text().contains("KörkortGo")}}
 @Test fun normalReferenceKeyboardAndFreshOwnerDefaults(){
  val rows=mutableListOf<Any>()
  for(dark in listOf(false,true))for(scale in listOf(1f,1.6f)){
   val setting="${if(dark)"dark" else "light"}-${if(scale==1f)"100" else "160"}"
   JourneyHarness11().use{h->
    h.start(scale);h.click("Learning library");h.click("Road signs and reference")
    val sign=navigationSigns.single{it.code=="B1"};val group=navigationReferenceGroups.first{sign.id in it.entryIds}
    h.click(group.title);h.click(sign.englishLabel);h.click("Enlarge image")
    h.await("Reference image loaded"){h.nodes().any{it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text=="Zoom in"}==true && it.config.getOrNull(SemanticsProperties.Disabled)==null}}
    assertFalse(h.text().contains("Learning library"));assertFalse(h.text().contains("‹ Road signs and reference"))
    h.key(Key.Tab);h.key(Key.Tab,true);h.key(Key.Equals);h.await("Keyboard zoom150"){h.text().contains("150%")}
    h.capture("11E1","reference-$setting-zoom");h.key(Key.DirectionRight);h.capture("11E1","reference-$setting-pan")
    h.key(Key.Home);assertTrue(h.text().contains("100%"));h.key(Key.Escape)
    h.await("Exact trigger focus"){h.nodes().any{it.config.getOrNull(SemanticsProperties.Focused)==true && it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text=="Enlarge image"}==true}}
    h.key(Key.Enter);h.await("Keyboard reopens same reference"){h.text().contains("150%").not() && h.text().contains("100%")};h.key(Key.Escape)
    h.click("‹ Road signs and reference");assertTrue(h.text().contains("Road signs and signals"))
    rows.add(mapOf("case_id" to "FLOW-desktop-reference-viewer-$setting","status" to "pass","reference" to "B1","normal_App" to true))
    rows.add(mapOf("case_id" to "FLOW-desktop-keyboard-accessibility-$setting","status" to "pass_shared_scope","neutral_assessment_supplement" to "11D1/result.json","tab_reverse_zoom_pan_home_escape_trigger_return" to true))
    h.click("Practice");val input=h.nodes().first{it.config.getOrNull(SemanticsActions.SetText)?.action!=null};input.config[SemanticsActions.SetText].action!!.invoke(AnnotatedString("1"));h.render();h.click("At the end of the test")
    h.click("Overview");h.click("Practice");assertTrue(h.nodes().any{it.config.getOrNull(SemanticsProperties.EditableText)?.text=="1"})
    assertTrue(h.nodes().any{it.config.getOrNull(SemanticsProperties.Selected)==true && it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text=="At the end of the test"}==true})
   }
   JourneyHarness11().use{h->h.start(scale);h.click("Practice");assertTrue(h.nodes().any{it.config.getOrNull(SemanticsProperties.EditableText)?.text=="70"});assertTrue(h.nodes().any{it.config.getOrNull(SemanticsProperties.Selected)==true && it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text=="After each question"}==true});assertFalse(h.text().contains("TEST COMPLETE"));h.capture("11E1","restart-$setting-defaults")}
   rows.add(mapOf("case_id" to "FLOW-desktop-restart-$setting","status" to "pass_shared_scope","same_owner_preferences" to true,"fresh_App_owner_defaults" to "70/IMMEDIATE; no result","scope" to "Configured desktop Compose harness; no native launcher claim"))
  }
  Proof10J.write("11E1","desktop-reference-keyboard-restart.json",mapOf("rows" to rows,"rendered_theme" to "approved fixed light production theme"))
 }
}
