package se.korkort
import kotlin.random.Random
import kotlin.test.*
class Guards10HTest {
 @Test fun acceptedAttemptGuardsAndSyntheticRecoveryBranches() {
  val rows=mutableListOf<Any>()
  fun record(id:String,value:Any?) {rows.add(mapOf("id" to id,"actual" to value,"status" to "pass"))}
  for(mode in Feedback.entries){
   var s=TransientQuizState(countText="3",feedback=mode,library=LibraryFilter("yield",Category.RULES)).showSetup().startPractice(acceptedPracticeBank9J,Random(112))
   val p=s.pinned!!;val token=p.token;s=s.select(token,token.displayedOptionIds.first())
   val related=NavigationRequest(AppDestination.Content(ContentTarget(ContentId("M03-L02"))),NavigationIntent.RELATED_READING)
   val blocked=s.request(related);assertIs<NavigationDecision.Denied>(blocked.second);assertEquals(s,blocked.first)
   record("$mode-preanswer-denied",blocked.second)
   val (pending,decision)=s.request(NavigationRequest(AppDestination.Library));assertEquals(NavigationDecision.ConfirmDiscard,decision)
   assertEquals(s,pending.cancelExit());assertEquals(s.pinned,pending.pinned);assertEquals(s.draft,pending.draft)
   assertFailsWith<IllegalArgumentException>{pending.confirm(token)}
   record("$mode-cancel-exact",mapOf("session" to p.id,"snapshot_hash" to Proof10H.hash(p),"draft" to s.draft))
   val discarded=pending.discardExit();assertNull(discarded.pinned);assertNull(discarded.draft);assertNull(discarded.review);assertNull(discarded.pendingPin)
   assertEquals(AppDestination.Library,discarded.navigation.current);assertEquals(s.countText,discarded.countText);assertEquals(mode,discarded.feedback);assertEquals(s.library,discarded.library);assertEquals(s.attemptSerial,discarded.attemptSerial)
   record("$mode-discard",discarded)
   assertEquals(s,s.request(NavigationRequest(s.navigation.current,NavigationIntent.IMAGE_VIEWER)).first)
   val confirmed=s.confirm(token);val r=confirmed.request(related)
   if(mode==Feedback.IMMEDIATE)assertEquals(NavigationDecision.ConfirmDiscard,r.second) else assertIs<NavigationDecision.Denied>(r.second)
   record("$mode-related-after-confirm",r.second)
   val source=navigationSources.references.first().id
   val request=NavigationRequest(s.navigation.current,NavigationIntent.SOURCE,sourceReferenceId=source)
   val withSource=s.request(request).first;assertNull(withSource.navigation.sourceToOpen);assertEquals(s,withSource.cancelExit())
   val left=withSource.discardExit();assertNull(left.pinned);assertEquals(AppDestination.QuizSetup,left.navigation.current);assertEquals(source,left.navigation.sourceToOpen)
   val effect=left.takeSourceToOpen();assertEquals(source,effect.first);assertNull(effect.second.takeSourceToOpen().first)
   record("$mode-source-once",effect.first)
   val different=withSource.copy(pinned=withSource.pinned!!.copy(assessment=withSource.pinned.assessment.answer(token.displayedOptionIds.first())))
   assertFailsWith<IllegalArgumentException>{different.discardExit()};record("$mode-stale-pending-rejected",true)
  }
  for(target in listOf(AppDestination.Quiz("missing"),AppDestination.Results("missing"),AppDestination.Review("missing"))){
   val original=TransientQuizState(countText="20",feedback=Feedback.AT_END)
   val (recovered,decision)=original.request(NavigationRequest(target));assertIs<NavigationDecision.MissingSession>(decision)
   assertEquals(AppDestination.QuizSetup,recovered.navigation.current);assertNull(recovered.pinned);assertEquals("20",recovered.countText);assertEquals(Feedback.AT_END,recovered.feedback)
   assertNotEquals(PracticeRecovery.NONE,recovered.recovery);assertNull(recovered.showSetup().pinned);assertEquals(PracticeRecovery.NONE,recovered.showSetup().recovery)
   record("missing-${target.javaClass.simpleName}",recovered)
  }
  val entry=canonicalEntries.first{it.blocks.isNotEmpty()};val moved=ContentTarget(entry.id,BlockId("synthetic-moved"))
  val found=assertIs<Resolution.Found>(canonicalResolver.canonical(moved));assertEquals(ContentTarget(entry.id),found.target);assertNotNull(found.notice)
  val restore=canonicalResolver.restore(ReturnContext(moved,ReadingPosition(BlockId("synthetic-moved"),10),"stale"),setOf("stale"));assertNull(restore.position);assertNull(restore.focusId);record("synthetic-moved-parent",restore)
  val unknown=canonicalResolver.restore(ReturnContext(ContentTarget(ContentId("synthetic-unknown")),ReadingPosition(BlockId("old"),10),"old"),setOf("old"));assertIs<Resolution.Unavailable>(unknown.resolution);assertNull(unknown.position);assertNull(unknown.focusId);record("synthetic-unknown-parent",unknown)
  for(count in 0..2){
   val tomb=ContentTombstone(ContentId("synthetic-retired"),canonicalEntries.take(count).map{it.id},"Reviewed retirement fixture",ReviewEvidence(navigationAliases.aliases.first().origin,null))
   val resolver=CanonicalResolver(canonicalEntries,canonicalAnchors,LegacyAliasPayload(1,emptyList(),listOf(tomb)))
   val actual=resolver.canonical(ContentTarget(tomb.retiredId))
   if(count==0)assertIs<Resolution.Unavailable>(actual) else assertEquals(tomb.replacementIds,(assertIs<Resolution.Choices>(actual)).choices.map{it.target.contentId})
   record("synthetic-retired-$count",actual)
  }
  Proof10H.write("10H2","guard-recovery-results.json",mapOf("identity" to acceptedIdentity9J,"cases" to rows,"status" to "pass_model_scope","synthetic_basis" to "No production tombstones, store or hot replacement feature; retirement/moved/unknown cases explicitly synthetic","native_modal_focus" to "pending fresh10K; shared semantics runs recorded separately"))
 }
}
