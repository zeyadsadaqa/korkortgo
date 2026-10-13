# 7A — Content baseline and app audit

**Audited:** 14 October 2026.

**Status:** Audit complete; provisional baseline awaiting an approved release.

**Execution authority:** User explicitly requested 7A. This request is not recorded as approval of the finished PDF or execution of 6N. No app content or design was changed.

[Machine-readable baseline](baseline.json) records SHA-256 hashes, sizes, exact question ID order, legacy chapter ranges, all bundled assets and check results. Paths in that file are relative to the repository root. These records freeze input identities, not immutable copies; recheck hashes before downstream work.

## Release identity and entry requirement

The current source review PDF at `docs/curriculum/pdf-production/korkortgo-curriculum-review.pdf` and delivery copy at `output/pdf/korkortgo-curriculum-review.pdf` are byte-identical. Their SHA-256 is `6af8cf9fa56297d742ee0a2e3f2f4449d7026afad14e4bc8f68b46581792402b`, matching the [H7 all-question coverage metadata](../question-book-review/all-question-coverage.json). That evidence records **578 pages** and 1,000 covered questions, with zero not-covered or prompt-only questions. The question-bank hash also matches that review.

**7A-B01 — approved release missing:** The progress tracker still records 6N as not started; no `pdf-production/verification.md` or finished `pdf-production/korkortgo-curriculum.pdf` release is present. H0–H7 approval and coverage evidence support the subsequent content work, but do not establish 6N completion or explicit final-book approval. The older 498-page tracker text is historical assembly information, not the current PDF identity. Do not treat this provisional baseline as an approved release or clear the entry requirement for 7B. Confirm the finished release after 6N verification/approval, then refresh this baseline if any input changes.

The root manuscript, chapter sources, reference source and assembly/build scripts are independently hashed: later approved production corrections must not be lost by importing only the earlier manuscript. Step 7B must reconcile the final editable production content with the final release. The complete input inventory includes production Python/JSON/Markdown, content sources, app source, platform hosts, Gradle configuration and curriculum/source/sign/coverage records.

## Content counts and checks

| Item | Observed baseline |
|---|---|
| Questions / unique IDs | 1,000 / 1,000 |
| Distinct concepts | 500 |
| Question families | 178 situations, 616 signs, 206 calculations |
| Categories | RULES 692; SAFETY 141; VEHICLE 74; ENVIRONMENT 64; PERSONAL 29 |
| App chapters | 39; README's 37 is stale |
| Generated study topics | 178; bundled in Bank.kt, not used by the current UI |
| Official sign records / bundled images | 343 / 343 |
| Questions with nonempty source URL | 646; 354 have no per-question URL |
| Legacy question pages | 7–353; every value resolves to an existing chapter range |

The generated Kotlin question lines match every JSON question field, option and ordering exactly. All registered sign paths exist and every asset hash matches `content/signs.json`. Both current PDF copies and the bank match H7 metadata. These are local consistency checks; they do not revalidate external guidance or certify question quality. Retain the four H7 fuel-rounding qualifications for 7D.

## App entry points and migration impact

| Entry point | Current behaviour / migration constraint |
|---|---|
| [Quiz.kt](../../../composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt) | `Question` has id, concept, category, prompt, options, correct, explanation, integer page, optional source/image. No lesson ID or multi-source relationship. `Topic` also carries a page. Preserve question/concept identity and category allocation semantics. |
| [Bank.kt](../../../composeApp/src/commonMain/kotlin/se/korkort/Bank.kt) | Compile-time lazy bank in 29 functions, plus studyTopics and roadSigns. App does not load questions.json at runtime. Changing JSON alone will not update the app. `RoadSign` contains code/title/image/url, without the full caption/reuse register. |
| [Chapters.kt](../../../composeApp/src/commonMain/kotlin/se/korkort/Chapters.kt) | 39 `Chapter` records: title, category, page, endPage, summary. No stable chapter/lesson ID, objectives, reviews, source bindings or curriculum version. Exact titles/ranges are in baseline.json for later aliases. |
| [App.kt](../../../composeApp/src/commonMain/kotlin/se/korkort/App.kt) | Eight internal Page enum states: HOME, LIBRARY, READER, SETUP, QUIZ, RESULTS, REVIEW, SIGNS. Library filters by category and title/summary search, keys rows by title. Reader displays summary paragraphs and advances by chapter list position. |
| App.kt `readPage`, `QuestionCard` | Answer feedback/review calls `readPage(q.page)` to select the first inclusive chapter range. Unmatched values silently open the first chapter. Replace this with explicit canonical destinations and a reviewed fallback in 7E. There is no external deep-link parser in the audited source. |
| App.kt learner labels / `SourceFooter` | Home, library, reader and answer feedback include Theory Book 2026, edition/publisher attribution or book-page ranges. SourceFooter links to Transportstyrelsen; per-question links and road-sign cards open their recorded URLs via LocalUriHandler. Replace labels and source presentation through 7E–7F and approved step 8 design. |
| App.kt `ResourceImage` / composeResources | Reads packaged `files/<path>` via Compose resources and decodes bitmap images. Question/option images and roadSigns use the same resource namespace. Keep official code/variant and caption/reuse provenance when binding the curriculum sign package; the app and curriculum registers are separate inputs. |
| [build_content.py](../../../tools/build_content.py) | Compiles concepts.tsv, sign/index inputs and calculation models into Bank.kt, questions.json, signs.json and quality-report.json. Do not regenerate during planning; future changes must preserve reviewed content and generated/source parity. |
| [scrape_sources.py](../../../tools/scrape_sources.py) | Official-source/asset collection pipeline; source-manifest.json and signs.json retain URLs, retrieval dates and asset hashes. Refreshing downloads is separate work. |
| [Android host](../../../composeApp/src/androidMain/kotlin/se/korkort/MainActivity.kt), [iOS host](../../../composeApp/src/iosMain/kotlin/se/korkort/MainViewController.kt), [web host](../../../composeApp/src/wasmJsMain/kotlin/se/korkort/main.kt), iosApp | All launch the shared App. No separate platform curriculum loader or persistence implementation found. Build/resource changes affect all three platforms. |
| [QuizTest.kt](../../../composeApp/src/commonTest/kotlin/se/korkort/QuizTest.kt), composeApp/build.gradle.kts | Existing shared test harness and targets; future checks must cover content/navigation migration alongside allocation, concept uniqueness, answer integrity and session transitions. No build or runtime test was needed for this audit-only step. |

## Saved progress and bookmarks

No durable progress, bookmark, completed-lesson or question-history store was found in `composeApp/src` or `iosApp`; declared dependencies include no persistence library. Source searches included SharedPreferences, DataStore, localStorage, NSUserDefaults, rememberSaveable and bookmarks. This is a source-audit finding, not a runtime storage inspection.

App uses Compose `remember` for page, test length, feedback mode, current session, selected chapter, category/search, review filter and pending quit destination. Question selection and expanded review cards also use `remember`. QuizSession holds questions, answers keyed by question ID, current index and finished flag. Selected option indices refer to shuffled session options, not original bank positions. Leaving an unfinished quiz explicitly discards the session. Results and review use that same in-memory session.

7E should therefore record that there is no existing durable dataset to convert, specify behaviour for transient sessions on content replacement, and avoid inventing existing bookmarks/history. Any new persistence feature requires an explicit scoped implementation item. Preserve concept deduplication and the five category quotas; modules must not implicitly replace quiz categories.

## Handoff

The input identities and all current content/link/state entry points are recorded. The only completion blocker is establishing the approved final release (7A-B01); the count/provenance/model differences above are explicit migration constraints, not silently corrected here. 7A remains in progress until that entry requirement is met. 7B–7G have not started. No design preview or implementation is part of 7A.
