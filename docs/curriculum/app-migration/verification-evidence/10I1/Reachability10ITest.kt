@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort
import androidx.compose.runtime.key
import androidx.compose.ui.semantics.*
import kotlin.test.*
class Reachability10ITest {
 @Test fun everyLibraryUnitModuleAndReferenceGroupHasAnActualRoute() {
  val rows=mutableListOf<Any>()
  Proof10I.write("10I1","compiled-teaching.json",mapOf("identity" to acceptedIdentity9J,"modules" to readerModules,"documents" to readerDocuments,"reference_groups" to navigationReferenceGroups,"reading_order" to readerOrder,"lesson_category_tags" to readerTags))
  LibraryHarness10I(1280,4096).use{h->
   val state=LearningLibraryState().apply{expanded=readerModules.map{it.id}.toSet()}
   val units=readerModules.sortedBy{it.order}.flatMap{it.lessonIds+it.reviewId}.map{id->readerDocuments.single{it.id==id}}+readerDocuments.filter{it.kind==DocumentKind.APPENDIX||it.kind==DocumentKind.FRONT_MATTER}.sortedBy{it.order}
   // Several supporting anchors intentionally share a title: verify each typed callback,
   // then choose the same stable occurrence in the real route instead of the first label.
   var received:ContentTarget?=null
   h.scene.setContent{key("typed-library-keys"){LearningTheme{LearningLibrary({received=it},{},{},state)}}}
   h.await("Typed library"){h.text().contains("Search lessons")}
   val typed=mutableMapOf<ContentId,ContentTarget>()
   for((index,doc) in units.withIndex()){
    val occurrence=units.take(index).count{it.title==doc.title}
    val candidates=h.nodes().filter{it.config.getOrNull(SemanticsProperties.Text).orEmpty().any{t->t.text==doc.title}&&it.config.getOrNull(SemanticsActions.OnClick)?.action!=null}
    assertTrue(candidates[occurrence].config[SemanticsActions.OnClick].action!!.invoke());assertEquals(ContentTarget(doc.id),received);typed[doc.id]=received!!
   }
   for((index,doc) in units.withIndex()){
    h.scene.setContent{key("unit-${doc.id.value}"){LearningRoute(libraryState=state){false}}}
    h.await("Library missing"){h.text().contains("Search lessons")}
    val occurrence=units.take(index).count{it.title==doc.title}
    val button=h.nodes().filter{it.config.getOrNull(SemanticsProperties.Text).orEmpty().any{t->t.text==doc.title}&&it.config.getOrNull(SemanticsActions.OnClick)?.action!=null}[occurrence]
    assertTrue(button.config[SemanticsActions.OnClick].action!!.invoke());h.render()
    h.await("Document ${doc.id} missing"){h.nodes().any{it.config.contains(SemanticsProperties.Heading)&&it.config.getOrNull(SemanticsProperties.Text).orEmpty().any{t->t.text==doc.title}}}
    rows.add(mapOf("id" to doc.id,"kind" to doc.kind,"title" to doc.title,"entry" to "library button","same_title_occurrence" to occurrence,"typed_callback_target" to typed.getValue(doc.id),"status" to "pass_shared_semantics"))
    if(doc.id.value in listOf("M01-L01","M07-L04","M10-L03","appendix-A"))h.capture("10I1","library-${doc.id.value}")
   }
   for(module in readerModules.sortedBy{it.order}){
    val first=readerDocuments.single{it.id==module.lessonIds.first()}
    h.scene.setContent{key("module-${module.id.value}"){LearningRoute(canonicalResolver.canonical(ContentTarget(first.id))){false}}}
    h.await("Reader missing"){h.nodes().any{it.config.getOrNull(SemanticsActions.ScrollToIndex)?.action!=null}}
    val scroll=h.nodes().first{it.config.getOrNull(SemanticsActions.ScrollToIndex)?.action!=null}
    assertTrue(scroll.config[SemanticsActions.ScrollToIndex].action!!.invoke(first.bodyBlocks.size+lessonSources(first).size+2));h.render()
    h.click("Previous: ${module.title}")
    h.await("Module introduction missing"){h.nodes().any{it.config.contains(SemanticsProperties.Heading)&&it.config.getOrNull(SemanticsProperties.Text).orEmpty().any{t->t.text==module.title}}}
    rows.add(mapOf("id" to module.id,"kind" to "module","title" to module.title,"entry" to "first lesson Previous edge","status" to "pass_shared_semantics"))
   }
   for(group in navigationReferenceGroups.sortedBy{it.order}){
    h.scene.setContent{key("reference-${group.id.value}"){LearningRoute{false}}}
    h.click("Road signs and reference");h.click(group.title)
    val required=listOf(group.title)+group.entryIds.map{id->navigationSigns.single{it.id==id}.englishLabel}+group.bodyBlocks.flatMap{teachingSegments10I(it.payload)}
    val missing=required.filter{!h.text().contains(it)}
    rows.add(mapOf("id" to group.id,"kind" to "reference_group","order" to group.order,"title" to group.title,"entry" to "library reference directory","missing" to missing,"status" to if(missing.isEmpty())"pass_shared_semantics" else "fail"))
   }
  }
  Proof10I.write("10I1","shared-route-observations.json",mapOf("identity" to acceptedIdentity9J,"routes" to rows,"scope" to "actual LearningRoute buttons/neighbours invoked through shared semantics1280x4096; not OS pointer/platform delivery"))
  assertEquals(115,rows.size);assertTrue(rows.all{(it as Map<*,*>)["status"]=="pass_shared_semantics"})
 }
}
