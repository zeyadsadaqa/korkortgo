package se.korkort
import java.lang.reflect.Modifier
import java.nio.file.Files
import java.nio.file.Path
import kotlin.test.*
class ArtworkContract10DTest {
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
    @Test fun exportActualAcceptedArtworkContracts() {
        val signQuestions=acceptedQuestions9J.filter{it.key.questionId.value.startsWith("sign-") && it.relationship.disposition!=QuestionDisposition.RETAIN}
        assertEquals(616,signQuestions.size)
        val rows=signQuestions.map{q->
            val snapshot=q.snapshot(acceptedPracticeBank9J.identity,kotlin.random.Random(10))
            val pre=snapshot.presentation(null,false,true)
            assertNull(pre.explanation);assertNull(pre.targetCode);assertNull(pre.targetLabel)
            assertTrue(pre.choices.all{it.correct==null && it.feedback==null && !it.selected})
            mapOf("question" to q,"pre_answer" to pre,"snapshot_order" to snapshot.displayedOptionIds)
        }
        Files.writeString(root.resolve("docs/curriculum/app-migration/verification-evidence/10D1/compiled-artwork-contracts.json"),canonical(mapOf("package_identity" to acceptedPracticeBank9J.identity,"rows" to rows)))
    }
}
