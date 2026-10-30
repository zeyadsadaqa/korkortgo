@file:OptIn(kotlin.uuid.ExperimentalUuidApi::class, kotlin.time.ExperimentalTime::class, kotlinx.serialization.ExperimentalSerializationApi::class)
package se.korkort.progress

import androidx.room3.withWriteTransaction
import kotlinx.coroutines.flow.map
import kotlinx.serialization.Serializable
import kotlinx.serialization.EncodeDefault
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.Json
import kotlin.uuid.Uuid

const val MAX_BACKUP_BYTES = 32 * 1024 * 1024
@Serializable data class StudyRecords(
    val lessons: List<LessonProgress> = emptyList(), val sessions: List<Session> = emptyList(),
    val questions: List<StoredQuestion> = emptyList(), val attempts: List<Attempt> = emptyList(),
    val events: List<StudyEvent> = emptyList(), val metadata: List<StoreMetadata> = emptyList(),
) {
    fun value(key:String) = metadata.singleOrNull { it.key==key }?.value
    fun latest(catalog:ContentCatalog): Map<String,Pair<StoredQuestion,Attempt>> {
        val questionsByPosition=questions.associateBy { it.sessionId to it.position }
        return buildMap {
            attempts.sortedBy { it.sequence }.filter { it.published }.forEach { a ->
                val q=questionsByPosition[a.sessionId to a.position] ?: return@forEach
                val revision=catalog.questions[q.questionId] ?: return@forEach
                if(q.revision==revision || catalog.equivalentQuestionRevisions["${q.questionId}@${q.revision}"]==revision) put(q.questionId,q to a)
            }
        }
    }
    fun summary(catalog:ContentCatalog): ProgressSummary {
        val read=lessons.filter { it.read && (catalog.lessons[it.lessonId]==it.revision ||
            it.lessonId in catalog.lessons && catalog.equivalentLessonRevisions["${it.lessonId}@${it.revision}"]==catalog.lessons[it.lessonId]) }.map { it.lessonId }.toSet()
        val latest=latest(catalog);val correct=latest.values.count { (q,a)->q.correctOption==a.selectedOption }
        return ProgressSummary(catalog.chapters.values.count {read.containsAll(it)},catalog.chapters.size,read.size,catalog.lessons.size,latest.size,catalog.questions.size,correct,latest.size-correct)
    }
}
@Serializable data class ProgressBackup(@EncodeDefault val format:String="korkortgo-progress",@EncodeDefault val version:Int=1,
    val exportedAt:Long, val catalog:ContentCatalog, val records:StudyRecords)

/** Structural validation is independent of app-level authentication of authored question content. */
fun decodeProgressBackup(text:String): ProgressBackup {
    require(text.length<=MAX_BACKUP_BYTES && text.encodeToByteArray().size<=MAX_BACKUP_BYTES) {"File is too large"}
    var depth=0;var quoted=false;var escaped=false
    for(c in text) {
        if(quoted) {if(escaped)escaped=false else if(c=='\\')escaped=true else if(c=='"')quoted=false}
        else if(c=='"')quoted=true else if(c=='{' || c=='['){depth++;require(depth<=64){"File nesting is too deep"}} else if(c=='}' || c==']')depth--
    }
    val envelope=Json.parseToJsonElement(text).jsonObject
    require(envelope["format"]?.jsonPrimitive?.content=="korkortgo-progress" && envelope["version"]?.jsonPrimitive?.content=="1") {"Unsupported progress format"}
    val backup=Json.decodeFromString<ProgressBackup>(text)
    require(backup.format=="korkortgo-progress" && backup.version==1 && backup.exportedAt>=0) {"Unsupported progress format"}
    validateRecords(backup.records)
    return backup
}
fun validateRecords(r:StudyRecords) {
    require(r.lessons.size<=10_000 && r.sessions.size<=10_000 && r.questions.size<=100_000 && r.attempts.size<=100_000 && r.events.size<=100_000 && r.metadata.size<=30_000)
    require(r.lessons.distinctBy { it.lessonId to it.revision }.size==r.lessons.size)
    require(r.lessons.all {it.lessonId.isNotBlank() && it.revision.isNotBlank() && it.offset>=0})
    require(r.sessions.distinctBy {it.id}.size==r.sessions.size && r.sessions.count{it.status=="active"}<=1)
    require(r.questions.distinctBy {it.sessionId to it.position}.size==r.questions.size)
    require(r.attempts.distinctBy {it.eventId}.size==r.attempts.size && r.attempts.distinctBy{it.sessionId to it.position}.size==r.attempts.size)
    require(r.attempts.map{it.sequence}.distinct().size==r.attempts.size && r.attempts.all{it.sequence in 1..Long.MAX_VALUE-1_000_000 && it.confirmedAt>=0})
    require(r.events.distinctBy{it.id}.size==r.events.size && r.events.all{it.id.isNotBlank() && it.occurredAt>=0 && it.kind in setOf("read","unread","completed","abandoned")})
    require(r.metadata.distinctBy{it.key}.size==r.metadata.size)
    val ids=r.sessions.map{it.id}.toSet()
    require(r.questions.all{it.sessionId in ids} && r.attempts.all{it.sessionId in ids})
    r.sessions.forEach { s ->
        require(s.id.isNotBlank() && s.packageId.isNotBlank() && s.status in setOf("active","completed","abandoned") && s.version in 0..Long.MAX_VALUE-1_000_000 && s.createdAt>=0)
        val snapshots=Json.decodeFromString<List<QuestionSnapshot>>(s.snapshot)
        require(snapshots.size in 1..70 && snapshots.distinctBy{it.id}.size==snapshots.size && snapshots.distinctBy{it.concept}.size==snapshots.size)
        val qs=r.questions.filter{it.sessionId==s.id}.sortedBy{it.position}
        require(qs.size==snapshots.size)
        qs.forEachIndexed { i,q -> val p=snapshots[i]
            require(q.position==i && q.questionId==p.id && q.revision==p.revision && q.conceptId==p.concept && q.correctOption==p.correctOption && Json.decodeFromString<List<String>>(q.optionsJson)==p.options)
        }
        val answers=r.attempts.filter{it.sessionId==s.id}.sortedBy{it.sequence}
        require(answers.size<=qs.size && answers.map{it.position}==answers.indices.toList())
        answers.forEach {a->require(a.eventId.isNotBlank() && a.selectedOption in snapshots[a.position].options)
            require(a.published==(!s.deferred || s.status=="completed")) }
        if(s.status=="completed")require(answers.size==qs.size)
        if(s.status=="active") {
            val cursor=r.value("cursor:${s.id}")?.toIntOrNull() ?: 0
            require(cursor in qs.indices && answers.size in cursor..cursor+1)
        }
    }
    r.metadata.forEach {m->
        require(m.key.length<=300 && m.value.length<=20_000)
        require(m.key=="openOrder" || m.key=="studyOrder" || m.key.startsWith("readOrder:") || m.key.startsWith("opened:") || m.key.startsWith("chapterPractice:") || m.key=="reviewDone" || m.key.startsWith("mode:") || m.key.startsWith("cursor:"))
        if(m.key.startsWith("mode:") || m.key.startsWith("cursor:"))require(m.key.substringAfter(':') in ids)
        if(m.key.startsWith("cursor:"))require(m.value.toIntOrNull()?.let{it in 0..69}==true)
        if(m.key=="openOrder" || m.key=="studyOrder" || m.key.startsWith("readOrder:") || m.key.startsWith("opened:"))require(m.value.toLongOrNull()?.let{it in 0..Long.MAX_VALUE-10000}==true)
        if(m.key=="openOrder" || m.key=="studyOrder" || m.key.startsWith("readOrder:") || m.key.startsWith("opened:") || m.key=="reviewDone" || m.key.startsWith("chapterPractice:"))require((m.value.toLongOrNull() ?: -1)>=0)
    }
}

suspend fun ProgressRepository.records(token:WriteToken): StudyRecords = db.withWriteTransaction {
    checkToken(token)
    StudyRecords(dao.lessons(token.profileId),dao.sessions(token.profileId),dao.allQuestions(token.profileId),dao.attempts(token.profileId),dao.events(token.profileId),
        dao.allMetadata().filter {it.key!="change" && !it.key.startsWith("catalog:")})
}
fun ProgressRepository.observeRecords(token:WriteToken)=dao.observeMetadata().map {records(token)}
suspend fun ProgressRepository.exportProgress(token:WriteToken): String = db.withWriteTransaction {
    val backup=ProgressBackup(exportedAt=kotlin.time.Clock.System.now().toEpochMilliseconds(),catalog=checkNotNull(currentCatalog(token)),records=records(token))
    Json.encodeToString(backup).also {require(it.encodeToByteArray().size<=MAX_BACKUP_BYTES){"Progress is too large for this backup format"}}
}
suspend fun ProgressRepository.recordOpen(token:WriteToken,id:String,revision:String) = db.withWriteTransaction {
    checkToken(token)
    val order=(dao.metadataByKey("openOrder")?.value?.toLongOrNull() ?: 0)+1
    require(order>0)
    dao.metadata(StoreMetadata("openOrder",order.toString()));dao.metadata(StoreMetadata("opened:$id",order.toString()))
    if(dao.lessons(token.profileId).none{it.lessonId==id && it.revision==revision})dao.saveLesson(LessonProgress(token.profileId,id,revision))
    changed()
}
suspend fun ProgressRepository.setValue(token:WriteToken,key:String,value:String)=db.withWriteTransaction {
    checkToken(token);dao.metadata(StoreMetadata(key,value));changed()
}
/** Clear and replacement share a generation barrier and a single rollback-capable transaction. */
suspend fun ProgressRepository.replaceProgress(token:WriteToken,catalog:ContentCatalog,records:StudyRecords=StudyRecords()):WriteToken = db.withWriteTransaction {
    checkToken(token);validateRecords(records)
    dao.clearAttempts();dao.clearQuestions();dao.clearSessions();dao.clearLessons();dao.clearEvents();dao.clearMetadata()
    val next=WriteToken(token.profileId,Uuid.random().toString());dao.generation(next.profileId,next.generation)
    records.lessons.forEach {dao.saveLesson(it.copy(profileId=next.profileId))}
    records.sessions.forEach {dao.insertSession(it.copy(profileId=next.profileId))}
    dao.insertQuestions(records.questions)
    records.attempts.sortedBy{it.sequence}.forEach{dao.insertAttempt(it)}
    records.events.forEach{dao.insertEvent(it.copy(profileId=next.profileId))}
    records.metadata.forEach{dao.metadata(it)}
    dao.metadata(StoreMetadata("catalog:${next.profileId}",Json.encodeToString(catalog)));changed()
    next
}
