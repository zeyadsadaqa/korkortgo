package se.korkort

/** IDs resolve inside the app only. This is deliberately not a public URL/deep-link parser. */
enum class DestinationKind { CURRICULUM, REFERENCE_GROUP, SIGN, SOURCE }
data class CanonicalEntry(val id: ContentId, val title: String, val kind: DestinationKind, val blocks: Set<BlockId>)
sealed interface Resolution {
    data class Found(val target: ContentTarget, val entry: CanonicalEntry, val notice: String? = null) : Resolution
    data class Choices(val choices: List<Found>, val notice: String) : Resolution
    data class Unavailable(val message: String, val officialReferenceId: SourceReferenceId? = null, val related: List<ContentTarget> = emptyList()) : Resolution
}

class CanonicalResolver(
    entries: List<CanonicalEntry>,
    anchors: Map<ContentId, ContentTarget>,
    private val aliases: LegacyAliasPayload,
) {
    private val entries = entries.associateBy { it.id }
    private val anchors = anchors.toMap()
    private val tombstones = aliases.tombstones.associateBy { it.retiredId }
    init {
        require(this.entries.size == entries.size)
        require(this.entries.keys.intersect(this.anchors.keys).isEmpty())
        require(tombstones.keys.intersect(this.entries.keys + this.anchors.keys).isEmpty())
        require(aliases.aliases.map { it.lookup }.distinct().size == aliases.aliases.size)
        require(this.anchors.values.all { target ->
            val entry = this.entries[target.contentId]
            entry != null && (target.blockId == null || target.blockId in entry.blocks)
        })
    }
    fun canonical(target: ContentTarget): Resolution {
        val anchored = anchors[target.contentId]
        if (anchored != null) {
            // An anchor already names one exact block; an extra block must agree with it.
            if (target.blockId != null && target.blockId != anchored.blockId)
                return Resolution.Unavailable("The requested passage is unavailable.")
            return canonical(anchored)
        }
        val entry = entries[target.contentId]
        if (entry != null) {
            if (target.blockId != null && target.blockId !in entry.blocks)
                return Resolution.Found(ContentTarget(entry.id), entry, "The precise passage has moved. Showing its parent.")
            return Resolution.Found(target, entry)
        }
        val retired = tombstones[target.contentId] ?: return Resolution.Unavailable("This content is unavailable.")
        val replacements = retired.replacementIds.mapNotNull { id ->
            // Replacement offers do not recursively follow tombstones or guess a target.
            entries[id]?.let { Resolution.Found(ContentTarget(id), it, retired.reason) }
        }
        return when (replacements.size) {
            0 -> Resolution.Unavailable(retired.reason)
            1 -> Resolution.Choices(replacements, "This content was retired. ${retired.reason}")
            else -> Resolution.Choices(replacements, "Choose a reviewed replacement. ${retired.reason}")
        }
    }
    fun legacy(lookup: LegacyLookup): Resolution {
        val normalized = if (lookup is LegacyLookup.Chapter)
            lookup.copy(title = normalizeLegacyTitle(lookup.title)) else lookup
        val alias = aliases.aliases.singleOrNull { (if (it.lookup is LegacyLookup.Chapter) it.lookup.copy(title = normalizeLegacyTitle(it.lookup.title)) else it.lookup) == normalized }
            ?: return Resolution.Unavailable("This legacy link is unavailable.")
        return when (val outcome = alias.outcome) {
            is AliasOutcome.Content -> canonical(outcome.target)
            is AliasOutcome.Chooser -> {
                val choices = outcome.targets.map { canonical(it) }
                if (choices.any { it !is Resolution.Found }) Resolution.Unavailable("These legacy destinations are unavailable.")
                else Resolution.Choices(choices.filterIsInstance<Resolution.Found>(), "The material was reorganised. Choose related teaching.")
            }
            is AliasOutcome.Unavailable -> Resolution.Unavailable(outcome.message, outcome.officialReferenceId, outcome.related.filter { canonical(it) is Resolution.Found })
        }
    }
    /** An explicitly supplied unknown question never falls through to a page/title guess. */
    fun lookup(canonical: ContentTarget? = null, questionId: QuestionId? = null, legacy: LegacyLookup? = null): Resolution = when {
        canonical != null -> this.canonical(canonical)
        questionId != null -> this.legacy(LegacyLookup.Question(questionId))
        legacy != null -> this.legacy(legacy)
        else -> Resolution.Unavailable("No destination was supplied.")
    }
    companion object {
        fun normalizeLegacyTitle(title: String) = title.trim().lowercase().replace(Regex("\\s+"), " ")
    }
}

/** The eight shared navigation states, with the session/target carried in the pending action. */
sealed interface AppDestination {
    data object Home : AppDestination
    data object Library : AppDestination
    data class Content(val target: ContentTarget) : AppDestination
    data object QuizSetup : AppDestination
    data class Quiz(val sessionId: String) : AppDestination
    data class Results(val sessionId: String) : AppDestination
    data class Review(val sessionId: String, val questionId: QuestionId? = null) : AppDestination
    data object SignCatalogue : AppDestination
}
enum class NavigationIntent { GENERAL, RELATED_READING, SOURCE, IMAGE_VIEWER }
data class SessionNavigation(val id: String, val finished: Boolean, val answerRevealed: Boolean)
sealed interface NavigationDecision {
    data object Allow : NavigationDecision
    data object ConfirmDiscard : NavigationDecision
    data class Denied(val message: String) : NavigationDecision
    data class MissingSession(val recovery: AppDestination = AppDestination.QuizSetup) : NavigationDecision
}
object QuizNavigationGuard {
    fun decide(current: AppDestination, target: AppDestination, session: SessionNavigation?, intent: NavigationIntent = NavigationIntent.GENERAL): NavigationDecision {
        val requested = when (target) {
            is AppDestination.Quiz -> target.sessionId
            is AppDestination.Results -> target.sessionId
            is AppDestination.Review -> target.sessionId
            else -> null
        }
        if (requested != null && (session == null || requested != session.id)) return NavigationDecision.MissingSession()
        if ((target is AppDestination.Results || target is AppDestination.Review) && session?.finished != true)
            return NavigationDecision.Denied("Finish the test before opening results.")
        return exitDecision(current is AppDestination.Quiz && session?.finished == false,target==current,session?.answerRevealed==true,intent)
    }
    /** Also used by the eight legacy Page states while canonical view integration is staged. */
    fun exitDecision(unfinishedQuiz: Boolean, sameDestination: Boolean, answerRevealed: Boolean, intent: NavigationIntent = NavigationIntent.GENERAL): NavigationDecision {
        if (unfinishedQuiz) {
            if (intent == NavigationIntent.RELATED_READING && !answerRevealed)
                return NavigationDecision.Denied("Related reading is available after the answer is revealed.")
            if (intent == NavigationIntent.IMAGE_VIEWER && sameDestination) return NavigationDecision.Allow
            if (!sameDestination || intent == NavigationIntent.SOURCE) return NavigationDecision.ConfirmDiscard
        }
        return NavigationDecision.Allow
    }
}

data class ReadingPosition(val blockId: BlockId, val offsetPx: Int) {
    init { require(offsetPx >= 0) }
}
data class ReturnContext(val origin: ContentTarget, val position: ReadingPosition?, val focusId: String?)
data class RestoredContext(val resolution: Resolution, val position: ReadingPosition?, val focusId: String?)
fun CanonicalResolver.restore(context: ReturnContext, validFocusIds: Set<String>): RestoredContext {
    val resolved = canonical(context.origin)
    if (resolved !is Resolution.Found) return RestoredContext(resolved, null, null)
    val position = context.position?.takeIf { it.blockId in resolved.entry.blocks && resolved.notice == null }
    val focus = context.focusId?.takeIf { it in validFocusIds && resolved.notice == null }
    return RestoredContext(resolved, position, focus)
}

/** Full pending requests survive the discard prompt; cancellation changes no session or reading state. */
data class NavigationRequest(val destination: AppDestination, val intent: NavigationIntent = NavigationIntent.GENERAL, val returnContext: ReturnContext? = null)
data class GuardedNavigation(
    val current: AppDestination,
    val session: SessionNavigation?,
    val pending: NavigationRequest? = null,
    val returnContext: ReturnContext? = null,
) {
    fun request(request: NavigationRequest, resolver: CanonicalResolver): Pair<GuardedNavigation, NavigationDecision> {
        if(request.destination is AppDestination.Content && resolver.canonical(request.destination.target) !is Resolution.Found)
            return this to NavigationDecision.Denied("This content is unavailable.")
        val decision=QuizNavigationGuard.decide(current,request.destination,session,request.intent)
        return when(decision) {
            NavigationDecision.Allow -> copy(current=request.destination,pending=null,returnContext=request.returnContext) to decision
            NavigationDecision.ConfirmDiscard -> copy(pending=request) to decision
            else -> this to decision
        }
    }
    fun cancel()=copy(pending=null)
    fun discard(): GuardedNavigation {
        val request=requireNotNull(pending)
        return copy(current=request.destination,session=null,pending=null,returnContext=request.returnContext)
    }
}
