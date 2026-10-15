# 9A2 — Typed curriculum and assessment contract

**Schema version:** 1. **Status:** Implemented as model declarations; populated imports and deterministic generation start in 9A3/9B. **Inputs:** The verified [9A1 baseline](../9A1/input-baseline.json), [7B registry](../../curriculum-map.json), [7C relationships](../../question-map.json), [7D proposals](../../question-actions.json), [7E state/link contracts](../../link-and-progress-map.json) and [approved design](../../../app-design-review.md).

The common Kotlin types are in [Curriculum.kt](../../../../../composeApp/src/commonMain/kotlin/se/korkort/Curriculum.kt) and the appended contract section in [Quiz.kt](../../../../../composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt). They use the standard library and compile-time data. There is no runtime JSON loading, serializer dependency, new persistence or UI in this step. Existing `Question`, `Option`, `QuizSession`, `QuizEngine`, `Category`, `Feedback` and bank constructors keep their current behaviour; future 9D/9M tasks integrate the new types.

## JSON-to-Kotlin rules

This document defines the future authoring/manifest schema. Kotlin declarations are the field inventory; JSON uses their snake_case equivalents. A sealed payload has a `type` discriminator equal to its snake_case variant name (for example `list_items`, `knowledge_check`, `external_source`). Its remaining properties are the corresponding Kotlin fields. Enums serialize as lower snake_case. Value-class IDs, revisions and SHA-256 values serialize as strings; `RichText` serializes as an ordered array of inline variants. `Set` values serialize as sorted, duplicate-free arrays. Optional scalar fields use explicit `null` when evidence is unknown. Collections use arrays, including empty arrays; no absent required fields or arbitrary untyped payload maps are accepted.

Object keys are sorted for canonical hashing; teaching/block/module/list/row/option order is semantic and is preserved. For a map with typed keys, such as `lesson_category_tags`, JSON object keys are the ID values. Dates retain evidence ISO `YYYY-MM-DD` strings, independently for checked/retrieved/published dates. Decimal metadata such as print dimensions is stored as decimal strings to avoid platform float-format differences. Exact authored equations and units remain selectable text, with separate spoken representations. Typed models are read-only views; generated collections must not be backed by mutable collections subsequently modified by the app.

There is no generated content in 9A2. 9A3 must implement and test these rules before real import. Constructor checks cover local identity/shape invariants; they do not claim cross-package validation, legal verification or actual accessible rendering.

## Identities, versions and provenance

| Type | Meaning and constraints |
|---|---|
| `ContentId` | One case-sensitive namespace for all 1,123 published destinations: modules, lessons, reviews, appendices, reference groups, signs, sources and supporting anchors. Expected kind is validated at each reference. Titles and folios do not generate IDs. |
| `BlockId` | Stable, parent-scoped authoring identity. Assign once and record origin; never derive from text/title/page or recycle a retired identity. Existing supporting IDs remain published aliases/anchors. |
| `AssetId` | Exact verified asset/variant identity, distinct from sign code and placement/anchor identity. |
| `SourceReferenceId` | Exact registered URL record identity, including 7C REF-* records. This is distinct from a canonical source-* destination and original TS-/SFS-/G-/MS evidence IDs. |
| `QuestionId`, `OptionId` | Stable authored identity; question/concept IDs are retained. Option IDs are interpreted with the question semantic revision, independent of shuffled letter, text or source code. Use 7D authored IDs where provided. New assignments for remaining questions must be recorded by 9A3/9D, never guessed from current shuffle position. |
| `SemanticRevision` | Nonblank immutable content revision. A wording/key/asset/option change requires a reviewed revision; route/source metadata alone does not reinterpret a prior result. |
| `Sha256`, `FileIdentity` | Lowercase 64-hex digest and repository/resource-relative exact file path. Paths do not permit traversal or absolute filesystem paths in deliverable payloads. Bundled paths are Compose file-resource paths, not runtime network resources. |
| `OriginLocator` | Exact file identity plus heading/line-range/JSON-pointer locator and original evidence IDs; optional physical PDF folio is technical evidence only. Every imported block, answer and destination keeps its origin. |
| `ReviewEvidence` | Exact review-record locator and retained review date, or null when no retained date exists. A type declaration is not an approval. |
| `CurriculumRelease` | Original approved screen `content_version` and PDF file identity: `screen-2026-10-14-78a89d8ffbb8`. |
| `ContentPackageIdentity` | Separate app-content `content_version` plus complete manifest digest. It changes for accepted app-content changes even if the PDF remains unchanged. It is independent of Android/iOS/app version numbers. |

## Content and manifest files

The planned authoring inputs are `content/curriculum.json`, `content/questions.json`, `content/sources.json` and `content/legacy-aliases.json`. `content/content-manifest.json` binds them and exact bundled assets. The existing questions JSON stays in its legacy form until its separately planned generation/migration; this document does not declare it schema-1 compliant.

The exact file roots are:

| File | Kotlin root | Required root fields |
|---|---|---|
| `content/curriculum.json` | `CurriculumPayload` | `schema_version`, `source_curriculum`, `modules`, `documents`, `reference_groups`, `anchors`, `sign_entries`, `assets`, `reading_order`, `lesson_category_tags` |
| `content/questions.json` | `QuestionPayload` | `schema_version`, `questions` (`AssessmentQuestion[]`) |
| `content/sources.json` | `SourcePayload` | `schema_version`, `destinations` (`SourceDestination[]`), `references` (`SourceReference[]`) |
| `content/legacy-aliases.json` | `LegacyAliasPayload` | `schema_version`, `aliases` (`LegacyAlias[]`), `tombstones` (`ContentTombstone[]`) |
| `content/content-manifest.json` | `ContentManifest` | All manifest fields in the table below |

All schema versions must agree. The schema-1 question root is an explicit future migration from the existing JSON array, not an in-place reinterpretation by a runtime loader. `CurriculumPackage` is the assembled compile-time view with `manifest`, `curriculum`, `questions`, `sources` and `legacy_aliases`; it is not an additional authoring file.

| Manifest field | Type / binding |
|---|---|
| `schema_version` | Positive integer, currently 1. Unknown versions fail generation. |
| `identity` | `ContentPackageIdentity`; the manifest's own digest has the exclusion rule below. |
| `source_curriculum` | `CurriculumRelease`; retained approved version/PDF hash, never implicit “latest”. |
| `inputs` | `FileIdentity[]` for exact source/manuscript/production corrections/registry/approval evidence and generator/schema inputs. Historical planning records remain provenance, not runtime teaching payloads. |
| `payloads` | `PayloadFile[]`: kind `curriculum`, `questions`, `sources`, `legacy_aliases` or `asset`, and exact bytes/hash/path. Every runtime content file is bound. |
| `canonical_revisions` | `CanonicalRevision[]` for published IDs and semantic revisions, including required supporting anchors. Unique namespace and expected destination kinds are checked. |
| `question_revisions` | `QuestionReleaseBinding[]`: question ID + semantic revision + scoring eligibility. The whole baseline is accounted for, including held records; no silent deletion. |
| `source_bindings` | `SourceScopeBinding[]`: canonical source ID, optional module/content scope and exact URL record ID. Scope-specific URL choices are retained. |
| `asset_bindings` | `AssetIdentityBinding[]`: exact asset ID and packaged file identity; must agree with asset records and byte parity. |

The package manifest hash is SHA-256 of UTF-8 canonical JSON (`ensure_ascii=False`, sorted keys, compact separators, no trailing newline) after removing **only** `identity.manifest_sha256`. All remaining version, input, payload, question/revision/eligibility, canonical, scoped-source and asset bindings are included. No manifest self-file digest or generated Kotlin output digest is placed in the hashed payload: those create cycles. Alias/tombstone changes are bound through the `legacy_aliases` payload hash. Generated-output hashes belong in build/evidence reports outside this identity calculation. 9A3 supplies a golden hash fixture and byte-identical generation checks; 9A2 does not calculate or invent a live app-content release identity.

## Teaching structure and complete blocks

`CurriculumModule` preserves ID, exact title/order, four distinct lesson IDs and review ID. Its ID also selects the `module_introduction` document. `CurriculumDocument` covers `module_introduction`, `lesson`, `module_review`, `appendix` and approved `front_matter`; fields are ID, kind, optional module ID, title/order, objectives, `body_blocks`, `answer_blocks`, canonical `source_ids`, asset IDs, related targets, source curriculum `content_version`, semantic revision and origin. Reviews retain their own tasks rather than fabricated objectives. All references use exact registered kinds.

`ReferenceGroup` retains RB01–RB24 IDs/titles/order, complete group prose, ordered entry IDs, origin and revision. Repeated sign placements use distinct block/anchor IDs and the same exact asset as appropriate. `PublishedAnchor` maps a retained supporting ID to an exact content/block target and origin. Supporting/front-matter anchors are not automatically library cards. `reading_order` remains the exact 60 module/lesson/review nodes; four appendices and reference groups remain separately discoverable. `lesson_category_tags` maps all forty lessons to the existing five `Category` values without renumbering modules.

`ContentBlock` pairs `BlockMetadata` (ID, origin, exact scoped source uses, related targets) with one typed `BlockPayload`:

| Payload | Retained structure |
|---|---|
| `heading` | Level 1–6 and rich inline text. |
| `paragraph` | Rich text plus teaching role: explanation, requirement, recommendation, exercise assumption, worked example, summary, source limit, disclaimer or credit. |
| `list_items` | Ordered/unordered flag, explicit start, ordered items containing complete nested blocks. |
| `table` | Optional caption, ordered heading cells and row cells with rich text. Every row has the declared number of columns. Empty practice-record cells remain valid. |
| `equation` | Exact selectable expression, spoken text and explicit authored assumptions. |
| `callout` | Role, optional title and ordered complete child blocks. |
| `scenario` | Optional title and complete nested scenario blocks. |
| `knowledge_check` | Ordered prompt blocks and the ID of a separate answer block. Supports one or multiple exercise/review questions without fabricating MCQ scoring. |
| `image` | Exact asset binding and contextual caption; study accessibility text comes from the verified asset record. |
| `related_links` | Ordered labelled links to registered internal destinations or exact registered external source records. |

`RichText` uses `text`, nested `emphasis` / `strong`, labelled `link` and inline `math` variants. A link targets `TeachingLink.Internal(ContentTarget)` or `ExternalSource(SourceReferenceId)`; importing raw URLs into route labels is not permitted. Text/source quotations/units are preserved exactly; no new substantive interpretation is added by the model.

The 7B `scenarios` and `knowledge_checks` fields are represented by the corresponding payload variants **in authored body order**, including nested blocks. They are discoverable by structural traversal, not duplicated out-of-order collections. This refines the planning field list without losing those entities. Answers use a separate ordered `answer_blocks` collection, each with metadata/origin, `after_deliberate_reveal` visibility and complete answer child blocks. Check `answer_id` is document-local and must resolve exactly once. Review guides use the same separation where the approved production source supplies an answer/review guide. A renderer must not traverse unrevealed answer content into visual/accessibility output; hiding pixels alone does not satisfy reveal semantics.

## Sources, sign entries and artwork

`SourceDestination` contains the canonical source ID, original alias, actual title, origin and scope-to-URL-record bindings. Global and module-specific scopes must be explicit; missing or ambiguous scope is a validation failure, not permission to select the first URL. `SourceReference` contains exact URL-record ID, actual title/publisher/URL, a set of classifications, retained classification note, editorial-inference flag, original evidence IDs and all scoped `SourceEvidence` records.

Classification supports Swedish legislation, Swedish authority guidance, research, foreign public authority, Swedish public service, manufacturer, commercial teaching and editorial application. These are sourced from evidence, never inferred from a domain or from presence in the bibliography. Hosted research may keep multiple classifications plus its precise note. `SourceEvidence` retains exact evidence origin, distinct checked/retrieved/published dates, scope, finding and limitations. Model/manufacturer limits, commercial arithmetic assumptions and limited 1177 first-aid scope survive import. Unknown dates stay null; approval/import dates do not become source-check dates.

`SourceUse` joins an exact URL record to an optional canonical source ID and scope, a retained claim/passage locator and an editorial-inference flag. Original caption evidence IDs remain in source evidence/origin records; they are not presumed interchangeable with REF-* or source-* identities. 9C must map exact URLs and scopes using the retained evidence.

`CurriculumAsset` carries ID, kind (`official_sign` / `contextual_illustration`), exact case-sensitive code or illustration ID, variant, original and bundled file identities, caption ID, study alt text, translation status, reuse/credit records, rendering constraints and approval evidence. Bundling must preserve bytes. `PhysicalSizeMm` stores explicit width/height decimal strings for retained print-size ceilings; absent limits remain null. These are not evidence of actual app legibility. Rendering constraints retain geometry/colour preservation, contain/no-crop requirements and all notes. No universal minimum dp or proven device size is invented.

`SignEntry` joins canonical sign ID, code, official Swedish name, English label/caption and editorial translation status to the exact asset, scoped sources, retained limitations and origin. SIG16–18 gain no sign entries in this step or by aliasing. Study alt text can describe meaning and is kept separate from assessment descriptions. Motion/audio/static-image limitations remain attached to sign entries.

## Assessment and eligibility

`AssessmentQuestion` contains a `QuestionRevisionKey`, unchanged concept/category, rich prompt, optional assessment image, four authored `AssessmentOption`s, separate `AssessmentFeedback`, canonical `QuestionRelationship`, acceptance and origin. It has no runtime old-page route or page-derived source field. An old folio may appear only in technical provenance.

`QuestionRelationship` retains primary/related lesson IDs, canonical reference/source IDs, exact scoped `SourceUse`s, 7D disposition and source curriculum `content_version`. `QuestionDisposition` supports retain/rewrite/replace/remove for future compatibility; zero baseline removals are authorised.

`AssessmentOption` holds ID, pre-answer rich text and optional `AssessmentImageBinding`. Equal visible labels are allowed; identity and asset distinctness govern the options. Display letters are derived from current shuffled position by 9D1, not authored into identity. `AssessmentFeedback` holds target sign code/English label if relevant, correct option ID, full question explanation and four option-feedback records. Each option-feedback record binds its own authored option ID to the explanation, optional post-answer code/label and exact sources. Feedback/code-bearing metadata remains outside pre-answer component semantics, and both IMMEDIATE and AT_END reveal rules remain binding.

`AssessmentImageBinding` contains only asset ID and a nullable `NeutralImageDescription` (reviewed physical features plus exact review evidence). Null explicitly represents unreviewed description work. No automatic study-alt-text fallback exists. A non-null reviewed field does not itself prove neutrality; 9D must inspect the actual image and authoring text. Every occurrence, including distractor images, must be reviewed.

`AssessmentAcceptance` records eligibility (`unreviewed`, `held`, `accepted`, `retired`), nullable content-review evidence, description-review records, delivery-proof records and explicit open holds with release conditions. Constructors forbid accepted items with no content review, open holds, removed disposition or image occurrences lacking reviewed descriptions. `AssessmentQuestion` also rejects duplicate/missing option identities, unknown correct IDs and missing/duplicate option feedback. Cross-record generator checks must additionally require all conditional faint-image/platform proofs, evidence-to-asset/hash association, complete per-ID acceptance and no active held items. An empty proof list never clears a hold that requires delivery proof.

The 336 retained questions require relationship/package integration without changed assessment fields; 626 rewrites require acceptance and 38 replacements additionally require exact-image delivery proof. All 1,000 IDs / 500 concepts remain accounted for. Active counts derive from the accepted manifest; insufficient capacity is a blocker, and unchanged five categories/quotas/concept uniqueness are verified later in 9J.

## Navigation, aliases and transient snapshots

`ContentTarget` carries canonical content ID and optional stable block ID. `LegacyLookup` separates question identity, namespace-qualified page, chapter title, topic row and exact sign code. `LegacyAlias` stores lookup, reviewed `AliasOutcome` (content, deliberate chooser or unavailable) and origin. The unavailable variant retains exact message, optional registered official URL action and related targets. The frozen namespace is `legacy-app-4768933c3d9a`; question lookup must take precedence over legacy page lookup. Unknown identity/namespace never permits a guessed route. `ContentTombstone` retains retired ID, reviewed replacements, reason and evidence; the initial production list remains empty. Resolvers, all eight navigation states, transition guards and return-context implementation are explicitly 9K work, not a new public route API in 9A2.

`SessionQuestionSnapshot` pins the full `AssessmentQuestion`, app-content identity and exact displayed option-ID order. Its order must be a complete permutation of the authored options. `SnapshotAnswer` binds selected authored option ID to question ID **and semantic revision**. Session code must validate that selection against its own pinned snapshot. Current package order/key cannot regrade an old snapshot. No conversion of unversioned shuffled indices is introduced.

The existing transient `QuizSession` remains operational with its original five fields until 9M. That step will integrate these snapshot types, pin feedback/score/index/filter/return state, require matching session/revision for pending selection and review expansion, and preserve setup/reset/missing-result rules. No durable history, bookmarks, completion, hot replacement or store migration is introduced by defining these types. Conditional future history compatibility remains conditional.

## Mapping the 7B planning field list

The following refinements are explicit; source identities/meaning are retained rather than silently dropping a planning field.

| 7B field | Typed representation |
|---|---|
| Lesson/review `scenarios`, `knowledge_checks` | In-order `BlockPayload.Scenario` / `KnowledgeCheck` nodes, recursively traversable within `body_blocks`; answers remain separate. |
| Block `type`, `text_or_payload` | Sealed `BlockPayload` discriminator and exact typed fields; rich inline text retains emphasis, mathematics and links. |
| Block `source_ids`, `asset_binding_ids` | `metadata.source_uses` provides canonical source IDs plus exact scope/URL evidence; image payloads carry exact asset IDs. Document-level source/asset arrays retain the aggregate bindings. |
| Block `answer_visibility` | Body blocks are visible; answer content is reachable only through `AnswerBlock.visibility = after_deliberate_reveal`. Answer blocks and their children are not mixed into `body_blocks`. |
| Relationship `question_id` | Parent `AssessmentQuestion.key.question_id`; relationship data is owned by this exact question revision. |
| Source `checked_on`, `evidence_scope` | Per-evidence `dates.checked_on` and `scope`, preserving multiple dates/scopes for one URL rather than flattening to one blanket date. |
| Asset `code_or_illustration_id`, `original_path`, `sha256`, `alt_text`, `reuse_record`, `rendering_constraints`, `approval_binding` | `code_or_illustration_id`, `original` + `bundled` file identities, `study_alt_text`, `reuse`, `rendering`, `approval`; all are explicit typed fields. Assessment descriptions are separately reviewed data. |

## Validation boundary and handoff

9A3 must fail generation for unsupported schema versions, duplicate/unknown IDs, wrong destination kinds, unstable/block collisions, unresolved answers/sources/assets/scopes, invalid origin paths or hashes, invalid dates/dimensions, illegal alias namespace or target choices, repeated authored/visual option choices and acceptance/revision inconsistencies. It must also verify manifest coverage/self-hash rules and emit source-to-output traceability. Full source parity remains 9B17; exact assets/source evidence remain 9C; authored option semantics, shuffling and reveal implementation remain 9D; per-ID release acceptance remains 9E–9J; routing/state/UI/device checks remain 9K–9O and step 10.

No live payload is declared accepted by this contract. Any later visual change follows the existing imagegen/approval workflow.

## Baseline evolution

9A1 remains the immutable pre-implementation identity record. 9A2 intentionally adds the declared contract/test files and appends model declarations to Quiz.kt. The full original Quiz.kt prefix is byte-identical to its 9A1 hash. No old expected hashes are rewritten to accept these changes. This step records the authorised before/after identities and unchanged protected-input checks in verification.json; subsequent tasks use this output together with 9A1, rather than treating an expected implementation edit as unexplained baseline drift. The execution-plan/tracker completion records are administrative changes and are recorded separately from approved teaching/design inputs.
