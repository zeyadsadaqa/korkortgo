package se.korkort
import kotlin.test.*
import kotlin.random.Random
import java.nio.file.Files

class Scoring10FTest {
 private val keys=Files.readAllLines(Proof10F.root.resolve("docs/curriculum/app-migration/verification-evidence/10F2/authored-key-oracle.tsv")).associate{it.split('\t').let{v->v[0] to v[2]}}
 private fun right(q:AssessmentQuestion)=OptionId(keys.getValue(q.key.questionId.value))
 private fun hidden(p:AssessmentPresentation){assertNull(p.explanation);assertNull(p.targetCode);assertNull(p.targetLabel);assertTrue(p.choices.all{it.correct==null && it.feedback==null})}
 private fun revealed(s:AssessmentSession,i:Int){
  val snap=s.snapshots[i];val p=s.presentation(i);assertEquals(snap.displayedOptionIds,p.choices.map{it.id})
  assertEquals(snap.question.feedback.explanation.assessmentText(),p.explanation)
  p.choices.forEachIndexed{position,c->val authored=snap.question.options.single{it.id==c.id};assertEquals(authored.text.assessmentText(),c.text);assertEquals(c.id==right(snap.question),c.correct);assertEquals(snap.question.feedback.optionFeedback.single{it.optionId==c.id}.let{listOfNotNull(it.signCode,it.englishLabel,it.explanation.assessmentText()).joinToString(" · ")},c.feedback);assertEquals(('A'+position).toString(),c.letter)}
 }
 @Test fun everyAcceptedQuestionAtEveryKeyPositionInBothModes() {
  val rows=mutableListOf<Any>()
  for(q in acceptedQuestions9J)for(rotation in 0..3)for(mode in Feedback.entries){
   assertEquals(right(q),q.feedback.correctOptionId)
   val ids=q.options.map{it.id}.let{it.drop(rotation)+it.take(rotation)};val snap=SessionQuestionSnapshot(q,acceptedIdentity9J,ids)
   var s=AssessmentSession(listOf(snap),mode);hidden(s.presentation());assertNull(s.score)
   ids.forEachIndexed{i,id->assertEquals(id,snap.optionAt(i).id)}
   val pick=ids[(rotation+1)%4];s=s.answer(pick)
   if(mode==Feedback.IMMEDIATE)revealed(s,0) else hidden(s.presentation())
   assertFailsWith<IllegalArgumentException>{s.answer(ids.first())};assertNull(s.score)
   s=s.next();assertEquals(if(pick==right(q))1 else 0,s.score);revealed(s,0)
   rows.add(mapOf("id" to q.key.questionId.value,"revision" to q.key.revision.value,"rotation" to rotation,"mode" to mode,"key_position" to ids.indexOf(right(q)),"selected" to pick,"score" to s.score,"image_kind" to if(q.options.any{it.image!=null})"image_choices" else if(q.image!=null)"stem_image" else "text","status" to "pass"))
  }
  Proof10F.write("10F2","all-question-key-position-observations.json",mapOf("status" to "pass","observations" to rows))
 }
 @Test fun allLengthsTwentySeedsBothModesAndReviewFilters() {
  val rows=mutableListOf<Any>();var answeredCount=0;var reviewedCount=0
  for(n in 1..70)for(seed in 0..19)for(mode in Feedback.entries){
   val snapshots=AssessmentEngine.select(acceptedQuestions9J,n,acceptedIdentity9J,Random(seed))
   val original=AssessmentSession(snapshots,mode);val id="10F-$n-$seed-${mode.name}"
   var state=TransientQuizState(pinned=PinnedPractice(id,original),navigation=GuardedNavigation(AppDestination.Quiz(id),SessionNavigation(id,false,false)))
   val picked=mutableListOf<OptionId>();var expected=0
   for(i in 0 until n){
    val q=snapshots[i].question;val token=state.pinned!!.token;val before=state.pinned!!.assessment
    hidden(before.presentation());assertFailsWith<IllegalArgumentException>{before.next()}
    val correct=right(q);val wanted=when(seed%3){0->true;1->false;else->i%2==0}
    val choice=if(wanted)correct else q.options.first{it.id!=correct}.id
    state=state.select(token,choice);assertEquals(before,state.pinned!!.assessment);assertNull(state.pinned!!.assessment.currentAnswer);hidden(state.pinned!!.assessment.presentation())
    state=state.confirm(token);assertEquals(choice,state.pinned!!.assessment.currentAnswer!!.selectedOptionId)
    assertFailsWith<IllegalArgumentException>{state.confirm(token)};assertFailsWith<IllegalArgumentException>{state.select(token,choice)}
    if(mode==Feedback.IMMEDIATE)revealed(state.pinned!!.assessment,i) else hidden(state.pinned!!.assessment.presentation())
    assertNull(state.pinned!!.assessment.score);picked.add(choice);if(choice==correct)expected++
    state=state.nextQuestion();answeredCount++
   }
   val finished=state.pinned!!.assessment;assertTrue(finished.finished);assertEquals(expected,finished.score);assertEquals(0,original.answers.size);assertNull(original.score)
   assertEquals(AppDestination.Results(id),state.navigation.current)
   val signature=Proof10F.hash(listOf(finished.snapshots,finished.answers))
   val byFilter=mutableMapOf<String,List<Int>>()
   state=state.openReview()
   for(filter in PracticeReviewFilter.entries){
    val positions=(0 until n).filter{filter==PracticeReviewFilter.ALL || (picked[it]==right(snapshots[it].question))==(filter==PracticeReviewFilter.CORRECT)}
    state=state.filterReview(filter);assertEquals(positions,state.reviewPositions());byFilter[filter.name]=positions
    if(positions.isEmpty()){assertNull(state.reviewSnapshotPosition());assertNull(state.reviewPresentation())}
    for(row in positions.indices){state=state.moveReview(row);assertEquals(positions[row],state.reviewSnapshotPosition());assertEquals(snapshots[positions[row]].question.key,state.reviewPresentation()!!.key);revealed(finished,positions[row]);assertEquals(picked[positions[row]],finished.answers[positions[row]].selectedOptionId);reviewedCount++}
   }
   assertEquals(signature,Proof10F.hash(listOf(state.pinned!!.assessment.snapshots,state.pinned!!.assessment.answers)))
   assertEquals(expected,state.pinned!!.assessment.score)
   rows.add(mapOf("size" to n,"seed" to seed,"mode" to mode,"expected_score" to expected,"actual_score" to finished.score,"filter_positions" to byFilter,"snapshot_and_answer_sha256" to signature,"status" to "pass"))
  }
  Proof10F.write("10F2","shuffle-feedback-scoring-results.json",mapOf("status" to "pass","identity" to acceptedIdentity9J,"sessions" to rows,"answered_transitions" to answeredCount,"reviewed_rows" to reviewedCount,"key_position_report" to "all-question-key-position-observations.json","oracle" to "Authored key IDs loaded independently from accepted JSON; no score/isCorrect helper used to calculate expected scores/filters."))
 }
}
