package se.korkort
import java.lang.reflect.Modifier
import java.nio.file.Files
import java.nio.file.Path
import kotlin.test.*
class QuestionContract10ETest {
    private val root: Path get() = generateSequence(Path.of(System.getProperty("user.dir"))) { it.parent }.first { Files.exists(it.resolve("content/curriculum.json")) }
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
        is Map<*, *> -> value.entries.sortedBy { it.key.toString() }.joinToString(",", "{", "}") { canonical(it.key) + ":" + canonical(it.value) }
        else -> {
            val fields = value.javaClass.declaredFields.filter { !Modifier.isStatic(it.modifiers) && !it.isSynthetic }.associate { field ->
                field.isAccessible = true
                field.name.replace(Regex("([A-Z])")) { "_" + it.value.lowercase() } to field.get(value)
            }.toMutableMap()
            if (fields.keys == setOf("value")) canonical(fields.getValue("value")) else {
                if(value is BlockPayload.RelatedLinks) fields["links"]=value.links.map{mapOf("label" to it.label,"target" to it.target)}
                if (value is InlineContent || value is BlockPayload || value is TeachingLink)
                    fields["type"] = value.javaClass.simpleName.replace(Regex("([a-z])([A-Z])"),"$1_$2").lowercase()
                canonical(fields)
            }
        }
    }
    @Test fun exportFullAcceptedQuestionContracts() {
        assertEquals(1000,acceptedQuestions9J.size)
        assertEquals(500,acceptedQuestions9J.map{it.conceptId}.toSet().size)
        Files.writeString(root.resolve("docs/curriculum/app-migration/verification-evidence/10E1/compiled-question-contracts.json"),canonical(mapOf("identity" to acceptedPracticeBank9J.identity,"questions" to acceptedQuestions9J)))
    }
}
