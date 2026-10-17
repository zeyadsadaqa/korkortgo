# Native reader and route checks — 17 October 2026

This records the first stage of the user's closure order: native reader/route checks before faint-asset decisions, final 9J acceptance, final 9M3 verification and 9L14 integration. It is verification of isolated components/routes, not production activation or acceptance of held questions.

## Changes verified

- The route retains library query, category, module expansion and scroll state while reading is open. Search has a persistent native accessible name and a Search keyboard action.
- A sign detail's “Road signs and reference” back action opens the reference catalogue. The catalogue retains the deliberate return-to-reading action when a reading origin exists.
- Source, answer-reveal and image triggers explicitly permit focus in touch mode, so a requested return does not silently fail on Android.
- The verification host can start exact canonical, question and frozen-namespace legacy destinations and applies the requested text scale to learning views. These inputs do not add a production URL parser.

## Evidence boundaries

| Check | Evidence |
|---|---|
| Shared regressions and parity | 80 desktop tests, zero failures/errors/skips; Android, iOS simulator and Wasm compilation. Includes complete authored teaching parity, all canonical/legacy route checks and the existing 616-question delivery matrix. [XML and build log](tests/) |
| Generators/content | 144 Python tests; `build_reader.py --check`, `build_navigation.py --check`, `assemble_question_package_9j.py --check` pass. The candidate remains 384 accepted / 616 held. |
| iOS native interaction | Five XCTest UI tests pass on iPhone 17 / iOS 26.5 simulator: search/source/library return, reference zoom/reset/catalogue back, unknown question and legacy chooser, deliberate answer reveal/next reading, and pending held-candidate selection across neutral zoom. [Log](tests/ios-tests.txt), [native trees and screenshots](ios/) |
| iOS scoped accessibility audits | `.sufficientElementDescription` and `.trait` audits pass in the four tests that call them. This is not a full contrast/hit-region audit or VoiceOver listening test. |
| Android native interaction | Five native `AccessibilityNodeInfo` route tests cover the corresponding flows, including actual keyboard focus on the restored source trigger. [Log](tests/android-tests.txt), [native trees and screenshots](android/routes/) |
| Android TalkBack interaction | Real pointer swipes in the embedded emulator move TalkBack focus through library controls, lesson content and pending assessment option/image controls. [Library](android/talkback-library/), [lesson](android/talkback-lesson/), [assessment](android/talkback-candidate/). The bound spoken-feedback service and touch exploration are recorded. |

TalkBack collection deliberately runs outside UiAutomation. The initial instrumentation plus injected-key/swipe approach did not establish traversal and is not counted as a pass; a standalone capture records visible native TalkBack focus movement with real emulator pointer input. The collector's green-outline bounds are an aid to reviewing the screenshots, not an automated assertion of speech content. Native tree and shared projection checks establish the neutral labels and reveal boundaries. No audio comprehension or every-question spoken review is claimed. Launch/scroll transitions can produce additional positions; count the visibly distinct controls/text in the screenshots, not the raw bounds count alone.

The user selected iOS simulator scope. Apple documents that VoiceOver is unavailable in Simulator; native XCTest interaction, accessibility trees and the named audits supply the chosen simulator evidence. [Apple accessibility testing guidance](https://developer.apple.com/documentation/accessibility/performing-accessibility-testing-for-your-app).

## Reproduction

Use Java 17. Verification binaries require `-PreferenceProof` and cannot be released or published.

```sh
python3 tools/build_reader.py --check
python3 tools/build_navigation.py --check
python3 tools/assemble_question_package_9j.py --check
python3 -m unittest discover -s tools -p 'test_*.py'
./gradlew :composeApp:desktopTest :composeApp:compileDebugKotlinAndroid :composeApp:compileKotlinIosSimulatorArm64 :composeApp:compileKotlinWasmJs --offline --no-daemon
./gradlew :composeApp:assembleDebug :composeApp:assembleDebugAndroidTest -PreferenceProof --offline --no-daemon
adb install -r composeApp/build/outputs/apk/debug/composeApp-debug.apk
adb install -r composeApp/build/outputs/apk/androidTest/debug/composeApp-debug-androidTest.apk
adb shell am instrument -w -r -e class se.korkort.NativeReaderRouteTest se.korkort.study.verification.test/androidx.test.runner.AndroidJUnitRunner
```

For real TalkBack traversal, use Python with Pillow and run `tools/run_native_reader_android.py --output <new-folder>`. After “Ready”, swipe right over the emulator's native surface. Use `--mode candidate --code sign-recognise-A1 --positions 14` for assessment and `--mode learning --code M01-L01 --positions 12` for reading. The collector restores the original accessibility settings in `finally`. Dismiss the optional notification prompt with “Don't allow”; notifications are unnecessary. Native functional checks were run with TalkBack enabled, restored afterward.

For iOS, build `:composeApp:linkDebugFrameworkIosSimulatorArm64 -PreferenceProof`, copy its framework to the Xcode framework search directory, then build the shared `NativeRouteTests` scheme with `OVERRIDE_KOTLIN_BUILD_IDE_SUPPORTED=YES CODE_SIGNING_ALLOWED=NO`. Copy aggregated simulator Compose resources into the built app's `compose-resources/composeResources`. Run `xcodebuild test-without-building -xctestrun <explicit generated .xctestrun> -destination 'id=<simulator>' -parallel-testing-enabled NO`. Use `xcresulttool export attachments` for the retained native trees/screenshots. The saved log records the concrete simulator/run.

## Remaining ordered work

1. Resolve S5, S6, S7, S11, S12, S13, T1, T2, T6, T8, T22 and X8. Any presentation change requires an imagegen preview and explicit user approval before implementation. Preserve original official artwork.
2. Finalize/revalidate the accepted 9J package, then rerun 9M3 against that exact accepted identity. The 616 delivery holds and original replacement records are unchanged by this checkpoint.
3. Execute 9L14 production integration, remove legacy content only with its prerequisites satisfied, then verify the complete production flow. Full integrated acceptance remains 9O/10.

Historical evidence stays unchanged. Current source, binary and evidence identities are in [verification.json](verification.json). Saved text logs have trailing whitespace trimmed; screenshots retain their original bytes.
