# 9A3 — Deterministic content compiler

**Status:** Complete. Uses the typed [9A2 contract](../9A2/content-contract.md). All outputs here are an **unscored compiler fixture**, not an imported curriculum or active bank.

[Execution review](review.md) · [Verification](verification.json) · [Source/output trace](trace.json) · [Golden hashes](golden.json)

## Compile the saved exact fixture

From the repository root:

```sh
python3 tools/build_content.py compile \
  --curriculum docs/curriculum/app-migration/implementation-evidence/9A3/fixture/curriculum.json \
  --questions docs/curriculum/app-migration/implementation-evidence/9A3/fixture/questions.json \
  --sources docs/curriculum/app-migration/implementation-evidence/9A3/fixture/sources.json \
  --legacy-aliases docs/curriculum/app-migration/implementation-evidence/9A3/fixture/legacy_aliases.json \
  --manifest docs/curriculum/app-migration/implementation-evidence/9A3/fixture/manifest.json \
  --profile fixture --symbol fixture9A3 \
  --output-dir docs/curriculum/app-migration/implementation-evidence/9A3/generated \
  --trace-output docs/curriculum/app-migration/implementation-evidence/9A3/trace.json
```

Every input/output path is explicit. Validation completes before writing. `GeneratedCurriculum.kt` and numbered parts contain standard-library constructors for the existing common Kotlin types. Constructor/list expressions are split into bounded functions/parts to avoid a single giant generated JVM method. `Curriculum.kt` remains the handwritten model file; future import steps use these generated files rather than overwriting those model declarations.

The trace records each emitted constructor/function, its authoring-file JSON pointer, inherited production origin when available, output filename and verified line number. Output hashes and app-content identity are separate from source PDF identity. No timestamps, temporary output-directory names or absolute host paths enter generated Kotlin/trace identity.

Existing non-generated Kotlin/trace files and source/input overlap are refused. Stale files carrying the exact generator marker can be cleaned within the explicit output directory. Outputs must use staging/build paths, not live app source or content directories. `--profile release` additionally requires full registry/bank closure, accepted questions, empty initial tombstones and correctly bundled curriculum resources; it does not replace 9B17 content parity, human acceptance or step 10/device verification. The partial fixture cannot pass release validation.

The old generation body remains available only through **`python3 tools/build_content.py legacy`**. It still rewrites the historical bank in place and is not a migration command. No-argument execution fails with usage; importing the entrypoint has no side effects. No legacy regeneration was run in 9A3.

## Frozen source authority and provenance

The default source authority is the unchanged [9A1 snapshot](../9A1/input-baseline.json). Retained content/source/asset/audit identities must still match it, even if an authoring manifest has been rehashed against changed bytes. Deliberate authoring payloads, generator/model evolution and administrative plan/progress changes are distinct from protected approved source changes. Later approved source revisions require an explicitly reviewed refreshed authority (`--source-authority <repository-relative-path>` with an `input_manifest` of path/SHA-256 records), itself bound by the manifest; changing a checksum alone does not establish approval.

The manifest binds the source authority, registries, model declarations, generator inputs, exact payload bytes, canonical revisions, question eligibility, scoped URLs and asset files. Its self-digest excludes only `identity.manifest_sha256`, as specified in 9A2. A fixed independent canonical-byte test checks this rule. Source origins use `json:<pointer>`, `line:<start>[-<end>]`, `heading:<exact heading>` or `whole-file`; every referenced file hash and locator is checked.

Schema fields and constructor names are derived from the reviewed Kotlin data classes, enums, inline IDs and five sealed hierarchies. Unknown/missing fields and unsupported variants fail rather than being discarded. IDs are authored explicitly; the compiler does not derive block IDs from text/pages or allocate options from a shuffled display order.

Faint-image acceptance proof records must resolve to JSON with `status: passed`, the exact `asset_sha256` and `platforms` covering `android`, `desktop`, `ios_device`, `ios_simulator` and `wasm_js`. These are required evidence associations, not proof that the device work has happened; 9F must actually record intended-size/light-dark/text-scale/zoom/equivalent-access checks. All present held items remain unaccepted. SIG16–18 alias validation preserves their distinct official URLs, unavailable message and M03-L02 related teaching.

## Fixture scope and exact bindings

The fixture contains M03's six reading nodes with bounded approved excerpts, the exact amber check and separate answer, a structured original sign-family table, RB02/B1 with its verified image/caption, three exact URL records/two canonical scoped sources, and unchanged situation-001 assessment text. Titles, module/lesson order and category tags come from the retained registry/mapping. It does not claim full M03 import or complete curriculum coverage.

Question option IDs `situation-001-option-1` through `-4` are an explicit fixture authoring assignment corresponding to the four original **authored** options. They are not generated from shuffled positions, not applied to the bank and not a blanket acceptance decision. The question remains `unreviewed`; the app-content label is `fixture-9A3-unscored`. The B1 bundle binding points at its retained source bytes for compilation only, without adding an app resource or asserting device legibility.

`build_fixture.py` is a reproducible selection adapter, not a general manuscript parser or a source-approval refresh. Rebuilding it after generator/input changes deliberately changes fixture/manifest hashes; review that change before replacing saved goldens.

## Reproduce checks

```sh
python3 -m unittest discover -s tools -p test_compile_curriculum.py -v
python3 docs/curriculum/app-migration/implementation-evidence/9A3/verify_generator.py
```

To run the generated values with the project's configured Kotlin compiler and all existing tests, temporarily add the saved fixture to the desktop **test** source set:

```sh
mkdir -p /tmp/korkort-9A3-tests
cp docs/curriculum/app-migration/implementation-evidence/9A3/fixture-test-adapter.kt.txt /tmp/korkort-9A3-tests/GeneratedFixtureTest.kt
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest --offline --no-daemon --init-script docs/curriculum/app-migration/implementation-evidence/9A3/jvm-test-init.gradle
```

The init script changes only that invocation's test source set. No Gradle configuration or production source set was changed. Retained JUnit reports document 12 passing tests: six existing quiz tests, five model tests and one generated-value probe. The separate standalone compiler/probe logs provide an additional compile/run check. Android/iOS/wasm/device tests are future 9O/step 10 work.

**Next:** 9B1, separately requested. The real import starts there.
