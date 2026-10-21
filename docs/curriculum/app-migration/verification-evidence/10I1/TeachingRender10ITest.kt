@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort
import androidx.compose.runtime.key
import androidx.compose.ui.semantics.*
import kotlin.test.*
class TeachingRender10ITest {
 @Test fun completeBodiesAndDeliberateAnswerRevealsRemainAvailable() {
  val rows=mutableListOf<Any>();val documents=mutableListOf<Any>()
  LibraryHarness10I(1280,4096).use{h->
   for(doc in readerDocuments){
    h.scene.setContent{key(doc.id){LearningTheme{LessonReader(ContentTarget(doc.id),{},{_,_->},{})}}}
    h.await("Reader ${doc.id}"){h.nodes().any{it.config.getOrNull(SemanticsActions.ScrollToIndex)?.action!=null}}
    for((i,b) in doc.bodyBlocks.withIndex()){
     val scroll=h.nodes().first{it.config.getOrNull(SemanticsActions.ScrollToIndex)?.action!=null}
     assertTrue(scroll.config[SemanticsActions.ScrollToIndex].action!!.invoke(i+1));repeat(6){h.render()}
     val expected=teachingSegments10I(b.payload);val missing=expected.filter{!h.text().contains(it)}
     var answerMissing=emptyList<String>();var premature=false;var collapsed:Boolean?=null
     if(b.payload is BlockPayload.KnowledgeCheck){
      premature=h.nodes().any{it.config.getOrNull(SemanticsProperties.PaneTitle)=="Answer"}
      h.click("Show answer")
      val answer=doc.answerBlocks.single{it.metadata.id==b.payload.answerId}
      answerMissing=answer.blocks.flatMap{teachingSegments10I(it.payload)}.filter{!h.text().contains(it)}
      h.click("Hide answer");collapsed=h.nodes().none{it.config.getOrNull(SemanticsProperties.PaneTitle)=="Answer"}
     }
     rows.add(mapOf("document_id" to doc.id,"block_id" to b.metadata.id,"kind" to b.payload.javaClass.simpleName,"expected_segments" to expected.size,"missing_segments" to missing,"missing_answer_segments" to answerMissing,"premature_answer_pane" to premature,"answer_collapsed" to collapsed,"status" to if(missing.isEmpty()&&answerMissing.isEmpty()&&!premature&&collapsed!=false)"pass" else "fail"))
    }
    documents.add(mapOf("id" to doc.id,"blocks" to doc.bodyBlocks.size,"answer_blocks" to doc.answerBlocks.size))
    Proof10I.write("10I1","shared-reader-observations.json",mapOf("identity" to acceptedIdentity9J,"documents" to documents,"blocks" to rows,"scope" to "fresh actual LessonReader1280x4096/default light/font1; full text semantics, not exhaustive pixel/native readability"))
   }
  }
  assertTrue(rows.all{(it as Map<*,*>)["status"]=="pass"},"See complete per-block evidence; no production edits are authorised by this audit")
 }
}
