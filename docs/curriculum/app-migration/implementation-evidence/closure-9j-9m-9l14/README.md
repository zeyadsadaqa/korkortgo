# 9J / 9M3 / 9L14 closure — 19 October 2026

**Status: complete.** Final package release validation, accepted transient contracts and production integration checks pass.

This directory records the accepted package and production integration, separately from the dated candidate checkpoints. The user authorized iOS simulator testing instead of a physical iPhone. No physical-device iOS pass is claimed.

## Accepted package

`release-validation.json` validates `content/accepted-content-manifest.json`: **1,000 accepted questions, zero held questions, 500 concepts**. Production uses `acceptedPracticeBank9J`; it cannot fall back to the historical 384-question accepted subset. `content/assessment-questions.json` and its candidate manifest retain the historical 616 holds and original decision trail. The accepted overlay activates the 38 previously approved replacements and clears exact-revision delivery holds using `delivery-acceptance.json`; authored question semantics are unchanged by this closure.

Delivery acceptance combines:

- Exhaustive shared execution of all **616 held revisions × four settings = 2,464 question runs**, with **6,160 exact-image enlargement/return checks**.
- Actual full-question native execution of all **38 replacements × four settings = 152 contexts and 380 enlargement/returns on each of Android and iOS simulator**. This includes all 24 questions affected by the twelve faint assets. The other revisions use exhaustive shared proof plus representative native renderer/route/accessibility evidence, not a separate native recording of every revision.
- Exact byte parity for **484 resources on four configured targets**, recorded in `resource-inventory.json`. Packaging parity is not a claim that every resource was individually visually inspected on every native target.
- Explicit visual decisions for the twelve faint assets in `asset-legibility-review.json`, with native captures and contact sheets. Their original thin/pale geometry is preserved within the approved larger artwork frame. Enlargement and neutral physical descriptions remain available. No artwork recoloring, thickening or contrast certification is claimed.

Four iOS machine summaries record passing normal/large light/dark runs. Large-text runs use a compact verification-only header after the original debug header consumed excessive space; production does not contain that header. Android X8 captures were refreshed after adding an idle/frame settle before screenshots; superseded loading/failure captures are omitted from the retained package. Fractional layout/antialiasing can differ between settings, so identical screenshot hashes are not an acceptance condition.

## Native raster correction

The native matrix exposed an Android canvas limit on the original M17a raster (6,497 × 11,162 pixels). `ExactRaster.kt` now decodes oversized rasters into bounded tiles, chooses resolution from the explicit viewer scale, and clips outside the viewport. The source bytes and intrinsic coordinates are unchanged. Eight native M17a contexts and twenty enlargement/returns pass; browser fit/enlargement captures are also retained. Ordinary raster decoding is unchanged. The production Android review crash found during integration is fixed with Bundle-compatible ID/revision list keys while assessment identities remain typed; final passing production evidence is retained.

## Accepted transient state

`accepted-state-contract-results.json` binds all **18 applicable passing contracts** to the exact accepted manifest, with **four future-store cases conditional** as specified by the plan. Actual accepted questions are checked at every length 1–70, twenty seeds per length, and both feedback modes, including exact snapshots, scoring, guards, review, sources, preferences and process reset. The final accepted-manifest report and passing shared test XML are retained; superseded preintegration reports are removed. The small production-owner fixture XML used by the delivery acceptance input remains bound and available.

The final integration also moves the review heading and filters into the existing scroller, preserving answer space at 160% text. Browser production guards and image viewers share the root scene because the bundled Compose 1.9.3 accessibility listener tracks only its last scene owner and loses the root after a separate dialog closes. Native dialogs keep their existing implementation. Browser background exclusion uses `aria-hidden` inside the Compose viewport shadow root, retaining its cached semantics nodes; Tab/Escape and close return are checked in the normal browser build.

No durable history, bookmarks, completion store, hot package replacement, public deep-link API or new source-currency certification was added.

## Production integration

`App()` launches the accepted canonical owner. Home counts come from the validated package summary; library, canonical reader, references, guarded practice, results and contextual answer review share the actual root. Search/filter context survives reader visits; returning through the header really opens the library. Review source actions are consumed once, and related teaching/source returns preserve the review context and source trigger.

`legacy-cleanup.json` records removal of **39 summaries, 178 unused Topic rows and 343 unused legacy catalogue rows**, with all **1,000 original question declarations byte-preserved**. Compatibility aliases, official publishers, dates, exact artwork credits, editorial-English notices, complete teaching and the learning-aid disclaimer remain available. README provenance/build guidance now distinguishes accepted artifacts from historical compiler inputs.

## Verification and reproduction

- `tests-final-shared/`: 85 passing shared cases retained from the full suite; the five affected accepted-state/parity/production-owner cases are replaced by their passing final rerun XML. This preserves the phase distinction rather than claiming a second full-suite run after every UI fix.
- `native-test-logs/final-python.txt`: 150 Python tests passing.
- `native-test-logs/final-shared-build.txt`: full shared suite and Android/iOS simulator/WebAssembly compilation.
- Previous representative native reader and route checks plus Android TalkBack evidence remain in `../native-reader-routes/`; iOS simulator description/trait audits do not claim VoiceOver listening.

```sh
python3 -m unittest discover -s tools -p 'test_*.py'
python3 tools/assemble_question_package_9j.py --check
python3 tools/review_question_delivery_9j.py --check
python3 tools/finalize_question_package_9j.py --check
./gradlew :composeApp:desktopTest :composeApp:compileDebugKotlinAndroid \
  :composeApp:compileKotlinIosSimulatorArm64 :composeApp:compileKotlinWasmJs --offline \
  --max-workers=1 -Pkotlin.compiler.execution.strategy=in-process \
  '-Dorg.gradle.jvmargs=-Xmx6g -Dfile.encoding=UTF-8'
python3 tools/verify_accepted_transient_state_9m.py
```

Final native results: three selected tests pass on Android and three on iOS simulator, including both production feedback modes plus reference/pending-choice modal return. `final-ios-test-summary.json`, `android-production/`, `ios-production/` and `native-test-logs/` retain their evidence. A subsequent metadata-only Xcode build confirms the display-name override is KörkortGo; it does not recertify the preceding UI run. Normal build outputs are restored without the opt-in proof launcher after native testing. `browser-production-flow.json` records the final normal browser flow, including guard/viewer background exclusion and keyboard dismissal, scoring, teaching/source return and retained count. A concurrent compiler attempt exhausted its daemon heap; the recorded sequential 6 GiB in-process retry passes.

Native proof builds use `-PreferenceProof`; Android instrumentation selects `NativeReaderRouteTest#productionPracticeAndReviewUseAcceptedPackage`. The iOS `NativeRouteTests` scheme selects `testAcceptedProductionPracticeAndReview`; copy `accepted-root-fixtures.json` into the test bundle. This fixture contains expected identities/labels from the real accepted bank and does not replace the running bank. Normal builds contain no proof launcher.

Text log/tree exports normalize trailing whitespace for version control; the recorded JSON/XML/image inputs and original xcresult bundles retain their separate identity.

9N assessment briefs remain next. Independent 9O integrated acceptance and step 10 release work retain their planned scope; this evidence does not claim those later stages or publication are complete.

## Evidence retention

Retain the machine acceptance matrices, their passing native logs/summaries, all inline faint-question screenshots/trees, eight legibility contact sheets, raster regression, final production/zoom return evidence and hash-bound release inputs. Repetitive per-option zoom/return captures, failed-run diagnostics, copied source snapshots and superseded intermediate reports are removed. The complete zoom assertions remain in the native test sources and machine matrices; the reduced package does not claim to retain every zoom screenshot. `cleanup.json` records the scope and size reduction.
