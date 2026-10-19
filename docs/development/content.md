# Build and reproduce the accepted content

The production root is `App.kt` → `CurriculumApp.kt`, using `acceptedPracticeBank9J` and `acceptedCurriculumSummary9J`. [The accepted manifest](../../content/accepted-content-manifest.json) binds the teaching, questions, package sources, aliases, exact artwork and acceptance inputs. [The provenance inventory](../curriculum/app-migration/provenance-inventory.md) explains credits and origin records.

## Verify without regeneration

Run from the repository root with Python 3 and the JDK/SDK requirements in [README](../../README.md):

```sh
python3 tools/import_curriculum_remaining.py --check
python3 tools/build_navigation.py --check
python3 tools/build_reader.py --check
python3 tools/assemble_question_package_9j.py --check
python3 tools/review_question_delivery_9j.py --check
python3 tools/finalize_question_package_9j.py --check
```

The assembler deliberately reports the historical candidate as 384 accepted / 616 held. That is retained audit data, not the production release status. The finalizer separately validates the accepted package: 1,000 accepted / zero held, using exact revision delivery decisions. Do not interpret successful structural compilation as delivery acceptance.

## Regeneration and changes

For unchanged approved inputs, the commands above compare generated outputs and receipts byte-for-byte. To restore generated outputs, use the same order: the importer uses `--write` instead of `--check`; navigation, reader, assembler, delivery review and finalizer use no `--check` flag. Review the resulting diff and rerun all check commands. The finalizer writes `accepted-assessment-questions.json`, `accepted-content-manifest.json`, `AcceptedQuestionPackage9J*.kt` and its release-validation receipt. It overlays acceptance decisions without rewriting the historical candidate. Navigation and reader generators own their respective generated Kotlin families and parity receipts.

This restoration sequence is for the existing approved inputs. Deliberately changed text, assets, source records, models or questions require renewed origin/parity checks, affected delivery decisions, generated output review and release validation; do not bypass hash failures or copy old acceptance decisions onto new revisions. The importer uses frozen approved production inputs and refuses edited/colliding authoring inputs. A curriculum editorial change therefore needs an updated approved import/source decision before regeneration, rather than editing generated Kotlin.

`tools/build_content.py` and `tools/scrape_sources.py` describe the original bank/catalogue pipeline. They are not the accepted-release regeneration path. A scrape downloads material; it does not approve new wording, reuse conditions or replacement resources. Keep source dates scoped to their recorded checks. The completed 9N briefs authorize no new scored questions or coverage-count changes.

## Resource packaging

Shared files live in `composeApp/src/commonMain/composeResources/`: `files/signs/`, `files/curriculum/`, `font/` and `files/font-licenses/`. Compose resources use package `se.korkort.resources`; reference those resources through generated resource APIs instead of filesystem paths. The 484 curriculum bindings use 419 distinct files; binding count is not a file count. Fonts and their licence texts are additional resources.

Normal builds omit `-PreferenceProof`. That opt-in property selects verification fixtures and an Android application suffix; those binaries must not be published. Android bundles files under APK `assets/composeResources/se.korkort.resources/`. Xcode embeds the shared framework and Compose resources in the iOS app's `compose-resources/`. Wasm distribution copies resources with the generated site; deploy the whole distribution over HTTP(S), preserving paths. Desktop processed resources support the JVM test harness, not a shipped desktop product.

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
