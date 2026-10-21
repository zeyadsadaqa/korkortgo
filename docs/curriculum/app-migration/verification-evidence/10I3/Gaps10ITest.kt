@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.AnnotatedString
import kotlin.test.*
class Gaps10ITest {
 @Test fun acceptedCoverageGapsDoNotPreventActualAppTeachingAccess() {
  val questions=acceptedQuestions9J.map{q->mapOf("key" to q.key,"concept_id" to q.conceptId,"eligibility" to q.acceptance.eligibility,"relationship" to q.relationship)}
  val gapIds=listOf("M01-L01","M07-L04","M10-L03");val rows=mutableListOf<Any>()
  assertEquals(1000,questions.size);assertEquals(500,acceptedQuestions9J.map{it.conceptId}.distinct().size);assertTrue(acceptedQuestions9J.all{it.acceptance.eligibility==ScoringEligibility.ACCEPTED})
  LibraryHarness10I().use{h->
   h.scene.setContent{App()};h.await("Acceptedhome"){h.text().contains("practice questions")};assertTrue("1000" in h.texts());h.click("Learning library")
   for(id in gapIds){
    val doc=readerDocuments.single{it.id.value==id}
    val field=h.nodes().first{it.config.getOrNull(SemanticsActions.SetText)?.action!=null};assertTrue(field.config[SemanticsActions.SetText].action!!.invoke(AnnotatedString(doc.title)));h.render();h.click(doc.title)
    h.await("Gap teaching missing"){h.nodes().any{it.config.contains(SemanticsProperties.Heading)&&it.config.getOrNull(SemanticsProperties.Text).orEmpty().any{t->t.text==doc.title}}}
    val i=doc.bodyBlocks.indexOfFirst{it.payload is BlockPayload.KnowledgeCheck};assertTrue(i>=0)
    val scroll=h.nodes().first{it.config.getOrNull(SemanticsActions.ScrollToIndex)?.action!=null};assertTrue(scroll.config[SemanticsActions.ScrollToIndex].action!!.invoke(i+1));h.render()
    assertFalse(h.nodes().any{it.config.getOrNull(SemanticsProperties.PaneTitle)=="Answer"});h.click("Show answer");assertTrue(h.nodes().any{it.config.getOrNull(SemanticsProperties.PaneTitle)=="Answer"})
    assertFalse(h.text().contains("Question 1 of"));assertFalse(h.text().contains("Your results"));h.capture("10I3","$id-unscored-teaching-answer");h.click("Hide answer")
    val primary=acceptedQuestions9J.filter{it.relationship.primaryLessonId==doc.id}.map{it.key.questionId}
    val related=acceptedQuestions9J.filter{doc.id in it.relationship.relatedLessonIds}.map{it.key.questionId}
    assertTrue(primary.isEmpty());assertEquals(if(id=="M07-L04")1 else 0,related.size)
    rows.add(mapOf("id" to id,"title" to doc.title,"primary_question_ids" to primary,"related_question_ids" to related,"body_blocks" to doc.bodyBlocks.size,"existing_unscored_check_revealed_deliberately" to true,"scored_test_auto_started" to false,"status" to "pass_shared_scope"))
    h.click("Learning library");h.await("Libraryreturn"){h.text().contains("Search lessons")}
   }
  }
  Proof10I.write("10I3","compiled-gap-observations.json",mapOf("identity" to acceptedIdentity9J,"release_accepted" to acceptedPracticeBank9J.releaseAccepted,"accepted_questions" to 1000,"held_questions" to 0,"concepts" to 500,"questions" to questions,"gaps" to rows,"scope" to "Actual App() accepted-bank home/library/reader with unscored teaching reveal; no new authoring, score, persistence or completion feature"))
 }
}
