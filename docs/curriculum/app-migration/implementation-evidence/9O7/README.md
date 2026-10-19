# 9O7 — WebAssembly production and browser checks

**Result — 20 October 2026:** Complete for the available in-app browser. The normal production distribution builds successfully; all 484 artwork bindings, four fonts and both licences match. A real accepted-bank deferred-feedback session and representative library/reader/source/reference/recovery flows pass. No production code or accepted content changed. This does not certify every browser engine or offline cold reload.

## Candidate and package

[Candidate](candidate.json) binds the unchanged 9O2 accepted manifest. `web-build.txt` records `wasmJsBrowserDistribution` without proof fixtures (1m 38s, successful). [Package resources](package-resources.json) fingerprints production JS/Wasm/host files and all artwork/font/licence resources. [HTTP samples](http-parity.json) verify five actual localhost responses against those built bytes.

A loopback server was initially opened on port 8772 before the build finished. That browser origin retained the prior executable after reload, despite the updated host title. The completed distribution was therefore checked on fresh origin **http://127.0.0.1:8773/**; its visible KörkortGo/10-module/40-lesson home established the correct integrated root. The stale page is excluded from acceptance evidence. [Cleanup](runtime-cleanup.json) records both task servers stopped and the temporary browser tab closed. No user browser tabs were changed.

For deployment, serve HTML and the fixed-name `composeApp.js` with cache revalidation; hashed Wasm assets may be cached by content identity. Deploy the complete distribution together. Do not interpret a cached old page as verification of a new deployment.

## Browser observations

[Checkpoint index](browser-checkpoints.json) lists each actual accessibility snapshot and its retained screenshot where available. [Machine results](results.json) assert the following observable checkpoints:

- Correct accepted home counts; library search for “Your route into driving”; exact lesson, keyboard paging and deliberate answer reveal. The answer is absent before Show answer and present afterward.
- Bundled classified source detail and return to the same lesson position; library query survives the visit. This run does not invoke the external Open source button or certify remote website availability.
- Official reference catalogue/group, exact Give way image, 150% zoom and Escape return. Modal accessibility tree contains modal content, not the background app.
- Actual accepted-bank one-question deferred session: neutral illustrated stem, wrong “Give way” choice, unfinished-test guard, keyboard dismissal, neutral assessment zoom/reset/return, confirmation without early feedback, and score **0/1**.
- Incorrect-filter expanded review includes the four options, explanations and correct answer. Exact “Read the rural road” teaching and “Varning för farthinder” source visits return to the expanded review. Another-test setup retains count **1**.
- An Environment filter intersecting the saved query produces “No matching lessons.” Clear filters restores the matching lesson while retaining the query. Fresh page load resets count to **70**.

Browser input automation needed the actual native input bridge: virtual textbox focus/fill and some rapid DOM waits produced intermediate or stale observations. Final evidence uses stable native accessibility snapshots and native keyboard events. A few short locator waits timed out while subsequent native snapshots showed the completed expected state; these are not counted as app failures or used alone as passing evidence. No app fix was made to accommodate automation.

The current run covers one deferred session and representative images, not all 1,000 browser questions or a fresh full light/dark/text-scale matrix. Immediate-mode/common contracts and broader previous delivery evidence remain separately recorded under [9O2](../9O2/README.md) and [accepted closure](../closure-9j-9m-9l14/README.md). Browser native accessibility-tree/modal and keyboard observations are not a screen-reader listening audit. No cross-engine or mobile-browser claim is made.

## Static/offline delivery boundary

All teaching, source metadata, question data, images and fonts are in the built distribution; no account, question-generation backend or external asset service is needed. The browser run uses local HTTP, not OS network isolation. This app has no service worker/offline-install mechanism: cold reload with the site host unavailable is not guaranteed and is not claimed. Static hosting remains necessary to load the website. These are the existing web delivery characteristics, not a newly added offline feature.

## Reproduce

```sh
JAVA_HOME=/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home ./gradlew :composeApp:wasmJsBrowserDistribution --offline --no-daemon --max-workers=1 -Pkotlin.compiler.execution.strategy=in-process '-Dorg.gradle.jvmargs=-Xmx6g -Dfile.encoding=UTF-8'
python3 -m http.server 8773 --bind 127.0.0.1 --directory composeApp/build/dist/wasmJs/productionExecutable
python3 tools/finalize_question_package_9j.py --check
```

Use a fresh origin or ensure executable cache revalidation before following the checkpoints above. Compare each asset's `bundled.sha256` in `content/curriculum.json` to `composeResources/se.korkort.resources/` in the production directory; compare font/licence bytes to shared resources. Preserve the manifest identity across build and runtime. Stop the temporary server afterward. No publishing or step 10 execution is included.

## Retention cleanup

Removed seven repetitive setup/return/recovery PNGs while keeping all 26 accessibility snapshots, the final result and expanded review screenshots, modal/neutral-image proof and distinct reader/source/recovery captures. The checkpoint index marks removed screenshots as null. [Cleanup record](cleanup.json).
