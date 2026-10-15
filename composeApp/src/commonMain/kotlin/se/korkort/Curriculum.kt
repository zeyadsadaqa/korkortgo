package se.korkort

/** Published IDs share one namespace; the generator validates the registered destination kind. */
@JvmInline value class ContentId(val value: String) {
    init { require(value.isNotBlank()) }
}
@JvmInline value class BlockId(val value: String) {
    init { require(value.isNotBlank()) }
}
@JvmInline value class AssetId(val value: String) {
    init { require(value.isNotBlank()) }
}
/** Exact URL evidence identity (for example REF-*), distinct from a source-* destination. */
@JvmInline value class SourceReferenceId(val value: String) {
    init { require(value.isNotBlank()) }
}
@JvmInline value class Sha256(val value: String) {
    init { require(value.matches(Regex("[0-9a-f]{64}"))) }
}
@JvmInline value class SemanticRevision(val value: String) {
    init { require(value.isNotBlank()) }
}

data class FileIdentity(val path: String, val sha256: Sha256)

/** Technical evidence only. PDF folios never identify a learner route or block. */
data class OriginLocator(
    val file: FileIdentity,
    val locator: String,
    val evidenceIds: List<String> = emptyList(),
    val pdfEvidencePage: Int? = null,
)

data class ReviewEvidence(val record: OriginLocator, val reviewedOn: String?)
data class CurriculumRelease(val contentVersion: String, val pdf: FileIdentity)

/** App content version is independent of app version and the original PDF release. */
data class ContentPackageIdentity(val contentVersion: String, val manifestSha256: Sha256)

enum class PayloadKind { CURRICULUM, QUESTIONS, SOURCES, LEGACY_ALIASES, ASSET }
data class PayloadFile(val kind: PayloadKind, val file: FileIdentity)
data class CanonicalRevision(val id: ContentId, val revision: SemanticRevision)
data class SourceScopeBinding(
    val sourceId: ContentId,
    val scopeId: ContentId?,
    val referenceId: SourceReferenceId,
)
data class AssetIdentityBinding(val id: AssetId, val file: FileIdentity)

data class ContentManifest(
    val schemaVersion: Int,
    val identity: ContentPackageIdentity,
    val sourceCurriculum: CurriculumRelease,
    val inputs: List<FileIdentity>,
    val payloads: List<PayloadFile>,
    val canonicalRevisions: List<CanonicalRevision>,
    val questionRevisions: List<QuestionReleaseBinding>,
    val sourceBindings: List<SourceScopeBinding>,
    val assetBindings: List<AssetIdentityBinding>,
) {
    init { require(schemaVersion > 0) }
}

data class ContentTarget(val contentId: ContentId, val blockId: BlockId? = null)

/** External links refer to registered URL evidence, never an old book-page URL table. */
sealed interface TeachingLink {
    data class Internal(val target: ContentTarget) : TeachingLink
    data class ExternalSource(val referenceId: SourceReferenceId) : TeachingLink
}

sealed interface InlineContent {
    data class Text(val text: String) : InlineContent
    data class Emphasis(val children: List<InlineContent>) : InlineContent
    data class Strong(val children: List<InlineContent>) : InlineContent
    data class Link(val label: List<InlineContent>, val target: TeachingLink) : InlineContent
    data class Math(val expression: String, val spokenText: String) : InlineContent
}
typealias RichText = List<InlineContent>

enum class TeachingRole {
    EXPLANATION, REQUIREMENT, RECOMMENDATION, EXERCISE_ASSUMPTION,
    WORKED_EXAMPLE, SUMMARY, SOURCE_LIMIT, DISCLAIMER, CREDIT,
}

data class SourceUse(
    val referenceId: SourceReferenceId,
    val sourceId: ContentId?,
    val scopeId: ContentId?,
    val locator: String,
    val editorialInference: Boolean,
)

/** Every block has a stable authored ID and an exact production-source origin. */
data class BlockMetadata(
    val id: BlockId,
    val origin: OriginLocator,
    val sourceUses: List<SourceUse> = emptyList(),
    val relatedContent: List<ContentTarget> = emptyList(),
)

data class ContentBlock(val metadata: BlockMetadata, val payload: BlockPayload)
data class TableColumn(val heading: RichText)
data class TableRow(val cells: List<RichText>)

/** Typed payloads retain structure needed for reading, reflow and accessibility. */
sealed interface BlockPayload {
    data class Heading(val level: Int, val text: RichText) : BlockPayload {
        init { require(level in 1..6) }
    }
    data class Paragraph(val text: RichText, val role: TeachingRole) : BlockPayload
    data class ListItems(
        val ordered: Boolean,
        val start: Int = 1,
        val items: List<List<ContentBlock>>,
    ) : BlockPayload
    data class Table(
        val caption: RichText?,
        val columns: List<TableColumn>,
        val rows: List<TableRow>,
    ) : BlockPayload {
        init {
            require(columns.isNotEmpty())
            require(rows.all { it.cells.size == columns.size })
        }
    }
    data class Equation(
        val expression: String,
        val spokenText: String,
        val assumptions: RichText,
    ) : BlockPayload
    data class Callout(
        val role: TeachingRole,
        val title: RichText?,
        val blocks: List<ContentBlock>,
    ) : BlockPayload
    data class Scenario(val title: RichText?, val blocks: List<ContentBlock>) : BlockPayload
    data class KnowledgeCheck(
        val prompts: List<ContentBlock>,
        val answerId: BlockId,
    ) : BlockPayload
    data class Image(val assetId: AssetId, val caption: RichText) : BlockPayload
    data class RelatedLinks(val links: List<InlineContent.Link>) : BlockPayload
}

enum class AnswerVisibility { AFTER_DELIBERATE_REVEAL }

/** Kept outside bodyBlocks; renderers must not place unrevealed answers in semantics. */
data class AnswerBlock(
    val metadata: BlockMetadata,
    val visibility: AnswerVisibility,
    val blocks: List<ContentBlock>,
)

enum class DocumentKind { MODULE_INTRODUCTION, LESSON, MODULE_REVIEW, APPENDIX, FRONT_MATTER }

data class CurriculumDocument(
    val id: ContentId,
    val kind: DocumentKind,
    val moduleId: ContentId?,
    val title: String,
    val order: Int,
    val objectives: List<RichText>,
    val bodyBlocks: List<ContentBlock>,
    val answerBlocks: List<AnswerBlock>,
    val sourceIds: List<ContentId>,
    val assetBindings: List<AssetId>,
    val relatedContent: List<ContentTarget>,
    val contentVersion: String,
    val revision: SemanticRevision,
    val origin: OriginLocator,
)

data class CurriculumModule(
    val id: ContentId,
    val title: String,
    val order: Int,
    val lessonIds: List<ContentId>,
    val reviewId: ContentId,
) {
    init { require(lessonIds.size == 4 && lessonIds.distinct().size == 4) }
}

data class ReferenceGroup(
    val id: ContentId,
    val title: String,
    val order: Int,
    val bodyBlocks: List<ContentBlock>,
    val entryIds: List<ContentId>,
    val origin: OriginLocator,
    val revision: SemanticRevision,
)

data class PublishedAnchor(
    val id: ContentId,
    val target: ContentTarget,
    val origin: OriginLocator,
)

enum class SourceClassification {
    SWEDISH_LEGISLATION, SWEDISH_AUTHORITY_GUIDANCE, RESEARCH,
    FOREIGN_PUBLIC_AUTHORITY, SWEDISH_PUBLIC_SERVICE, MANUFACTURER,
    COMMERCIAL_TEACHING, EDITORIAL_APPLICATION,
}

/** Dates stay distinct; null means no retained evidence, not the import/approval date. */
data class SourceDates(
    val checkedOn: String? = null,
    val retrievedOn: String? = null,
    val publishedOn: String? = null,
)

data class SourceEvidence(
    val origin: OriginLocator,
    val dates: SourceDates,
    val scope: String,
    val finding: String,
    val limitations: List<String>,
)

data class SourceReference(
    val id: SourceReferenceId,
    val title: String,
    val publisher: String,
    val url: String,
    val classifications: Set<SourceClassification>,
    val classificationNote: String,
    val editorialInference: Boolean,
    val originalEvidenceIds: List<String>,
    val evidence: List<SourceEvidence>,
)

data class ScopedSourceUrl(val scopeId: ContentId?, val referenceId: SourceReferenceId)
data class SourceDestination(
    val id: ContentId,
    val originalAlias: String,
    val title: String,
    val scopedUrls: List<ScopedSourceUrl>,
    val origin: OriginLocator,
)

enum class AssetKind { OFFICIAL_SIGN, CONTEXTUAL_ILLUSTRATION }
enum class TranslationStatus { EDITORIAL_ENGLISH, OFFICIAL_TRANSLATION, NOT_APPLICABLE }
data class ReuseRecord(val evidence: OriginLocator, val conditions: String, val credit: String)
data class PhysicalSizeMm(val width: String, val height: String)
data class AssetRenderingConstraints(
    val preserveGeometryAndColours: Boolean,
    val containWithoutCrop: Boolean,
    val maximumPrintSizeMm: PhysicalSizeMm?,
    val notes: List<String>,
)

data class CurriculumAsset(
    val id: AssetId,
    val kind: AssetKind,
    val codeOrIllustrationId: String,
    val variant: String,
    val original: FileIdentity,
    val bundled: FileIdentity,
    val captionId: String,
    val studyAltText: String,
    val translationStatus: TranslationStatus,
    val reuse: List<ReuseRecord>,
    val rendering: AssetRenderingConstraints,
    val approval: List<ReviewEvidence>,
)

data class SignEntry(
    val id: ContentId,
    val code: String,
    val officialNameSv: String,
    val englishLabel: String,
    val captionId: String,
    val caption: RichText,
    val assetId: AssetId,
    val translationStatus: TranslationStatus,
    val sourceUses: List<SourceUse>,
    val limitations: List<String>,
    val origin: OriginLocator,
)

/** Lookup request variants retain identity and namespace; no resolver is introduced here. */
sealed interface LegacyLookup {
    data class Question(val questionId: QuestionId) : LegacyLookup
    data class Page(val namespace: String, val page: Int) : LegacyLookup
    data class Chapter(val namespace: String, val title: String) : LegacyLookup
    data class Topic(val namespace: String, val rowId: String) : LegacyLookup
    data class Sign(val namespace: String, val code: String) : LegacyLookup
}
sealed interface AliasOutcome {
    data class Content(val target: ContentTarget) : AliasOutcome
    data class Chooser(val targets: List<ContentTarget>) : AliasOutcome
    data class Unavailable(
        val message: String,
        val officialReferenceId: SourceReferenceId?,
        val related: List<ContentTarget>,
    ) : AliasOutcome
}
data class LegacyAlias(val lookup: LegacyLookup, val outcome: AliasOutcome, val origin: OriginLocator)
data class ContentTombstone(
    val retiredId: ContentId,
    val replacementIds: List<ContentId>,
    val reason: String,
    val review: ReviewEvidence,
)

/** Authoring-file roots; these are converted to common Kotlin at build time. */
data class CurriculumPayload(
    val schemaVersion: Int,
    val sourceCurriculum: CurriculumRelease,
    val modules: List<CurriculumModule>,
    val documents: List<CurriculumDocument>,
    val referenceGroups: List<ReferenceGroup>,
    val anchors: List<PublishedAnchor>,
    val signEntries: List<SignEntry>,
    val assets: List<CurriculumAsset>,
    val readingOrder: List<ContentId>,
    val lessonCategoryTags: Map<ContentId, Set<Category>>,
)
data class SourcePayload(
    val schemaVersion: Int,
    val destinations: List<SourceDestination>,
    val references: List<SourceReference>,
)
data class LegacyAliasPayload(
    val schemaVersion: Int,
    val aliases: List<LegacyAlias>,
    val tombstones: List<ContentTombstone>,
)

/** Compile-time assembled view; no runtime loader or populated payload is introduced in 9A2. */
data class CurriculumPackage(
    val manifest: ContentManifest,
    val curriculum: CurriculumPayload,
    val questions: QuestionPayload,
    val sources: SourcePayload,
    val legacyAliases: LegacyAliasPayload,
)
