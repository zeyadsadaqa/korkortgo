package se.korkort

/** Counts compiled from the exact curriculum/question payloads bound by the accepted manifest. */
data class CurriculumSummary(
    val releaseLabel: String,
    val modules: Int,
    val lessons: Int,
    val questions: Int,
    val signEntries: Int,
)
