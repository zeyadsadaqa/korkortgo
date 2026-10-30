package se.korkort.progress

import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import java.nio.file.Files
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.Json
import kotlin.test.*

class ProgressTransferTest {
    private val q=QuestionSnapshot("q","r","concept",listOf("a","b"),"a","accepted")
    private val catalog=ContentCatalog("pkg",mapOf("chapter" to listOf("lesson")),mapOf("lesson" to "r"),mapOf("q" to "r"))
    private fun test(action:suspend (ProgressRepository,String)->Unit)=runBlocking {
        val dir=Files.createTempDirectory("transfer-test").toFile();val path=dir.resolve("progress.db").path
        val db=openProgressDatabase(path,BundledSQLiteDriver())
        try {action(ProgressRepository(db),path)}finally{db.close();dir.deleteRecursively()}
    }
    @Test fun roundTripKeepsDeferredSnapshotCursorAndRejectsOldGeneration()=test{r,path->
        val old=r.createProfile();r.setCatalog(old,catalog);r.recordOpen(old,"lesson","r");r.markLesson(old,"lesson","r",true);r.savePosition(old,"lesson","r","block",17)
        val id=r.start(old,"pkg",true,listOf(q),"REVIEW||");r.confirm(old,id,0,0,"b","event")
        val backup=decodeProgressBackup(r.exportProgress(old));assertEquals(0,backup.records.summary(catalog).answered)
        val next=r.replaceProgress(old,catalog,backup.records)
        assertNotEquals(old.generation,next.generation);assertEquals(backup.records,r.records(next))
        assertFailsWith<IllegalStateException>{r.savePosition(old,"lesson","r","wrong",0)}
        val reopened=openProgressDatabase(path,BundledSQLiteDriver())
        try {val repo=ProgressRepository(reopened);assertEquals(next,repo.createProfile());assertEquals(17,repo.lessons(next).single().offset);assertEquals("REVIEW||",repo.records(next).value("mode:$id"))}finally{reopened.close()}
    }
    @Test fun resetClearsEveryLearnerRecordButRetainsCatalogue()=test{r,_->
        val t=r.createProfile();r.setCatalog(t,catalog);r.recordOpen(t,"lesson","r");r.markLesson(t,"lesson","r",true)
        val id=r.start(t,"pkg",false,listOf(q));r.confirm(t,id,0,0,"a","e")
        val next=r.replaceProgress(t,catalog)
        assertEquals(StudyRecords(),r.records(next));assertEquals(catalog,r.currentCatalog(next))
        assertFailsWith<IllegalStateException>{r.confirm(t,id,0,0,"a","e")}
    }
    @Test fun replacementFailureRollsBackDeletionAndGeneration()=test{r,path->
        val t=r.createProfile();r.setCatalog(t,catalog);r.markLesson(t,"lesson","r",true)
        val before=r.records(t)
        val connection=BundledSQLiteDriver().open(path)
        try {connection.prepare("CREATE TRIGGER refuse_import BEFORE INSERT ON lesson_progress WHEN NEW.offset=99 BEGIN SELECT RAISE(ABORT,'injected'); END").use{it.step()}}finally{connection.close()}
        assertFails{r.replaceProgress(t,catalog,before.copy(lessons=before.lessons.map{it.copy(offset=99)}))}
        assertEquals(t,r.createProfile());assertEquals(before,r.records(t))
    }
    @Test fun malformedFilesNeverMutateTheStore()=test{r,_->
        val t=r.createProfile();r.setCatalog(t,catalog);r.markLesson(t,"lesson","r",true)
        val before=r.records(t)
        assertFails{decodeProgressBackup("{")}
        assertFails{decodeProgressBackup("{}")}
        assertFails{decodeProgressBackup("[".repeat(65)+"]".repeat(65))}
        assertFails{decodeProgressBackup(Json.encodeToString(ProgressBackup(version=999,exportedAt=0,catalog=catalog,records=before)))}
        assertFails{r.replaceProgress(t,catalog,before.copy(lessons=before.lessons+before.lessons))}
        assertEquals(before,r.records(t))
    }
    @Test fun forgedPublicationAndBrokenSessionInvariantsAreRejected()=test{r,_->
        val t=r.createProfile();r.setCatalog(t,catalog);val id=r.start(t,"pkg",true,listOf(q));r.confirm(t,id,0,0,"b","e")
        val saved=r.records(t)
        assertFails{validateRecords(saved.copy(attempts=saved.attempts.map{it.copy(published=true)}))}
        assertFails{validateRecords(saved.copy(questions=emptyList()))}
        assertFails{validateRecords(saved.copy(sessions=saved.sessions+saved.sessions.single().copy(id="other")))}
        assertFails{validateRecords(saved.copy(attempts=saved.attempts.map{it.copy(selectedOption="foreign")}))}
        assertFails{validateRecords(saved.copy(metadata=listOf(StoreMetadata("cursor:$id","5"))))}
        r.finish(t,id,1,true);assertEquals(0,r.records(t).summary(catalog).answered)
    }
    @Test fun readingOrderChangesOnOpenNotOnPositionSave()=test{r,_->
        val t=r.createProfile();r.setCatalog(t,catalog)
        r.recordOpen(t,"lesson","r");val order=r.records(t).value("opened:lesson")
        r.savePosition(t,"lesson","r","block",100);assertEquals(order,r.records(t).value("opened:lesson"))
        r.recordOpen(t,"lesson","r");assertTrue(r.records(t).value("opened:lesson")!!.toLong()>order!!.toLong())
    }

    @Test fun completionOrderDoesNotMoveBackWithTheWallClock()=test{r,_->
        val t=r.createProfile();r.setCatalog(t,catalog)
        r.setValue(t,"studyOrder","9000000000000")
        r.markLesson(t,"lesson","r",true)
        assertTrue(r.records(t).value("readOrder:lesson")!!.toLong()>9000000000000)
        val before=r.records(t).value("readOrder:lesson")!!.toLong()
        r.markLesson(t,"lesson","r",false);r.markLesson(t,"lesson","r",true)
        assertTrue(r.records(t).value("readOrder:lesson")!!.toLong()>before)
    }
}
