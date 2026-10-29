package se.korkort

import java.lang.reflect.Modifier
import java.security.MessageDigest
import kotlin.test.*

/** Compiled teaching must match the accepted step10-r1 hashes retained as test resources. */
class LearningReaderParityTest {
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
    @Test fun completeCompiledTeachingMatchesAllAuthoringFields() {
        val expected = checkNotNull(javaClass.getResourceAsStream("/content-parity/reader-parity.tsv")) {
            "Missing reader parity fixture"
        }.bufferedReader().use { it.readLines() }
            .associate { line -> line.split('\t').let { it[0] to it[1] } }
        val fields=mapOf("modules" to readerModules,"documents" to readerDocuments,"reading_order" to readerOrder,"lesson_category_tags" to readerTags,"assets" to readerAssets)
        fields.forEach{(name,value)->
            val text=canonical(value)
            val digest=MessageDigest.getInstance("SHA-256").digest(text.toByteArray()).joinToString(""){"%02x".format(it)}
            assertEquals(expected.getValue(name),digest,name)
        }
    }
}
