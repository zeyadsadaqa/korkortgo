# 9L — approved learning views and interactions

17 October 2026. Implemented the independently executable 9L1–9L13 view components against the already approved 8B–8M/8O package. **9L14 is blocked**, not accepted or activated: 9J remains a candidate with 616 delivery-held questions and 9M1–9M3 are separate prerequisites. Component implementation is not finished-app, platform screen-reader or release acceptance.

The saved screenshots exercise component bodies; they do not replace or prove the approved integrated app shell. Full shell/learner-label integration remains 9L14.

The production `App.kt`, legacy summaries/topics and scored bank remain unchanged. `LearningRoute` is an isolated learning/reference host, reachable only from an explicitly built verification binary with mode `learning`. No test starts, scoring acceptance, stored history, completion state, public URI scheme, new artwork or visual redesign was introduced. The fixture switch does not make a production learner route. Previous 9F/9K evidence remains historical; its receipts were not regenerated as fresh approvals.

## Sequential outputs

| Step | Implemented output | Verification and remaining scope |
|---|---|---|
| 9L1 | `LearningLibrary`: all ten canonically numbered modules, forty lessons, ten reviews, introductory/appendix entries, Sources and reference actions. Module 3 starts expanded; every other module can expand. | Complete counts/order and zero-primary-question discoverability; phone/wide renders. No progress or active-question count. |
| 9L2 | Search across canonical titles/objectives/body, intersected with exact five category tags; separate clear actions and exact empty state. | Model and actual Compose filter/clear-action checks; canonical numbering survives filtering. |
| 9L3 | `LessonReader`: complete compiled documents, module/title/goal context, all 60 previous/next reading nodes, inline canonical/source links and validated source return. | Complete-object parity against all authored document fields; neighbour and opening checks. No integer-page lookup. Production legacy adapter removal remains 9L14. |
| 9L4 | Deliberate Show answer/Hide answer; expanded/collapsed semantics and answer region; focus returns to toggle before collapse. | Actual semantics confirm hidden answer is absent, revealed answer is present and collapse removes it again. No scoring. |
| 9L5 | Exhaustive typed block renderer: prose, emphasis, links, lists, tables, scenarios, callouts, equations, related links, shared sign examples and exact contextual crop/polygon/composite metadata. | Same 390-pixel viewport at actual 1.0/1.5 font scale; calculation and table samples. Tables reflow as labelled cells; no teaching ellipsis. Full per-illustration/platform visual acceptance remains open. |
| 9L6 | `LearningAnswerReview`: pinned shuffled IDs, selected/correct labels, main/per-option explanations and exact source/related teaching actions only after permitted reveal. | Exact situation-001 A-selected/B-correct fixture and both feedback modes. Callbacks remain owned by guarded production integration in 9L14/9M; isolated host contains no active quiz. |
| 9L7 | Exact fuel-saving-150-0.5 revision through the same review renderer. | A = 0.375 litres, B = 0.75 litres; full unrounded explanation and supplied-assumption limitation. Fixture does not create score/history or change eligibility. |
| 9L8 | Exact source directory/detail, publisher/classification and distinct retained date fields; source scopes/limits, external-failure recovery and retained directory scroll. | Scoped source checks and source/reader return regression; no inferred source currency or all-official badge. |
| 9L9 | Reuses exact `SignReferenceDetail`/`SignReferenceRoute`, adds group navigation in isolated learning host. | Existing B1 exact asset/caption/notice and viewer tests rerun. Earlier 9L9/9F holds remain. |
| 9L10 | Reuses accessible viewer in reference, reader sign examples and assessment-review images; unique labelled enlarge controls and trigger focus return. | Existing keyboard/pan/reset/neutral-description tests rerun. Full supported-platform reader/delivery acceptance remains open. |
| 9L11 | Deliberate chooser and known-parent moved-passage notice. | Exact four page-46 choices, question precedence, chooser activation and moved-parent render. No PDF equivalence. |
| 9L12 | Exact unavailable messages/official references/related lesson and generic library recovery. | SIG16–18 distinct registered URLs; failed external action keeps internal recovery. No substituted sign. |
| 9L13 | `MissingResults`: exact no-result message and deliberate setup action. | Actual Compose callback check: no automatic setup/test/result. Full preference/reset integration remains 9M2/9L14. |
| 9L14 | **Blocked; not executed.** | Requires accepted 9J package and 9M1–9M3; legacy label/summary/topic removal must happen with integrated activation, not before. |

## Exact data, fonts and rendering

`tools/build_reader.py` uses the existing typed compiler to generate the complete approved teaching payload separately from navigation and assessment data. It does not re-author content. `reader-parity.tsv` binds modules, every document field (including nested/hidden content), all 60 reading IDs, lesson tags and all asset metadata. The independent JVM reflection test reconstructs canonical authored JSON from the actual compiled objects; concrete related-link lists omit a redundant union discriminator to match the authored schema.

Source controls are individually keyed lazy-list items. A validated return requests the exact item, waits until that row is actually visible, then restores its trigger focus once. Later user scrolling does not repeatedly steal focus. Headless tests wait for asynchronous font layout before initiating the source visit. Inline source links retain reading position; complete platform assistive/link-focus acceptance is still open.

Layout uses the existing 24 dp outer inset, 8/12/16 dp internal spacing, a maximum 800 dp reading measure and 900 dp library measure, natural text wrapping and standard Material grouping. These are implementation values within the approved direction, not measurements inferred from the raster boards.

The production Source Sans 3 regular/semibold and Source Serif 4 semibold/bold bytes and both OFL licences are bundled unchanged. [Font identities](fonts.json) retain upstream release tags, URLs and SHA-256. Only the new learning components use this typography; actual font scaling preserves one body family. The approved Paper/Forest theme is used with an opaque background. The first test-host capture lacked that background; it was corrected and is not acceptance evidence.

Wide-reader bounds are checked against the 800 dp measure; an inner centring box prevents the host surface from forcing a full-window minimum width. A painted regression checks blank following-content pixels so an original contextual source sheet cannot escape its approved crop window.

Official art is never cropped/recoloured/redrawn. Contextual illustrations use their explicitly approved windows/polygons/composite overlays, with source coordinates and insets retained. Loading verifies the bundled SHA-256. Caption, textual equivalent, overlay labels and credit remain available at user text scale. This implementation does not clear any faint-outline delivery hold or assert visual review of every illustration.

## Reproduction

```sh
python3 tools/build_reader.py --check
python3 tools/build_navigation.py --check
python3 tools/assemble_question_package_9j.py --check
python3 -m unittest discover -s tools -p 'test_*.py'
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest :composeApp:compileKotlinIosSimulatorArm64 :composeApp:compileKotlinWasmJs :composeApp:compileDebugKotlinAndroid --offline --no-daemon
```

Verification builds retain the existing `-PreferenceProof` release/publish exclusion. Android uses verification activity extra `mode=learning`; iOS simulator uses `PROOF_MODE=learning`; verification Wasm uses `#S1/learning`. This route contains study/reference content only. It does not activate a quiz or clear the release gate. Native/mobile screen-reader and full interaction evidence remain separate from compilation and headless desktop semantics.

## Final validation

**137 Python tests and 68 desktop tests pass**, including eleven new actual Compose UI checks, four canonical view-model checks and complete compiled teaching parity. Android debug, iOS simulator and WebAssembly compilation pass with the verification host. [Verification receipt](verification.json) · [Step results and open acceptance](step-results.json) · [25 component captures](capture-index.json) · [Saved test results](tests/).

The final fixes include explicit contextual crop clipping, the actual wide reading limit, stable placeholder dimensions from verified PNG headers, and a source-return check that verifies the focused control remains inside the viewport after artwork decoding. All source titles/dates, question revisions, original artwork, delivery holds and 9J activation gates are preserved.
