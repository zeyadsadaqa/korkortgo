# Phase-1 storage proof

An independent build for the progress dashboard storage decision. It is not included in the production settings and does not write to the production app's database. The one-table probe is disposable; the learner-progress schema belongs to phase 2.

[Decision, evidence and remaining checks](../docs/plans/evidence/storage-phase1/README.md)

## Pinned dependencies

| Component | Version |
| --- | --- |
| Kotlin and serialization compiler plugin | 2.3.20 |
| Android Gradle Plugin | 8.13.2 |
| KSP | 2.3.12 |
| Room | 3.0.3 |
| AndroidX SQLite | 2.7.1 |
| Coroutines | 1.10.2 |
| JSON serialization | 1.9.0 |
| Kotlin browser bindings | 0.3 |
| SQLite Wasm | 3.50.1-build1 |
| Optional Playwright test engines | 1.64.1 |

The app was separately upgraded to Kotlin 2.3.20 with the user's authorization. Room's iOS artifacts could not be consumed by its previous Kotlin 2.2.20 compiler; the original failure is retained in the evidence.

## Build

Run commands from the repository root. Requirements: JDK 17/21, Android SDK 36, Xcode for iOS, Node 22+ and npm. Supply Android SDK access through `ANDROID_HOME` or an ignored `storage-spike/local.properties` file, for example by copying the root `local.properties`.

```sh
./gradlew -p storage-spike desktopTest assembleDebug assembleDebugAndroidTest compileKotlinIosArm64 linkDebugExecutableIosSimulatorArm64 wasmJsBrowserDistribution
```

The web build runs `npm ci --ignore-scripts` using the committed lock file and packages the worker, Wasm binary and OPFS proxy beside the generated app. There is no runtime CDN dependency. Test engines are downloaded only by the optional install command below.

## Independent JVM processes

```sh
./gradlew -p storage-spike runDesktopProbe -PprobeAction=write
./gradlew -p storage-spike runDesktopProbe -PprobeAction=verify
```

The first process overwrites only the probe database at `storage-spike/build/proof/desktop.db`. The second process reads it without creating the expected row. Verification checks Unicode, ordered option IDs, question IDs, a reading block and that writing the same row twice did not duplicate it.

## Android

Use an emulator serial from `adb devices`. The example uses `emulator-5554`.

```sh
adb -s emulator-5554 install -r storage-spike/build/outputs/apk/debug/KorkortStorageSpike-debug.apk
adb -s emulator-5554 install -r storage-spike/build/outputs/apk/androidTest/debug/KorkortStorageSpike-debug-androidTest.apk
adb -s emulator-5554 shell am instrument -w -e probeAction write se.korkort.storageprobe.test/androidx.test.runner.AndroidJUnitRunner
adb -s emulator-5554 shell am force-stop se.korkort.storageprobe
adb -s emulator-5554 shell am instrument -w -e probeAction verify se.korkort.storageprobe.test/androidx.test.runner.AndroidJUnitRunner
```

Both instrumentation processes must report `OK (1 test)`. Without a `probeAction`, the test performs an ordinary write/close/reopen check. The probe has no activities and uses a separate `se.korkort.storageprobe` package.

## iOS simulator

Boot an available simulator with `xcrun simctl boot <device-id>` first. The executable accesses Application Support through Foundation. Copying it out of Desktop avoids a simulator launch stall observed on this machine.

```sh
cp storage-spike/build/bin/iosSimulatorArm64/debugExecutable/KorkortStorageSpike.kexe /private/tmp/korkort-storage-proof.kexe
xcrun simctl spawn booted /private/tmp/korkort-storage-proof.kexe write
xcrun simctl spawn booted /private/tmp/korkort-storage-proof.kexe verify
```

Both processes must print `STORAGE_PROBE_PASS ios` with the requested action. This proves the simulator's SQLite/serialization path, not full app-container integration or a physical iPhone runtime. The device target is compile-checked separately.

## Browser

```sh
node storage-spike/tools/browser-proof.mjs
```

This starts temporary loopback servers, launches a dedicated headless Chrome profile, writes the probe, verifies it in a new tab, closes Chrome, restarts with the same profile, and verifies it again. It also asserts that a server without isolation headers produces an explicit failure. It closes its browser and servers afterward. Set `PROBE_CHROME` to override the default macOS Chrome executable. Results are in `storage-spike/build/proof/browser/result.json`.

The optional engine matrix uses WebKit and Firefox builds from Playwright:

```sh
PLAYWRIGHT_BROWSERS_PATH="$PWD/storage-spike/build/playwright-browsers" node storage-spike/web/node_modules/playwright/cli.js install webkit firefox
PLAYWRIGHT_BROWSERS_PATH="$PWD/storage-spike/build/playwright-browsers" node storage-spike/tools/browser-matrix.mjs
```

The matrix repeats write, new-tab read and full engine restart for each browser. Temporary profiles are deleted afterward. `PROBE_PROFILE_ROOT` can override the temporary-profile directory. A nonzero result is a failed or unavailable check, not a pass; inspect `storage-spike/build/proof/browser-matrix/result.json`. On the recorded host WebKit passed and Firefox failed before page launch because it could not open its profile. Branded Safari could not be automated because remote automation is disabled.

## Web deployment contract

The selected worker uses SQLite OPFS and requires a secure context plus these response headers:

```text
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

For a manual proof, `python3 storage-spike/tools/serve.py` serves the built artifacts at `http://127.0.0.1:18765`; localhost qualifies as a secure context. `--no-isolation` exercises the rejection path. Real deployments need HTTPS and compatible headers on the app and its assets; cross-origin resources and external-link behavior must be verified during integration. No silent in-memory fallback is provided.

Browser storage is origin-local and may be cleared or evicted. Export/import and persistence requests are later integration work. The proof does not implement offline caching of the app shell, learner metrics, actual question history, migrations, active-exercise restoration or cloud sync.
