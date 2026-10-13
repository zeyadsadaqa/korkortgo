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

## 7. Plan the app’s curriculum migration

Assign stable module and lesson IDs. Map existing practice questions to approved lessons and official references. Identify questions requiring rewriting, replacement, or removal.

**Deliverable:** Curriculum and question migration map.

## 8. Generate previews of the revised app

Use imagegen to show the library, lesson reader, and answer review using the approved curriculum. Replace book-page labels with useful lesson information.

**Deliverable:** App design previews.

**Approval:** Wait for explicit design approval before implementation. If changes are requested, revise the previews and wait for approval again.

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

Request a step by number, for example: “Execute step 2.” For sign preparation, PDF design or chapter production, request a substep such as “Execute step 4A”, “Execute step 5A” or “Execute step 6B” (chapter 1). Use the saved deliverables from preceding steps and respect each approval checkpoint. Saving this plan does not start the remaining steps.


**Sequencing update — 2 October 2026:** Following the 5A blocker notice, the user directly requested execution of 5B. A limited cover/opening-page preview without sign artwork was prepared under that instruction and is [awaiting approval](pdf-design/5b/review.md). The 13 required sign gaps and 4F completion gate remain unresolved; this exception does not clear sign-dependent layouts or final PDF production.
