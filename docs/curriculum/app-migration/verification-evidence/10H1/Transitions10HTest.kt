package se.korkort
import kotlin.test.*
class Transitions10HTest {
 @Test fun actualTransitionsReadingEdgesAndValidatedReturns() {
  val states=listOf(AppDestination.Home,AppDestination.Library,AppDestination.Content(ContentTarget(ContentId("M03-L02"))),AppDestination.QuizSetup,AppDestination.Quiz("accepted-attempt"),AppDestination.Results("accepted-attempt"),AppDestination.Review("accepted-attempt"),AppDestination.SignCatalogue)
  val matrix=listOf(false,true).flatMap{finished->states.flatMap{from->states.map{to->
   val session=SessionNavigation("accepted-attempt",finished,finished)
   val expected=when{!finished&&(to is AppDestination.Results||to is AppDestination.Review)->"denied";!finished&&from is AppDestination.Quiz&&to!=from->"confirm_discard";else->"allow"}
   val start=GuardedNavigation(from,session)
   val (after,decision)=start.request(NavigationRequest(to),canonicalResolver)
   val actual=when(decision){NavigationDecision.Allow->"allow";NavigationDecision.ConfirmDiscard->"confirm_discard";is NavigationDecision.Denied->"denied";is NavigationDecision.MissingSession->"missing_session"}
   assertEquals(expected,actual)
   when(actual){"allow"->assertEquals(to,after.current);"confirm_discard"->{assertEquals(to,after.pending!!.destination);assertEquals(start,after.cancel())};"denied"->assertEquals(start,after)}
   mapOf("finished" to finished,"from" to from,"to" to to,"expected" to expected,"actual" to actual)
  }}}
  val edges=readerOrder.map{id->val n=readingNeighbours(id);mapOf("id" to id,"previous" to n.first,"next" to n.second)}
  assertEquals(60,edges.size);assertEquals(null to null,readingNeighbours(ContentId("appendix-A")))
  val returns=canonicalEntries.filter{it.blocks.isNotEmpty()}.flatMap{entry->entry.blocks.map{block->
   val context=ReturnContext(ContentTarget(entry.id,block),ReadingPosition(block,37),"valid-trigger")
   val restored=canonicalResolver.restore(context,setOf("valid-trigger"))
   assertEquals(context.position,restored.position);assertEquals(context.focusId,restored.focusId)
   val routes=canonicalEntries.groupBy{it.kind}.values.map{it.first()}.map{dest->
    val nav=GuardedNavigation(AppDestination.Library,null).request(NavigationRequest(AppDestination.Content(ContentTarget(dest.id)),returnContext=context),canonicalResolver).first
    assertEquals(context,nav.returnContext);assertEquals(AppDestination.Content(ContentTarget(dest.id)),nav.current)
    mapOf("kind" to dest.kind,"target" to dest.id)
   }
   mapOf("context" to context,"restored" to restored,"routes" to routes)
  }}
  Proof10H.write("10H1","navigation-transition-results.json",mapOf("identity" to acceptedIdentity9J,"scope" to "compiled production navigation model; not native lifecycle proof","states" to states,"transitions" to matrix,"validated_returns" to returns))
  Proof10H.write("10H1","reading-edge-results.json",mapOf("edges" to edges,"unknown_or_appendix_neighbours" to readingNeighbours(ContentId("appendix-A"))).let{it-mapOf<String,Any>().keys})
 }
}
