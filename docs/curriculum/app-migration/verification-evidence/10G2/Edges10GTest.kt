package se.korkort
import kotlin.test.*
class Edges10GTest {
 @Test fun everyFrozenExampleAndTypedBoundary() {
  val ns="legacy-app-4768933c3d9a";val cases=mutableListOf<Any>()
  fun record(id:String,result:Resolution,example:String?=null){cases.add(mapOf("case_id" to id,"example_id" to example,"actual" to result))}
  record("retained-question",canonicalResolver.lookup(questionId=QuestionId("situation-001"),legacy=LegacyLookup.Page(ns,8)),"retained-question")
  record("same-old-page-a",canonicalResolver.lookup(questionId=QuestionId("situation-017"),legacy=LegacyLookup.Page(ns,46)),"same-old-page-a")
  record("same-old-page-b",canonicalResolver.lookup(questionId=QuestionId("situation-103"),legacy=LegacyLookup.Page(ns,46)),"same-old-page-b")
  record("changed-fuel-key",canonicalResolver.lookup(questionId=QuestionId("fuel-saving-150-1.5")),"changed-fuel-key")
  record("replacement-image",canonicalResolver.lookup(questionId=QuestionId("sign-meaning-S1")),"replacement-image")
  record("retired-question",canonicalResolver.lookup(questionId=QuestionId("fixture-retired-question")),"retired-question")
  record("missing-exact-signal",canonicalResolver.legacy(LegacyLookup.Sign(ns,"SIG16")),"missing-exact-signal")
  record("gap-page",canonicalResolver.legacy(LegacyLookup.Page(ns,13)),"gap-page")
  record("missing-block",canonicalResolver.canonical(ContentTarget(ContentId("M03-L04"),BlockId("fixture-removed-block"))),"missing-block")
  for(page in listOf(Int.MIN_VALUE,-1,0,1,5,13,21,45,368,578,999,Int.MAX_VALUE))record("page-$page",canonicalResolver.legacy(LegacyLookup.Page(ns,page)))
  for(lookup in listOf(LegacyLookup.Page("foreign",46),LegacyLookup.Chapter("foreign","The foundations"),LegacyLookup.Topic("foreign","0"),LegacyLookup.Sign("foreign","F31a"),LegacyLookup.Sign(ns,"f31a"),LegacyLookup.Sign(ns,"F31A"),LegacyLookup.Sign(ns," F31a"),LegacyLookup.Sign(ns,"F31a "),LegacyLookup.Topic(ns,"-1"),LegacyLookup.Topic(ns,"178"),LegacyLookup.Topic(ns,"00"),LegacyLookup.Topic(ns,"unknown"),LegacyLookup.Chapter(ns,"unknown"),LegacyLookup.Sign(ns,"UNKNOWN")))record("unknown-$lookup",canonicalResolver.legacy(lookup))
  record("F31a-exact",canonicalResolver.legacy(LegacyLookup.Sign(ns,"F31a")))
  record("normalized-chapter",canonicalResolver.legacy(LegacyLookup.Chapter(ns,"  THE\n  FOUNDATIONS  ")))
  assertEquals(canonicalResolver.legacy(LegacyLookup.Chapter(ns,"The foundations")),canonicalResolver.legacy(LegacyLookup.Chapter(ns,"  THE\n  FOUNDATIONS  ")))
  record("page46-alone",canonicalResolver.legacy(LegacyLookup.Page(ns,46)))
  record("unknown-question-no-page-fallback",canonicalResolver.lookup(questionId=QuestionId("unknown"),legacy=LegacyLookup.Page(ns,46)))
  record("unknown-question-no-title-fallback",canonicalResolver.lookup(questionId=QuestionId("unknown"),legacy=LegacyLookup.Chapter(ns,"The foundations")))
  record("valid-canonical-over-question",canonicalResolver.lookup(canonical=ContentTarget(ContentId("M01-L01")),questionId=QuestionId("situation-017"),legacy=LegacyLookup.Page(ns,46)))
  record("invalid-canonical-no-question-fallback",canonicalResolver.lookup(canonical=ContentTarget(ContentId("unknown")),questionId=QuestionId("situation-017"),legacy=LegacyLookup.Page(ns,46)))
  record("unknown-canonical",canonicalResolver.canonical(ContentTarget(ContentId("unknown"))))
  record("no-input",canonicalResolver.lookup())
  val anchor=canonicalAnchors.entries.first();record("conflicting-anchor-block",canonicalResolver.canonical(ContentTarget(anchor.key,BlockId("unrelated"))))
  val chooser=canonicalResolver.legacy(LegacyLookup.Page(ns,46)) as Resolution.Choices
  val choices=chooser.choices.map{f->val initial=GuardedNavigation(AppDestination.Library,null);val (next,decision)=initial.request(NavigationRequest(AppDestination.Content(f.target)),canonicalResolver);assertEquals(NavigationDecision.Allow,decision);assertEquals(AppDestination.Content(f.target),next.current);mapOf("offered" to f.target,"navigated" to next.current,"decision" to decision)}
  val moved=canonicalResolver.restore(ReturnContext(ContentTarget(ContentId("M03-L04"),BlockId("fixture-removed-block")),ReadingPosition(BlockId("fixture-removed-block"),50),"old-focus"),setOf("old-focus"));assertNull(moved.position);assertNull(moved.focusId)
  val noninteger=listOf("46.0","1.5","abc","","9999999999999999999999").map{raw->assertNull(raw.toIntOrNull());mapOf("input" to raw,"status" to "not_representable_as_LegacyLookup_Page_Int","scope" to "Test-only input classification; there is no production string/URL page parser.")}
  val construction=listOf("blank-question" to {QuestionId(" ")},"blank-canonical" to {ContentId("")}).map{(name,call)->assertFailsWith<IllegalArgumentException>{call()};mapOf("case_id" to name,"status" to "rejected_by_typed_constructor")}
  assertTrue(navigationAliases.tombstones.isEmpty())
  Proof10G.write("10G2","compiled-edge-observations.json",mapOf("identity" to acceptedIdentity9J,"cases" to cases,"chooser_actions" to choices,"moved_restore" to moved,"anchor_fixture" to anchor.key,"noninteger_boundaries" to noninteger,"construction_boundaries" to construction,"production_tombstones" to navigationAliases.tombstones))
 }
}
