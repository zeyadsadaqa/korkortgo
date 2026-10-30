package se.korkort

import se.korkort.progress.*
import kotlin.random.Random

internal enum class ExerciseMode(val label:String) { MIXED("Mixed practice"),UNANSWERED("Unanswered practice"),REVIEW("Review mistakes"),CHAPTER("Chapter practice"),CATEGORY("Category practice") }
internal data class ExerciseRequest(val mode:ExerciseMode=ExerciseMode.MIXED,val chapter:String?=null,val category:Category?=null) {
    fun encode()="${mode.name}|${chapter.orEmpty()}|${category?.name.orEmpty()}"
    val label get()=when(mode){ExerciseMode.CHAPTER->readerModules.firstOrNull{it.id.value==chapter}?.let{"Chapter ${it.order} practice"} ?: mode.label;ExerciseMode.CATEGORY->category?.title ?: mode.label;else->mode.label}
    companion object { fun decode(text:String?):ExerciseRequest {
        if(text==null)return ExerciseRequest()
        val parts=text.split('|');require(parts.size==3)
        val mode=ExerciseMode.valueOf(parts[0]);val chapter=parts[1].ifBlank{null};val category=parts[2].ifBlank{null}?.let(Category::valueOf)
        require(chapter==null || readerModules.any{it.id.value==chapter})
        require((mode!=ExerciseMode.CHAPTER || chapter!=null) && (mode!=ExerciseMode.CATEGORY || category!=null))
        return ExerciseRequest(mode,chapter,category)
    }}
}
internal fun exercisePool(bank:PracticeBank,request:ExerciseRequest,records:StudyRecords,catalog:ContentCatalog):List<AssessmentQuestion> {
    require(bank.releaseAccepted && bank.identity==acceptedIdentity9J && bank.questions==acceptedQuestions9J)
    val latest=records.latest(catalog)
    val lessons=request.chapter?.let{chapter->readerModules.singleOrNull{it.id.value==chapter}?.lessonIds?.toSet() ?: emptySet()}
    return bank.questions.filter {q->q.acceptance.eligibility==ScoringEligibility.ACCEPTED &&
        (request.category==null || q.category==request.category) &&
        (lessons==null || q.relationship.primaryLessonId in lessons) && when(request.mode) {
            ExerciseMode.UNANSWERED->q.key.questionId.value !in latest
            ExerciseMode.REVIEW->latest[q.key.questionId.value]?.let{(stored,a)->stored.correctOption!=a.selectedOption}==true
            else->true
        }
    }
}
internal fun selectExercise(bank:PracticeBank,request:ExerciseRequest,records:StudyRecords,catalog:ContentCatalog,size:Int,random:Random=Random.Default):List<SessionQuestionSnapshot> {
    val pool=exercisePool(bank,request,records,catalog)
    require(size in 1..70)
    val answered=records.latest(catalog).keys
    if(request.mode==ExerciseMode.MIXED && request.category==null && request.chapter==null) {
        require(practiceStartCheck(size.toString(),bank).allowed)
        return AssessmentEngine.select(bank.questions,size,bank.identity,random,answered)
    }
    val groups=pool.groupBy{it.conceptId}.values.toList()
    require(groups.size>=size){"Choose no more than ${groups.size} questions for this pool."}
    return groups.shuffled(random).take(size).map {g->g.filter{it.key.questionId.value !in answered}.ifEmpty{g}.random(random).snapshot(bank.identity,random)}.shuffled(random)
}
internal data class NextStudyStep(val title:String,val reason:String,val action:String,val lesson:ContentId?=null,val request:ExerciseRequest?=null,val resume:String?=null)
internal data class Dashboard(val records:StudyRecords,val summary:ProgressSummary,val next:NextStudyStep,val lastChapter:CurriculumModule?=null)

internal fun dashboard(records:StudyRecords,study:DurableStudy):Dashboard {
    val catalog=study.catalog;val summary=records.summary(catalog)
    val read=readLessonIds(records.lessons,readerDocuments)
    val modules=readerModules.sortedBy{it.order}
    val readModules=modules.filter{read.containsAll(it.lessonIds)}
    fun chapterTime(m:CurriculumModule)=m.lessonIds.maxOfOrNull{id->records.value("readOrder:${id.value}")?.toLongOrNull() ?: (records.events.filter{it.kind=="read" && it.target==id.value}.maxOfOrNull{it.occurredAt} ?: 0)} ?: 0
    val last=readModules.filter{chapterTime(it)>0}.maxWithOrNull(compareBy<CurriculumModule>{chapterTime(it)}.thenBy{-it.order})
    val active=records.sessions.singleOrNull{it.status=="active" && it.packageId==study.packageId}
    val opened=readerDocuments.filter{it.kind==DocumentKind.LESSON && it.id !in read && records.lessons.any{p->p.lessonId==it.id.value && p.revision==it.revision.value}}
        .filter{(records.value("opened:${it.id.value}")?.toLongOrNull() ?: 0)>0}
        .sortedWith(compareByDescending<CurriculumDocument>{records.value("opened:${it.id.value}")?.toLongOrNull() ?: 0}.thenBy{it.order})
    fun lesson(id:ContentId,continuing:Boolean):NextStudyStep {
        val d=readerDocuments.single{it.id==id};val m=modules.first{ id in it.lessonIds }
        return NextStudyStep(if(continuing)"Continue chapter ${m.order}" else "Start chapter ${m.order}",d.title,if(continuing)"Continue learning" else "Start learning",lesson=id)
    }
    val latestSequence=records.attempts.filter{it.published}.maxOfOrNull{it.sequence} ?: 0
    val reviewDone=records.value("reviewDone")?.toLongOrNull() ?: -1
    val chapter=last?.takeIf {m->summary.lessonsRead<summary.lessonsTotal && chapterTime(m)>(records.value("chapterPractice:${m.id.value}")?.toLongOrNull() ?: -1) && study.pool(ExerciseRequest(ExerciseMode.CHAPTER,m.id.value),records).isNotEmpty()}
    val next=when {
        active!=null->NextStudyStep("Finish your exercise","${records.attempts.count{it.sessionId==active.id}} of ${records.questions.count{it.sessionId==active.id}} questions answered","Resume exercise",resume=active.id)
        opened.isNotEmpty()->lesson(opened.first().id,true)
        chapter!=null->NextStudyStep("Practise chapter ${chapter.order}","You have read all ${chapter.lessonIds.size} lessons. Practise questions linked to this chapter.","Practise this chapter",request=ExerciseRequest(ExerciseMode.CHAPTER,chapter.id.value))
        summary.revisit>=(if(summary.lessonsRead==summary.lessonsTotal)1 else 5) && reviewDone<latestSequence->NextStudyStep("Revisit tricky questions","${summary.revisit} questions need another look based on your latest published answers.","Review mistakes",request=ExerciseRequest(ExerciseMode.REVIEW))
        summary.lessonsRead<summary.lessonsTotal->lesson(modules.flatMap{it.lessonIds}.first{it !in read},false)
        summary.answered<summary.questionTotal->NextStudyStep("Try unanswered questions","${summary.questionTotal-summary.answered} current questions are waiting for your first answer.","Practise unanswered",request=ExerciseRequest(ExerciseMode.UNANSWERED))
        else->NextStudyStep("Keep practising","Revisit any topic with a mixed exercise.","Start an exercise",request=ExerciseRequest())
    }
    return Dashboard(records,summary,next,last)
}
