package se.korkort.progress

import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import java.nio.file.Files
import kotlinx.coroutines.runBlocking
import kotlin.test.*
import kotlinx.serialization.json.*

class ProgressRepositoryTest {
    private val question = QuestionSnapshot("q1","r1","concept1",listOf("b","a"),"a","{\"text\":\"Å Ä Ö\"}")
    private val catalog = ContentCatalog("pkg",mapOf("chapter" to listOf("lesson")),mapOf("lesson" to "r1"),mapOf("q1" to "r1"))
    private fun test(block: suspend (ProgressRepository, ProgressDatabase, String) -> Unit) = runBlocking {
        val directory = Files.createTempDirectory("progress-data-test").toFile()
        val path = directory.resolve("progress.db").absolutePath
        val db = openProgressDatabase(path,BundledSQLiteDriver())
        try { block(ProgressRepository(db),db,path) } finally { db.close(); directory.deleteRecursively() }
    }
    @Test fun migrationPreservesVersionOneRecords() = runBlocking {
        val directory=Files.createTempDirectory("progress-migration").toFile()
        val path=directory.resolve("v1.db").absolutePath
        try {
            val fixture=javaClass.getResourceAsStream("/schema-v1.json")!!.bufferedReader().use { it.readText() }
            val schema=Json.parseToJsonElement(fixture).jsonObject.getValue("database").jsonObject
            val connection=BundledSQLiteDriver().open(path)
            fun sql(value: String) { connection.prepare(value).use { it.step() } }
            try {
                for(entity in schema.getValue("entities").jsonArray) {
                    val e=entity.jsonObject
                    sql(e.getValue("createSql").jsonPrimitive.content.replace("\${TABLE_NAME}",e.getValue("tableName").jsonPrimitive.content))
                    for(index in e["indices"]?.jsonArray.orEmpty()) sql(index.jsonObject.getValue("createSql").jsonPrimitive.content.replace("\${TABLE_NAME}",e.getValue("tableName").jsonPrimitive.content))
                }
                for(query in schema.getValue("setupQueries").jsonArray) sql(query.jsonPrimitive.content)
                sql("INSERT INTO learner_profile VALUES ('profile','generation')")
                sql("INSERT INTO lesson_progress VALUES ('profile','lesson','r1',1,'block',23)")
                sql("PRAGMA user_version=1")
            } finally { connection.close() }
            val migrated=openProgressDatabase(path,BundledSQLiteDriver())
            try {
                assertEquals("generation",migrated.progress().profile("profile")!!.generation)
                assertEquals(23,migrated.progress().lessons("profile").single().offset)
                assertTrue(migrated.progress().lessons("profile").single().read)
            } finally { migrated.close() }
        } finally { directory.deleteRecursively() }
    }
    @Test fun readingAndQuestionsSurviveReopen() = test { repo,db,path ->
        val token=repo.createProfile()
        repo.setCatalog(token,catalog)
        repo.markLesson(token,"lesson","r1",true)
        repo.savePosition(token,"lesson","r1","block",42)
        val id=repo.start(token,"pkg",false,listOf(question))
        repo.confirm(token,id,0,0,"a","event1")
        repo.confirm(token,id,0,0,"a","event1")
        repo.finish(token,id,1)
        db.close()
        val reopened=openProgressDatabase(path,BundledSQLiteDriver())
        try {
            val r=ProgressRepository(reopened)
            assertEquals(token,r.createProfile())
            assertEquals(catalog,r.currentCatalog(token))
            assertEquals(ProgressSummary(1,1,1,1,1,1,1,0),r.summary(token,catalog))
            val (session,answers)=r.restore(token,id)
            assertTrue(session.snapshot.contains("Å Ä Ö"));assertEquals(1,answers.size)
            assertEquals(42,reopened.progress().lessons(token.profileId).single().offset)
        } finally { reopened.close() }
    }
    @Test fun deferredAnswersPublishOnlyOnCompletion() = test { r,_,_ ->
        val t=r.createProfile();val id=r.start(t,"pkg",true,listOf(question))
        r.confirm(t,id,0,0,"b","e1")
        assertEquals(0,r.summary(t,catalog).answered)
        r.finish(t,id,1)
        assertEquals(1,r.summary(t,catalog).revisit)
        val second=r.start(t,"pkg",false,listOf(question))
        r.confirm(t,second,0,0,"a","e2")
        val s=r.summary(t,catalog)
        assertEquals(1,s.answered);assertEquals(1,s.correct);assertEquals(0,s.revisit)
    }
    @Test fun abandonedDeferredAnswersRemainUnpublished() = test { r,_,_ ->
        val t=r.createProfile();val id=r.start(t,"pkg",true,listOf(question))
        r.confirm(t,id,0,0,"a","e1");r.finish(t,id,1,true)
        assertEquals(0,r.summary(t,catalog).answered)
    }
    @Test fun staleWritersAndInvalidOptionsCannotMutateData() = test { r,db,_ ->
        val t=r.createProfile();val id=r.start(t,"pkg",false,listOf(question))
        assertFailsWith<IllegalStateException>{r.start(t,"pkg",false,listOf(question))}
        assertFailsWith<IllegalArgumentException>{r.confirm(t,id,0,0,"foreign","e")}
        assertEquals(0,db.progress().answers(id).size)
        r.confirm(t,id,0,0,"a","e")
        assertFailsWith<IllegalStateException>{r.finish(t,id,0)}
        assertFailsWith<IllegalStateException>{r.confirm(t,id,0,0,"b","different")}
        assertFailsWith<IllegalStateException>{r.markLesson(t.copy(generation="old"),"lesson","r1",true)}
        assertEquals(1,r.summary(t,catalog).answered)
    }
    @Test fun contentRevisionsRequireExplicitEquivalence() = test { r,_,_ ->
        val t=r.createProfile();r.markLesson(t,"lesson","r1",true)
        val id=r.start(t,"pkg",false,listOf(question));r.confirm(t,id,0,0,"a","e")
        val updated=catalog.copy(lessons=mapOf("lesson" to "r2"),questions=mapOf("q1" to "r2"))
        assertEquals(0,r.summary(t,updated).answered);assertEquals(0,r.summary(t,updated).lessonsRead)
        val equivalent=updated.copy(equivalentLessonRevisions=mapOf("lesson@r1" to "r2"),equivalentQuestionRevisions=mapOf("q1@r1" to "r2"))
        assertEquals(1,r.summary(t,equivalent).answered);assertEquals(1,r.summary(t,equivalent).chaptersRead)
        r.markLesson(t,"lesson","r1",false)
        assertEquals(0,r.summary(t,equivalent).chaptersRead)
    }
    @Test fun conflictingEventRollsBackSessionVersion() = test { r,db,_ ->
        val t=r.createProfile();val id=r.start(t,"pkg",false,listOf(question));r.confirm(t,id,0,0,"a","same")
        r.finish(t,id,1)
        val next=r.start(t,"pkg",false,listOf(question))
        assertFails { r.confirm(t,next,0,0,"a","same") }
        assertEquals(0,db.progress().answers(next).size);assertEquals(0L,db.progress().session(next)!!.version)
    }
}
