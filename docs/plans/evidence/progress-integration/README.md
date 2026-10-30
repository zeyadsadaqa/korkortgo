# Approved Exercise, Home and data controls integration

30 October 2026. Implements the approved phase-5, phase-6 and phase-7 light-theme flows. Release qualification remains separate from feature implementation.

## Delivered

- Exercise coverage, mixed/unanswered/review/chapter/category setup, real pool capacity, one question per concept, preference for unanswered variants across sessions, durable mode/filter labels, resume, paginated history presentation and completed-result reopening. Ended entries have no completed score. Older unavailable snapshots remain history with an explicit unavailable result.
- Home uses one committed record snapshot for reading/question counts, last completed chapter and a deterministic next action. Priorities are active exercise, recent incomplete reading, eligible practice for a newly read chapter, an appropriate review set, first unread lesson, then unanswered/mixed practice after reading is complete. Completion suppression is written in the same transaction as exercise finish. Reading/open and completion order are persisted in metadata; block saves do not reorder openings.
- Your data exports a version-1 JSON backup, stages and validates import before explicit replacement, offers export first, and confirms reset consequences. Replacement/reset rotate the generation in a rollback-capable transaction and rebuild the UI against that generation. Curriculum/assets and external backup files remain. A generation change observed by another window refreshes its environment.
- Platform file adapters use Android document contracts, iOS document pickers, a desktop chooser, and browser file input/download. Browser download handoff is described as requested, not proof that a file was saved.
- Android retains tab, setup, reader and draft UI state in a ViewModel through Activity recreation. The prior `configChanges` opt-out is removed. Durable records recover after process death; transient navigation/filter/draft UI is not promised across process death. Navigation consumes safe drawing and keyboard insets.
- Store-opening recovery preserves the file and offers Retry plus a confirmed logical reset attempt. Reset succeeds only if the store can open and complete an atomic operation. It never silently deletes a damaged SQLite file. An unrecoverably corrupt/unopenable database can still require external recovery; this is not an automatic file-repair feature.

## Automated and build evidence

The final test results are recorded in [test-summary.json](test-summary.json). Tests cover targeted pool boundaries, accepted-bank authentication, concept deduplication and variant rotation, deferred publication, recommendation priority and suppression, ordered reading completion, historical-result reopening with an active exercise, format/content validation, reopen after transfer, stale-generation rejection, reset scope and injected transaction rollback. Existing migration and scoring/navigation checks remain in the suite.

See [final platform build](platform-build.txt) and [test build](test-build.txt). One preceding combined Android build hit a Kotlin heap limit; final platform verification uses one worker and a 6GB compiler/Gradle heap. No dependency/compiler version was changed to work around that resource failure.

The schema stays at version 2: mode labels, cursors and reading/recommendation ordering use the existing metadata table. Existing schema-1-to-2 migration tests continue to run. JSON transfer format version 1 is distinct from the Room schema version.

## Android runtime

The `verification` build installs as `se.korkort.study.verification`, with separate storage. Runtime checks used emulator-5554; the normal application's database and the other emulator were untouched. See [journey assertions](android-journey-summary.json) and the corresponding `integrated-*.json` hierarchies.

1. Fresh profile shows zero current coverage and a real first-lesson action.
2. A one-question end-feedback exercise confirms an answer while Home remains at zero answered. Finish publishes it, producing one answered/one to revisit and a completed result.
3. Android's native document picker saves the backup, and the application reports completion. [Format summary](backup-format-summary.json) confirms an explicit format/version and the synthetic exercise records; the full answer-bearing backup is not copied into this evidence folder.
4. Keep my progress cancels reset without losing history. Explicit reset clears the disposable profile. Selecting its saved backup shows a checked replacement preview; explicit Replace restores history.
5. An unsupported file is rejected before mutation. The existing completed exercise remains. Force-stop/relaunch retains imported coverage.
6. Review setup derives a one-question pool from the latest incorrect answer. Mode and setup survive real landscape/font-scale recreation. At 200% text, primary setup actions remain reachable by scrolling and all bottom labels remain visible. Display settings were restored.

The screenshot artifacts show synthetic test data. Mockup images are approval references, not runtime evidence.

- [Final Android Home](android-home.png) and [Exercise](android-exercise.png).
- [200% text checkpoint](android-200-percent.png); the final build also corrects singular-question wording shown in this earlier checkpoint.
- [Chrome phone](chrome-phone.png), [wide window](chrome-wide.png), and [startup/reopen result](chrome-startup.json). The isolated profile creates and reopens its OPFS progress file across browser restart. This startup-only check is supplemented by the native-to-Chrome transfer check below.

Final automated total: **119 tests**, 105 application and 14 repository tests, with no failures, errors or skips. The final clean test command succeeds. Android debug and isolated verification APKs, iOS device/simulator compilation, and the Wasm production distribution all build successfully. Chrome uses a disposable profile and a local server with the required isolation headers; both are cleaned up afterward.

## Android-to-Chrome portability

The final Wasm build imported the Android-exported synthetic backup through a Chrome file input, displayed its checked record preview, and required explicit Replace progress. Home then showed one answered question and one to revisit. Chrome downloaded a new backup of that imported state. Comparing the two files, allowing the intentional local profile-ID remapping, found identical sessions, snapshots, option order, answers/publication, events and mode metadata. See [portability assertions](chrome-portability.json), [import review](chrome-import-review.png), [import completion](chrome-imported.png) and [Home after import](chrome-imported-home.png).

The file chooser was intercepted through Chrome DevTools for the headless test. This is a real UI/file-input and download path in isolated Chrome, not evidence of Safari/Firefox chooser compatibility. Disposable browser profiles and servers were closed afterward.

## Limits of release acceptance

Android journeys above and desktop automated tests were exercised. iOS device/simulator and Wasm compilation are build evidence, not proof of platform picker/lifecycle acceptance. Chrome startup/reopen and native-backup import/re-export checks are limited to the tested Chrome engine and isolated profiles.

Final branded Safari/Firefox file handling, iOS picker/termination journeys, screen-reader journeys, production-host storage denial/quota, cross-tab runtime mutation races and dark-mode acceptance remain release gates. The approved design scope retains the established light theme; no dark layout was approved or implemented. Do not advertise full release acceptance from this report. See the [release checklist](../../progress-release-checklist.md).

Platform API references used during implementation: [Android document access](https://developer.android.com/training/data-storage/shared/documents-files) and [Apple document picker](https://developer.apple.com/documentation/uikit/uidocumentpickerviewcontroller).
