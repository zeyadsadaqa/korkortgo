package se.korkort

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertTrue

class M01ImportTest {
    private val payload get() = stagedCurriculum9B2.curriculum
    private fun doc(id: String) = payload.documents.single { it.id.value == id }

    @Test fun onlyM01HasCompleteTeachingAndAnswers() {
        assertEquals(64, payload.documents.size)
        assertEquals(60, payload.readingOrder.size)
        assertEquals(54, payload.documents.count { it.id in payload.readingOrder && it.bodyBlocks.isEmpty() })
        assertEquals(4, payload.documents.count { it.kind == DocumentKind.LESSON && it.objectives.isNotEmpty() })
        assertTrue(doc("M01").bodyBlocks.isNotEmpty())
        for (id in listOf("M01-L01", "M01-L02", "M01-L03", "M01-L04", "M01-R")) {
            val d = doc(id)
            val check = d.bodyBlocks.map { it.payload }.filterIsInstance<BlockPayload.KnowledgeCheck>().single()
            assertEquals(d.answerBlocks.single().metadata.id, check.answerId)
            assertEquals(AnswerVisibility.AFTER_DELIBERATE_REVEAL, d.answerBlocks.single().visibility)
            assertTrue(check.prompts.none { it.metadata.id == check.answerId })
        }
        assertTrue(stagedCurriculum9B2.questions.questions.isEmpty())
    }

    @Test fun approvedArtworkWindowsAndAltTextSurviveGeneration() {
        val crops = listOf("M01-L02", "M01-L03", "M01-L04", "M01-R").map { id ->
            doc(id).bodyBlocks.map { it.payload }.filterIsInstance<BlockPayload.CroppedImage>().single()
        }
        assertEquals(ApprovedImageRegion(35, 171, 827, 501, 1671, 941), crops[0].region)
        assertEquals(listOf(857, 28, 855), crops.drop(1).map { it.region.left })
        assertEquals(4, payload.assets.size)
        for (crop in crops) {
            val asset = payload.assets.single { it.id == crop.assetId }
            assertEquals(asset.original, asset.bundled)
            assertTrue(asset.studyAltText.isNotBlank())
            assertEquals(AssetKind.CONTEXTUAL_ILLUSTRATION, asset.kind)
        }
        assertTrue(doc("M01-L01").assetBindings.isEmpty())
        assertFailsWith<IllegalArgumentException> { ApprovedImageRegion(0, 0, 10, 10, 5, 5) }
    }

    @Test fun scopedSourcesKeepActualClassificationAndCheckDates() {
        val sources = stagedCurriculum9B2.sources
        assertEquals(16, sources.destinations.size)
        assertEquals(16, sources.references.size)
        assertTrue(sources.destinations.all { it.scopedUrls.single().scopeId == ContentId("M01") })
        val microsleep = sources.references.single { "cdc.gov" in it.url }
        assertEquals(setOf(SourceClassification.FOREIGN_PUBLIC_AUTHORITY), microsleep.classifications)
        assertEquals("2026-10-12", microsleep.evidence.single().dates.checkedOn)
        assertTrue(microsleep.evidence.single().limitations.isNotEmpty())
        val supervisor = sources.destinations.single { it.id.value == "source-supervisor" }
        val reference = sources.references.single { it.id == supervisor.scopedUrls.single().referenceId }
        assertEquals("2026-10-04", reference.evidence.single().dates.checkedOn)
        assertEquals(null, reference.evidence.single().dates.publishedOn)
        assertEquals(listOf(ContentTarget(ContentId("M07-L03"))), doc("M01-L02").relatedContent)
    }
}
