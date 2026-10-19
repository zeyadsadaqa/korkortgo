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

## Content and provenance

See [accepted-content build and regeneration guidance](docs/development/content.md) and the [provenance and credit inventory](docs/curriculum/app-migration/provenance-inventory.md).

- `content/concepts.tsv`: 178 authored situation questions and misconception-specific explanations.
- `content/accepted-assessment-questions.json`: the accepted, reviewable 1,000-question production bank.
- `content/accepted-content-manifest.json`: validated release identity, payload hashes and counts.
- `content/assessment-questions.json`: retained historical candidate and hold evidence.
- `content/curriculum.json`: canonical teaching, references, exact artwork and source evidence.
- `content/package-sources.json`: the accepted manifest’s classified source references, dates and scope limits.
- `content/delivery-targets.json`: explicit platform acceptance policy, including simulator-scoped iOS evidence.
- `content/signs.json`: official sign URLs, image URLs, retrieval dates and SHA-256 hashes.
- `content/source-manifest.json`: the official catalogue and rules pages visited.
- `content/quality-report.json`: counts and content composition.
- `composeApp/src/commonMain/kotlin/se/korkort/CurriculumApp.kt`: integrated canonical learning and practice routes.
- `tools/finalize_question_package_9j.py`: accepted package assembly and release validation.
- `tools/build_content.py`: historical question compiler, including explicit calculation models.
- `tools/scrape_sources.py`: bounded downloader for the public Transportstyrelsen section.

The bank contains **178 situation questions, 616 two-direction sign-recognition questions and 206 calculation scenarios**, representing **500 distinct learning concepts**. It does not present reworded copies as independent learning concepts. The distribution of the stored bank is not the distribution of a test; the engine enforces the requested test allocation.

The original research and migration provenance remains in `docs/curriculum/`; learner routes use the original KörkortGo curriculum and classified supporting sources. Official sign artwork retains its exact source bytes and attribution. Approved editorial illustrations are separately identified. Source dates and scope limits are retained; this integration does not claim a new universal source check.

Calculations are labelled with assumptions. Approximate braking models are educational estimates, not guaranteed stopping distances. Rules and source links should be maintained as the source material changes.

To verify the current candidate and accepted package without changing acceptance decisions:

```sh
python3 tools/assemble_question_package_9j.py --check
python3 tools/finalize_question_package_9j.py --check
./gradlew :composeApp:desktopTest
```

Do not run the historical `build_content.py` over the accepted release. Content changes require renewed parity, delivery and release validation.

Official asset refreshes require a separate source/reuse review and renewed hash, delivery and release checks. The historical scraper is documented in the build guide; running it alone does not update the accepted release.

Road-sign illustrations: Transportstyrelsen. English labels and explanations are editorial translations. Contextual illustrations: KörkortGo, built-in imagegen artwork. Source Sans 3 and Source Serif 4 ship with their SIL Open Font License texts; retain them with redistributed font resources. Exact per-asset credits, reuse conditions, approval records and licence locations are listed in the provenance inventory.

## Design

Original ImageGen boards are in `design/mockups/`, with prompts in `prompts.md`; the curriculum migration’s approved screen references and bindings are in `docs/curriculum/app-design/`. They cover overview, library, reader, setup, question, feedback, results and review, including mobile adaptations. They are design references; the app uses actual UI components and official sign assets, not mockup images as screens.

## Project structure

- `composeApp/src/commonMain`: shared UI, content and quiz engine.
- `composeApp/src/commonTest`: allocation, uniqueness, answer integrity and state-transition tests.
- `composeApp/src/wasmJsMain`: browser entry point and HTML host.
- `composeApp/src/androidMain`: Android activity and manifest.
- `composeApp/src/iosMain`: UIKit controller entry point.
- `iosApp`: SwiftUI host and Xcode project.

The desktop target is a test harness for shared code, not a separately packaged desktop application.
