# Curriculum migration brief

Recorded on 29 October 2026, before project cleanup.

## What migrated

KörkortGo now uses the original English-language curriculum prepared from the theory-book research and recorded supporting sources. The approved new book was imported into structured teaching, navigation, references and shared Kotlin content for Android, iOS and the web.

The current content contains **10 modules, 40 lessons, 91 teaching/supporting documents, 400 sign/marking/signal reference entries, and 1,000 accepted questions covering 500 distinct concepts**. Lesson links, explanations, source classifications, compatibility aliases and exact artwork bindings accompany the migration. Question variants sharing a concept are not separate learning concepts.

The accepted content version is `screen-2026-10-14-78a89d8ffbb8-accepted-9j-step10-r1`. The accepted manifest declares identity digest `e08dddeb7f744029096d7e64568bd3980d272a503415f3837db3dddaaa293a79`; this is the compiler's identity field, not a claim about the complete manifest file's SHA-256. The step-10 correction release includes source-classification, caption and seven question-description revisions.

## The two books to retain

| Book | Retained path | Size in bytes |
| --- | --- | ---: |
| Old research book | [theory-book-2026-1 (1).pdf](<theory-book-2026-1 (1).pdf>) | 33,076,466 |
| Approved new book | [output/pdf/korkortgo-curriculum.pdf](output/pdf/korkortgo-curriculum.pdf) | 207,678,543 |

SHA-256 identities, checked against the step-1 recovery checkpoint:

```text
Old: e9aadde3822471a1ea2d85d17cdd23df30ff9f91c41c2dcb27e222104a71d994
New: 78a89d8ffbb83b6e9eec6193396871ac2fb9feccf245b85112809646dd595581
```

The new book is the **578-page tagged screen edition approved on 14 October 2026**. Print masters and print approval were deferred. Its retained output copy matches the approved production copy and the tagged duplicate exactly. Duplicate exports and the production-folder copies were removed in step 4; the output path above is the retained new book. The old research PDF is Git-ignored and is separately protected by the recovery archive.

## Where the maintained app content lives

- `content/curriculum.json`: structured teaching, references, navigation and artwork/source records.
- `content/accepted-assessment-questions.json` and `content/accepted-content-manifest.json`: current accepted bank, revisions and release identity.
- `content/package-sources.json` and `content/legacy-aliases.json`: classified sources/dates and compatibility routes.
- `composeApp/src/commonMain/kotlin/se/korkort/`: shared UI, engine and generated teaching/question/navigation code. Production starts at `App.kt` → `CurriculumApp.kt`.
- `composeApp/src/commonMain/composeResources/`: bundled artwork, fonts and complete font licences. These are app assets, including small reference PDFs.
- `composeApp/src/androidMain`, `iosMain`, `wasmJsMain`, and `iosApp/`: platform entry points and the native iOS host.

Generated production Kotlin remains necessary for normal builds. Step 5 retired historical import/release scripts and superseded JSON candidates. The retained reader/navigation generators consume only current content; `compile_curriculum.py` is now their small Kotlin-emission helper and `content_schema.py` reads the app model declarations. Original official-source provenance and the delivery-scope policy are retained. Accepted question-release automation remains archived; changing the scored bank requires separate generation/review work. Normal Gradle builds use the retained production Kotlin and resources. Current question/reader parity tests use small retained fixtures in `composeApp/src/desktopTest/resources/content-parity/`; candidate runtime tests no longer read or write migration evidence. Historical candidate banks and import-state files are archived and do not supersede the accepted release. Build commands remain in `README.md`.

## Credits and maintenance

Road-sign illustrations: **Transportstyrelsen**. English labels and explanations are editorial translations. Contextual illustrations: **KörkortGo, built-in imagegen artwork**. Preserve recorded artwork geometry, colours, approved crops and exact bundled bytes, together with source/reuse conditions. This summary grants no additional reuse rights.

Source Sans 3 and Source Serif 4 ship with their complete SIL Open Font License notices under `composeApp/src/commonMain/composeResources/files/font-licenses/`; retain those notices with redistributed fonts. Source dates, classifications and scope limits remain in the content records. Migration does not establish that every cited rule is current today. This is an independent learning aid, not an official examination or a substitute for current authority guidance.

## Remaining limitations

The content import and approved screen book are complete within their recorded scope; final app acceptance is unfinished. The archived journey ledger records **92/132 scoped passing dispositions**, including proof-host coverage, rather than 132 fully accepted normal-app journeys. Keyboard/focus behaviour, assistive listening, recovery equivalence, remaining target journeys and formal defect/gate reconciliation still require work. Proof-build dark requests can render the fixed light theme. iOS runtime evidence is simulator-scoped; physical-device acceptance is unperformed.

Reading and practice state is currently transient. Persistent progress and the dashboard are a separate, unapproved proposal. Cleanup does not implement them or close the outstanding acceptance work.

## Recovery and cleanup status

Step 1 created and verified an external recovery archive containing Git/LFS data, working changes, untracked files, temporary work and both books; generated caches and IDE state were excluded. Its location on the original machine is:

```text
/Users/zeyad/.codex/visualizations/2026/10/29/01a1887e-b633-70c2-a6ac-f18f594043ce/korkort-recovery-20261029T165342Z/
```

The folder contains `project-checkpoint.tar`, `manifest.json`, `VERIFIED.json` and restore instructions in `README.md`. The checkpoint records branch `main` at `9c611f7ffa3f4ab69480306b5a9cf83579b541a7`, plus the original uncommitted work. Detailed historical approvals, provenance and verification evidence are recoverable there if later removed from the project. Restore into an empty directory first.

Step 2 verified both retained book identities and created this brief. Step 3 removes the five verification-only source sets, their opt-in Gradle wiring, the iOS migration test target/scheme and the historical held-candidate capture test. Production app code and resources remain intact. Useful runtime tests and the current accepted question/reader parity checks are retained; running these tests no longer writes into the migration archive. Cleanup does not change historical acceptance decisions.

Step-3 validation: all 86 retained JVM tests passed, and Android, Wasm and iOS simulator Kotlin compilation succeeded. The Xcode project parses with valid app-scheme references. Both books, all 1,147 production source/resource files and the five protected redesign files were checked for unchanged bytes. Full platform packaging and final acceptance remain separate work.

Step 4 removed the historical curriculum/migration archive, obsolete development/verification documents, old mockup/brand/icon design sources and all duplicate/chapter PDF exports. The retained new book stays at `output/pdf/korkortgo-curriculum.pdf`. All 42,769 removed files matched the recovery checkpoint before deletion (5,584,103,127 bytes). Historical file paths embedded in provenance records identify archived evidence; they are not active build inputs. README links and PDF Git/LFS rules now match the retained layout. After removal, all 86 retained JVM tests passed again with zero failures, errors or skips; both books, all production files and all five protected redesign files remain byte-for-byte unchanged. The protected redesign plan, preview and prompt remain in the project.

Step 5 removed 53 obsolete tool files (including their migration-only tests and vector-decoder requirements) and 11 superseded content files, all matched to the recovery checkpoint before deletion (19,709,248 bytes). The old split source JSON files were redundant with `content/package-sources.json`. Current accepted data, provenance, generated production Kotlin and app assets remain intact. The retained reader/navigation tools reproduce the existing Kotlin and parity fixture without the migration archive; their check modes do not grant or renew content acceptance. Original source assets remain archived as requested. Step-5 checks: both retained generators passed check → write → check in an isolated checkout containing no migration archive or superseded inputs, reproducing all existing output bytes. All 86 retained JVM tests passed again. Both books, all 1,147 production source/resource files, seven retained content files and five protected redesign files are unchanged.

## Protected redesign files

The following files are explicitly retained for the redesign and must be excluded from subsequent cleanup:

- `docs/plans/progress-dashboard-plan.md`
- `design/progress-dashboard/preview-v2.png`
- `design/progress-dashboard/prompt-v2.md`
- `/Users/zeyad/.codex/generated_images/01a17def-b781-78b2-8ca0-132cfd37c804/exec-d08f48bb-ead1-44d1-a213-6313a2a83ff6.png`
- `/Users/zeyad/.codex/generated_images/01a17def-b781-78b2-8ca0-132cfd37c804/exec-9ef7c968-8632-48c0-81d5-8a94c29e46b8.png`
