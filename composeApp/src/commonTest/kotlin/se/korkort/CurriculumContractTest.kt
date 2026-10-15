package se.korkort

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertNotEquals
import kotlin.test.assertTrue

class CurriculumContractTest {
    private val hash = Sha256("a".repeat(64))
    private val origin = OriginLocator(FileIdentity("fixture.md", hash), "heading/check")
    private val review = ReviewEvidence(origin, null)
    private fun text(value: String): RichText = listOf(InlineContent.Text(value))
    private fun metadata(id: String) = BlockMetadata(BlockId(id), origin)
    private fun question(acceptance: AssessmentAcceptance = AssessmentAcceptance(
        ScoringEligibility.UNREVIEWED, null, emptyList(), emptyList(), emptyList(),
    )): AssessmentQuestion {
        val options = (1..4).map { AssessmentOption(OptionId("option-$it"), text("Choice $it"), null) }
        return AssessmentQuestion(
            QuestionRevisionKey(QuestionId("fixture-question"), SemanticRevision("r1")),
            "fixture-concept", Category.RULES, text("Choose an option"), null, options,
            AssessmentFeedback(null, null, options[1].id, text("Explanation"), options.map {
                AssessmentOptionFeedback(it.id, text("Why"), null, null, emptyList())
            }),
            QuestionRelationship(ContentId("M03-L02"), emptyList(), emptyList(), emptyList(),
                emptyList(), QuestionDisposition.REWRITE, "screen-fixture"),
            acceptance, origin,
        )
    }

    @Test fun duplicateOrIncompleteAssessmentIdentityIsRejected() {
        val q = question()
        assertFailsWith<IllegalArgumentException> { q.copy(options = listOf(q.options[0], q.options[0], q.options[2], q.options[3])) }
        assertFailsWith<IllegalArgumentException> { q.copy(feedback = q.feedback.copy(correctOptionId = OptionId("unknown"))) }
        assertFailsWith<IllegalArgumentException> { q.copy(feedback = q.feedback.copy(optionFeedback = q.feedback.optionFeedback.drop(1))) }
        // Equal learner labels are valid: authored identity, not code-bearing label uniqueness, governs options.
        assertEquals(4, q.copy(options = q.options.map { it.copy(text = text("Illustration")) }).options.size)
    }

    @Test fun acceptedQuestionsCannotContainUnreviewedImagesOrOpenHolds() {
        val accepted = AssessmentAcceptance(ScoringEligibility.ACCEPTED, review, emptyList(), emptyList(), emptyList())
        assertFailsWith<IllegalArgumentException> {
            accepted.copy(openHolds = listOf(AssessmentHold("faint", "Unproven image", "Device proof")))
        }
        assertFailsWith<IllegalArgumentException> { accepted.copy(contentReview = null) }
        val q = question(accepted)
        assertFailsWith<IllegalArgumentException> {
            q.copy(image = AssessmentImageBinding(AssetId("exact-image"), null))
        }
        assertFailsWith<IllegalArgumentException> {
            q.copy(options = q.options.mapIndexed { index, option ->
                if (index == 2) option.copy(image = AssessmentImageBinding(AssetId("distractor"), null)) else option
            })
        }
        assertFailsWith<IllegalArgumentException> {
            q.copy(relationship = q.relationship.copy(disposition = QuestionDisposition.REMOVE))
        }
        assertEquals(ScoringEligibility.ACCEPTED,
            q.copy(image = AssessmentImageBinding(AssetId("exact-image"), NeutralImageDescription("Visible features", review))).acceptance.eligibility)
    }

    @Test fun snapshotPinsExactRevisionPackageAndOptionOrder() {
        val q = question()
        val packageId = ContentPackageIdentity("app-content-r1", hash)
        val snapshot = SessionQuestionSnapshot(q, packageId, listOf(q.options[3].id, q.options[0].id, q.options[2].id, q.options[1].id))
        val answer = SnapshotAnswer(snapshot.question.key, snapshot.displayedOptionIds[3])
        assertEquals(q.feedback.correctOptionId, answer.selectedOptionId)
        val changed = q.copy(key = q.key.copy(revision = SemanticRevision("r2")), feedback = q.feedback.copy(correctOptionId = q.options[0].id))
        assertNotEquals(changed.key, answer.question)
        assertEquals(SemanticRevision("r1"), snapshot.question.key.revision)
        assertEquals(packageId, snapshot.packageIdentity)
        assertFailsWith<IllegalArgumentException> { snapshot.copy(displayedOptionIds = List(4) { q.options[0].id }) }
        assertFailsWith<IllegalArgumentException> { snapshot.copy(displayedOptionIds = q.options.map { it.id }.drop(1)) }
    }

    @Test fun knowledgeCheckAnswersAreSeparateFromVisibleBody() {
        val answerId = BlockId("M03-L02/check-1/answer")
        val prompt = ContentBlock(metadata("M03-L02/check-1/prompt"), BlockPayload.Paragraph(text("What should you do?"), TeachingRole.EXPLANATION))
        val check = ContentBlock(metadata("M03-L02/check-1"), BlockPayload.KnowledgeCheck(listOf(prompt), answerId))
        val answer = AnswerBlock(BlockMetadata(answerId, origin), AnswerVisibility.AFTER_DELIBERATE_REVEAL,
            listOf(ContentBlock(metadata("M03-L02/check-1/answer/text"), BlockPayload.Paragraph(text("Reviewed answer"), TeachingRole.EXPLANATION))))
        val doc = CurriculumDocument(ContentId("M03-L02"), DocumentKind.LESSON, ContentId("M03"), "Fixture", 2,
            emptyList(), listOf(check), listOf(answer), emptyList(), emptyList(), emptyList(), "screen-fixture", SemanticRevision("r1"), origin)
        assertTrue(doc.bodyBlocks.none { it.metadata.id == answerId })
        assertEquals(doc.answerBlocks.single().metadata.id, (doc.bodyBlocks.single().payload as BlockPayload.KnowledgeCheck).answerId)
        assertEquals(AnswerVisibility.AFTER_DELIBERATE_REVEAL, doc.answerBlocks.single().visibility)
    }

    @Test fun tableAndSourceMetadataPreserveRequiredDistinctions() {
        val table = BlockPayload.Table(text("Distances"), listOf(TableColumn(text("Speed")), TableColumn(text("Distance"))),
            listOf(TableRow(listOf(text("70 km/h"), text("40.6 m")))))
        assertEquals(2, table.rows.single().cells.size)
        assertFailsWith<IllegalArgumentException> { table.copy(rows = listOf(TableRow(listOf(text("Incomplete"))))) }
        val dates = SourceDates(retrievedOn = "2026-10-01")
        assertEquals(null, dates.checkedOn)
        assertEquals(null, dates.publishedOn)
        val source = SourceDestination(ContentId("source-traffic-law"), "traffic-law", "Fixture",
            listOf(ScopedSourceUrl(ContentId("M03"), SourceReferenceId("REF-module-3")),
                ScopedSourceUrl(ContentId("M08"), SourceReferenceId("REF-module-8"))), origin)
        assertNotEquals(source.scopedUrls[0].referenceId, source.scopedUrls[1].referenceId)
    }
}
