package se.korkort
import kotlin.test.*
import kotlin.random.Random
class QuizTest {
 @Test fun fullTestAllocation() { val a=QuizEngine.allocation(70); assertEquals(listOf(7,5,16,32,5),Category.entries.map { a.categories[it] }); assertEquals(5,a.random) }
 @Test fun everyLengthAndSeed() { for(n in 1..70) for(seed in 0..9) { val q=QuizEngine.select(questionBank,n,Random(seed)); assertEquals(n,q.size); assertEquals(n,q.map { it.concept }.distinct().size); assertTrue(q.all { it.options.size==4 && it.correct in 0..3 }); val a=QuizEngine.allocation(n); a.categories.forEach { (c,k) -> assertTrue(q.count { it.category==c }>=k) } } }
 @Test fun bankIntegrity() { assertTrue(questionBank.size>=1000); assertEquals(questionBank.size,questionBank.map { it.id }.distinct().size); assertEquals(questionBank.size,questionBank.map { it.prompt }.distinct().size); questionBank.forEach { q -> assertEquals(4,q.options.map { it.text }.distinct().size); assertTrue(q.options.all { it.explanation.isNotBlank() }); assertTrue(q.page in 1..367) } }
 @Test fun answerAndFinishAreGuarded() { var s=QuizSession(QuizEngine.select(questionBank,1,Random(5)),Feedback.AT_END); assertFailsWith<IllegalArgumentException> { s.next() }; s=s.answer(s.current.correct); assertEquals(1,s.score); assertFailsWith<IllegalArgumentException> { s.answer(0) }; s=s.next(); assertTrue(s.finished); assertFailsWith<IllegalArgumentException> { s.answer(0) } }
 @Test fun shufflingPreservesAnswer() { val q=questionBank.first(); repeat(30) { assertEquals(q.options[q.correct],q.shuffled(Random(it)).let { it.options[it.correct] }) } }
 @Test fun invalidCountsRejected() { assertFailsWith<IllegalArgumentException> { QuizEngine.allocation(0) }; assertFailsWith<IllegalArgumentException> { QuizEngine.allocation(71) } }
}
