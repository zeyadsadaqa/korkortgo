package se.korkort
import kotlin.test.*
class Alias10GTest {
 @Test fun exportEveryActualAliasAndAcceptedQuestionRoute() {
  assertEquals(1921,navigationAliases.aliases.size)
  assertEquals(1000,acceptedQuestions9J.size)
  val aliases=navigationAliases.aliases.map{a->mapOf("lookup" to a.lookup,"declared_outcome" to a.outcome,"origin" to a.origin,"actual" to canonicalResolver.legacy(a.lookup))}
  val pages=questionBank.associate{it.id to it.page}
  val questions=acceptedQuestions9J.map{q->val page=pages.getValue(q.key.questionId.value);mapOf("key" to q.key,"concept_id" to q.conceptId,"accepted_status" to q.acceptance.eligibility,"relationship" to q.relationship,"legacy_page" to page,"actual" to canonicalResolver.lookup(questionId=q.key.questionId),"with_page_context" to canonicalResolver.lookup(questionId=q.key.questionId,legacy=LegacyLookup.Page("legacy-app-4768933c3d9a",page)),"related" to q.relationship.relatedLessonIds.map{canonicalResolver.canonical(ContentTarget(it))},"references" to q.relationship.referenceIds.map{canonicalResolver.canonical(ContentTarget(it))},"sources" to q.relationship.sourceIds.map{canonicalResolver.canonical(ContentTarget(it))})}
  Proof10G.write("10G1","compiled-alias-observations.json",mapOf("identity" to acceptedIdentity9J,"aliases" to aliases,"questions" to questions,"entries" to canonicalEntries,"anchors" to canonicalAnchors,"tombstones" to navigationAliases.tombstones))
 }
}
