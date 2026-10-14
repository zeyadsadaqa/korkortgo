# 7E — Link and learner-state migration plan

**Completed:** 14 October 2026. Every audited question, chapter, topic, sign-catalogue reference, navigation state and learner-state field has a migration rule. Three exact signal destinations are explicitly unresolved with fallbacks; they are handed to 7F. The live app, 1,000-question bank, assets and approved PDF are unchanged. This plan does not add persistence or public deep links.

- [Structured map](link-and-progress-map.json)
- [Acceptance checks and compatibility fixtures](link-and-progress-checks.json)
- [7A baseline](baseline.json), [7B registry](curriculum-map.json), [7C question links](question-map.json), [7D dispositions](question-actions.md)

## Coverage

| Audited input | Planned handling |
|---|---|
| 1,000 questions / 145 distinct old page values | Exact question-ID routes to 7C lessons, related references and scoped sources; 7D disposition/revision policy retained. |
| 39 legacy chapters | 10 single-destination aliases and 29 topic choosers; no imported old chapter structure or case narratives. |
| Numeric legacy span 6–366 | All 361 integers recorded; 38 gap pages explicitly unavailable. No nearest-page or first-chapter fallback. |
| 178 generated study topics | Exact source-row/question identity resolves a canonical lesson; retire unused old summary payload. |
| 343 legacy sign records | 340 exact canonical sign routes; SIG16, SIG17 and SIG18 explicitly held. |
| Five quiz categories | Preserve IDs, exact labels and allocation; separate many-to-many library tags cover all 40 lessons. |
| Eight Page states | Typed internal destinations and shared active-test guard; required session/content context checked. |
| Learner state | 18 transient/derived field rules plus four explicit absent-store/progress contracts. No database migration exists to run. |
| Main reading sequence | 60 stable nodes: ten module introductions, 40 lessons and ten reviews; appendices/sign/reference navigation is separate. |

## Link resolution

Question ID takes precedence over a legacy folio. `situation-017` and `situation-103` both carry old page 46, but their approved teaching targets are M04-L03 and M04-L01 respectively. A shared page is not enough to infer the intended passage. An unknown question must not fall through to a guessed page route. PDF folios in 7C remain evidence, not app navigation keys.

Known canonical IDs open the correct content. Optional removed blocks fall back only to their known canonical parent with a moved-passage notice. Unknown/retired IDs show an explicit unavailable state and validated related/library actions. A retirement with one reviewed replacement can offer that replacement with notice; multiple replacements require a chooser. Nothing silently opens the first module or awards completion.

Legacy chapter/title/page lookup requires the frozen app namespace recorded in JSON, tied to the audited Chapters.kt hash. Titles are normalized for compatibility lookup only; new library identity/order never comes from titles or folios. A page-only request maps to related teaching or a chooser, not an asserted exact translation of an old book page into the new PDF. Invalid numbers, old-range gaps, foreign namespaces and unknown titles are unsupported.

The old chapter titles and ranges below are technical audit inputs only. Learners see canonical module/lesson titles. The “Lessons from court cases” alias points to related principles; its old case narratives are not ported or represented as cases in the approved curriculum.

| Legacy chapter | Old range | Canonical destinations | Resolution |
|---|---|---|---|
| The foundations | 6–12 | M03-L02, M03-L04, M05-L01 | topic_chooser |
| Lanes & positioning | 14–20 | M03-L02, M03-L03, M04-L02 | topic_chooser |
| Priority & junctions | 22–44 | M03-L01, M03-L02, M04-L01, M04-L02, M05-L01 | topic_chooser |
| Pedestrians & cyclists | 46–56 | M04-L01, M04-L02, M04-L03, M05-L01 | topic_chooser |
| Roundabouts | 58–66 | M04-L04 | content |
| Stopping & parking | 68–76 | M05-L03, M05-L04 | topic_chooser |
| Country roads | 78–88 | M03-L03, M03-L04, M04-L02, M05-L01, M06-L01, M06-L04 | topic_chooser |
| Motorways & clearways | 90–96 | M06-L03 | content |
| Overtaking | 98–106 | M06-L02 | content |
| Railway crossings | 108–114 | M06-L04 | content |
| Special streets | 116–122 | M05-L02 | content |
| Winter & changing grip | 124–130 | M03-L04, M07-L01, M07-L02 | topic_chooser |
| Learning & judgement | 132–138 | M01-L03, M01-L04, M02-L01, M06-L04, M07-L04, M10-L04 | topic_chooser |
| Alcohol, medication & distraction | 140–146 | M01-L02, M07-L03 | topic_chooser |
| Fatigue | 148–152 | M01-L02, M01-L04, M07-L03 | topic_chooser |
| Vision & perception | 154–160 | M03-L04, M07-L01, M07-L03 | topic_chooser |
| Sharing the road with disabilities | 162–166 | M04-L03, M05-L01 | topic_chooser |
| Children in traffic | 168–172 | M04-L03, M05-L01 | topic_chooser |
| Collisions & emergency response | 174–186 | M01-L03, M06-L01, M10-L01, M10-L02 | topic_chooser |
| Vehicle types | 188–194 | M05-L01, M06-L03, M08-L01 | topic_chooser |
| Reaction, braking & stopping | 196–202 | M03-L04 | content |
| Tyres | 204–212 | M02-L02, M07-L02, M09-L02, M09-L04 | topic_chooser |
| Steering & stability | 214–222 | M07-L02, M08-L04 | topic_chooser |
| Brakes | 224–230 | M02-L01, M05-L04, M07-L02, M08-L04 | topic_chooser |
| Crash protection | 232–236 | M02-L03, M08-L02 | topic_chooser |
| Child restraints | 238–242 | M02-L03 | content |
| Dimensions & projecting loads | 244–250 | M08-L01, M08-L02 | topic_chooser |
| Loads & trailers | 252–260 | M08-L01, M08-L02 | topic_chooser |
| Lights & signals | 262–270 | M02-L02, M02-L04, M04-L02, M07-L01 | topic_chooser |
| Before you drive | 272–276 | M02-L01, M02-L02, M02-L03 | topic_chooser |
| Inspections | 278–282 | M08-L03 | content |
| Maintenance essentials | 284–288 | M02-L01, M02-L02, M10-L01 | topic_chooser |
| Registration & ownership | 290–296 | M08-L03 | content |
| Insurance | 298–302 | M08-L03, M10-L02 | topic_chooser |
| Environment & health | 304–310 | M09-L01, M09-L02, M09-L03 | topic_chooser |
| Eco-driving | 312–316 | M09-L02 | content |
| Fuels & environmental zones | 318–322 | M09-L01, M09-L03, M09-L04 | topic_chooser |
| Road signs & markings | 324–360 | M03-L01, M03-L02, M03-L03, M03-L04, M04-L01, M04-L02, M04-L03, M04-L04, M05-L01, M05-L02, M05-L03, M05-L04, M06-L01, M06-L02, M06-L03, M06-L04, M07-L01, M07-L02, M08-L01, M08-L02, M09-L04, M10-L01, M10-L02, appendix-B | topic_chooser |
| Lessons from court cases | 362–366 | M03-L04, M04-L01, M05-L03, M05-L04, M10-L02 | topic_chooser |

## Navigation, categories and sources

Retain the existing five quiz categories and quotas: VEHICLE 7, ENVIRONMENT 5, SAFETY 16, RULES 32 and PERSONAL 5, plus five random slots for a 70-question test. Existing rounding for shorter tests and concept deduplication remain. Categories are filters/scoring domains, not replacements for the ten modules. Lesson tags combine objective/topic classification with reviewed primary-question categories so every related lesson remains discoverable, including lessons with no practice questions. Filtered modules keep canonical order and numbering.

Replace the reader’s title/list-position identity with canonical IDs. Previous/next follows the saved module/lesson/review sequence. Source/sign/reference visits retain a validated return context rather than dropping the user into an unrelated chapter. All navigation that leaves an unfinished test uses the existing confirm/discard guard; related reading is not a pre-answer shortcut. Missing results/review sessions show no saved result and an explicit setup action.

Question source references resolve through the exact URL/classification in 7C; a source alias retains its module scope. Do not build links from the old `url_by_page` table. Display the actual publisher and distinguish legislation, official guidance/research, manufacturer cautions, commercial teaching and editorial applications. Preserve per-source dates and scope limits, without claiming all sources were checked on one new date. Official artwork credits and editorial-English notices remain.

All audited Android/iOS/web hosts launch the shared App without an external content-route parser or content URL scheme. The registry defines planned internal typed destinations, not a new public deep-link API. Exact sign codes retain their registered case, including F31a.

## Learner-facing legacy labels

| Current source or label | Replacement rule |
|---|---|
| home_attribution (App.kt:94) | KörkortGo original curriculum and explained practice. This is a learning aid, not an official examination. |
| edition_stat (App.kt:86) | Use the accepted curriculum release’s human-readable label; module/lesson/question counts come from its manifest. |
| chapter_count (App.kt:97) | Explore 10 modules and 40 lessons; render actual accepted manifest counts. Five quiz areas remain filters. |
| chapter_page_badge (App.kt:105) | Canonical module/lesson title and optional objective; remove old book page ranges. |
| reader_attribution (App.kt:111) | KörkortGo · canonical module/lesson title. Source/evidence folios remain metadata, not routing labels. |
| question_attribution (App.kt:238) | Related learning: exact canonical lesson title, plus separately classified supporting sources. |
| source_footer (App.kt:255) | Use the complete approved learning-aid disclaimer, official artwork credits, editorial-English notice and per-source dates/classifications; do not claim a universal new check date. |
| question_source_label (App.kt:239) | Use each actual publisher and classification from the 7C source evidence; distinguish legislation, official advice/research, manufacturer guidance and commercial/editorial teaching. |
| related_learning_button (App.kt:240) | Read the related lesson; route by question ID → canonical primary_lesson_id. |
| previous_next (App.kt:117) | Previous / Next in canonical reading_order; explicit module review boundary and reference return context. |
| old_sign_chapter_condition (App.kt:113) | Use typed sign-catalogue action / appendix-B ID; do not branch on a retired title. |
| sign_catalogue_label (App.kt:100) | Road signs and signals; verified official artwork with editorial English teaching. Derive current count from accepted entries. |
| chapter_empty_state (App.kt:102) | No matching learning material; offer category/query reset without opening an unrelated first lesson. |
| home_summary (App.kt:94) | Original modules, lessons and references; do not imply the old 39 summaries are the finished curriculum. |

README’s stale 37-chapter feature claim and supplied-book attribution are also queued for implementation updates. Compatibility aliases and research provenance remain in technical records, not new learner-facing chapter/page labels. This step records the edits; it does not apply them. App branding remains outside this migration.

## Sessions and content versions

There is **no durable progress, bookmark, completed-lesson or question-history store** in the audited source. The existing `remember` and QuizSession data normally disappear on app restart. No old progress is invented or converted, and no new database/cloud sync is authorised. The JSON enumerates all nine App state variables, two local question/review states, five QuizSession fields, two derived properties and four absent-store contracts.

For any later same-process package switch, activate the new package atomically at a safe idle boundary. Pin each active/completed session’s original questions, shuffled option order, keys, answers, feedback and package/revision identity until finish, deliberate quit or review ends. Do not hot-swap its bank or silently discard answers. Pending navigation and unconfirmed selections must be tied to the same session/question revision; new sessions reset review filters and expansion state.

An immutable app-content version must bind the curriculum, accepted question revisions, assets, aliases and source bindings through a manifest digest. The approved PDF hash alone does not identify an app package after question edits. Historical review keeps its original feedback/score; opening newer teaching must state that the learning material changed since that attempt.

A recorded answer index is an index in its **original shuffled options**, not the generated bank. Historical results must never be regraded using a new key or order. The four exact-fuel rewrites are a concrete example: `fuel-saving-150-1.5` currently displays 2.2 litres under the disclosed rounding convention; the proposed exact task keys 2.25 litres. Keep a future old attempt as historical and request fresh current assessment after revision. The proposal is still unapplied.

For future separately authorised durable stores, unchanged semantic revisions may preserve mastery; rewrite/replace defaults to a new revision and no automatic current credit. A bookmark can keep an unchanged canonical destination; a moved block falls back to its known parent with notice. Changed/split/merged lessons need explicit completion-compatibility review. An old chapter marked read or a range of pages never awards completion to all related new lessons. Unversioned/orderless imported answers are unsupported until separately audited. These are conditional compatibility rules, not existing user records or a persistence feature.

## Held links and retired content

SIG16 (red flashing light), SIG17 (fixed red light) and SIG18 (extra-caution flashing amber) have legacy catalogue records but no exact approved 7B sign destination. Keep their recorded official URLs as separate labelled actions and offer M03-L02 as related teaching. Do **not** alias them to SIG1, SIG5, Y1 or any visually similar signal. 7F must either schedule exact-entry verification/addition through the content/asset workflow or retain the unavailable internal-route policy. No new sign is silently approved here.

7D removes zero questions, so the production tombstone list is empty. Synthetic retirement fixtures exercise no replacement, one replacement and multiple replacements without pretending any real question was removed. For future approved retirement, never reuse the ID; preserve valid historical snapshots, exclude the item from new selection and give an explicit unavailable/replacement choice.

The 38 7D image replacements retain their teaching/source links but remain ineligible for new scored use until accepted. All rewritten content must also pass its recorded acceptance criteria before inclusion in an active package. Derive displayed counts from accepted active content; preflight category/concept availability for every supported test size. Do not silently borrow unaccepted/retired items or alter quotas to fill a shortfall. The live bank still has 1,000 unchanged questions.

## Before/after cases

| Case | Before | After |
|---|---|---|
| Retained question | situation-001 → old page 8 / first legacy chapter | M03-L02 via question ID; preserve concept and reviewed question. |
| Shared old folio | situation-017 and situation-103 → page 46 | M04-L03 and M04-L01 respectively; no page-only guess. |
| Changed exact fuel key | fuel-saving-150-1.5 → rounded 2.2-litre key | M09-L02 teaching; proposed 2.25-litre exact key gets a new revision. No historical regrading. |
| Replaced visual item | sign-meaning-S1 → faint legacy image | Related lesson/sign-S1 remains reachable; scored delivery stays gated pending proof. |
| Retired item (synthetic) | fixture-retired-question | Unavailable; no first-chapter fallback, selection or automatic completion. Zero real retirements. |
| Unmapped signal | SIG16 legacy catalogue record | Explicit missing-entry state, recorded official URL and optional related M03-L02 action. |
| Invalid old page | namespace-qualified page 13, between audited ranges | Unavailable; no clamping to adjacent/first chapter. |
| Removed block (synthetic) | M03-L04 with removed passage anchor | M03-L04 with a moved-passage notice; unknown parent stays unavailable. |

## Verify and hand off

```sh
python3 docs/curriculum/app-migration/build_link_progress_map.py
python3 docs/curriculum/app-migration/verify_link_progress_map.py
```

Checks cover every frozen upstream input; all 1,000 question links, 39 chapter aliases, 361 integer-page cases, 178 topics, 343 sign records, five categories, eight navigation states and 22 state/progress contracts. All destinations resolve or have the explicit three-gap policy. Compatibility fixtures cover retained/changed/replaced/retired content, shared-page ambiguity, missing targets, namespace errors and shuffled-answer identity. The generated plan rebuilds byte-identically. No app/runtime tests or source changes were needed for this planning step.

**Next:** 7F — bounded implementation backlog and representative preview handoff, including the three exact-sign decisions and 7D acceptance holds. It has not started.
