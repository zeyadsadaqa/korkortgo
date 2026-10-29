# Progress dashboard and persistent learning plan

Created: 27 October 2026. Updated: 29 October 2026. Phase 1's storage proof is implemented, with remaining browser acceptance checks recorded in the [phase-1 report](evidence/storage-phase1/README.md). The user authorized the required Kotlin upgrade to 2.3.20. Dashboard layouts and later phases still await their applicable design approval; this update does not implement the redesigned screens.

Phase 2 implementation: the `progress-data` library now contains the versioned Room schema, transactional repository, persisted snapshots/catalogue, revision-aware metrics and migration/reopen tests. See [module documentation](../../progress-data/README.md). UI and lifecycle integration remain phase 3.

## 1. Intended outcome

Replace the current promotional overview with a useful personal dashboard. The three primary destinations are exactly **Home**, **Learning**, and **Exercise**. A learner can see what they have read, how much of the accepted question bank they have covered, what needs review, and one useful next action. Progress and an unfinished exercise survive an app restart.

Default scope: one local learner profile, no sign-in, offline progress storage on Android and iOS, and persistent browser storage for the web build. A local database is sufficient for this scope. Automatic cross-device synchronization requires a backend and is a separate optional phase.

[Three-screen visual proposal](../../design/progress-dashboard/preview-v2.png) · [Exact image generation prompt](../../design/progress-dashboard/prompt-v2.md)

The preview uses an illustrative learner who has read chapters 1 and 2 and two lessons in chapter 3: 2/10 chapters and 10/40 lessons. They have answered 320/1,000 unique questions; 246 are correct on their latest published attempt and 74 need review. These are consistent sample values, never production defaults.

## 2. Current implementation and implications

Inspected source:

- `composeApp/src/commonMain/kotlin/se/korkort/CurriculumApp.kt`: root navigation, home layout and a `remember`-owned `TransientQuizState`.
- `LearningLibrary.kt` and `LearningRoute.kt`: in-memory library expansion, search, navigation and return state; no durable reading completion.
- `LessonReader.kt` and `Navigation.kt`: reader and canonical content navigation; `ReadingPosition` already identifies a block and offset.
- `TransientQuizState.kt` and `TransientQuizSetup.kt`: same-process exercise state, deliberate confirmation, restart resets, and process-local `practice-N` session IDs.
- `Assessment.kt`: exact question snapshots, option-ID shuffling, accepted-content selection and immediate/deferred feedback safeguards.
- `composeApp/build.gradle.kts`: Android, iOS, JVM and Wasm browser targets, with no database dependency.

The accepted curriculum currently has 10 modules, 40 lessons and 1,000 questions. The public UI will call modules **chapters**, while preserving their canonical IDs and internal model names. The bank also groups question variants into concepts; the 1,000-question dashboard must count question IDs, not concept IDs.

Old reading and exercise activity cannot be reconstructed from the existing transient state after a restart. First launch after this feature ships starts with honest empty progress and explains that tracking starts now. Do not infer completion from which screen is open.

## 3. Screen and navigation design

### Home

Order on a phone:

1. Compact wordmark and “Your progress” heading.
2. Two tappable summary cards: chapters read out of the current total, and unique questions answered out of the current bank total.
3. A prominent “Your next step” card with one action, its reason and destination. For the sample learner: continue chapter 3 at “Find your way without rushing”.
4. Learning overview: last completed chapter and access to all chapter progress.
5. Review insight: number of questions whose latest published answer was incorrect, linked to a targeted exercise.
6. Secondary activity/history and data-management entry, below the primary content if necessary.

Tap chapters to open Learning with progress visible; tap question coverage to open Exercise; tap the last completed chapter to reopen it. Avoid decorative hero space and a single invented “exam readiness” percentage. Reading coverage and practice performance remain separate signals.

### Learning

- Chapter list with “Not started”, “In progress”, or “Read”, plus completed/total lesson counts.
- Expand a chapter to show each lesson's state; automatically reveal the current chapter on first entry, while retaining subsequent user expansion choices.
- Continue a lesson at its saved block. Retain search, topic filters, module reviews, appendices, sources and road-sign references.
- Reader footer: “Mark lesson as read” followed by “Next lesson”. Make the completion action accessible without requiring a particular scroll gesture. Provide “Mark as unread” to correct mistakes.
- A chapter is read when all its teaching lessons are marked read. A module review is a separate learning activity and is not required for the reading indicator.
- Returning to an already completed lesson does not erase completion.

### Exercise

- Coverage summary: unique questions answered, correct on latest published attempt, and questions to revisit.
- Primary start action, or a resume card when an unfinished exercise exists.
- Modes: mixed practice, unanswered questions, review mistakes; chapter/category practice where existing content relationships support it.
- Existing 1–70 question choice and immediate/end-of-exercise feedback remain available, subject to the eligible pool size.
- Recent exercise history with date, mode, score, and completed/abandoned state. Partial work never receives a completed-test score.
- Result and answer review retain explanations and links to related reading and source references.

### Shared navigation behavior

- Phones: fixed bottom navigation with the exact labels Home / Learning / Exercise, icons, selected state and safe-area padding. Each tab retains its own navigation stack and scroll position.
- Larger windows: use a navigation rail and a wider dashboard layout with the same three destinations. Adapt to window width and font scale, not device names.
- Reading and result pages remain within their owning tabs. System Back follows that tab's stack; root behavior follows the platform convention.
- During an active exercise, switching tabs saves and pauses it. Returning to Exercise offers resume. Starting another exercise offers “Resume” or “End this exercise” before replacement. This deliberately replaces the current discard-on-navigation behavior.
- Hide exercise-specific related-reading and correctness routes until the existing reveal rules allow them. Ordinary Learning navigation remains available; this is a study app, not a secure examination system.

### Required design states before implementing each affected flow

The attached board defines the three main destinations. After feedback, produce any requested revision and obtain explicit approval. Supplementary previews are needed for the reader completion control, exercise setup/resume/history, new learner, loading, storage failure, fully completed curriculum, dark mode and large text before implementing those new layouts. The board alone is not approval of unshown layouts.

Use existing brand tokens and bundled Source Serif 4 / Source Sans 3 fonts. Minimum 48dp interactive targets, scalable text, visible focus, icon-plus-text status, and semantic progress values. Avoid clipped titles, reliance on color, or horizontal scrolling for essential actions. Stack summary cards at narrow widths or large text. Illustrative imagegen geometry does not replace runtime accessibility verification.

## 4. Exact progress definitions

| Insight | Definition |
| --- | --- |
| Lesson started | Opened a teaching lesson; saved as in progress, never automatically read. |
| Lesson read | Explicit completion event for that lesson's current progress revision. |
| Chapter read | Every required teaching lesson in that chapter is read. Derived, not separately editable. |
| Questions answered | Distinct eligible question IDs with at least one published confirmed answer for the current question revision. Repeated attempts add no coverage. |
| Correct on latest attempt | Current questions whose most recent published answer is correct. |
| Questions to revisit | Current questions whose most recent published answer is incorrect. A later correct answer removes the question from this queue. |
| Unanswered | Current eligible bank size minus unique answered count. |
| Exercise score | Correct answers / total questions for a completed exercise, retaining its original content revision. |
| Total attempts | All published answer events, including retries; secondary detail only, never the numerator of “out of 1,000”. |

“Answered” is the primary coverage label because “solved” could imply correctness. Do not call one correct attempt mastery. Current-bank totals come from accepted content metadata, not hard-coded UI constants. A separate concept-level metric may be added later, but it must never substitute for question coverage.

**Publication and deferred feedback:** save every confirmed answer immediately. In immediate-feedback mode, publish its progress at confirmation; these answers remain counted even if the rest of the exercise is later ended. In end-of-exercise mode, stage answers and publish progress/results atomically when the exercise completes. Until then, show only “Exercise in progress: X of Y answered”. If it is explicitly ended early, retain partial history without publishing its deferred answers into coverage or correctness metrics. This keeps dashboard counts, review queues and recommendations from revealing deferred results. Explain this rule in the exercise UI.

Selecting an option without confirming it is a draft and never counts. A duplicate confirm, retry after an interrupted save, or repeated import must not create another answer event.

## 5. Suggested-next-step rules

Implement a deterministic, independently tested rule engine. It returns an action type, target ID and plain-language reason; it does not store a recommendation as permanent truth.

Priority:

1. Resume a valid unfinished exercise: “Finish your exercise — 7 of 20 answered.”
2. Continue the most recently opened incomplete lesson at its saved location.
3. After a newly completed chapter, offer an associated practice set if that chapter has eligible question links and no completed chapter-practice exercise for its current revision.
4. Offer a short review set when at least five current questions need review and the learner has not just completed that suggested review. Keep a secondary review link available for smaller queues.
5. Start the first unread lesson in canonical curriculum order.
6. When all lessons are read, prioritize review mistakes, then unanswered questions, then optional mixed practice.

Tie-break by canonical order and stable ID. Remember the completed suggestion's source/revision so the same recommendation does not immediately repeat. Never fabricate an empty exercise: constrain size to available distinct concepts, explain smaller pools, and fall back to a valid action. Do not invent per-chapter question mappings; use accepted relationships, and label a category-based fallback honestly. No account, AI service, time estimate or readiness claim is required.

## 6. Storage and application architecture

Recommended starting point: a shared Kotlin progress domain and repository backed by **Room 3 / SQLite**, with platform database factories. Separate persistence into a small KMP module, tentatively `progress-data`, so generated database code and platform setup do not spread through UI code.

Room 3.0.3 is listed as stable at research time and Room 3 includes WasmJS support. Browser setup uses a worker-backed SQLite driver; verify its persistence and packaging in the first implementation spike. Do not copy the alpha version shown in an example into production without a deliberate decision. [Official Room releases](https://developer.android.com/jetpack/androidx/releases/room3)

The spike was required to test this repository's original Kotlin 2.2.20, Compose 1.9.3 and AGP 8.13.2 and identify necessary toolchain changes. The recorded build found that Room's iOS artifacts require Kotlin 2.3.20. That compiler upgrade is now applied with user authorization, and existing app tests and platform builds pass. See the phase-1 report for pinned dependencies, persistence results and remaining Firefox/branded-Safari acceptance checks.

Platform strategy:

- Android/iOS/JVM: SQLite file in the appropriate private application-data location, migrations enabled, I/O away from the UI thread.
- Web: persistent worker-backed SQLite in browser storage; prove reload/reopen recovery, worker asset loading and deployment requirements on supported browsers. The official driver requires a worker implementation rather than providing a turnkey worker. [Room web setup](https://developer.android.com/jetpack/androidx/releases/room3#3.0.0)
- If the web spike fails the supported-browser or deployment checks, select a single IndexedDB-backed web repository before shipping, retaining the same domain and repository contract. Do not silently switch between independent stores per launch. [IndexedDB overview](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)

Browser storage belongs to a site origin and may be cleared by the user or evicted. Request persistence where appropriate and provide export/import; never promise that browser storage is an account backup. Native uninstall/reinstallation and another device are also outside the basic local-persistence guarantee. [Browser storage durability](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria)

Data flow:

```text
Compose screens -> shared action/state coordinator -> ProgressRepository
                                                    -> transactional database
Database observation -> ProgressSummary + NextStep -> screen state
Accepted curriculum metadata -> identity/revision validation and totals
```

Keep the current pure assessment engine for selection, scoring and reveal behavior. Add an application coordinator that validates transitions, commits durable state, then publishes the new UI state. Avoid database calls directly from composables or recomposition-driven writes. Use observable state for Home, Learning and Exercise so all three update from the same committed records.

## 7. Proposed data model

| Record | Important fields and purpose |
| --- | --- |
| `learner_profile` | Local UUID, created time, preferences and data-generation ID used for resets/imports. No email required. |
| `lesson_progress` | Profile + lesson ID + progress revision, started/read state, completion time, last-opened time, last block ID and position. |
| `exercise_session` | Durable UUID, profile, accepted package identity, mode, feedback mode, selected pool, active/paused/completed/abandoned/invalidated status, current index, timestamps and row version. |
| `session_question` | Session + position, exact question ID/revision/concept/category, immutable question snapshot and displayed option-ID order. |
| `answer_attempt` | Unique event ID, session + question position, selected option ID, confirmation time, deterministic local sequence, correctness, publication state/time. |
| `study_event` | Stable event ID, lesson completion/reopening or exercise completion, target/revision and time; supports recent activity and recommendation suppression. |
| `content_revision_map` | Accepted package metadata and explicit equivalence mappings for progress preservation after reviewed content updates. |
| `store_metadata` | Database schema version, export format version, selected backend and initialization/migration state. |

Constraints: one answer per session-question position; unique question IDs per session; valid option IDs against the pinned snapshot; at most one unfinished exercise per local profile. Use transaction checks/constraints to enforce these rules, including across browser tabs. Replace process-local `practice-N` IDs with durable UUIDs before persisting sessions. Use database sequence ordering to resolve local “latest”, with timestamps for display, so wall-clock changes do not reorder attempts.

Question progress, chapter completion, category statistics and dashboard totals are derived views. Add rebuildable materialized summaries only if measurements justify them. Index profile/lesson, profile/question/revision, session/position and profile/session-status. Keep exercise history paginated. Content text and artwork remain in the accepted content bundle; only exact snapshots needed for session/history fidelity are stored separately.

## 8. Saving, recovery, and updates

### Reading

Save lesson start and explicit completion transactionally. Save block-based reading position on navigation and lifecycle transitions, with a short debounce while scrolling. Reuse canonical target resolution; a missing block restores to the lesson start with a clear notice. Saved offsets are advisory across font-size and layout changes. Never let a delayed position write undo a newer completion event.

### Exercises

Persist the session and exact question/option order before displaying its first question. On confirmation, atomically save the answer, publication state and session transition, then show success/feedback. While committing, prevent another confirmation. If storage fails, retain the draft and offer retry rather than displaying “saved”. A crash after commit but before UI update rehydrates the committed state without counting twice.

Save pause, next-question and finish transitions. Final completion and deferred publication share one transaction. Restore a paused exercise without reshuffling, changing feedback mode or revealing explanations early. UI projections, accessibility labels, dashboard aggregates and recommendations must all respect the publication rule.

A second browser tab must not race the same active session: use a session lease or transactionally checked row version and refresh stale views after writes. Reset/import invalidate old session writers through the profile data-generation ID.

### Content and schema changes

Use canonical IDs plus semantic/progress revisions. Preserve progress for unchanged content; editorially equivalent updates can carry progress through an explicit reviewed mapping. A substantive lesson update is shown as needing a reread; a substantive question update is unanswered in current-bank coverage until answered again. Retain old history and clearly label it as an earlier content version. Removed questions are excluded from the current denominator without deleting historical results.

Before resuming, validate the pinned package, question revisions and required assets. If the app can no longer faithfully render the saved snapshot/assets, invalidate the active exercise with a clear restart action; do not silently replace questions or rescore old answers against new content.

Database schema migrations are versioned and tested against saved fixtures; never use destructive fallback for user progress. On unreadable storage, preserve the file/data, show a recoverable state, and allow deliberate reset only through the data-management flow.

### Data controls

Include “Your data” below the main dashboard actions: versioned JSON export, validated import and confirmed reset. Exports contain records and the content/version identifiers needed to interpret them; no bundled artwork is necessary. Validate format, size, IDs, relationships and completion invariants before a transaction. Recompute scores from validated accepted snapshots where available; label unverifiable older imports as historical rather than trusting arbitrary aggregate values.

For version 1, import is an explicit replacement, with a review of record counts and an export opportunity first. Cross-device merging is not implied. Reset confirms the exact scope, clears active/derived/local history state together, and leaves the accepted curriculum intact.

## 9. Delivery sequence and completion gates

| Phase | Work | Exit condition |
| --- | --- | --- |
| 0. Design approval | Review the three-tab board, tracking rules and local-first scope; generate supplementary/revised states as needed. | Explicit approval for the layouts to be implemented. |
| 1. Storage spike | Small persistent database across Android, iOS, JVM and browser; compatibility, worker packaging and reopen checks. | Recorded dependency/backend decision; write/read/restart proof on real platform targets. |
| 2. Progress foundation | Schema, migrations, repository, stable IDs, snapshots, metrics and content reconciliation. | Contract tests and migration fixtures pass; duplicate writes cannot inflate progress. |
| 3. Durable user actions | Wire lesson completion/position and confirmed answers; implement pause/resume/finish and failure handling. | Kill/relaunch retains readings and resumes exact exercise state with correct reveal behavior. |
| 4. Navigation and Learning | Three tabs, retained tab stacks, chapter progress and approved reader actions. | Real completion data appears consistently after navigation and restart. |
| 5. Exercise hub | New modes, coverage, targeted selection, history and result navigation. | Small/empty pools handled; mixed selection and accepted-content constraints preserved. |
| 6. Home dashboard | Derived insight cards, last read, next-step engine and all approved empty/error states. | Each insight agrees with stored events and every CTA opens the intended content. |
| 7. Data controls and release | Export/import/reset, content-update cases, accessibility, cross-platform acceptance and documentation. | End-to-end release checklist below passes. |

Phases are ordered dependencies, not a promise of parallel execution. Storage, reader tracking and exercise tracking can be reviewed as separate changes. Do not activate the dashboard with fake progress while persistence is unfinished. Existing user changes and migration verification evidence must remain untouched unless a later implementation task explicitly requires updating relevant behavior/tests.

### Selection changes that need explicit implementation work

The current mixed selector validates a full accepted bank and uses category quotas plus concept deduplication. Targeted modes must authenticate the full accepted package first and derive their pool internally; do not pass a filtered list through the existing full-bank identity check or bypass it. Targeted pools use their own capacity checks and mode labels, and do not promise the mixed-test distribution. Continue preventing duplicate concepts within an exercise. Rotate among unanswered variants across sessions so coverage can eventually reach all 1,000 question IDs despite the concept-level deduplication rule.

## 10. Acceptance and verification

- Fresh installation: 0/10 chapters, 0/40 lessons, 0/1,000 questions; useful first action and no fabricated accuracy.
- Mark all four lessons in chapter 1 read: Home shows 1/10 and Learning shows 4/40; force-stop/relaunch retains both. Mark one unread: chapter returns to in progress.
- Confirm 10 different immediate-feedback questions: coverage rises by 10. Repeat one question three times: coverage stays unchanged while attempt history grows.
- Latest correct/incorrect status changes review membership consistently; correct plus revisit equals published unique coverage for the current revision.
- Deferred exercise: no score, correctness, review-queue change or next-step leak before finish, including after restart and in accessibility output.
- Crash before/after confirmation and final completion: no lost committed answer, duplicate event, double completion or changed option order.
- Resume from Home after process restart. Switch tabs, follow a reference, return, and end/replace an exercise without losing unrelated progress.
- One remaining distinct concept, no unanswered questions, empty review pool and unsupported chapter mappings produce valid smaller exercises or useful empty states.
- Current-content update changes only the affected progress; removed/changed questions remain traceable in historical results. Expired snapshots fail safely.
- Export/import round trip, malformed import, migration from older fixtures, storage quota failure, reset with a stale tab, and multi-tab confirm races are verified.
- Android and iOS process termination; browser reload, tab close/reopen, persistence denial and supported Chrome/Safari/Firefox configurations tested. Offline progress operations verified separately from availability of the web app's cached shell/assets.
- At 320–430dp widths, tablet widths, dark mode and 160–200% text scaling: no hidden primary action, overlapping navigation, clipped essential text or inaccessible completion control. Verify TalkBack/VoiceOver, keyboard focus and reading order.
- Existing accepted question/content tests, scoring, no-duplicate-concept selection, source/reference routes and feedback reveal tests remain passing; tests that intentionally asserted process-loss behavior are updated to the new durable contract with a documented reason.

Keep pure domain tests for metrics/recommendations separate from database integration tests and a small set of platform journeys. Run the same repository behavior contract against each selected backend. No separate benchmark project is necessary; measure dashboard startup and write responsiveness on representative devices before release.

## 11. Optional later phase: cross-device sync

If desired, add accounts and an authenticated backend after local persistence is stable. The local repository remains usable offline; upload immutable answer/study event IDs through an outbox and deduplicate them on the server. Define lesson completion/unread conflict resolution, reset/deletion tombstones, content revision compatibility and server ordering before rollout. Initially keep active exercises device-local to avoid concurrent-answer conflicts; sync completed history and reading progress first.

Backend provider, account UX, retention/deletion policy and operating cost need a separate selection. They are not dependencies for the requested local progress dashboard. Manual export/import in version 1 provides portability, not automatic synchronization.

## 12. Approval boundary

This turn delivers the plan and generated design. Implementation begins only after explicit design approval, following the user's design workflow. Approval of the main board permits that layout; any newly requested or substantially revised design is previewed and approved again before implementation. Commit and PR wording must follow the user's naming restrictions.
