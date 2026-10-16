package se.korkort

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class CompleteReadingImportTest {
    private val pack get() = stagedCurriculum9B17
    private val curriculum get() = pack.curriculum
    @Test fun everyPublishedDestinationIsUniqueAndReadingIsComplete() {
        val ids=curriculum.documents.map { it.id }+curriculum.referenceGroups.map { it.id }+curriculum.signEntries.map { it.id }+curriculum.anchors.map { it.id }+pack.sources.destinations.map { it.id }
        assertEquals(1123,ids.size)
        assertEquals(ids.size,ids.toSet().size)
        assertEquals(60,curriculum.readingOrder.size)
        assertEquals(40,curriculum.lessonCategoryTags.size)
        val documents=curriculum.documents.associateBy { it.id }
        assertTrue(curriculum.readingOrder.all { documents.getValue(it).bodyBlocks.isNotEmpty() })
        assertTrue(documents.values.filter { it.kind==DocumentKind.LESSON }.all { it.objectives.isNotEmpty() })
    }
    @Test fun fiftyAnswersStaySeparateAndModuleHubsReachAllFive() {
        assertEquals(50,curriculum.documents.sumOf { it.answerBlocks.size })
        assertTrue(curriculum.documents.flatMap { it.answerBlocks }.all { it.visibility==AnswerVisibility.AFTER_DELIBERATE_REVEAL })
        for (n in 1..10) {
            val hub=curriculum.documents.single { it.id.value=="M"+n.toString().padStart(2,'0')+"-answers" }
            assertEquals(5,(hub.bodyBlocks.single().payload as BlockPayload.RelatedLinks).links.size)
        }
        assertTrue(pack.questions.questions.isEmpty())
    }
    @Test fun referenceMembershipAndExactArtworkAreComplete() {
        assertEquals(24,curriculum.referenceGroups.size)
        assertEquals(400,curriculum.signEntries.size)
        assertEquals(400,curriculum.referenceGroups.flatMap { it.entryIds }.toSet().size)
        assertEquals(484,curriculum.assets.size)
        assertTrue(curriculum.assets.all { it.original.sha256==it.bundled.sha256 && it.bundled.path.startsWith("composeApp/src/commonMain/composeResources/files/curriculum/") })
        assertTrue(curriculum.signEntries.any { it.code=="F31a" })
        assertTrue(curriculum.signEntries.none { it.code in setOf("SIG16","SIG17","SIG18") })
    }
    @Test fun scopedSourcesPreserveCommercialManufacturerForeignAndHealthcareLimits() {
        assertEquals(116,pack.sources.destinations.size)
        val refs=pack.sources.references
        assertTrue(refs.any { SourceClassification.COMMERCIAL_TEACHING in it.classifications })
        assertTrue(refs.any { SourceClassification.MANUFACTURER in it.classifications })
        assertTrue(refs.any { SourceClassification.FOREIGN_PUBLIC_AUTHORITY in it.classifications })
        assertTrue(refs.any { "1177.se" in it.url && SourceClassification.SWEDISH_PUBLIC_SERVICE in it.classifications })
        assertTrue(refs.all { it.evidence.isNotEmpty() })
    }
}
