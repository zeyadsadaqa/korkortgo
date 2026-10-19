# 9O5 — iOS simulator integrated candidate

This run verifies the configured `iosSimulatorArm64` framework and iPhone 17 / iOS 26.5 simulator (`F6E93C4B-958D-4CBB-B95E-537B4FB8070C`) against the unchanged [9O2 manifest](../9O2/candidate.json). [Candidate metadata](candidate.json) retains exact manifest and source fingerprints. This is the user's authorized simulator scope; no physical iPhone acceptance is implied.

**Result — 19 October 2026:** Complete for the authorized iOS simulator scope. Normal/proof/restored framework and app builds pass; all six native tests pass with zero failures/skips, including both production feedback modes and four scoped accessibility audits. All 484 packaged artwork bindings, four fonts and both licence files match. The normal app is restored on the original simulator. No unresolved required simulator check remains; physical-device, speech and full-matrix limitations stay explicit below.

## Build configuration correction

The README instructed users to select a `Korkort` app scheme, but the project only contained the test-only `NativeRouteTests` scheme. The initial normal build failed for that missing scheme; a generic `build` with the test-only scheme also had no runnable destination. The existing `build-for-testing` action confirmed the underlying app target was buildable. Added a shared `Korkort.xcscheme` pointing to the existing app target with normal Build/Run/Profile/Archive actions. `normal-app-scheme-build.txt` verifies the normal simulator build now works. No application source, authored content, artwork, acceptance decision or package identity changed. The new Archive configuration is not an archive/signing/publication test.

## Package and normal launch

`normal-framework-build.txt` records the Gradle framework build. `normal-package-resources.json` binds the normal simulator executable, display name KörkortGo, all 484 artwork bindings and both font licence files. Because Xcode's Kotlin build phase is explicitly skipped in this CLI path, the assembled simulator Compose resources are copied into the app's `compose-resources/composeResources` directory before installation. This is required for this overridden build path, not a claim that an unmodified skipped script copies resources automatically.

The normal app was installed and launched with `simctl`; `normal-home.png` was captured after the launch animation and visually inspected. Source details, teaching, images and fonts are bundled locally. The host's network interfaces were not disabled: this is local-resource/runtime evidence, not an OS network-isolation test or a guarantee that external source sites load offline.

## Native tests and accessibility

`proof-framework-build.txt` and `proof-xcode-build.txt` build the opt-in `-PreferenceProof` host. `native-test-configuration.json` records the six selected tests, proof executable hash and exact expected-label fixture. The fixture is independently reproduced from the accepted JSON; it supplies expected labels for all 1,000 records and does not replace the real running bank. `native-tests.txt`, `native-summary.json` and the retained `native/` attachments record actual execution.

| Test | Scope |
| --- | --- |
| testAcceptedProductionPracticeAndReview | Actual accepted production owner in both feedback modes at 160% text: count 1, pending wrong choice, leave guard/cancel, retained selection, feedback boundary, score 0/1, Incorrect expanded review, related teaching/return and retained count. |
| testLibrarySearchAndSourceReturn | Persistent native search label, exact lesson, bundled source detail, return-to-reading and retained library query. |
| testExactReferenceModalAndCatalogueBack | B1 reference, native image zoom/reset/close and catalogue return at 160% text. |
| testUnknownQuestionAndLegacyChooser | Explicit unavailable recovery and deliberate legacy chooser. |
| testDeliberateAnswerAndNextReading | Hidden/revealed answer and canonical next-reading destination at 160% text. |
| testPendingCandidateSelectionAndNeutralModal | Unscored historical fixture, neutral image viewer, zoom/reset/close and preserved selection; not production acceptance of a held item. |

The four test methods that call `performAccessibilityAudit` check `.sufficientElementDescription` and `.trait`; they do not claim every audit type, spoken-output comprehension or VoiceOver listening. The source-return check asserts existence/hittability, not an iOS VoiceOver focus announcement. Native screenshot/tree evidence supplements those assertions. Existing [accepted delivery matrices](../closure-9j-9m-9l14/README.md) remain separate; this step does not repeat every accepted question/asset visual context.

## Reproduction and restoration

Use Java 17, Xcode 26.6 / simulator SDK 26.5. The simulator is reused, not erased or replaced.

```sh
JAVA_HOME=/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home ./gradlew :composeApp:linkDebugFrameworkIosSimulatorArm64 --offline --no-daemon --max-workers=1 -Pkotlin.compiler.execution.strategy=in-process '-Dorg.gradle.jvmargs=-Xmx6g -Dfile.encoding=UTF-8'
```

Copy `composeApp/build/bin/iosSimulatorArm64/debugFramework/KorkortKit.framework` to `composeApp/build/xcode-frameworks/Debug/iphonesimulator26.5/KorkortKit.framework`, then:

```sh
xcodebuild -project iosApp/Korkort.xcodeproj -scheme Korkort -configuration Debug -sdk iphonesimulator -destination id=F6E93C4B-958D-4CBB-B95E-537B4FB8070C -derivedDataPath /tmp/korkort-9o5-normal OVERRIDE_KOTLIN_BUILD_IDE_SUPPORTED=YES CODE_SIGNING_ALLOWED=NO build
```

For native tests, link with `-PreferenceProof`, copy that framework, build `NativeRouteTests` using `build-for-testing` into `/tmp/korkort-9o5-proof`, copy assembled resources into its app, and copy the hash-verified accepted-root fixture into `NativeRouteTests.xctest`. Set `OnlyTestIdentifiers` to the six methods above in a copy of the generated xctestrun, then run:

```sh
xcodebuild test-without-building -xctestrun /tmp/korkort-9o5-proof/Build/Products/9O5.xctestrun -destination id=F6E93C4B-958D-4CBB-B95E-537B4FB8070C -parallel-testing-enabled NO -resultBundlePath /tmp/korkort-9o5-native.xcresult
```

Normal framework/app outputs are rebuilt without `-PreferenceProof`, resource parity is rechecked, and the normal app is reinstalled/launched after native tests. `final-normal-package.json` records final restoration. `results.json` records the actual native summary, required-check status, limitations and artifact fingerprints. Large temporary build products and xcresult bundles remain outside Git; selected explicit screenshots/trees, summary and logs are retained. Other platforms, physical-device work and step 10 release/publication remain separately scoped.

## Retention cleanup — 20 October 2026

Removed two initial scheme/action failure logs, the superseded fallback build log, an attachment-export status log and three repetitive result/setup screenshots. The configuration issue and correction remain described above. All native trees, passing native summary/log, both feedback-mode assertions, representative screenshots, resource hashes and final normal build/launch evidence remain. The attachment map lists only retained files. [Cleanup record](cleanup.json).
