package se.korkort

import kotlin.jvm.JvmInline
import kotlin.math.floor
import kotlin.random.Random

enum class Category(val title: String, val short: String, val quota: Int) {
    VEHICLE("Vehicle knowledge & maneuvering", "Vehicle knowledge", 7),
    ENVIRONMENT("Environment", "Environment", 5),
    SAFETY("Traffic safety", "Traffic safety", 16),
    RULES("Traffic rules", "Traffic rules", 32),
    PERSONAL("Personal conditions", "Personal conditions", 5)
}
data class Option(val text: String, val explanation: String, val image: String = "")
data class Question(val id: String, val concept: String, val category: Category, val prompt: String, val options: List<Option>, val correct: Int, val explanation: String, val page: Int, val source: String = "", val image: String = "") {
    fun shuffled(random: Random): Question {
        val order = options.indices.shuffled(random)
        return copy(options = order.map { options[it] }, correct = order.indexOf(correct))
    }
}
data class Topic(val title: String, val category: Category, val text: String, val page: Int)
enum class Feedback { IMMEDIATE, AT_END }
data class Allocation(val categories: Map<Category, Int>, val random: Int)
object QuizEngine {
    fun allocation(size: Int): Allocation {
        require(size in 1..70)
        val weights = Category.entries.map { it.quota } + 5
        val raw = weights.map { size * it / 70.0 }
        val counts = raw.map { floor(it).toInt() }.toMutableList()
        val order = raw.indices.sortedWith(compareByDescending<Int> { raw[it] - counts[it] }.thenBy { it })
        repeat(size - counts.sum()) { counts[order[it]]++ }
        return Allocation(Category.entries.associateWith { counts[it.ordinal] }, counts.last())
    }
    fun select(bank: List<Question>, size: Int, random: Random = Random.Default): List<Question> {
        val allocation = allocation(size)
        val selected = mutableListOf<Question>()
        val used = mutableSetOf<String>()
        fun pick(pool: List<Question>, count: Int) {
            val choices = pool.filter { it.concept !in used }.groupBy { it.concept }.values.shuffled(random)
            require(choices.size >= count) { "Not enough distinct learning topics" }
            choices.take(count).forEach { variants -> val q=variants.random(random); used.add(q.concept); selected.add(q.shuffled(random)) }
        }
        allocation.categories.forEach { (category,count) -> pick(bank.filter { it.category == category }, count) }
        pick(bank,allocation.random)
        return selected.shuffled(random)
    }
}
data class QuizSession(val questions: List<Question>, val feedback: Feedback, val answers: Map<String, Int> = emptyMap(), val index: Int = 0, val finished: Boolean = false) {
    val current get() = questions[index]
    val score get() = questions.count { answers[it.id] == it.correct }
    fun answer(option: Int): QuizSession {
        require(!finished && option in 0..3 && current.id !in answers)
        return copy(answers = answers + (current.id to option))
    }
    fun next(): QuizSession {
        require(current.id in answers && !finished)
        return if (index == questions.lastIndex) copy(finished = true) else copy(index = index + 1)
    }
}

// Migration contract only. The legacy bank/session above remains in use until its planned migration.
@JvmInline value class QuestionId(val value: String) {
    init { require(value.isNotBlank()) }
}
@JvmInline
value class OptionId(val value: String) {
    init { require(value.isNotBlank()) }
}

data class QuestionRevisionKey(val questionId: QuestionId, val revision: SemanticRevision)
enum class QuestionDisposition { RETAIN, REWRITE, REPLACE, REMOVE }
enum class ScoringEligibility { UNREVIEWED, HELD, ACCEPTED, RETIRED }

data class AssessmentHold(val id: String, val reason: String, val releaseCondition: String)

data class AssessmentAcceptance(
    val eligibility: ScoringEligibility,
    val contentReview: ReviewEvidence?,
    val descriptionReviews: List<ReviewEvidence>,
    val deliveryProof: List<ReviewEvidence>,
    val openHolds: List<AssessmentHold>,
) {
    init {
        if (eligibility == ScoringEligibility.ACCEPTED) {
            require(contentReview != null && openHolds.isEmpty())
        }
    }
}

data class QuestionReleaseBinding(
    val key: QuestionRevisionKey,
    val eligibility: ScoringEligibility,
)

data class QuestionRelationship(
    val primaryLessonId: ContentId,
    val relatedLessonIds: List<ContentId>,
    val referenceIds: List<ContentId>,
    val sourceIds: List<ContentId>,
    val sourceUses: List<SourceUse>,
    val disposition: QuestionDisposition,
    val contentVersion: String,
)

/** Separate from study alt text; the recorded review must establish physical-feature neutrality. */
data class NeutralImageDescription(val text: String, val review: ReviewEvidence)
data class AssessmentImageBinding(
    val assetId: AssetId,
    val neutralDescription: NeutralImageDescription?,
)

/** Pre-answer text/image only; code, meaning and option explanations live in feedback. */
data class AssessmentOption(
    val id: OptionId,
    val text: RichText,
    val image: AssessmentImageBinding?,
)
data class AssessmentOptionFeedback(
    val optionId: OptionId,
    val explanation: RichText,
    val signCode: String?,
    val englishLabel: String?,
    val sourceUses: List<SourceUse>,
)
data class AssessmentFeedback(
    val targetSignCode: String?,
    val englishLabel: String?,
    val correctOptionId: OptionId,
    val explanation: RichText,
    val optionFeedback: List<AssessmentOptionFeedback>,
)

/** New package contract; existing Question constructors and scoring are not adapted in 9A2. */
data class AssessmentQuestion(
    val key: QuestionRevisionKey,
    val conceptId: String,
    val category: Category,
    val prompt: RichText,
    val image: AssessmentImageBinding?,
    val options: List<AssessmentOption>,
    val feedback: AssessmentFeedback,
    val relationship: QuestionRelationship,
    val acceptance: AssessmentAcceptance,
    val origin: OriginLocator,
) {
    init {
        val ids = options.map { it.id }
        require(options.size == 4 && ids.distinct().size == 4)
        require(feedback.correctOptionId in ids)
        require(feedback.optionFeedback.map { it.optionId }.let { it.size == 4 && it.toSet() == ids.toSet() })
        if (acceptance.eligibility == ScoringEligibility.ACCEPTED) {
            require(listOfNotNull(image).plus(options.mapNotNull { it.image }).all { it.neutralDescription != null })
            require(relationship.disposition != QuestionDisposition.REMOVE)
        }
    }
}

data class QuestionPayload(val schemaVersion: Int, val questions: List<AssessmentQuestion>)

/** An ordered, versioned question snapshot; stored answers never refer to a current bank index. */
data class SessionQuestionSnapshot(
    val question: AssessmentQuestion,
    val packageIdentity: ContentPackageIdentity,
    val displayedOptionIds: List<OptionId>,
) {
    init {
        require(displayedOptionIds.size == 4 && displayedOptionIds.toSet() == question.options.map { it.id }.toSet())
    }
}
data class SnapshotAnswer(val question: QuestionRevisionKey, val selectedOptionId: OptionId)
