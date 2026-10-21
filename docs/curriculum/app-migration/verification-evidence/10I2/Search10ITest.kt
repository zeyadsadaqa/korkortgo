@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.AnnotatedString
import kotlin.test.*
class Search10ITest {
 @Test fun independentExpectedSetsMatchModelsAndActualLibrarySemantics() {
  val rows=mutableListOf<Any>();val state=LearningLibraryState().apply{expanded=readerModules.map{it.id}.toSet()};val opened=mutableListOf<ContentTarget>()
  val ordered=readerModules.sortedBy{it.order}.flatMap{it.lessonIds}.map{id->readerDocuments.single{it.id==id}}
  val titles=ordered.associate{it.title to it.id.value}
  LibraryHarness10I().use{h->
   h.scene.setContent{LearningTheme{LearningLibrary({opened.add(it)},{},{},state)}}
   for(line in java.nio.file.Files.readAllLines(Proof10I.root.resolve("docs/curriculum/app-migration/verification-evidence/10I2/search-inputs.tsv"))){
    val fields=line.split('\t');val category=Category.entries.singleOrNull{it.name==fields[1]};val query=fields[2];val expected=fields[3].split(',').filter{it.isNotBlank()}
    val filter=LibraryFilter(query,category);val model=ordered.filter{filter.matches(it,readerTags)}.map{it.id.value}
    state.filter=filter;h.render();val ui=h.texts().filter{it in titles}.map{titles.getValue(it)}.distinct()
    val empty=h.text().contains("No matching lessons.");val ok=model==expected&&ui==expected&&(expected.isEmpty()==empty)&&opened.isEmpty()
    rows.add(mapOf("id" to fields[0],"query" to query,"category" to fields[1],"expected" to expected,"model" to model,"ui" to ui,"empty_message" to empty,"status" to if(ok)"pass" else "fail"))
    if(query==""&&category!=null)h.capture("10I2","category-${category.name.lowercase()}")
    if(query=="zzzxq10I"&&category==Category.SAFETY)h.capture("10I2","empty-safety")
   }
   state.filter=LibraryFilter("zzzxq10I",Category.SAFETY);h.render();h.click("Clear search");assertEquals(LibraryFilter("",Category.SAFETY),state.filter)
   state.filter=LibraryFilter("green",Category.SAFETY);h.render();h.click("Clear filters");assertEquals(LibraryFilter("green",null),state.filter)
   val field=h.nodes().first{it.config.getOrNull(SemanticsActions.SetText)?.action!=null};assertTrue(field.config[SemanticsActions.SetText].action!!.invoke(AnnotatedString("zzzxq10I")));h.render();assertEquals("zzzxq10I",state.filter.query)
   for(category in Category.entries){h.click(category.title);assertEquals(category,state.filter.category);assertEquals("zzzxq10I",state.filter.query)}
   h.click("All topics");assertNull(state.filter.category);assertEquals("zzzxq10I",state.filter.query);h.click("Clear search");assertEquals(LibraryFilter(),state.filter)
   assertTrue(opened.isEmpty())
  }
  Proof10I.write("10I2","compiled-search-observations.json",mapOf("identity" to acceptedIdentity9J,"tags" to readerTags,"category_titles" to Category.entries.associate{it.name to it.title},"cases" to rows,"clear_actions_preserve_other_input" to true,"chips_preserve_query" to true,"empty_never_opens_content" to opened.isEmpty(),"scope" to "288 independent expected cases against actual LibraryFilter and actual LearningLibrary shared semantics1000x1800; no native pointer claim"))
  assertTrue(rows.all{(it as Map<*,*>)["status"]=="pass"})
 }
 @Test fun actualRouteRoundTripPreservesCombinedSearchAndExpansion() {
  val state=LearningLibraryState().apply{filter=LibraryFilter("Your route into driving",Category.PERSONAL);expanded=setOf(ContentId("M01"),ContentId("M07"))}
  LibraryHarness10I().use{h->
   h.scene.setContent{LearningRoute(libraryState=state){false}}
   h.click("Your route into driving");h.await("Reader"){h.text().contains("Your route into driving")&&!h.text().contains("Search lessons")};h.click("Learning library")
   assertEquals(LibraryFilter("Your route into driving",Category.PERSONAL),state.filter);assertEquals(setOf(ContentId("M01"),ContentId("M07")),state.expanded)
   val field=h.nodes().first{it.config.getOrNull(SemanticsProperties.EditableText)!=null};assertEquals("Your route into driving",field.config[SemanticsProperties.EditableText].text)
   h.capture("10I2","returned-combined-search")
   Proof10I.write("10I2","search-return-observations.json",mapOf("status" to "pass","filter" to state.filter,"expanded" to state.expanded,"field_semantics" to field.config[SemanticsProperties.EditableText].text,"scope" to "actual shared LearningRoute, semantic navigation; no native scroll/keyboard claim"))
  }
 }
}
