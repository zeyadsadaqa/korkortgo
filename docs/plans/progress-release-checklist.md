# Progress dashboard release gates

Prepared 30 October 2026. **Not release-ready.** This is an implementation and verification checklist, not a record of tests executed in phase 7. The user approved the [data-controls design](../../design/progress-dashboard/phase7/README.md), and the Exercise, Home and data-control features are implemented. See [integration evidence](evidence/progress-integration/README.md). Full release acceptance remains pending.

## Baseline and dependencies

| Area | Recorded status | Required next evidence |
| --- | --- | --- |
| Storage, repository and durable actions | Phases 1–3 implemented; see [phase 1](evidence/storage-phase1/README.md) and [phase 3](evidence/storage-phase3/README.md). | Recheck final integrated behavior after later changes. |
| Navigation and Learning | Phase 4 implemented; [102 passing tests and Android runtime checks](evidence/navigation-phase4/README.md) are prior evidence. | Final regression and accessibility journeys. |
| Exercise hub | Implemented following explicit design approval. | Approved implementation, targeted selection, coverage and historical results. |
| Home dashboard | Implemented following explicit design approval. | Approved implementation, consistent metrics, recency and next-step rules. |
| Export/import/reset | Repository and all four platform file adapters implemented; Android file journeys verified. | Approved flows, transactional operations and runtime file handling. |
| Release acceptance | Pending. | Pass the matrix below on the final integrated code and record evidence. |

Unrelated root README and migration edits remain outside this task. Integrated automated tests and platform builds were run; Android journeys use a separate verification package. Prior evidence is distinguished from these new checks in the integration report.

## Implemented data-control contract

1. Define a versioned portable JSON envelope with format identifier, format version, export time, content identities and learner records. Include reading positions, exercise settings/modes, immutable snapshots, confirmed attempts, session status and recommendation/event metadata needed to restore meaning. Exclude bundled artwork and disposable derived totals. Add explicit byte/record bounds before accepting input.
2. Read exports from one consistent repository snapshot. Preserve ordering and publication semantics. Provide Android/iOS/JVM/browser file operations behind a shared contract; use system pickers/save or share UI and truthful cancellation/completion statuses. Keep potentially large serialization and file work off the UI thread. Do not log exported learner contents.
3. Validate import off to the side before any write: format/version, size, unique IDs, known enums, references, snapshot option order, selected options, revision compatibility, sequential answers, concept deduplication, session completion invariants and at most one unfinished session. Derive correctness and publication from authenticated content and status rather than trusting imported aggregates or flags. Unsupported files leave the live database unchanged.
4. Reconcile historical content explicitly. Retain unverifiable old records as clearly historical, without contributing trusted current coverage or silently becoming an active exercise. Resume only when the exact question content and required assets can be restored. Do not run imported paths, URLs or content as executable instructions. If reconciliation needs a new material user-facing layout, preview that layout before implementing it.
5. Stage the validated file for review with record counts and compatibility notices. Bind confirmation to that exact staged content. Exporting current progress must return to the staged review. Never replace data just because the file picker closed or a validation check succeeded.
6. Commit replacement atomically. Remap incoming profile ownership to the local profile and rotate the data-generation token; normalize event ordering without changing which answer is latest. Retain the local accepted catalogue as authoritative. On any error, roll back all learner changes. Make retries unable to create duplicate records or a second active session.
7. Commit reset atomically, rotating the generation and clearing all learner records, session cursors/modes, recommendations and cached projections while retaining accepted content. Serialize against queued writes; stale readers/writers in this process or another browser tab must not recreate pre-reset data. Reconnect the UI to the new generation only after commit. Do not use a destructive schema fallback as a reset mechanism.
8. Preserve unreadable storage during recovery. A deliberate logical reset recovery path is available when normal opening fails, using the approved consequence/confirmation flow. It requires the store to become readable/writable enough to complete the atomic reset; unrecoverable file corruption is preserved for external recovery rather than silently deleting the database. A failed or cancelled recovery must preserve the original data; do not quietly create an empty replacement database and report success.

## Required verification matrix

The integration report links automated and Android evidence for transfer, rollback, generation invalidation, deferred feedback and navigation. The complete cross-platform rows below remain release requirements; a partial pass is not a platform-wide acceptance claim.

| Gate | Acceptance evidence required |
| --- | --- |
| Export/import round trip | Close and reopen a temporary test store after replacement; verify exact reading, snapshot/options, answer order, feedback, active cursor, modes and published coverage. No duplicate events on retry. |
| Malformed or unsupported files | Reject bad JSON, future format, oversized input, duplicate/dangling IDs, invalid options, forged scores/publication, incomplete completed sessions and multiple active sessions. Verify the live store remains byte/record-equivalent as appropriate. |
| Replacement/reset rollback | Inject transactional failure and cancellation; old data survives. Success clears precisely the stated scope and leaves accepted content available. |
| Stale writers and multiple tabs | Queue position/answer writes during reset/import and attempt a stale-generation write afterward. Reopened tabs refresh or present a recoverable conflict; old progress cannot return. |
| Deferred feedback | Export/restore and every Home/Exercise projection preserve staged answers without showing score, latest-correct or review changes before completion. Ended deferred sessions remain unscored and unpublished. |
| Content and schema updates | Migrate saved fixtures without destructive fallback. Equivalent revisions preserve approved progress; changed/removed content has honest current coverage and historical labels. Invalid active snapshots fail safely. |
| Metrics and recommendation routes | Complete/uncomplete a chapter, repeat questions, change latest correctness and finish/end an exercise. Verify consistent cards, recommendation priority/suppression and exact CTA targets; empty/small targeted pools remain valid. |
| Android production lifecycle | File picker/save/cancel flows, force-stop/restart, offline progress, reading recovery, active exercise recovery, rotation and phone/wide layouts on the integrated build. |
| iOS production lifecycle | Simulator/device app-level file handling, cancel/save, app-container persistence and termination/relaunch. Earlier simulator storage-probe execution alone does not satisfy this row. |
| JVM production app | File picker/save/cancel, private storage permissions, restart and keyboard navigation. |
| Browser production app | Chrome, branded Safari and Firefox on the supported deployment; secure context, required headers/workers, file download/import, reload/reopen, storage denial/quota, private-mode behavior and two-tab conflicts. Record unsupported cases accurately. |
| Accessibility | TalkBack/VoiceOver reading and focus order, keyboard/Escape/Back, meaningful progress/status announcements, 48dp targets, 320–430dp and wide windows, 160–200% text, and no nav/IME overlap. |
| Dark mode | Current app retains its established light theme. A supported dark layout requires a supplementary preview, approval and runtime checks before this planned gate can pass; do not mark it verified from a light mockup. |
| Final build and documentation | Appropriate domain/repository/UI tests and Android/iOS/JVM/Wasm builds pass once on final code. Document supported platforms, local-storage limits, file format/recovery, migrations and unresolved gaps. |

Use temporary profiles and synthetic data for destructive tests. Do not reset the user's normal app data as a test shortcut. Do not publish or tag a release merely because this checklist exists. Mark each release gate complete only after the corresponding implementation and evidence are present.
