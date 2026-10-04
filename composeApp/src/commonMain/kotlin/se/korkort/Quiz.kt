package se.korkort

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
