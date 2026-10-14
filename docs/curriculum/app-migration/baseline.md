# 7A — Content baseline and app audit

**Audited:** 14 October 2026.

**Status:** Complete. The user explicitly approved 6N and authorised 7C on 14 October 2026. The approved tagged screen edition is frozen in [baseline.json](baseline.json); print masters are explicitly deferred. Original provisional identities are preserved in [history](history/pre-6N-approved-baseline.json).

## Release identity

The current approved release is `pdf-production/korkortgo-curriculum.pdf`, SHA-256 `78a89d8ffbb83b6e9eec6193396871ac2fb9feccf245b85112809646dd595581`, 578 pages, identical to its delivery copy. See [approval and scope](../pdf-production/final-review/screen-release.json). The untagged review source remains `ae872daf…`; historical H7 coverage retains its earlier `6af8cf9f…` identity. Those different hashes are explicit history, not current-release equality claims. The 6N evidence and fresh 7C passage comparison transfer the coverage to this approved edition, including the page-193 wildlife cross-reference correction.

7A-B01 is closed. Twelve expected production/document inputs changed during 6N; all audited app sources, the 1,000-question bank and 343 bundled assets remain unchanged. Updated hashes and a change list are saved in baseline.json. This refresh does not alter the audited persistence/navigation findings below.

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

7A is complete against the approved screen release. 7B retains all canonical IDs and titles, and 7C maps every question to teaching and sources. Quality/disposition review is 7D; legacy-link reconciliation is 7E. No app implementation or visual design occurred. The old 39-chapter inventory below/in JSON is audited migration history only, not the canonical learning structure.
