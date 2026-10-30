package se.korkort

import kotlin.random.Random

/** Only authored identities are shuffled. Feedback and semantic revisions stay attached. */
fun AssessmentQuestion.snapshot(packageIdentity: ContentPackageIdentity, random: Random = Random.Default) =
    SessionQuestionSnapshot(this, packageIdentity, options.map { it.id }.shuffled(random))

fun SessionQuestionSnapshot.optionAt(position: Int): AssessmentOption =
    question.options.single { it.id == displayedOptionIds[position] }

fun SessionQuestionSnapshot.feedbackFor(optionId: OptionId): AssessmentOptionFeedback {
    require(optionId in displayedOptionIds)
    return question.feedback.optionFeedback.single { it.optionId == optionId }
}

fun SessionQuestionSnapshot.isCorrect(answer: SnapshotAnswer): Boolean {
    require(answer.question == question.key && answer.selectedOptionId in displayedOptionIds)
    return answer.selectedOptionId == question.feedback.correctOptionId
}

/** This selector is the scored entry point. Fixtures can use snapshot() without activating a bank. */
object AssessmentEngine {
    fun select(bank: List<AssessmentQuestion>, size: Int, packageIdentity: ContentPackageIdentity,
               random: Random = Random.Default, answered: Set<String> = emptySet()): List<SessionQuestionSnapshot> {
        require(bank.map { it.key.questionId }.distinct().size == bank.size)
        val eligible = bank.filter { it.acceptance.eligibility == ScoringEligibility.ACCEPTED }
        val result = mutableListOf<AssessmentQuestion>()
        val used = mutableSetOf<String>()
        fun pick(pool: List<AssessmentQuestion>, count: Int) {
            val groups = pool.filter { it.conceptId !in used }.groupBy { it.conceptId }.values.shuffled(random)
            require(groups.size >= count) { "Not enough accepted distinct learning topics" }
            groups.take(count).forEach { group ->
                val question = group.filter { it.key.questionId.value !in answered }.ifEmpty { group }.random(random)
                used.add(question.conceptId)
                result.add(question)
            }
        }
        val allocation = QuizEngine.allocation(size)
        allocation.categories.forEach { (category, count) -> pick(eligible.filter { it.category == category }, count) }
        pick(eligible, allocation.random)
        return result.shuffled(random).map { it.snapshot(packageIdentity, random) }
    }
}

/** Deliberate confirmation stores an authored ID against the exact revision; selection alone never reveals. */
data class AssessmentSession(
    val snapshots: List<SessionQuestionSnapshot>,
    val feedbackMode: Feedback,
    val answers: List<SnapshotAnswer> = emptyList(),
    val index: Int = 0,
    val finished: Boolean = false,
) {
    init {
        require(snapshots.isNotEmpty() && index in snapshots.indices)
        require(snapshots.all { it.question.acceptance.eligibility == ScoringEligibility.ACCEPTED })
        require(snapshots.map { it.question.key.questionId }.distinct().size == snapshots.size)
        require(snapshots.map { it.packageIdentity }.distinct().size == 1)
        require(answers.size == index + if (finished || answers.any { it.question == snapshots[index].question.key }) 1 else 0)
        require(answers.map { it.question } == snapshots.take(answers.size).map { it.question.key })
        answers.forEachIndexed { position, answer -> snapshots[position].isCorrect(answer) }
        require(!finished || index == snapshots.lastIndex && answers.size == snapshots.size)
    }
    val current get() = snapshots[index]
    val currentAnswer get() = answers.singleOrNull { it.question == current.question.key }
    val score: Int? get() = if (finished) snapshots.zip(answers).count { (q, a) -> q.isCorrect(a) } else null
    fun answer(optionId: OptionId): AssessmentSession {
        require(!finished && currentAnswer == null && optionId in current.displayedOptionIds)
        return copy(answers = answers + SnapshotAnswer(current.question.key, optionId))
    }
    fun next(): AssessmentSession {
        require(!finished && currentAnswer != null)
        return if (index == snapshots.lastIndex) copy(finished = true) else copy(index = index + 1)
    }
    fun presentation(position: Int = index): AssessmentPresentation {
        require(position in snapshots.indices && (finished || position == index))
        val snapshot = snapshots[position]
        val answer = answers.singleOrNull { it.question == snapshot.question.key }
        val revealed = answer != null && (feedbackMode == Feedback.IMMEDIATE || finished)
        return snapshot.presentation(answer, revealed, !finished && position == index && answer == null)
    }
}

/** UI-safe projection. No code, key, correctness, source URL, study caption or explanation before reveal. */
data class AssessmentImagePresentation(val assetId: AssetId, val description: String)
data class AssessmentChoicePresentation(
    val id: OptionId, val letter: String, val text: String, val image: AssessmentImagePresentation?,
    val selected: Boolean, val correct: Boolean?, val feedback: String?,
)
data class AssessmentPresentation(
    val key: QuestionRevisionKey, val prompt: String, val image: AssessmentImagePresentation?,
    val choices: List<AssessmentChoicePresentation>, val canConfirm: Boolean,
    val explanation: String?, val targetLabel: String?, val targetCode: String?,
)

internal fun RichText.assessmentText(): String = joinToString("") {
    when (it) {
        is InlineContent.Text -> it.text
        is InlineContent.Emphasis -> it.children.assessmentText()
        is InlineContent.Strong -> it.children.assessmentText()
        is InlineContent.Link -> it.label.assessmentText()
        is InlineContent.Math -> it.spokenText
    }
}

private fun AssessmentImageBinding.presentation(): AssessmentImagePresentation {
    val description = requireNotNull(neutralDescription) { "Reviewed physical description required" }
    return AssessmentImagePresentation(assetId, description.text)
}

// Also used by isolated delivery verification. Projection does not create a scored session.
internal fun SessionQuestionSnapshot.presentation(answer: SnapshotAnswer?, revealed: Boolean, canConfirm: Boolean): AssessmentPresentation {
    answer?.let { isCorrect(it) } // Reject stale revisions/foreign IDs even in an unscored fixture.
    return AssessmentPresentation(question.key, question.prompt.assessmentText(), question.image?.presentation(),
        displayedOptionIds.indices.map { position ->
            val option = optionAt(position)
            val feedback = if (revealed) feedbackFor(option.id) else null
            AssessmentChoicePresentation(option.id, ('A' + position).toString(), option.text.assessmentText(),
                option.image?.presentation(), answer?.selectedOptionId == option.id,
                if (revealed) option.id == question.feedback.correctOptionId else null,
                feedback?.let { listOfNotNull(it.signCode, it.englishLabel, it.explanation.assessmentText()).joinToString(" · ") })
        }, canConfirm, if (revealed) question.feedback.explanation.assessmentText() else null,
        if (revealed) question.feedback.englishLabel else null, if (revealed) question.feedback.targetSignCode else null)
}
