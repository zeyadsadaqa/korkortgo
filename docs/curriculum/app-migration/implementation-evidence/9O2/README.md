# 9O2 — Common integration verification

This run checks the integrated accepted package after 9O1 documentation/provenance and all three 9N briefs. [Candidate identity](candidate.json) records the exact accepted manifest's file SHA-256, declared package identity and starting Git commit. No content, runtime, generation inputs or acceptance decisions are changed.

## Result

**Passed — 19 October 2026:** 150 Python tests; fresh full JVM suite of 85 tests across 22 suites, no failures/errors/skips; all six generation/delivery checks; 932 referenced file hashes and 484 original/bundled artwork bindings. All 18 applicable accepted-package state contracts pass; four future-store cases remain conditional. The forced Gradle build completed successfully in 6m 20s, including the exhaustive 2,464-context artwork/zoom-return test. See [machine results](results.json), [command log](common-commands.json) and [resource/origin parity](resource-origin-parity.json). No content or runtime fix was required.

## Reproduce

From the repository root:

```sh
python3 -m unittest discover -s tools -p 'test_*.py'
python3 tools/import_curriculum_remaining.py --check
python3 tools/build_navigation.py --check
python3 tools/build_reader.py --check
python3 tools/assemble_question_package_9j.py --check
python3 tools/review_question_delivery_9j.py --check
python3 tools/finalize_question_package_9j.py --check
JAVA_HOME=/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home ./gradlew :composeApp:desktopTest --rerun-tasks --offline --no-daemon --max-workers=1 -Pkotlin.compiler.execution.strategy=in-process '-Dorg.gradle.jvmargs=-Xmx6g -Dfile.encoding=UTF-8'
python3 tools/verify_accepted_transient_state_9m.py --reports composeApp/build/test-results/desktopTest --check
```

The check commands reproduce the complete import, navigation, reader, historical candidate and final accepted package without writing over them. Historical assembler output still describes its own 384 accepted / 616 held candidate; final release validation independently checks the production 1,000 accepted / zero held artifact. This distinction is intentional and does not hide a production hold.

`common-commands.json` records Python command arguments, exit codes, elapsed times and individual logs. `shared-build-retry.txt` is the fresh forced JVM build/test run; The initial sandbox-denied cache-lock attempt is summarized in `results.json`; its redundant stack trace was removed. The retry uses the same command with cache access allowed. Test XML is copied into `tests/`, and `results.json` records totals and fingerprints. `state-contract-check.txt` checks the new suite against the accepted identity and retained state contract receipt.

`resource-origin-parity.json` verifies 932 recursively referenced file/hash pairs in the manifest and all non-asset payloads, plus every original/bundled artwork pair for 484 bindings. To reproduce its algorithm, recursively collect objects with string `path` and `sha256` fields from the accepted manifest and each JSON payload listed by it; hash those files, then hash both `original` and `bundled` files for every `content/curriculum.json` asset. Every actual digest must equal the recorded value. This is repository resource and origin parity; Android/iOS/Wasm packaged-byte and runtime checks belong to subsequent 9O platform tasks.

The JVM suite includes allocation, concept uniqueness, feedback/scoring, source and alias routing, reader parity, modal semantics, both production-owner feedback flows, full compiled/JSON accepted-question parity and all 1–70 lengths at twenty seeds in both feedback modes. Four future-store/hot-replacement contracts remain conditional by their existing specification; no durable store or new scope is implied. JVM checks do not substitute for native screen-reader/runtime checks. Existing simulator-only iOS policy remains in force.
