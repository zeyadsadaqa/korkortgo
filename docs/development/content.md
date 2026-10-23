# Build and reproduce the accepted content

The production root is `App.kt` → `CurriculumApp.kt`, using `acceptedPracticeBank9J` and `acceptedCurriculumSummary9J`. [The accepted manifest](../../content/accepted-content-manifest.json) binds the teaching, questions, package sources, aliases, exact artwork and acceptance inputs. [The provenance inventory](../curriculum/app-migration/provenance-inventory.md) explains credits and origin records.

## Verify without regeneration

Run from the repository root with Python 3 and the JDK/SDK requirements in [README](../../README.md):

```sh
python3 tools/stage_step10_corrections.py --check
python3 tools/review_step10_delivery.py --check
python3 tools/finalize_step10_corrections.py --check
python3 tools/build_navigation.py --check
python3 tools/verify_step10_content.py reader
python3 tools/verify_step10_content.py baseline
```

The step-10 correction release retains 1,000 accepted questions and 500 concepts. Six source classifications and the C18/M8 captions are corrected; seven questions have new X9 neutral-description revisions with renewed delivery acceptance. Prompts, answer keys, feedback, IDs, official artwork bytes and source dates are preserved. The [authored amendments](../curriculum/app-migration/verification-evidence/10L1/content-corrections/amendments.json), immutable compressed baseline and [renewed delivery receipt](../curriculum/app-migration/verification-evidence/10L3/content-corrections/renewed-delivery-acceptance.json) bind this bounded change.

These six checks cover the approved baseline/amendments, exact-revision delivery, complete release regeneration and typed validation, navigation/aliases, reader generation/parity and preservation of the historical candidate/assets. JVM parity tests independently compare every compiled accepted question and every reader field with the current JSON receipts. Structural validation and delivery acceptance remain separate checks.

## Regeneration and changes

For unchanged approved inputs, restore the current generated outputs with:

```sh
python3 tools/stage_step10_corrections.py --stage
python3 tools/review_step10_delivery.py --write
python3 tools/finalize_step10_corrections.py --write
```

The review producer requires retained exact-revision rows on all four configured targets and settings. The finalizer rejects missing/stale inputs and validates prospective payloads in an isolated filesystem copy before changing active files. It emits accepted questions/manifest, navigation, reader and the current parity receipts under `verification-evidence/10L3/content-corrections/release/`; it never rewrites the historical 9J/9L receipts. Review the diff and run all six checks afterward. New editorial or runtime changes require affected evidence and renewed acceptance; do not manufacture rows, copy old acceptance onto revised questions or bypass hash failures.

The original `import_curriculum_remaining.py`, `assemble_question_package_9j.py`, `review_question_delivery_9j.py` and `finalize_question_package_9j.py` preserve the pre-correction release. Their full historical checks belong in the original checkout at `fcafdadc80bcda06c71e8c6ebdca4916f3d69930`; they intentionally do not regenerate the corrected live release. Do not run their write modes over this release. The original candidate remains 384 accepted / 616 held as audit data; its retained question JSON, manifest and policy are checked by the baseline command. The new finalizer overlays the seven corrected records on the retained candidate without changing it.

`tools/build_content.py` and `tools/scrape_sources.py` describe the original bank/catalogue pipeline and are not the accepted-release regeneration path. Source checks remain scoped to their recorded editions and dates. The 9N briefs authorize no new scored questions or coverage-count changes.

## Resource packaging

Shared files live in `composeApp/src/commonMain/composeResources/`: `files/signs/`, `files/curriculum/`, `font/` and `files/font-licenses/`. Compose resources use package `se.korkort.resources`; reference those resources through generated resource APIs instead of filesystem paths. The 484 curriculum bindings use 419 distinct files; binding count is not a file count. Fonts and their licence texts are additional resources.

Normal builds omit `-PreferenceProof`. That opt-in property selects verification fixtures and an Android application suffix; those binaries must not be published. Android bundles files under APK `assets/composeResources/se.korkort.resources/`. Xcode embeds the shared framework and Compose resources in the iOS app's `compose-resources/`. Wasm distribution copies resources with the generated site; deploy the whole distribution over HTTP(S), preserving paths. Desktop processed resources support the JVM test harness, not a shipped desktop product.

For web deployments, revalidate HTML and the fixed-name `composeApp.js` when publishing a new distribution; cache hashed Wasm assets by content identity. Verify the visible release on a fresh origin or after cache revalidation. A stale executable can otherwise retain the previous UI even when the host title has changed. This static website has no service-worker/offline-install mechanism: bundled local resources remove external content-service dependencies, but do not guarantee a cold reload when the site host is unavailable.

Build commands and output locations are in README. Exact byte parity can be checked after producing all four development/test bundles:

```sh
python3 tools/verify_resource_delivery_9j.py --ios-bundle /absolute/path/to/Korkort.app --check
```

This verifier expects the debug APK, `composeApp/build/dist/wasmJs/developmentExecutable`, desktop processed resources and the supplied simulator bundle. A production Wasm distribution alone does not populate its development path. `--check` compares the retained resource receipt; omitting it rewrites that historical receipt and is not appropriate for a new evidence run. Byte parity does not establish visual legibility or accessibility. Consult the [closure reproduction record](../curriculum/app-migration/implementation-evidence/closure-9j-9m-9l14/README.md) for the accepted platform evidence and its limits. iOS acceptance is simulator-scoped under the explicit [delivery policy](../../content/delivery-targets.json); device configuration/signing support does not imply physical-device acceptance.

## Checks beyond documentation

```sh
python3 -m unittest discover -s tools -p 'test_*.py'
./gradlew :composeApp:desktopTest
./gradlew :composeApp:assembleDebug
./gradlew :composeApp:linkDebugFrameworkIosSimulatorArm64
./gradlew :composeApp:wasmJsBrowserDistribution
```

Use a configured Android SDK for Android and macOS/Xcode for iOS. These are reproduction instructions, not new 9O2–9O5 run results. Platform rendering, complete flow and step 10 handoff remain separately tracked in the implementation plan.
