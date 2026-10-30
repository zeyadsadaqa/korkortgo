package se.korkort

import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import java.nio.file.Files
import kotlinx.coroutines.*
import se.korkort.progress.*
import kotlinx.serialization.json.Json
import kotlin.test.*

class SavingRecoveryTest {
    private fun test(action:suspend (DurableStudy,ProgressRepository,String)->Unit)=runBlocking {
        val dir=Files.createTempDirectory("saving-recovery").toFile();val path=dir.resolve("progress.db").path
        val db=openProgressDatabase(path,BundledSQLiteDriver())
        try{val r=ProgressRepository(db);val s=DurableStudy(r,r.createProfile(),acceptedPracticeBank9J);s.initialize();action(s,r,path)}finally{db.close();dir.deleteRecursively()}
    }
    @Test fun staleWindowCannotConfirmAfterAnotherWindowPauses()=test{s,r,path->
        val shown=s.start(TransientQuizState(countText="1",feedback=Feedback.AT_END)).pinned!!
        val otherDb=openProgressDatabase(path,BundledSQLiteDriver())
        try {
            val other=DurableStudy(ProgressRepository(otherDb),s.token,acceptedPracticeBank9J)
            other.pause(other.active()!!)
            assertFailsWith<StaleSessionWrite>{s.confirm(shown,shown.token.displayedOptionIds.first())}
            assertTrue(r.restore(s.token,shown.id).second.isEmpty())
            val resumed=s.quizState(shown.id).pinned!!
            assertFalse(resumed.paused);assertEquals(shown.assessment.snapshots,resumed.assessment.snapshots)
            s.confirm(resumed,resumed.token.displayedOptionIds.first())
            assertEquals(0,r.summary(s.token,s.catalog).answered)
        }finally{otherDb.close()}
    }
    @Test fun staleWindowCannotAdvancePastAnUnseenConfirmation()=test{s,r,_->
        val shown=s.start(TransientQuizState(countText="2")).pinned!!
        val confirmed=s.confirm(shown,shown.token.displayedOptionIds.first()).pinned!!
        assertFailsWith<StaleSessionWrite>{s.next(shown)}
        assertEquals(0,r.cursor(s.token,shown.id))
        val next=s.next(confirmed).pinned!!;assertEquals(1,next.assessment.index)
        assertEquals(next,s.next(confirmed).pinned) // Same committed advance is a safe retry.
    }
    @Test fun pausedBackupRestoresExactOrderAndFeedback()=test{s,r,_->
        val shown=s.start(TransientQuizState(countText="1",feedback=Feedback.AT_END)).pinned!!
        s.pause(shown)
        val backup=s.validateImport(r.exportProgress(s.token));assertEquals(2,backup.version)
        val token=r.replaceProgress(s.token,s.catalog,backup.records)
        val reopened=DurableStudy(r,token,acceptedPracticeBank9J)
        assertTrue(reopened.active()!!.paused)
        val resumed=reopened.quizState(shown.id).pinned!!
        assertEquals(shown.assessment.snapshots,resumed.assessment.snapshots)
        assertEquals(Feedback.AT_END,resumed.assessment.feedbackMode);assertFalse(resumed.paused)
        val v1=backup.copy(version=1)
        assertEquals(1,reopened.validateImport(Json.encodeToString(v1)).version)
    }
    @Test fun unavailableSavedPackageIsArchivedWithoutPublishing()=test{s,r,_->
        val q=acceptedQuestions9J.first();val options=q.options.map{it.id.value}
        val id=r.start(s.token,"retired-package",true,listOf(QuestionSnapshot(q.key.questionId.value,q.key.revision.value,q.conceptId,options,q.feedback.correctOptionId.value,q.toString())))
        r.confirm(s.token,id,0,0,options.first(),"old-answer")
        s.initialize()
        assertNull(r.activeSession(s.token));assertTrue(s.invalidatedExercise)
        val records=r.records(s.token)
        assertEquals("1",records.value("unavailable:$id"));assertEquals("abandoned",records.sessions.single().status)
        assertFalse(records.attempts.single().published);assertEquals(0,records.summary(s.catalog).answered)
    }
    @Test fun unavailableArtworkNeverProducesAResumedQuestion()=test{s,r,_->
        val q=acceptedQuestions9J.first{it.image!=null};val options=q.options.map{it.id.value}
        r.start(s.token,s.packageId,true,listOf(QuestionSnapshot(q.key.questionId.value,q.key.revision.value,q.conceptId,options,q.feedback.correctOptionId.value,q.toString())))
        val missing=DurableStudy(r,s.token,acceptedPracticeBank9J){throw IllegalArgumentException("missing artwork")}
        missing.initialize();assertNull(missing.active());assertTrue(missing.invalidatedExercise)
    }
    @Test fun backgroundFlushRunsBeforePauseWrite()=test{s,_,_->
        val order=mutableListOf<String>();val done=CompletableDeferred<Unit>()
        coroutineScope {
            val environment=StudyEnvironment(s,this)
            val unregister=environment.registerPositionFlush {environment.position{order.add("position")}}
            environment.background{order.add("pause");done.complete(Unit)}
            done.await();unregister()
            assertEquals(listOf("position","pause"),order)
        }
    }
    @Test fun simultaneousResumeAndImportShareSerializedAssetChecks()=test{s,r,_->
        val q=acceptedQuestions9J.first{it.image!=null};val options=q.options.map{it.id.value}
        val id=r.start(s.token,s.packageId,true,listOf(QuestionSnapshot(q.key.questionId.value,q.key.revision.value,q.conceptId,options,q.feedback.correctOptionId.value,q.toString())))
        val backup=r.exportProgress(s.token)
        val checks=java.util.concurrent.atomic.AtomicInteger()
        val shared=DurableStudy(r,s.token,acceptedPracticeBank9J){checks.incrementAndGet();delay(10)}
        coroutineScope {
            val resume=async(Dispatchers.Default){shared.restore(id)}
            val imported=async(Dispatchers.Default){shared.validateImport(backup)}
            resume.await();imported.await()
        }
        val ids=(listOfNotNull(q.image?.assetId)+q.options.mapNotNull{it.image?.assetId}).distinct()
        assertEquals(ids.size,checks.get())
    }
}
