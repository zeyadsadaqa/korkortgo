# Section 8: saving, recovery, and updates

30 October 2026. This addresses **section 8** of the dashboard plan, not an additional delivery phase. Delivery phases still end at 7. Existing approved layouts are reused.

## Audit and fixes

| Requirement | Implementation |
| --- | --- |
| Transactional lesson start/completion | Existing repository transactions and monotonic reading order retained. |
| Debounced position plus navigation/lifecycle save | Existing 200ms debounce and disposal flush retained; registered position flushes now also run on Android stop, iOS resign-active, desktop deactivation/closing, and browser visibility/page-hide callbacks. A cached in-process reader position is not overwritten by an older database position on remount. |
| Missing saved block | Restore to the lesson start with an accessible notice. Explicit canonical navigation continues to use the canonical resolver. |
| Exact exercise restore | Session row, confirmed answers, cursor and pause flag are read in one transaction. Displayed option order and feedback remain pinned. |
| Concurrency | Visible exercises carry their observed row version. Confirmation/advance/finish use that version rather than fetching a new version just before writing. Competing writes fail without mutation; committed identical answer/advance retries remain idempotent. Live quiz views refresh from the persisted state after another connection changes it. |
| Durable pause | Leaving a live quiz, pausing explicitly, or backgrounding records pause metadata and increments the session version. Returning offers resume; explicit resume clears pause and reads the current snapshot. A stale window cannot confirm through a pause/resume cycle. |
| Unavailable saved content | Package, revisions, option membership and required artwork identity/integrity are validated. Unsupported packages or integrity failures archive the active exercise as unscored ended history with an unavailable marker and a restart action. Deferred answers stay unpublished. Resource I/O failures remain retryable rather than being treated as successful saves or silently deleting progress. |
| Data controls and migrations | Existing generation barriers, atomic replacement/reset, bounded import validation and non-destructive schema migration remain. JSON exports now use format **2** for pause/unavailable state; readers still accept format **1**. The Room schema remains **2**. |

The current accepted package supplies no reviewed editorial-equivalence mappings. Existing repository support and revision/equivalence tests remain; no mappings are fabricated by this work. Changed/removed questions remain excluded from current coverage while historical records are preserved.

Lifecycle saves request a flush before normal background handling. They cannot guarantee a write after abrupt OS/process termination; the last committed state remains authoritative. Unreadable database files are preserved, with the established retry/confirmed logical-reset flow; this does not introduce automatic repair or deletion of corrupt files.

## Composable previews

The updated user instructions require a preview when writing a composable. [RecoveryPreviews.kt](../../../../composeApp/src/commonMain/kotlin/se/korkort/RecoveryPreviews.kt) includes database-free previews for the touched app/reader/loading/recovery/exercise/lifecycle content. The history-row preview is next to its private composable in [StudyScreens.kt](../../../../composeApp/src/commonMain/kotlin/se/korkort/StudyScreens.kt). The shared lifecycle preview binds to each platform's actual implementation.

The host preview bypasses storage creation. Exercise UI accepts immutable bank/catalogue/record inputs so it can preview without a repository. Compose 1.9.3's existing preview annotation library and debug-only renderer are configured; no Compose/compiler upgrade is required. See [official preview setup and supported versions](https://kotlinlang.org/docs/multiplatform/compose-previews.html).

## Verification

- [Build/test transcript](build.txt) and [test totals](test-summary.json).
- Seven new integration tests cover two-connection stale writes, advance races and idempotent retries, paused backup recovery and format-1 compatibility, unavailable package/artwork recovery without deferred publication, position-flush ordering, and serialized asset validation during simultaneous resume/import.
- Android runtime uses only `se.korkort.study.verification` on emulator-5554. [Pause proof](pause-proof.json) reads the stopped synthetic app's database and confirms durable pause, retained active exercise/mode, and incremented row version.
- [Home after pause](section8-paused-home.json), [Home after process restart](section8-after-restart.json), and [resumed question](section8-resumed-question.json) record the resume journey. A real launcher/background transition then returns to the [resume hub](section8-background-resume-hub.json).

Platform lifecycle hooks and previews compile across the configured targets. IDE visual rendering, iOS lifecycle runtime, and live multi-tab browser refresh are not claimed as newly exercised here. Existing outstanding [release gates](../../progress-release-checklist.md) remain open. The unrelated root README and migration edits are untouched.

Final result: **126 tests pass** (112 application, 14 repository), with no failures, errors or skips. Android debug/verification APKs, iOS device/simulator compilation and the Wasm production distribution build successfully with the preview sources included. IDE rendering itself is not claimed as exercised.
