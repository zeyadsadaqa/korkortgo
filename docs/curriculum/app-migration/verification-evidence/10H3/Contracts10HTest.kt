package se.korkort
import kotlin.random.Random
import kotlin.test.*
class Contracts10HTest {
 @Test fun eighteenTransientContractsUseTheActualAcceptedIdentity() {
  val rows=mutableListOf<Any>()
  fun record(n:Int,checks:List<String>,actual:Any?){rows.add(mapOf("id" to "7E-STATE-%02d".format(n),"status" to "pass_accepted_model_scope","checks" to checks,"actual" to actual))}
  val defaults=TransientQuizState();assertEquals("70",defaults.countText);assertEquals(Feedback.IMMEDIATE,defaults.feedback)
  assertEquals(1000,acceptedPracticeBank9J.questions.size);assertTrue(acceptedPracticeBank9J.releaseAccepted);assertEquals(acceptedIdentity9J,acceptedPracticeBank9J.identity)
  val missing=defaults.request(NavigationRequest(AppDestination.Results("absent"))).first
  assertNull(missing.pinned);assertEquals(AppDestination.QuizSetup,missing.navigation.current);assertNotEquals(PracticeRecovery.NONE,missing.recovery)
  record(1,listOf("128 transitions in10H1","absent result explicit setup without invented session"),missing.navigation.current)
  for(n in 1..70)assertTrue(practiceStartCheck(n.toString(),acceptedPracticeBank9J).allowed)
  for(raw in listOf("","0","71","bad","1.5"))assertFalse(practiceStartCheck(raw,acceptedPracticeBank9J).allowed)
  val setup=TransientQuizState(countText="3",feedback=Feedback.AT_END,library=LibraryFilter("yield",Category.RULES)).showSetup()
  assertEquals("3",setup.request(NavigationRequest(AppDestination.Library)).first.showSetup().countText)
  record(2,listOf("valid same-process preference","all1–70 accepted preflight","invalid inputs blocked","fresh70"),mapOf("default" to defaults.countText,"retained" to setup.countText))
  var finished:TransientQuizState?=null
  for(mode in Feedback.entries){
   var s=setup.copy(feedback=mode).startPractice(acceptedPracticeBank9J,Random(20261021))
   val pin=s.pinned!!;assertEquals(acceptedIdentity9J,pin.token.packageIdentity);assertEquals(mode,s.copy(feedback=if(mode==Feedback.IMMEDIATE)Feedback.AT_END else Feedback.IMMEDIATE).pinned!!.assessment.feedbackMode)
   repeat(3){i->
    val p=s.pinned!!;val token=p.token
    val option=if(i==1)token.displayedOptionIds.first{it!=p.assessment.current.question.feedback.correctOptionId}else p.assessment.current.question.feedback.correctOptionId
    assertNull(p.assessment.score);assertEquals(i,p.assessment.index);assertFalse(p.assessment.finished)
    val selected=s.select(token,option);assertNull(selected.pinned!!.assessment.currentAnswer);assertNull(selected.pinned.assessment.presentation().explanation)
    for(stale in listOf(token.copy(sessionId="other"),token.copy(key=token.key.copy(revision=SemanticRevision("r-future"))),token.copy(packageIdentity=acceptedIdentity9J.copy(contentVersion="other")),token.copy(displayedOptionIds=token.displayedOptionIds.reversed())))assertFailsWith<IllegalArgumentException>{s.select(stale,option)}
    val answered=selected.confirm(token);assertEquals(option,answered.pinned!!.assessment.currentAnswer!!.selectedOptionId)
    assertEquals(mode==Feedback.IMMEDIATE,answered.pinned.assessment.presentation().explanation!=null)
    assertFailsWith<IllegalArgumentException>{answered.confirm(token)}
    s=answered.nextQuestion();assertNull(s.draft)
    if(i<2)assertFailsWith<IllegalArgumentException>{s.select(token,option)}
   }
   assertTrue(s.pinned!!.assessment.finished);assertEquals(2,s.pinned!!.assessment.score);assertEquals(pin.assessment.snapshots,s.pinned!!.assessment.snapshots)
   assertEquals(AppDestination.Results(pin.id),s.navigation.current)
   rows.add(mapOf("feedback_run" to mode,"identity" to pin.token.packageIdentity,"snapshot_hash" to Proof10H.hash(pin.assessment.snapshots),"final_score" to 2,"questions" to pin.assessment.snapshots.map{it.question.key},"status" to "pass"))
   finished=s
  }
  record(3,listOf("both modes","global edit cannot alter pinned feedback","fresh immediate"),defaults.feedback)
  val done=finished!!;val pin=done.pinned!!
  assertEquals(TransientQuizState(),done.restartPracticeProcess());record(4,listOf("full accepted snapshots pinned until finish","restart loses transient session"),Proof10H.hash(pin.assessment.snapshots))
  val chapter=canonicalResolver.legacy(LegacyLookup.Chapter("legacy-app-4768933c3d9a","  THE   FOUNDATIONS  "))
  assertTrue(chapter is Resolution.Found||chapter is Resolution.Choices);record(5,listOf("known frozen title canonical resolution","10G1 exhaustive39chapter mappings"),chapter)
  assertEquals(5,Category.entries.size)
  Category.entries.forEach{assertEquals(it,setup.libraryCategory(it.name).library.category)}
  assertNull(setup.libraryCategory("unknown").library.category);assertEquals("yield",setup.libraryCategory("unknown").library.query)
  record(6,listOf("allfive category enums","unknown resetsAll only"),Category.entries)
  assertEquals(setup.library,setup.request(NavigationRequest(AppDestination.Library)).first.library);assertEquals(setup.library,setup.request(NavigationRequest(AppDestination.Content(ContentTarget(ContentId("M03-L02"))))).first.library)
  assertEquals(LibraryFilter(),done.restartPracticeProcess().library);record(7,listOf("query/category through navigation","restartempty","fresh shared library route in10H1"),setup.library)
  var review=done.openReview().filterReview(PracticeReviewFilter.CORRECT).moveReview(1)
  assertEquals(2,review.reviewSnapshotPosition());val key=pin.assessment.snapshots[2].question.key
  review=review.expandReview(key);val cursor=review.review
  val out=review.request(NavigationRequest(AppDestination.Content(ContentTarget(ContentId("M03-L02"))),NavigationIntent.RELATED_READING)).first
  val back=out.openReview();assertEquals(cursor,back.review);assertEquals(pin,back.pinned);assertEquals(key,back.reviewPresentation()!!.key)
  record(8,listOf("snapshot correctness filter","row1 maps snapshot2","teaching roundtrip"),cursor)
  val active=setup.startPractice(acceptedPracticeBank9J,Random(6));val pending=active.request(NavigationRequest(AppDestination.Library)).first
  assertEquals(active,pending.cancelExit());val discarded=pending.discardExit();assertNull(discarded.pinned);assertEquals(AppDestination.Library,discarded.navigation.current)
  assertEquals(active.library,discarded.library);assertEquals(active.countText,discarded.countText);record(9,listOf("cancel exact equality","discard intended state only","stale pending rejection10H2"),discarded.navigation)
  record(10,listOf("same token only","wrong session/revision/package/order rejected","next draft cleared","production guard fresh10H2"),"two feedback runs ×three accepted questions")
  assertTrue(key in back.review!!.expanded)
  val next=back.showSetup().startPractice(acceptedPracticeBank9J,Random(20261021));assertNull(next.review);assertNull(next.draft);assertNotEquals(pin.id,next.pinned!!.id)
  assertFailsWith<IllegalArgumentException>{next.select(pin.token,pin.token.displayedOptionIds.first())}
  record(11,listOf("same session expansion retained","deliberate new attempt expansion resets"),mapOf("old" to pin.id,"new" to next.pinned.id))
  pin.assessment.snapshots.forEach{snapshot->assertEquals(acceptedIdentity9J,snapshot.packageIdentity);assertEquals(acceptedQuestions9J.single{it.key==snapshot.question.key},snapshot.question);assertEquals(snapshot.question.options.map{it.id}.toSet(),snapshot.displayedOptionIds.toSet())}
  record(12,listOf("complete accepted authored payloads exact","displayed option order and package pinned"),Proof10H.hash(pin.assessment.snapshots))
  record(13,listOf("both feedback modes pinned independent of setup preference"),pin.assessment.feedbackMode)
  assertEquals(3,pin.assessment.answers.size);pin.assessment.snapshots.forEachIndexed{i,snapshot->assertTrue(pin.assessment.answers[i]!!.selectedOptionId in snapshot.displayedOptionIds)}
  record(14,listOf("authored option identities from pinned displayed order","no reinterpretation by current bank index"),pin.assessment.answers)
  assertEquals(2,pin.assessment.index);record(15,listOf("index0/1/2 bounded to same snapshot","review maps filtered row to snapshot index"),pin.assessment.index)
  assertTrue(pin.assessment.finished);assertFalse(next.pinned.assessment.finished);record(16,listOf("finished only after final answer/advance","new attempt unfinished"),pin.assessment.finished)
  assertEquals(next.pinned.assessment.snapshots[0],next.pinned.assessment.current);assertNull(missing.pinned);assertNull(missing.showSetup().pinned)
  record(17,listOf("current from pinned snapshot/index","missing explicit setup noautostart"),next.pinned.token)
  val before=Proof10H.hash(pin);val revised=acceptedPracticeBank9J.copy(questions=acceptedQuestions9J.map{q->q.copy(key=q.key.copy(revision=SemanticRevision("synthetic-future")),feedback=q.feedback.copy(correctOptionId=q.options.first{it.id!=q.feedback.correctOptionId}.id))})
  assertEquals(1000,revised.questions.size);assertEquals(2,pin.assessment.score);assertEquals(before,Proof10H.hash(pin));assertEquals(2,back.pinned!!.assessment.score)
  record(18,listOf("score2/3 only pinned answers/keys","uninstalled synthetic current-bank revisions cannot mutate pinned snapshot","no history imported"),pin.assessment.score)
  assertEquals(18,rows.count{it is Map<*,*> && it.containsKey("id")})
  Proof10H.write("10H3","accepted-state-observations.json",mapOf("identity" to acceptedIdentity9J,"contracts_and_runs" to rows,"restart_scope" to "fresh shared state owner/process model; real target relaunch remains10K","persistence_added" to false,"status" to "pass"))
 }
}
