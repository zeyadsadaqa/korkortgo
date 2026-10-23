@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort

import androidx.compose.runtime.*
import androidx.compose.ui.platform.*
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.unit.Density
import kotlin.test.*

class LearningJourneyStep11Test {
 @Test fun libraryReaderRevealNeighboursSourcesAndFilters() {
  val rows=mutableListOf<Any>()
  for(dark in listOf(false,true))for(scale in listOf(1f,1.6f))JourneyHarness11().use { h ->
   val opened=mutableListOf<String>();var fail=false
   h.scene.setContent {CompositionLocalProvider(LocalDensity provides Density(1f,scale),LocalUriHandler provides object:UriHandler {
    override fun openUri(uri:String){opened.add(uri);if(fail)error("Controlled dispatch failure")}
   }){App()}}
   h.await("Normal home"){h.text().contains("KörkortGo")};h.click("Learning library")
   val doc=readerDocuments.single{it.id.value=="M01-L01"}
   val input=h.nodes().first{it.config.getOrNull(SemanticsActions.SetText)?.action!=null}
   assertTrue(input.config[SemanticsActions.SetText].action!!.invoke(AnnotatedString(doc.title)));h.render();h.click(doc.title)
   val seen=mutableSetOf<String>()
   repeat(80){seen.addAll(h.texts());h.scroll(400f)}
   fun normalized(text:String)=text.replace(Regex("\\s+")," ").trim()
   val complete=normalized(seen.joinToString(" "))
   for(block in doc.bodyBlocks)if(block.payload is BlockPayload.Paragraph || block.payload is BlockPayload.Heading) {
    assertTrue(complete.contains(normalized(block.searchText())),"Complete authored block ${block.metadata.id} must be available while reading")
   }
   val check=doc.bodyBlocks.first{it.payload is BlockPayload.KnowledgeCheck}.payload as BlockPayload.KnowledgeCheck
   val answer=doc.answerBlocks.single{it.metadata.id==check.answerId}.blocks.first().searchText().removePrefix("Answer:").trim()
   h.reach("Show answer");assertFalse(h.text().contains(answer));h.capture("11E1","reader-hidden-$dark-$scale")
   h.click("Show answer");h.await("Authored answer revealed"){h.text().contains(answer)};h.capture("11E1","reader-revealed-$dark-$scale")
   h.click("Hide answer");assertFalse(h.text().contains(answer))
   val next=readingNeighbours(doc.id).second!!;val title=readerDocuments.single{it.id==next}.title
   h.click("Next: $title");h.await("Exact next lesson"){h.text().contains(title)}
   h.click("Previous: ${doc.title}");h.await("Exact previous lesson"){h.text().contains(doc.title)}
   val source=lessonSources(doc).first()
   h.click(source.title);h.click("Open source");assertEquals(source.url,opened.last())
   fail=true;h.click("Open source");h.await("Controlled source failure"){h.text().contains("The source could not be opened.")}
   h.capture("11E1","source-failure-$dark-$scale");h.click("Return to reading")
   h.await("Source trigger focus restored"){h.nodes().any{it.config.getOrNull(SemanticsProperties.Focused)==true && it.config.getOrNull(SemanticsProperties.Text)?.any{t->t.text==source.title}==true}}
   h.click("Learning library")
   h.await("Query retained"){h.nodes().any{it.config.getOrNull(SemanticsProperties.EditableText)?.text==doc.title}}
   h.click("Environment");assertTrue(h.text().contains("No matching lessons."));h.capture("11E1","library-empty-$dark-$scale")
   h.click("Clear filters");h.await("Filter reset"){h.text().contains(doc.title)}
   h.click("Clear search");h.await("Query cleared"){h.nodes().any{it.config.getOrNull(SemanticsProperties.EditableText)?.text==""}}
   rows.add(mapOf("case_id" to "FLOW-desktop-library-reader-${if(dark)"dark" else "light"}-${if(scale==1f)"100" else "160"}","document_id" to doc.id.value,"search_text" to doc.title,"font_scale" to scale,"requested_appearance" to if(dark)"dark" else "light","rendered_theme" to "approved fixed light production theme","full_body_paragraphs_and_headings" to true,"deliberate_reveal" to true,"neighbours" to true,"source_callback_and_controlled_failure_return" to true,"query_filter_and_reset" to true,"status" to "pass"))
  }
  Proof10J.write("11E1","desktop-library-journeys.json",mapOf("status" to "pass_shared_scope","rows" to rows,"scope" to "Normal App() and accepted bank in the configured desktop Compose harness; URI callbacks are not OS launches."))
 }
}
