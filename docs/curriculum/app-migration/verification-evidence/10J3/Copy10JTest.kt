@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort
import androidx.compose.runtime.key
import androidx.compose.ui.semantics.*
import kotlin.test.*
class Copy10JTest {
 @Test fun completeReaderVisibleAndAccessibleCopy() {
  val rows=mutableListOf<Any>()
  LibraryHarness10J(1280,4096).use{h->
   for(doc in readerDocuments){
    h.scene.setContent{key(doc.id){LearningTheme{LessonReader(ContentTarget(doc.id),{},{_,_->},{})}}}
    h.await("Reader ${doc.id}"){h.nodes().any{it.config.getOrNull(SemanticsActions.ScrollToIndex)?.action!=null}}
    rows.add(mapOf("surface" to "reader-opening","subject" to doc.id,"text" to h.text()))
    for((i,b) in doc.bodyBlocks.withIndex()){
     assertTrue(h.nodes().first{it.config.getOrNull(SemanticsActions.ScrollToIndex)?.action!=null}.config[SemanticsActions.ScrollToIndex].action!!.invoke(i+1));repeat(6){h.render()}
     val expected=teachingSegments10J(b.payload)
     rows.add(mapOf("surface" to "reader-block","subject" to b.metadata.id,"document" to doc.id,"text" to h.text(),"missing_segments" to expected.filter{!h.text().contains(it)}))
     if(b.payload is BlockPayload.KnowledgeCheck){
      assertFalse(h.nodes().any{it.config.getOrNull(SemanticsProperties.PaneTitle)=="Answer"});h.click("Show answer")
      val answer=doc.answerBlocks.single{it.metadata.id==b.payload.answerId}
      rows.add(mapOf("surface" to "revealed-answer","subject" to answer.metadata.id,"document" to doc.id,"text" to h.text(),"missing_segments" to answer.blocks.flatMap{teachingSegments10J(it.payload)}.filter{!h.text().contains(it)}));h.click("Hide answer")
     }
    }
    val end=doc.bodyBlocks.size+lessonSources(doc).size+2
    h.nodes().first{it.config.getOrNull(SemanticsActions.ScrollToIndex)?.action!=null}.config[SemanticsActions.ScrollToIndex].action!!.invoke(end);h.render()
    rows.add(mapOf("surface" to "reader-navigation","subject" to doc.id,"text" to h.text()))
    Proof10J.write("10J3","reader-copy-observations.json",mapOf("identity" to acceptedIdentity9J,"scope" to "fresh full reader blocks/answers/shared semantics at1280/defaultlight/font1; not native accessibility","cases" to rows))
   }
  }
  assertTrue(rows.all{(it as Map<*,*>)["missing_segments"]?.let{x->(x as List<*>).isEmpty()}!=false})
 }
 @Test fun everySourceReferenceRetainsPublisherClassificationAndDates() {
  val rows=mutableListOf<Any>()
  LibraryHarness10J(1280,2000).use{h->
   for(s in navigationSources.references){
    h.scene.setContent{key(s.id){LearningTheme{SourceDetail(s.id,{},{},{false})}}};h.render()
    val expected=listOf(s.title,s.publisher,s.classificationNote,s.classifications.joinToString(" · "){it.name.lowercase().replace('_',' ')})+s.evidence.flatMap{e->listOf("Checked: ${e.dates.checkedOn ?: "Not recorded"}","Retrieved: ${e.dates.retrievedOn ?: "Not recorded"}","Published: ${e.dates.publishedOn ?: "Not recorded"}",e.scope,e.finding)+e.limitations}
    rows.add(mapOf("subject" to s.id,"text" to h.text(),"missing_segments" to expected.filter{!h.text().contains(it)}))
   }
  }
  Proof10J.write("10J3","source-copy-observations.json",mapOf("identity" to acceptedIdentity9J,"records" to navigationSources.references,"cases" to rows,"scope" to "fresh SourceDetail semantics all519 references including offscreen composed scroll content; no external request or fresh currency claim"))
  assertTrue(rows.all{((it as Map<*,*>)["missing_segments"] as List<*>).isEmpty()})
 }
 @Test fun everySignRetainsNoticeAndArtworkCredit() {
  val rows=mutableListOf<Any>()
  LibraryHarness10J(1000,2200).use{h->
   for(s in navigationSigns){
    val a=readerAssets.single{it.id==s.assetId}
    h.scene.setContent{key(s.id){LearningTheme{SignReferenceDetail(s,a,navigationSources.references,{},{false})}}};h.render();h.click("Sources and artwork credits")
    val expected=listOf(s.code,s.englishLabel,s.officialNameSv,s.caption.assessmentText())+s.limitations+a.reuse.flatMap{listOf(it.credit,it.conditions)}+if(s.translationStatus==TranslationStatus.EDITORIAL_ENGLISH)listOf("Editorial English translation; not an official agency translation.") else emptyList()
    rows.add(mapOf("subject" to s.id,"text" to h.text(),"missing_segments" to expected.filter{!h.text().contains(it)}))
   }
  }
  Proof10J.write("10J3","sign-copy-observations.json",mapOf("identity" to acceptedIdentity9J,"cases" to rows,"scope" to "fresh400 sign-detail+expandedcredits semantics; not400 pixel reviews"))
  assertTrue(rows.all{((it as Map<*,*>)["missing_segments"] as List<*>).isEmpty()})
 }
 @Test fun everyAcceptedQuestionReviewCopy() {
  val rows=mutableListOf<Any>()
  LibraryHarness10J(1280,2500).use{h->
   for(q in acceptedPracticeBank9J.questions){
    val snap=SessionQuestionSnapshot(q,acceptedIdentity9J,q.options.map{it.id})
    val session=AssessmentSession(listOf(snap),Feedback.IMMEDIATE).answer(q.options.first().id)
    h.scene.setContent{key(q.key){LearningTheme{LearningAnswerReview(session,onRelated={},onSource={})}}};h.render()
    val expected=listOf(q.prompt.assessmentText())+session.presentation().choices.flatMap{listOfNotNull(it.text,it.feedback)}+listOfNotNull(session.presentation().explanation)+listOf(readerDocuments.single{it.id==q.relationship.primaryLessonId}.title)
    rows.add(mapOf("subject" to q.key,"text" to h.text(),"missing_segments" to expected.filter{!h.text().contains(it)}))
   }
  }
  Proof10J.write("10J3","question-copy-observations.json",mapOf("identity" to acceptedIdentity9J,"cases" to rows,"scope" to "fresh1000 accepted LearningAnswerReview components; shared composed scroll semantics; no score/content alteration"))
  assertTrue(rows.all{((it as Map<*,*>)["missing_segments"] as List<*>).isEmpty()})
 }
}
