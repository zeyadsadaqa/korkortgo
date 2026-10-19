package se.korkort

import java.lang.reflect.Modifier
import java.nio.file.Files
import java.nio.file.Path
import java.security.MessageDigest
import kotlin.random.Random
import kotlin.test.*

/** End-to-end parity uses actual compiled objects, independent of the Python emitter. */
class AcceptedQuestionParityTest {
    private val root: Path get() = generateSequence(Path.of(System.getProperty("user.dir"))) { it.parent }.first { Files.exists(it.resolve("content/assessment-questions.json")) }
    private val evidence get() = root.resolve("docs/curriculum/app-migration/implementation-evidence/closure-9j-9m-9l14")
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
        val expected = Files.readAllLines(evidence.resolve("accepted-question-parity.tsv")).associate { line -> line.split('\t').let { it[0] to it[1] } }
        val manifest = Files.readString(root.resolve("content/accepted-content-manifest.json"))
        val manifestDigest = Regex("\"manifest_sha256\": \"([a-f0-9]+)\"").find(manifest)!!.groupValues[1]
        assertEquals(manifestDigest, acceptedIdentity9J.manifestSha256.value)
        assertEquals(1000, acceptedQuestions9J.size)
        assertEquals(500, acceptedQuestions9J.map { it.conceptId }.toSet().size)
        acceptedQuestions9J.forEach { q ->
            val digest = MessageDigest.getInstance("SHA-256").digest(canonical(q).toByteArray()).joinToString("") { "%02x".format(it) }
            assertEquals(expected.getValue(q.key.questionId.value), digest, q.key.questionId.value)
        }
        Files.writeString(evidence.resolve("accepted-compiled-parity.json"), """{"questions":1000,"concepts":500,"complete_object_sha256_parity":"passed","release_accepted":true}
""")
    }
}
