# 9O3 — Android integrated candidate checks

The Android candidate uses the unchanged [9O2 accepted identity](../9O2/candidate.json): file SHA-256 `ba91c96975c39b5f6db552c6bead17c0e0474c11dd590f811a7eeb1e1ae54a21`, declared package digest `d9ba2f0261dc9c908146676f903a5ee7fd9c73b50231cd10c2182ecf5d87f82a`. The [package report](package-resources.json) records the normal APK hash, all 484 packaged artwork bindings and both bundled font licences. ZIP hashes are package identities, not claims that two separately built APKs must be byte-identical.

**Result — 19 October 2026:** Complete for the available Android emulator. Normal builds/resource parity and offline launch pass; all six native checks pass across five initial passes and the corrected-selector focused rerun. The final normal APK is restored with no proof activity. No required check remains unresolved within this emulator scope; limitations and prior supporting accessibility/delivery evidence are explicit below.

## Scope and evidence

The available target is `emulator-5554`, Android API 36 / ARM64. [Environment](runtime-environment.json) retains device and original connectivity/accessibility settings. Wi-Fi and mobile data were disabled before the normal launch and remained disabled during the native checks. External websites are not expected to load offline; the source test opens the app's locally bundled source records and returns to teaching.

- `android-normal-build.txt`, `normal-apk-badging.txt`, `normal-offline-home.png` and `.xml`: normal `se.korkort.study` APK without the proof launcher; actual offline home displays the accepted counts and editorial artwork.
- `android-proof-build.txt`, `proof-apk.json`, `native-command.json` and `native-tests.txt`: opt-in native harness and its initial six checks. Five passed; library search selected the identically named EditText instead of the lesson row and failed to open the reader. `native/failure.*` preserves the observed library screen/tree. This is a test-selector failure, not a passing reader run.
- The corrected test waits for a visible noneditable matching lesson row and activates its clickable ancestor. `android-proof-retry-build.txt` and `native-retry-tests.txt` retain the affected test rerun. `test-inputs.json` records the original harness phase; `test-inputs-final.json` records the corrected harness, leaving production sources unchanged.
- `native/` contains initial native screenshots and accessibility trees; `native-retry/` retains the corrected search → lesson → source → focus return → query-preserving library return evidence.
- `android-final-normal-build.txt` records final normal-output restoration; the redundant interim restoration log was removed. `final-normal-package.json` binds the final output and confirms normal identity, absence of proof activity and exact resource parity.
- `results.json` records the actual pass/failure phases, manifest binding, required-check status, limitations and retained artifact fingerprints. `runtime-restored.json` records restored original connectivity settings.

## Reproduction

Use JDK 17 and the configured SDK. Run the normal build and package checks first. The shared build settings are:

```sh
JAVA_HOME=/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home ./gradlew :composeApp:assembleDebug --offline --no-daemon --max-workers=1 -Pkotlin.compiler.execution.strategy=in-process '-Dorg.gradle.jvmargs=-Xmx6g -Dfile.encoding=UTF-8'
```

For native checks, add `:composeApp:assembleDebugAndroidTest -PreferenceProof`; install both APKs and run the exact class/method list in `native-command.json`. The test calls Android `AccessibilityNodeInfo` actions, asserts source trigger focus, captures native trees/screenshots and uses the actual `CurriculumApp(acceptedPracticeBank9J, acceptedCurriculumSummary9J)` for both production feedback modes. Other methods deliberately enter exact isolated routes for unavailable-content recovery, legacy chooser, reader answer reveal/reading order, sign-reference catalogue return and pending-choice neutral zoom. Held candidate zoom is an unscored fixture, not a production session. The production test checks unfinished-session guard cancellation, retained choice, wrong-answer score, Incorrect review expansion, exact related lesson return and retained setup count at 160% text.

Normal builds must omit `-PreferenceProof`; restore/install/launch the normal APK afterward. Preserve and restore emulator connectivity settings when testing offline. Do not publish verification binaries.

## Accessibility and delivery limits

Fresh native node interaction, reveal boundaries, focus restoration and zoom/selection behavior are checked here. The prior [Android TalkBack traversal evidence](../native-reader-routes/README.md) and accepted [artwork/native delivery matrices](../closure-9j-9m-9l14/README.md) remain supporting evidence, not newly recorded speech or a fresh exhaustive matrix in this step. No production UI or artwork changes were made. This run does not claim physical-device coverage, spoken-content comprehension, every asset visually inspected again or external-site availability offline. Platform checks beyond this available Android emulator and step 10 release acceptance retain their own scope.

## Retention cleanup

[Cleanup record](cleanup.json) lists the removed interim restoration log and three repetitive result/setup PNGs. The deferred-result screenshot, all native accessibility trees, both feedback-mode passing assertions, initial selector-failure proof, corrected source-return captures, normal APK/resource identities and final restoration evidence remain. Full runtime/acceptance inputs and historical evidence are unchanged.
