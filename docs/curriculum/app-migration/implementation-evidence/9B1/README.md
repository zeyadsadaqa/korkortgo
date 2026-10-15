# 9B1 — Approved opening and reading structure

**Status:** Complete. [Execution review](review.md) · [Verification](verification.json) · [Source/output trace](trace.json)

The cumulative authoring payload is [content/curriculum.json](../../../../../content/curriculum.json). It now contains the approved cover text, introduction with the exact learning-aid disclaimer, study guide, contents and the canonical 60-node module/lesson/review skeleton. Ten modules, forty lessons, ten reviews and all forty category-tag records preserve their reviewed IDs, titles and order.

The four published opening IDs are `cover`, `introduction`, `study-guide` and `contents`. They use `front_matter` document kind and are excluded from `reading_order` and module cards. Their 22 top-level blocks preserve all opening text and strong emphasis. The contents links resolve to the ten canonical modules. Appendix letters/titles and the Sources and references label are retained as text; their destination actions remain pending until those destinations are imported. PDF running headers, printed folios and PDF viewer controls are technical/renderer material, not app teaching blocks.

The 60 reading documents contain exact metadata and production origins, with empty body/answer arrays. Their goals, complete teaching, scenarios, checks, answers, source/asset bindings and module-review tasks are imported in 9B2–9B11. No placeholder teaching or learner completion was invented.

[content/curriculum-import-state.json](../../../../../content/curriculum-import-state.json) is a **build-time import ledger**, not learner state or a persistence feature. It records each pending body's owner, required source IDs/asset register, front-matter/library policy and deferred work. `production_ready` remains false. Cover artwork/crop bindings remain 9C4 work; source/reference/appendix actions, assets and supporting-anchor completion remain in their assigned tasks. Importing cover text does not select a new app cover design.

The partial, assessment-free staging package is generated under [generated/GeneratedCurriculum.kt](generated/GeneratedCurriculum.kt) and numbered parts, with `stagedCurriculum9B1` as its root value. The local empty question/source/alias files satisfy the compiler's four explicit input roots without editing or replacing the live question bank. The manifest's identity is labelled `staging-9B1-opening-and-structure`, and the compiler's non-release `fixture` profile is used for incremental import staging. Full release validation deliberately rejects this incomplete package. No generated source is connected to a production app source set yet.

## Reproduce the bounded import

From the repository root:

```sh
python3 tools/import_curriculum_opening.py --check
```

This read-only command rebuilds the 9B1 selection in memory and compares the two saved authoring files. It is an exact check of **this step's snapshot**; after a later module import, use that step's cumulative checks rather than expecting the original empty-body snapshot to remain identical.

```sh
python3 tools/import_curriculum_opening.py --write
```

This initializes identical 9B1 data and regenerates its staging manifest, empty local support files, Kotlin parts and trace. It refuses to overwrite authoring files with different/accumulated later imports. No old content-generation command is run. All opening block IDs are explicit authored assignments; they do not depend on wording or pagination. Future steps replace their own pending body records while retaining these opening IDs and metadata.

## Verify against the approved PDF and current Kotlin compiler

The four opening pages were freshly extracted from the exact approved 578-page screen release; [pdf-opening-text.json](pdf-opening-text.json) records the source hash and text. The PDF was not edited. The four pages were also rendered and inspected as an intermediate contact sheet.

Run the independent verification using the bundled Python with pypdf:

```sh
/Users/zeyad/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 docs/curriculum/app-migration/implementation-evidence/9B1/verify_opening.py
```

It freshly extracts the approved PDF again and compares all imported opening text, not only the disclaimer. The comparison removes known PDF headers/footers and contents-only numerical labels/folios; it retains wording, punctuation, appendix letters, order and source dates. It independently checks all sixty titles/orders/production origins, the module/category structure, pending-body ledger, unchanged approved inputs and prior compiler evidence. Fresh repeated generation must equal the staged Kotlin/trace byte for byte. Only this step's verification.json is written.

```sh
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest --offline --no-daemon --init-script docs/curriculum/app-migration/implementation-evidence/9B1/jvm-test-init.gradle
```

The init script adds only this step's staged Kotlin and import tests to that invocation's desktop test source set. It does not change production configuration. All 14 tests pass: six existing quiz tests, five content-contract tests and three imported-value tests. [Build transcript](gradle-tests.txt) and the three saved JUnit XML files retain the evidence.

**Next:** 9B2 — import M01, only when separately requested.
