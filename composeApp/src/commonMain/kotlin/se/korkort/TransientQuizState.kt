package se.korkort

/** Every draft/expansion is scoped to an exact in-memory attempt, never just a question ID. */
data class PracticeQuestionToken(
    val sessionId: String,
    val key: QuestionRevisionKey,
    val packageIdentity: ContentPackageIdentity,
    val displayedOptionIds: List<OptionId>,
)
data class PinnedPractice(val id: String, val assessment: AssessmentSession) {
    init { require(id.isNotBlank()) }
    val token get() = assessment.current.let { PracticeQuestionToken(id,it.question.key,it.packageIdentity,it.displayedOptionIds) }
    val navigation get() = SessionNavigation(id,assessment.finished,assessment.presentation().explanation!=null)
}
data class PendingAnswer(val token: PracticeQuestionToken, val optionId: OptionId) {
    init { require(optionId in token.displayedOptionIds) }
}
enum class PracticeReviewFilter { ALL, INCORRECT, CORRECT }
data class PracticeReviewCursor(
    val sessionId: String,
    val filter: PracticeReviewFilter = PracticeReviewFilter.ALL,
    val row: Int = 0,
    val expanded: Set<QuestionRevisionKey> = emptySet(),
) { init { require(row>=0) } }
enum class PracticeRecovery { NONE, MISSING_QUIZ, MISSING_RESULT }

/** Pure, same-process state. No store, restoration/import API or package hot replacement. */
data class TransientQuizState(
    val countText: String = "70",
    val feedback: Feedback = Feedback.IMMEDIATE,
    val pinned: PinnedPractice? = null,
    val navigation: GuardedNavigation = GuardedNavigation(AppDestination.Home,null),
    val draft: PendingAnswer? = null,
    val review: PracticeReviewCursor? = null,
    val library: LibraryFilter = LibraryFilter(),
    val recovery: PracticeRecovery = PracticeRecovery.NONE,
    val pendingPin: PinnedPractice? = null,
    val attemptSerial: Long = 0,
) {
    init { require(attemptSerial>=0) }
    private fun active(): PinnedPractice {
        val p=requireNotNull(pinned)
        require(navigation.current==AppDestination.Quiz(p.id) && navigation.pending==null && !p.assessment.finished)
        return p
    }
    fun select(token: PracticeQuestionToken, optionId: OptionId): TransientQuizState {
        val p=active();require(token==p.token && p.assessment.currentAnswer==null)
        return copy(draft=PendingAnswer(token,optionId))
    }
    fun confirm(token: PracticeQuestionToken): TransientQuizState {
        val p=active();val answer=requireNotNull(draft)
        require(token==p.token && answer.token==token)
        val next=p.copy(assessment=p.assessment.answer(answer.optionId))
        return copy(pinned=next,draft=null,navigation=navigation.withSession(next.navigation),pendingPin=null)
    }
    fun nextQuestion(): TransientQuizState {
        val p=active();val next=p.copy(assessment=p.assessment.next())
        val destination=if(next.assessment.finished)AppDestination.Results(next.id) else AppDestination.Quiz(next.id)
        return copy(pinned=next,draft=null,review=null,pendingPin=null,recovery=PracticeRecovery.NONE,
            navigation=GuardedNavigation(destination,next.navigation))
    }
    fun reviewPositions(filter: PracticeReviewFilter = review?.filter ?: PracticeReviewFilter.ALL): List<Int> {
        val a=pinned?.assessment ?: return emptyList()
        if(!a.finished)return emptyList()
        return a.snapshots.indices.filter { i ->
            val correct=a.snapshots[i].isCorrect(a.answers[i])
            filter==PracticeReviewFilter.ALL || correct==(filter==PracticeReviewFilter.CORRECT)
        }
    }
    /** Filtered rows map back to the pinned snapshot index; an empty filter has no question. */
    fun reviewSnapshotPosition(): Int? {
        val cursor=review ?: return null
        if(cursor.sessionId!=pinned?.id)return null
        return reviewPositions(cursor.filter).getOrNull(cursor.row)
    }
    fun reviewPresentation(): AssessmentPresentation? = reviewSnapshotPosition()?.let{pinned!!.assessment.presentation(it)}
    fun openReview(questionId: QuestionId? = null): TransientQuizState {
        val p=pinned ?: return recoverMissing(PracticeRecovery.MISSING_RESULT)
        require(p.assessment.finished && navigation.pending==null)
        require(questionId==null || p.assessment.snapshots.any{it.question.key.questionId==questionId})
        var cursor=review?.takeIf{it.sessionId==p.id} ?: PracticeReviewCursor(p.id)
        if(questionId!=null){
            val visible=reviewPositions(cursor.filter)
            if(visible.none{p.assessment.snapshots[it].question.key.questionId==questionId})cursor=cursor.copy(filter=PracticeReviewFilter.ALL)
            cursor=cursor.copy(row=reviewPositions(cursor.filter).indexOfFirst{p.assessment.snapshots[it].question.key.questionId==questionId})
        }
        val rows=reviewPositions(cursor.filter)
        val valid=cursor.copy(row=cursor.row.coerceAtMost((rows.size-1).coerceAtLeast(0)),expanded=cursor.expanded.intersect(p.assessment.snapshots.map{it.question.key}.toSet()))
        val question=rows.getOrNull(valid.row)?.let{p.assessment.snapshots[it].question.key.questionId}
        return copy(review=valid,recovery=PracticeRecovery.NONE,
            navigation=navigation.copy(current=AppDestination.Review(p.id,question),session=p.navigation,pending=null,pendingSession=null,pendingNotice=null,notice=null,sourceToOpen=null),pendingPin=null)
    }
    fun filterReview(filter: PracticeReviewFilter): TransientQuizState {
        val p=requireNotNull(pinned);require(p.assessment.finished && navigation.current is AppDestination.Review)
        val cursor=(review ?: PracticeReviewCursor(p.id)).copy(filter=filter,row=0)
        return copy(review=cursor).openReview()
    }
    fun moveReview(row: Int): TransientQuizState {
        require(navigation.current is AppDestination.Review && row in reviewPositions().indices)
        return copy(review=requireNotNull(review).copy(row=row)).openReview()
    }
    fun expandReview(key: QuestionRevisionKey): TransientQuizState {
        val p=requireNotNull(pinned);require(p.assessment.finished && navigation.current is AppDestination.Review)
        require(p.assessment.snapshots.any{it.question.key==key})
        val cursor=requireNotNull(review)
        return copy(review=cursor.copy(expanded=if(key in cursor.expanded)cursor.expanded-key else cursor.expanded+key))
    }
    fun request(request: NavigationRequest, resolver: CanonicalResolver = canonicalResolver): Pair<TransientQuizState,NavigationDecision> {
        // A stale route must never silently discard a different, valid active attempt.
        val requestedId=when(val d=request.destination){is AppDestination.Quiz->d.sessionId;is AppDestination.Results->d.sessionId;is AppDestination.Review->d.sessionId;else->null}
        if(pinned!=null && requestedId!=null && requestedId!=pinned.id)
            return this to NavigationDecision.Denied("This session is unavailable.")
        val reviewTarget=request.destination as? AppDestination.Review
        if(reviewTarget?.questionId!=null && pinned?.assessment?.snapshots?.none{it.question.key.questionId==reviewTarget.questionId}==true)
            return this to NavigationDecision.Denied("This review question is unavailable.")
        val synced=navigation.copy(session=pinned?.navigation)
        val (nav,decision)=synced.request(request,resolver)
        if(decision is NavigationDecision.MissingSession) {
            if(pinned!=null){
                val safe=if(pinned.assessment.finished)AppDestination.Results(pinned.id) else AppDestination.Quiz(pinned.id)
                return copy(navigation=GuardedNavigation(safe,pinned.navigation),pendingPin=null,recovery=PracticeRecovery.NONE) to NavigationDecision.Denied("This session route is unavailable.")
            }
            val kind=if(request.destination is AppDestination.Quiz)PracticeRecovery.MISSING_QUIZ else PracticeRecovery.MISSING_RESULT
            return recoverMissing(kind) to decision
        }
        if(decision==NavigationDecision.Allow && request.destination is AppDestination.Review && request.intent!=NavigationIntent.SOURCE)
            return copy(navigation=nav,pendingPin=null).openReview((request.destination as AppDestination.Review).questionId) to decision
        return when(decision){
            NavigationDecision.Allow -> copy(navigation=nav,recovery=PracticeRecovery.NONE,pendingPin=null) to decision
            NavigationDecision.ConfirmDiscard -> copy(navigation=nav,pendingPin=pinned) to decision
            else -> this to decision
        }
    }
    /** Consume URL delivery once; opening the same source again remains a deliberate new effect. */
    fun takeSourceToOpen()=navigation.sourceToOpen to copy(navigation=navigation.copy(sourceToOpen=null))
    fun cancelExit()=copy(navigation=navigation.cancel(),pendingPin=null)
    fun discardExit(): TransientQuizState {
        require(navigation.pending!=null && pendingPin==pinned)
        return copy(navigation=navigation.discard(),pinned=null,draft=null,review=null,pendingPin=null,recovery=PracticeRecovery.NONE)
    }
    /** Only valid same-process preferences survive recovery; no missing result is fabricated. */
    internal fun recoverMissing(kind: PracticeRecovery): TransientQuizState {
        require(pinned==null) {"An existing attempt must use the shared navigation guard"}
        return copy(countText=if(countText.toIntOrNull() in 1..70)countText else "70",
            pinned=null,draft=null,review=null,pendingPin=null,recovery=kind,
            navigation=GuardedNavigation(AppDestination.QuizSetup,null))
    }
    fun showSetup()=if(recovery!=PracticeRecovery.NONE && pinned==null)copy(recovery=PracticeRecovery.NONE)else request(NavigationRequest(AppDestination.QuizSetup)).first
    fun libraryCategory(raw: String?)=copy(library=library.copy(category=Category.entries.firstOrNull{it.name==raw}))
}
