# 7B — Stable curriculum IDs and app content contract

**Prepared:** 14 October 2026, following the user's request to continue to the next step.

**Status:** Complete; release bindings refreshed against the explicitly approved tagged screen edition on 14 October 2026. All canonical IDs and exact titles remain unchanged; original provisional identities are retained in history/pre-6N-approved-curriculum-map.json.

[Structured curriculum map](curriculum-map.json) is the complete registry: exact titles and ordering, production-source paths/lines/hashes, objectives, source destinations, sign caption/asset bindings and supporting anchors. [7A baseline](baseline.md) supplies the audited app constraints and approved release identity. [7C](question-map-review.md) now assigns all 1,000 questions; source checks remain dated evidence, not refreshed external guidance.

## Canonical teaching structure

Keep M01–M10, their four lesson IDs and Mxx-R review IDs unchanged. Titles are checked against both the curriculum source map and the current chapter production source. Import the complete production content, including later approved additions, rather than rebuilding it from the old app summaries. The old 39 chapter titles and page ranges are migration evidence only; their destination mapping belongs to 7E.

| Module ID | Exact title | Lesson IDs | Review ID |
|---|---|---|---|
| M01 | Choose to drive responsibly | M01-L01–M01-L04 | M01-R |
| M02 | Prepare a car that is ready | M02-L01–M02-L04 | M02-R |
| M03 | Read the road before acting | M03-L01–M03-L04 | M03-R |
| M04 | Negotiate shared space | M04-L01–M04-L04 | M04-R |
| M05 | Make room in busy streets | M05-L01–M05-L04 | M05-R |
| M06 | Travel beyond the town | M06-L01–M06-L04 | M06-R |
| M07 | Adapt when conditions change | M07-L01–M07-L04 | M07-R |
| M08 | Take responsibility for the vehicle and load | M08-L01–M08-L04 | M08-R |
| M09 | Reduce the impact of each journey | M09-L01–M09-L04 | M09-R |
| M10 | Respond, reflect and keep learning | M10-L01–M10-L04 | M10-R |

| Lesson ID | Exact title |
|---|---|
| M01-L01 | Your route into driving |
| M01-L02 | Am I ready today? |
| M01-L03 | Pressure is a driving risk |
| M01-L04 | Plan the journey before the ignition |
| M02-L01 | Know what the controls tell you |
| M02-L02 | A check before moving |
| M02-L03 | Protect everyone inside |
| M02-L04 | Move with control |
| M03-L01 | Recognise what a sign asks |
| M03-L02 | Combine the instructions |
| M03-L03 | Find your way without rushing |
| M03-L04 | Leave room to respond |
| M04-L01 | Decide who goes first |
| M04-L02 | Turn with a complete picture |
| M04-L03 | Crossings belong to people |
| M04-L04 | Choose a safe path through a roundabout |
| M05-L01 | See the person behind the movement |
| M05-L02 | When the street changes purpose |
| M05-L03 | Choose a lawful place to stop |
| M05-L04 | Manoeuvre where people may appear |
| M06-L01 | Read the rural road |
| M06-L02 | Is passing worth the risk? |
| M06-L03 | Join faster traffic calmly |
| M06-L04 | Expect an interrupted route |
| M07-L01 | Drive within what you can see |
| M07-L02 | Grip is a changing resource |
| M07-L03 | Protect your attention |
| M07-L04 | Change the plan when risk grows |
| M08-L01 | Understand what you may drive |
| M08-L02 | Make the load part of the safety check |
| M08-L03 | Keep the car legally ready |
| M08-L04 | Know what assistance cannot do |
| M09-L01 | Look beyond the exhaust |
| M09-L02 | Use energy with foresight |
| M09-L03 | Choose the journey as well as the car |
| M09-L04 | Check where the vehicle can go |
| M10-L01 | When the car cannot continue |
| M10-L02 | When someone may be hurt |
| M10-L03 | Explain a whole journey |
| M10-L04 | Make a realistic readiness plan |

Every Mxx-R keeps the exact title “Review and self-assessment” within its module. There are 10 modules, 40 lessons and 10 reviews; quiz categories remain a separate five-area hierarchy.

## Reference destinations and aliases

Preserve `appendix-A` through `appendix-D` and their exact published titles. Preserve all 24 RB01–RB24 reference-group IDs, canonical sign destinations, source aliases and published supporting anchors. The registry accounts for all **1,123 existing PDF destinations**, with unique IDs: 88 teaching/appendix/group nodes, 400 caption-bound sign entries, 116 source destinations and 519 supporting anchors. PDF page numbers are evidence against the frozen release, never routing keys or source-book labels in the app.

Use the final assembly navigation register, not the initial front-matter navigation file. Preserve the final reference-production illustrations/bindings, including later H-step additions. The original placement group's selected codes show provenance and do not define exhaustive final group membership. A supporting anchor is available for precise content links; it is not automatically a library item or a separate lesson. Repeated sign placements remain distinct supporting anchors where the book defines them; they do not create duplicate canonical lessons.

No renumbering or new alias is needed for the published curriculum IDs. Keep aliases empty until an actual change is justified. Do not infer a one-to-one mapping from 39 old chapters to 10 modules. New imported blocks may use parent-scoped IDs, but their assignment must be recorded and stable across text/title edits; IDs must never depend on page number. Retired IDs require tombstones and explicit replacements, and must not be reused.

## Planned content contract

| Entity | Required behaviour and fields |
|---|---|
| Content package | Immutable content_version, schema_version and release/input hashes. Approved screen version `screen-2026-10-14-78a89d8ffbb8` binds to the release hash. No implicit “latest” selection. |
| Module | id, exact title, order, four lesson_ids, review_id. Validate all references and order. |
| Lesson / review | id, module_id, title, order, objectives, complete body_blocks, scenarios, knowledge_checks, separate answer_blocks, source_ids, asset_bindings, related_content_ids and content_version. Reviews have their own tasks rather than fabricated lesson objectives. |
| Content block | Stable parent-scoped id, type, text/payload, source and asset references, answer visibility. Include requirements/recommendations, scenarios, captions and accessible text; avoid flattening all content to a short summary. |
| Question relationship | Existing question_id, one primary_lesson_id, related_lesson_ids, reference_ids, source_ids, disposition and content_version. Actual assignments belong to 7C–7D. Preserve question/concept IDs and option/answer integrity. |
| Source | id, title, publisher, URL, classification, check date, evidence scope, editorial-inference flag, original alias/evidence IDs. Retain scoped URLs where a chapter defines an alias. A bibliography link alone does not establish official status or claim support. |
| Asset binding | ID/code/variant, original path and SHA-256, caption ID, alt text, editorial-translation status, reuse record, rendering constraints and approval binding. Do not substitute generated signs or conflate visually similar variants. |
| Navigation | Canonical content ID plus optional block/anchor ID. Keep folios only in evidence metadata. Unknown/retired target handling and old routes belong to 7E. |
| Session / progress | Preserve question IDs, shuffled-option session semantics, concept uniqueness and category quotas. No durable learner store exists to convert; 7E specifies transient-session behaviour. New persistence is separate scoped work. |

The source destination registry retains published URLs and their aliases without declaring every reference official. At import, preserve the existing distinction between official agency/legal/research evidence, supplementary commercial teaching, manufacturer guidance and editorial inference, including check dates and limitations. Source-map planning IDs (including G/MS additions) are retained as evidence IDs; they are not assumed to be interchangeable with book source aliases.

Knowledge checks and reviews retain explicit answer separation. The reader must not expose keyed answers before deliberate reveal. Keep scenarios, source context and the limited first-aid scope. Treat the full disclaimer and credits as package content with stable destinations. Visual presentation is still designed and approved in step 8.

## Required app changes

The audited app cannot consume this contract as-is. These changes are recorded for the 7F implementation backlog and later step 9:

- `Quiz.kt`: add typed curriculum/reference relationships while retaining existing quiz categories, quotas and concept deduplication.
- `Chapters.kt`: replace the 39 legacy summaries with the complete versioned curriculum and stable IDs.
- `tools/build_content.py` and `Bank.kt`: prepare deterministic curriculum import and generated question relationships; preserve JSON/Kotlin parity. Do not run the current compiler as a migration shortcut.
- `App.kt`: replace `readPage` and title/list-position identity with canonical destinations; support full lesson/review content, deliberate answer reveal and accurate source classification after approved previews.
- Compose resource packaging: bind exact official assets and approved illustrations to captions/accessibility text with reuse and variant constraints for Android, iOS and web.

## Verification and handoff

Verified unchanged 7A hashes; exact module/lesson titles; all 10 modules, 40 lessons and 10 reviews; four appendices; 24 sign groups; unique registry IDs; and resolution of every lesson's published source destination. All 1,123 published destinations are registered and bound to the 578-page navigation record. Production locations and current register hashes are recorded in JSON. No question assignments, new designs or app implementation were created.

The contract fits the app through the explicitly listed model/import/navigation/resource changes. The 6N release prerequisite is now satisfied and 7A–7B are complete. Recheck the registry and hashes if the approved final release changes before import.

## 6N release change — 14 October 2026

The wildlife-collision cross-reference was corrected and the 578-page book rebuilt during 6N. The original provisional input hashes identify the earlier review edition and are now preserved in history. See [release-change-notice.json](release-change-notice.json). Canonical IDs/titles were unchanged; the input/release bindings were refreshed before 7C.

## Approved-release handoff

The earlier 6N release-change notice is resolved by the refreshed bindings in this file and baseline.json. 7C is complete; 7D–7G remain separate steps. Print masters are deferred by explicit user choice.
