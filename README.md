# KörkortGo

An English-language Swedish category B theory app built with Kotlin Multiplatform and Compose Multiplatform. One shared UI, question bank and test engine run on Android, iOS and the web.

## Features

- **1,000 questions**, four options each, with a correct answer and an explanation for every option.
- Five knowledge areas: vehicle knowledge, environment, traffic safety, traffic rules and personal conditions.
- Any test length from **1 to 70**.
- Immediate feedback or answers revealed only after completing the test.
- Results by category, filtered answer review, related lessons and another-test flow.
- 10 original modules, 40 lessons, module reviews, appendices and a searchable learning library.
- 400 official sign, marking and signal reference entries, available offline in the native apps and bundled with the website.
- Responsive layouts, accessible labels and explicit correct/incorrect states.

### Selection rules

A 70-question test first draws 7 vehicle, 5 environment, 16 safety, 32 rules and 5 personal questions. It then draws 5 additional questions from the remaining whole bank. All 70 count towards the practice score. Questions and option order are shuffled.

For shorter tests, the six allocations are proportionally scaled using the largest-remainder method. Rounding ties are resolved in category order. Both sign-recognition directions and calculation variants share a concept identifier, preventing the same learning point from appearing twice in a test. Selection is random across available learning points, then across their variants.

This is an independent practice app, not an official Trafikverket examination or a claim to reproduce official exam questions.

## Run

Requirements: JDK 17 or 21, Android SDK 36 for Android, and macOS with Xcode for iOS. Dependencies download on the first build. The checked-in Gradle wrapper pins Gradle 8.14.3.

```sh
# Shared engine/content tests on the JVM
./gradlew :composeApp:desktopTest

# Browser development server
./gradlew :composeApp:wasmJsBrowserDevelopmentRun

# Static production website
./gradlew :composeApp:wasmJsBrowserDistribution
# Serve composeApp/build/dist/wasmJs/productionExecutable over HTTP(S).

# Android APK
./gradlew :composeApp:assembleDebug
# Output: composeApp/build/outputs/apk/debug/composeApp-debug.apk
```

Set `sdk.dir` in an untracked `local.properties`, or configure `ANDROID_HOME`. Android Studio can open the repository directly.

For iOS, open `iosApp/Korkort.xcodeproj`, select the Korkort scheme and an iPhone/iPad simulator, then Run. The Xcode build phase builds and embeds the shared Kotlin framework and Compose resources. Device installation requires your own signing team. Both Apple Silicon simulator and ARM64 device targets are configured.

The browser uses WebAssembly GC, supported by modern Chrome, Edge, Firefox and Safari. No server, account or remote question-generation service is required.

## Content and migration

[Migration brief](MIGRATION.md) records the migration outcome, retained book hashes, source credits, recovery archive and remaining acceptance work.

- `content/curriculum.json`: canonical teaching, references, navigation and artwork records.
- `content/accepted-assessment-questions.json`: the accepted 1,000-question production bank.
- `content/accepted-content-manifest.json`: release identity, payload hashes and revisions.
- `content/package-sources.json`: classified source references, dates and scope limits.
- `content/legacy-aliases.json`: compatibility routes.
- `content/source-manifest.json`: original official catalogue/source provenance.
- `content/delivery-targets.json`: recorded platform acceptance scope.
- `composeApp/src/commonMain/kotlin/se/korkort/`: shared UI, quiz engine and generated curriculum code.
- `composeApp/src/commonMain/composeResources/`: bundled artwork, fonts and font licences.

The bank contains 178 situation questions, 616 two-direction sign-recognition questions and 206 calculation scenarios, representing 500 distinct concepts. The engine enforces test allocations independently of these bank totals.

The approved 578-page tagged screen book is [korkortgo-curriculum.pdf](output/pdf/korkortgo-curriculum.pdf). The old research book remains locally as `theory-book-2026-1 (1).pdf` and is Git-ignored. Duplicate exports and the historical migration/design/verification archive have been removed from the working folder after backup.

Run the maintained shared tests with `./gradlew :composeApp:desktopTest`. Their content-parity fixtures live under `composeApp/src/desktopTest/resources/content-parity/`. The reader and navigation generators use the retained content directly:

```sh
python3 tools/build_reader.py --check
python3 tools/build_navigation.py --check
```

Omit `--check` to regenerate their Kotlin outputs; the reader also updates its test parity fixture. Review those diffs and run the JVM tests after content changes. Historical import, scraping, correction and release-approval scripts are archived. These two generators do not publish or approve question-bank revisions. Keep the generated production Kotlin when building the app; changes to the scored bank require separate generation/review work rather than the archived commands.

Road-sign illustrations: Transportstyrelsen. English labels and explanations are editorial translations. Contextual illustrations: KörkortGo, built-in imagegen artwork. Retain bundled Source Sans 3 and Source Serif 4 licence notices and the per-asset source/reuse conditions recorded in the content. Calculations carry educational assumptions; sources and rules require ongoing maintenance. Migration does not establish a fresh source-currency or final platform acceptance review.

## Planned redesign

The proposed dashboard and persistent-progress work is preserved in the [implementation plan](docs/plans/progress-dashboard-plan.md), [revised preview](design/progress-dashboard/preview-v2.png), and [generation prompt](design/progress-dashboard/prompt-v2.md). It awaits explicit design approval. Additional original generated images remain at the protected local paths listed in `MIGRATION.md`.

## Project structure

- `composeApp/src/commonMain`: shared UI, content and quiz engine.
- `composeApp/src/commonTest`: allocation, uniqueness, answer integrity and state-transition tests.
- `composeApp/src/wasmJsMain`: browser entry point and HTML host.
- `composeApp/src/androidMain`: Android activity and manifest.
- `composeApp/src/iosMain`: UIKit controller entry point.
- `iosApp`: SwiftUI host and Xcode project.

The desktop target is a test harness for shared code, not a separately packaged desktop application.
