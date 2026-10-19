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

**Execution record — 15 October 2026:** 8L v1 explicitly approved: “approved”. Signal/generic unavailable wide/phone directions complete; see [preview and approval record](app-design/8l/review.md). 8M has not started.

### 8M. Preview missing-results and setup recovery

Use imagegen to show the exact missing-results/setup fixture and its permitted recovery actions. Carry forward existing route and saved-state limitations; do not add persistence or new deep links.

**Input:** Approved visual direction and exact recovery fixture.  
**Deliverable:** `app-design/8m/` — preview images, exact content/asset notes and `review.md`.  
**Done when:** The user explicitly approves the recovery state and its actions.

**Execution record — 15 October 2026:** 8M v1 explicitly approved: “approved”. Missing-results/setup-recovery wide/phone direction complete; see [preview and approval record](app-design/8m/review.md). 8N has not started.

### 8N. Assemble the app design specification

Index the approved preview revisions and record shared typography, colour, spacing, navigation, responsive/large-text intent, exact content bindings and accessibility requirements. Map each required handoff state to its approved preview and future implementation work item. If consolidation needs a visual change, revise the affected imagegen preview and obtain approval again.

**Input:** Approved 8B–8M previews and their review records.  
**Deliverable:** `app-design-spec.md`.  
**Done when:** Every required state has an approved revision and an implementation requirement; unresolved issues are listed.

**Execution record — 15 October 2026:** 8N consolidation complete: [design specification](app-design-spec.md) and [approved-revision index/checks](app-design/8n/package-index.json) bind twelve approval records and sixteen boards. Visual variants and future acceptance requirements remain explicit; no new visual/implementation generated. 8O has not started; complete-package approval remains pending.

### 8O. Verify the design package and obtain final approval

Cross-check the brief, exact fixtures, approved revisions and specification for complete library, reader, answer-review, source, reference and fallback coverage. Confirm learner copy contains no third-party book names, borrowed chapter labels or source-book folios, while preserving legitimate source publishers. Present the complete package for explicit approval.

**Input:** 8N specification and all preview/review records.  
**Deliverable:** `app-design-review.md and updated progress.md`.  
**Done when:** The user explicitly approves the complete app design package and no design blockers remain. Record approval only after it is given; step 9 still requires a separate request.

**Execution record — 15 October 2026:** 8O technical verification passes 681/681 checks; [complete-package review](app-design-review.md) and [results](app-design/8o/verification.json) saved. Final package approval remains pending; 8O/step 8 are not complete and step 9 has not started.

**Final package approval — 15 October 2026:** User explicitly said “yes approved”, approving the complete design package and documented dispositions. 8O and step 8 are complete; see [final approval](app-design-review.md). Implementation has not started; request step 9 separately.

All deliverables are saved under `docs/curriculum/`. Update the [progress tracker](progress.md) after each executed substep with artifact links, approval status and outstanding issues. Step 8 is complete only after 8A–8O meet their completion criteria; implementation begins only after explicit design approval and a separate request for step 9.

## 9. Implement the approved app changes

Execute the numbered tasks below separately, using their saved inputs. **9A–9O are groups matching the existing migration backlog; the executable steps are 9A1, 9A2, and so on.** A request such as “Execute step 9E3” selects one bounded task, not its entire group. Completing a task does not automatically start another. This breakdown is planning only; it does not start implementation or mark any task complete.

**Entry requirements:** Completed 7G and explicit complete-package approval in [8O](app-design-review.md), plus a separate implementation request. Recheck input identity before work: the recorded approval does not establish that today's files still match. Any new or changed visual design requires an imagegen preview and explicit approval before implementation.

**Binding inputs:** [Implementation backlog](app-migration/implementation-backlog.md), [exact assignments and batches](app-migration/implementation-backlog.json), [curriculum map](app-migration/curriculum-map.json), [question actions](app-migration/question-actions.json), [link/state contracts](app-migration/link-and-progress-map.json), [exact preview fixtures](app-migration/preview-content.json), [design specification](app-design-spec.md) and [final design dispositions](app-design-review.md). Existing backlog IDs and acceptance requirements remain valid. This section refines their execution boundaries; it does not renumber the frozen JSON or waive any requirement.

**Execution rules:**

- Each task names its dependencies, output and completion check. Dependencies need to pass before dependent work starts; unrelated tasks need not wait for alphabetically earlier groups. Within import and question batches, use the shared contract plus the current accumulated output and change only the assigned IDs.
- Save each task's exact input identities, changed files/IDs, commands, observed checks and blockers in `docs/curriculum/app-migration/implementation-evidence/<step-id>/review.md`. Outputs named below are repository-relative; review filenames without a full path live in that evidence directory. These are future deliverables, not files claimed to exist now.
- Update [progress.md](progress.md) after each executed task. Failed acceptance leaves the task open with a specific blocker. An evidence record must not label unrun device, source or accessibility checks as passing.
- Keep compile-time content delivery, all approved teaching and all 1,000 baseline question IDs / 500 concepts. The 336 retained assessments, 626 rewrites and 38 replacements retain their separate acceptance gates. Never silently drop held questions, weaken selection quotas or claim 1,000 active questions before acceptance.
- Preserve source scope, exact official artwork, both feedback modes and existing transient-state behaviour. New persistence, completion/bookmark/history features, hot replacement, public deep-link schemes and additional scored questions remain outside this implementation.

### 9A. Establish the input and generation boundary

#### 9A1. Freeze and check the approved inputs

Compare current app, questions, manuscript, production corrections, registries, assets and design approvals with the retained manifests. Record any changed inputs and the affected audit that must be refreshed.

**Input:** 7G evidence, 8O approval and current repository files.

**Output:** input-baseline.json and readiness.md.

**Done when:** All required input identities match or have an explicitly refreshed review; unresolved drift blocks dependent implementation.

**Execution record — 15 October 2026:** 9A1 completed; current inputs match the retained migration/design/release identities and final design approval is recorded. See [frozen baseline](app-migration/implementation-evidence/9A1/input-baseline.json), [readiness](app-migration/implementation-evidence/9A1/readiness.md) and [review](app-migration/implementation-evidence/9A1/review.md). No app/content migration performed; 9A2 requires a separate request.

#### 9A2. Define the typed content contract

Define canonical IDs, block variants, answer visibility, source/asset bindings, question and option identities, semantic revisions and eligibility. Separate curriculum release identity from app version.

**Input:** 9A1 and the 7B–7E contracts.

**Output:** Typed models in Curriculum.kt / Quiz.kt and a documented content/manifest schema.

**Done when:** The contract represents every approved block and state without a runtime JSON loader or new persistence.

**Execution record — 15 October 2026:** 9A2 completed: common Kotlin content/assessment models and the [documented schema](app-migration/implementation-evidence/9A2/content-contract.md) define complete block/answer/source/asset/version/eligibility contracts. Final desktop/common compilation and all 11 tests pass; the original live quiz code/data remains intact. See [review](app-migration/implementation-evidence/9A2/review.md) and [verification](app-migration/implementation-evidence/9A2/verification.json). No runtime import/UI migration performed; 9A3 requires a separate request.

#### 9A3. Implement deterministic generation and validation

Extend tools/build_content.py to validate the contract and emit Kotlin plus source-to-output locators to explicit paths. Start with a small exact fixture.

**Input:** 9A2 models and representative approved content/source/asset fixtures.

**Output:** Generator changes, fixture output and validation checks.

**Done when:** Repeated generation is byte-identical; duplicate IDs, unknown bindings and invalid option identities fail with useful errors.

**Execution record — 15 October 2026:** 9A3 completed: explicit schema-1 compile entrypoint, frozen-source validation, bounded Kotlin constructor generation and source/output trace implemented. All 44 compiler tests and 12 configured Kotlin/desktop tests pass; repeated fixture outputs are byte-identical. The [saved fixture](app-migration/implementation-evidence/9A3/README.md) is unscored and partial; the live bank/assets remain unchanged. See [review](app-migration/implementation-evidence/9A3/review.md) and [verification](app-migration/implementation-evidence/9A3/verification.json). 9B1 requires a separate request.

### 9B. Import the approved teaching

Use 9A3 for every import. Generated payload constructors use `GeneratedCurriculum.kt` and numbered parts in an explicit staging/build directory; `Curriculum.kt` retains the handwritten models. Preserve exact approved text/order, complete blocks, origin locators and final production corrections. Import tasks produce data, not screen designs; unresolved cross-import references are tracked until 9B17.

#### 9B1. Import introductions and reading structure

Import approved introductory content, the learning-aid disclaimer and the 60-node reading-order skeleton. Keep supporting/front-matter anchors out of top-level cards where required.

**Input:** 9A3 and approved production sources / 7B structure.

**Output:** Opening content and canonical reading-order records in content/curriculum.json and staged GeneratedCurriculum.kt/parts.

**Done when:** Titles, order, disclaimer and origin locators match the approved sources.

**Execution record — 15 October 2026:** 9B1 completed: approved opening text/disclaimer and all 60 reading records imported into [content/curriculum.json](../../content/curriculum.json), with a [pending-import ledger](../../content/curriculum-import-state.json). Four front-matter destinations remain outside module cards/reading order. All 86 checks and 14 configured Kotlin/desktop tests pass; all opening text matches the approved PDF and generation is byte-identical. See [review](app-migration/implementation-evidence/9B1/review.md) and [verification](app-migration/implementation-evidence/9B1/verification.json). The sixty chapter bodies remain pending; 9B2 requires a separate request.

#### 9B2. Import module M01

Import only M01: its introduction, four complete lessons and module review, including tables, examples, checks, hidden answers, illustrations and scoped references.

**Input:** 9B1, M01 production sources/corrections, placements and 7B records.

**Output:** M01 records in content/curriculum.json, generated Kotlin and module-parity.json.

**Done when:** Normalized block-by-block comparison passes; no teaching is truncated or replaced by legacy summaries. Preserve the limited 1177 scope wherever present.

**Execution record — 15 October 2026:** 9B2 completed: M01 introduction, four full lessons and review imported into the cumulative payload, with five hidden answers, four approved illustration windows and sixteen scoped sources. All 216 normalized source/PDF parity checks, 59 Python regression tests and 14 configured Kotlin/desktop tests pass; fresh/repeated Kotlin generation is byte-identical. Other 58 documents remain unchanged and 54 reading bodies remain pending. See [review](app-migration/implementation-evidence/9B2/review.md), [module parity](app-migration/implementation-evidence/9B2/module-parity.json) and [reproduction notes](app-migration/implementation-evidence/9B2/README.md). Asset delivery/source-directory/runtime work remains assigned later steps. 9B3 requires a separate request.

#### 9B3. Import module M02

Import only M02: its introduction, four complete lessons and module review, including tables, examples, checks, hidden answers, illustrations and scoped references.

**Input:** 9B1, M02 production sources/corrections, placements and 7B records.

**Output:** M02 records in content/curriculum.json, generated Kotlin and module-parity.json.

**Done when:** Normalized block-by-block comparison passes; no teaching is truncated or replaced by legacy summaries. Preserve the limited 1177 scope wherever present.

**Execution record — 15 October 2026:** 9B3 completed: M02 introduction, four full lessons and review imported with 46 source blocks, the complete symptom/action table, five hidden answers, six illustration bindings (including two approved polygon masks) and nineteen source scopes. All 243 source/PDF parity checks, 74 Python regression tests and 15 configured Kotlin/desktop tests pass; generated Kotlin/trace is byte-identical. Other 58 documents and all M01 bindings remain unchanged; 48 reading bodies remain pending. See [review](app-migration/implementation-evidence/9B3/review.md), [module parity](app-migration/implementation-evidence/9B3/module-parity.json) and [reproduction notes](app-migration/implementation-evidence/9B3/README.md). Resource delivery/source-directory/runtime work remains later. 9B4 requires a separate request.

#### 9B4. Import module M03

Import only M03: its introduction, four complete lessons and module review, including tables, examples, checks, hidden answers, illustrations and scoped references.

**Input:** 9B1, M03 production sources/corrections, placements and 7B records.

**Output:** M03 records in content/curriculum.json, generated Kotlin and module-parity.json.

**Done when:** Normalized block-by-block comparison passes; no teaching is truncated or replaced by legacy summaries. Preserve the limited 1177 scope wherever present.

**Execution record — 15 October 2026:** 9B4 completed. Completed in the authorized remaining-9B batch, with complete production text/structure, source origins, canonical links and approved artwork bindings. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9B4 evidence](app-migration/implementation-evidence/9B4/module-parity.json), [review](app-migration/implementation-evidence/9B4/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9B5. Import module M04

Import only M04: its introduction, four complete lessons and module review, including tables, examples, checks, hidden answers, illustrations and scoped references.

**Input:** 9B1, M04 production sources/corrections, placements and 7B records.

**Output:** M04 records in content/curriculum.json, generated Kotlin and module-parity.json.

**Done when:** Normalized block-by-block comparison passes; no teaching is truncated or replaced by legacy summaries. Preserve the limited 1177 scope wherever present.

**Execution record — 15 October 2026:** 9B5 completed. Completed in the authorized remaining-9B batch, with complete production text/structure, source origins, canonical links and approved artwork bindings. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9B5 evidence](app-migration/implementation-evidence/9B5/module-parity.json), [review](app-migration/implementation-evidence/9B5/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9B6. Import module M05

Import only M05: its introduction, four complete lessons and module review, including tables, examples, checks, hidden answers, illustrations and scoped references.

**Input:** 9B1, M05 production sources/corrections, placements and 7B records.

**Output:** M05 records in content/curriculum.json, generated Kotlin and module-parity.json.

**Done when:** Normalized block-by-block comparison passes; no teaching is truncated or replaced by legacy summaries. Preserve the limited 1177 scope wherever present.

**Execution record — 15 October 2026:** 9B6 completed. Completed in the authorized remaining-9B batch, with complete production text/structure, source origins, canonical links and approved artwork bindings. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9B6 evidence](app-migration/implementation-evidence/9B6/module-parity.json), [review](app-migration/implementation-evidence/9B6/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9B7. Import module M06

Import only M06: its introduction, four complete lessons and module review, including tables, examples, checks, hidden answers, illustrations and scoped references.

**Input:** 9B1, M06 production sources/corrections, placements and 7B records.

**Output:** M06 records in content/curriculum.json, generated Kotlin and module-parity.json.

**Done when:** Normalized block-by-block comparison passes; no teaching is truncated or replaced by legacy summaries. Preserve the limited 1177 scope wherever present.

**Execution record — 15 October 2026:** 9B7 completed. Completed in the authorized remaining-9B batch, with complete production text/structure, source origins, canonical links and approved artwork bindings. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9B7 evidence](app-migration/implementation-evidence/9B7/module-parity.json), [review](app-migration/implementation-evidence/9B7/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9B8. Import module M07

Import only M07: its introduction, four complete lessons and module review, including tables, examples, checks, hidden answers, illustrations and scoped references.

**Input:** 9B1, M07 production sources/corrections, placements and 7B records.

**Output:** M07 records in content/curriculum.json, generated Kotlin and module-parity.json.

**Done when:** Normalized block-by-block comparison passes; no teaching is truncated or replaced by legacy summaries. Preserve the limited 1177 scope wherever present.

**Execution record — 15 October 2026:** 9B8 completed. Completed in the authorized remaining-9B batch, with complete production text/structure, source origins, canonical links and approved artwork bindings. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9B8 evidence](app-migration/implementation-evidence/9B8/module-parity.json), [review](app-migration/implementation-evidence/9B8/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9B9. Import module M08

Import only M08: its introduction, four complete lessons and module review, including tables, examples, checks, hidden answers, illustrations and scoped references.

**Input:** 9B1, M08 production sources/corrections, placements and 7B records.

**Output:** M08 records in content/curriculum.json, generated Kotlin and module-parity.json.

**Done when:** Normalized block-by-block comparison passes; no teaching is truncated or replaced by legacy summaries. Preserve the limited 1177 scope wherever present.

**Execution record — 15 October 2026:** 9B9 completed. Completed in the authorized remaining-9B batch, with complete production text/structure, source origins, canonical links and approved artwork bindings. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9B9 evidence](app-migration/implementation-evidence/9B9/module-parity.json), [review](app-migration/implementation-evidence/9B9/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9B10. Import module M09

Import only M09: its introduction, four complete lessons and module review, including tables, examples, checks, hidden answers, illustrations and scoped references.

**Input:** 9B1, M09 production sources/corrections, placements and 7B records.

**Output:** M09 records in content/curriculum.json, generated Kotlin and module-parity.json.

**Done when:** Normalized block-by-block comparison passes; no teaching is truncated or replaced by legacy summaries. Preserve the limited 1177 scope wherever present.

**Execution record — 15 October 2026:** 9B10 completed. Completed in the authorized remaining-9B batch, with complete production text/structure, source origins, canonical links and approved artwork bindings. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9B10 evidence](app-migration/implementation-evidence/9B10/module-parity.json), [review](app-migration/implementation-evidence/9B10/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9B11. Import module M10

Import only M10: its introduction, four complete lessons and module review, including tables, examples, checks, hidden answers, illustrations and scoped references.

**Input:** 9B1, M10 production sources/corrections, placements and 7B records.

**Output:** M10 records in content/curriculum.json, generatBamBuser24624_ed Kotlin and module-parity.json.

**Done when:** Normalized block-by-block comparison passes; no teaching is truncated or replaced by legacy summaries. Preserve the limited 1177 scope wherever present.

**Execution record — 15 October 2026:** 9B11 completed. Completed in the authorized remaining-9B batch, with complete production text/structure, source origins, canonical links and approved artwork bindings. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9B11 evidence](app-migration/implementation-evidence/9B11/module-parity.json), [review](app-migration/implementation-evidence/9B11/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9B12. Import appendix 1

Import only the 1th appendix in the approved canonical order, including its tables, source links and supporting anchors.

**Input:** 9B1 and the exact appendix production sources / 7B records.

**Output:** Appendix records in content/curriculum.json, generated Kotlin and appendix-parity.json.

**Done when:** Every approved appendix block and origin is retained, with no invented titles or destinations.

**Execution record — 15 October 2026:** 9B12 completed. Completed in the authorized remaining-9B batch, with complete production text/structure, source origins, canonical links and approved artwork bindings. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9B12 evidence](app-migration/implementation-evidence/9B12/appendix-parity.json), [review](app-migration/implementation-evidence/9B12/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9B13. Import appendix 2

Import only the 2th appendix in the approved canonical order, including its tables, source links and supporting anchors.

**Input:** 9B1 and the exact appendix production sources / 7B records.

**Output:** Appendix records in content/curriculum.json, generated Kotlin and appendix-parity.json.

**Done when:** Every approved appendix block and origin is retained, with no invented titles or destinations.

**Execution record — 15 October 2026:** 9B13 completed. Completed in the authorized remaining-9B batch, with complete production text/structure, source origins, canonical links and approved artwork bindings. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9B13 evidence](app-migration/implementation-evidence/9B13/appendix-parity.json), [review](app-migration/implementation-evidence/9B13/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9B14. Import appendix 3

Import only the 3th appendix in the approved canonical order, including its tables, source links and supporting anchors.

**Input:** 9B1 and the exact appendix production sources / 7B records.

**Output:** Appendix records in content/curriculum.json, generated Kotlin and appendix-parity.json.

**Done when:** Every approved appendix block and origin is retained, with no invented titles or destinations.

**Execution record — 15 October 2026:** 9B14 completed. Completed in the authorized remaining-9B batch, with complete production text/structure, source origins, canonical links and approved artwork bindings. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9B14 evidence](app-migration/implementation-evidence/9B14/appendix-parity.json), [review](app-migration/implementation-evidence/9B14/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9B15. Import appendix 4

Import only the 4th appendix in the approved canonical order, including its tables, source links and supporting anchors.

**Input:** 9B1 and the exact appendix production sources / 7B records.

**Output:** Appendix records in content/curriculum.json, generated Kotlin and appendix-parity.json.

**Done when:** Every approved appendix block and origin is retained, with no invented titles or destinations.

**Execution record — 15 October 2026:** 9B15 completed. Completed in the authorized remaining-9B batch, with complete production text/structure, source origins, canonical links and approved artwork bindings. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9B15 evidence](app-migration/implementation-evidence/9B15/appendix-parity.json), [review](app-migration/implementation-evidence/9B15/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9B16. Import reference-group structure

Import the 24 reference groups and their canonical membership/order; bind sign and source IDs without duplicating their payloads.

**Input:** 9B1 and approved reference-section production sources / 7B registry.

**Output:** Reference-group records and generated Kotlin.

**Done when:** All 24 groups match the approved structure and every member has an explicit registry binding.

**Execution record — 15 October 2026:** 9B16 completed. Completed in the authorized remaining-9B batch, with complete production text/structure, source origins, canonical links and approved artwork bindings. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9B16 evidence](app-migration/implementation-evidence/9B16/reference-group-parity.json), [review](app-migration/implementation-evidence/9B16/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9B17. Check complete import parity

Cross-check all teaching, reference groups and supporting anchors, including the page-193 wildlife correction. Report missing or duplicate blocks.

**Input:** 9B1–9B16 and completed 9C1–9C4.

**Output:** import-parity.json and review.md.

**Done when:** All 1,123 published destinations resolve uniquely: 88 curriculum, 400 signs, 116 sources and 519 supporting anchors; full production-source parity passes.

**Execution record — 15 October 2026:** 9B17 completed. Completed in the authorized remaining-9B batch, with complete production text/structure, source origins, canonical links and approved artwork bindings. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9B17 evidence](app-migration/implementation-evidence/9B17/import-parity.json), [review](app-migration/implementation-evidence/9B17/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

### 9C. Import source records and verified artwork

#### 9C1. Import scoped source metadata

Import the 116 source destinations and 404 question URL records. Retain exact URLs, publishers, classifications, dates, module-specific choices and scope limitations.

**Input:** 9A3 and retained 7B/7C source evidence.

**Output:** content/sources.json and generated source records.

**Done when:** All records resolve; commercial, manufacturer, foreign, research and editorial material is accurately labelled and unknown dates remain explicit.

**Execution record — 15 October 2026:** 9C1 completed. Completed as an explicit prerequisite of the user-authorized 9B17; source/caption records and exact bundled artwork identities are retained. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9C1 evidence](app-migration/implementation-evidence/9C1/source-import.json), [review](app-migration/implementation-evidence/9C1/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9C2. Import sign captions and bindings

Import the 400 exact sign/code/variant bindings, official Swedish names, captions, editorial-English notices and reuse/credit records.

**Input:** 9A3, verified sign manifest/captions and 7B registry.

**Output:** Sign metadata in content/curriculum.json and generated Kotlin.

**Done when:** Every registered sign has the correct caption, code/variant and asset hash; case-sensitive F31a is preserved.

**Execution record — 15 October 2026:** 9C2 completed. Completed as an explicit prerequisite of the user-authorized 9B17; source/caption records and exact bundled artwork identities are retained. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9C2 evidence](app-migration/implementation-evidence/9C2/sign-import.json), [review](app-migration/implementation-evidence/9C2/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9C3. Bundle the official sign files

Copy the verified files into composeApp/src/commonMain/composeResources/files/curriculum/ and bind resource paths without changing artwork.

**Input:** 9C2 and verified source asset files.

**Output:** Bundled sign files and asset manifest entries.

**Done when:** Bundled hashes equal approved hashes; no missing files, geometry changes or generated replacements exist.

**Execution record — 15 October 2026:** 9C3 completed. Completed as an explicit prerequisite of the user-authorized 9B17; source/caption records and exact bundled artwork identities are retained. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9C3 evidence](app-migration/implementation-evidence/9C3/asset-parity.json), [review](app-migration/implementation-evidence/9C3/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

#### 9C4. Bundle lesson illustrations

Copy approved contextual illustrations and bind their captions, accessibility text, credits and lesson placements.

**Input:** 9A3, approved illustration files and placement records.

**Output:** Bundled lesson illustrations and manifest/placement entries.

**Done when:** All required placements resolve to approved bytes and retained reuse evidence; missing or unapproved illustrations remain blockers.

**Execution record — 15 October 2026:** 9C4 completed. Completed as an explicit prerequisite of the user-authorized 9B17; source/caption records and exact bundled artwork identities are retained. The cumulative package resolves all 1,123 destinations; all 2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. See [9C4 evidence](app-migration/implementation-evidence/9C4/illustration-parity.json), [review](app-migration/implementation-evidence/9C4/review.md) and [shared generated package/reproduction](app-migration/implementation-evidence/9B17/README.md). Assessment/release/device acceptance remains later work.

### 9D. Implement assessment identity and neutral descriptions

Description batches below select the exact execution_batches entry by work_item_id = 9D and batch number in implementation-backlog.json. Each covers at most 50 question IDs. Reused asset descriptions may be shared, but every assigned stem and option must be checked in context; study captions must never substitute for neutral assessment descriptions.

#### 9D1. Add stable question and option identity

Use authored option IDs and semantic question revisions through generation, shuffle, selection and scoring; derive display letters after shuffling.

**Input:** 9A3, 9C2 and current question/quiz models.

**Output:** Quiz.kt / generator identity changes and focused shuffle/key checks.

**Done when:** All four display positions preserve the correct key and per-option feedback; uniqueness checks use identities and distinct assets rather than code-bearing labels.

**Execution record — 16 October 2026:** 9D1 completed. Added executable assessment selection, authored-ID shuffling/confirmation/scoring and semantic-revision snapshots; generator validation binds option IDs to reviewed assignments. The saved ledger covers all 1,000 baseline questions and 4,000 options. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D1 evidence](app-migration/implementation-evidence/9D1/authored-identities.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

#### 9D2. Implement pre-answer image and feedback semantics

Implement neutral image-description fields and answer-gated feedback semantics in the assessment components. Keep code/meaning metadata out of pre-answer accessibility reading.

**Input:** 9D1, 9C3 and approved assessment/review requirements.

**Output:** Assessment component changes and hidden/revealed semantic checks.

**Done when:** Both feedback modes enforce their reveal boundary with keyboard/focus and assistive-reading order preserved.

**Execution record — 16 October 2026:** 9D2 completed. Added gated assessment presentation/component semantics, enforced neutral image descriptions and keyboard/focus handoff. Actual Compose semantics and Space/Tab/Enter tests pass for immediate and end feedback. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D2 evidence](app-migration/implementation-evidence/9D2/reviewed-descriptions.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

#### 9D3. Review neutral descriptions — batch 1

Author or reuse and review physical descriptions for every stem/option image used by the 50 assigned questions; inspect actual images and record per-ID results.

**Input:** 9D2, 9C3 and backlog 9D batch 1 (sign-meaning-A1 through sign-recognise-A25; JSON list is authoritative).

**Output:** Reviewed description records and description-acceptance.json for this batch.

**Done when:** Descriptions identify visible features without leaking the correct meaning or target/option codes; every assigned image has review evidence.

**Execution record — 16 October 2026:** 9D3 completed. Reviewed all 50 assigned questions against exact proposed stems/options and visible assets; per-ID acceptance binds physical descriptions to exact hashes and visual evidence. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D3 evidence](app-migration/implementation-evidence/9D3/description-acceptance.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

#### 9D4. Review neutral descriptions — batch 2

Author or reuse and review physical descriptions for every stem/option image used by the 50 assigned questions; inspect actual images and record per-ID results.

**Input:** 9D2, 9C3 and backlog 9D batch 2 (sign-meaning-A26 through sign-recognise-C1; JSON list is authoritative).

**Output:** Reviewed description records and description-acceptance.json for this batch.

**Done when:** Descriptions identify visible features without leaking the correct meaning or target/option codes; every assigned image has review evidence.

**Execution record — 16 October 2026:** 9D4 completed. Reviewed all 50 assigned questions against exact proposed stems/options and visible assets; per-ID acceptance binds physical descriptions to exact hashes and visual evidence. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D4 evidence](app-migration/implementation-evidence/9D4/description-acceptance.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

#### 9D5. Review neutral descriptions — batch 3

Author or reuse and review physical descriptions for every stem/option image used by the 50 assigned questions; inspect actual images and record per-ID results.

**Input:** 9D2, 9C3 and backlog 9D batch 3 (sign-meaning-C2 through sign-recognise-C26; JSON list is authoritative).

**Output:** Reviewed description records and description-acceptance.json for this batch.

**Done when:** Descriptions identify visible features without leaking the correct meaning or target/option codes; every assigned image has review evidence.

**Execution record — 16 October 2026:** 9D5 completed. Reviewed all 50 assigned questions against exact proposed stems/options and visible assets; per-ID acceptance binds physical descriptions to exact hashes and visual evidence. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D5 evidence](app-migration/implementation-evidence/9D5/description-acceptance.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

#### 9D6. Review neutral descriptions — batch 4

Author or reuse and review physical descriptions for every stem/option image used by the 50 assigned questions; inspect actual images and record per-ID results.

**Input:** 9D2, 9C3 and backlog 9D batch 4 (sign-meaning-C27 through sign-recognise-D5; JSON list is authoritative).

**Output:** Reviewed description records and description-acceptance.json for this batch.

**Done when:** Descriptions identify visible features without leaking the correct meaning or target/option codes; every assigned image has review evidence.

**Execution record — 16 October 2026:** 9D6 completed. Reviewed all 50 assigned questions against exact proposed stems/options and visible assets; per-ID acceptance binds physical descriptions to exact hashes and visual evidence. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D6 evidence](app-migration/implementation-evidence/9D6/description-acceptance.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

#### 9D7. Review neutral descriptions — batch 5

Author or reuse and review physical descriptions for every stem/option image used by the 50 assigned questions; inspect actual images and record per-ID results.

**Input:** 9D2, 9C3 and backlog 9D batch 5 (sign-meaning-D6 through sign-recognise-E18; JSON list is authoritative).

**Output:** Reviewed description records and description-acceptance.json for this batch.

**Done when:** Descriptions identify visible features without leaking the correct meaning or target/option codes; every assigned image has review evidence.

**Execution record — 16 October 2026:** 9D7 completed. Reviewed all 50 assigned questions against exact proposed stems/options and visible assets; per-ID acceptance binds physical descriptions to exact hashes and visual evidence. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D7 evidence](app-migration/implementation-evidence/9D7/description-acceptance.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

#### 9D8. Review neutral descriptions — batch 6

Author or reuse and review physical descriptions for every stem/option image used by the 50 assigned questions; inspect actual images and record per-ID results.

**Input:** 9D2, 9C3 and backlog 9D batch 6 (sign-meaning-E19 through sign-recognise-F10; JSON list is authoritative).

**Output:** Reviewed description records and description-acceptance.json for this batch.

**Done when:** Descriptions identify visible features without leaking the correct meaning or target/option codes; every assigned image has review evidence.

**Execution record — 16 October 2026:** 9D8 completed. Reviewed all 50 assigned questions against exact proposed stems/options and visible assets; per-ID acceptance binds physical descriptions to exact hashes and visual evidence. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D8 evidence](app-migration/implementation-evidence/9D8/description-acceptance.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

#### 9D9. Review neutral descriptions — batch 7

Author or reuse and review physical descriptions for every stem/option image used by the 50 assigned questions; inspect actual images and record per-ID results.

**Input:** 9D2, 9C3 and backlog 9D batch 7 (sign-meaning-F11 through sign-recognise-F34; JSON list is authoritative).

**Output:** Reviewed description records and description-acceptance.json for this batch.

**Done when:** Descriptions identify visible features without leaking the correct meaning or target/option codes; every assigned image has review evidence.

**Execution record — 16 October 2026:** 9D9 completed. Reviewed all 50 assigned questions against exact proposed stems/options and visible assets; per-ID acceptance binds physical descriptions to exact hashes and visual evidence. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D9 evidence](app-migration/implementation-evidence/9D9/description-acceptance.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

#### 9D10. Review neutral descriptions — batch 8

Author or reuse and review physical descriptions for every stem/option image used by the 50 assigned questions; inspect actual images and record per-ID results.

**Input:** 9D2, 9C3 and backlog 9D batch 8 (sign-meaning-F35 through sign-recognise-H9; JSON list is authoritative).

**Output:** Reviewed description records and description-acceptance.json for this batch.

**Done when:** Descriptions identify visible features without leaking the correct meaning or target/option codes; every assigned image has review evidence.

**Execution record — 16 October 2026:** 9D10 completed. Reviewed all 50 assigned questions against exact proposed stems/options and visible assets; per-ID acceptance binds physical descriptions to exact hashes and visual evidence. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D10 evidence](app-migration/implementation-evidence/9D10/description-acceptance.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

#### 9D11. Review neutral descriptions — batch 9

Author or reuse and review physical descriptions for every stem/option image used by the 50 assigned questions; inspect actual images and record per-ID results.

**Input:** 9D2, 9C3 and backlog 9D batch 9 (sign-meaning-H10 through sign-recognise-J3; JSON list is authoritative).

**Output:** Reviewed description records and description-acceptance.json for this batch.

**Done when:** Descriptions identify visible features without leaking the correct meaning or target/option codes; every assigned image has review evidence.

**Execution record — 16 October 2026:** 9D11 completed. Reviewed all 50 assigned questions against exact proposed stems/options and visible assets; per-ID acceptance binds physical descriptions to exact hashes and visual evidence. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D11 evidence](app-migration/implementation-evidence/9D11/description-acceptance.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

#### 9D12. Review neutral descriptions — batch 10

Author or reuse and review physical descriptions for every stem/option image used by the 50 assigned questions; inspect actual images and record per-ID results.

**Input:** 9D2, 9C3 and backlog 9D batch 10 (sign-meaning-M1 through sign-recognise-M24; JSON list is authoritative).

**Output:** Reviewed description records and description-acceptance.json for this batch.

**Done when:** Descriptions identify visible features without leaking the correct meaning or target/option codes; every assigned image has review evidence.

**Execution record — 16 October 2026:** 9D12 completed. Reviewed all 50 assigned questions against exact proposed stems/options and visible assets; per-ID acceptance binds physical descriptions to exact hashes and visual evidence. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D12 evidence](app-migration/implementation-evidence/9D12/description-acceptance.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

#### 9D13. Review neutral descriptions — batch 11

Author or reuse and review physical descriptions for every stem/option image used by the 50 assigned questions; inspect actual images and record per-ID results.

**Input:** 9D2, 9C3 and backlog 9D batch 11 (sign-meaning-M25 through sign-recognise-T2; JSON list is authoritative).

**Output:** Reviewed description records and description-acceptance.json for this batch.

**Done when:** Descriptions identify visible features without leaking the correct meaning or target/option codes; every assigned image has review evidence.

**Execution record — 16 October 2026:** 9D13 completed. Reviewed all 50 assigned questions against exact proposed stems/options and visible assets; per-ID acceptance binds physical descriptions to exact hashes and visual evidence. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D13 evidence](app-migration/implementation-evidence/9D13/description-acceptance.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

#### 9D14. Review neutral descriptions — batch 12

Author or reuse and review physical descriptions for every stem/option image used by the 50 assigned questions; inspect actual images and record per-ID results.

**Input:** 9D2, 9C3 and backlog 9D batch 12 (sign-meaning-T3 through sign-recognise-X2; JSON list is authoritative).

**Output:** Reviewed description records and description-acceptance.json for this batch.

**Done when:** Descriptions identify visible features without leaking the correct meaning or target/option codes; every assigned image has review evidence.

**Execution record — 16 October 2026:** 9D14 completed. Reviewed all 50 assigned questions against exact proposed stems/options and visible assets; per-ID acceptance binds physical descriptions to exact hashes and visual evidence. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D14 evidence](app-migration/implementation-evidence/9D14/description-acceptance.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

#### 9D15. Review neutral descriptions — batch 13

Author or reuse and review physical descriptions for every stem/option image used by the 16 assigned questions; inspect actual images and record per-ID results.

**Input:** 9D2, 9C3 and backlog 9D batch 13 (sign-meaning-X3 through sign-recognise-X10; JSON list is authoritative).

**Output:** Reviewed description records and description-acceptance.json for this batch.

**Done when:** Descriptions identify visible features without leaking the correct meaning or target/option codes; every assigned image has review evidence.

**Execution record — 16 October 2026:** 9D15 completed. Reviewed all 16 assigned questions against exact proposed stems/options and visible assets; per-ID acceptance binds physical descriptions to exact hashes and visual evidence. All 91 Python tests and 21 Kotlin/desktop tests pass across the group. Description acceptance does not release question/delivery holds or activate the bank. See [9D15 evidence](app-migration/implementation-evidence/9D15/description-acceptance.json) and [shared verification/reproduction](app-migration/implementation-evidence/9D1/README.md).

### 9E. Apply the 578 sign rewrites

Each task below uses the exact backlog 9E batch and changes only its IDs. Preserve question/concept IDs, apply exact 7D proposals, review all options/explanations and the overlapping distractor changes, then assign semantic revisions. Keep a per-ID before/after diff and acceptance result. The 38 held replacements belong to 9F. A rewrite using a faint-outline image as a distractor still requires that image’s delivery proof before scored activation.

#### 9E1. Apply sign rewrite batch 1 — 50 questions

Apply and check this batch only, including exact caption/source meanings and paired-direction distractor consistency.

**Input:** 9D1–9D15, 9C1–9C3 and backlog 9E batch 1 (sign-meaning-A1 through sign-recognise-A25; exact JSON list controls).

**Output:** Updated content/questions.json, generated Bank.kt and batch-acceptance.json.

**Done when:** Every assigned rewrite passes content/key/feedback checks; unresolved delivery requirements are recorded and prevent active eligibility.

**Execution record — 16 October 2026:** 9E1 completed. Applied the exact 50 A1–A25 rewrites to content/questions.json and generated Bank.kt, preserving question/concept/option IDs and assigning `rewrite-r2`. Reviewed all options/explanations, 12 overlapping distractor-change records and 125 exact artwork/neutral-description bindings. The other 950 question rows are unchanged. Full typed package checks, 98 Python tests and 23 Kotlin/desktop tests pass. All 50 rewrites remain delivery-held and are excluded from both legacy and new scored selection; 9L/9O delivery/integration acceptance is still required. See [per-ID before/after and acceptance](app-migration/implementation-evidence/9E1/batch-acceptance.json), [review](app-migration/implementation-evidence/9E1/review.md) and [reproduction](app-migration/implementation-evidence/9E1/README.md).

#### 9E2. Apply sign rewrite batch 2 — 50 questions

Apply and check this batch only, including exact caption/source meanings and paired-direction distractor consistency.

**Input:** 9D1–9D15, 9C1–9C3 and backlog 9E batch 2 (sign-meaning-A26 through sign-recognise-C1; exact JSON list controls).

**Output:** Updated content/questions.json, generated Bank.kt and batch-acceptance.json.

**Done when:** Every assigned rewrite passes content/key/feedback checks; unresolved delivery requirements are recorded and prevent active eligibility.

**Execution record — 16 October 2026:** 9E2 completed. Applied the exact 50 backlog rewrites with stable authored identity, `rewrite-r2`, exact 7D content/key/feedback and reviewed 9D artwork/description bindings. Other question records are unchanged at this batch boundary. Content checks pass; all assigned rewrites remain delivery-held and excluded from scoring. [Per-ID acceptance and diff](app-migration/implementation-evidence/9E2/README.md) · [Combined package/test verification](app-migration/implementation-evidence/9E/README.md).

#### 9E3. Apply sign rewrite batch 3 — 50 questions

Apply and check this batch only, including exact caption/source meanings and paired-direction distractor consistency.

**Input:** 9D1–9D15, 9C1–9C3 and backlog 9E batch 3 (sign-meaning-C2 through sign-recognise-C26; exact JSON list controls).

**Output:** Updated content/questions.json, generated Bank.kt and batch-acceptance.json.

**Done when:** Every assigned rewrite passes content/key/feedback checks; unresolved delivery requirements are recorded and prevent active eligibility.

**Execution record — 16 October 2026:** 9E3 completed. Applied the exact 50 backlog rewrites with stable authored identity, `rewrite-r2`, exact 7D content/key/feedback and reviewed 9D artwork/description bindings. Other question records are unchanged at this batch boundary. Content checks pass; all assigned rewrites remain delivery-held and excluded from scoring. [Per-ID acceptance and diff](app-migration/implementation-evidence/9E3/README.md) · [Combined package/test verification](app-migration/implementation-evidence/9E/README.md).

#### 9E4. Apply sign rewrite batch 4 — 50 questions

Apply and check this batch only, including exact caption/source meanings and paired-direction distractor consistency.

**Input:** 9D1–9D15, 9C1–9C3 and backlog 9E batch 4 (sign-meaning-C27 through sign-recognise-D5; exact JSON list controls).

**Output:** Updated content/questions.json, generated Bank.kt and batch-acceptance.json.

**Done when:** Every assigned rewrite passes content/key/feedback checks; unresolved delivery requirements are recorded and prevent active eligibility.

**Execution record — 16 October 2026:** 9E4 completed. Applied the exact 50 backlog rewrites with stable authored identity, `rewrite-r2`, exact 7D content/key/feedback and reviewed 9D artwork/description bindings. Other question records are unchanged at this batch boundary. Content checks pass; all assigned rewrites remain delivery-held and excluded from scoring. [Per-ID acceptance and diff](app-migration/implementation-evidence/9E4/README.md) · [Combined package/test verification](app-migration/implementation-evidence/9E/README.md).

#### 9E5. Apply sign rewrite batch 5 — 50 questions

Apply and check this batch only, including exact caption/source meanings and paired-direction distractor consistency.

**Input:** 9D1–9D15, 9C1–9C3 and backlog 9E batch 5 (sign-meaning-D6 through sign-recognise-E18; exact JSON list controls).

**Output:** Updated content/questions.json, generated Bank.kt and batch-acceptance.json.

**Done when:** Every assigned rewrite passes content/key/feedback checks; unresolved delivery requirements are recorded and prevent active eligibility.

**Execution record — 16 October 2026:** 9E5 completed. Applied the exact 50 backlog rewrites with stable authored identity, `rewrite-r2`, exact 7D content/key/feedback and reviewed 9D artwork/description bindings. Other question records are unchanged at this batch boundary. Content checks pass; all assigned rewrites remain delivery-held and excluded from scoring. [Per-ID acceptance and diff](app-migration/implementation-evidence/9E5/README.md) · [Combined package/test verification](app-migration/implementation-evidence/9E/README.md).

#### 9E6. Apply sign rewrite batch 6 — 50 questions

Apply and check this batch only, including exact caption/source meanings and paired-direction distractor consistency.

**Input:** 9D1–9D15, 9C1–9C3 and backlog 9E batch 6 (sign-meaning-E19 through sign-recognise-F10; exact JSON list controls).

**Output:** Updated content/questions.json, generated Bank.kt and batch-acceptance.json.

**Done when:** Every assigned rewrite passes content/key/feedback checks; unresolved delivery requirements are recorded and prevent active eligibility.

**Execution record — 16 October 2026:** 9E6 completed. Applied the exact 50 backlog rewrites with stable authored identity, `rewrite-r2`, exact 7D content/key/feedback and reviewed 9D artwork/description bindings. Other question records are unchanged at this batch boundary. Content checks pass; all assigned rewrites remain delivery-held and excluded from scoring. [Per-ID acceptance and diff](app-migration/implementation-evidence/9E6/README.md) · [Combined package/test verification](app-migration/implementation-evidence/9E/README.md).

#### 9E7. Apply sign rewrite batch 7 — 50 questions

Apply and check this batch only, including exact caption/source meanings and paired-direction distractor consistency.

**Input:** 9D1–9D15, 9C1–9C3 and backlog 9E batch 7 (sign-meaning-F11 through sign-recognise-F34; exact JSON list controls).

**Output:** Updated content/questions.json, generated Bank.kt and batch-acceptance.json.

**Done when:** Every assigned rewrite passes content/key/feedback checks; unresolved delivery requirements are recorded and prevent active eligibility.

**Execution record — 16 October 2026:** 9E7 completed. Applied the exact 50 backlog rewrites with stable authored identity, `rewrite-r2`, exact 7D content/key/feedback and reviewed 9D artwork/description bindings. Other question records are unchanged at this batch boundary. Content checks pass; all assigned rewrites remain delivery-held and excluded from scoring. [Per-ID acceptance and diff](app-migration/implementation-evidence/9E7/README.md) · [Combined package/test verification](app-migration/implementation-evidence/9E/README.md).

#### 9E8. Apply sign rewrite batch 8 — 50 questions

Apply and check this batch only, including exact caption/source meanings and paired-direction distractor consistency.

**Input:** 9D1–9D15, 9C1–9C3 and backlog 9E batch 8 (sign-meaning-F35 through sign-recognise-H9; exact JSON list controls).

**Output:** Updated content/questions.json, generated Bank.kt and batch-acceptance.json.

**Done when:** Every assigned rewrite passes content/key/feedback checks; unresolved delivery requirements are recorded and prevent active eligibility.

**Execution record — 16 October 2026:** 9E8 completed. Applied the exact 50 backlog rewrites with stable authored identity, `rewrite-r2`, exact 7D content/key/feedback and reviewed 9D artwork/description bindings. Other question records are unchanged at this batch boundary. Content checks pass; all assigned rewrites remain delivery-held and excluded from scoring. [Per-ID acceptance and diff](app-migration/implementation-evidence/9E8/README.md) · [Combined package/test verification](app-migration/implementation-evidence/9E/README.md).

#### 9E9. Apply sign rewrite batch 9 — 50 questions

Apply and check this batch only, including exact caption/source meanings and paired-direction distractor consistency.

**Input:** 9D1–9D15, 9C1–9C3 and backlog 9E batch 9 (sign-meaning-H10 through sign-recognise-J3; exact JSON list controls).

**Output:** Updated content/questions.json, generated Bank.kt and batch-acceptance.json.

**Done when:** Every assigned rewrite passes content/key/feedback checks; unresolved delivery requirements are recorded and prevent active eligibility.

**Execution record — 16 October 2026:** 9E9 completed. Applied the exact 50 backlog rewrites with stable authored identity, `rewrite-r2`, exact 7D content/key/feedback and reviewed 9D artwork/description bindings. Other question records are unchanged at this batch boundary. Content checks pass; all assigned rewrites remain delivery-held and excluded from scoring. [Per-ID acceptance and diff](app-migration/implementation-evidence/9E9/README.md) · [Combined package/test verification](app-migration/implementation-evidence/9E/README.md).

#### 9E10. Apply sign rewrite batch 10 — 50 questions

Apply and check this batch only, including exact caption/source meanings and paired-direction distractor consistency.

**Input:** 9D1–9D15, 9C1–9C3 and backlog 9E batch 10 (sign-meaning-M1 through sign-recognise-M24; exact JSON list controls).

**Output:** Updated content/questions.json, generated Bank.kt and batch-acceptance.json.

**Done when:** Every assigned rewrite passes content/key/feedback checks; unresolved delivery requirements are recorded and prevent active eligibility.

**Execution record — 16 October 2026:** 9E10 completed. Applied the exact 50 backlog rewrites with stable authored identity, `rewrite-r2`, exact 7D content/key/feedback and reviewed 9D artwork/description bindings. Other question records are unchanged at this batch boundary. Content checks pass; all assigned rewrites remain delivery-held and excluded from scoring. [Per-ID acceptance and diff](app-migration/implementation-evidence/9E10/README.md) · [Combined package/test verification](app-migration/implementation-evidence/9E/README.md).

#### 9E11. Apply sign rewrite batch 11 — 50 questions

Apply and check this batch only, including exact caption/source meanings and paired-direction distractor consistency.

**Input:** 9D1–9D15, 9C1–9C3 and backlog 9E batch 11 (sign-meaning-M25 through sign-recognise-T19; exact JSON list controls).

**Output:** Updated content/questions.json, generated Bank.kt and batch-acceptance.json.

**Done when:** Every assigned rewrite passes content/key/feedback checks; unresolved delivery requirements are recorded and prevent active eligibility.

**Execution record — 16 October 2026:** 9E11 completed. Applied the exact 50 backlog rewrites with stable authored identity, `rewrite-r2`, exact 7D content/key/feedback and reviewed 9D artwork/description bindings. Other question records are unchanged at this batch boundary. Content checks pass; all assigned rewrites remain delivery-held and excluded from scoring. [Per-ID acceptance and diff](app-migration/implementation-evidence/9E11/README.md) · [Combined package/test verification](app-migration/implementation-evidence/9E/README.md).

#### 9E12. Apply sign rewrite batch 12 — 28 questions

Apply and check this batch only, including exact caption/source meanings and paired-direction distractor consistency.

**Input:** 9D1–9D15, 9C1–9C3 and backlog 9E batch 12 (sign-meaning-T20 through sign-recognise-X10; exact JSON list controls).

**Output:** Updated content/questions.json, generated Bank.kt and batch-acceptance.json.

**Done when:** Every assigned rewrite passes content/key/feedback checks; unresolved delivery requirements are recorded and prevent active eligibility.

**Execution record — 16 October 2026:** 9E12 completed. Applied the exact 28 backlog rewrites with stable authored identity, `rewrite-r2`, exact 7D content/key/feedback and reviewed 9D artwork/description bindings. Other question records are unchanged at this batch boundary. Content checks pass; all assigned rewrites remain delivery-held and excluded from scoring. [Per-ID acceptance and diff](app-migration/implementation-evidence/9E12/README.md) · [Combined package/test verification](app-migration/implementation-evidence/9E/README.md).

### 9F. Resolve faint-outline delivery holds

**Execution record — 16 October 2026:** Reviewed all 9F1–9F19 and implemented required 9K1–9K4 navigation foundations plus 9L9–9L10 reference/viewer components. User selected iOS simulator scope. Retained 76 Android captures and all 19 iOS simulator/Wasm renders; 119 Python and 39 desktop tests pass. All 38 original replacement records remain unchanged and are now excluded from scoring. Twelve small previews remain faint; reader and complete delivery acceptance remain open. These are reviewed holds, not completed acceptances. [Results, decisions and replay](app-migration/implementation-evidence/9F/README.md).

Use the approved framing/zoom implementation from 9L9–9L10. Each code task handles exactly two replacements plus occurrences of that same image in other option sets. Prove actual intended-size delivery and accessible equivalence on supported targets, light/dark surfaces and text scaling. Never thicken, recolour, redraw or substitute a similar sign; changed visual treatment requires an approved imagegen revision. Failed proof keeps the affected questions ineligible and requires an explicit content/ID decision.

#### 9F1. Prove exact S1 delivery and accept its pair

Check the exact S1 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-S1 and sign-recognise-S1 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F2. Prove exact S2 delivery and accept its pair

Check the exact S2 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-S2 and sign-recognise-S2 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F3. Prove exact S3 delivery and accept its pair

Check the exact S3 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-S3 and sign-recognise-S3 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F4. Prove exact S4 delivery and accept its pair

Check the exact S4 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-S4 and sign-recognise-S4 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F5. Prove exact S5 delivery and accept its pair

Check the exact S5 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-S5 and sign-recognise-S5 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F6. Prove exact S6 delivery and accept its pair

Check the exact S6 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-S6 and sign-recognise-S6 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F7. Prove exact S7 delivery and accept its pair

Check the exact S7 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-S7 and sign-recognise-S7 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F8. Prove exact S8 delivery and accept its pair

Check the exact S8 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-S8 and sign-recognise-S8 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F9. Prove exact S9 delivery and accept its pair

Check the exact S9 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-S9 and sign-recognise-S9 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F10. Prove exact S10 delivery and accept its pair

Check the exact S10 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-S10 and sign-recognise-S10 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F11. Prove exact S11 delivery and accept its pair

Check the exact S11 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-S11 and sign-recognise-S11 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F12. Prove exact S12 delivery and accept its pair

Check the exact S12 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-S12 and sign-recognise-S12 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F13. Prove exact S13 delivery and accept its pair

Check the exact S13 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-S13 and sign-recognise-S13 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F14. Prove exact T1 delivery and accept its pair

Check the exact T1 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-T1 and sign-recognise-T1 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F15. Prove exact T2 delivery and accept its pair

Check the exact T2 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-T2 and sign-recognise-T2 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F16. Prove exact T6 delivery and accept its pair

Check the exact T6 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-T6 and sign-recognise-T6 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F17. Prove exact T8 delivery and accept its pair

Check the exact T8 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-T8 and sign-recognise-T8 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F18. Prove exact T22 delivery and accept its pair

Check the exact T22 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-T22 and sign-recognise-T22 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

#### 9F19. Prove exact X8 delivery and accept its pair

Check the exact X8 asset at the smallest implemented size, zoom/return and equivalent access. Apply and review only sign-meaning-X8 and sign-recognise-X8 after proof passes.

**Input:** 9D1–9D15, 9C3, 9L9–9L10, the 7D hold and exact proposal for this code.

**Output:** delivery-proof.json with asset hash/platform evidence, the two revised question records and acceptance results.

**Done when:** Both directions pass content and delivery checks and every use of this asset is covered; missing target evidence leaves this task open.

### 9G. Apply the eight scenario corrections

**Execution 16 October 2026:** 9G1–9G8 applied and content-reviewed sequentially. All eight exact proposals retain IDs/concepts and original keys, with `scenario-r2` assessment metadata. [Evidence and source limitations](app-migration/implementation-evidence/9G/README.md). This does not clear 9F holds or constitute release acceptance.

For each scenario, recheck affected time-sensitive guidance against primary sources, recording verification dates and refreshing changed decisions before acceptance. Review the complete stem, four options, key and all explanations; retain IDs/concepts and assign a semantic revision.

#### 9G1. Correct situation-032 — weekday times

Apply only the exact situation-032 proposal and verify the complete resulting question.

**Input:** 9A3, 9D1, question-actions.json and current supporting primary-source evidence.

**Output:** Updated situation-032 in content/questions.json / Bank.kt and question-acceptance.json.

**Done when:** The proposal and source limits are preserved, one answer is correct and every explanation supports the revised question.

#### 9G2. Correct situation-045 — car-lighting scope

Apply only the exact situation-045 proposal and verify the complete resulting question.

**Input:** 9A3, 9D1, question-actions.json and current supporting primary-source evidence.

**Output:** Updated situation-045 in content/questions.json / Bank.kt and question-acceptance.json.

**Done when:** The proposal and source limits are preserved, one answer is correct and every explanation supports the revised question.

#### 9G3. Correct situation-105 — conditional rural return

Apply only the exact situation-105 proposal and verify the complete resulting question.

**Input:** 9A3, 9D1, question-actions.json and current supporting primary-source evidence.

**Output:** Updated situation-105 in content/questions.json / Bank.kt and question-acceptance.json.

**Done when:** The proposal and source limits are preserved, one answer is correct and every explanation supports the revised question.

#### 9G4. Correct situation-107 — emergency braking

Apply only the exact situation-107 proposal and verify the complete resulting question.

**Input:** 9A3, 9D1, question-actions.json and current supporting primary-source evidence.

**Output:** Updated situation-107 in content/questions.json / Bank.kt and question-acceptance.json.

**Done when:** The proposal and source limits are preserved, one answer is correct and every explanation supports the revised question.

#### 9G5. Correct situation-125 — prompt notification

Apply only the exact situation-125 proposal and verify the complete resulting question.

**Input:** 9A3, 9D1, question-actions.json and current supporting primary-source evidence.

**Output:** Updated situation-125 in content/questions.json / Bank.kt and question-acceptance.json.

**Done when:** The proposal and source limits are preserved, one answer is correct and every explanation supports the revised question.

#### 9G6. Correct situation-162 — ready weight

Apply only the exact situation-162 proposal and verify the complete resulting question.

**Input:** 9A3, 9D1, question-actions.json and current supporting primary-source evidence.

**Output:** Updated situation-162 in content/questions.json / Bank.kt and question-acceptance.json.

**Done when:** The proposal and source limits are preserved, one answer is correct and every explanation supports the revised question.

#### 9G7. Correct situation-172 — inspection bans

Apply only the exact situation-172 proposal and verify the complete resulting question.

**Input:** 9A3, 9D1, question-actions.json and current supporting primary-source evidence.

**Output:** Updated situation-172 in content/questions.json / Bank.kt and question-acceptance.json.

**Done when:** The proposal and source limits are preserved, one answer is correct and every explanation supports the revised question.

#### 9G8. Correct situation-178 — personal-injury cover

Apply only the exact situation-178 proposal and verify the complete resulting question.

**Input:** 9A3, 9D1, question-actions.json and current supporting primary-source evidence.

**Output:** Updated situation-178 in content/questions.json / Bank.kt and question-acceptance.json.

**Done when:** The proposal and source limits are preserved, one answer is correct and every explanation supports the revised question.

### 9H. Clarify load-question definitions

**Execution 16 October 2026:** 9H1–9H6 applied sequentially, five questions each. All 30 exact drafts use driver-inclusive tjänstevikt, retain original supplied weights and numeric keys, and have unique-answer arithmetic receipts plus `load-r2` metadata. [Evidence](app-migration/implementation-evidence/9H/README.md). Release acceptance and 9F holds remain separate.

These tasks cover the 30 exact backlog 9H IDs in six batches of five. Use the approved driver-inclusive tjänstevikt definition consistently. Independently recalculate all displayed inputs/options; retain existing numeric keys and record one-answer checks.

#### 9H1. Clarify load prompts — batch 1

Apply only these five prompt drafts: `load-1200-350`, `load-1200-450`, `load-1200-550`, `load-1350-350`, `load-1350-450`.

**Input:** 9A3, 9D1 and exact 7D drafts / source definition.

**Output:** Five revised question records, generated Bank.kt and arithmetic/acceptance evidence.

**Done when:** Driver inclusion is unambiguous, all original numeric keys remain unchanged and each revised question has exactly one correct option.

#### 9H2. Clarify load prompts — batch 2

Apply only these five prompt drafts: `load-1350-550`, `load-1500-350`, `load-1500-450`, `load-1500-550`, `load-1650-350`.

**Input:** 9A3, 9D1 and exact 7D drafts / source definition.

**Output:** Five revised question records, generated Bank.kt and arithmetic/acceptance evidence.

**Done when:** Driver inclusion is unambiguous, all original numeric keys remain unchanged and each revised question has exactly one correct option.

#### 9H3. Clarify load prompts — batch 3

Apply only these five prompt drafts: `load-1650-450`, `load-1650-550`, `load-1800-350`, `load-1800-450`, `load-1800-550`.

**Input:** 9A3, 9D1 and exact 7D drafts / source definition.

**Output:** Five revised question records, generated Bank.kt and arithmetic/acceptance evidence.

**Done when:** Driver inclusion is unambiguous, all original numeric keys remain unchanged and each revised question has exactly one correct option.

#### 9H4. Clarify load prompts — batch 4

Apply only these five prompt drafts: `load-1950-350`, `load-1950-450`, `load-1950-550`, `load-2100-350`, `load-2100-450`.

**Input:** 9A3, 9D1 and exact 7D drafts / source definition.

**Output:** Five revised question records, generated Bank.kt and arithmetic/acceptance evidence.

**Done when:** Driver inclusion is unambiguous, all original numeric keys remain unchanged and each revised question has exactly one correct option.

#### 9H5. Clarify load prompts — batch 5

Apply only these five prompt drafts: `load-2100-550`, `load-2250-350`, `load-2250-450`, `load-2250-550`, `load-2400-350`.

**Input:** 9A3, 9D1 and exact 7D drafts / source definition.

**Output:** Five revised question records, generated Bank.kt and arithmetic/acceptance evidence.

**Done when:** Driver inclusion is unambiguous, all original numeric keys remain unchanged and each revised question has exactly one correct option.

#### 9H6. Clarify load prompts — batch 6

Apply only these five prompt drafts: `load-2400-450`, `load-2400-550`, `load-2550-350`, `load-2550-450`, `load-2550-550`.

**Input:** 9A3, 9D1 and exact 7D drafts / source definition.

**Output:** Five revised question records, generated Bank.kt and arithmetic/acceptance evidence.

**Done when:** Driver inclusion is unambiguous, all original numeric keys remain unchanged and each revised question has exactly one correct option.

### 9I. Correct fuel calculations and unit wording

**Execution 16 October 2026:** 9I1–9I5 applied sequentially: four exact Decimal answer corrections and six exact unit-wording drafts. Stable IDs/concepts/options receive `fuel-exact-r2` or `fuel-unit-r2` revisions. [Arithmetic evidence and draft limitations](app-migration/implementation-evidence/9I/README.md). No release approval or 9F hold clearance is implied.

#### 9I1. Correct fuel-saving-150-0.5

Apply the exact no-rounding draft; independently calculate the 0.75-litre key and check every alternative/explanation using decimal arithmetic.

**Input:** 9A3, 9D1 and this question’s 7D proposal / assumptions.

**Output:** Revised fuel-saving-150-0.5, generated Bank.kt and arithmetic/acceptance evidence.

**Done when:** The exact key is unique, measured-rate assumptions are explicit and the semantic revision prevents reinterpretation of earlier rounded answers.

#### 9I2. Correct fuel-saving-150-1.5

Apply the exact no-rounding draft; independently calculate the 2.25-litre key and check every alternative/explanation using decimal arithmetic.

**Input:** 9A3, 9D1 and this question’s 7D proposal / assumptions.

**Output:** Revised fuel-saving-150-1.5, generated Bank.kt and arithmetic/acceptance evidence.

**Done when:** The exact key is unique, measured-rate assumptions are explicit and the semantic revision prevents reinterpretation of earlier rounded answers.

#### 9I3. Correct fuel-saving-250-0.5

Apply the exact no-rounding draft; independently calculate the 1.25-litre key and check every alternative/explanation using decimal arithmetic.

**Input:** 9A3, 9D1 and this question’s 7D proposal / assumptions.

**Output:** Revised fuel-saving-250-0.5, generated Bank.kt and arithmetic/acceptance evidence.

**Done when:** The exact key is unique, measured-rate assumptions are explicit and the semantic revision prevents reinterpretation of earlier rounded answers.

#### 9I4. Correct fuel-saving-250-1.5

Apply the exact no-rounding draft; independently calculate the 3.75-litre key and check every alternative/explanation using decimal arithmetic.

**Input:** 9A3, 9D1 and this question’s 7D proposal / assumptions.

**Output:** Revised fuel-saving-250-1.5, generated Bank.kt and arithmetic/acceptance evidence.

**Done when:** The exact key is unique, measured-rate assumptions are explicit and the semantic revision prevents reinterpretation of earlier rounded answers.

#### 9I5. Apply the six litre-unit grammar fixes

Apply only fuel-40-5, fuel-saving-100-0.5, fuel-saving-100-1, fuel-saving-100-2, fuel-saving-200-0.5 and fuel-saving-200-1.

**Input:** 9A3, 9D1 and six exact 7D grammar drafts.

**Output:** Six corrected records, generated Bank.kt and before/after checks.

**Done when:** Only approved wording changes; numeric keys and mathematical meaning are unchanged.

### 9J. Assemble and validate the accepted question package

**Approved artwork presentation — 17 October 2026:** Implemented the explicitly approved larger frames while preserving all official bytes and neutral semantics. All 80 desktop and 144 Python tests pass; Android's six native tests and iOS's 48-context artwork matrix plus five corrected route tests pass. Each target has all twelve assets at light/dark and 100%/160% text; 48 actual browser contexts are also captured. All 24 affected question revisions pass four shared delivery runs. Native asset fixtures are not full-question native acceptance, and original fine strokes remain pale in narrow browser views; no scoring hold was cleared. [Exact evidence, visual review and remaining scope](app-migration/implementation-evidence/faint-assets-approved/README.md).


**Native closure checkpoint — 17 October 2026:** The first stage of the user's closure order is verified on the isolated flow: five Android native route tests, five iOS simulator UI tests with scoped description/trait audits, and real Android TalkBack traversal of library, lesson and neutral assessment content. Search/filter/expansion retention, persistent search naming, reference catalogue back navigation and touch-mode source-trigger focus are fixed. All 80 desktop and 144 Python tests pass; Android/iOS simulator/Wasm compilation and generator checks pass. [Native evidence, reproduction and exact limits](app-migration/implementation-evidence/native-reader-routes/README.md). This closes the representative native reader/route checkpoint; it does not accept the twelve faint assets, release the 616 holds or complete production integration. Next: preview/approval for any changed faint-asset presentation, final 9J package plus 9M3 rerun, then 9L14 and complete-flow verification.


**Execution 16 October 2026:** 9J1 complete for all 1,000 IDs. 9J2 assembled as a held candidate: 384 accepted records and 616 delivery-held records; release validation correctly blocks completion. 9J3–9J4 validate the candidate capacity/parity/shuffling, without weakening quotas or activating held records. Exact integer remainders fix tie drift at shorter lengths. [Evidence and remaining acceptance conditions](app-migration/implementation-evidence/9J/README.md).

**Joint checkpoint — 17 October 2026:** Delivery and 9M3 candidate checks proceed together through the isolated real-candidate verification host. All 616 held revisions pass the desktop light/dark × 100%/160% text matrix (2,464 question runs; 6,160 image zoom/returns). The twelve faint assets affect 24 questions; the other 592 can progress independently through native/route acceptance. Two actual S5 candidate contexts have simulator AX/modal/selection evidence. Native reader, complete platform/route and faint-preview legibility acceptance remain open; no hold is cleared. [Per-question readiness and next inputs/outputs](app-migration/implementation-evidence/9J-followup/README.md).

#### 9J1. Bind canonical relationships for all questions

Apply exact primary/related lesson IDs, source IDs and URL-record references for all 1,000 baseline IDs from the validated map; keep retained assessment fields unchanged.

**Input:** 9B17, 9D1, question-map.json and exhaustive question assignments.

**Output:** Question relationship metadata and relationship-parity.json.

**Done when:** All 1,000 IDs have the exact mapped relationships; all targets resolve or use the explicit approved unavailable policy.

#### 9J2. Assemble accepted eligibility and package identity

**Finalization attempt — 17 October 2026:** Fresh structural validation and all 41 focused package/state/navigation/reader tests pass. Direct release validation still rejects the exact manifest with 384 accepted / 616 held questions. The fresh 9M3 rerun records 18 passing current contracts and four conditional future-store contracts against this manifest; accepted-release verification remains open. No holds, replacements or release flag were changed. [Finalization result and required acceptance work](app-migration/implementation-evidence/9J-finalization/README.md).


Merge per-ID results for 336 retained assessments, 626 rewrites and 38 replacements. Bind accepted content, sources, assets and aliases into a release manifest digest.

**Input:** 9J1, all 9E–9I acceptance records, 9K2 aliases and reviewed 9D descriptions.

**Output:** content/content-manifest.json, generated Bank.kt and eligibility-audit.json.

**Done when:** All 1,000 IDs / 500 concepts are accounted for, each active item has complete acceptance and retained fields remain unchanged; unresolved holds block completion.

#### 9J3. Verify quiz selection capacity

Exercise every test length 1–70, category allocation, residual random picks and concept uniqueness using the accepted pool.

**Input:** 9J2 package and existing selection contract.

**Output:** Selection checks and capacity-report.json.

**Done when:** Existing 7/5/16/32/5 plus five random allocation at 70 and largest-remainder rules pass; no quota is weakened to mask insufficient capacity.

#### 9J4. Verify generated question parity and shuffling

Compare JSON/Kotlin output and exercise fixed seeds across all key positions and both feedback modes.

**Input:** 9J2–9J3 and generated bank.

**Output:** Question parity/shuffle checks and review.md.

**Done when:** No IDs, links, keys, option identities or explanations drift; rerunning generation is byte-identical.

### 9K. Implement canonical navigation and legacy resolution

**Execution 17 October 2026:** Revalidated 9K1–9K4 foundations against 9J. Added missing-session recovery, normalised moved-block requests, preserved exact pending source references, and rejected stale discard confirmations after session replacement. All twelve entry-point contracts have explicit verification/integration scope. [Results](app-migration/implementation-evidence/9K/README.md). Full canonical view activation remains 9L14 and does not clear 9J/9F holds.

#### 9K1. Implement typed canonical destinations

**Execution record — 16 October 2026:** Implemented and verified the prerequisite foundation/component for 9F. Full route activation and outstanding platform reader/delivery acceptance are separate. [Implementation scope](app-migration/implementation-evidence/9K/README.md) · [Verification](app-migration/implementation-evidence/9F/README.md).

Create one internal resolver for curriculum, sign, source and supporting-anchor destinations. Validate parent/block targets without adding platform URL schemes.

**Input:** 9B17 and the 7E routing contract.

**Output:** Typed route/resolver code and canonical-resolution checks.

**Done when:** Every published ID resolves to its exact type; invalid IDs return an explicit unavailable result.

#### 9K2. Import and resolve legacy aliases

**Execution record — 16 October 2026:** Implemented and verified the prerequisite foundation/component for 9F. Full route activation and outstanding platform reader/delivery acceptance are separate. [Implementation scope](app-migration/implementation-evidence/9K/README.md) · [Verification](app-migration/implementation-evidence/9F/README.md).

Import the frozen legacy-app-4768933c3d9a namespace, 39 chapter aliases, 361 integers including 38 gaps, 178 topics, 343 sign records and 1,000 question routes.

**Input:** 9K1 and exact 7E alias records.

**Output:** content/legacy-aliases.json, generated aliases and precedence checks.

**Done when:** Question identity beats page; ambiguous values return all canonical choices; unknown inputs never guess first/nearest content. SIG16–18 remain explicit unavailable routes.

#### 9K3. Implement the shared quiz navigation guard

**Execution record — 16 October 2026:** Implemented and verified the prerequisite foundation/component for 9F. Full route activation and outstanding platform reader/delivery acceptance are separate. [Implementation scope](app-migration/implementation-evidence/9K/README.md) · [Verification](app-migration/implementation-evidence/9F/README.md).

Route all eight navigation states and twelve entry-point rules through the existing unfinished-quiz guard and related-reading restrictions.

**Input:** 9K1–9K2 and 7E transitions.

**Output:** Central transition/guard code and entry-point checks.

**Done when:** Every outbound action uses the same guard; cancellation preserves the current quiz and no new action bypasses unanswered-test restrictions.

#### 9K4. Implement validated return context

**Execution record — 16 October 2026:** Implemented and verified the prerequisite foundation/component for 9F. Full route activation and outstanding platform reader/delivery acceptance are separate. [Implementation scope](app-migration/implementation-evidence/9K/README.md) · [Verification](app-migration/implementation-evidence/9F/README.md).

Carry content/block/reading position/focus through reference/source visits and restore only valid origins. Support moved, retired-one/many/none and unavailable resolver outcomes.

**Input:** 9K1–9K3 and 7E return/tombstone rules.

**Output:** Return-context handling and focused navigation checks.

**Done when:** Known missing blocks fall back to their parent with a notice; unknown parents stay unavailable; production tombstones remain empty and no position is invented.

### 9L. Implement one approved view or interaction at a time

**Execution record — 17 October 2026:** Implemented isolated 9L1–9L13 components in sequence using the approved designs: complete typed teaching renderer, library filtering, deliberate reveal, snapshot reviews, sources, reference/viewer reuse and recovery states. [Outputs, checks and remaining acceptance](app-migration/implementation-evidence/9L/README.md). This is component implementation, not release/platform acceptance. **9L14 remains blocked** by the unaccepted 9J candidate and unfinished 9M state prerequisites; production activation and legacy payload removal were not performed.

Use the exact approved revisions and final 8O dispositions, including accepted state-specific visual variants. UI tasks may use imported content and the exact preview fixtures before the final scored bank is accepted; only 9L14 activates the integrated flow after 9J passes. This dependency refinement permits actual renderer/zoom work before 9F delivery proof without clearing any scoring hold. Each task verifies its own rendering, keyboard/focus and accessibility behaviour; changed design requires a new approved preview.

#### 9L1. Build the library overview

Render ten modules, forty lessons, reviews and reference/source entry actions using canonical titles/order.

**Input:** 9B17, 9K3 and approved 8B.

**Output:** Library view and fixture comparison.

**Done when:** Module numbering is stable, every lesson is discoverable and no invented completion or active-question count appears.

#### 9L2. Add library search and category filters

Add query/category intersection, five mapped categories, clear-query/clear-category actions and the exact empty state.

**Input:** 9L1, 7E tags and approved 8C.

**Output:** Search/filter state and matching checks.

**Done when:** Canonical order survives filtering; no-primary-question lessons remain discoverable and each clear action resets only its own input.

#### 9L3. Build the lesson-reader opening and navigation

Render exact module context, title, goal and complete prose blocks; wire previous/next through all 60 reading nodes.

**Input:** 9B17, 9K4 and approved 8D.

**Output:** Reader shell/prose rendering and navigation checks.

**Done when:** Full lesson content is available; source/lesson navigation follows canonical order and respects guards.

#### 9L4. Add deliberate knowledge-check reveal

Add Show answer/Hide answer with expanded state, answer association and safe focus restoration on collapse.

**Input:** 9L3 and approved 8E.

**Output:** Knowledge-check component and reveal/semantics checks.

**Done when:** Hidden answers are absent from accessibility reading until deliberate reveal; no new scoring or completion state is created.

#### 9L5. Render long content, tables and calculations

Implement full tables, selectable equations, illustrations and long-content scrolling with the approved body family and actual user text scaling.

**Input:** 9L3, 9C4 and approved 8F.

**Output:** Rich block rendering and same-viewport large-text evidence.

**Done when:** No approved block is omitted, clipped or ellipsized; operator/unit association and reading order survive scaling.

#### 9L6. Build the standard answer review

Render selected/correct shuffled options, main and per-option explanations, sources and related-lesson actions after permitted reveal.

**Input:** 9D2, 9K4 and approved 8G / exact situation-001 fixture.

**Output:** Answer-review view and immediate/end-mode checks.

**Done when:** Identity, displayed order and feedback remain aligned; related teaching cannot bypass the unfinished-test guard.

#### 9L7. Add calculation answer-review rendering

Render the exact fuel calculation fixture through the shared review component, retaining assumptions, units and complete explanations.

**Input:** 9L6 and approved 8H / exact proposed fuel fixture.

**Output:** Calculation review rendering and fixture evidence.

**Done when:** Displayed A-selected/B-correct order and 0.75-litre explanation match; fixture rendering alone does not accept the question for scoring or add history.

#### 9L8. Build the source directory and detail

Render exact source titles/publishers, distinct date types, classifications and scope; wire external actions and validated return.

**Input:** 9C1, 9K4, 9L3 and approved 8I.

**Output:** Sources directory/detail and return-context checks.

**Done when:** Lesson-scoped bindings are exact, external failure retains usable recovery and Back restores directory/lesson position and focus.

#### 9L9. Build sign and reference details

**Execution record — 16 October 2026:** Implemented and verified the prerequisite foundation/component for 9F. Full route activation and outstanding platform reader/delivery acceptance are separate. [Implementation scope](app-migration/implementation-evidence/9L9/README.md) · [Verification](app-migration/implementation-evidence/9F/README.md).

Render exact sign bytes, official name/caption, English editorial notice, white framing and reference-group navigation.

**Input:** 9C2–9C3, 9B16, 9K4 and approved 8J.

**Output:** Reference/detail view and exact B1 binding checks.

**Done when:** Images preserve aspect/geometry and captions/credits; study meanings never become pre-answer descriptions. Layout completion does not clear delivery holds.

#### 9L10. Implement the accessible image viewer

**Execution record — 16 October 2026:** Implemented and verified the prerequisite foundation/component for 9F. Full route activation and outstanding platform reader/delivery acceptance are separate. [Implementation scope](app-migration/implementation-evidence/9L10/README.md) · [Verification](app-migration/implementation-evidence/9F/README.md).

Add fit, Zoom in/Zoom out/Reset, keyboard/pointer pan and Close; integrate the viewer into approved study and assessment contexts without revealing hidden meanings.

**Input:** 9L9, 9D2 and approved zoom/accessibility requirements.

**Output:** Shared image viewer and zoom/return/focus checks.

**Done when:** No pinch-only action is required; Close restores origin and trigger focus; no crop, recolour or geometry change is introduced.

#### 9L11. Build ambiguous and moved-link states

Render deliberate canonical choices and the known-parent moved-passage notice with the exact page-46 context fixtures.

**Input:** 9K2–9K4, 9L3 and approved 8K.

**Output:** Chooser/moved views and context-specific route checks.

**Done when:** situation-017 opens M04-L03, situation-103 opens M04-L01, page alone offers four approved choices; no old-PDF equivalence is implied.

#### 9L12. Build unavailable-destination states

Render exact SIG16–18 messages with their distinct official actions, optional M03-L02 and library action; add the generic unavailable fallback.

**Input:** 9K2–9K4 and approved 8L.

**Output:** Unavailable views and recovery checks.

**Done when:** No substitute sign/registry entry is invented; failed external actions leave valid recovery and unknown destinations never guess.

#### 9L13. Build missing-results recovery

Render No saved result is available. and Set up a practice test. from the approved fixture.

**Input:** 9K3, 9M2 and approved 8M.

**Output:** Recovery view and deliberate-setup navigation check.

**Done when:** No result is fabricated, setup does not auto-start a test and valid same-process setup preferences remain intact.

#### 9L14. Connect the accepted package and remove legacy learner content

**Status — 17 October 2026: Blocked; production activation and legacy removal have not started.** The 9L1–9L13 components are implemented in an isolated verification flow; their desktop checks and target compilation do not constitute full platform acceptance.

Resolve these prerequisites before executing 9L14:

- **9J release acceptance:** The candidate still contains 616 held questions: 578 sign rewrites and 38 unapplied replacement proposals. The approved larger presentation for S5, S6, S7, S11, S12, S13, T1, T2, T6, T8, T22 and X8 is implemented with full native/browser asset captures; per-question scored-use legibility and remaining native question acceptance still need explicit decisions; representative native reader/route evidence is now recorded in the [native closure checkpoint](app-migration/implementation-evidence/native-reader-routes/README.md). Final package delivery acceptance still requires the faint-asset decisions and reconciliation of the per-question readiness evidence. Close the recorded 9F acceptance conditions and rerun 9J release validation; component rendering or compilation cannot clear these holds. Preserve exact official artwork and the original held replacement records. [9J blockers](app-migration/implementation-evidence/9J/README.md) · [9F delivery decisions](app-migration/implementation-evidence/9F/README.md).
- **9M1–9M3 transient state:** 9M1–9M2 model/component work is implemented and fixture/candidate checked. All 22 contracts are recorded: 18 current checks pass and four future-store cases remain conditional. Final 9M3 verification still requires the accepted 9J package; production preference/reset integration remains part of 9L14. [9M results and scope](app-migration/implementation-evidence/9M/README.md).
- **Remaining view acceptance:** Representative Android TalkBack and iOS simulator native interaction plus inline source-trigger return are now verified in the [native closure checkpoint](app-migration/implementation-evidence/native-reader-routes/README.md). Retain per-illustration visual acceptance and complete integrated production-flow checks for their remaining stages. The 25 desktop component captures and Android/iOS simulator/Wasm compilation are bounded evidence; full integrated acceptance remains 9O. iOS testing uses the user's selected simulator scope. [9L results and open checks](app-migration/implementation-evidence/9L/README.md).

**Execution order:** 9M1–9M2 model prerequisites are implemented. Work through 9F/9J delivery acceptance and 9M3 candidate verification together, using isolated verification routes before production activation. After acceptance, repeat 9M3 against the final package; then execute 9L14 and the integrated 9O checks. Delivery/route evidence can be gathered before activation; it must not depend on enabling held questions in production. Until the prerequisites pass, keep activation, the fourteen label replacements, removal of the 39 summaries/178 Topic payloads and manifest-derived learner counts pending together.

Connect the new views to the accepted package; apply all fourteen learner-label replacements, remove 39 old summaries and unused 178 Topic payloads, and derive counts from the manifest.

**Input:** 9L1–9L13, 9J4 and 9M1–9M3.

**Output:** Integrated App.kt / Chapters.kt / Curriculum.kt and learner-copy checks.

**Done when:** No old book names, borrowed chapter labels, source folios or court-case narratives remain in learner payloads; legitimate publishers/credits and full teaching remain available.

### 9M. Preserve transient quiz state

**Execution record — 17 October 2026:** 9M1–9M2 model/component work is implemented with exact session tokens, pinned review/filter state, guarded discard, missing-context recovery, process-reset defaults and release/capacity validation. 9M3 records all 22 audited contracts with fixture/candidate evidence; final release verification awaits acceptance of 9J's 616 held questions; its fixture/candidate checks can proceed alongside 9J. No production activation or persistence was added. [Evidence, reproduction and integration scope](app-migration/implementation-evidence/9M/README.md).

#### 9M1. Preserve session and review identity

**Status — 17 October 2026:** Model/component implementation and checks pass; production wiring remains 9L14.

Carry question revision, package identity, shuffled option IDs, selection, key, feedback and score through quiz/results/review. Keep both feedback modes and review-filter position.

**Input:** 9D1–9D2, 9K3–9K4 and 7E session contracts; exact fixtures may be used before 9J.

**Output:** Session/review model changes and score/order checks.

**Done when:** A selected displayed option never rebinds to bank order; navigation returns to the same valid review context without regrading.

#### 9M2. Preserve reset and missing-session rules

**Status — 17 October 2026:** Model implementation and checks pass, including rejected production start for the held candidate; production wiring remains 9L14.

Implement the audited restart, missing-result and setup validation rules using existing transient state only.

**Input:** 9A2, 9K3 and 7E state contracts.

**Output:** Reset/setup validation and missing-context checks.

**Done when:** Restart clears state as before; same-process preferences survive only where valid, fresh defaults remain 70/existing feedback, and starting requires valid 1–70 capacity.

#### 9M3. Verify all transient-state contracts

**Status — 17 October 2026:** [All 22 contracts recorded](app-migration/implementation-evidence/9M/state-contract-results.json). Eighteen current checks pass on fixtures/candidate; four future-store cases are conditional. **Awaiting final release verification against accepted 9J content.** Continue delivery acceptance and transient-state checks together; candidate results do not waive release acceptance.

Exercise the 22 recorded contracts against the accepted package, including guards, review filters, quit/restart and version compatibility limits.

**Input:** 9M1–9M2, 9J4 and 7E contracts.

**Output:** state-contract-results.json and focused regression checks.

**Done when:** Every applicable contract passes; conditional future-store/hot-replacement cases remain documented separate scope, with no invented database or attempt history.

### 9N. Prepare the three assessment-coverage briefs

Each task writes one reviewable brief only. State the objective, sources, proposed format, plausible mistakes and acceptance rubric. Additional scored IDs require a separate content decision; retain all teaching and the baseline bank.

#### 9N1. Write the M01-L01 assessment brief

Prepare only the brief for preparation, entitlement and training checklist; recheck current official requirements.

**Input:** 9B17, M01-L01 objectives/content and its 7D coverage gap.

**Output:** The M01-L01 section of docs/curriculum/app-migration/assessment-coverage-briefs.md.

**Done when:** The proposed assessment addresses this lesson’s gap with a checkable rubric; no scored item or baseline ID is added/replaced.

#### 9N2. Write the M07-L04 assessment brief

Prepare only the brief for combined-risk decisions to adapt, stop or change route.

**Input:** 9B17, M07-L04 objectives/content and its 7D coverage gap.

**Output:** The M07-L04 section of docs/curriculum/app-migration/assessment-coverage-briefs.md.

**Done when:** The proposed assessment addresses this lesson’s gap with a checkable rubric; no scored item or baseline ID is added/replaced.

#### 9N3. Write the M10-L03 assessment brief

Prepare only the brief for whole-journey explanation/reflection with a rationale and rubric.

**Input:** 9B17, M10-L03 objectives/content and its 7D coverage gap.

**Output:** The M10-L03 section of docs/curriculum/app-migration/assessment-coverage-briefs.md.

**Done when:** The proposed assessment addresses this lesson’s gap with a checkable rubric; no scored item or baseline ID is added/replaced.

### 9O. Prepare platform evidence and the step 10 handoff

Platform tasks validate the same candidate manifest. Record exact commands, toolchains, devices, observed results and artifact hashes. Unavailable tooling/device checks stay open; a successful compile alone does not prove device rendering, delivery or accessibility. Fixes affecting shared code/content require rerunning affected prior checks.

#### 9O1. Update documentation and provenance

Replace stale README book/chapter/feature claims using the accepted manifest, and document regeneration, resource packaging and retained credits.

**Input:** 9L14, 9J4, 9N1–9N3 and accepted source/reuse records.

**Output:** Updated README.md / build documentation and provenance inventory.

**Done when:** Feature/count claims match implemented behaviour and all required credits remain available.

#### 9O2. Run common integration checks

Run meaningful common tests plus full generation, resource and origin-parity checks on the integrated candidate.

**Input:** 9O1, 9B17, 9J4, 9K/9L/9M completed outputs.

**Output:** Common test/build logs and candidate manifest digest.

**Done when:** Content, routing, scoring and state checks pass against one reproducible package; no unresolved integration failure is hidden.

#### 9O3. Check the Android candidate

Check the configured Android build/resources and available device or emulator: package resources, offline teaching/assets and representative library/reader/quiz/source/reference/recovery paths.

**Input:** 9O2 candidate, configured toolchain and target runtime.

**Output:** Platform build/runtime evidence, resource hashes and unresolved-check list.

**Done when:** Build/resource checks and available runtime checks pass for this exact manifest; missing required device/accessibility/delivery evidence is explicit and remains a release blocker.

#### 9O4. Check the desktop candidate

Check the configured JVM desktop package and desktop runtime: package resources, offline teaching/assets and representative library/reader/quiz/source/reference/recovery paths.

**Input:** 9O2 candidate, configured toolchain and target runtime.

**Output:** Platform build/runtime evidence, resource hashes and unresolved-check list.

**Done when:** Build/resource checks and available runtime checks pass for this exact manifest; missing required device/accessibility/delivery evidence is explicit and remains a release blocker.

#### 9O5. Check the iOS simulator candidate

Check the configured iosSimulatorArm64 framework and simulator runtime: package resources, offline teaching/assets and representative library/reader/quiz/source/reference/recovery paths.

**Input:** 9O2 candidate, configured toolchain and target runtime.

**Output:** Platform build/runtime evidence, resource hashes and unresolved-check list.

**Done when:** Build/resource checks and available runtime checks pass for this exact manifest; missing required device/accessibility/delivery evidence is explicit and remains a release blocker.

#### 9O6. Check the iOS device candidate

Check the configured iosArm64 framework and physical-device runtime: package resources, offline teaching/assets and representative library/reader/quiz/source/reference/recovery paths.

**Input:** 9O2 candidate, configured toolchain and target runtime.

**Output:** Platform build/runtime evidence, resource hashes and unresolved-check list.

**Done when:** Build/resource checks and available runtime checks pass for this exact manifest; missing required device/accessibility/delivery evidence is explicit and remains a release blocker.

#### 9O7. Check the web candidate

Check the configured wasmJs build/resources and browser runtime: package resources, offline teaching/assets and representative library/reader/quiz/source/reference/recovery paths.

**Input:** 9O2 candidate, configured toolchain and target runtime.

**Output:** Platform build/runtime evidence, resource hashes and unresolved-check list.

**Done when:** Build/resource checks and available runtime checks pass for this exact manifest; missing required device/accessibility/delivery evidence is explicit and remains a release blocker.

#### 9O8. Assemble the implementation handoff

Cross-check every executable step, per-ID acceptance, source/asset evidence, platform results and T01–T10 coverage. Record the exact candidate, reproduction commands and remaining issues for independent verification.

**Input:** All 9A–9O7 task records, three coverage briefs and original step 10 verification specification.

**Output:** docs/curriculum/app-migration/implementation-evidence/implementation-review.md, evidence-index.json and updated progress.md.

**Done when:** Every required step is complete with no blocking implementation/acceptance/platform gaps; otherwise step 9 remains in progress. Step 10 is separately requested and remains the final app verification.

All 9A–9O outputs must satisfy the original backlog acceptance criteria as well as these task-specific checks. Stop after each requested task and save its evidence; neither this breakdown nor task completion authorises publishing or starts step 10.

## 10. Verify the finished app

Check navigation, question-to-lesson links, learning coverage, sign accuracy, and consistency with the approved PDF. Confirm that learner-facing content contains no third-party book names, original chapter labels, or source-book page numbers.

**Deliverable:** Verification report and any necessary fixes.

## Content principle

The work will use independently written material and appropriately sourced illustrations. Removing attribution alone is not the method for addressing copyright concerns.

**Book disclaimer:** Prominently state in the book’s introduction: “This material is a learning aid to help you understand Swedish driving theory. It is not an official source and cannot replace official information from Trafikverket and Transportstyrelsen. Always consult their current guidance and the applicable rules.”

## Execution

Request a step by number, for example: “Execute step 2.” For sign preparation, PDF design, chapter production, app migration planning, app previews or app implementation, request a substep such as “Execute step 4A”, “Execute step 5A” or “Execute step 6B” (chapter 1), “Execute step 7A”, “Execute step 8B” or “Execute step 9A1”. Step 9 group labels (9A–9O) contain smaller executable tasks; request the exact task ID to keep work bounded. Use the saved deliverables from preceding steps and respect each approval checkpoint. Saving this plan does not start the remaining steps.


**Sequencing update — 2 October 2026:** Following the 5A blocker notice, the user directly requested execution of 5B. A limited cover/opening-page preview without sign artwork was prepared under that instruction and is [awaiting approval](pdf-design/5b/review.md). The 13 required sign gaps and 4F completion gate remain unresolved; this exception does not clear sign-dependent layouts or final PDF production.
