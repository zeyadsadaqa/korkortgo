@file:OptIn(kotlin.uuid.ExperimentalUuidApi::class, kotlin.time.ExperimentalTime::class)
package se.korkort.progress

import androidx.room3.withWriteTransaction
import kotlinx.coroutines.flow.map
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlin.uuid.Uuid

@Serializable
data class QuestionSnapshot(val id: String, val revision: String, val concept: String,
    val options: List<String>, val correctOption: String, val contentJson: String) {
    init { require(id.isNotBlank() && revision.isNotBlank() && concept.isNotBlank())
        require(options.size >= 2 && options.distinct().size == options.size && correctOption in options) }
}
@Serializable
data class ContentCatalog(val packageId: String, val chapters: Map<String, List<String>>,
    val lessons: Map<String, String>, val questions: Map<String, String>,
    val equivalentLessonRevisions: Map<String, String> = emptyMap(),
    val equivalentQuestionRevisions: Map<String, String> = emptyMap()) {
    init { require(packageId.isNotBlank()); require(chapters.values.all { it.isNotEmpty() && it.distinct().size == it.size && lessons.keys.containsAll(it) }) }
}
data class WriteToken(val profileId: String, val generation: String)
data class ProgressSummary(val chaptersRead: Int, val chaptersTotal: Int, val lessonsRead: Int,
    val lessonsTotal: Int, val answered: Int, val questionTotal: Int, val correct: Int, val revisit: Int)

/** Phase-2 data boundary. Callers supply authenticated accepted content through the phase-3 adapter. */
class ProgressRepository(internal val db: ProgressDatabase) {
    internal val dao = db.progress()
    private val json = Json
    private fun now() = kotlin.time.Clock.System.now().toEpochMilliseconds()
    private fun newId() = Uuid.random().toString()
    internal suspend fun checkToken(token: WriteToken) {
        check(dao.profile(token.profileId)?.generation == token.generation) { "Stale learner generation" }
    }
    internal suspend fun changed() { dao.metadata(StoreMetadata("change", newId())) }
    suspend fun createProfile(): WriteToken = db.withWriteTransaction {
        dao.localProfile()?.let { return@withWriteTransaction WriteToken(it.id,it.generation) }
        val p = Profile(newId(), newId()); dao.insertProfile(p); changed(); WriteToken(p.id, p.generation)
    }
    suspend fun setCatalog(token: WriteToken, catalog: ContentCatalog) = db.withWriteTransaction {
        checkToken(token)
        dao.metadata(StoreMetadata("catalog:${token.profileId}", json.encodeToString(catalog)))
        changed()
    }
    suspend fun currentCatalog(token: WriteToken): ContentCatalog? = db.withWriteTransaction {
        checkToken(token)
        dao.metadataByKey("catalog:${token.profileId}")?.let { json.decodeFromString<ContentCatalog>(it.value) }
    }
    suspend fun markLesson(token: WriteToken, id: String, revision: String, read: Boolean) = db.withWriteTransaction {
        checkToken(token)
        require(id.isNotBlank() && revision.isNotBlank())
        val old = dao.lessons(token.profileId).find { it.lessonId == id && it.revision == revision }
        dao.clearLesson(token.profileId,id)
        dao.saveLesson((old ?: LessonProgress(token.profileId, id, revision)).copy(read = read))
        val previousOrder=dao.metadataByKey("studyOrder")?.value?.toLongOrNull() ?: (dao.events(token.profileId).maxOfOrNull{it.occurredAt} ?: 0)
        val order=maxOf(previousOrder,now())+1;require(order>0)
        dao.metadata(StoreMetadata("studyOrder",order.toString()))
        if(read)dao.metadata(StoreMetadata("readOrder:$id",order.toString()))
        dao.insertEvent(StudyEvent(newId(), token.profileId, id, if(read) "read" else "unread",now())); changed()
    }
    suspend fun savePosition(token: WriteToken, id: String, revision: String, block: String, offset: Int) = db.withWriteTransaction {
        checkToken(token); require(offset >= 0 && block.isNotBlank())
        val old = dao.lessons(token.profileId).find { it.lessonId == id && it.revision == revision }
        dao.saveLesson((old ?: LessonProgress(token.profileId, id, revision)).copy(blockId = block, offset = offset)); changed()
    }
    suspend fun start(token: WriteToken, packageId: String, deferred: Boolean, questions: List<QuestionSnapshot>, mode: String? = null): String = db.withWriteTransaction {
        checkToken(token); check(dao.active(token.profileId).isEmpty()) { "An unfinished exercise exists" }
        require(questions.size in 1..70 && packageId.isNotBlank())
        require(questions.map { it.id }.distinct().size == questions.size)
        require(questions.map { it.concept }.distinct().size == questions.size)
        val id = newId()
        dao.insertSession(Session(id, token.profileId, packageId, deferred, json.encodeToString(questions), createdAt=now()))
        dao.insertQuestions(questions.mapIndexed { i,q -> StoredQuestion(id,i,q.id,q.revision,q.concept,json.encodeToString(q.options),q.correctOption) })
        mode?.let { dao.metadata(StoreMetadata("mode:$id",it)) }
        changed(); id
    }
    suspend fun confirm(token: WriteToken, sessionId: String, version: Long, position: Int, option: String, eventId: String) = db.withWriteTransaction {
        checkToken(token); require(eventId.isNotBlank())
        val s = checkNotNull(dao.session(sessionId)); check(s.profileId == token.profileId)
        val previous = dao.answers(sessionId).find { it.position == position }
        if (previous != null) {
            check(previous.eventId == eventId && previous.selectedOption == option) { "Conflicting repeated answer" }
        } else {
            check(s.status == "active" && s.version == version) { "Stale session writer" }
            check(position == dao.answers(sessionId).size) { "Answers must follow snapshot order" }
            val q = dao.questions(sessionId).getOrNull(position) ?: error("Unknown question position")
            require(option in json.decodeFromString<List<String>>(q.optionsJson))
            dao.insertAttempt(Attempt(eventId=eventId,sessionId=sessionId,position=position,selectedOption=option,published=!s.deferred,confirmedAt=now()))
            check(dao.transition(sessionId,version,"active") == 1); changed()
        }
    }
    suspend fun finish(token: WriteToken, id: String, version: Long, abandon: Boolean = false, metadata: List<StoreMetadata> = emptyList()) = db.withWriteTransaction {
        checkToken(token); val s = checkNotNull(dao.session(id))
        check(s.profileId == token.profileId && s.status == "active" && s.version == version)
        if (!abandon) check(dao.answers(id).size == dao.questions(id).size) { "Exercise incomplete" }
        check(dao.transition(id,version,if(abandon) "abandoned" else "completed") == 1)
        if (!abandon) {dao.publish(id);metadata.forEach{dao.metadata(it)}}
        dao.insertEvent(StudyEvent(newId(),token.profileId,id,if(abandon) "abandoned" else "completed",now())); changed()
    }
    suspend fun restore(token: WriteToken, id: String): Pair<Session,List<Attempt>> = db.withWriteTransaction {
        checkToken(token); val s = checkNotNull(dao.session(id)); check(s.profileId == token.profileId)
        s to dao.answers(id)
    }
    suspend fun activeSession(token: WriteToken): Session? = db.withWriteTransaction {
        checkToken(token); dao.active(token.profileId).singleOrNull()
    }
    suspend fun lessons(token: WriteToken): List<LessonProgress> = db.withWriteTransaction {
        checkToken(token); dao.lessons(token.profileId)
    }
    suspend fun cursor(token: WriteToken, id: String): Int = db.withWriteTransaction {
        checkToken(token); check(dao.session(id)?.profileId == token.profileId)
        dao.metadataByKey("cursor:$id")?.value?.toInt() ?: 0
    }
    suspend fun advance(token: WriteToken, id: String, position: Int, version: Long) = db.withWriteTransaction {
        checkToken(token); val s=checkNotNull(dao.session(id)); check(s.profileId==token.profileId)
        val cursor=dao.metadataByKey("cursor:$id")?.value?.toInt() ?: 0
        if(cursor!=position+1) {
            check(cursor==position && s.status=="active" && s.version==version)
            check(dao.answers(id).any { it.position==position })
            check(position+1 < dao.questions(id).size)
            check(dao.transition(id,version,"active")==1)
            dao.metadata(StoreMetadata("cursor:$id",(position+1).toString())); changed()
        }
    }
    suspend fun history(token: WriteToken, limit: Int = 20, offset: Int = 0): List<Session> = db.withWriteTransaction {
        checkToken(token); require(limit in 1..100 && offset >= 0); dao.history(token.profileId,limit,offset)
    }
    fun observeLessons(token: WriteToken) = dao.observeMetadata().map { lessons(token) }
    fun observeSummary(token: WriteToken, catalog: ContentCatalog) = dao.observeMetadata().map { summary(token,catalog) }
    suspend fun summary(token: WriteToken, catalog: ContentCatalog): ProgressSummary = db.withWriteTransaction {
        checkToken(token)
        val read = dao.lessons(token.profileId).filter { it.read &&
            (catalog.lessons[it.lessonId] == it.revision || catalog.equivalentLessonRevisions["${it.lessonId}@${it.revision}"] == catalog.lessons[it.lessonId] && it.lessonId in catalog.lessons) }.map { it.lessonId }.toSet()
        val latest = linkedMapOf<String,Pair<StoredQuestion,Attempt>>()
        for(a in dao.attempts(token.profileId).filter { it.published }) {
            val q = dao.questions(a.sessionId).first { it.position == a.position }
            val current = catalog.questions[q.questionId] ?: continue
            if(q.revision == current || catalog.equivalentQuestionRevisions["${q.questionId}@${q.revision}"] == current) latest[q.questionId] = q to a
        }
        val correct = latest.values.count { (q,a) -> q.correctOption == a.selectedOption }
        ProgressSummary(catalog.chapters.values.count { read.containsAll(it) },catalog.chapters.size,read.size,catalog.lessons.size,
            latest.size,catalog.questions.size,correct,latest.size-correct)
    }
}
