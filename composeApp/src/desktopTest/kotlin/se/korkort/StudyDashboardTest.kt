package se.korkort

import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import java.nio.file.Files
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.Json
import se.korkort.progress.*
import kotlin.random.Random
import kotlin.test.*

class StudyDashboardTest {
    private fun test(action:suspend (DurableStudy)->Unit)=runBlocking {
        val dir=Files.createTempDirectory("study-dashboard").toFile();val db=openProgressDatabase(dir.resolve("progress.db").path,BundledSQLiteDriver())
        try{val r=ProgressRepository(db);val study=DurableStudy(r,r.createProfile(),acceptedPracticeBank9J);study.initialize();action(study)}finally{db.close();dir.deleteRecursively()}
    }
    private fun answered(questions:List<AssessmentQuestion>,correct:Boolean=true,published:Boolean=true):StudyRecords {
        val rows=questions.mapIndexed{i,q->StoredQuestion("session",i,q.key.questionId.value,q.key.revision.value,q.conceptId,Json.encodeToString(q.options.map{it.id.value}),q.feedback.correctOptionId.value)}
        return StudyRecords(questions=rows,attempts=rows.mapIndexed{i,q->Attempt(i+1L,"event$i","session",i,if(correct)q.correctOption else questions[i].options.first{it.id.value!=q.correctOption}.id.value,published)})
    }
    @Test fun targetedPoolsRespectPublishedRevisionAndEmptyCapacity()=test {s->
        val q=acceptedQuestions9J.first();val draft=answered(listOf(q),correct=false,published=false)
        assertTrue(s.pool(ExerciseRequest(ExerciseMode.UNANSWERED),draft).any{it.key==q.key})
        assertTrue(s.pool(ExerciseRequest(ExerciseMode.REVIEW),draft).isEmpty())
        val published=answered(listOf(q),correct=false)
        assertEquals(listOf(q),s.pool(ExerciseRequest(ExerciseMode.REVIEW),published))
        assertFalse(s.pool(ExerciseRequest(ExerciseMode.UNANSWERED),published).any{it.key==q.key})
        val old=published.copy(questions=published.questions.map{it.copy(revision="old")})
        assertTrue(s.pool(ExerciseRequest(ExerciseMode.REVIEW),old).isEmpty())
        val all=answered(acceptedQuestions9J)
        assertTrue(s.pool(ExerciseRequest(ExerciseMode.UNANSWERED),all).isEmpty());assertTrue(s.pool(ExerciseRequest(ExerciseMode.REVIEW),all).isEmpty())
    }
    @Test fun oneConceptPoolCanOnlyStartOneQuestion()=test{s->
        val variants=acceptedQuestions9J.groupBy{it.conceptId}.values.first{it.size>1}
        val rest=answered(acceptedQuestions9J.filter{it.conceptId!=variants.first().conceptId})
        val request=ExerciseRequest(ExerciseMode.UNANSWERED)
        assertEquals(variants.size,s.pool(request,rest).size)
        assertEquals(1,selectExercise(s.bank,request,rest,s.catalog,1,Random(1)).size)
        assertFails{selectExercise(s.bank,request,rest,s.catalog,2)}
    }
    @Test fun mixedDistributionRemainsAndUnansweredVariantsArePreferred()=test{s->
        val answeredQuestions=acceptedQuestions9J.groupBy{it.conceptId}.values.map{it.first()}
        val records=answered(answeredQuestions)
        val selected=selectExercise(s.bank,ExerciseRequest(),records,s.catalog,70,Random(9))
        assertEquals(70,selected.size);assertEquals(70,selected.map{it.question.conceptId}.distinct().size)
        selected.forEach{snap->val group=acceptedQuestions9J.filter{it.conceptId==snap.question.conceptId}
            if(group.size>1)assertFalse(snap.question in answeredQuestions)}
        val allocation=QuizEngine.allocation(70)
        allocation.categories.forEach{(c,n)->assertTrue(selected.count{it.question.category==c}>=n)}
        assertFails{exercisePool(s.bank.copy(questions=s.bank.questions.drop(1)),ExerciseRequest(),records,s.catalog)}
    }
    @Test fun chapterAndCategoryPoolsUseAcceptedRelationships()=test{s->
        val m=readerModules.first();val chapter=s.pool(ExerciseRequest(ExerciseMode.CHAPTER,m.id.value),StudyRecords())
        assertTrue(chapter.isNotEmpty());assertTrue(chapter.all{it.relationship.primaryLessonId in m.lessonIds})
        val category=s.pool(ExerciseRequest(ExerciseMode.CATEGORY,category=Category.ENVIRONMENT),StudyRecords())
        assertTrue(category.isNotEmpty());assertTrue(category.all{it.category==Category.ENVIRONMENT})
    }
    @Test fun nextStepPrioritizesResumeThenActualReadingRecency()=test{s->
        assertEquals(readerModules.first().lessonIds.first(),dashboard(StudyRecords(),s).next.lesson)
        val first=readerDocuments.first{it.kind==DocumentKind.LESSON};val last=readerDocuments.last{it.kind==DocumentKind.LESSON}
        val records=StudyRecords(lessons=listOf(LessonProgress("p",first.id.value,first.revision.value),LessonProgress("p",last.id.value,last.revision.value)),metadata=listOf(StoreMetadata("opened:${first.id.value}","1"),StoreMetadata("opened:${last.id.value}","2")))
        assertEquals(last.id,dashboard(records,s).next.lesson)
        val state=s.start(TransientQuizState(countText="1"),ExerciseRequest())
        val withSession=s.repository.records(s.token)
        assertEquals(state.pinned!!.id,dashboard(withSession.copy(lessons=records.lessons,metadata=withSession.metadata+records.metadata),s).next.resume)
    }
    @Test fun allLessonsReadOffersReviewThenUnansweredWithoutLooping()=test{s->
        val lessons=readerDocuments.filter{it.kind==DocumentKind.LESSON}.map{LessonProgress("p",it.id.value,it.revision.value,true)}
        val progress=answered(acceptedQuestions9J.take(10),correct=false).copy(lessons=lessons)
        assertEquals(ExerciseMode.REVIEW,dashboard(progress,s).next.request!!.mode)
        val reviewed=progress.copy(metadata=listOf(StoreMetadata("reviewDone","10")))
        assertEquals(ExerciseMode.UNANSWERED,dashboard(reviewed,s).next.request!!.mode)
    }
    @Test fun completedChapterRecommendationTracksCompletionAndUnmark()=test{s->
        val m=readerModules.first()
        val lessons=m.lessonIds.map{id->LessonProgress("p",id.value,s.catalog.lessons.getValue(id.value),true)}
        val events=m.lessonIds.mapIndexed{i,id->StudyEvent("e$i","p",id.value,"read",100L+i)}
        val records=StudyRecords(lessons=lessons,events=events)
        assertEquals(1,dashboard(records,s).summary.chaptersRead)
        assertEquals(m.id.value,dashboard(records,s).next.request?.chapter)
        val practiced=records.copy(metadata=listOf(StoreMetadata("chapterPractice:${m.id.value}","103")))
        assertNotEquals(m.id.value,dashboard(practiced,s).next.request?.chapter)
        assertEquals(0,dashboard(records.copy(lessons=lessons.mapIndexed{i,l->if(i==0)l.copy(read=false) else l}),s).summary.chaptersRead)
    }
    @Test fun importingForgedAcceptedContentIsRejected()=test{s->
        val p=s.start(TransientQuizState(countText="1"),ExerciseRequest(ExerciseMode.UNANSWERED)).pinned!!
        val backup=decodeProgressBackup(s.repository.exportProgress(s.token))
        assertEquals(ExerciseMode.UNANSWERED,ExerciseRequest.decode(backup.records.value("mode:${p.id}")).mode)
        val session=backup.records.sessions.single();val snapshots=Json.decodeFromString<List<QuestionSnapshot>>(session.snapshot)
        val changed=session.copy(snapshot=Json.encodeToString(snapshots.map{it.copy(contentJson="forged")}))
        val forged=backup.copy(records=backup.records.copy(sessions=listOf(changed)))
        assertFails{s.validateImport(Json.encodeToString(forged))}
        assertEquals(backup,s.validateImport(Json.encodeToString(backup)))
    }

    @Test fun completingChapterPracticeSuppressesThatRecommendationAtomically()=test{s->
        val module=readerModules.first()
        module.lessonIds.forEach{id->s.repository.markLesson(s.token,id.value,s.catalog.lessons.getValue(id.value),true)}
        assertEquals(module.id.value,dashboard(s.repository.records(s.token),s).next.request?.chapter)
        var state=s.start(TransientQuizState(countText="1"),ExerciseRequest(ExerciseMode.CHAPTER,module.id.value))
        val p=state.pinned!!;state=s.confirm(p,p.assessment.current.displayedOptionIds.first());state=s.next(state.pinned!!)
        assertTrue(state.pinned!!.assessment.finished)
        val records=s.repository.records(s.token)
        assertNotNull(records.value("chapterPractice:${module.id.value}"))
        assertNotEquals(module.id.value,dashboard(records,s).next.request?.chapter)
    }
    @Test fun reopeningHistoryDoesNotReplaceAnUnfinishedExercise()=test{s->
        var state=s.start(TransientQuizState(countText="1"))
        val first=state.pinned!!;state=s.confirm(first,first.assessment.current.displayedOptionIds.first());s.next(state.pinned!!)
        val active=s.start(TransientQuizState(countText="1",feedback=Feedback.AT_END),ExerciseRequest(ExerciseMode.UNANSWERED)).pinned!!
        assertTrue(s.quizState(first.id).pinned!!.assessment.finished)
        assertEquals(active.id,s.active()!!.id)
        assertFalse(s.quizState(active.id).pinned!!.assessment.finished)
    }
}
