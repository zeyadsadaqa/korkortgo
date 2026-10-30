package se.korkort

import kotlinx.serialization.json.Json
import se.korkort.progress.*

/** Bridges only the authenticated accepted bank to durable, revision-pinned learner actions. */
internal class DurableStudy(val repository: ProgressRepository, val token: WriteToken, internal val bank: PracticeBank) {
    init { require(bank.releaseAccepted && bank.identity==acceptedIdentity9J && bank.questions==acceptedQuestions9J) }
    val packageId = "${bank.identity.contentVersion}:${bank.identity.manifestSha256.value}"
    val catalog = ContentCatalog(packageId,readerModules.associate { it.id.value to it.lessonIds.map { id->id.value } },
        readerDocuments.filter { it.kind==DocumentKind.LESSON }.associate { it.id.value to it.revision.value },
        bank.questions.associate { it.key.questionId.value to it.key.revision.value })
    suspend fun initialize() { repository.setCatalog(token,catalog) }
    fun pool(request:ExerciseRequest,records:StudyRecords)=exercisePool(bank,request,records,catalog)
    suspend fun start(state: TransientQuizState,request:ExerciseRequest=ExerciseRequest()): TransientQuizState {
        repository.activeSession(token)?.let { return quizState(it.id) }
        val records=repository.records(token)
        val size=state.countText.toIntOrNull() ?: error("Choose a number of questions")
        val selected=selectExercise(bank,request,records,catalog,size)
        val id=repository.start(token,packageId,state.feedback==Feedback.AT_END,
            selected.map { snap-> val q=snap.question
                QuestionSnapshot(q.key.questionId.value,q.key.revision.value,q.conceptId,snap.displayedOptionIds.map { it.value },q.feedback.correctOptionId.value,q.toString()) },request.encode())
        return quizState(id).copy(countText=state.countText,feedback=state.feedback)
    }
    fun validateImport(text:String):ProgressBackup {
        val backup=decodeProgressBackup(text)
        val current=bank.questions.associateBy{it.key.questionId.value to it.key.revision.value}
        backup.records.sessions.forEach { s->
            val snapshots=Json.decodeFromString<List<QuestionSnapshot>>(s.snapshot)
            var available=s.packageId==packageId
            snapshots.forEach {q->
                val authored=current[q.id to q.revision]
                if(authored!=null)require(q.contentJson==authored.toString() && q.correctOption==authored.feedback.correctOptionId.value && q.concept==authored.conceptId && q.options.toSet()==authored.options.map{it.id.value}.toSet()) {"Question content does not match the accepted bank"}
                else { require(catalog.questions[q.id]!=q.revision);available=false }
            }
            if(s.status=="active")require(available){"Unfinished exercise content is unavailable"}
            ExerciseRequest.decode(backup.records.value("mode:${s.id}"))
        }
        backup.records.lessons.forEach {require(it.lessonId in catalog.lessons){"Unknown teaching lesson"}}
        backup.records.events.forEach {event->
            if(event.kind=="read" || event.kind=="unread")require(event.target in catalog.lessons)
            else require(backup.records.sessions.any{it.id==event.target && it.status==event.kind})
        }
        backup.records.metadata.filter{it.key.startsWith("opened:") || it.key.startsWith("readOrder:")}.forEach{require(it.key.substringAfter(':') in catalog.lessons)}
        return backup
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
            if(p.assessment.index==p.assessment.snapshots.lastIndex) {
                val records=repository.records(token)
                val completed=mutableListOf<StoreMetadata>()
                val request=ExerciseRequest.decode(records.value("mode:${p.id}"))
                if(request.mode==ExerciseMode.REVIEW)completed.add(StoreMetadata("reviewDone",(records.attempts.maxOfOrNull{it.sequence} ?: 0).toString()))
                if(request.mode==ExerciseMode.CHAPTER) {
                    val ids=readerModules.single{it.id.value==request.chapter}.lessonIds.map{it.value}
                    completed.add(StoreMetadata("chapterPractice:${request.chapter}",(ids.maxOfOrNull{id->records.value("readOrder:$id")?.toLongOrNull() ?: (records.events.filter{it.kind=="read" && it.target==id}.maxOfOrNull{it.occurredAt} ?: 0)} ?: 0).toString()))
                }
                repository.finish(token,p.id,stored.version,metadata=completed)
            }
            else repository.advance(token,p.id,p.assessment.index,stored.version)
        }
        return quizState(p.id)
    }
    suspend fun endActive() {
        repository.activeSession(token)?.let { repository.finish(token,it.id,it.version,true) }
    }
}
