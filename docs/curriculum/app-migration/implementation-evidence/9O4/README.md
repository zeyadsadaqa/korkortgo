# 9O4 — Configured desktop JVM verification

**Result — 19 October 2026:** Complete for the configured JVM desktop harness. Fresh build and 35 runtime/parity/state tests across eight suites pass without failures, errors or skips. All 484 artwork bindings match both the desktop JAR and processed runtime classpath; four fonts and two complete licence files match source bytes. No code or accepted content changes were required.

## Candidate and package

[Candidate record](candidate.json) binds the same accepted manifest as 9O2: file SHA-256 `ba91c96975c39b5f6db552c6bead17c0e0474c11dd590f811a7eeb1e1ae54a21`, declared package digest `d9ba2f0261dc9c908146676f903a5ee7fd9c73b50231cd10c2182ecf5d87f82a`. [Package resources](package-resources.json) records the newly built `composeApp/build/libs/composeApp-desktop.jar` hash and each exact resource entry. There are 484 logical bindings and 419 distinct artwork files; fonts/licences are additional resources.

The project configures `jvm("desktop")` as a shared-code test harness. It has no desktop `main`, executable JAR manifest or desktop app distribution task. Consequently this step verifies the configured JVM library/resource package and real Compose/Skia raster runtime scenes. It does not invent a desktop shipping product or claim a native desktop window was launched.

## Fresh runtime checks

[Build log](desktop-build-tests.txt), [test summary](test-summary.json), `tests/` XML and nine representative `screenshots/` preserve this fresh forced run. Both the library-wide and deferred-review captures were visually inspected. The eight suites cover:

| Suite | Scope |
| --- | --- |
| CurriculumAppFlowTest | Actual production owner with one deterministic already-accepted question fixture: library query/reader return, immediate and deferred feedback, unfinished-test guard, score, filtered/expanded review, related teaching, exact source URI dispatch, focus return, another-test preference and discard recovery. This UI fixture does not substitute a 1,000-question runtime bank or claim random whole-bank UI traversal. |
| AcceptedQuestionParityTest | Full compiled accepted question objects versus accepted JSON, including source/feedback/acceptance metadata. |
| AcceptedReleaseStateTest | Actual accepted bank and package identity, every 1–70 length at twenty seeds in both feedback modes; exact snapshots/scoring, guard/review/source/preferences/reset behavior. |
| LearningReaderParityTest | Complete compiled authored reader structure, navigation origins and exact resource identities versus canonical payloads. |
| NavigationTest | Canonical and legacy routes, source resolution, deliberate chooser/unavailable outcomes and recovery without guessed destinations. |
| LearningViewsSemanticsTest | Library search/filter/expansion retention, reader/answer reveal, large text, review explanations, tables, source-open failure/return focus, unavailable recovery and missing-result setup. |
| ReferenceViewerSemanticsTest | Exact sign caption and image loading, keyboard zoom/pan/reset/Escape, neutral descriptions and pending choice/focus restoration at light/dark and large text. |
| ExactVectorRenderingTest | Exact official vector rendering regressions in the desktop raster runtime. |

## Offline and accessibility boundaries

Teaching, reference details, images and fonts are read from local packaged resources. The build runs Gradle offline. External source navigation is intercepted by a local URI handler in the production-owner fixture, and failure/return behavior is explicitly tested separately; no remote webpage is needed or asserted to load offline. Host network interfaces were not disabled, so this is local-resource/runtime proof, not a network-isolated operating-system test.

Fresh Compose semantics assertions and real keyboard events verify the listed reveal/focus/modal behaviors. There is no configured desktop app window/native accessibility bridge to audit with macOS VoiceOver. No native desktop screen-reader listening, OS browser launch, installer, every-asset visual inspection or release publication is claimed. There are no unresolved required checks within the configured harness scope. A future desktop product would need its own launcher, packaging and native accessibility/runtime acceptance. Android/iOS/web and step 10 gates remain separate.

## Reproduce

```sh
JAVA_HOME=/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home ./gradlew :composeApp:desktopJar :composeApp:desktopTest \
  --tests se.korkort.CurriculumAppFlowTest \
  --tests se.korkort.LearningViewsSemanticsTest \
  --tests se.korkort.ReferenceViewerSemanticsTest \
  --tests se.korkort.LearningReaderParityTest \
  --tests se.korkort.NavigationTest \
  --tests se.korkort.AcceptedQuestionParityTest \
  --tests se.korkort.AcceptedReleaseStateTest \
  --tests se.korkort.ExactVectorRenderingTest \
  --rerun-tasks --offline --no-daemon --max-workers=1 \
  -Pkotlin.compiler.execution.strategy=in-process \
  '-Dorg.gradle.jvmargs=-Xmx6g -Dfile.encoding=UTF-8'
```

The build executed all fifteen tasks and completed in 1m 20s. Resource checks hash each `curriculum.json` asset's `bundled` path inside `composeResources/se.korkort.resources/` in both the JAR and `composeApp/build/processedResources/desktop/main`, comparing to the accepted payload hash. Font/licence entries are byte-compared to shared source resources. `results.json` fingerprints retained evidence; no duplicate JAR binary or generated class cache is checked in. The exhaustive 85-test common suite remains separately recorded under [9O2](../9O2/README.md); this step is the focused desktop rerun, not another claim of that full suite.

## Retention cleanup

Removed the repetitive immediate-feedback expanded-review PNG; the deferred-review image and both passing feedback-mode test cases remain. All eight suite XML files, build log, candidate/package hashes and distinct library/reader/source/reference/recovery captures are retained. [Cleanup record](cleanup.json).
