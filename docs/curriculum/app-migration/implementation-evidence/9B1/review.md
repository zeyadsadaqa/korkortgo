# 9B1 — Opening import execution review

**Executed:** 15 October 2026. **Status:** Complete. **Authorization:** “ok go ahead with next step” after 9A3.

[Usage and scope](README.md) · [Verification](verification.json) · [Approved PDF text extraction](pdf-opening-text.json) · [Source/output trace](trace.json)

Imported the approved introductory material into [content/curriculum.json](../../../../../content/curriculum.json): four published opening documents with 22 top-level blocks, followed by all sixty canonical module/lesson/review records. The full learning-aid disclaimer is retained verbatim in `introduction/disclaimer` with an explicit disclaimer role. Exact module/lesson/review titles, numbering, order, parent IDs, category tags and production-source origins are preserved. Front matter remains outside module cards and the 60-node reading sequence.

The selection uses the frozen manuscript intro and production builder for text/headings, plus the reviewed 7B/7E registries for IDs/order and production heading locations. Cover labels and the rendered study-guide headings are copied from production literals without executing the PDF builder. Manuscript editorial status and unrelated review bookkeeping are not imported as learner teaching. Strong text in the study guide stays structured as strong inline content. Contents links use canonical module IDs; unimported appendix/source actions remain explicit deferred bindings rather than fabricated routes. Appendix letters/titles remain in the opening text.

The companion [import ledger](../../../../../content/curriculum-import-state.json) explicitly marks sixty chapter bodies `structure_only`, names their 9B2–9B11 owners, retains required source/asset-register information and lists deferred cover/reference work. Skeletons have no fabricated objectives, summaries, knowledge checks, answers or completion. The ledger is build-time metadata; no learner store was added.

Added the bounded [importer](../../../../../tools/import_curriculum_opening.py) with explicit write/read-only check modes and overwrite protection for accumulated later imports. It stages data through the unchanged 9A3 compiler. The local empty assessment/source/alias roots are staging support, not edits to the live bank or claims that their future import tasks are complete. Generated output is not wired into the app's production source set. The payload remains ineligible for release until the later imports and acceptance work pass.

## Verification

- All stored 9A3 artifact/tool identities matched before work; no input drift needed repair. The final check also verifies that earlier compiler/evidence files remain unchanged.
- Used the PDF skill for a read-only inspection of the approved screen edition. Fresh pypdf extraction confirms the approved SHA-256 and 578-page count. All four opening pages were rendered with bundled Poppler and visually inspected as a contact sheet; no source PDF or layout was changed.
- Compared all imported opening text against the fresh approved-PDF extraction after removing known PDF chrome and contents-only numbers. The check preserves punctuation, text order, disclaimer, dates, appendix letters and every introductory paragraph. Source headings and all sixty title/order/origin records are checked independently.
- `python3 tools/import_curriculum_opening.py --check` passes, reproducing both authoring files in memory without writes.
- The final configured Kotlin/desktop build passes **14 tests**: six existing quiz regressions, five contract checks and three staged opening/reading-structure checks. See [build transcript](gradle-tests.txt), [import tests](TEST-se.korkort.OpeningImportTest.xml), [quiz tests](TEST-se.korkort.QuizTest.xml) and [contract tests](TEST-se.korkort.CurriculumContractTest.xml).
- Fresh compilation into a temporary directory matches all saved generated Kotlin parts and trace. Repeating it is byte-identical. Release-profile validation rejects the partial package. The live question JSON, bank, original summaries/app UI, official assets, approved PDFs and frozen teaching/design evidence remain unchanged.

The exact commands are in the [README](README.md). [verify_opening.py](verify_opening.py) writes only this step's machine-readable verification. Its saved XML checks do not claim a fresh JVM execution on every verification run. Later accepted cumulative imports may change this step's authoring-file hashes; the original execution snapshot remains a provenance record rather than a mandate to restore empty bodies.

## Completion and handoff

9B1 meets its completion criteria: opening text/disclaimer, canonical titles/order and exact origins match the approved sources, and the staged Kotlin constructs those values under the project's compiler. No blocking 9B1 issue remains.

Cover artwork delivery, appendix/source actions, supporting anchors, complete lesson/module-review bodies and all existing question/delivery/platform acceptance requirements remain in their assigned tasks. These deferrals are recorded in the import ledger and do not imply the curriculum is complete or production-ready.

**Next:** 9B2 — import module M01, separately requested. No module body import was started here.
