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
        ui.clearCache()
        fun walk(n:Node):List<Node> = listOf(n)+(0 until n.childCount).flatMap{n.getChild(it)?.let(::walk).orEmpty()}
        return ui.rootInActiveWindow?.also {it.refresh()}?.let(::walk).orEmpty()
    }
    private fun label(n:Node)=listOfNotNull(n.text?.toString(),n.contentDescription?.toString()).joinToString(" | ")
    private fun find(text:String)=nodes().firstOrNull{it.isVisibleToUser && (it.text?.toString()?.trim()?.replace(Regex("\\s+")," ")==text.trim().replace(Regex("\\s+")," ") || it.contentDescription?.toString()==text)}
    private fun waitFor(message:String,condition:()->Boolean){val end=SystemClock.uptimeMillis()+10000;while(SystemClock.uptimeMillis()<end){if(condition())return;SystemClock.sleep(75)};dump("failure");error(message+"\n"+nodes().joinToString("\n",transform=::label))}
    private fun launch(mode:String,code:String="S1",scale:Float=1f,dark:Boolean=false){
        instrumentation.startActivitySync(Intent().setClassName(instrumentation.targetContext.packageName,"se.korkort.DeliveryProofActivity").addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK).putExtra("mode",mode).putExtra("code",code).putExtra("fontScale",scale).putExtra("dark",dark))
        instrumentation.waitForIdleSync();waitFor("App did not expose native nodes"){nodes().any{it.packageName==instrumentation.targetContext.packageName}}
    }
    private fun click(text:String){waitFor("Missing $text"){find(text)!=null};var n=find(text)!!;while(!n.isClickable && n.parent!=null)n=n.parent;assertTrue("Cannot activate $text",n.performAction(Node.ACTION_CLICK));instrumentation.waitForIdleSync();SystemClock.sleep(150)}
    private fun scrollTo(text:String,forward:Boolean=true){
        repeat(80){
            if(find(text)!=null)return
            val scroll=nodes().firstOrNull{it.isScrollable && it.isVisibleToUser}?:error("No scroll container for $text")
            val bounds=android.graphics.Rect();scroll.getBoundsInScreen(bounds)
            val x=bounds.exactCenterX();val from=bounds.top+bounds.height()*(if(forward)0.8f else 0.25f);val to=bounds.top+bounds.height()*(if(forward)0.25f else 0.8f)
            val now=SystemClock.uptimeMillis()
            for(step in 0..12){
                val action=when(step){0->android.view.MotionEvent.ACTION_DOWN;12->android.view.MotionEvent.ACTION_UP;else->android.view.MotionEvent.ACTION_MOVE}
                val event=android.view.MotionEvent.obtain(now,now+step*25L,action,x,from+(to-from)*step/12f,0)
                event.source=android.view.InputDevice.SOURCE_TOUCHSCREEN;ui.injectInputEvent(event,true);event.recycle()
            }
            instrumentation.waitForIdleSync();SystemClock.sleep(150)
        }
        if(find(text)!=null)return
        dump("scroll-failure");error("Not reached: $text")
    }

    private fun dump(name:String){
        // Accessibility readiness can precede presentation of the next GPU frame.
        instrumentation.waitForIdleSync();SystemClock.sleep(200)
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
    /** Full actual question contexts, not asset fixtures. Optional range permits resumable runs. */
    @Test fun heldQuestionNativeDeliveryMatrix() {
        val args=InstrumentationRegistry.getArguments()
        val start=args.getString("questionStart")?.toInt() ?: 0
        val replacements=(args.getString("questionGroup") ?: if(args.containsKey("questionStart"))"all" else "replacements")=="replacements"
        val count=args.getString("questionCount")?.toInt() ?: if(replacements)38 else 616
        val questions=candidateQuestions9J.filter {it.acceptance.eligibility==ScoringEligibility.HELD && (!replacements || it.key.revision.value=="replacement-candidate-r2")}.drop(start).take(count)
        require(questions.isNotEmpty())
        val rows=JSONArray()
        val output=File(folder,"question-matrix-$start-$count.json")
        val themes=args.getString("matrixDark")?.let{listOf(it.toBoolean())} ?: listOf(false,true)
        val scales=args.getString("matrixScale")?.let{listOf(it.toFloat())} ?: listOf(1f,1.6f)
        for(dark in themes) for(scale in scales) {
            launch(if(replacements)"candidate-replacements" else "candidate",questions.first().key.questionId.value,scale,dark)
            for((index,q) in questions.withIndex()) {
                val id=q.key.questionId.value
                waitFor("Wrong exact question: $id"){find("Fixture: $id")!=null}
                waitFor("Images not loaded: $id"){find("Exact question images ready")!=null}
                assertFalse(nodes().any{label(it).contains("Correct answer")})
                val capture=args.getString("captureAll")=="true" || id.substringAfterLast('-') in listOf("S5","S6","S7","S11","S12","S13","T1","T2","T6","T8","T22","X8")
                val captureName="question-$id-${if(dark)"dark" else "light"}-$scale"
                if(capture)dump("$captureName-inline")
                repeat(40) {
                    if(nodes().any{it.isVisibleToUser && it.isCheckable})return@repeat
                    nodes().first{it.isVisibleToUser && it.isScrollable}.performAction(Node.ACTION_SCROLL_FORWARD)
                    SystemClock.sleep(75)
                }
                val radio=nodes().first{it.isVisibleToUser && it.isCheckable}
                val choiceLabel=label(radio)
                assertTrue(radio.performAction(Node.ACTION_CLICK))
                val projection=q.snapshot(candidateIdentity9J,kotlin.random.Random(9)).presentation(null,false,true)
                val triggers=listOfNotNull(projection.image?.let{"Enlarge question image"})+projection.choices.filter{it.image!=null}.map{"Enlarge option ${it.letter} image"}
                for(trigger in triggers) {
                    if(find(trigger)==null)scrollTo(trigger,forward=trigger!="Enlarge question image")
                    click(trigger);waitFor("No neutral modal: $id / $trigger"){find("Close")!=null}
                    assertFalse(nodes().any{label(it).contains("Correct answer")})
                    click("Zoom in");waitFor("No zoom: $id"){nodes().any{label(it).contains("150%")}}
                    if(capture)dump("$captureName-$trigger-zoom")
                    click("Reset");waitFor("No reset: $id"){nodes().any{label(it).contains("100%")}}
                    click("Close");instrumentation.waitForIdleSync()
                    waitFor("Lost trigger: $id / $trigger"){find(trigger)!=null}
                    waitFor("Lost focus: $id / $trigger"){var n=find(trigger);var focused=false;while(n!=null){focused=focused || n.isFocused;n=n.parent};focused}
                    nodes().filter{it.isFocused}.forEach{it.performAction(Node.ACTION_CLEAR_FOCUS)}
                }
                scrollTo("A",forward=false)
                waitFor("Lost pending option: $id"){nodes().any{label(it)==choiceLabel && it.isCheckable && (it.isChecked || it.isSelected)}}
                scrollTo("Confirm answer  >");waitFor("Confirm not settled"){find("Confirm answer  >")!=null};click("Confirm answer  >")
                waitFor("No recorded confirmation: $id"){find("Selection recorded for this unscored verification fixture.")!=null}
                rows.put(JSONObject().put("question_id",id).put("revision",q.key.revision.value).put("dark",dark).put("font_scale",scale).put("image_zoom_returns",triggers.size).put("native_selection_focus_confirm","passed"))
                output.writeText(JSONObject().put("package",candidateIdentity9J.toString()).put("complete",false).put("rows",rows).toString(2))
                if(index<questions.lastIndex)click("Next fixture")
            }
        }
        output.writeText(JSONObject().put("package",candidateIdentity9J.toString()).put("complete",true).put("rows",rows).toString(2))
    }

    @Test fun productionPracticeAndReviewUseAcceptedPackage() {
        for(mode in Feedback.entries) {
            launch("production",scale=1.6f)
            waitFor("Accepted production shell missing"){find("KörkortGo")!=null}
            assertTrue(acceptedPracticeBank9J.releaseAccepted)
            assertEquals(1000,acceptedPracticeBank9J.questions.size)
            click("Start a practice test  >")
            waitFor("No setup field"){nodes().any{it.isEditable}}
            assertTrue(nodes().first{it.isEditable}.performAction(Node.ACTION_SET_TEXT,Bundle().apply{putCharSequence(Node.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE,"1")}))
            if(mode==Feedback.AT_END)click("At the end of the test")
            scrollTo("Start test  >");click("Start test  >")
            waitFor("Quiz did not start"){find("Question 1 of 1")!=null}
            val labels=nodes().flatMap{listOfNotNull(it.text?.toString(),it.contentDescription?.toString())}.toSet()
            val q=acceptedQuestions9J.single{it.prompt.assessmentText() in labels && (it.image?.let{image->image.neutralDescription!!.text in labels} ?: true)}
            val choiceLabels=q.options.associate{it.id to (it.image?.neutralDescription?.text ?: it.text.assessmentText())}
            val wrong=q.options.first{it.id!=q.feedback.correctOptionId && choiceLabels.values.count{label->label==choiceLabels[it.id]}==1}
            val wrongLabel=choiceLabels.getValue(wrong.id)
            scrollTo(wrongLabel);click(wrongLabel)
            click("Learning library");waitFor("No unfinished-test guard"){find("Leave this test?")!=null};click("Keep practising")
            var selected=find(wrongLabel)!!;while(!selected.isCheckable && selected.parent!=null)selected=selected.parent
            assertTrue("Wrong pending choice lost",selected.isChecked || selected.isSelected)
            scrollTo("Confirm answer  >");click("Confirm answer  >")
            if(mode==Feedback.AT_END)assertFalse(nodes().any{label(it).contains("Correct answer")})
            click("Finish test  >");waitFor("Wrong score or missing results"){find("0 / 1")!=null};dump("production-${mode.name}-results")
            click("Review answers  >");click("Incorrect");scrollTo("Review all four options ↓");click("Review all four options ↓")
            scrollTo("Correct answer");dump("production-${mode.name}-review")
            val lesson=readerDocuments.single{it.id==q.relationship.primaryLessonId}
            scrollTo(lesson.title);click(lesson.title);waitFor("No review return"){find("Return to answer review")!=null};dump("production-${mode.name}-teaching")
            click("Return to answer review");scrollTo("Hide explanation ↑",forward=false);waitFor("Review expansion lost"){find("Hide explanation ↑")!=null}
            scrollTo("Take another test  >");click("Take another test  >")
            waitFor("Same-process count preference lost"){nodes().any{it.isEditable && it.text?.toString()=="1"}}
            dump("production-${mode.name}-setup-return")
        }
    }

}
