package se.korkort
import kotlin.test.*

class NavigationTest {
    private val resolver get() = canonicalResolver
    @Test fun everyPublishedDestinationAndBlockResolvesExactly() {
        assertEquals(1123,canonicalEntries.size+canonicalAnchors.size)
        canonicalEntries.forEach { entry ->
            assertEquals(entry,(resolver.canonical(ContentTarget(entry.id)) as Resolution.Found).entry)
            entry.blocks.forEach { block -> assertEquals(ContentTarget(entry.id,block),(resolver.canonical(ContentTarget(entry.id,block)) as Resolution.Found).target) }
        }
        canonicalAnchors.forEach { (id,target) -> assertEquals(target,(resolver.canonical(ContentTarget(id)) as Resolution.Found).target) }
        assertTrue(resolver.canonical(ContentTarget(ContentId("unknown"))) is Resolution.Unavailable)
    }
    @Test fun allFrozenAliasesResolveWithoutGuessing() {
        assertEquals(1921,navigationAliases.aliases.size)
        assertTrue(navigationAliases.tombstones.isEmpty())
        navigationAliases.aliases.forEach { alias ->
            when(val expected=alias.outcome) {
                is AliasOutcome.Content -> assertEquals(expected.target,(resolver.legacy(alias.lookup) as Resolution.Found).target)
                is AliasOutcome.Chooser -> assertEquals(expected.targets,(resolver.legacy(alias.lookup) as Resolution.Choices).choices.map { it.target })
                is AliasOutcome.Unavailable -> assertEquals(expected.message,(resolver.legacy(alias.lookup) as Resolution.Unavailable).message)
            }
        }
        val ns="legacy-app-4768933c3d9a"
        assertEquals(ContentId("M04-L03"),(resolver.lookup(questionId=QuestionId("situation-017"),legacy=LegacyLookup.Page(ns,46)) as Resolution.Found).target.contentId)
        assertEquals(ContentId("M04-L01"),(resolver.lookup(questionId=QuestionId("situation-103"),legacy=LegacyLookup.Page(ns,46)) as Resolution.Found).target.contentId)
        assertTrue(resolver.lookup(questionId=QuestionId("unknown"),legacy=LegacyLookup.Page(ns,46)) is Resolution.Unavailable)
        assertTrue(resolver.legacy(LegacyLookup.Page("foreign",46)) is Resolution.Unavailable)
        assertTrue(resolver.legacy(LegacyLookup.Page(ns,13)) is Resolution.Unavailable)
        assertTrue(resolver.legacy(LegacyLookup.Page(ns,999)) is Resolution.Unavailable)
        assertTrue(resolver.legacy(LegacyLookup.Sign(ns,"f31a")) is Resolution.Unavailable)
        for(code in listOf("SIG16","SIG17","SIG18")) {
            val missing=resolver.legacy(LegacyLookup.Sign(ns,code)) as Resolution.Unavailable
            val reference=navigationSources.references.single { it.id==missing.officialReferenceId }
            assertTrue(reference.url.startsWith("https://www.transportstyrelsen.se/"))
            assertEquals(listOf(ContentTarget(ContentId("M03-L02"))),missing.related)
        }
        assertEquals(resolver.legacy(LegacyLookup.Chapter(ns,"The foundations")),resolver.legacy(LegacyLookup.Chapter(ns,"  THE   FOUNDATIONS  ")))
    }
    @Test fun restoreValidatesParentBlockPositionAndFocus() {
        val entry=canonicalEntries.first { it.blocks.isNotEmpty() };val block=entry.blocks.first()
        val context=ReturnContext(ContentTarget(entry.id,block),ReadingPosition(block,42),"enlarge")
        val restored=resolver.restore(context,setOf("enlarge"))
        assertEquals(context.position,restored.position);assertEquals("enlarge",restored.focusId)
        val moved=resolver.restore(context.copy(origin=ContentTarget(entry.id,BlockId("gone"))),setOf("enlarge"))
        assertNotNull((moved.resolution as Resolution.Found).notice);assertNull(moved.position);assertNull(moved.focusId)
        val badPosition=resolver.restore(context.copy(position=ReadingPosition(BlockId("gone"),100)),emptySet())
        assertNull(badPosition.position);assertNull(badPosition.focusId)
        val unknown=resolver.restore(context.copy(origin=ContentTarget(ContentId("unknown"))),setOf("enlarge"))
        assertTrue(unknown.resolution is Resolution.Unavailable);assertNull(unknown.position)
    }
    @Test fun retiredNoneOneAndManyOfferOnlyReviewedChoices() {
        val origin=navigationAliases.aliases.first().origin;val id=ContentId("retired")
        for(count in 0..2) {
            val replacement=canonicalEntries.take(count).map { it.id }
            val r=CanonicalResolver(canonicalEntries,canonicalAnchors,LegacyAliasPayload(1,emptyList(),listOf(ContentTombstone(id,replacement,"Reviewed retirement",ReviewEvidence(origin,null)))))
            val result=r.canonical(ContentTarget(id))
            if(count==0)assertTrue(result is Resolution.Unavailable) else assertEquals(replacement,(result as Resolution.Choices).choices.map { it.target.contentId })
        }
    }
    @Test fun allEightStatesUseTheSameGuardAndPreservePendingTargets() {
        val session=SessionNavigation("session",false,false)
        val states=listOf(AppDestination.Home,AppDestination.Library,AppDestination.Content(ContentTarget(ContentId("sign-B1"))),AppDestination.QuizSetup,AppDestination.Quiz("session"),AppDestination.Results("session"),AppDestination.Review("session"),AppDestination.SignCatalogue)
        assertEquals(8,states.size)
        states.forEach { current -> states.forEach { target ->
            val d=QuizNavigationGuard.decide(current,target,session)
            when {
                target is AppDestination.Results || target is AppDestination.Review -> assertTrue(d is NavigationDecision.Denied)
                current is AppDestination.Quiz && target!=current -> assertEquals(NavigationDecision.ConfirmDiscard,d)
                else -> assertEquals(NavigationDecision.Allow,d)
            }
        } }
        assertTrue(QuizNavigationGuard.decide(AppDestination.Home,AppDestination.Results("missing"),null) is NavigationDecision.MissingSession)
        assertTrue(QuizNavigationGuard.decide(AppDestination.Quiz("session"),states[2],session,NavigationIntent.RELATED_READING) is NavigationDecision.Denied)
        assertEquals(NavigationDecision.ConfirmDiscard,QuizNavigationGuard.decide(AppDestination.Quiz("session"),states[2],session.copy(answerRevealed=true),NavigationIntent.RELATED_READING))
        assertEquals(NavigationDecision.Allow,QuizNavigationGuard.decide(AppDestination.Quiz("session"),AppDestination.Quiz("session"),session,NavigationIntent.IMAGE_VIEWER))
    }
    @Test fun cancellationPreservesSessionAndDiscardKeepsExactPendingReturn() {
        val session=SessionNavigation("live",false,true)
        val entry=canonicalEntries.first {it.blocks.isNotEmpty()};val block=entry.blocks.first()
        val origin=ReturnContext(ContentTarget(entry.id,block),ReadingPosition(block,17),"enlarge")
        val start=GuardedNavigation(AppDestination.Quiz("live"),session,returnContext=origin)
        val request=NavigationRequest(AppDestination.Content(ContentTarget(ContentId("sign-B1"))),NavigationIntent.RELATED_READING,origin)
        val (pending,decision)=start.request(request,resolver)
        assertEquals(NavigationDecision.ConfirmDiscard,decision);assertEquals(request,pending.pending)
        assertEquals(start,pending.cancel())
        val accepted=pending.discard()
        assertEquals(request.destination,accepted.current);assertEquals(origin,accepted.returnContext);assertNull(accepted.session)
        val sourceDecision=QuizNavigationGuard.decide(start.current,start.current,session,NavigationIntent.SOURCE)
        assertEquals(NavigationDecision.ConfirmDiscard,sourceDecision)
    }

}
