package se.korkort.progress

import androidx.room3.*
import androidx.sqlite.SQLiteDriver
import androidx.sqlite.SQLiteConnection
import androidx.sqlite.async.executeSQL
import androidx.room3.migration.Migration
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow

@Entity(tableName = "learner_profile")
data class Profile(@PrimaryKey val id: String, val generation: String)
@Entity(tableName = "lesson_progress", primaryKeys = ["profileId", "lessonId", "revision"])
data class LessonProgress(val profileId: String, val lessonId: String, val revision: String,
    val read: Boolean = false, val blockId: String? = null, val offset: Int = 0)
@Entity(tableName = "exercise_session", indices = [Index("profileId")])
data class Session(@PrimaryKey val id: String, val profileId: String, val packageId: String,
    val deferred: Boolean, val snapshot: String, val status: String = "active", val version: Long = 0, @ColumnInfo(defaultValue="0") val createdAt: Long = 0)
@Entity(tableName = "session_question", primaryKeys = ["sessionId", "position"],
    indices = [Index(value = ["sessionId", "questionId"], unique = true)])
data class StoredQuestion(val sessionId: String, val position: Int, val questionId: String,
    val revision: String, val conceptId: String, val optionsJson: String, val correctOption: String)
@Entity(tableName = "answer_attempt", indices = [Index(value = ["sessionId", "position"], unique = true), Index(value = ["eventId"], unique = true)])
data class Attempt(@PrimaryKey(autoGenerate = true) val sequence: Long = 0, val eventId: String,
    val sessionId: String, val position: Int, val selectedOption: String, val published: Boolean, @ColumnInfo(defaultValue="0") val confirmedAt: Long = 0)
@Entity(tableName = "study_event", indices = [Index(value = ["profileId", "target"])])
data class StudyEvent(@PrimaryKey val id: String, val profileId: String, val target: String, val kind: String, @ColumnInfo(defaultValue="0") val occurredAt: Long = 0)
@Entity(tableName = "store_metadata")
data class StoreMetadata(@PrimaryKey val key: String, val value: String)

@Dao
interface ProgressDao {
    @Query("SELECT * FROM learner_profile ORDER BY id LIMIT 1") suspend fun localProfile(): Profile?
    @Insert suspend fun insertProfile(profile: Profile)
    @Query("SELECT * FROM learner_profile WHERE id=:id") suspend fun profile(id: String): Profile?
    @Query("DELETE FROM lesson_progress WHERE profileId=:profile AND lessonId=:id") suspend fun clearLesson(profile: String,id: String)
    @Upsert suspend fun saveLesson(lesson: LessonProgress)
    @Query("SELECT * FROM lesson_progress WHERE profileId=:profile") suspend fun lessons(profile: String): List<LessonProgress>
    @Insert suspend fun insertSession(session: Session)
    @Query("SELECT * FROM exercise_session WHERE id=:id") suspend fun session(id: String): Session?
    @Query("SELECT * FROM exercise_session WHERE profileId=:profile AND status='active'") suspend fun active(profile: String): List<Session>
    @Query("SELECT * FROM exercise_session WHERE profileId=:profile ORDER BY createdAt DESC, id DESC LIMIT :limit OFFSET :offset") suspend fun history(profile: String, limit: Int, offset: Int): List<Session>
    @Query("UPDATE exercise_session SET status=:status, version=version+1 WHERE id=:id AND version=:version") suspend fun transition(id: String, version: Long, status: String): Int
    @Insert suspend fun insertQuestions(questions: List<StoredQuestion>)
    @Query("SELECT * FROM session_question WHERE sessionId=:id ORDER BY position") suspend fun questions(id: String): List<StoredQuestion>
    @Insert suspend fun insertAttempt(attempt: Attempt)
    @Query("SELECT * FROM answer_attempt WHERE sessionId=:id ORDER BY sequence") suspend fun answers(id: String): List<Attempt>
    @Query("SELECT a.* FROM answer_attempt a JOIN exercise_session s ON s.id=a.sessionId WHERE s.profileId=:profile ORDER BY a.sequence") suspend fun attempts(profile: String): List<Attempt>
    @Query("UPDATE answer_attempt SET published=1 WHERE sessionId=:id") suspend fun publish(id: String)
    @Insert suspend fun insertEvent(event: StudyEvent)
    @Query("SELECT * FROM store_metadata") fun observeMetadata(): Flow<List<StoreMetadata>>
    @Query("SELECT * FROM store_metadata WHERE `key`=:key") suspend fun metadataByKey(key: String): StoreMetadata?
    @Upsert suspend fun metadata(value: StoreMetadata)
}
@Database(entities = [Profile::class, LessonProgress::class, Session::class, StoredQuestion::class,
    Attempt::class, StudyEvent::class, StoreMetadata::class], version = 2, exportSchema = true)
@ConstructedBy(ProgressDatabaseConstructor::class)
abstract class ProgressDatabase : RoomDatabase() { abstract fun progress(): ProgressDao }
@Suppress("KotlinNoActualForExpect")
expect object ProgressDatabaseConstructor : RoomDatabaseConstructor<ProgressDatabase> { override fun initialize(): ProgressDatabase }
fun openProgressDatabase(path: String, driver: SQLiteDriver): ProgressDatabase =
    Room.databaseBuilder<ProgressDatabase>(path).setDriver(driver).addMigrations(PROGRESS_MIGRATION_1_2).setQueryCoroutineContext(Dispatchers.Default).build()

val PROGRESS_MIGRATION_1_2 = object : Migration(1, 2) {
    override suspend fun migrate(connection: SQLiteConnection) {
        connection.executeSQL("ALTER TABLE exercise_session ADD COLUMN createdAt INTEGER NOT NULL DEFAULT 0")
        connection.executeSQL("ALTER TABLE answer_attempt ADD COLUMN confirmedAt INTEGER NOT NULL DEFAULT 0")
        connection.executeSQL("ALTER TABLE study_event ADD COLUMN occurredAt INTEGER NOT NULL DEFAULT 0")
        connection.executeSQL("CREATE INDEX IF NOT EXISTS index_study_event_profileId_target ON study_event(profileId,target)")
    }
}
