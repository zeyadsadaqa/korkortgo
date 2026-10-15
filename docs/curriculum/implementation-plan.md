# KörkortGo Curriculum PDF and App Implementation Plan

The finished PDF will become the app’s learning source, with original teaching material supported by official references. Each step produces a saved deliverable and can be requested independently.

## 1. Build the source inventory — completed

Identify relevant category B topics and official references from Trafikverket and Transportstyrelsen. Record verification dates, coverage gaps, and road-sign availability. Existing research notes remain internal.

**Deliverable:** [Source inventory and findings](source-inventory.md).

## 2. Draft the original curriculum and official-source map

Create original modules, lesson titles, objectives, and a teaching sequence. Map each objective to official sources, using the official syllabus and examination domains to check completeness. Secondary reading serves only as background.

**Deliverable:** Curriculum outline and official-source coverage map.

**Approval:** Wait for approval of the outline before writing the manuscript.

## 3. Write the complete learning material

Develop original explanations, scenarios, summaries, and knowledge checks for the approved outline. Support factual claims with official references and distinguish legal requirements from recommendations. Flag unsupported details for research.

**Deliverable:** Editable manuscript without third-party book references or page numbers.

## 4. Prepare official road-sign illustrations

Execute the following substeps in order. Each can be requested separately, using the saved output from the preceding substep. These steps prepare official assets and editorial placements; visual layout design and its approval remain in step 5.

### 4A. List the signs needed for the curriculum

Review the manuscript and existing road-sign inventory. List the signs, supplementary plates and relevant variants needed for lesson examples and the sign reference section. Include the known F1-1/F1-2 gaps and record why each selected item is needed.

**Input:** Step 3 manuscript and step 1 road-sign inventory.  
**Deliverable:** `sign-selection.md` — selected sign codes, variants, intended lessons and missing items.  
**Done when:** Every manuscript sign example has a selected official sign or an explicitly recorded research gap.

### 4B. Verify official sources and reuse conditions

For the selected items, locate Transportstyrelsen’s official pages and image links. Record retrieval dates, reuse conditions and any required attribution. Resolve selection gaps where possible and clearly identify assets whose use is not yet supported.

**Input:** 4A selection.  
**Deliverable:** `sign-sources.json` and `sign-reuse.md` — official source links and reuse evidence.  
**Done when:** Each selected item has a source and reuse status; unsupported items are explicitly held out of the usable set.

### 4C. Collect and check the image files

Download supported official assets, retaining original files and identifying codes and variants. Check file integrity, dimensions or vector format, transparency and visual correspondence to the official source. Record checksums and replace unsuitable copies when an official alternative exists.

**Input:** 4B source and reuse records.  
**Deliverable:** `sign-assets/` and `sign-asset-manifest.json` — collected files and quality checks.  
**Done when:** Every collected asset matches its official variant and has a recorded quality status. Record print-size limits for later PDF layout; do not redraw or generate substitute official signs.

### 4D. Write and verify labels and explanations

Record each sign’s official Swedish name, a clear English label, concise original teaching text and accessibility text. Verify meanings and important exceptions against official guidance; identify English translations as editorial where no official English wording is available.

**Input:** 4B references and 4C verified assets.  
**Deliverable:** `sign-captions.md` and `sign-captions.json` — reviewed labels, explanations and source references.  
**Done when:** Each usable asset has a checked caption and accessibility text, with unsupported meanings or translations flagged.

### 4E. Map signs to lessons and the reference section

Assign verified assets and captions to the relevant lesson IDs and passage locations. Specify the learning purpose, related plates or variants to show together, and reference-section grouping. Keep this as an editorial placement map; page layouts are designed in step 5.

**Input:** 4A selection, 4C assets and 4D captions.  
**Deliverable:** `sign-placement-map.md` and `sign-placement-map.json`.  
**Done when:** Every selected teaching example has a usable asset and caption mapped to a manuscript location, or an explicit unresolved gap.

### 4F. Verify the complete sign package and update progress

Cross-check selection, files, variants, captions, sources, reuse records and placements. Check for missing files, duplicate or mismatched codes and unresolved blockers. Save the result and update the progress tracker with completed substeps and any outstanding work.

**Input:** All 4A–4E deliverables.  
**Deliverable:** `sign-verification.md` and updated [progress tracker](progress.md).  
**Done when:** All required signs have verified assets, captions, reuse records and placements, with no blocking gaps. Otherwise keep step 4 in progress and list what remains. Final rendered print quality is checked in step 6.

All listed deliverables are saved under `docs/curriculum/`. Update the progress tracker after each substep; completing one does not automatically start the next.

## 5. Generate a PDF design preview

Execute the following substeps separately. This step produces visual proposals and a design handoff; the finished PDF is built in step 6. Use the imagegen skill for each visual preview. After each preview, wait for feedback or explicit approval; if revisions are requested, revise the preview and wait again before proceeding.

### 5A. Define the design brief and check readiness

Review the manuscript, sign placement map and 4F verification report. Define page format, reading audience, visual hierarchy, accessibility goals, navigation needs and representative content for the previews. Record where the learning-aid disclaimer, official-source references and illustration credits must appear. Carry forward unresolved sign holds and print-size limits.

**Input:** Step 3 manuscript and all step 4 deliverables.  
**Deliverable:** `pdf-design-brief.md` — design requirements, preview content and readiness checklist.  
**Done when:** The brief is complete and blockers are explicit. The brief may be prepared while step 4 remains in progress, but resolve its required sign blockers and rerun 4F before starting 5B.

### 5B. Preview the cover and opening pages

Use imagegen to propose the cover and introductory page treatment, establishing typography, colour, spacing and the visual identity. Make the learning-aid disclaimer prominent and avoid any appearance of official endorsement.

**Input:** 5A brief and a sign package that passes 4F.  
**Deliverable:** `pdf-design/5b/` — visual previews and `review.md` recording feedback, revisions and approval status.  
**Done when:** The user explicitly approves the cover and opening-page direction. Pause for approval before 5C.

### 5C. Preview contents and navigation

Use imagegen to show the contents pages, module opening and running navigation using the approved visual direction. Demonstrate original module and lesson titles, stable lesson IDs and the PDF’s own page numbering. Preview how readers find the sign reference section and official sources.

**Input:** Approved 5B previews, 5A brief and manuscript structure.  
**Deliverable:** `pdf-design/5c/` — navigation previews and `review.md`.  
**Done when:** The user explicitly approves the contents and navigation treatment. Preview page numbers are illustrative until step 6 pagination is final.

### 5D. Preview representative lesson pages

Use imagegen to show a short sequence of lesson pages covering explanations, legal requirements versus recommendations, scenarios, summaries and knowledge checks. Include both dense text and a page with an illustration area, plus source-reference treatment and answer placement. Use original manuscript excerpts as the content basis. Revise representative lesson and self-assessment previews to include scenario illustrations and sign placements following the [illustration instructions](../../design/brand/illustration-guide.md); an empty image area alone does not satisfy the requested illustrated treatment.

**Input:** Approved 5B–5C previews and representative lessons selected in 5A.  
**Deliverable:** `pdf-design/5d/` — lesson previews and `review.md`.  
**Done when:** The user explicitly approves the lesson layouts and readability direction.

### 5E. Preview sign layouts and contextual diagrams

Use imagegen to preview sign-reference pages, signs with related plates and lesson illustration layouts from the placement map. Address the contextual diagram briefs individually and record any that remain deferred. Audit all 40 lessons and 10 module reviews for scenario/sign illustration needs, extend D01–D08 as needed, and prepare a consistent Swedish vehicle, people, police and road reference sheet. Identify exact verified assets by code in accompanying notes and respect their print-size limits. Generated sign depictions are layout placeholders only: they do not replace official assets or verify a traffic rule. The finished PDF must use the verified official files, and contextual diagrams must preserve the reviewed teaching meaning.

**Input:** Approved 5B–5D previews, verified sign assets and captions, and 4E placements and diagram briefs.  
**Deliverable:** `pdf-design/5e/` — sign and diagram previews, asset mapping notes, `illustration-register.md`, `style-reference-sheet.md` and `review.md`.  
**Done when:** The user explicitly approves the proposed sign layouts and each diagram intended for implementation; unresolved teaching or asset gaps remain listed as blockers.

### 5F. Consolidate the approved design and obtain final approval

Review all previews together for consistency and completeness. Record the approved page templates, typography, colour, spacing, navigation, disclaimer, source and credit treatment, asset constraints and diagram decisions in a design specification. If consolidation requires visual changes, use imagegen to revise the affected previews and obtain approval again. Keep the specification separate from PDF implementation.

**Input:** Approved 5B–5E previews and their review records.  
**Deliverable:** `pdf-design-spec.md` and `pdf-design-review.md` — approved preview index, implementation requirements, approval record and outstanding issues.  
**Done when:** The user explicitly approves the complete design package and no design or required-asset blockers remain. Record approval only after it is given. Step 6 starts only when separately requested.

All step 5 deliverables are saved under `docs/curriculum/`. Update the [progress tracker](progress.md) after each executed substep; completing one does not automatically start the next. Imagegen previews guide the design; exact text, official artwork, pagination and rendered accessibility/readability are verified during step 6.

## 6. Produce and verify the curriculum PDF

Execute 6A–6N separately: preparation, ten chapter builds, reference material, assembly and final verification. Each chapter corresponds to one approved manuscript module; keep its exact original title and stable lesson IDs. Completing a substep does not authorise the next one.

**Entry requirements:** Approved manuscript and complete design package, resolved [5F completion blockers](pdf-design-review.md), and verified required sign assets. Confirm illustration coverage, Swedish visual consistency, official sign bindings and individual preview approvals under the [illustration instructions](../../design/brand/illustration-guide.md). This planning breakdown does not clear existing blockers or start PDF production. Any new or changed design requires an imagegen preview and explicit approval before implementation.

### 6A. Prepare the reusable PDF build and opening pages

Check and record entry requirements. Set up the editable source, reproducible build instructions, approved fonts and licences, shared page templates and asset bindings. Build the approved cover, introduction and prominent learning-aid disclaimer. Prepare the contents structure and stable navigation destinations; final page numbers are assigned in 6M.

**Input:** Approved manuscript, design specification, brand guide and verified illustration/sign package.  
**Deliverable:** `pdf-production/README.md`, shared editable build source, `pdf-production/front-matter.pdf` and readiness/render review.  
**Done when:** Entry requirements are met, the build is reproducible and rendered opening pages match the approved design with selectable text, embedded fonts and the exact disclaimer.

### Shared requirements for every chapter (6B–6K)

Use the corresponding section of [manuscript.md](manuscript.md), its evidence records, sign placements and approved illustrations. Include the chapter opening, all four complete lessons, worked scenarios, knowledge checks and answers, and the module review/self-assessment. Keep assessment answers separate from the question as specified in the approved design. Include official references and illustration captions/accessibility text; preserve the limited 1177 first-aid scope.

For each chapter, save editable source, a standalone review PDF and a review record under `pdf-production/chapters/Mxx/`. Render and inspect every page for legibility, overflow, sign quality and Swedish scene accuracy. Check lesson/review coverage, factual claims against their official references, internal destinations and absence of third-party book names or page references. Record source-check dates and unresolved issues. Chapter PDF folios are provisional; final book pagination and cross-chapter links are verified in 6M–6N.

**Done when, for each chapter:** All four lessons and its review are present, required approved illustrations and exact official sign assets are included, rendered checks pass and no chapter-specific blockers remain. Record its status and review PDF in progress before stopping. Chapter completion does not mean final book approval.

### 6B. Produce chapter 1 — Choose to drive responsibly

Build module M01, including M01-L01–M01-L04 and M01-R, using the shared chapter requirements above.

**Input:** Completed 6A and the approved content/assets for M01.  
**Deliverable:** `pdf-production/chapters/M01/chapter.pdf`, editable chapter source and `review.md`.  
**Done when:** This chapter meets every shared chapter completion requirement. It can be requested independently after 6A; other chapter builds are not a dependency.

### 6C. Produce chapter 2 — Prepare a car that is ready

Build module M02, including M02-L01–M02-L04 and M02-R, using the shared chapter requirements above.

**Input:** Completed 6A and the approved content/assets for M02.  
**Deliverable:** `pdf-production/chapters/M02/chapter.pdf`, editable chapter source and `review.md`.  
**Done when:** This chapter meets every shared chapter completion requirement. It can be requested independently after 6A; other chapter builds are not a dependency.

### 6D. Produce chapter 3 — Read the road before acting

Build module M03, including M03-L01–M03-L04 and M03-R, using the shared chapter requirements above.

**Input:** Completed 6A and the approved content/assets for M03.  
**Deliverable:** `pdf-production/chapters/M03/chapter.pdf`, editable chapter source and `review.md`.  
**Done when:** This chapter meets every shared chapter completion requirement. It can be requested independently after 6A; other chapter builds are not a dependency.

### 6E. Produce chapter 4 — Negotiate shared space

Build module M04, including M04-L01–M04-L04 and M04-R, using the shared chapter requirements above.

**Input:** Completed 6A and the approved content/assets for M04.  
**Deliverable:** `pdf-production/chapters/M04/chapter.pdf`, editable chapter source and `review.md`.  
**Done when:** This chapter meets every shared chapter completion requirement. It can be requested independently after 6A; other chapter builds are not a dependency.

### 6F. Produce chapter 5 — Make room in busy streets

Build module M05, including M05-L01–M05-L04 and M05-R, using the shared chapter requirements above.

**Input:** Completed 6A and the approved content/assets for M05.  
**Deliverable:** `pdf-production/chapters/M05/chapter.pdf`, editable chapter source and `review.md`.  
**Done when:** This chapter meets every shared chapter completion requirement. It can be requested independently after 6A; other chapter builds are not a dependency.

### 6G. Produce chapter 6 — Travel beyond the town

Build module M06, including M06-L01–M06-L04 and M06-R, using the shared chapter requirements above.

**Input:** Completed 6A and the approved content/assets for M06.  
**Deliverable:** `pdf-production/chapters/M06/chapter.pdf`, editable chapter source and `review.md`.  
**Done when:** This chapter meets every shared chapter completion requirement. It can be requested independently after 6A; other chapter builds are not a dependency.

### 6H. Produce chapter 7 — Adapt when conditions change

Build module M07, including M07-L01–M07-L04 and M07-R, using the shared chapter requirements above.

**Input:** Completed 6A and the approved content/assets for M07.  
**Deliverable:** `pdf-production/chapters/M07/chapter.pdf`, editable chapter source and `review.md`.  
**Done when:** This chapter meets every shared chapter completion requirement. It can be requested independently after 6A; other chapter builds are not a dependency.

### 6I. Produce chapter 8 — Take responsibility for the vehicle and load

Build module M08, including M08-L01–M08-L04 and M08-R, using the shared chapter requirements above.

**Input:** Completed 6A and the approved content/assets for M08.  
**Deliverable:** `pdf-production/chapters/M08/chapter.pdf`, editable chapter source and `review.md`.  
**Done when:** This chapter meets every shared chapter completion requirement. It can be requested independently after 6A; other chapter builds are not a dependency.

### 6J. Produce chapter 9 — Reduce the impact of each journey

Build module M09, including M09-L01–M09-L04 and M09-R, using the shared chapter requirements above.

**Input:** Completed 6A and the approved content/assets for M09.  
**Deliverable:** `pdf-production/chapters/M09/chapter.pdf`, editable chapter source and `review.md`.  
**Done when:** This chapter meets every shared chapter completion requirement. It can be requested independently after 6A; other chapter builds are not a dependency.

### 6K. Produce chapter 10 — Respond, reflect and keep learning

Build module M10, including M10-L01–M10-L04 and M10-R, using the shared chapter requirements above.

**Input:** Completed 6A and the approved content/assets for M10.  
**Deliverable:** `pdf-production/chapters/M10/chapter.pdf`, editable chapter source and `review.md`.  
**Done when:** This chapter meets every shared chapter completion requirement. It can be requested independently after 6A; other chapter builds are not a dependency.

### 6L. Produce appendices, sign reference and official sources

Build appendices A–D: practical checklists, the sign reference, Swedish–English glossary and personal practice record. Include all required sign-reference groups with exact verified official images, checked captions and reuse credits. Build the official-sources section with usable links and recorded check dates. Preserve approved image size limits and the disclaimer/source treatment.

**Input:** Completed 6A, approved manuscript appendices and verified sign/reference package.  
**Deliverable:** `pdf-production/reference-material.pdf`, editable source and reference-material review.  
**Done when:** Every appendix and required sign group is covered, links/credits are checked and all rendered pages pass review with no missing required assets.

### 6M. Assemble the complete book and final navigation

Combine opening pages, all ten completed chapters, appendices and official references using the shared build source. Generate the final contents, the book’s own page numbers, bookmarks and cross-chapter/source links. Check consistent typography, spacing, illustration treatment, headers and footers across chapter boundaries.

**Input:** Completed 6A–6L and their review records.  
**Deliverable:** `pdf-production/korkortgo-curriculum-review.pdf`, complete editable source and assembly review.  
**Done when:** All 40 lessons, 10 self-assessments, appendices and references appear exactly once; final navigation resolves correctly and the combined book renders without assembly defects.

### 6N. Verify the complete PDF and submit for approval

Render and inspect the entire assembled book. Verify factual coverage and dated requirements against current official guidance, exact sign artwork, image resolution, selectable text, font embedding, reading order/accessibility, contrast, links and the learning-aid disclaimer. Confirm there are no third-party book names, borrowed chapter labels or source-book page numbers. Fix production defects and rerender affected pages; design changes still require preview approval. Save the final verification report, reproducible build instructions and release candidate.

**Input:** Completed 6M and all chapter/reference reviews.  
**Deliverable:** `pdf-production/korkortgo-curriculum.pdf`, complete editable source and `pdf-production/verification.md`.  
**Done when:** All required checks pass, no blocking issues remain and the user explicitly approves the finished PDF. Until approval, mark it “Awaiting approval”; do not start app migration.

Update [progress.md](progress.md) after each executed substep with artifact links, checks, outstanding issues and any explicit approval. Step 6 is complete only after 6A–6N meet their completion criteria.

**6N approval — 14 October 2026:** Finished tagged screen edition explicitly approved. Print masters/proof deferred by user choice. [Release identity and scope](pdf-production/final-review/screen-release.json).

## 7. Plan the app’s curriculum migration

Execute 7A–7G separately, using the saved deliverables from preceding substeps. This step prepares the migration; app previews belong to step 8 and implementation belongs to step 9. Completing a substep does not automatically start the next.

**Entry requirements:** Step 6N verification and explicit approval of the finished PDF. Use the latest approved book and its editable source, including subsequent approved content corrections. The existing [question coverage review](question-book-review/review.md) records a 578-page review book and 1,000 questions; confirm its hashes and applicability to the approved release instead of assuming the earlier 498-page assembly is current. Coverage evidence does not replace PDF approval or question-quality review.

### 7A. Freeze the approved content and audit the app

Record the approved PDF, manuscript/build source, question bank and official-source/asset registers with versions or hashes. Inspect the app's content models, loaders, bundled assets, question IDs, categories, book-page links, saved progress and bookmarks. Record where migration will affect content, navigation and persisted user data.

**Input:** Approved 6N release, app source, `content/questions.json` and existing coverage records.

**Deliverable:** `app-migration/baseline.md` and `app-migration/baseline.json` — release identity, content counts, relevant app file paths and migration constraints.

**Done when:** The exact inputs are reproducibly identified and every current content/link/persistence entry point is listed, with discrepancies or missing inputs explicit.

### 7B. Confirm stable curriculum IDs and the app content contract

Retain the existing M01–M10, Mxx-L01–Mxx-L04 and Mxx-R identifiers and exact approved titles. Register appendices, sign-reference entries and source references that need app destinations. Define the planned content fields, ordering, question relationships, asset bindings and versioning rules. Document any necessary aliases rather than silently renumbering existing IDs.

**Input:** 7A baseline, approved curriculum structure, source map and sign package.

**Deliverable:** `app-migration/curriculum-map.md` and `app-migration/curriculum-map.json` — canonical IDs, titles, order, source locations and planned app fields.

**Done when:** All 10 modules, 40 lessons, 10 reviews and required reference destinations have unique IDs and complete mappings; the content contract fits the audited app or lists the required changes.

### 7C. Map every existing practice question to teaching and sources

Preserve question IDs. Assign each question a primary lesson, related lessons/reference entries where useful, supporting approved-book passages and official references. Reuse the existing coverage evidence only when it matches the frozen inputs. Keep PDF folios as evidence; planned app links use stable curriculum IDs. Record unmatched or ambiguous questions explicitly.

**Input:** 7A question baseline, 7B curriculum map, question coverage records and official-source evidence.

**Deliverable:** `app-migration/question-map.json` and `app-migration/question-map-review.md`.

**Done when:** Every baseline question appears exactly once, every target ID resolves, and each mapping has teaching/source evidence or an explicit unresolved finding. Record coverage totals and gaps by lesson.

**Execution record — 14 October 2026:** 7C completed against the approved tagged screen release: 1,000 unique questions mapped, no unmatched/ambiguous mappings, four fuel-rounding qualifications retained for 7D. See [question-map-review.md](app-migration/question-map-review.md). 7D has not started.

### 7D. Decide which questions to retain, rewrite, replace or remove

Review prompts, options, keyed answers, explanations, calculations, sign variants and illustrations against approved teaching and official references. Distinguish teaching coverage from question quality. Carry forward the four fuel-rounding qualifications in the existing review and assess whether their prompts need clarification. Assign one disposition per question, with rationale and concrete acceptance criteria for every proposed change; do not edit the live question bank in this planning step.

**Input:** 7C map and review, frozen questions and supporting evidence.

**Deliverable:** `app-migration/question-actions.md` and `app-migration/question-actions.json` — dispositions, proposed corrections/replacement briefs, removal reasons and research holds.

**Done when:** All questions have a disposition, flagged answers and ambiguities are resolved or held explicitly, and each proposed change has a source and reviewable completion criteria.

**Execution record — 14 October 2026:** 7D planning completed: 336 retain, 626 rewrite, 38 replace and zero remove. All 1,000 IDs retained in the planning package; 38 exact-code image-delivery holds have acceptance criteria. No live questions changed. See [question-actions.md](app-migration/question-actions.md). 7E has not started.

### 7E. Plan link replacement and preservation of learner progress

Map existing categories, chapter/book-page references and navigation routes to canonical destinations. Specify handling for retired questions, stale links, bookmarks, completed lessons and question history, including aliases, fallback behaviour and version transitions. Identify learner-facing third-party book names, borrowed labels and source-book page numbers that must be replaced.

**Input:** 7A app/persistence audit, 7B curriculum IDs, 7C mappings and 7D dispositions.

**Deliverable:** `app-migration/link-and-progress-map.md` and `app-migration/link-and-progress-map.json`.

**Done when:** Every audited legacy reference and saved-data field has a migration rule, unresolved destinations are listed, and concrete before/after examples cover retained, changed and retired content.

**Execution record — 14 October 2026:** 7E planning completed with all audited legacy references/state covered, exact question routes, chapter/topic aliases and explicit version/fallback rules. SIG16–18 lack exact approved destinations and have recorded gap policies for 7F. No live app/question/storage changes. See [link-and-progress-map.md](app-migration/link-and-progress-map.md). 7F has not started.

### 7F. Prepare the implementation backlog and app-preview handoff

List bounded step 9 work items for content import, model/loader changes, question updates, route replacement, progress migration, official sources and verified assets. Give each item dependencies, affected files, outputs and acceptance checks. Prepare representative library, lesson-reader and answer-review content for step 8, including source/reference and legacy-link cases. Specify verification cases for step 10 without creating or implementing a new visual design.

**Input:** All 7A–7E records.

**Deliverable:** `app-migration/implementation-backlog.md` and `app-migration/preview-handoff.md`.

**Done when:** Every planned content/data change has an executable work item and verification criteria; step 8 has exact representative content and constraints. Any new app design still requires imagegen previews and explicit approval before implementation.

**Execution record — 14 October 2026:** 7F completed: 15 dependency-ordered implementation work items, exhaustive per-question assignments and bounded batches, ten future verification cases and exact library/reader/answer-review/source/legacy fixtures. SIG16–18 retain explicit unavailable internal routes with recorded official-source and related-teaching actions; no new sign entries approved. All 68 local handoff checks pass, including frozen-input/asset hashes and byte-identical regeneration. No live app/question/asset/PDF changes or design previews. See [implementation-backlog.md](app-migration/implementation-backlog.md) and [preview-handoff.md](app-migration/preview-handoff.md). 7G has not started.

### 7G. Verify the migration package and update progress

Cross-check baseline counts/hashes, unique curriculum and question IDs, complete question dispositions, valid destinations, official references, asset bindings, persistence rules and backlog coverage. Save machine-readable results and a human-readable review; list unresolved research, content or migration blockers.

**Input:** All 7A–7F deliverables.

**Deliverable:** `app-migration/verification.md`, `app-migration/verification.json` and updated [progress tracker](progress.md).

**Done when:** All baseline questions are accounted for, required destinations and references resolve, every action is covered by the backlog and no blocking migration-planning issues remain. Otherwise keep step 7 in progress and identify the substep that must be revisited.

**Execution record — 14 October 2026:** 7G passed; step 7 planning is complete. Fresh 7C–7F acceptance runs and 60 cross-stage checks pass: all 1,000 baseline question IDs, 1,123 unique published destinations, source/asset bindings, learner-state contracts and backlog ownership verified. No blocking migration-planning issues remain. The 38 image-delivery holds, all proposed question edits, three explicit unavailable signal routes and deferred print scope remain recorded future requirements/limits. App, live questions, assets and approved PDFs are unchanged. See [verification.md](app-migration/verification.md) and [verification.json](app-migration/verification.json). Step 8 has not started and must be requested separately; imagegen previews and explicit design approval remain required before implementation.

All step 7 deliverables are saved under `docs/curriculum/`. Update the progress tracker after each executed substep with artifact links, checks and remaining issues. This breakdown does not execute migration or mark any substep completed. Request step 8 separately after 7G passes.

## 8. Generate previews of the revised app

Execute 8A–8O separately. Each task covers one small preparation, preview or review activity. Use the saved output from its dependencies; completing a task does not automatically start the next. This breakdown only updates the plan and does not execute step 8.

**Entry requirements:** Completed 7G verification, the approved curriculum and [app-preview handoff](app-migration/preview-handoff.md), including its exact `preview-content.json` fixtures. Carry forward all content, asset and persistence constraints; design approval does not clear question-quality or image-delivery holds.

**Shared preview workflow (8B–8M):** Use the imagegen skill to generate the specified visual preview. Save the image, exact copy/asset bindings and `review.md` in the stated directory. Record feedback, revision identity, constraints and approval status. Present that preview and wait for explicit user approval before proceeding to another design task. If edits are requested, revise with imagegen and wait for approval again. Generated previews establish visual direction; exact official artwork, text rendering and accessibility behaviour require implementation verification. No app implementation occurs in step 8.

### 8A. Prepare the app-preview brief

Review the verified migration package, current app screens and exact preview fixtures. Record the visual constraints, representative content, required states and approval checklist. Do not create a new visual design in this preparation task.

**Input:** Completed 7G and the app-migration handoff.  
**Deliverable:** `app-design/brief.md`.  
**Done when:** Every required preview below has an exact fixture and a bounded scope; remaining blockers are explicit.

### 8B. Preview the learning-library overview

Use imagegen to show Learning library, 10 modules and 40 lessons, with module 3 and its four exact lesson titles and review. Include Sources and Road signs and reference actions. Preserve canonical module numbering; do not invent learner completion or bookmarks.

**Input:** 8A brief and exact library fixtures.  
**Deliverable:** `app-design/8b/` — preview images, exact content/asset notes and `review.md`.  
**Done when:** The user explicitly approves the library overview.

**Execution record — 14 October 2026:** 8B v1 explicitly approved: “Looks great, approved”. Wide/phone library direction complete; see [preview and approval record](app-design/8b/review.md). 8C has not started.

### 8C. Preview library search and filters

Use imagegen to show one filtered library state and the empty-search message “No matching lessons.” Use the five existing category labels and mapped tags. Keep lessons without primary bank questions discoverable; do not imply filters renumber modules.

**Input:** Approved 8B and library/search constraints.  
**Deliverable:** `app-design/8c/` — preview images, exact content/asset notes and `review.md`.  
**Done when:** The user explicitly approves search, filtering and the empty state.

**Execution record — 14 October 2026:** 8C v1 explicitly approved: “yes looks great, approved”. Filtered and empty-search wide/phone previews complete; see [preview and approval record](app-design/8c/review.md). 8D has not started.

### 8D. Preview the lesson-reader opening

Use imagegen to show M03-L02, Combine the instructions, with its exact goal and opening requirements paragraph. Show the module context and previous/next lesson actions. Replace book-page labels with useful lesson information.

**Input:** Approved 8B and exact M03-L02 content.  
**Deliverable:** `app-design/8d/` — preview images, exact content/asset notes and `review.md`.  
**Done when:** The user explicitly approves the reader opening and lesson navigation.

**Execution record — 14 October 2026:** 8D v1 explicitly approved: “approved”. Wide/phone lesson-reader opening complete; see [preview and approval record](app-design/8d/review.md). 8E has not started.

### 8E. Preview the lesson knowledge-check reveal

Use imagegen to show the amber-signal knowledge check before and after deliberate answer reveal. Record that hidden answers must stay outside accessibility reading before reveal.

**Input:** Approved 8D and the exact knowledge-check fixture.  
**Deliverable:** `app-design/8e/` — preview images, exact content/asset notes and `review.md`.  
**Done when:** The user explicitly approves the hidden and revealed answer states.

**Execution record — 14 October 2026:** 8E v2 explicitly approved: “approved”. Wide/phone before-and-after knowledge-check reveal previews complete; see [preview and approval record](app-design/8e/review.md). 8F has not started.

### 8F. Preview long-content and large-text reading

Use imagegen to show a focused M03-L04 reader example covering longer content, a table or calculation, and enlarged text. Record intended scrolling and wrapping behaviour without omitting approved teaching content.

**Input:** Approved 8D and exact long-content fixtures from the approved curriculum.  
**Deliverable:** `app-design/8f/` — preview images, exact content/asset notes and `review.md`.  
**Done when:** The user explicitly approves the long-content and large-text treatment; actual rendering remains a step 9–10 check.

**Execution record — 14 October 2026:** 8F v1 explicitly approved: “approved”. Long-content and enlarged-text preview direction complete; see [preview and approval record](app-design/8f/review.md). 8G has not started.

### 8G. Preview the standard answer review

Use imagegen to show the answered situation-001 fixture with exact shuffled options, selected incorrect answer, correct answer, explanation and related lesson. Record availability in both immediate and end-of-test review modes; related teaching must not bypass the unanswered-test guard.

**Input:** Approved reader direction and exact situation-001 fixture.  
**Deliverable:** `app-design/8g/` — preview images, exact content/asset notes and `review.md`.  
**Done when:** The user explicitly approves feedback and related-lesson presentation after answering.

**Execution record — 14 October 2026:** 8G v1 explicitly approved: “approved”. Wide/phone standard answer-review direction complete; see [preview and approval record](app-design/8g/review.md). 8H has not started.

### 8H. Preview the calculation answer review

Use imagegen to show the exact proposed fuel-saving-150-0.5 revision, shuffled options and 0.75-litre explanation. Mark its proposed status in review notes. Document the historical-score/version-notice compatibility case without inventing an attempt-history feature.

**Input:** Approved 8G and exact fuel fixture.  
**Deliverable:** `app-design/8h/` — preview images, exact content/asset notes and `review.md`.  
**Done when:** The user explicitly approves calculation feedback presentation; this does not accept the proposed question for live scoring.

**Execution record — 15 October 2026:** 8H v1 explicitly approved: “approved”. Calculation answer-review visual direction complete; proposed question not accepted for live scoring. See [preview and approval record](app-design/8h/review.md). 8I has not started.

### 8I. Preview the sources area

Use imagegen to show the legislation, commercial exercise-assumption and model-specific manufacturer examples from the handoff. Display their actual titles, publishers, retained dates and limitations; distinguish editorial arithmetic. Include entry from a lesson and return to the same reading position.

**Input:** Approved 8D and exact source fixtures.  
**Deliverable:** `app-design/8i/` — preview images, exact content/asset notes and `review.md`.  
**Done when:** The user explicitly approves source distinctions, detail presentation and return behaviour.

**Execution record — 15 October 2026:** 8I v1 explicitly approved: “approved”. Source-directory/detail wide/phone visual direction complete; see [preview and approval record](app-design/8i/review.md). 8J has not started.

### 8J. Preview the road-sign reference

Use imagegen to show the registered B1 study/reference entry, Swedish official name, CAP-B1 caption and editorial-English notice. Preview intended size, framing and zoom for faint outlines. Use the exact official asset when possible; otherwise mark a placement placeholder and retain the exact asset binding alongside it. Never generate replacement sign artwork.

**Input:** Approved reader direction and registered sign fixture/asset.  
**Deliverable:** `app-design/8j/` — preview images, exact content/asset notes and `review.md`.  
**Done when:** The user explicitly approves the reference layout and zoom treatment. All 38 image-delivery holds remain uncleared until actual delivery tests.

**Execution record — 15 October 2026:** 8J v1 explicitly approved: “approved”. B1 reference/framing/zoom direction complete with exact official artwork bound separately; all 38 delivery holds remain open. See [preview and approval record](app-design/8j/review.md). 8K has not started.

### 8K. Preview ambiguous and moved legacy links

Use imagegen to show the canonical destination chooser and moved-passage notice. Document the exact page-46 question-context examples using the handoff, with canonical lesson labels in learner copy. Do not imply equivalence between old folios and approved PDF pages.

**Input:** Approved library/reader direction and exact legacy fixtures.  
**Deliverable:** `app-design/8k/` — preview images, exact content/asset notes and `review.md`.  
**Done when:** The user explicitly approves chooser and moved-passage presentation, with context-specific destinations recorded.

**Execution record — 15 October 2026:** 8K chooser v2 and moved-passage v1 explicitly approved: “OK approved”. See [preview and approval record](app-design/8k/review.md). 8L has not started.

### 8L. Preview unavailable destinations

Use imagegen to show the exact SIG16–18 unavailable message, official-description action and optional Combine the instructions action. Also show the generic unavailable/library fallback. Do not substitute another signal or invent an approved internal destination.

**Input:** Approved 8K and exact unavailable fixtures.  
**Deliverable:** `app-design/8l/` — preview images, exact content/asset notes and `review.md`.  
**Done when:** The user explicitly approves both unavailable states and their recovery actions.

### 8M. Preview missing-results and setup recovery

Use imagegen to show the exact missing-results/setup fixture and its permitted recovery actions. Carry forward existing route and saved-state limitations; do not add persistence or new deep links.

**Input:** Approved visual direction and exact recovery fixture.  
**Deliverable:** `app-design/8m/` — preview images, exact content/asset notes and `review.md`.  
**Done when:** The user explicitly approves the recovery state and its actions.

### 8N. Assemble the app design specification

Index the approved preview revisions and record shared typography, colour, spacing, navigation, responsive/large-text intent, exact content bindings and accessibility requirements. Map each required handoff state to its approved preview and future implementation work item. If consolidation needs a visual change, revise the affected imagegen preview and obtain approval again.

**Input:** Approved 8B–8M previews and their review records.  
**Deliverable:** `app-design-spec.md`.  
**Done when:** Every required state has an approved revision and an implementation requirement; unresolved issues are listed.

### 8O. Verify the design package and obtain final approval

Cross-check the brief, exact fixtures, approved revisions and specification for complete library, reader, answer-review, source, reference and fallback coverage. Confirm learner copy contains no third-party book names, borrowed chapter labels or source-book folios, while preserving legitimate source publishers. Present the complete package for explicit approval.

**Input:** 8N specification and all preview/review records.  
**Deliverable:** `app-design-review.md and updated progress.md`.  
**Done when:** The user explicitly approves the complete app design package and no design blockers remain. Record approval only after it is given; step 9 still requires a separate request.

All deliverables are saved under `docs/curriculum/`. Update the [progress tracker](progress.md) after each executed substep with artifact links, approval status and outstanding issues. Step 8 is complete only after 8A–8O meet their completion criteria; implementation begins only after explicit design approval and a separate request for step 9.

## 9. Implement the approved app changes

Import the curriculum, update lesson titles and explanations, replace page-based links with lesson IDs, and update practice questions. Provide official references in a dedicated sources area.

**Deliverable:** Updated app implementing the approved curriculum and design.

## 10. Verify the finished app

Check navigation, question-to-lesson links, learning coverage, sign accuracy, and consistency with the approved PDF. Confirm that learner-facing content contains no third-party book names, original chapter labels, or source-book page numbers.

**Deliverable:** Verification report and any necessary fixes.

## Content principle

The work will use independently written material and appropriately sourced illustrations. Removing attribution alone is not the method for addressing copyright concerns.

**Book disclaimer:** Prominently state in the book’s introduction: “This material is a learning aid to help you understand Swedish driving theory. It is not an official source and cannot replace official information from Trafikverket and Transportstyrelsen. Always consult their current guidance and the applicable rules.”

## Execution

Request a step by number, for example: “Execute step 2.” For sign preparation, PDF design, chapter production, app migration planning or app previews, request a substep such as “Execute step 4A”, “Execute step 5A” or “Execute step 6B” (chapter 1), “Execute step 7A” or “Execute step 8B”. Use the saved deliverables from preceding steps and respect each approval checkpoint. Saving this plan does not start the remaining steps.


**Sequencing update — 2 October 2026:** Following the 5A blocker notice, the user directly requested execution of 5B. A limited cover/opening-page preview without sign artwork was prepared under that instruction and is [awaiting approval](pdf-design/5b/review.md). The 13 required sign gaps and 4F completion gate remain unresolved; this exception does not clear sign-dependent layouts or final PDF production.
