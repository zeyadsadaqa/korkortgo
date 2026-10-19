# Approved larger artwork presentation — 17 October 2026

Implemented after the user explicitly replied **“approved”** to the [saved imagegen preview](../../../app-design/faint-assets-v1/review.md). This checkpoint verifies the approved presentation and exact-asset delivery. It does not accept the 616 held questions or activate the production migration.

## Implementation

`readableArtworkFrame` provides the available width, a 3:2 image area and a minimum height of 220 dp. All assessment image options use the same frame, without testing the asset's code or whether the option is correct. Stem, review and lesson images reuse it; wide reference details retain their existing 380 dp minimum. Images remain aspect-fit within the frame, with white backing in both themes. The existing neutral viewer titles, zoom/pan/reset/Close controls and focus/selection behavior remain in place.

All twelve original and bundled asset hashes match the approved bindings. No source geometry, line weight, colour, crop, authored question, explanation, description, semantic revision or eligibility changed. The small 105 dp assessment image minimum has been removed. Verification fixtures use the actual new frame rather than replaying the obsolete size.

## Checks and captures

| Check | Result / evidence |
|---|---|
| Shared component, parity, state and delivery tests | **80 desktop tests pass**, zero failures/errors/skips. Includes 616 held revisions × four theme/text settings: 2,464 question runs and 6,160 image zoom/returns. [XML/build log](tests/), [fresh matrix](desktop-delivery.json) |
| Affected question bindings | All **24** affected revisions have four passing shared delivery rows. [Exact slots and results](affected-question-checks.json) |
| Authoring/generator checks | **144 Python tests pass**; deterministic 9J assembly, complete reader and navigation checks pass. Content remains 384 accepted / 616 held. |
| Android native | **Six tests pass**, including twelve assets × light/dark × 100%/160% text. Every context captures inline/option/enlarged artwork and exercises zoom/reset/Close. [48 contexts / 144 screenshots and native trees](android/), [test log](tests/android-tests.txt) |
| iOS simulator artwork | The **48-context matrix passes**, with 144 screenshots and native trees. [Captures](ios/), [export-name map](ios-attachment-map.json), [matrix run log](tests/ios-matrix-and-initial-routes.txt) |
| iOS route regressions | **Five route tests pass** after correcting the test's scrolling assumptions for larger images. [Final run](tests/ios-route-tests.txt), [native trees/screenshots](ios-routes/) |
| Wasm browser | Actual 390×844 browser rendering captured for all **48 contexts**. [Screenshots, exposed labels and index](wasm/). This is visual rendering evidence, not browser screen-reader certification. |
| Compilation/builds | Normal Android, iOS simulator and Wasm compilation pass; native verification and Wasm development builds pass. [Build logs](tests/) |

Native geometry confirms equal stem/option areas: Android frames are 1,198×799 physical pixels on the tested emulator; iOS frames are 370×246.7 points. At large text, the first stem and last option can require separate scroll positions. Their complete frames were compared across the inline and option captures, rather than mistaking clipped accessibility bounds for actual image sizing. [Android geometry](android-geometry.json), [iOS geometry](ios-geometry.json).

## Visual review and limits

Reviewed all twelve codes across the four theme/text combinations using the raw captures and analytical sheets: [Android](android-review/), [iOS](ios-review/), [browser](wasm-review/). The larger frame removes the miniature-option presentation; original outlines, panel text, wheels/windows and other distinguishing geometry are visible at the enlarged size. Original strokes remain thin, and narrow browser captures still show pale fine detail. **Larger layout and successful decoding alone do not establish final scored-use legibility.** No line was thickened or contrast boosted to manufacture a pass. [Per-asset delivery review](asset-review.json).

The analytical sheets crop/resize captured viewports only for comparison; raw screenshots are retained unchanged. They are not replacement official assets. The asset fixtures are not full-question native matrices. The 24-question report records actual shared question runs and links exact asset slots; it does not infer native per-question acceptance from the fixture captures. Existing held records therefore remain held pending those decisions and the remaining route/release conditions. No historical 9F/9J/9M receipt is rewritten as a new approval.

The first iOS run passed the artwork matrix but failed two route tests because the old harness could overshoot controls or tap a partly visible answer toggle. The corrected harness uses slow held drags, safe-area bounds and reversal when the target is above the viewport, and scrolls deliberately to revealed answer content. An intermediate rerun was stopped to correct an over-restrictive bottom bound. The final five-route rerun passes. Earlier logs are retained; no failed run is represented as an entirely passing suite. The matrix runner/source snapshot is preserved in [test-snapshots](test-snapshots/); no app-rendering code changed between matrix capture and the route-harness repair.

Browser rendering used a temporary localhost-only verification server and a temporary phone viewport. Both were cleaned up. Android accessibility settings were restored to their original values. iOS evidence uses the user's selected simulator scope, not a VoiceOver listening run or a new physical-device requirement.

## Reproduction

Use Java 17 and the existing opt-in verification build. Release/publish is prohibited for these binaries.

```sh
./gradlew :composeApp:desktopTest :composeApp:compileDebugKotlinAndroid :composeApp:compileKotlinIosSimulatorArm64 :composeApp:compileKotlinWasmJs --offline --no-daemon
python3 -m unittest discover -s tools -p 'test_*.py'
python3 tools/assemble_question_package_9j.py --check
python3 tools/build_reader.py --check
python3 tools/build_navigation.py --check
./gradlew :composeApp:assembleDebug :composeApp:assembleDebugAndroidTest :composeApp:linkDebugFrameworkIosSimulatorArm64 :composeApp:iosSimulatorArm64AggregateResources :composeApp:wasmJsBrowserDevelopmentExecutableDistribution -PreferenceProof --offline --no-daemon
adb install -r composeApp/build/outputs/apk/debug/composeApp-debug.apk
adb install -r composeApp/build/outputs/apk/androidTest/debug/composeApp-debug-androidTest.apk
adb shell am instrument -w -r -e class se.korkort.NativeReaderRouteTest se.korkort.study.verification.test/androidx.test.runner.AndroidJUnitRunner
```

Build and run the shared `NativeRouteTests` Xcode scheme against the verification framework as described in the [native route checkpoint](../native-reader-routes/README.md). `testFaintArtworkDeliveryMatrix` captures the 48 asset contexts; the other five tests exercise routes. Export attachments with `xcresulttool`; decimal text-scale names require retaining the suffix after the exporter-inserted `_0_<UUID>` fragment, as recorded in the attachment map. Wasm uses `#CODE/delivery/light/1` (or `dark/1.6`) with a full page reload for each startup configuration.

[Verification and file fingerprints](verification.json) bind the app sources, exact assets, binaries, approval and saved evidence. Text logs have trailing whitespace trimmed. Next: complete per-question acceptance using the updated renderer, finalize 9J only when its release validator passes, rerun 9M3 against that accepted manifest, then perform 9L14 integration/legacy cleanup and complete-flow verification.
