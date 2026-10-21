package se.korkort
import kotlin.test.*
import kotlin.random.Random
import java.nio.file.Files

class Allocation10FTest {
 @Test fun allLengthsSeedsCapacityAndIneligibleBoundaries() {
  val bank=acceptedPracticeBank9J
  val oracle=Files.readAllLines(Proof10F.root.resolve("docs/curriculum/app-migration/verification-evidence/10F1/allocation-oracle.tsv")).associate{line->val v=line.split('\t').map{it.toInt()};v[0] to v.drop(1)}
  val capacity=bank.questions.groupBy{it.conceptId};assertEquals(500,capacity.size)
  assertTrue(capacity.values.all{it.map{q->q.category}.distinct().size==1})
  val cases=mutableListOf<Any>();val rejected=mutableListOf<Any>()
  for(n in 1..70) {
   val expected=oracle.getValue(n);val actual=QuizEngine.allocation(n)
   assertEquals(expected,Category.entries.map{actual.categories.getValue(it)}+actual.random)
   assertTrue(practiceStartCheck(n.toString(),bank).allowed)
   for(seed in 0..19) {
    val snapshots=AssessmentEngine.select(bank.questions,n,bank.identity,Random(seed))
    assertEquals(n,snapshots.size);assertEquals(n,snapshots.map{it.question.conceptId}.distinct().size)
    assertTrue(snapshots.all{it.packageIdentity==bank.identity && it.question in bank.questions && it.question.acceptance.eligibility==ScoringEligibility.ACCEPTED})
    val counts=Category.entries.map{c->snapshots.count{it.question.category==c}}
    assertTrue(counts.indices.all{counts[it]>=expected[it]});assertEquals(expected.last(),counts.indices.sumOf{counts[it]-expected[it]})
    assertEquals(snapshots,AssessmentEngine.select(bank.questions,n,bank.identity,Random(seed)))
    cases.add(mapOf("size" to n,"seed" to seed,"quota" to expected,"actual_categories" to counts,"residual" to counts.indices.map{counts[it]-expected[it]},"selected" to snapshots.map{mapOf("id" to it.question.key.questionId.value,"revision" to it.question.key.revision.value,"concept" to it.question.conceptId,"category" to it.question.category,"option_ids" to it.displayedOptionIds)},"status" to "pass"))
   }
  }
  val unique=capacity.values.map{it.first()}
  fun reject(name:String,qs:List<AssessmentQuestion>,size:Int=70,release:Boolean=true) {
   val candidate=bank.copy(questions=qs,releaseAccepted=release)
   val check=practiceStartCheck(size.toString(),candidate);assertFalse(check.allowed,name)
   assertFailsWith<IllegalArgumentException>(name){TransientQuizState(countText=size.toString()).showSetup().startPractice(candidate,Random(4))}
   rejected.add(mapOf("case" to name,"size" to size,"errors" to check.errors,"status" to "rejected"))
  }
  for(e in listOf(ScoringEligibility.HELD,ScoringEligibility.RETIRED,ScoringEligibility.UNREVIEWED))reject("all_${e.name.lowercase()}",unique.map{it.copy(acceptance=it.acceptance.copy(eligibility=e))},1)
  val quotaOnly=Category.entries.flatMap{c->unique.filter{it.category==c}.take(c.quota)}
  reject("65_quota_topics_no_five_residual",quotaOnly)
  reject("rules_short_others_surplus",unique.filter{it.category!=Category.RULES}+unique.filter{it.category==Category.RULES}.take(31))
  reject("duplicate_question",bank.questions+bank.questions.first())
  val crossed=unique.last().copy(conceptId=unique.first().conceptId,category=Category.entries.first{it!=unique.first().category})
  reject("concept_spans_categories",unique.dropLast(1)+crossed)
  reject("historical_candidate_release_gate",candidatePracticeBank9M.questions,1,false)
  for(raw in listOf("","0","71","-1","1.5","x","999999999999999")){assertFalse(practiceStartCheck(raw,bank).allowed);rejected.add(mapOf("case" to "invalid_count","input" to raw,"status" to "rejected"))}
  val eligibleMixed=bank.questions+unique.take(5).mapIndexed{i,q->q.copy(key=q.key.copy(questionId=QuestionId("fixture-held-$i")),conceptId="fixture-held-$i",acceptance=q.acceptance.copy(eligibility=ScoringEligibility.HELD))}
  assertTrue(AssessmentEngine.select(eligibleMixed,70,bank.identity,Random(3)).none{it.question.key.questionId.value.startsWith("fixture-")})
  Proof10F.write("10F1","length-quota-capacity-results.json",mapOf("status" to "pass","identity" to bank.identity,"cases" to cases,"rejections" to rejected,"category_concept_capacity" to Category.entries.associateWith{c->capacity.values.count{it.first().category==c}},"mixed_held_exclusion" to "pass","limits" to "Actual accepted bank engine/model evidence; no platform UI assertion."))
 }
}
