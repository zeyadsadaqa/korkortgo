package se.korkort

import kotlin.random.Random
import kotlin.test.*

class AssessmentTest {
    private val hash = Sha256("b".repeat(64))
    private val origin = OriginLocator(FileIdentity("review.json", hash), "json:/review")
    private val review = ReviewEvidence(origin, "2026-10-16")
    private val packageId = ContentPackageIdentity("assessment-test", hash)
    private fun text(s: String): RichText = listOf(InlineContent.Text(s))
    internal fun question(id: String = "test", category: Category = Category.RULES): AssessmentQuestion {
        val options = (1..4).map { AssessmentOption(OptionId("$id-authored-$it"), text("Illustration"),
            AssessmentImageBinding(AssetId("$id-asset-$it"), NeutralImageDescription("Circle with $it visible dots", review))) }
        return AssessmentQuestion(QuestionRevisionKey(QuestionId(id), SemanticRevision("r1")), id, category,
            text("Which picture?"), null, options,
            AssessmentFeedback("SECRET-TARGET", "SECRET-MEANING", options[2].id, text("SECRET-EXPLANATION"), options.map {
                AssessmentOptionFeedback(it.id, text("SECRET-${it.id.value}"), "SECRET-CODE", "SECRET-LABEL", emptyList())
            }), QuestionRelationship(ContentId("M03-L02"), emptyList(), emptyList(), emptyList(), emptyList(),
                QuestionDisposition.REWRITE, "assessment-test"),
            AssessmentAcceptance(ScoringEligibility.ACCEPTED, review, listOf(review), emptyList(), emptyList()), origin)
    }
    @Test fun allTwentyFourPermutationsPreserveKeyAndFeedback() {
        val q = question()
        val positions = mutableSetOf<Int>()
        val orders = mutableSetOf<List<OptionId>>()
        repeat(1000) { seed ->
            val snapshot = q.snapshot(packageId, Random(seed))
            orders.add(snapshot.displayedOptionIds)
            positions.add(snapshot.displayedOptionIds.indexOf(q.feedback.correctOptionId))
            snapshot.displayedOptionIds.forEachIndexed { position, id ->
                assertEquals(id, snapshot.optionAt(position).id)
                assertTrue(snapshot.feedbackFor(id).explanation.assessmentText().endsWith(id.value))
                assertEquals(id == q.feedback.correctOptionId, snapshot.isCorrect(SnapshotAnswer(q.key, id)))
            }
        }
        assertEquals(24, orders.size)
        assertEquals(setOf(0, 1, 2, 3), positions)
    }
    @Test fun scoresRejectForeignOptionAndStaleRevision() {
        val s = question().snapshot(packageId)
        assertFailsWith<IllegalArgumentException> { s.isCorrect(SnapshotAnswer(s.question.key, OptionId("foreign"))) }
        assertFailsWith<IllegalArgumentException> { s.isCorrect(SnapshotAnswer(s.question.key.copy(revision = SemanticRevision("r2")), s.displayedOptionIds[0])) }
    }
    @Test fun immediateRevealRequiresConfirmationAndFeedbackFollowsDisplayedIdentity() {
        val q = question()
        var s = AssessmentSession(listOf(q.snapshot(packageId, Random(11))), Feedback.IMMEDIATE)
        val hidden = s.presentation()
        assertFalse(hidden.toString().contains("SECRET"))
        assertTrue(hidden.choices.all { it.correct == null && it.feedback == null })
        assertNull(s.score)
        s = s.answer(q.feedback.correctOptionId)
        assertTrue(s.presentation().explanation!!.contains("SECRET"))
        assertEquals(q.feedback.correctOptionId, s.presentation().choices.single { it.correct == true }.id)
        assertFalse(s.presentation().canConfirm)
        assertNull(s.score)
        assertEquals(1, s.next().score)
    }
    @Test fun endModeNeverRevealsEvenConfirmedAnswersUntilFinished() {
        val first = question("first")
        val second = question("second")
        var s = AssessmentSession(listOf(first.snapshot(packageId), second.snapshot(packageId)), Feedback.AT_END)
        s = s.answer(first.feedback.correctOptionId)
        assertFalse(s.presentation().toString().contains("SECRET"))
        assertFailsWith<IllegalArgumentException> { s.presentation(1) }
        s = s.next().answer(second.options[0].id)
        assertFalse(s.presentation().toString().contains("SECRET"))
        assertFailsWith<IllegalArgumentException> { s.presentation(0) }
        s = s.next()
        assertEquals(1, s.score)
        assertTrue(s.presentation(0).toString().contains("SECRET"))
        assertTrue(s.presentation(1).toString().contains("SECRET"))
        assertFailsWith<IllegalArgumentException> { s.answer(second.options[1].id) }
        assertFailsWith<IllegalArgumentException> { s.next() }
    }
    @Test fun confirmationAndSnapshotConsistencyAreGuarded() {
        val q = question()
        val snapshot = q.snapshot(packageId)
        val s = AssessmentSession(listOf(snapshot), Feedback.AT_END)
        assertFailsWith<IllegalArgumentException> { s.next() }
        assertFailsWith<IllegalArgumentException> { s.answer(OptionId("unknown")) }
        val answered = s.answer(q.options[0].id)
        assertFailsWith<IllegalArgumentException> { answered.answer(q.options[1].id) }
        assertFailsWith<IllegalArgumentException> { s.copy(finished = true) }
        assertFailsWith<IllegalArgumentException> { s.copy(snapshots = listOf(snapshot, snapshot)) }
        assertFailsWith<IllegalArgumentException> { s.copy(answers = listOf(SnapshotAnswer(q.key.copy(revision = SemanticRevision("r2")), q.options[0].id))) }
        assertFailsWith<IllegalArgumentException> { s.copy(snapshots = listOf(snapshot.copy(question = q.copy(acceptance = q.acceptance.copy(eligibility = ScoringEligibility.HELD))))) }
    }
    @Test fun duplicateVisualChoicesRejectedWhileEqualLearnerLabelsRemainValid() {
        val q = question()
        assertEquals(1, q.options.map { it.text }.distinct().size)
        assertFailsWith<IllegalArgumentException> { q.copy(options = q.options.mapIndexed { i, o -> if (i == 1) o.copy(image = q.options[0].image) else o }) }
        assertFailsWith<IllegalArgumentException> { NeutralImageDescription("  ", review) }
    }
    @Test fun selectionUsesAcceptedConceptsAndPinsPackageAndRevision() {
        val bank = Category.entries.flatMap { category -> (1..80).map { question("${category.name}-$it", category) } }
        for (size in 1..70) {
            val selected = AssessmentEngine.select(bank, size, packageId, Random(size))
            assertEquals(size, selected.size)
            assertEquals(size, selected.map { it.question.conceptId }.distinct().size)
            assertTrue(selected.all { it.packageIdentity == packageId && it.question.key.revision == SemanticRevision("r1") })
        }
        val held = bank.map { it.copy(acceptance = it.acceptance.copy(eligibility = ScoringEligibility.HELD)) }
        assertFailsWith<IllegalArgumentException> { AssessmentEngine.select(held, 1, packageId) }
    }
    @Test fun spokenMathSurvivesAndLinkTargetsAreNeverReadAsMetadata() {
        val rich = listOf(InlineContent.Math("x=2", "x equals two"), InlineContent.Link(text("source label"), TeachingLink.Internal(ContentTarget(ContentId("hidden-destination")))))
        assertEquals("x equals twosource label", rich.assessmentText())
    }
}
