package se.korkort
import kotlin.test.*
import kotlin.random.Random

class Snapshot10FTest {
 @Test fun exactOldRoundedOptionsScoreAndFeedbackStayPinned() {
  val oldIdentity=ContentPackageIdentity("conditional-pre-fuel-correction-snapshot",Sha256("a".repeat(64)))
  val rows=mutableListOf<Any>()
  for(old in oldFuel10F())for(mode in Feedback.entries){
   val snapshot=old.snapshot(oldIdentity,Random(17));var session=AssessmentSession(listOf(snapshot),mode)
   session=session.answer(old.feedback.correctOptionId).next();assertEquals(1,session.score)
   val current=acceptedQuestions9J.single{it.key.questionId==old.key.questionId};assertNotEquals(old.key.revision,current.key.revision)
   assertNotEquals(old.options.map{it.text},current.options.map{it.text})
   val before=Proof10F.hash(session);val view=session.presentation(0)
   assertEquals(old.options.map{it.text.assessmentText()}.toSet(),view.choices.map{it.text}.toSet());assertEquals(old.feedback.explanation.assessmentText(),view.explanation)
   // Stronger conditional newer-key case: no active package replacement API is called.
   val newer=current.copy(feedback=current.feedback.copy(correctOptionId=current.options.first{it.id!=current.feedback.correctOptionId}.id))
   assertNotEquals(newer.feedback.correctOptionId,session.answers.single().selectedOptionId)
   assertEquals(1,session.score);assertEquals(before,Proof10F.hash(session));assertEquals(oldIdentity,session.current.packageIdentity)
   rows.add(mapOf("id" to old.key.questionId.value,"old_revision" to old.key.revision.value,"current_revision" to current.key.revision.value,"mode" to mode,"old_order" to snapshot.displayedOptionIds,"selected" to session.answers.single().selectedOptionId,"old_option_text" to view.choices.map{it.text},"current_option_text" to current.options.map{it.text.assessmentText()},"score_before" to 1,"score_after_newer_teaching_and_conditional_key" to session.score,"snapshot_sha256_before_and_after" to before,"status" to "pass"))
  }
  Proof10F.write("10F3","historical-snapshot-observations.json",mapOf("status" to "pass","scope" to "Conditional model reconstruction, no durable history/import/hot replacement feature or legacy release activation.","cases" to rows))
 }
 @Test fun requiredInvalidInputsAreObservedWithoutBypassingProductionStart() {
  val bank=acceptedPracticeBank9J;val q=bank.questions.first();val snap=q.snapshot(bank.identity,Random(5));val s=AssessmentSession(listOf(snap),Feedback.AT_END);val cases=mutableListOf<Map<String,Any?>>()
  fun rejects(name:String,scope:String="existing_session_guard",f:()->Unit){
   val error=runCatching{f()}.exceptionOrNull();val rejected=error is IllegalArgumentException
   cases.add(mapOf("case" to name,"scope" to scope,"expected" to "rejected","observed" to if(rejected)"rejected" else if(error==null)"accepted" else "unexpected_exception","error" to error?.toString(),"status" to if(rejected)"pass" else "fail"))
  }
  rejects("foreign_option"){s.answer(OptionId("foreign"))}
  rejects("stale_answer_revision"){s.copy(answers=listOf(SnapshotAnswer(q.key.copy(revision=SemanticRevision("wrong")),snap.displayedOptionIds.first())))}
  rejects("missing_displayed_identity"){snap.copy(displayedOptionIds=snap.displayedOptionIds.dropLast(1))}
  rejects("foreign_displayed_identity"){snap.copy(displayedOptionIds=listOf(OptionId("foreign"))+snap.displayedOptionIds.drop(1))}
  rejects("mixed_session_package_identities"){AssessmentSession(listOf(snap,bank.questions[1].snapshot(bank.identity.copy(contentVersion="mismatch"))),Feedback.AT_END)}
  rejects("held_snapshot"){AssessmentSession(listOf(snap.copy(question=q.copy(acceptance=q.acceptance.copy(eligibility=ScoringEligibility.HELD)))),Feedback.IMMEDIATE)}
  rejects("retired_snapshot"){AssessmentSession(listOf(snap.copy(question=q.copy(acceptance=q.acceptance.copy(eligibility=ScoringEligibility.RETIRED)))),Feedback.IMMEDIATE)}
  rejects("historical_candidate_release","current_production_start"){TransientQuizState(countText="1").showSetup().startPractice(candidatePracticeBank9M,Random(1))}
  rejects("not_release_accepted","current_production_start"){TransientQuizState(countText="1").showSetup().startPractice(bank.copy(releaseAccepted=false),Random(1))}
  rejects("duplicate_bank_ids","current_production_start"){TransientQuizState(countText="1").showSetup().startPractice(bank.copy(questions=bank.questions+q),Random(1))}
  for((name,identity) in listOf("missing_content_version" to bank.identity.copy(contentVersion=""),"wrong_content_version" to bank.identity.copy(contentVersion="unrelated-package"),"wrong_manifest_digest" to bank.identity.copy(manifestSha256=Sha256("0".repeat(64))))){
   rejects(name,"conditional_invalid_injected_bank_model_contract; fixed App() does not expose package injection"){TransientQuizState(countText="1").showSetup().startPractice(bank.copy(identity=identity),Random(1))}
  }
  val status=if(cases.all{it["status"]=="pass"})"pass" else "fail_required_identity_rejection"
  Proof10F.write("10F3","invalid-input-observations.json",mapOf("status" to status,"cases" to cases,"limits" to "Missing/wrong bank identity is an explicitly injected conditional model input. App() is statically wired to acceptedPracticeBank9J; no user-facing package switch or hostile import is claimed."))
  assertTrue(cases.all{it["status"]=="pass"},"See invalid-input-observations.json for exact required rejection failures")
 }
}
