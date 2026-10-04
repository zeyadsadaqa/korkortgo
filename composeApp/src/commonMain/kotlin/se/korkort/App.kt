@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class, org.jetbrains.compose.resources.ExperimentalResourceApi::class)
package se.korkort

import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import org.jetbrains.compose.resources.decodeToImageBitmap
import se.korkort.resources.Res
import kotlin.math.roundToInt

private val Forest=Color(0xFF173E32)
private val Paper=Color(0xFFF7F8F3)
private val Sage=Color(0xFFE7EEE5)
private val Ink=Color(0xFF172C29)
private val Muted=Color(0xFF61706B)
private val Line=Color(0xFFD5DED5)
private val Ochre=Color(0xFFE7BD4A)
private val Wrong=Color(0xFF9A332F)
private val WrongBg=Color(0xFFFFEDEA)
private enum class Page { HOME, LIBRARY, READER, SETUP, QUIZ, RESULTS, REVIEW, SIGNS }

@Composable fun App() {
    MaterialTheme(colorScheme=lightColorScheme(primary=Forest, onPrimary=Color.White, background=Paper, surface=Color.White, onSurface=Ink, secondary=Forest, secondaryContainer=Sage, onSecondaryContainer=Forest, surfaceVariant=Sage, outline=Line)) {
        var page by remember { mutableStateOf(Page.HOME) }
        var countText by remember { mutableStateOf("70") }
        var feedback by remember { mutableStateOf(Feedback.IMMEDIATE) }
        var session by remember { mutableStateOf<QuizSession?>(null) }
        var chapter by remember { mutableStateOf(chapters.first()) }
        var category by remember { mutableStateOf<Category?>(null) }
        var search by remember { mutableStateOf("") }
        var reviewFilter by remember { mutableStateOf("All") }
        var quitTarget by remember { mutableStateOf<Page?>(null) }
        fun navigate(target: Page) { if(page==Page.QUIZ && session?.finished==false) quitTarget=target else page=target }
        fun readPage(number: Int) { chapter=chapters.firstOrNull { number in it.page..it.endPage } ?: chapters.first(); page=Page.READER }
        Surface(Modifier.fillMaxSize(),color=Paper) {
            Column(Modifier.fillMaxSize().windowInsetsPadding(WindowInsets.safeDrawing)) {
                Box(Modifier.fillMaxWidth().background(Paper),contentAlignment=Alignment.Center) {
                    Column(Modifier.widthIn(max=1160.dp).fillMaxWidth().padding(horizontal=24.dp,vertical=16.dp)) {
                        Row(Modifier.fillMaxWidth(),verticalAlignment=Alignment.CenterVertically) {
                            Text("Körkort",fontFamily=FontFamily.Serif,fontWeight=FontWeight.Bold,fontSize=27.sp,color=Forest,modifier=Modifier.clickable { navigate(Page.HOME) }.semantics { role=Role.Button })
                            Spacer(Modifier.weight(1f))
                            Text("ENGLISH · CATEGORY B",fontSize=10.sp,letterSpacing=1.sp,color=Muted)
                        }
                        Spacer(Modifier.height(12.dp))
                        Row(horizontalArrangement=Arrangement.spacedBy(8.dp)) {
                            Nav("Overview",page==Page.HOME) { navigate(Page.HOME) }
                            Nav("Theory library",page in listOf(Page.LIBRARY,Page.READER,Page.SIGNS)) { navigate(Page.LIBRARY) }
                            Nav("Practice",page in listOf(Page.SETUP,Page.QUIZ,Page.RESULTS,Page.REVIEW)) { navigate(Page.SETUP) }
                        }
                    }
                }
                HorizontalDivider(color=Line)
                Box(Modifier.weight(1f).fillMaxWidth(),contentAlignment=Alignment.TopCenter) {
                    key(page, if(page==Page.READER) chapter.title else if(page==Page.QUIZ) session?.current?.id else "") {
                        LazyColumn(Modifier.widthIn(max=1160.dp).fillMaxSize(),contentPadding=PaddingValues(24.dp),verticalArrangement=Arrangement.spacedBy(20.dp)) {
                            when(page) {
                                Page.HOME -> {
                                    item { AdaptiveColumns({
                                        Eyebrow("YOUR SWEDISH DRIVING JOURNEY")
                                        Heading("Your road to\nconfidence.",large=true)
                                        Text("Learn the rules. Understand the why. Practise at your pace.",color=Muted,fontSize=18.sp,lineHeight=27.sp)
                                        Spacer(Modifier.height(24.dp))
                                        Primary("Start a practice test  >") { page=Page.SETUP }
                                        TextButton(onClick={page=Page.LIBRARY}) { Text("Explore the theory  >") }
                                    }, { RoadIllustration() }) }
                                    item { Panel(Sage) { FlowRow(horizontalArrangement=Arrangement.spacedBy(32.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
                                        Stat("1,000","practice questions"); Stat("5","knowledge areas"); Stat("2026","theory edition")
                                    } } }
                                    item { Heading("A little learning. A safer journey.") }
                                    item { FlowRow(horizontalArrangement=Arrangement.spacedBy(12.dp),verticalArrangement=Arrangement.spacedBy(12.dp)) {
                                        Category.entries.forEach { c -> Surface(onClick={category=c;search="";page=Page.LIBRARY},shape=RoundedCornerShape(14.dp),border=BorderStroke(1.dp,Line),color=Color.White,modifier=Modifier.widthIn(min=175.dp,max=210.dp).heightIn(min=125.dp)) {
                                            Column(Modifier.padding(20.dp)) { Text(categoryIcon(c),fontSize=24.sp,color=Forest); Spacer(Modifier.height(12.dp)); Text(c.title,fontWeight=FontWeight.SemiBold); Text("Explore  >",color=Forest,fontSize=12.sp,modifier=Modifier.padding(top=8.dp)) }
                                        }
                                    } } }
                                    item { Panel { Text("Built for understanding",fontWeight=FontWeight.Bold,fontSize=18.sp); Text("Original explained practice questions, a complete chapter guide, and official Swedish road-sign artwork. Choose 1–70 questions and learn in the way that suits you.",color=Muted,lineHeight=23.sp); Text("Study material based on Theory Book 2026, edition 2026-1, and Transportstyrelsen. This is independent practice, not an official examination.",color=Muted,fontSize=12.sp,lineHeight=18.sp) } }
                                }
                                Page.LIBRARY -> {
                                    item { Eyebrow("THEORY LIBRARY"); Heading("Understand every journey."); Text("Explore ${chapters.size} chapters across the five knowledge areas.",color=Muted) }
                                    item { OutlinedTextField(search,{search=it},label={Text("Search topics, rules and road signs")},singleLine=true,modifier=Modifier.fillMaxWidth()) }
                                    item { CategoryFilters(category) { category=it } }
                                    item { OutlinedButton(onClick={search="";page=Page.SIGNS},modifier=Modifier.fillMaxWidth()) { Text("Open the official road-sign catalogue  ·  ${roadSigns.size} illustrations  >") } }
                                    val filtered=chapters.filter { (category==null || it.category==category) && (it.title+it.summary).contains(search,true) }
                                    if(filtered.isEmpty()) item { EmptyState("No chapters found", "Try another search or choose All topics.") }
                                    items(filtered,key={it.title}) { ch -> Surface(onClick={chapter=ch;page=Page.READER},color=Color.White,shape=RoundedCornerShape(14.dp),border=BorderStroke(1.dp,Line)) {
                                        Row(Modifier.fillMaxWidth().padding(22.dp),verticalAlignment=Alignment.CenterVertically) {
                                            Column(Modifier.weight(1f)) { Eyebrow(ch.category.short); Text(ch.title,fontFamily=FontFamily.Serif,fontSize=24.sp,fontWeight=FontWeight.Bold); Text(ch.summary.substringBefore("\n").take(150)+"…",color=Muted,lineHeight=21.sp,modifier=Modifier.padding(top=8.dp)); Text("Book pages ${ch.page}–${ch.endPage}",fontSize=12.sp,color=Muted,modifier=Modifier.padding(top=10.dp)) }; Text(">",fontSize=24.sp,color=Forest)
                                        }
                                    } }
                                    item { SourceFooter() }
                                }
                                Page.READER -> {
                                    item { TextButton(onClick={page=Page.LIBRARY}) { Text("< Theory library") }; Eyebrow(chapter.category.title); Heading(chapter.title); Text("Theory Book 2026 · pages ${chapter.page}–${chapter.endPage}",color=Muted,fontSize=12.sp) }
                                    items(chapter.summary.split("\n\n")) { paragraph -> Text(paragraph,lineHeight=29.sp,fontSize=18.sp,color=Ink,modifier=Modifier.widthIn(max=820.dp)) }
                                    if(chapter.title=="Road signs & markings") item { Primary("Explore official road signs  >") {search="";page=Page.SIGNS} }
                                    item { Panel(Sage) { Text("Check your understanding",fontFamily=FontFamily.Serif,fontSize=25.sp,fontWeight=FontWeight.Bold); Text("Can you explain the rule and why it makes the road safer? Use the practice questions to apply what you have read.",color=Muted); Primary("Practise with a new test  >") {page=Page.SETUP} } }
                                    item { Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.SpaceBetween) {
                                        val index=chapters.indexOf(chapter)
                                        TextButton(onClick={chapter=chapters[index-1]},enabled=index>0) { Text("< Previous chapter") }
                                        TextButton(onClick={chapter=chapters[index+1]},enabled=index<chapters.lastIndex) {Text("Next chapter >")}
                                    } }
                                    item { SourceFooter() }
                                }
                                Page.SIGNS -> {
                                    item { TextButton(onClick={page=Page.LIBRARY}) { Text("< Theory library") }; Heading("Read the road."); Text("Official artwork from Transportstyrelsen. Search by name or sign code.",color=Muted) }
                                    item { OutlinedTextField(search,{search=it},label={Text("Search signs, e.g. parking or B1")},singleLine=true,modifier=Modifier.fillMaxWidth()) }
                                    val signs=roadSigns.filter { (it.code+" "+it.title).contains(search,true) }
                                    if(signs.isEmpty()) item { EmptyState("No matching signs", "Try a sign code or a shorter search.") }
                                    items(signs.chunked(3)) { group -> AdaptiveSignRow(group) }
                                    item { Text("Still images do not reproduce flashing or moving signals. Open the official source to study each signal's full meaning.",color=Muted,fontSize=12.sp) }
                                }
                                Page.SETUP -> {
                                    item { Eyebrow("PRACTICE, YOUR WAY"); Heading("Make this practice yours."); Text("Choose your length and when you want to see the answers.",color=Muted) }
                                    item { AdaptiveColumns({
                                        Panel { Text("1. How many questions?",fontSize=20.sp,fontWeight=FontWeight.Bold)
                                            val n=countText.toIntOrNull()
                                            OutlinedTextField(countText,{if(it.length<=3 && it.all(Char::isDigit)) countText=it},label={Text("Number of questions")},singleLine=true,isError=n==null || n !in 1..70,supportingText={Text("Choose any number from 1 to 70")},modifier=Modifier.fillMaxWidth())
                                            Slider(value=(n?:1).coerceIn(1,70).toFloat(),onValueChange={countText=it.roundToInt().toString()},valueRange=1f..70f,steps=68,modifier=Modifier.semantics { contentDescription="Number of questions, 1 to 70" })
                                            Row(horizontalArrangement=Arrangement.spacedBy(8.dp)) { listOf(10,20,40,70).forEach { count -> FilterChip(selected=n==count,onClick={countText=count.toString()},label={Text(count.toString())}) } }
                                        }
                                        Spacer(Modifier.height(16.dp))
                                        Panel { Text("2. Reveal the answers",fontSize=20.sp,fontWeight=FontWeight.Bold)
                                            ModeCard("After each question","See the answer and all four explanations as you go.",feedback==Feedback.IMMEDIATE) {feedback=Feedback.IMMEDIATE}
                                            ModeCard("At the end of the test","Finish the test first, then review every answer.",feedback==Feedback.AT_END) {feedback=Feedback.AT_END}
                                        }
                                    },{
                                        Panel(Sage) { Text("Your question mix",fontFamily=FontFamily.Serif,fontSize=26.sp,fontWeight=FontWeight.Bold)
                                            val n=countText.toIntOrNull(); val valid=n!=null && n in 1..70
                                            val mix=QuizEngine.allocation((n?:1).coerceIn(1,70))
                                            Category.entries.forEach { c -> Row(Modifier.fillMaxWidth().padding(vertical=8.dp),verticalAlignment=Alignment.CenterVertically) {Text(c.title,modifier=Modifier.weight(1f),fontSize=14.sp); Text((mix.categories[c]?:0).toString(),fontWeight=FontWeight.Bold)} }
                                            HorizontalDivider(color=Line)
                                            Row(Modifier.fillMaxWidth().padding(vertical=8.dp)) { Text("Random from any category",modifier=Modifier.weight(1f),fontSize=14.sp);Text(mix.random.toString(),fontWeight=FontWeight.Bold) }
                                            Text("The extra random questions can belong to any category. No repeated learning point within a test.",fontSize=12.sp,color=Muted,lineHeight=18.sp)
                                            Primary("Start test  >",enabled=valid) { session=QuizSession(QuizEngine.select(questionBank,n!!),feedback);page=Page.QUIZ }
                                            Text("No time pressure. All questions count towards your practice score.",fontSize=12.sp,color=Muted)
                                        }
                                    }) }
                                }
                                Page.QUIZ -> {
                                    val s=session
                                    if(s!=null) {
                                        item { Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.SpaceBetween,verticalAlignment=Alignment.CenterVertically) { Eyebrow("PRACTICE TEST"); TextButton(onClick={quitTarget=Page.SETUP}) {Text("End test")}}; LinearProgressIndicator(progress={s.index.toFloat()/s.questions.size},modifier=Modifier.fillMaxWidth(),color=Forest,trackColor=Sage);Text("Question ${s.index+1} of ${s.questions.size}",color=Muted,modifier=Modifier.padding(top=12.dp)) }
                                        item(key=s.current.id) { QuestionCard(s.current,s.answers[s.current.id],s.feedback==Feedback.IMMEDIATE && s.current.id in s.answers,onConfirm={i->session=s.answer(i)},onRead={readPage(it)},allowRead=false) }
                                        item { val answered=s.current.id in s.answers
                                            if(answered) { if(s.feedback==Feedback.AT_END) Panel(Sage) { Text("Answer saved. Your result will be revealed after the final question.") }
                                                Spacer(Modifier.height(12.dp)); Primary(if(s.index==s.questions.lastIndex) "Finish test  >" else "Next question  >") { val next=s.next();session=next;if(next.finished) page=Page.RESULTS }
                                            } else Text(if(s.feedback==Feedback.AT_END) "Answers revealed at the end" else "Answers explained after each question",color=Muted,fontSize=12.sp)
                                        }
                                    }
                                }
                                Page.RESULTS -> {
                                    val s=session
                                    if(s!=null) {
                                        item { Eyebrow("TEST COMPLETE"); Heading("Every question is\na step forward.");Text("Take a moment to understand what you missed.",color=Muted) }
                                        item { AdaptiveColumns({Panel(Sage) { Text("${s.score} / ${s.questions.size}",fontFamily=FontFamily.Serif,fontSize=64.sp,fontWeight=FontWeight.Bold,color=Forest);Text("${(100.0*s.score/s.questions.size).roundToInt()}% correct",fontSize=22.sp);Text("${s.score} correct · ${s.questions.size-s.score} to revisit",color=Muted);Primary("Review answers  >") {reviewFilter="All";page=Page.REVIEW};OutlinedButton(onClick={page=Page.SETUP},modifier=Modifier.fillMaxWidth()) {Text("Take another test")};Text("Practice score · not an official exam result",fontSize=12.sp,color=Muted)}},{Panel { Text("Results by category",fontFamily=FontFamily.Serif,fontSize=25.sp,fontWeight=FontWeight.Bold)
                                            Category.entries.forEach { c -> val qs=s.questions.filter {it.category==c}; val correct=qs.count {s.answers[it.id]==it.correct}
                                                Row(Modifier.fillMaxWidth()) {Text(c.title,modifier=Modifier.weight(1f),fontSize=14.sp);Text("$correct / ${qs.size}",fontWeight=FontWeight.Bold)}
                                                LinearProgressIndicator(progress={if(qs.isEmpty())0f else correct.toFloat()/qs.size},modifier=Modifier.fillMaxWidth().padding(bottom=12.dp),color=Forest,trackColor=Sage)
                                            }
                                            Text("Category totals include the additional random questions.",fontSize=12.sp,color=Muted)
                                        }}) }
                                    }
                                }
                                Page.REVIEW -> {
                                    val s=session
                                    if(s!=null) {
                                        item { TextButton(onClick={page=Page.RESULTS}) {Text("< Results")};Heading("Turn mistakes into\nunderstanding."); Row(horizontalArrangement=Arrangement.spacedBy(8.dp)) {listOf("All","Incorrect","Correct").forEach { f -> FilterChip(selected=reviewFilter==f,onClick={reviewFilter=f},label={Text(f)})}} }
                                        val qs=s.questions.filter { reviewFilter=="All" || (s.answers[it.id]==it.correct)==(reviewFilter=="Correct") }
                                        if(qs.isEmpty()) item { EmptyState("Nothing to revisit here", "Use another filter to explore your answers.") }
                                        items(qs,key={it.id}) { q -> var open by remember(q.id) {mutableStateOf(false)}
                                            Panel { val correct=s.answers[q.id]==q.correct
                                                Text(if(correct) "Correct" else "Incorrect",color=if(correct)Forest else Wrong,fontWeight=FontWeight.Bold,fontSize=12.sp)
                                                Text(q.prompt,fontWeight=FontWeight.SemiBold,fontSize=18.sp,lineHeight=25.sp)
                                                TextButton(onClick={open=!open}) {Text(if(open) "Hide explanation ↑" else "Review all four options ↓")}
                                                if(open) QuestionCard(q,s.answers[q.id],true,onConfirm={},onRead={readPage(it)},showPrompt=false)
                                            }
                                        }
                                        item { Primary("Take another test  >") {page=Page.SETUP} }
                                    }
                                }
                            }
                            item { Spacer(Modifier.height(12.dp));HorizontalDivider(color=Line);Text("Körkort  ·  More knowledge. A safer tomorrow.",fontSize=12.sp,color=Muted,modifier=Modifier.padding(vertical=20.dp)) }
                        }
                    }
                }
            }
        }
        if(quitTarget!=null) AlertDialog(onDismissRequest={quitTarget=null},title={Text("Leave this test?")},text={Text("Your unfinished answers will be discarded. You can start a fresh test whenever you are ready.")},confirmButton={TextButton(onClick={session=null;page=quitTarget!!;quitTarget=null}) {Text("Leave test")}},dismissButton={TextButton(onClick={quitTarget=null}) {Text("Keep practising")}})
    }
}

@Composable private fun QuestionCard(q:Question,answer:Int?,reveal:Boolean,onConfirm:(Int)->Unit,onRead:(Int)->Unit,allowRead:Boolean=true,showPrompt:Boolean=true) {
    var selected by remember(q.id) { mutableStateOf<Int?>(answer) }
    Column(verticalArrangement=Arrangement.spacedBy(14.dp)) {
        if(showPrompt) { Eyebrow(q.category.title); Text(q.prompt,fontFamily=FontFamily.Serif,fontSize=28.sp,lineHeight=36.sp,fontWeight=FontWeight.Bold,color=Ink) }
        if(q.image.isNotEmpty()) ResourceImage(q.image,"Question illustration from Transportstyrelsen",Modifier.fillMaxWidth().height(180.dp))
        q.options.forEachIndexed { i,o ->
            val chosen=(answer?:selected)==i; val isCorrect=q.correct==i
            val bg=when {reveal && isCorrect->Sage;reveal && chosen->WrongBg;chosen->Sage;else->Color.White}
            val border=when {reveal && chosen && !isCorrect->Wrong;chosen || reveal && isCorrect->Forest;else->Line}
            Surface(onClick={selected=i},enabled=answer==null,shape=RoundedCornerShape(12.dp),color=bg,border=BorderStroke(1.dp,border),modifier=Modifier.fillMaxWidth().semantics { role=Role.RadioButton;this.selected=chosen }) {
                Column(Modifier.padding(18.dp),verticalArrangement=Arrangement.spacedBy(8.dp)) {
                    Row(verticalAlignment=Alignment.CenterVertically,horizontalArrangement=Arrangement.spacedBy(12.dp)) {
                        Text(('A'+i).toString(),fontWeight=FontWeight.Bold,color=Forest)
                        if(o.image.isEmpty()) Text(o.text,modifier=Modifier.weight(1f),lineHeight=22.sp)
                        else ResourceImage(o.image,"Option ${'A'+i}: ${o.text}",Modifier.weight(1f).height(105.dp))
                        if(chosen) Text("●",color=border)
                    }
                    if(reveal) {
                        Text(when {isCorrect && chosen->"Correct · Your answer";isCorrect->"Correct answer";chosen->"Your answer · Incorrect";else->"Incorrect option"},color=if(isCorrect)Forest else Wrong,fontSize=12.sp,fontWeight=FontWeight.Bold)
                        Text(o.explanation,color=Ink,lineHeight=22.sp,fontSize=14.sp)
                    }
                }
            }
        }
        if(answer==null) Primary("Confirm answer  >",enabled=selected!=null) {onConfirm(selected!!)}
        if(reveal) {
            Text(if(answer==q.correct) "Well understood." else "Let’s understand this one.",fontFamily=FontFamily.Serif,fontSize=23.sp,fontWeight=FontWeight.Bold,color=Forest)
            Text(q.explanation,lineHeight=23.sp,color=Muted)
            Text("Source: Theory Book 2026 · page ${q.page}",fontSize=12.sp,color=Muted)
            if(q.source.isNotEmpty()) SourceLink("Transportstyrelsen · Official source >",q.source)
            if(allowRead) TextButton(onClick={onRead(q.page)}) {Text("Read the related chapter  >")}
        }
    }
}
@Composable private fun Nav(label:String,active:Boolean,onClick:()->Unit) { TextButton(onClick=onClick,colors=ButtonDefaults.textButtonColors(containerColor=if(active)Sage else Color.Transparent)) { Text(label,color=Forest,fontWeight=if(active)FontWeight.Bold else FontWeight.Normal) } }
@Composable private fun Eyebrow(text:String) { Text(text.uppercase(),fontSize=11.sp,letterSpacing=1.3.sp,color=Muted,fontWeight=FontWeight.SemiBold,modifier=Modifier.padding(bottom=10.dp)) }
@Composable private fun Heading(text:String,large:Boolean=false) { Text(text,fontFamily=FontFamily.Serif,fontWeight=FontWeight.Bold,fontSize=if(large)48.sp else 36.sp,lineHeight=if(large)54.sp else 43.sp,color=Forest,modifier=Modifier.padding(bottom=16.dp)) }
@Composable private fun Primary(text:String,enabled:Boolean=true,onClick:()->Unit) { Button(onClick=onClick,enabled=enabled,shape=RoundedCornerShape(9.dp),contentPadding=PaddingValues(horizontal=24.dp,vertical=16.dp),modifier=Modifier.heightIn(min=52.dp)) {Text(text,fontWeight=FontWeight.SemiBold)} }
@Composable private fun Panel(color:Color=Color.White,content:@Composable ColumnScope.()->Unit) { Surface(color=color,shape=RoundedCornerShape(16.dp),border=BorderStroke(1.dp,Line),modifier=Modifier.fillMaxWidth()) { Column(Modifier.padding(24.dp),verticalArrangement=Arrangement.spacedBy(14.dp),content=content) } }
@Composable private fun Stat(value:String,label:String) { Column {Text(value,fontFamily=FontFamily.Serif,fontWeight=FontWeight.Bold,fontSize=30.sp,color=Forest);Text(label,color=Muted,fontSize=13.sp)} }
@Composable private fun AdaptiveColumns(left:@Composable ColumnScope.()->Unit,right:@Composable ColumnScope.()->Unit) { BoxWithConstraints(Modifier.fillMaxWidth()) { if(maxWidth>760.dp) Row(horizontalArrangement=Arrangement.spacedBy(28.dp)) {Column(Modifier.weight(1.2f),content=left);Column(Modifier.weight(1f),content=right)} else Column(verticalArrangement=Arrangement.spacedBy(24.dp)) {Column(content=left);Column(content=right)} } }
@Composable private fun ModeCard(title:String,description:String,selected:Boolean,onClick:()->Unit) { Surface(onClick=onClick,color=if(selected)Sage else Color.White,border=BorderStroke(1.dp,if(selected)Forest else Line),shape=RoundedCornerShape(10.dp),modifier=Modifier.fillMaxWidth().semantics {role=Role.RadioButton;this.selected=selected}) {Row(Modifier.padding(16.dp),verticalAlignment=Alignment.CenterVertically) {RadioButton(selected=selected,onClick=null);Column(Modifier.padding(start=8.dp)) {Text(title,fontWeight=FontWeight.SemiBold);Text(description,fontSize=13.sp,lineHeight=19.sp,color=Muted)}}} }
@Composable private fun CategoryFilters(selected:Category?,onSelect:(Category?)->Unit) { FlowRow(horizontalArrangement=Arrangement.spacedBy(8.dp)) {FilterChip(selected=selected==null,onClick={onSelect(null)},label={Text("All topics")});Category.entries.forEach { c->FilterChip(selected=selected==c,onClick={onSelect(c)},label={Text(c.short)})}} }
@Composable private fun EmptyState(title:String,body:String) {Panel(Sage) {Text(title,fontSize=22.sp,fontWeight=FontWeight.Bold);Text(body,color=Muted)} }
@Composable private fun SourceLink(label:String,url:String) {val uri=LocalUriHandler.current;TextButton(onClick={uri.openUri(url)}) {Text(label,fontSize=12.sp)} }
@Composable private fun SourceFooter() {Panel(Sage) {Text("Your study sources",fontWeight=FontWeight.Bold);Text("Theory Book 2026 · edition 2026-1 · Körkortonline.se. Chapters here are original study summaries. Official road-sign artwork and additional rule guidance: Transportstyrelsen. Sources checked 26 September 2026.",fontSize=12.sp,color=Muted,lineHeight=19.sp);SourceLink("Transportstyrelsen · Rules and signs >","https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/")} }
@Composable private fun ResourceImage(path:String,description:String,modifier:Modifier=Modifier) {
    val bitmap by produceState<ImageBitmap?>(null,path) { value=runCatching {Res.readBytes("files/$path").decodeToImageBitmap()}.getOrNull() }
    Box(modifier.background(Color.White,RoundedCornerShape(8.dp)).padding(10.dp),contentAlignment=Alignment.Center) {
        if(bitmap!=null) Image(bitmap!!,description,Modifier.fillMaxSize(),contentScale=ContentScale.Fit)
        else Text("Loading illustration…",color=Muted,fontSize=12.sp)
    }
}
@Composable private fun AdaptiveSignRow(signs:List<RoadSign>) { BoxWithConstraints {if(maxWidth>650.dp) Row(horizontalArrangement=Arrangement.spacedBy(12.dp)) {signs.forEach {s->Box(Modifier.weight(1f)){SignCard(s)}};repeat(3-signs.size){Spacer(Modifier.weight(1f))}} else Column(verticalArrangement=Arrangement.spacedBy(12.dp)) {signs.forEach {SignCard(it)}}} }
@Composable private fun SignCard(s:RoadSign) {Panel {ResourceImage(s.image,"${s.code}: ${s.title}",Modifier.fillMaxWidth().height(130.dp));Text(s.code,fontSize=12.sp,color=Muted);Text(s.title,fontWeight=FontWeight.SemiBold);SourceLink("Official description >",s.url)} }
private fun categoryIcon(c:Category)=when(c){Category.VEHICLE->"01";Category.ENVIRONMENT->"02";Category.SAFETY->"03";Category.RULES->"04";Category.PERSONAL->"05"}
@Composable private fun RoadIllustration() {Canvas(Modifier.fillMaxWidth().height(300.dp).background(Sage,RoundedCornerShape(24.dp)).semantics {contentDescription="Illustration of a winding road through a quiet landscape"}) {
    val w=size.width;val h=size.height
    drawCircle(Color(0xFFF3D77F),radius=h*.12f,center=Offset(w*.77f,h*.2f))
    val hill=Path().apply {moveTo(0f,h*.65f);cubicTo(w*.25f,h*.2f,w*.65f,h*.8f,w,h*.4f);lineTo(w,h);lineTo(0f,h);close()};drawPath(hill,Color(0xFFB9CBB6))
    val road=Path().apply {moveTo(w*.55f,h*1.1f);cubicTo(w*.03f,h*.58f,w*.95f,h*.6f,w*.5f,h*.16f)}
    drawPath(road,Color(0xFFF9FAF4),style=Stroke(width=w*.15f,cap=StrokeCap.Round));drawPath(road,Color(0xFF7A8A80),style=Stroke(width=w*.12f,cap=StrokeCap.Round));drawPath(road,Color(0xFFF6E7A0),style=Stroke(width=2.dp.toPx()))
    listOf(.13f to .63f,.22f to .38f,.82f to .68f,.89f to .49f,.71f to .37f).forEach { (x,y)->val tree=Path().apply {moveTo(w*x,h*(y-.17f));lineTo(w*(x-.055f),h*y);lineTo(w*(x+.055f),h*y);close()};drawPath(tree,Forest);drawLine(Forest,Offset(w*x,h*y),Offset(w*x,h*(y+.05f)),3.dp.toPx())}
} }
