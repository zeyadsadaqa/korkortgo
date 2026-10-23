package se.korkort

import kotlin.random.Random

/** A release gate is explicit: the held 9J candidate cannot become a production start. */
data class PracticeBank(
    val identity: ContentPackageIdentity,
    val questions: List<AssessmentQuestion>,
    val releaseAccepted: Boolean,
)
data class PracticeStartCheck(val size: Int?, val errors: List<String>) {
    val allowed get() = size!=null && errors.isEmpty()
}

fun practiceStartCheck(countText: String, bank: PracticeBank, fixture: Boolean = false): PracticeStartCheck {
    val size=countText.toIntOrNull()?.takeIf{it in 1..70}
    val errors=mutableListOf<String>()
    if(size==null)errors.add("Choose a number from 1 to 70.")
    if(!fixture && !bank.releaseAccepted)errors.add("The question package is not accepted for release.")
    // A caller-supplied release flag or identity cannot authenticate a changed payload.
    // Synthetic model banks use the explicit internal fixture start, never the app route.
    if(!fixture && (bank.identity!=acceptedIdentity9J || bank.questions!=acceptedQuestions9J)) {
        errors.add("The question package does not match the accepted release.")
    }
    if(bank.questions.map{it.key.questionId}.distinct().size!=bank.questions.size)errors.add("Duplicate question identity.")
    val eligible=bank.questions.filter{it.acceptance.eligibility==ScoringEligibility.ACCEPTED}
    val concepts=eligible.groupBy{it.conceptId}
    // The current selector allocates categories in enum order. A concept spanning categories
    // could consume a later category's quota for some seed; reject rather than promise capacity.
    if(concepts.values.any{variants->variants.map{it.category}.distinct().size!=1})errors.add("A concept spans multiple categories.")
    if(size!=null){
        val allocation=QuizEngine.allocation(size)
        allocation.categories.forEach{(category,quota)->
            if(concepts.values.count{it.first().category==category}<quota)errors.add("Not enough accepted topics for ${category.title}.")
        }
        if(concepts.size<size)errors.add("Not enough accepted distinct topics for the full test and random slots.")
    }
    return PracticeStartCheck(size,errors)
}

private fun TransientQuizState.startChecked(bank: PracticeBank, random: Random, fixture: Boolean): TransientQuizState {
    require(navigation.current==AppDestination.QuizSetup && navigation.pending==null && recovery==PracticeRecovery.NONE)
    require(pinned?.assessment?.finished!=false) {"Finish or deliberately discard the active test first"}
    require(attemptSerial<Long.MAX_VALUE) {"Session identity exhausted; restart the process"}
    val nextSerial=attemptSerial+1
    val sessionId="practice-$nextSerial"
    require(pinned?.id!=sessionId) {"Session identity conflicts with the existing attempt"}
    val check=practiceStartCheck(countText,bank,fixture);require(check.allowed){check.errors.joinToString(" ")}
    val assessment=AssessmentSession(AssessmentEngine.select(bank.questions,check.size!!,bank.identity,random),feedback)
    val practice=PinnedPractice(sessionId,assessment)
    return copy(attemptSerial=nextSerial,pinned=practice,navigation=GuardedNavigation(AppDestination.Quiz(sessionId),practice.navigation),draft=null,review=null,pendingPin=null,recovery=PracticeRecovery.NONE)
}
fun TransientQuizState.startPractice(bank: PracticeBank, random: Random = Random.Default)=startChecked(bank,random,false)

/** Test-only call site, with the same eligibility/capacity/state checks; never wired to production UI. */
internal fun TransientQuizState.startPracticeFixture(bank: PracticeBank, random: Random = Random.Default)=startChecked(bank,random,true)

/** Model a normal process restart: there is no durable attempt or preference restoration. */
fun TransientQuizState.restartPracticeProcess()=TransientQuizState()

/** Uses the actual 9J release decision; currently false. No activation is implied. */
internal val candidatePracticeBank9M by lazy { PracticeBank(candidateIdentity9J,candidateQuestions9J,candidateReleaseAccepted9J) }
