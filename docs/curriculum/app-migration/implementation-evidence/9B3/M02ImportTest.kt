package se.korkort

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertTrue

class M02ImportTest {
    private val payload get() = stagedCurriculum9B3.curriculum
    private fun doc(id: String) = payload.documents.single { it.id.value == id }

    @Test fun twoCompleteModulesLeaveFortyEightBodiesPending() {
        assertEquals(64, payload.documents.size)
        assertEquals(60, payload.readingOrder.size)
        assertEquals(48, payload.documents.count { it.id in payload.readingOrder && it.bodyBlocks.isEmpty() })
        assertEquals(8, payload.documents.count { it.kind == DocumentKind.LESSON && it.objectives.isNotEmpty() })
        for (module in listOf("M01", "M02")) {
            assertTrue(doc(module).bodyBlocks.isNotEmpty())
            for (id in (1..4).map { "$module-L0$it" } + "$module-R") {
                val d = doc(id)
                val check = d.bodyBlocks.map { it.payload }.filterIsInstance<BlockPayload.KnowledgeCheck>().single()
                assertEquals(d.answerBlocks.single().metadata.id, check.answerId)
                assertEquals(AnswerVisibility.AFTER_DELIBERATE_REVEAL, d.answerBlocks.single().visibility)
            }
        }
        assertTrue(stagedCurriculum9B3.questions.questions.isEmpty())
    }

    @Test fun symptomTableAndSixIllustrationsRetainStructure() {
        val table = doc("M02-L01").bodyBlocks.map { it.payload }.filterIsInstance<BlockPayload.Table>().single()
        assertEquals(3, table.columns.size)
        assertEquals(4, table.rows.size)
        assertTrue(table.rows.all { it.cells.size == 3 })
        val assets = payload.assets.filter { it.id.value.startsWith("M02") }
        assertEquals(6, assets.size)
        assertTrue(assets.all { it.original == it.bundled && it.studyAltText.isNotBlank() })
        assertEquals(2, doc("M02-L04").assetBindings.size)
        val mask = doc("M02-R").bodyBlocks.map { it.payload }.filterIsInstance<BlockPayload.PolygonImage>().single()
        assertEquals(listOf(SourcePixelPoint(777,156),SourcePixelPoint(1464,156),SourcePixelPoint(1464,729),SourcePixelPoint(844,729),SourcePixelPoint(844,446),SourcePixelPoint(777,446)), mask.polygon)
        assertEquals(6, doc("M02-L01").bodyBlocks.map { it.payload }.filterIsInstance<BlockPayload.PolygonImage>().single().polygon.size)
    }

    @Test fun invalidMasksFailAtConstruction() {
        val region = ApprovedImageRegion(0, 0, 10, 10, 20, 20)
        fun mask(points: List<SourcePixelPoint>) = BlockPayload.PolygonImage(AssetId("fixture"),region,points,emptyList())
        assertFailsWith<IllegalArgumentException> { mask(listOf(SourcePixelPoint(0,0),SourcePixelPoint(10,0))) }
        assertFailsWith<IllegalArgumentException> { mask(listOf(SourcePixelPoint(0,0),SourcePixelPoint(5,0),SourcePixelPoint(10,0))) }
        assertFailsWith<IllegalArgumentException> { mask(listOf(SourcePixelPoint(0,0),SourcePixelPoint(30,0),SourcePixelPoint(0,10))) }
    }

    @Test fun sourceScopesAndVehicleLimitsRemainDistinct() {
        val sources=stagedCurriculum9B3.sources
        assertEquals(33, sources.references.size)
        assertEquals(19, sources.destinations.count { d -> d.scopedUrls.any { it.scopeId == ContentId("M02") } })
        val traffic=sources.destinations.single { it.id.value=="source-traffic-law" }
        assertEquals(listOf("M01","M02"),traffic.scopedUrls.map { it.scopeId?.value })
        val volvo=sources.references.single { "volvocars.com" in it.url }
        assertEquals(setOf(SourceClassification.MANUFACTURER),volvo.classifications)
        assertTrue(volvo.evidence.any { e -> e.limitations.any { "not imported as a universal rule" in it } })
        val seats=sources.references.single { "/saten-och-huvudstod/" in it.url }
        assertEquals(listOf("2026-10-04","2026-10-12"),seats.evidence.map { it.dates.checkedOn })
    }
}
