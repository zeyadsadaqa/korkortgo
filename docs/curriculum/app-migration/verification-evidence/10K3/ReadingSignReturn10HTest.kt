@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.LinkAnnotation
import kotlin.test.*
class ReadingSignReturn10HTest {
 @Test fun readingSignLinkMustOfferReturnToReading() {
  RecoveryHarness10H().use{h->
   val initial=ContentTarget(ContentId("M03-L01"),BlockId("M03-L01/teaching-005"))
   h.scene.setContent{LearningRoute(canonicalResolver.canonical(initial)){false}}
   var clicked=false
   h.await("B1 link missing"){
    val link=h.nodes().flatMap{it.config.getOrNull(SemanticsProperties.Text).orEmpty()}.flatMap{it.getLinkAnnotations(0,it.length)}.map{it.item}.filterIsInstance<LinkAnnotation.Clickable>().firstOrNull{it.tag.contains("sign-B1")}
    if(link!=null && !clicked){clicked=true;link.linkInteractionListener!!.onClick(link)}
    clicked
   }
   h.await("Sign detail missing"){h.text().contains("‹ Road signs and reference")}
   h.capture("10K3","reading-to-sign-B1")
   val hasReturn=h.text().contains("Return to reading")
   h.click("‹ Road signs and reference")
   val catalogueReturn=h.text().contains("Return to reading")
   h.click("Return to reading")
   repeat(30){h.render();Thread.sleep(5)}
   val returned=!h.text().contains("Road signs and signals")
   h.capture("10K3","catalogue-return-stuck")
   Proof10H.write("10K3","reading-sign-return-observations.json",mapOf("origin" to initial,"link" to "sign-B1","shared_link_callback_invoked" to clicked,"sign_return_action" to hasReturn,"catalogue_return_action" to catalogueReturn,"returned_to_origin" to returned,"after_return_text" to h.text(),"expected" to "Reach the validated reading origin and position through the sign catalogue","status" to if(catalogueReturn&&returned)"pass" else "fail"))
   assertTrue(catalogueReturn&&returned,"Sign catalogue must retain a reachable return to the reading origin")
  }
 }
}
