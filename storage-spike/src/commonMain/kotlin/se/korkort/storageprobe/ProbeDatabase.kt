package se.korkort.storageprobe

import androidx.room3.ConstructedBy
import androidx.room3.Dao
import androidx.room3.Database
import androidx.room3.Entity
import androidx.room3.PrimaryKey
import androidx.room3.Query
import androidx.room3.RoomDatabase
import androidx.room3.RoomDatabaseConstructor
import androidx.room3.Upsert
import androidx.sqlite.SQLiteDriver
import kotlinx.coroutines.Dispatchers
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

// Deliberately a disposable probe, not the phase-2 learner-progress schema.
@Entity(tableName = "storage_probe")
data class ProbeRow(@PrimaryKey val id: String, val payload: String)

@Dao
interface ProbeDao {
    @Upsert suspend fun save(row: ProbeRow)
    @Query("SELECT * FROM storage_probe WHERE id = :id") suspend fun find(id: String): ProbeRow?
    @Query("SELECT count(*) FROM storage_probe") suspend fun count(): Int
    @Query("DELETE FROM storage_probe") suspend fun clear()
}

@Database(entities = [ProbeRow::class], version = 1, exportSchema = true)
@ConstructedBy(ProbeDatabaseConstructor::class)
abstract class ProbeDatabase : RoomDatabase() {
    abstract fun probes(): ProbeDao
}

@Suppress("KotlinNoActualForExpect")
expect object ProbeDatabaseConstructor : RoomDatabaseConstructor<ProbeDatabase> {
    override fun initialize(): ProbeDatabase
}

fun openProbeDatabase(builder: RoomDatabase.Builder<ProbeDatabase>, driver: SQLiteDriver): ProbeDatabase =
    builder.setDriver(driver).setQueryCoroutineContext(Dispatchers.Default).build()

@Serializable
data class ProbePayload(
    val lessonId: String,
    val revision: String,
    val title: String,
    val blockId: String,
    val confirmedQuestionIds: List<String>,
    val displayedOptionIds: List<String>,
)

val expectedPayload = ProbePayload(
    lessonId = "M03-L03", revision = "storage-spike-v1",
    title = "KörkortGo · Å Ä Ö · å ä ö", blockId = "block-7",
    confirmedQuestionIds = listOf("question-12", "question-4"),
    displayedOptionIds = listOf("option-c", "option-a", "option-d", "option-b"),
)

suspend fun writeProbe(db: ProbeDatabase) {
    db.probes().clear()
    val row = ProbeRow("restart-proof", Json.encodeToString(expectedPayload))
    db.probes().save(row)
    db.probes().save(row) // Repeating an acknowledged write must not duplicate the record.
    verifyProbe(db)
}

suspend fun verifyProbe(db: ProbeDatabase) {
    check(db.probes().count() == 1) { "Expected exactly one durable probe record" }
    val row = checkNotNull(db.probes().find("restart-proof")) { "Missing durable record" }
    check(Json.decodeFromString<ProbePayload>(row.payload) == expectedPayload) {
        "Payload, Unicode, reading target, question identities or option order changed"
    }
}
