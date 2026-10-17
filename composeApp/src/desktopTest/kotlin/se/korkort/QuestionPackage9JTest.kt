package se.korkort

import java.lang.reflect.Modifier
import java.nio.file.Files
import java.nio.file.Path
import java.security.MessageDigest
import kotlin.random.Random
import kotlin.test.*

/** End-to-end parity uses actual compiled objects, independent of the Python emitter. */
class QuestionPackage9JTest {
    private val root: Path get() = generateSequence(Path.of(System.getProperty("user.dir"))) { it.parent }.first { Files.exists(it.resolve("content/assessment-questions.json")) }
    private val evidence get() = root.resolve("docs/curriculum/app-migration/implementation-evidence/9J")
    private fun quote(text: String): String = buildString {
        append('"')
        text.forEach { c -> when (c) {
            '"' -> append("\\\""); '\\' -> append("\\\\"); '\n' -> append("\\n"); '\r' -> append("\\r"); '\t' -> append("\\t")
            else -> if (c.code < 32) append("\\u%04x".format(c.code)) else append(c)
        } }
        append('"')
    }
    private fun canonical(value: Any?): String = when (value) {
        null -> "null"
        is String -> quote(value)
        is Number, is Boolean -> value.toString()
        is Enum<*> -> quote(value.name.lowercase())
        is Iterable<*> -> value.joinToString(",", "[", "]") { canonical(it) }
        is Map<*, *> -> value.entries.sortedBy { it.key.toString() }.joinToString(",", "{", "}") { quote(it.key.toString()) + ":" + canonical(it.value) }
        else -> {
            val fields = value.javaClass.declaredFields.filter { !Modifier.isStatic(it.modifiers) && !it.isSynthetic }.associate { field ->
                field.isAccessible = true
                field.name.replace(Regex("([A-Z])")) { "_" + it.value.lowercase() } to field.get(value)
            }.toMutableMap()
            if (fields.keys == setOf("value")) canonical(fields.getValue("value")) else {
                if (value is InlineContent.Text) fields["type"] = "text"
                canonical(fields)
            }
        }
    }
    @Test fun everyCompiledRecordMatchesFullJsonIncludingSourcesHoldsAndFeedback() {
        val expected = Files.readAllLines(evidence.resolve("question-parity.tsv")).associate { line -> line.split('\t').let { it[0] to it[1] } }
        val manifest = Files.readString(root.resolve("content/content-manifest.json"))
        val manifestDigest = Regex("\"manifest_sha256\": \"([a-f0-9]+)\"").find(manifest)!!.groupValues[1]
        assertEquals(manifestDigest, candidateIdentity9J.manifestSha256.value)
        assertEquals(1000, candidateQuestions9J.size)
        assertEquals(500, candidateQuestions9J.map { it.conceptId }.toSet().size)
        candidateQuestions9J.forEach { q ->
            val digest = MessageDigest.getInstance("SHA-256").digest(canonical(q).toByteArray()).joinToString("") { "%02x".format(it) }
            assertEquals(expected.getValue(q.key.questionId.value), digest, q.key.questionId.value)
        }
        Files.writeString(evidence.resolve("compiled-parity.json"), """{"questions":1000,"concepts":500,"complete_object_sha256_parity":"passed","release_accepted":false}
""")
    }
    @Test fun allCanonicalRelationshipsResolveAndHeldProposalsStayOutOfLiveBank() {
        assertFalse(candidateReleaseAccepted9J)
        assertEquals(1000, questionRelationships9J.size)
        questionBank.forEach { row ->
            val r = row.canonicalRelationship
            (listOf(r.primaryLessonId) + r.relatedLessonIds + r.referenceIds + r.sourceIds).forEach { id -> assertIs<Resolution.Found>(canonicalResolver.canonical(ContentTarget(id))) }
            if (row.id.startsWith("sign-") && row.assessment == null) assertTrue(QuestionId(row.id) in replacementDeliveryHolds)
        }
        assertEquals(384, candidateQuestions9J.count { it.acceptance.eligibility == ScoringEligibility.ACCEPTED })
        assertEquals(616, candidateQuestions9J.count { it.acceptance.eligibility == ScoringEligibility.HELD })
    }
    @Test fun everyLengthAndSeedPreserveQuotasConceptUniquenessAndResidualPicks() {
        val accepted = candidateQuestions9J.filter { it.acceptance.eligibility == ScoringEligibility.ACCEPTED }
        val counts = Category.entries.associateWith { category -> accepted.filter { it.category == category }.map { it.conceptId }.distinct().size }
        assertEquals(listOf(45, 26, 45, 47, 29), Category.entries.map { counts[it] })
        assertEquals(listOf(7,5,16,32,5), Category.entries.map { QuizEngine.allocation(70).categories[it] })
        assertEquals(5, QuizEngine.allocation(70).random)
        for (size in 1..70) for (seed in 0..19) {
            val selected = AssessmentEngine.select(candidateQuestions9J, size, candidateIdentity9J, Random(seed))
            val allocation = QuizEngine.allocation(size)
            assertEquals(size, selected.size)
            assertEquals(size, selected.map { it.question.conceptId }.distinct().size)
            assertTrue(selected.all { it.question.acceptance.eligibility == ScoringEligibility.ACCEPTED })
            allocation.categories.forEach { (category, quota) -> assertTrue(selected.count { it.question.category == category } >= quota) }
            assertEquals(allocation.random, size-allocation.categories.values.sum())
            // Largest-remainder allocation, independently reconstructed from integer remainders.
            val weights = Category.entries.map { it.quota } + 5
            val independent = weights.map { size * it / 70 }.toMutableList()
            val order = weights.indices.sortedWith(compareByDescending<Int> { size * weights[it] % 70 }.thenBy { it })
            repeat(size-independent.sum()) { independent[order[it]]++ }
            assertEquals(independent, Category.entries.map { allocation.categories.getValue(it) } + allocation.random)
        }
        val categoryJson=Category.entries.joinToString(",") { quote(it.name.lowercase())+":"+counts.getValue(it) }
        Files.writeString(evidence.resolve("capacity-report.json"), """{"pool":"held candidate accepted subset","accepted_questions":384,"accepted_concepts":192,"held_questions":616,"category_concepts":{$categoryJson},"lengths_checked":[1,70],"seeds_per_length":20,"selections_checked":1400,"quota_at_70":[7,5,16,32,5],"residual_at_70":5,"largest_remainder":"passed","concept_uniqueness":"passed","quota_changes":false,"release_accepted":false}
""")
    }
    @Test fun allKeysVisitEveryPositionAndBothFeedbackModesStayGuarded() {
        candidateQuestions9J.forEach { q ->
            val positions=mutableSetOf<Int>()
            repeat(80) { seed ->
                val snapshot=q.snapshot(candidateIdentity9J,Random(seed))
                positions+=snapshot.displayedOptionIds.indexOf(q.feedback.correctOptionId)
                assertEquals(1,snapshot.displayedOptionIds.count { snapshot.isCorrect(SnapshotAnswer(q.key,it)) })
                snapshot.displayedOptionIds.forEach { id -> assertEquals(id,snapshot.feedbackFor(id).optionId) }
            }
            assertEquals(setOf(0,1,2,3),positions,q.key.questionId.value)
            if (q.acceptance.eligibility==ScoringEligibility.ACCEPTED) {
                Feedback.entries.forEach { mode ->
                    var session=AssessmentSession(listOf(q.snapshot(candidateIdentity9J,Random(9))),mode)
                    assertNull(session.presentation().explanation)
                    session=session.answer(q.feedback.correctOptionId)
                    assertEquals(mode==Feedback.IMMEDIATE,session.presentation().explanation!=null)
                    session=session.next()
                    assertEquals(1,session.score)
                    assertNotNull(session.presentation().explanation)
                }
            } else assertFailsWith<IllegalArgumentException> { AssessmentSession(listOf(q.snapshot(candidateIdentity9J)),Feedback.IMMEDIATE) }
        }
        Files.writeString(evidence.resolve("shuffle-report.json"), """{"questions":1000,"seeds_per_question":80,"all_four_key_positions":"passed","feedback_identity":"passed","accepted_questions_in_both_feedback_modes":384,"held_session_rejections":616,"release_accepted":false}
""")
    }
}
