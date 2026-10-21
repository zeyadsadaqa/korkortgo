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
class AdditionalNative10KTest {
    private val instrumentation=InstrumentationRegistry.getInstrumentation()
    private val ui=instrumentation.getUiAutomation(UiAutomation.FLAG_DONT_SUPPRESS_ACCESSIBILITY_SERVICES)
    private val folder=File(instrumentation.targetContext.filesDir,"native-10k-additional").apply{mkdirs()}
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
    @Test fun exactUnavailableSignalsDispatchAndReturnOffline() {
        val rows=JSONArray()
        for(code in listOf("SIG16","SIG17","SIG18")) {
            launch("learning-sign",code)
            waitFor("No exact unavailable state"){find("Content unavailable")!=null}
            assertFalse(nodes().any{label(it).contains("Exact illustration loaded")})
            dump("$code-unavailable")
            click("Open official description")
            SystemClock.sleep(1200)
            val rootPackage=ui.rootInActiveWindow?.packageName?.toString()
            val uri=canonicalResolver.legacy(LegacyLookup.Sign("legacy-app-4768933c3d9a",code)) as Resolution.Unavailable
            val expected=navigationSources.references.single{it.id==uri.officialReferenceId}.url
            val text=ui.executeShellCommand("dumpsys activity activities").use { fd->java.io.FileInputStream(fd.fileDescriptor).readBytes().toString(Charsets.UTF_8) }
            val matching=text.lineSequence().filter{it.contains(expected)}.toList()
            fun normalizedUrl(value:String)=value.substringAfter("://").removePrefix("www.").trimEnd('/')
            val browserAddressMatches=nodes().map(::label).filter{normalizedUrl(it)==normalizedUrl(expected)}
            val urlObserved=matching.isNotEmpty() || browserAddressMatches.isNotEmpty()
            File(folder,"$code-dispatch.json").writeText(JSONObject().put("expected_url",expected).put("foreground_package",rootPackage).put("matching_activity_lines",JSONArray(matching)).put("matching_native_browser_address",JSONArray(browserAddressMatches)).toString(2))
            ui.takeScreenshot()?.let{bitmap->File(folder,"$code-external.png").outputStream().use{bitmap.compress(Bitmap.CompressFormat.PNG,100,it)};bitmap.recycle()}
            repeat(3) {
                if(ui.rootInActiveWindow?.packageName?.toString()!=instrumentation.targetContext.packageName) {
                    ui.executeShellCommand("input keyevent KEYCODE_BACK").use {fd->java.io.FileInputStream(fd.fileDescriptor).readBytes()}
                    SystemClock.sleep(600)
                }
            }
            waitFor("No internal recovery after external return"){find("Open learning library")!=null}
            dump("$code-return")
            click("Open learning library");waitFor("Lost library recovery"){nodes().any{it.isEditable}}
            rows.put(JSONObject().put("signal",code).put("expected_url",expected).put("dispatch_url_observed",urlObserved).put("external_package",rootPackage).put("returned_library",true))
        }
        File(folder,"signal-actions.json").writeText(JSONObject().put("rows",rows).put("scope","Fresh offline OS dispatch and internal recovery; website availability and online success not established").toString(2))
        assertTrue((0 until rows.length()).all{rows.getJSONObject(it).getBoolean("dispatch_url_observed")})
    }
    @Test fun productionFeedbackModesWithVisibleSetupControls() {
        for(mode in Feedback.entries) {
            launch("production",scale=1.6f)
            waitFor("Accepted production shell missing"){find("KörkortGo")!=null}
            assertTrue(acceptedPracticeBank9J.releaseAccepted)
            assertEquals(1000,acceptedPracticeBank9J.questions.size)
            click("Start a practice test  >")
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
