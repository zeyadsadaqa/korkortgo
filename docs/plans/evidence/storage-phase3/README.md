# Phase 3 — durable learner actions

30 October 2026. The user approved the supplemental completion, resume and save-failure controls in `design/progress-dashboard/phase3/preview-v1.png`. The selected main design remains `preview-v2.png`.

## Implementation

- Production `App` owns a private Room database through platform factories and an application-scoped save coordinator. Android uses its private databases directory, iOS uses Application Support, desktop uses `.korkortgo` under the user home, and web uses origin-private SQLite storage. There is no silent in-memory fallback or destructive reset on storage failure.
- The accepted-bank adapter authenticates the release before selecting questions. Persisted UUID sessions pin the manifest identity, exact authored question representation, revisions and displayed option IDs. Restoration validates these against the available accepted content; an unavailable exercise can be deliberately ended without substituting questions.
- Confirmation commits before feedback appears. Navigation retains the active exercise. Home and Practice offer resume/end controls. Advancing saves the cursor transactionally before changing questions. The cursor uses session-scoped metadata, so schema version 2 remains compatible without an additional table migration.
- Deferred answers stay unpublished until the exercise completes. Abandoned deferred answers remain excluded from current coverage. Immediate confirmed answers retain their published progress after the exercise is ended.
- Save failure retains the selected answer and offers retry. Answer selection is disabled while committing or awaiting retry. Stable session/position event IDs and idempotent cursor advancement prevent retries from duplicating answers or skipping questions.
- Teaching lessons load their saved block and offset, unless an explicit passage or source-return position takes precedence. Scroll positions are saved after a short debounce and flushed on reader disposal. Writes serialize with other learner actions; completion is never overwritten by a position save. Missing saved blocks fall back to the lesson start.
- The reader exposes mark-read, saved completion, chapter progress, next-lesson and mark-unread controls. These use real repository state. Sources, references and previous/next reading links remain available.
- Browser development runs include COOP/COEP headers. `python3 tools/serve_progress_app.py` serves the production web bundle with the same headers. Real hosting must provide HTTPS and equivalent isolation headers. Worker assets and license notices are packaged locally with the app.

## Validation

[Build transcript](build.txt) and [test totals](tests.json) record 91 application tests and 7 repository tests passing, with no failures or skips. Android APK, iOS device/simulator compilation and Wasm production distribution succeeded.

Five new adapter integration tests cover actual accepted-bank selection, close/reopen with the same question/option order and cursor, deferred reveal/publication, idempotent advance/completion, abandoned-exercise behavior, rejected-bank isolation, an injected closed-database confirmation failure followed by retry, and queued reader writes during an active save. Existing seven repository tests retain migration, revision reconciliation and duplicate-write coverage.

Android emulator evidence records a production-app confirmation, force-stop, APK update, resume of the same deferred question, and advancement to question 2. The exercise retained one confirmed answer and did not reveal correctness. See the captured accessibility layouts and journey assertions. The completed lesson was also reopened after force-stop, and its saved completion control and reading location were restored. See `android-reader.json` and `android-reader-restored.json`.

Chrome production startup creates the OPFS database, closes the browser, and reopens it with the same isolated profile. The [settled screenshot](chrome-startup.png) shows the normal home screen after reopening. This is a database-startup/reopen smoke check, not a complete browser exercise journey.

## Scope and remaining checks

The navigation shell, chapter list redesign, exercise hub and dashboard insights belong to the later phases. Their existing screen layout is retained while these data paths are connected. An unfinished exercise is stored as active; being on another screen or restarting implicitly pauses its presentation without changing its accepted answers or feedback mode.

The iOS factories compile, but the full production iOS lifecycle journey has not been repeated here. The phase-1 Firefox launch and branded-Safari automation limitations remain. Storage quota denial, physical-device accessibility acceptance, reset/import/export, cross-tab ownership and the complete release matrix remain release checks. No cross-device synchronization is introduced.

Confirmed answers and acknowledged completion are durable. Unconfirmed selections remain drafts. A hard kill during the reader's short position debounce can restore the most recently committed position; operating systems do not guarantee a final callback before termination.
