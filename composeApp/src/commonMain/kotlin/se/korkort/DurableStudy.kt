package se.korkort

import kotlinx.serialization.json.Json
import se.korkort.progress.*

/** Bridges only the authenticated accepted bank to durable, revision-pinned learner actions. */
internal class DurableStudy(val repository: ProgressRepository, val token: WriteToken, private val bank: PracticeBank) {
    init { require(bank.releaseAccepted && bank.identity==acceptedIdentity9J && bank.questions==acceptedQuestions9J) }
    val packageId = "${bank.identity.contentVersion}:${bank.identity.manifestSha256.value}"
    val catalog = ContentCatalog(packageId,readerModules.associate { it.id.value to it.lessonIds.map { id->id.value } },
        readerDocuments.filter { it.kind==DocumentKind.LESSON }.associate { it.id.value to it.revision.value },
        bank.questions.associate { it.key.questionId.value to it.key.revision.value })
    suspend fun initialize() { repository.setCatalog(token,catalog) }
    suspend fun start(state: TransientQuizState): TransientQuizState {
        repository.activeSession(token)?.let { return quizState(it.id) }
        val selected=state.startPractice(bank).pinned!!
        val id=repository.start(token,packageId,selected.assessment.feedbackMode==Feedback.AT_END,
            selected.assessment.snapshots.map { snap-> val q=snap.question
                QuestionSnapshot(q.key.questionId.value,q.key.revision.value,q.conceptId,snap.displayedOptionIds.map { it.value },q.feedback.correctOptionId.value,q.toString()) })
        return quizState(id)
    }
    suspend fun active(): PinnedPractice? = repository.activeSession(token)?.let { restore(it.id) }
    suspend fun restore(id: String): PinnedPractice {
        val (stored,answers)=repository.restore(token,id)
        require(stored.packageId==packageId) { "The saved exercise belongs to an earlier content version. End it to start again." }
        val snapshots=Json.decodeFromString<List<QuestionSnapshot>>(stored.snapshot).map { saved->
            val q=bank.questions.singleOrNull { it.key.questionId.value==saved.id && it.key.revision.value==saved.revision } ?: throw IllegalArgumentException("Saved question revision is unavailable")
            require(q.toString()==saved.contentJson && saved.options.toSet()==q.options.map { it.id.value }.toSet()) { "Saved question content is unavailable" }
            SessionQuestionSnapshot(q,bank.identity,saved.options.map(::OptionId))
        }
        val finished=stored.status=="completed"
        require(stored.status=="active" || finished)
        val index=if(finished)snapshots.lastIndex else repository.cursor(token,id)
        return PinnedPractice(id,AssessmentSession(snapshots,if(stored.deferred)Feedback.AT_END else Feedback.IMMEDIATE,
            answers.map { answer->SnapshotAnswer(snapshots[answer.position].question.key,OptionId(answer.selectedOption)) },index,finished))
    }
    suspend fun quizState(id: String): TransientQuizState {
        val p=restore(id)
        return TransientQuizState(pinned=p,navigation=GuardedNavigation(if(p.assessment.finished)AppDestination.Results(id) else AppDestination.Quiz(id),p.navigation))
    }
    suspend fun confirm(p: PinnedPractice, option: OptionId): TransientQuizState {
        val stored=repository.restore(token,p.id).first
        repository.confirm(token,p.id,stored.version,p.assessment.index,option.value,"${p.id}:${p.assessment.index}")
        return quizState(p.id)
    }
    suspend fun next(p: PinnedPractice): TransientQuizState {
        val stored=repository.restore(token,p.id).first
        if(stored.status!="completed") {
            if(p.assessment.index==p.assessment.snapshots.lastIndex) repository.finish(token,p.id,stored.version)
            else repository.advance(token,p.id,p.assessment.index,stored.version)
        }
        return quizState(p.id)
    }
    suspend fun endActive() {
        repository.activeSession(token)?.let { repository.finish(token,it.id,it.version,true) }
    }
}
