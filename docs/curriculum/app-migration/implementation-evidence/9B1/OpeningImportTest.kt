package se.korkort

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

/** Staged-import checks; this source is included only by the saved test init script. */
class OpeningImportTest {
    private val payload get() = stagedCurriculum9B1.curriculum
    private fun plain(nodes: RichText): String = nodes.joinToString("") {
        when (it) {
            is InlineContent.Text -> it.text
            is InlineContent.Strong -> plain(it.children)
            is InlineContent.Emphasis -> plain(it.children)
            is InlineContent.Link -> plain(it.label)
            is InlineContent.Math -> it.expression
        }
    }

    @Test fun sixtyReadingNodesPreserveStructureWithoutInventedBodies() {
        val expected = (1..10).flatMap { n ->
            val id = "M" + n.toString().padStart(2, '0')
            listOf(id) + (1..4).map { id + "-L" + it.toString().padStart(2, '0') } + (id + "-R")
        }
        assertEquals(expected, payload.readingOrder.map { it.value })
        assertEquals(10, payload.modules.size)
        val documents = payload.documents.associateBy { it.id.value }
        assertTrue(expected.all { documents.getValue(it).bodyBlocks.isEmpty() && documents.getValue(it).answerBlocks.isEmpty() })
        assertEquals(40, payload.lessonCategoryTags.size)
        assertTrue(payload.modules.all { it.lessonIds.size == 4 })
        assertTrue(listOf("M01-L01", "M07-L04", "M10-L03").all { id -> payload.lessonCategoryTags.keys.any { it.value == id } })
    }

    @Test fun completeDisclaimerIsPartOfIntroductoryContent() {
        val doc = payload.documents.single { it.id.value == "introduction" }
        val disclaimer = doc.bodyBlocks.map { it.payload }.filterIsInstance<BlockPayload.Paragraph>().single { it.role == TeachingRole.DISCLAIMER }
        assertEquals("This material is a learning aid to help you understand Swedish driving theory. It is not an official source and cannot replace official information from Trafikverket and Transportstyrelsen. Always consult their current guidance and the applicable rules.", plain(disclaimer.text))
        assertEquals(setOf("cover", "introduction", "study-guide", "contents"), payload.documents.filter { it.kind == DocumentKind.FRONT_MATTER }.map { it.id.value }.toSet())
        assertTrue(payload.documents.filter { it.kind == DocumentKind.FRONT_MATTER }.none { it.id in payload.readingOrder })
        assertTrue(payload.modules.none { it.id.value in setOf("cover", "introduction", "study-guide", "contents") })
    }

    @Test fun contentsLinksUseCanonicalModulesAndNoPendingReferenceRoutes() {
        val contents = payload.documents.single { it.id.value == "contents" }
        val lists = contents.bodyBlocks.map { it.payload }.filterIsInstance<BlockPayload.ListItems>()
        val moduleList = lists.single { it.ordered }
        val targets = moduleList.items.map { item ->
            val paragraph = item.single().payload as BlockPayload.Paragraph
            ((paragraph.text.single() as InlineContent.Link).target as TeachingLink.Internal).target
        }
        assertEquals(payload.modules.map { ContentTarget(it.id) }, targets)
        val appendices = lists.single { !it.ordered }
        assertEquals(4, appendices.items.size)
        assertTrue(appendices.items.all { row -> (row.single().payload as BlockPayload.Paragraph).text.all { it is InlineContent.Text } })
        assertTrue(stagedCurriculum9B1.questions.questions.isEmpty())
        assertTrue(stagedCurriculum9B1.sources.destinations.isEmpty())
        assertTrue(stagedCurriculum9B1.legacyAliases.aliases.isEmpty())
    }
}
