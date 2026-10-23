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

/** Native AccessibilityNodeInfo actions, not Compose test semantics. Normal production package; test APK supplies the native driver only. */
class NormalJourneyStep11Test {
    private val instrumentation=InstrumentationRegistry.getInstrumentation()
    private val sourceDispatches=java.util.concurrent.CopyOnWriteArrayList<String>()
    private val sourceMonitor=object:android.app.Instrumentation.ActivityMonitor(){
        override fun onStartActivity(intent:Intent):android.app.Instrumentation.ActivityResult? {
            if(intent.action==Intent.ACTION_VIEW)intent.dataString?.let{sourceDispatches.add(it)}
            return null // Observe the actual intent; never intercept the external browser.
        }
    }
    init { instrumentation.addMonitor(sourceMonitor) }
    private val ui=instrumentation.getUiAutomation(UiAutomation.FLAG_DONT_SUPPRESS_ACCESSIBILITY_SERVICES)
    private val folder=File(instrumentation.targetContext.filesDir,InstrumentationRegistry.getArguments().getString("evidenceRun") ?: "native-reader-step1").apply{mkdirs()}
    private fun nodes():List<Node> {
        ui.clearCache()
        fun walk(n:Node):List<Node> = listOf(n)+(0 until n.childCount).flatMap{n.getChild(it)?.let(::walk).orEmpty()}
        return ui.rootInActiveWindow?.also {it.refresh()}?.let(::walk).orEmpty()
    }
    private fun returnFromExternalSource(){
        shell("input keyevent 4")
        val end=SystemClock.uptimeMillis()+2500
        while(SystemClock.uptimeMillis()<end && ui.rootInActiveWindow?.packageName?.toString()!=instrumentation.targetContext.packageName)SystemClock.sleep(100)
        // Chrome may retain history/redirects in its existing task. Switch back
        // to the existing app activity, just as selecting its task in Recents.
        if(ui.rootInActiveWindow?.packageName?.toString()!=instrumentation.targetContext.packageName)
            shell("am start --activity-reorder-to-front -n ${instrumentation.targetContext.packageName}/se.korkort.MainActivity")
    }
    private fun settle(){ try { ui.waitForIdle(100,2000) } catch (_:java.util.concurrent.TimeoutException) { /* Conditions below decide readiness. */ } }
    private fun label(n:Node)=listOfNotNull(n.text?.toString(),n.contentDescription?.toString()).joinToString(" | ")
    private fun find(text:String)=nodes().firstOrNull{it.isVisibleToUser && (it.text?.toString()?.trim()?.replace(Regex("\\s+")," ")==text.trim().replace(Regex("\\s+")," ") || it.contentDescription?.toString()==text)}
    private fun waitFor(message:String,condition:()->Boolean){val end=SystemClock.uptimeMillis()+10000;while(SystemClock.uptimeMillis()<end){if(condition())return;SystemClock.sleep(75)};dump("failure");error(message+"\n"+nodes().joinToString("\n",transform=::label))}
    private fun shell(command:String):String = ui.executeShellCommand(command).use{descriptor->java.io.FileInputStream(descriptor.fileDescriptor).bufferedReader().readText()}
    private fun launch(scale:Float,dark:Boolean){
        shell("settings put system font_scale $scale")
        shell("cmd uimode night ${if(dark)"yes" else "no"}")
        instrumentation.startActivitySync(Intent().setClassName(instrumentation.targetContext.packageName,"se.korkort.MainActivity").addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK))
        settle();waitFor("Normal app did not expose native nodes"){nodes().any{it.packageName==instrumentation.targetContext.packageName}}
    }
    private fun click(text:String){waitFor("Missing $text"){find(text)!=null};var n=find(text)!!;while(!n.isClickable && n.parent!=null)n=n.parent;assertTrue("Cannot activate $text",n.performAction(Node.ACTION_CLICK));settle();SystemClock.sleep(150)}
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
            settle();SystemClock.sleep(150)
        }
        if(find(text)!=null)return
        dump("scroll-failure");error("Not reached: $text")
    }

    private fun dump(name:String){
        // Accessibility readiness can precede presentation of the next GPU frame.
        settle();SystemClock.sleep(200)
        val rows=JSONArray();nodes().filter{it.packageName==instrumentation.targetContext.packageName}.forEach{n->val b=android.graphics.Rect();n.getBoundsInScreen(b);rows.put(JSONObject().put("label",label(n)).put("class",n.className).put("visible",n.isVisibleToUser).put("heading",n.isHeading).put("state_description",n.stateDescription).put("focused",n.isFocused).put("accessibility_focused",n.isAccessibilityFocused).put("selected",n.isSelected).put("checked",n.isChecked).put("bounds",b.toShortString()).put("actions",JSONArray(n.actionList.map{it.id})))}
        File(folder,"$name.json").writeText(rows.toString(2));ui.takeScreenshot()?.let{bitmap->File(folder,"$name.png").outputStream().use{bitmap.compress(Bitmap.CompressFormat.PNG,100,it)};bitmap.recycle()}
    }
    @Test fun productionPracticeAndReviewUseAcceptedPackage() {
        for(dark in listOf(false,true)) for(scale in listOf(1f,1.6f)) for(mode in Feedback.entries) {
            val args=InstrumentationRegistry.getArguments()
            val setting="${if(dark)"dark" else "light"}-${if(scale==1f)"100" else "160"}"
            if(args.getString("onlySetting")?.let{it!=setting}==true || args.getString("onlyMode")?.let{it!=mode.name}==true)continue
            launch(scale,dark)
            waitFor("Accepted production shell missing"){find("KörkortGo")!=null}
            assertTrue(acceptedPracticeBank9J.releaseAccepted)
            assertEquals(1000,acceptedPracticeBank9J.questions.size)
            scrollTo("Start a practice test  >");click("Start a practice test  >")
            waitFor("No setup field"){nodes().any{it.isEditable}}
            assertTrue(nodes().first{it.isEditable}.performAction(Node.ACTION_SET_TEXT,Bundle().apply{putCharSequence(Node.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE,"1")}))
            if(mode==Feedback.AT_END){scrollTo("At the end of the test");click("At the end of the test")}
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
            scrollTo("Finish test  >");click("Finish test  >");waitFor("Wrong score or missing results"){find("0 / 1")!=null};dump("production-$dark-$scale-${mode.name}-results")
            scrollTo("Review answers  >");click("Review answers  >");click("Incorrect");scrollTo("Review all four options ↓");click("Review all four options ↓")
            scrollTo("Correct answer");dump("production-$dark-$scale-${mode.name}-review")
            val lesson=readerDocuments.single{it.id==q.relationship.primaryLessonId}
            scrollTo(lesson.title);click(lesson.title);waitFor("No review return"){find("Return to answer review")!=null};dump("production-$dark-$scale-${mode.name}-teaching")
            click("Return to answer review");scrollTo("Hide explanation ↑",forward=false);waitFor("Review expansion lost"){find("Hide explanation ↑")!=null}
            val reference=navigationSources.references.single{it.id==q.relationship.sourceUses.first().referenceId}
            scrollTo(reference.title);click(reference.title);waitFor("No source return"){find("Back to answer review")!=null};dump("source-$dark-$scale-${mode.name}")
            scrollTo("Open source");click("Open source")
            waitFor("External source callback did not leave app"){ui.rootInActiveWindow?.packageName?.toString()=="com.android.chrome"}
            assertTrue("Exact registered source intent not observed: ${reference.url}; observed=$sourceDispatches",sourceDispatches.contains(reference.url))
            returnFromExternalSource()
            waitFor("App context not restored after source callback"){ui.rootInActiveWindow?.packageName?.toString()==instrumentation.targetContext.packageName}
            scrollTo("Return to answer review")
            click("Return to answer review");scrollTo("Hide explanation ↑",forward=false)
            waitFor("Source return lost expanded review"){find("Hide explanation ↑")!=null}
            scrollTo("Take another test  >");click("Take another test  >")
            waitFor("Same-process count preference lost"){nodes().any{it.isEditable && it.text?.toString()=="1"}}
            dump("production-$dark-$scale-${mode.name}-setup-return")
            val id="FLOW-android-production-${if(mode==Feedback.IMMEDIATE)"immediate" else "deferred"}-${if(dark)"dark" else "light"}-${if(scale==1f)"100" else "160"}"
            val rows=File(folder,"production-journeys.jsonl")
            rows.appendText(JSONObject().put("case_id",id).put("question_id",q.key.questionId.value).put("revision",q.key.revision.value).put("source_url",reference.url).put("normal_app",instrumentation.targetContext.packageName).put("status","pass").toString()+"\n")
        }
    }


    private fun saveCase(id:String, details:JSONObject=JSONObject()) {
        details.put("case_id",id).put("normal_app",instrumentation.targetContext.packageName).put("status","pass")
        File(folder,"learning-journeys.jsonl").appendText(details.toString()+"\n")
    }
    @Test fun normalLibraryAndReferenceJourneys() {
        for(dark in listOf(false,true)) for(scale in listOf(1f,1.6f)) {
            val setting="${if(dark)"dark" else "light"}-${if(scale==1f)"100" else "160"}"
            launch(scale,dark);click("Learning library")
            val doc=readerDocuments.single{it.id.value=="M01-L01"}
            waitFor("No library search"){nodes().any{it.isEditable}}
            nodes().first{it.isEditable}.performAction(Node.ACTION_SET_TEXT,Bundle().apply{putCharSequence(Node.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE,doc.title)})
            scrollTo(doc.title);click(doc.title)
            waitFor("Lesson heading not ready"){nodes().any{it.isHeading && it.text?.toString()==doc.title}}
            dump("reader-opening-$setting")
            val seen=mutableSetOf<String>()
            // Read every authored paragraph/heading while physically traversing the lesson.
            repeat(65){
                seen.addAll(nodes().filter{it.isVisibleToUser}.map(::label))
                val n=nodes().first{it.isScrollable && it.isVisibleToUser}
                val bounds=android.graphics.Rect();n.getBoundsInScreen(bounds)
                val x=bounds.exactCenterX();val from=bounds.top+bounds.height()*0.7f;val to=bounds.top+bounds.height()*0.45f
                val now=SystemClock.uptimeMillis()
                for(step in 0..12){val action=when(step){0->android.view.MotionEvent.ACTION_DOWN;12->android.view.MotionEvent.ACTION_UP;else->android.view.MotionEvent.ACTION_MOVE};val event=android.view.MotionEvent.obtain(now,now+step*25L,action,x,from+(to-from)*step/12f,0);event.source=android.view.InputDevice.SOURCE_TOUCHSCREEN;ui.injectInputEvent(event,true);event.recycle()}
                settle();SystemClock.sleep(100)
            }
            fun normalized(t:String)=t.replace(Regex("\\s+")," ").trim()
            File(folder,"reader-full-text-$setting.txt").writeText(seen.joinToString("\n"))
            val text=normalized(seen.joinToString(" "))
            doc.bodyBlocks.filter{it.payload is BlockPayload.Paragraph || it.payload is BlockPayload.Heading}.forEach{assertTrue("Missing authored block ${it.metadata.id}",text.contains(normalized(it.searchText())))}
            val check=doc.bodyBlocks.first{it.payload is BlockPayload.KnowledgeCheck}.payload as BlockPayload.KnowledgeCheck
            val answer=doc.answerBlocks.single{it.metadata.id==check.answerId}.blocks.first().searchText().removePrefix("Answer:").trim()
            scrollTo("Show answer",false);assertFalse(nodes().any{label(it).contains(answer)})
            click("Show answer");scrollTo(answer);assertNotNull(find(answer));dump("reader-reveal-$setting")
            scrollTo("Hide answer",false);click("Hide answer");assertFalse(nodes().any{label(it).contains(answer)})
            val next=readerDocuments.single{it.id==readingNeighbours(doc.id).second!!}
            scrollTo("Next: ${next.title}");click("Next: ${next.title}")
            scrollTo("Previous: ${doc.title}");click("Previous: ${doc.title}")
            val source=lessonSources(doc).first();scrollTo(source.title);click(source.title)
            scrollTo("Open source");click("Open source");waitFor("Source did not dispatch"){ui.rootInActiveWindow?.packageName?.toString()=="com.android.chrome"}
            assertTrue("Registered reader URL not dispatched",sourceDispatches.contains(source.url));returnFromExternalSource()
            waitFor("Reader source context lost"){ui.rootInActiveWindow?.packageName?.toString()==instrumentation.targetContext.packageName};scrollTo("Return to reading");click("Return to reading")
            scrollTo("Learning library",false);click("Learning library")
            waitFor("Query not retained"){nodes().any{it.isEditable && it.text?.toString()==doc.title}}
            scrollTo("Environment");click("Environment");waitFor("No intersected empty state"){find("No matching lessons.")!=null};dump("library-empty-$setting")
            scrollTo("Clear filters",false);click("Clear filters");scrollTo("Clear search",false);click("Clear search")
            assertTrue(nodes().any{it.isEditable && it.text?.toString()==""})
            saveCase("FLOW-android-library-reader-$setting",JSONObject().put("source_url",source.url).put("full_authored_body",true))
            scrollTo("Road signs and reference",false);click("Road signs and reference")
            val sign=navigationSigns.single{it.code=="B1"};val group=navigationReferenceGroups.first{sign.id in it.entryIds}
            scrollTo(group.title);click(group.title);scrollTo(sign.englishLabel);click(sign.englishLabel)
            scrollTo("Enlarge image");val trigger=find("Enlarge image")!!;click("Enlarge image")
            waitFor("Reference modal missing"){find("Close")!=null};assertNull(find("Learning library"));assertNull(find("‹ Road signs and reference"))
            click("Zoom in");waitFor("No zoom150"){nodes().any{label(it).contains("150%")}}
            shell("input keyevent 22");dump("reference-pan-$setting")
            click("Reset");waitFor("No reset100"){nodes().any{label(it).contains("100%")}};click("Close")
            waitFor("Reference trigger not restored"){find("Enlarge image")!=null}
            var focus=find("Enlarge image")!!;while(!focus.isFocusable && focus.parent!=null)focus=focus.parent
            assertTrue("Reference focus not restored",focus.isFocused)
            dump("reference-return-$setting");scrollTo("‹ Road signs and reference",false);click("‹ Road signs and reference")
            waitFor("Catalogue return missing"){find("Road signs and signals")!=null}
            saveCase("FLOW-android-reference-viewer-$setting",JSONObject().put("reference_code","B1").put("keyboard_pan_issued",true).put("focus_return",true))
        }
    }

}
