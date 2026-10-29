# Progress data foundation

Phase 2 adds an independent KMP library to the root build, targeting Android, JVM, iOS device/simulator and Wasm. Production screens are connected in phase 3. The disposable `storage-spike` application is not a dependency.

`openProgressDatabase(path, driver)` accepts the private database location and platform SQLite driver. The application owner must keep the database open outside composables and close it at the end of its scope. Native bundled-driver and web worker deployment requirements remain those established in phase 1.

`ProgressRepository.createProfile()` creates or returns the single local profile and its generation token. Repository transactions validate that token. UUIDs identify profiles, sessions and study events; callers supply a stable answer-event ID and reuse it when retrying an interrupted confirmation. A database-assigned sequence orders answer history independently of wall-clock changes. Stored timestamps support history display.

The normalized schema stores profiles, versioned lesson state, pinned sessions, ordered question identities/options, confirmed attempts, study events and metadata. Accepted catalogue revisions and explicitly reviewed equivalence maps are serialized in metadata rather than duplicated into another table. Question snapshots retain the caller's content JSON and original option order. The application adapter must authenticate the accepted package and validate content/asset availability before calling start/restore; the storage module does not depend on the app's generated question bank.

Repository guarantees:

- Writes and session-version checks share a Room write transaction. A second unfinished session is rejected. Wrong-generation tokens, stale session writers, invalid options, out-of-order answers and conflicting retries fail without partial writes.
- Immediate answers enter coverage at confirmation. Deferred answers remain unpublished until atomic exercise completion; abandoned deferred exercises remain excluded.
- Unique coverage counts current question IDs, correctness uses the latest published answer, and substantive revisions require fresh work. Explicit equivalence maps preserve approved progress; removed questions do not count toward current totals.
- Position saves preserve completion. Explicit read/unread actions replace the logical lesson's current completion state. Chapter completion is derived from its required lessons.
- Reopening the database restores the profile, catalogue, snapshots, option ordering and history. Repository summaries can be observed through Room invalidation of a change marker.
- History queries are bounded and paginated. Inactive sessions remain historical records; no destructive fallback migration is enabled.

Schema 1 is retained as a bootstrap fixture. Schema 2 adds history timestamps and an indexed study-event lookup. The explicit migration adds columns with zero meaning an unknown historical time, preserves existing records, and is tested against the saved schema-1 database. Future changes must retain the schema exports and extend the migration tests.

Run from the repository root:

```sh
./gradlew :progress-data:desktopTest :progress-data:assembleDebug :progress-data:compileKotlinIosArm64 :progress-data:compileKotlinIosSimulatorArm64 :progress-data:compileKotlinWasmJs :composeApp:desktopTest
```

The integration tests cover reopen/serialization, saved catalogue/profile identity, migration, retries, transaction rollback, deferred publication/abandonment, current-content metrics and stale writer rejection. Cross-platform compilation is distinct from exercising these repository flows on each device/browser; runtime integration and those journeys belong to phase 3. Browser cross-tab observation/leases, export/import/reset, lifecycle pausing, package acceptance adapters and the recommendation engine are later integration work.
