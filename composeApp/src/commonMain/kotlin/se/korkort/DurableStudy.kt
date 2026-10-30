package se.korkort

import kotlinx.serialization.json.Json
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import se.korkort.resources.Res

import se.korkort.progress.*

internal class UnavailableExercise(message:String):IllegalArgumentException(message)

/** Bridges only the authenticated accepted bank to durable, revision-pinned learner actions. */
internal class DurableStudy(val repository: ProgressRepository, val token: WriteToken, internal val bank: PracticeBank,private val assetVerifier:suspend (AssetId)->Unit=::verifyResumeAsset) {
    init { require(bank.releaseAccepted && bank.identity==acceptedIdentity9J && bank.questions==acceptedQuestions9J) }
    val packageId = "${bank.identity.contentVersion}:${bank.identity.manifestSha256.value}"
    val catalog = ContentCatalog(packageId,readerModules.associate { it.id.value to it.lessonIds.map { id->id.value } },
        readerDocuments.filter { it.kind==DocumentKind.LESSON }.associate { it.id.value to it.revision.value },
        bank.questions.associate { it.key.questionId.value to it.key.revision.value })
    var invalidatedExercise=false
        private set
    private val checkedAssets=mutableSetOf<AssetId>()
    private val assetChecks=Mutex()
    private suspend fun checkAssets(questions:List<AssessmentQuestion>) = assetChecks.withLock {
        val ids=questions.flatMap{q->listOfNotNull(q.image?.assetId)+q.options.mapNotNull{it.image?.assetId}}.distinct()
        for(id in ids)if(id !in checkedAssets) {
            try{assetVerifier(id);checkedAssets.add(id)}catch(e:CancellationException){throw e}catch(e:IllegalArgumentException){throw UnavailableExercise("Saved artwork is unavailable")}
        }
    }
    suspend fun initialize() {repository.setCatalog(token,catalog);active()}

    fun pool(request:ExerciseRequest,records:StudyRecords)=exercisePool(bank,request,records,catalog)
    suspend fun start(state: TransientQuizState,request:ExerciseRequest=ExerciseRequest()): TransientQuizState {
        repository.activeSession(token)?.let { return quizState(it.id) }
        val records=repository.records(token)
        val size=state.countText.toIntOrNull() ?: error("Choose a number of questions")
        val selected=selectExercise(bank,request,records,catalog,size)
        checkAssets(selected.map{it.question})
        val id=repository.start(token,packageId,state.feedback==Feedback.AT_END,
            selected.map { snap-> val q=snap.question
                QuestionSnapshot(q.key.questionId.value,q.key.revision.value,q.conceptId,snap.displayedOptionIds.map { it.value },q.feedback.correctOptionId.value,q.toString()) },request.encode())
        return quizState(id,false).copy(countText=state.countText,feedback=state.feedback)
    }
    suspend fun validateImport(text:String):ProgressBackup {
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
            if(s.status=="active") {require(available){"Unfinished exercise content is unavailable"};checkAssets(snapshots.map{current.getValue(it.id to it.revision)})}
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
    suspend fun active(): PinnedPractice? {
        val session=repository.activeSession(token) ?: return null
        return try{restore(session.id)}catch(e:UnavailableExercise){
            repository.finish(token,session.id,session.version,true,listOf(StoreMetadata("unavailable:${session.id}","1")))
            invalidatedExercise=true;null
        }
    }
    suspend fun restore(id: String): PinnedPractice {
        val view=repository.sessionView(token,id)
        val stored=view.session;val answers=view.answers
        try {
        require(stored.packageId==packageId) { "The saved exercise belongs to an earlier content version. End it to start again." }
        val snapshots=Json.decodeFromString<List<QuestionSnapshot>>(stored.snapshot).map { saved->
            val q=bank.questions.singleOrNull { it.key.questionId.value==saved.id && it.key.revision.value==saved.revision } ?: throw IllegalArgumentException("Saved question revision is unavailable")
            require(q.toString()==saved.contentJson && saved.options.toSet()==q.options.map { it.id.value }.toSet()) { "Saved question content is unavailable" }
            SessionQuestionSnapshot(q,bank.identity,saved.options.map(::OptionId))
        }
        val finished=stored.status=="completed"
        require(stored.status=="active" || finished)
        checkAssets(snapshots.map{it.question})
        val index=if(finished)snapshots.lastIndex else view.cursor
        return PinnedPractice(id,AssessmentSession(snapshots,if(stored.deferred)Feedback.AT_END else Feedback.IMMEDIATE,
            answers.map { answer->SnapshotAnswer(snapshots[answer.position].question.key,OptionId(answer.selectedOption)) },index,finished),stored.version,view.paused)
        }catch(e:IllegalArgumentException){throw UnavailableExercise(e.message ?: "Saved exercise content is unavailable")}
    }
    suspend fun quizState(id: String,resume:Boolean=true): TransientQuizState {
        val stored=repository.restore(token,id).first
        if(resume && stored.status=="active"){assetChecks.withLock{checkedAssets.clear()};restore(id);repository.resume(token,id)}
        val p=restore(id)
        return TransientQuizState(pinned=p,navigation=GuardedNavigation(if(p.paused)AppDestination.QuizSetup else if(p.assessment.finished)AppDestination.Results(id) else AppDestination.Quiz(id),p.navigation))
    }
    suspend fun confirm(p: PinnedPractice, option: OptionId): TransientQuizState {
        repository.confirm(token,p.id,requireNotNull(p.storeVersion),p.assessment.index,option.value,"${p.id}:${p.assessment.index}")
        return quizState(p.id,false)
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
                repository.finish(token,p.id,requireNotNull(p.storeVersion),metadata=completed)
            }
            else repository.advance(token,p.id,p.assessment.index,requireNotNull(p.storeVersion))
        }
        return quizState(p.id,false)
    }
    suspend fun pause(p:PinnedPractice) {
        if(!p.assessment.finished)repository.pause(token,p.id,requireNotNull(p.storeVersion))
    }
    suspend fun endActive() {
        repository.activeSession(token)?.let { repository.finish(token,it.id,it.version,true) }
    }
}

@OptIn(org.jetbrains.compose.resources.ExperimentalResourceApi::class)
private suspend fun verifyResumeAsset(id:AssetId) {
    val asset=requireNotNull(navigationAssets.singleOrNull{it.id==id})
    val prefix="composeApp/src/commonMain/composeResources/"
    require(asset.bundled.path.startsWith(prefix) && asset.bundled.sha256==asset.original.sha256)
    val bytes=Res.readBytes(asset.bundled.path.removePrefix(prefix))
    require(assetSha256(bytes)==asset.bundled.sha256)
    if(asset.bundled.path.endsWith(".pdf"))require(decodedOfficialVector(asset.bundled.sha256)?.sourceSha256==asset.bundled.sha256)
}
