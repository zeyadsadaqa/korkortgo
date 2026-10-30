package se.korkort

import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import java.nio.file.Files
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.CompletableDeferred
import kotlin.test.*
import se.korkort.progress.*

class DurableStudyTest {
    @Test fun restartRetainsCursorOptionsAndDeferredFeedback(): Unit = runBlocking {
        val dir=Files.createTempDirectory("durable-study").toFile()
        val path=dir.resolve("progress.db").absolutePath
        var db=openProgressDatabase(path,BundledSQLiteDriver())
        try {
            var repo=ProgressRepository(db)
            val token=repo.createProfile()
            var study=DurableStudy(repo,token,acceptedPracticeBank9J)
            study.initialize()
            var state=study.start(TransientQuizState(countText="2",feedback=Feedback.AT_END).showSetup())
            val original=state.pinned!!
            val chosen=original.assessment.current.displayedOptionIds.first()
            state=study.confirm(original,chosen)
            assertNull(state.pinned!!.assessment.presentation().explanation)
            assertEquals(0,repo.summary(token,study.catalog).answered)
            db.close()
            db=openProgressDatabase(path,BundledSQLiteDriver())
            repo=ProgressRepository(db);study=DurableStudy(repo,repo.createProfile(),acceptedPracticeBank9J)
            val restored=study.active()!!
            assertEquals(original.id,restored.id)
            assertEquals(original.assessment.snapshots,restored.assessment.snapshots)
            assertEquals(chosen,restored.assessment.currentAnswer!!.selectedOptionId)
            state=study.next(restored)
            val second=state.pinned!!
            assertEquals(1,second.assessment.index)
            assertEquals(1,repo.cursor(token,second.id))
            assertEquals(state,study.next(restored)) // Retried advance cannot skip a question.
            state=study.confirm(second,second.assessment.current.displayedOptionIds.first())
            state=study.next(state.pinned!!)
            assertTrue(state.pinned!!.assessment.finished)
            assertNotNull(state.pinned!!.assessment.score)
            assertEquals(2,repo.summary(token,study.catalog).answered)
            assertEquals(state,study.next(state.pinned!!)) // Completion retry is idempotent.
        } finally {db.close();dir.deleteRecursively()}
    }
    @Test fun endRetainsImmediateCoverageAndClearsResume(): Unit = runBlocking {
        val dir=Files.createTempDirectory("durable-end").toFile()
        val db=openProgressDatabase(dir.resolve("progress.db").absolutePath,BundledSQLiteDriver())
        try {
            val repo=ProgressRepository(db);val token=repo.createProfile()
            val study=DurableStudy(repo,token,acceptedPracticeBank9J)
            val state=study.start(TransientQuizState(countText="2").showSetup())
            study.confirm(state.pinned!!,state.pinned!!.assessment.current.displayedOptionIds.first())
            study.endActive();study.endActive()
            assertNull(study.active());assertEquals(1,repo.summary(token,study.catalog).answered)
        } finally {db.close();dir.deleteRecursively()}
    }
    @Test fun failedConfirmationCanBeRetriedAfterReopeningStore(): Unit = runBlocking {
        val dir=Files.createTempDirectory("durable-retry").toFile()
        val path=dir.resolve("progress.db").absolutePath
        var db=openProgressDatabase(path,BundledSQLiteDriver())
        try {
            var repo=ProgressRepository(db);val token=repo.createProfile()
            var study=DurableStudy(repo,token,acceptedPracticeBank9J)
            val p=study.start(TransientQuizState(countText="1").showSetup()).pinned!!
            val option=p.assessment.current.displayedOptionIds.first()
            db.close()
            assertFails { study.confirm(p,option) }
            assertNull(p.assessment.currentAnswer)
            db=openProgressDatabase(path,BundledSQLiteDriver());repo=ProgressRepository(db)
            study=DurableStudy(repo,token,acceptedPracticeBank9J)
            val resumed=study.active()!!
            assertNull(resumed.assessment.currentAnswer)
            study.confirm(resumed,option);study.confirm(resumed,option)
            assertEquals(1,repo.restore(token,p.id).second.size)
        } finally {db.close();dir.deleteRecursively()}
    }
    @Test fun readingWritesQueueBehindAnActiveSave(): Unit = runBlocking {
        val dir=Files.createTempDirectory("durable-queue").toFile()
        val db=openProgressDatabase(dir.resolve("progress.db").absolutePath,BundledSQLiteDriver())
        try {
            val repo=ProgressRepository(db)
            val environment=StudyEnvironment(DurableStudy(repo,repo.createProfile(),acceptedPracticeBank9J),this)
            val entered=CompletableDeferred<Unit>();val release=CompletableDeferred<Unit>();val finished=CompletableDeferred<Unit>()
            val order=mutableListOf<Int>()
            environment.save {entered.complete(Unit);release.await();order.add(1)}
            entered.await();assertTrue(environment.busy)
            environment.position {order.add(2);finished.complete(Unit)}
            release.complete(Unit);finished.await()
            assertEquals(listOf(1,2),order)
            assertFalse(environment.busy)
        } finally {db.close();dir.deleteRecursively()}
    }
    @Test fun rejectedBankCannotEnterDurableRoutes(): Unit = runBlocking {
        val dir=Files.createTempDirectory("durable-bank").toFile()
        val db=openProgressDatabase(dir.resolve("progress.db").absolutePath,BundledSQLiteDriver())
        try {
            val repo=ProgressRepository(db)
            assertFailsWith<IllegalArgumentException>{DurableStudy(repo,repo.createProfile(),acceptedPracticeBank9J.copy(releaseAccepted=false))}
        } finally {db.close();dir.deleteRecursively()}
    }
}
