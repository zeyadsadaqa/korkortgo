package se.korkort

import android.app.UiAutomation
import android.content.Intent
import android.graphics.Bitmap
import android.os.Bundle
import android.os.SystemClock
import android.view.accessibility.AccessibilityNodeInfo as Node
import androidx.test.platform.app.InstrumentationRegistry
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Test
import org.junit.Assert.*
import java.io.File

/** Native AccessibilityNodeInfo actions, not Compose test semantics. Verification build only. */
class NativeReaderRouteTest {
    private val instrumentation=InstrumentationRegistry.getInstrumentation()
    private val ui=instrumentation.getUiAutomation(UiAutomation.FLAG_DONT_SUPPRESS_ACCESSIBILITY_SERVICES)
    private val folder=File(instrumentation.targetContext.filesDir,"native-reader-step1").apply{mkdirs()}
    private fun nodes():List<Node> {
        fun walk(n:Node):List<Node> = listOf(n)+(0 until n.childCount).flatMap{n.getChild(it)?.let(::walk).orEmpty()}
        return ui.rootInActiveWindow?.let(::walk).orEmpty()
    }
    private fun label(n:Node)=listOfNotNull(n.text?.toString(),n.contentDescription?.toString()).joinToString(" | ")
    private fun find(text:String)=nodes().firstOrNull{it.isVisibleToUser && !it.isEditable && (it.text?.toString()==text || it.contentDescription?.toString()==text)}
    private fun waitFor(message:String,condition:()->Boolean){val end=SystemClock.uptimeMillis()+10000;while(SystemClock.uptimeMillis()<end){if(condition())return;SystemClock.sleep(75)};dump("failure");error(message+"\n"+nodes().joinToString("\n",transform=::label))}
    private fun launch(mode:String,code:String="S1",scale:Float=1f,dark:Boolean=false){
        instrumentation.startActivitySync(Intent().setClassName(instrumentation.targetContext.packageName,"se.korkort.DeliveryProofActivity").addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK).putExtra("mode",mode).putExtra("code",code).putExtra("fontScale",scale).putExtra("dark",dark))
        instrumentation.waitForIdleSync();waitFor("App did not expose native nodes"){nodes().any{it.packageName==instrumentation.targetContext.packageName}}
    }
    private fun click(text:String){waitFor("Missing $text"){find(text)!=null};var n=find(text)!!;while(!n.isClickable && n.parent!=null)n=n.parent;assertTrue("Cannot activate $text",n.performAction(Node.ACTION_CLICK));instrumentation.waitForIdleSync()}
    private fun scrollTo(text:String,forward:Boolean=true){repeat(80){if(find(text)!=null)return;val scroll=nodes().firstOrNull{it.isScrollable && it.isVisibleToUser}?:error("No scroll container for $text");scroll.performAction(if(forward)Node.ACTION_SCROLL_FORWARD else Node.ACTION_SCROLL_BACKWARD);SystemClock.sleep(150)};dump("scroll-failure");error("Not reached: $text")}
    private fun dump(name:String){
        val rows=JSONArray();nodes().filter{it.packageName==instrumentation.targetContext.packageName}.forEach{n->val b=android.graphics.Rect();n.getBoundsInScreen(b);rows.put(JSONObject().put("label",label(n)).put("class",n.className).put("visible",n.isVisibleToUser).put("heading",n.isHeading).put("state_description",n.stateDescription).put("focused",n.isFocused).put("accessibility_focused",n.isAccessibilityFocused).put("selected",n.isSelected).put("checked",n.isChecked).put("bounds",b.toShortString()).put("actions",JSONArray(n.actionList.map{it.id})))}
        File(folder,"$name.json").writeText(rows.toString(2));ui.takeScreenshot()?.let{bitmap->File(folder,"$name.png").outputStream().use{bitmap.compress(Bitmap.CompressFormat.PNG,100,it)};bitmap.recycle()}
    }
    @Test fun librarySearchSurvivesLessonAndNativeSourceReturn(){
        launch("learning")
        waitFor("No native search field"){nodes().any{it.isEditable}}
        val title="Your route into driving"
        val input=nodes().first{it.isEditable};assertTrue(input.performAction(Node.ACTION_SET_TEXT,Bundle().apply{putCharSequence(Node.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE,title)}))
        click(title);waitFor("Reader title missing"){nodes().any{it.isHeading && it.text?.toString()==title}};dump("reader-opening")
        val doc=readerDocuments.single{it.id.value=="M01-L01"};val source=lessonSources(doc).first()
        scrollTo(source.title);click(source.title);waitFor("Source detail missing"){find("Back to Sources")!=null};dump("source-detail")
        scrollTo("Return to reading");click("Return to reading");waitFor("Source row not restored"){find("Back to Sources")==null && find(source.title)!=null}; waitFor("Source trigger did not regain native keyboard focus"){var n=find(source.title);var focused=false;while(n!=null){focused=focused || n.isFocused;n=n.parent};focused};dump("source-return")
        // Return to library through native scroll rather than replacing the route in test code.
        scrollTo("Learning library",forward=false)
        click("Learning library");waitFor("Search query was lost on native return"){nodes().any{it.isEditable && it.text?.toString()==title}};dump("library-return")
    }
    @Test fun unknownQuestionAndLegacyChooserNeverGuessReading(){
        launch("learning-question","unknown-question")
        waitFor("Missing unavailable state"){find("Content unavailable")!=null};dump("unknown-question")
        click("Open learning library");waitFor("Missing library recovery"){find("Search lessons")!=null || nodes().any{it.isEditable}}
        launch("learning-chapter","The foundations")
        waitFor("No legacy chooser"){find("Choose related teaching")!=null};dump("legacy-chooser")
        val choices=canonicalResolver.legacy(LegacyLookup.Chapter("legacy-app-4768933c3d9a","The foundations")) as Resolution.Choices
        click(choices.choices.first().entry.title);waitFor("Chooser did not open exact lesson"){find("Learning library")!=null};dump("chooser-destination")
    }
    @Test fun referenceBackAndNativeModalPreserveContext(){
        launch("learning-sign","B1",1.6f)
        scrollTo("Enlarge image");click("Enlarge image");waitFor("Native modal not opened"){find("Close")!=null};dump("reference-modal")
        click("Zoom in");waitFor("Zoom did not change"){nodes().any{label(it).contains("150%")}}
        click("Reset");waitFor("Reset did not fit"){nodes().any{label(it).contains("100%")}};click("Close")
        waitFor("Sign detail not restored"){find("Enlarge image")!=null};dump("reference-modal-return")
        scrollTo("‹ Road signs and reference",forward=false)
        click("‹ Road signs and reference");waitFor("Back must open reference catalogue, not library"){find("Search lessons")==null && nodes().none{it.isEditable} && nodes().any{label(it).contains(navigationReferenceGroups.first().title)}};dump("reference-back")
    }
    @Test fun pendingCandidateSelectionSurvivesNativeZoom(){
        launch("candidate","sign-recognise-A1")
        waitFor("Missing native radio options"){nodes().any{it.isCheckable}}
        val radio=nodes().first{it.isCheckable};val choiceLabel=label(radio);assertTrue(radio.performAction(Node.ACTION_CLICK))
        scrollTo("Enlarge option A image");click("Enlarge option A image");waitFor("No native modal"){find("Close")!=null};dump("candidate-modal")
        assertFalse(nodes().any{label(it).contains("Correct answer")});click("Zoom in");click("Reset");click("Close")
        waitFor("Native choice was lost"){nodes().any{label(it)==choiceLabel && (it.isChecked || it.isSelected)}};dump("candidate-return")
    }
    @Test fun nativeKnowledgeCheckRevealAndReadingNeighbours(){
        val doc=readerDocuments.first{d->d.kind==DocumentKind.LESSON && d.bodyBlocks.any{it.payload is BlockPayload.KnowledgeCheck}}
        val check=doc.bodyBlocks.first{it.payload is BlockPayload.KnowledgeCheck}.payload as BlockPayload.KnowledgeCheck
        val answer=doc.answerBlocks.single{it.metadata.id==check.answerId}.blocks.first().searchText()
        launch("learning",doc.id.value,1.6f)
        scrollTo("Show answer");assertFalse(nodes().any{label(it).contains(answer)});dump("answer-hidden")
        click("Show answer");waitFor("Authored answer was not revealed"){nodes().any{label(it).contains(answer)}};dump("answer-revealed")
        click("Hide answer");waitFor("Hidden answer remained accessible"){nodes().none{label(it).contains(answer)}}
        val next=readingNeighbours(doc.id).second!!;val nextTitle=readerDocuments.single{it.id==next}.title
        scrollTo("Next: $nextTitle");click("Next: $nextTitle");waitFor("Next used wrong reading order"){nodes().any{it.isHeading && it.text?.toString()==nextTitle}};dump("next-reading")
    }

    @Test fun allTwelveFaintAssetsHaveNativeDeliveryAndZoomProof() {
        val codes=listOf("S5","S6","S7","S11","S12","S13","T1","T2","T6","T8","T22","X8")
        for(dark in listOf(false,true)) for(scale in listOf(1f,1.6f)) for(code in codes) {
            launch("delivery",code,scale,dark)
            val description=requireNotNull(deliveryCandidate(code,"meaning").image).description
            waitFor("Missing exact $code illustration"){find(description)!=null}
            waitFor("Exact artwork still loading: $code"){nodes().none{label(it).contains("Loading image") || label(it).contains("Image unavailable")}}
            val name="faint-$code-${if(dark) "dark" else "light"}-$scale"
            dump("$name-inline")
            scrollTo("Enlarge image");dump("$name-option")
            click("Enlarge image");waitFor("Missing $code viewer"){find("Close")!=null}
            click("Zoom in");waitFor("Zoom did not enlarge $code"){nodes().any{label(it).contains("150%")}}
            dump("$name-zoom")
            click("Reset");waitFor("Reset did not fit $code"){nodes().any{label(it).contains("100%")}};click("Close")
            waitFor("Lost enlarge trigger for $code"){find("Enlarge image")!=null}
        }
    }
}
