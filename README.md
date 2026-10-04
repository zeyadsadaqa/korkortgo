# Körkort

An English-language Swedish category B theory app built with Kotlin Multiplatform and Compose Multiplatform. One shared UI, question bank and test engine run on Android, iOS and the web.

## Features

- **1,000 questions**, four options each, with a correct answer and an explanation for every option.
- Five knowledge areas using the requested category names.
- Any test length from **1 to 70**.
- Immediate feedback or answers revealed only after completing the test.
- Results by category, filtered answer review, related chapters and another-test flow.
- 37 original study chapters covering the supplied book's chapter structure.
- 343 official Transportstyrelsen sign, marking and signal illustrations, available offline in the native apps and bundled with the website.
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

- `content/concepts.tsv`: 178 authored situation questions and misconception-specific explanations.
- `content/questions.json`: the complete reviewable 1,000-question bank.
- `content/signs.json`: official sign URLs, image URLs, retrieval dates and SHA-256 hashes.
- `content/source-manifest.json`: the official catalogue and rules pages visited.
- `content/quality-report.json`: counts and content composition.
- `composeApp/src/commonMain/kotlin/se/korkort/Chapters.kt`: original study summaries.
- `tools/build_content.py`: deterministic content compiler, including explicit calculation models.
- `tools/scrape_sources.py`: bounded downloader for the public Transportstyrelsen section.

The bank contains **178 situation questions, 616 two-direction sign-recognition questions and 206 calculation scenarios**, representing **500 distinct learning concepts**. It does not present reworded copies as independent learning concepts. The distribution of the stored bank is not the distribution of a test; the engine enforces the requested test allocation.

The supplied *Theory Book 2026*, edition 2026-1 (Körkortonline.se / Hagberg Media AB), is a research source with page references. **No book images, page scans or PDF are bundled in the app.** Every road-sign image in the application was downloaded from Transportstyrelsen. The user's source PDF remains in the workspace only. Still-image signal previews link to their official descriptions; signals requiring motion are excluded from static-image practice questions.

Calculations are labelled with assumptions. Approximate braking models are educational estimates, not guaranteed stopping distances. Rules and source links should be maintained as the source material changes.

To regenerate Kotlin data after editing the TSV or sign index:

```sh
python3 tools/build_content.py
./gradlew :composeApp:desktopTest
```

To refresh official assets, install `beautifulsoup4`, then run `python3 tools/scrape_sources.py`. The downloader only follows the requested public website section and stores a source manifest; review updated wording before regenerating the bank.

## Design

The approved ImageGen boards are in `design/mockups/`, with the full prompts in `prompts.md`. They cover overview, library, reader, setup, question, feedback, results and review, including mobile adaptations. They are design references; the app uses actual UI components and official sign assets, not mockup images as screens.

## Project structure

- `composeApp/src/commonMain`: shared UI, content and quiz engine.
- `composeApp/src/commonTest`: allocation, uniqueness, answer integrity and state-transition tests.
- `composeApp/src/wasmJsMain`: browser entry point and HTML host.
- `composeApp/src/androidMain`: Android activity and manifest.
- `composeApp/src/iosMain`: UIKit controller entry point.
- `iosApp`: SwiftUI host and Xcode project.

The desktop target is a test harness for shared code, not a separately packaged desktop application.
