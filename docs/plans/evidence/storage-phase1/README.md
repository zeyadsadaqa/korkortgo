# Phase 1: persistent-storage decision and proof

Date: 29 October 2026. Scope: the saved dashboard plan's phase 1, storage compatibility and persistence. The user additionally authorized a Kotlin upgrade when required. This work does not implement the dashboard or the phase-2 progress schema.

## Decision

Proceed with Room 3 / SQLite as the shared storage foundation. Native and browser proof code builds, and independent-process persistence passes on JVM, Android, iOS Simulator, Chrome and the WebKit test engine. The app compiler and Compose compiler plugin have been upgraded together from Kotlin 2.2.20 to **2.3.20**. Compose 1.9.3, AGP 8.13.2 and the Gradle wrapper are unchanged.

The web choice is conditional on configuring HTTPS/secure context and COOP/COEP isolation headers at deployment. The proof intentionally refuses unsupported storage conditions. Retain the plan's IndexedDB alternative if the intended host cannot meet those requirements; decide before shipping real learner data. Do not switch stores automatically across launches.

**Remaining acceptance checks:** Firefox could not launch on this host, so its storage compatibility is unverified. Branded Safari automation was unavailable; WebKit-engine coverage is recorded separately. These gaps must be closed before advertising full supported-browser persistence. No failure of the Room/OPFS runtime was observed in Firefox because no page ran.

## Compatibility finding

The original Kotlin 2.2.20 build passed the desktop test and compiled Android, but failed to compile the Room iOS dependency:

```text
room3-common-iosArm64Main-3.0.3.klib: incompatible ABI version '2.3.0'
The library was produced by '2.3.20' compiler.
The current Kotlin compiler can consume libraries having ABI version <= '2.2.0'.
```

See [original build](kotlin-2.2.20-build.txt). This was an actual compiler result, rather than an inference from the library's Maven Kotlin-stdlib version. Kotlin 2.3.20 resolved it. Pin KSP 2.3.12, Room 3.0.3, SQLite 2.7.1, coroutines 1.10.2, JSON serialization 1.9.0 and browser bindings 0.3 in the isolated build. The complete dependency list and commands are in [the proof README](../../../../storage-spike/README.md).

## Evidence matrix

| Check | Result | Evidence |
| --- | --- | --- |
| Desktop file close/reopen test | 1 test, 0 failures | [native build](native-build.txt) |
| JVM independent writer and reader processes | Passed; Unicode, IDs, option order and row count retained | [write](desktop-write.txt), [read](desktop-verify.txt) |
| Android emulator | Passed two instrumentation runs with target-package force-stop between them | [Android transcript](android-persistence.txt) |
| iOS 26.5 iPhone 17 simulator | Passed separate writer and reader executable launches | [iOS transcript](ios-persistence.txt) |
| iOS device architecture | Compiled successfully; no physical-device runtime claim | [native build](native-build.txt) |
| Chrome 156.0.8078.74 | Passed write, new-tab read and full browser-process restart | [Chrome results](chrome-persistence.json) |
| WebKit 27.2 / Playwright | Passed write, new-tab read and full engine-process restart | [engine results](browser-engine-persistence.json) |
| Missing isolation headers | Explicit rejection, as expected; no in-memory success | [Chrome negative case](chrome-persistence.json) |
| Firefox 157 / Playwright | Unavailable: exits before page launch with “Could not find profile folder”, including alternate temporary-profile paths | [engine results](browser-engine-persistence.json) |
| Branded Safari 27.0.1 | Unavailable: WebDriver reports remote automation must be enabled; settings were not changed | [Safari response](safari-availability.json) |
| Existing app regression suite on Kotlin 2.3.20 | 86 tests, 0 failures/errors/skips; Android APK, iOS device compile, simulator framework and web production distribution built | [app build](app-kotlin-upgrade.txt), [test totals](test-summary.json) |

The browser matrix command deliberately exits nonzero when an engine fails or is unavailable. The recorded Firefox launch failure is not treated as successful browser acceptance. WebKit automation is not identical to branded Safari acceptance on a physical iPhone.

## What the proof establishes

The independent `storage-spike` build has one Room entity keyed by a stable string. It serializes a payload with a lesson ID, revision, block ID, Unicode text, question IDs and an exact option order. A writer stores the same row twice; a separate reader verifies exactly one row and exact decoded equality. Readers never insert a missing record. The web path uses the released Room driver and a pinned, locally packaged SQLite Wasm worker; no runtime CDN or in-memory substitute is involved.

Android uses an application-private database. iOS uses Foundation's Application Support directory. The iOS command-line proof is a simulator executable, not an installation of the production app; app-container/lifecycle integration remains phase 3. On this host an executable launched directly from Desktop stalled in the simulator's loader, so the reproducible command copies it to `/private/tmp` first. The successful transcript uses that accessible path.

This does not yet establish learner metric calculations, answer publication rules, durable active-session recovery, migrations, corrupted-store recovery, eviction protection, import/export, reset behavior, multi-tab ownership, or cloud synchronization. Those are the later phases already specified in the plan. The sample row must not become the real progress schema.

## Production integration requirements

1. Create the phase-2 `progress-data` module and real schema using the versions proven here. Do not depend on this disposable Android probe application.
2. Keep the native app-data database factories and browser worker setup behind the shared repository contract. Database ownership and coroutine scope belong outside composables.
3. Include and version the complete worker/runtime asset set; preserve third-party notices and verify MIME types, CSP, caching and COOP/COEP on the actual deployment. Worker initialization errors must reach the application’s storage-error state.
4. Complete Firefox and branded Safari acceptance; exercise normal/private storage, storage denial, multiple tabs and app lifecycle recovery before release.
5. Verify browser persistence requests and supply the planned export/import flow. Origin-local storage is not a cross-device backup.

## Sources

- [Room release notes and web setup](https://developer.android.com/jetpack/androidx/releases/room3): stable version and worker-backed browser support.
- [SQLite releases](https://developer.android.com/jetpack/androidx/releases/sqlite): released web and bundled drivers.
- [Room KMP setup](https://developer.android.com/kotlin/multiplatform/room): shared database declarations and platform factories.
- [KSP releases](https://github.com/google/ksp/releases): compiler plugin selection; actual compatibility is established by the recorded builds.
- [Browser storage durability](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria): storage may be cleared or evicted.

The worker's exact upstream revision, source hash and Apache license are retained in [third-party provenance](../../../../storage-spike/web/THIRD_PARTY.md).
