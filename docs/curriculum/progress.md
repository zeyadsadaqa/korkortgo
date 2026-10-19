# KörkortGo Curriculum Plan Progress

**Source of truth:** [Implementation plan](implementation-plan.md)  
**Last updated:** 17 October 2026 (approved larger artwork presentation implemented and verified)
**Current position:** Steps 1–8 remain complete for the approved screen edition. Step 9: the approved larger artwork presentation is implemented; 80 desktop and 144 Python tests pass, alongside Android native tests, the iOS artwork matrix/route checks and 48 browser captures. [Current delivery evidence](app-migration/implementation-evidence/faint-assets-approved/README.md). The package remains 384 accepted / 616 held. 9M model/component checks pass; accepted-package 9M3, question-level delivery acceptance and 9L14 production integration remain open.
**Next action:** Finish remaining per-question/native and scored-use legibility acceptance using the approved larger renderer, finalize 9J only after release validation passes, rerun 9M3 against that accepted manifest, then complete 9L14 production integration/legacy cleanup and complete-flow verification. Do not infer question acceptance from asset fixture captures. The user selected iOS simulator scope.

This file records actual work and approvals. It does not authorise the next step or replace the implementation plan. Eight of ten steps have cleared their requirements for the chosen screen-edition scope; print production is deferred. This is a step count, not an estimate of total effort completed.

## Status overview

| Step | Work | Status | Deliverable / next requirement |
|---|---|---|---|
| 1 | Build the source inventory | Completed | [Source inventory](source-inventory.md); details below |
| 2 | Draft the original curriculum and official-source map | Completed | [Outline v1.0](curriculum-outline.md), [official-source map](curriculum-source-map.md) and [structured map](curriculum-source-map.json) approved for curriculum planning on 1 October 2026 |
| 3 | Write the complete learning material | Completed | [Editable manuscript](manuscript.md), [evidence register](manuscript-evidence.md) and [verification report](manuscript-verification.md); final illustrations and PDF remain later steps |
| 4 | Prepare official road-sign illustrations | Completed | [Official-vector resolution](sign-assets/official-poster/README.md); 4F passes with zero selected gaps; four optional variants excluded |
| 5 | Generate a PDF design preview | Completed for approved visual direction | All current previews approved; chapter artwork/typography/render checks remain in step 6 |
| 6 | Produce and verify the curriculum PDF | Completed for screen edition | [Approved release](pdf-production/korkortgo-curriculum.pdf), [verification](pdf-production/verification.md), [approval/scope](pdf-production/final-review/screen-release.json); print masters deferred |
| 7 | Plan the app’s curriculum migration | Completed; 7G passed, no planning blockers | [Verification report](app-migration/verification.md), [60 cross-stage checks](app-migration/verification.json), [implementation backlog](app-migration/implementation-backlog.md), [preview handoff](app-migration/preview-handoff.md) |
| 8 | Generate previews of the revised app | Completed; complete package explicitly approved | [Final approval](app-design-review.md), [681 checks](app-design/8o/verification.json), [specification](app-design-spec.md) |
| 9 | Implement the approved app changes | In progress; 9M1–9M2 prerequisites implemented, 9M3 awaiting release verification; 9L14 acceptance pending | [9M model/contract results](app-migration/implementation-evidence/9M/README.md); [9J release holds](app-migration/implementation-evidence/9J/README.md) remain |
| 10 | Verify the finished app | Not started | Verify the implementation and save the results |

## Step 4 substep tracker

The breakdown is saved in the [implementation plan](implementation-plan.md). Planning these substeps does not execute them. Update each row when its work is performed.

| Substep | Work | Status | Planned deliverable |
|---|---|---|---|
| 4A | List required signs and variants | Completed | [Sign selection](sign-selection.md): 263 identifiers, 24 teaching groups, 8 explicit gaps |
| 4B | Verify official sources and reuse | Completed | [Source register](sign-sources.json), [reuse and gap report](sign-reuse.md) |
| 4C | Collect and check image files | Completed with quality holds | [Asset package and findings](sign-assets/README.md), [manifest](sign-asset-manifest.json), [checks](sign-asset-checks.json) |
| 4D | Verify labels and explanations | Completed with image holds retained | [Captions](sign-captions.md), [structured captions](sign-captions.json), [review](sign-caption-review.md), [checks](sign-caption-checks.json) |
| 4E | Map signs to lessons and reference section | Completed with explicit gaps | [Placement map](sign-placement-map.md), [structured map](sign-placement-map.json), [checks](sign-placement-checks.json) |
| 4F | Verify package and record completion | Completed, rechecked 3 October | [Verification report](sign-verification.md), [checks](sign-verification-checks.json); zero selected image gaps |

## Step 5 substep tracker

| Substep | Work | Status | Deliverable / next requirement |
|---|---|---|---|
| 5A | Define brief and check readiness | Completed | [Design brief](pdf-design-brief.md); requirements, preview content and blockers recorded |
| 5B | Preview cover and opening pages | Completed; v4 approved | [Version 4 and review](pdf-design/5b/review.md); limited sign-free preview authorised by the subsequent user request |
| 5C | Preview contents and navigation | Completed; v1 approved | [Navigation v1 and review](pdf-design/5c/review.md) |
| 5D | Preview lesson pages | Revision requested | [Six sample pages and review](pdf-design/5d/review.md) |
| 5E | Preview sign layouts and diagrams | Direction accepted; required work remains | [Review](pdf-design/5e/review.md), [50-section coverage register](pdf-design/5e/illustration-register.md); revised chapter/diagram previews prepared; explicit approval pending; zero selected sign holds |
| 5F | Consolidate design and obtain approval | Consolidated; completion blocked | [Specification](pdf-design-spec.md), [review](pdf-design-review.md); final package approval pending blocker resolution |

## Step 6 substep tracker

6A completed on 4 October 2026 after sequential visual approval and the renewed execution request. Each chapter can be requested separately; completion does not start the next substep.

| Substep | Work | Status | Planned output |
|---|---|---|---|
| 6A | Shared build and opening pages | Completed | [Opening PDF](pdf-production/front-matter.pdf), [build instructions](pdf-production/README.md), [readiness/render review](pdf-production/readiness-review.md), [checks](pdf-production/verification.json) |
| 6B | Chapter 1 — Choose to drive responsibly | Completed | [Chapter PDF](pdf-production/chapters/M01/chapter.pdf), [review](pdf-production/chapters/M01/review.md), [checks](pdf-production/chapters/M01/verification.json); 15-page screen-review build |
| 6C | Chapter 2 — Prepare a car that is ready | Completed | [Chapter PDF](pdf-production/chapters/M02/chapter.pdf), [review](pdf-production/chapters/M02/review.md), [checks](pdf-production/chapters/M02/verification.json); 15-page screen-review build |
| 6D | Chapter 3 — Read the road before acting | Completed | [Chapter PDF](pdf-production/chapters/M03/chapter.pdf), [review](pdf-production/chapters/M03/review.md), [checks](pdf-production/chapters/M03/verification.json); 50-page screen-review build |
| 6E | Chapter 4 — Negotiate shared space | Completed | [Chapter PDF](pdf-production/chapters/M04/chapter.pdf), [review](pdf-production/chapters/M04/review.md), [checks](pdf-production/chapters/M04/verification.json); 42-page screen-review build |
| 6F | Chapter 5 — Make room in busy streets | Completed | [Chapter PDF](pdf-production/chapters/M05/chapter.pdf), [review](pdf-production/chapters/M05/review.md), [checks](pdf-production/chapters/M05/verification.json); 44-page screen-review build |
| 6G | Chapter 6 — Travel beyond the town | Completed | [Chapter PDF](pdf-production/chapters/M06/chapter.pdf), [review](pdf-production/chapters/M06/review.md), [checks](pdf-production/chapters/M06/verification.json); 48-page screen-review build |
| 6H | Chapter 7 — Adapt when conditions change | Completed | [Chapter PDF](pdf-production/chapters/M07/chapter.pdf), [review](pdf-production/chapters/M07/review.md), [checks](pdf-production/chapters/M07/verification.json); 23-page screen-review build |
| 6I | Chapter 8 — Take responsibility for the vehicle and load | Completed | [Chapter PDF](pdf-production/chapters/M08/chapter.pdf), [review](pdf-production/chapters/M08/review.md), [checks](pdf-production/chapters/M08/verification.json); 29-page screen-review build |
| 6J | Chapter 9 — Reduce the impact of each journey | Completed | [Chapter PDF](pdf-production/chapters/M09/chapter.pdf), [review](pdf-production/chapters/M09/review.md), [checks](pdf-production/chapters/M09/verification.json); 22-page screen-review build |
| 6K | Chapter 10 — Respond, reflect and keep learning | Completed | [Chapter PDF](pdf-production/chapters/M10/chapter.pdf), [review](pdf-production/chapters/M10/review.md), [checks](pdf-production/chapters/M10/verification.json); 23-page screen-review build |
| 6L | Appendices, sign reference and official sources | Completed | [Reference PDF](pdf-production/reference-material.pdf), [editable source](pdf-production/reference/build_reference.py), [review](pdf-production/reference-material-review.md), [checks](pdf-production/reference/verification.json); 183-page screen-review build |
| 6M | Complete book assembly and navigation | Completed | [Complete PDF](pdf-production/korkortgo-curriculum-review.pdf), [assembly review](pdf-production/assembly/assembly-review.md), [checks](pdf-production/assembly/verification.json); 498 pages with final folios and navigation |
| 6N | Final verification and PDF approval | Completed for screen edition; explicitly approved 14 October | [Report](pdf-production/verification.md), [approved screen PDF](pdf-production/korkortgo-curriculum.pdf), [tagging checks](pdf-production/accessibility/verification.json); print deferred |

## Step 7 substep tracker

The [7A–7G breakdown](implementation-plan.md#7-plan-the-apps-curriculum-migration) remains the execution plan. The user explicitly approved 6N and authorised 7C on 14 October 2026. The 7A–7B identities now bind to the approved tagged screen edition, with historical snapshots retained. All 1,000 H7 decisions were checked against fresh approved-page text; the two page-193 records carry the reviewed 6N correction. 7D records all 1,000 dispositions and explicit replacement holds; 7E records link/state/alias/version rules and three exact sign gaps. 7F assigns bounded work, acceptance checks and exact preview content, retaining the explicit unavailable policy for the three signals. 7G reran the 7C–7F validators and passed all 60 cross-stage checks. Step 7 planning is complete; implementation holds remain future acceptance work, not cleared by this audit.

| Substep | Work | Status | Planned deliverable |
|---|---|---|---|
| 7A | Freeze content and audit app | Completed; approved release bindings refreshed | [Baseline](app-migration/baseline.md), [hashes and checks](app-migration/baseline.json) |
| 7B | Confirm curriculum IDs and content contract | Completed; canonical IDs unchanged | [Registry](app-migration/curriculum-map.md), [structured map](app-migration/curriculum-map.json) |
| 7C | Map questions to teaching and official sources | Completed; 1,000 mapped, no unresolved mappings | [Question map](app-migration/question-map.json), [review](app-migration/question-map-review.md), [checks](app-migration/question-map-checks.json) |
| 7D | Review question dispositions and corrections | Completed planning review; 38 asset/display holds explicit | [Dispositions](app-migration/question-actions.md), [all 1,000 records](app-migration/question-actions.json), [checks](app-migration/question-actions-checks.json) |
| 7E | Plan link and learner-progress migration | Completed planning map; three exact signal gaps explicit | [Plan](app-migration/link-and-progress-map.md), [structured rules](app-migration/link-and-progress-map.json), [checks](app-migration/link-and-progress-checks.json) |
| 7F | Prepare implementation backlog and preview handoff | Completed planning; 68 handoff checks pass | [Backlog](app-migration/implementation-backlog.md), [all question assignments](app-migration/implementation-backlog.json), [preview handoff](app-migration/preview-handoff.md), [exact content](app-migration/preview-content.json), [checks](app-migration/handoff-checks.json) |
| 7G | Verify complete migration package | Completed; 60/60 cross-stage checks pass, no planning blockers | [Review](app-migration/verification.md), [machine-readable results and input manifest](app-migration/verification.json), [reproducible verifier](app-migration/verify_migration_package.py) |

## Step 8 substep tracker

Each preview requires imagegen and explicit user approval before the next design task. 8A is preparation only; no visual proposal or implementation is approved.

| Substep | Work | Status | Deliverable / next requirement |
|---|---|---|---|
| 8A | Prepare the app-preview brief | Completed preparation | [Brief](app-design/brief.md), [readiness](app-design/readiness.json) |
| 8B | Preview the learning-library overview | Completed; v1 explicitly approved | [Wide/phone preview and review](app-design/8b/review.md) |
| 8C | Preview library search and filters | Completed; v1 explicitly approved | [Filtered/empty wide and phone previews](app-design/8c/review.md) |
| 8D | Preview the lesson-reader opening | Completed; v1 explicitly approved | [Wide/phone reader preview and review](app-design/8d/review.md) |
| 8E | Preview the lesson knowledge-check reveal | Completed; v2 explicitly approved | [Before/after wide and phone preview](app-design/8e/review.md) |
| 8F | Preview long-content and large-text reading | Completed; v1 explicitly approved | [Wide/phone regular and enlarged preview](app-design/8f/review.md) |
| 8G | Preview the standard answer review | Completed; v1 explicitly approved | [Wide/phone answered review](app-design/8g/review.md) |
| 8H | Preview the calculation answer review | Completed; v1 explicitly approved | [Wide/phone calculation review](app-design/8h/review.md) |
| 8I | Preview the sources area | Completed; v1 explicitly approved | [Directory/detail wide and phone previews](app-design/8i/review.md) |
| 8J | Preview the road-sign reference | Completed; v1 explicitly approved | [B1 detail/zoom layout and exact asset binding](app-design/8j/review.md) |
| 8K | Preview ambiguous and moved legacy links | Completed; chooser v2/moved v1 explicitly approved | [Wide/phone chooser and moved notice](app-design/8k/review.md) |
| 8L | Preview unavailable destinations | Completed; v1 explicitly approved | [Signal/generic wide and phone previews](app-design/8l/review.md) |
| 8M | Preview missing-results and setup recovery | Completed; v1 explicitly approved | [Wide/phone recovery preview](app-design/8m/review.md) |
| 8N | Assemble the app design specification | Completed consolidation; final package approval pending 8O | [Specification](app-design-spec.md), [index/checks](app-design/8n/package-index.json) |
| 8O | Verify the design package and obtain final approval | Completed; complete package explicitly approved | [Final review](app-design-review.md), [checks](app-design/8o/verification.json) |

## Step 9 substep tracker

9A–9O group labels retain the migration backlog references. Execute only the requested numbered task; completion does not start another task.

| Substep | Work | Status | Deliverable / next requirement |
|---|---|---|---|
| 9A1 | Freeze and check approved inputs | Completed; no blocking drift | [Baseline](app-migration/implementation-evidence/9A1/input-baseline.json), [readiness](app-migration/implementation-evidence/9A1/readiness.md), [review](app-migration/implementation-evidence/9A1/review.md); 1,174 matching bindings and 21 passing checks |
| 9A2 | Define typed content contract | Completed; desktop/common build and 11 tests pass | [Schema](app-migration/implementation-evidence/9A2/content-contract.md), [review](app-migration/implementation-evidence/9A2/review.md), [checks](app-migration/implementation-evidence/9A2/verification.json) |
| 9A3 | Implement deterministic generation/validation | Completed; 44 compiler and 12 Kotlin/desktop tests pass | [Compiler usage/fixture](app-migration/implementation-evidence/9A3/README.md), [review](app-migration/implementation-evidence/9A3/review.md), [checks](app-migration/implementation-evidence/9A3/verification.json) |
| 9B1 | Import introductions and reading structure | Completed; 86 checks and 14 JVM tests pass | [Authoring payload](../../content/curriculum.json), [ledger](../../content/curriculum-import-state.json), [review](app-migration/implementation-evidence/9B1/review.md) |
| 9B2 | Import module M01 | Not started | Separate request; preserve 9B1 opening IDs and cumulative import state |
| Remaining step 9 tasks | Content, questions, routes, UI, state and platform evidence | Not started | Follow exact task dependencies in the [implementation plan](implementation-plan.md#9-implement-the-approved-app-changes) |

## Completed work

### Step 1 — Source inventory

**Completed:** 1 October 2026.

- Inventoried all 367 pages and 39 sections of the supplied background material. The coverage records remain internal research documents.
- Created 125 official-source records: 121 successfully retrieved references, two failed discovery URLs with working replacements, one hub requiring manual content inspection, and one background PDF located through a search excerpt only.
- Recorded source URLs, retrieval dates, checksums, topic coverage and verification limitations.
- Identified official syllabus objectives, examination domains, self-assessment requirements and additional licensing/practical preparation topics.
- Inventoried 19 official sign-category pages and checked all 343 existing sign assets against their recorded local hashes.
- Identified missing F1 direction-sign variants and limitations in the older sign index.
- Recorded road-sign reuse guidance and a verification queue for the manuscript.

| Saved deliverable | Purpose |
|---|---|
| [Source inventory and findings](source-inventory.md) | Main research report, scope, additions and verification queue |
| [Official source index](official-source-index.md) | Readable official references and retrieval statuses |
| [Official source data](official-sources.json) | Structured source metadata |
| [Internal coverage checklist](book-coverage.md) | Background topic coverage; not the new curriculum or its source map |
| [Internal coverage data](book-coverage.json) | Page and section accounting |
| [Road-sign inventory](road-sign-inventory.json) | Existing assets, integrity checks, gaps and reuse reference |

**Verification completed:** All pages accounted for, all section source IDs resolved, all 343 local asset hashes matched, and local report links resolved. Direct official links in the main report matched the retrieval manifest.

**Limits:** Retrieval and topic inventory do not certify every factual claim. Detailed legal exceptions, emergency procedures, statistics, vehicle-specific advice and illustration variants still require validation during their respective steps. Existing sign files were not freshly downloaded or fully checked for print quality. No manuscript, PDF design, finished curriculum PDF or app migration was produced in step 1.

### Step 2 — Original curriculum and official-source map

**Draft deliverables prepared:** 1 October 2026. **Version:** 1.0. **Status:** Completed; outline version 1.0 approved by the user on 1 October 2026.

- Created an original sequence of 10 modules, with 40 lesson objectives and 10 module self-assessment objectives.
- Added entry guidance, module scenario briefs, a future lesson format, reference-section scope and the required introduction disclaimer.
- Mapped every objective to official sources only, using 77 successfully retrieved references from Trafikverket and Transportstyrelsen. The new deliverables contain no background-book references or source-book page numbers.
- Cross-checked planned coverage against all four official syllabus areas, including self-assessment, and all five theory-test domains. These are editorial mappings, not official examination weightings.
- Recorded evidence limits for each lesson and a research handoff covering legal exceptions, dated requirements, numerical examples, vehicle-specific advice, first aid, emergency procedures and sign variants.

| Saved deliverable | Purpose |
|---|---|
| [Curriculum outline v1.0](curriculum-outline.md) | Reviewable module sequence, lesson objectives, scenarios and approval checkpoint |
| [Official-source coverage map](curriculum-source-map.md) | Readable objective-level references, framework coverage and unresolved research |
| [Structured curriculum map](curriculum-source-map.json) | Matching objective IDs, source IDs, URLs, retrieval dates and evidence limits |

**Verification completed:** Checked 10 modules, 40 unique lesson IDs and 10 unique reflection IDs; all objectives have references; all 77 referenced sources resolve to successfully retrieved official-domain entries in the inventory; source dates are recorded; relative links in the new deliverables and tracker resolve. Confirmed the outline and source map contain no background-book names or page-based references.

**Limits at completion of step 2:** The approved outline provided topic-level support. Its evidence gaps were handed to step 3; their treatment is recorded below. Step 2 produced no sign assets, PDF design, finished PDF, question migration or app changes.

### Step 3 — Complete editable learning material

**Completed:** 1 October 2026. **Status:** Text and evidence handoff complete; manuscript approval and final PDF verification are not implied.

- Wrote the 10 approved modules and all 40 lessons, each with an explanation, original worked decision, answered knowledge check and reminder. Added 10 module reflections, practical checklists, a glossary and a practice record.
- Included the prominent learning-aid disclaimer and distinguished legal requirements, official recommendations and original learning exercises.
- Recorded 66 cited official references and 96 evidence records (86 material claim groups and 10 reflection-scope records). Detailed legal exceptions use primary legislation on Sveriges riksdag alongside Trafikverket and Transportstyrelsen guidance.
- Kept first aid to a 58-word passage and a reference to 1177, following the user's instruction. No clinical course or claim that first aid is excluded from assessment was added.
- Documented the treatment of all V01–V14 research items, including dated rules, numerical examples, emergency guidance and the limits of vehicle-specific advice. Sign artwork remains step 4.

| Saved deliverable | Purpose |
|---|---|
| [Editable manuscript](manuscript.md) | Complete original teaching text, scenarios, checks, appendices and references |
| [Source manifest](manuscript-sources.json) | Official URLs, retrieval dates and checksums for cited sources |
| [Evidence register](manuscript-evidence.md) | Readable claim support, source locators and scope limits |
| [Structured evidence](manuscript-claims.json) | Matching claim and reflection records |
| [Verification report](manuscript-verification.md) | Research dispositions, checks and later-stage requirements |
| [Structural check results](manuscript-checks.json) | Recorded validation results and manuscript checksum |

**Verification completed:** All 40 approved lesson IDs and titles and 10 reflections are present; lesson sections and answered checks are complete; citation aliases and evidence references resolve; cited domains are official; retrieval dates and hashes are recorded; the disclaimer is prominent; worked arithmetic and local deliverable links pass checks. No background-book names or source-book page references occur in the new manuscript. No app tests were needed for this documentation-only step.

**Limits:** This is editable teaching text, not a finished illustrated PDF or official publication. Step 4 must verify sign assets and placements; steps 5–6 must obtain design approval, render and inspect the PDF, and recheck time-sensitive rules before release. No app content or question migration was performed.

### Step 4A — Select required signs and variants

**Completed:** 1 October 2026, following the user's request to execute 4A.

- Reviewed manuscript sign examples and Appendix B against the existing catalogue inventory.
- Saved [sign-selection.md](sign-selection.md): 263 unique codes/variant identifiers in 24 teaching groups, with intended lessons, reference-section inclusion, selection reasons and variant needs.
- Recorded eight explicit research or illustration gaps, including missing local F1-1/F1-2 assets, signal variants, compound parking examples and non-sign equipment.
- Selected representatives for all 18 Appendix B catalogue families; did not assume the selection is an exhaustive examination sign list.

**Verification:** All selected identifiers resolve to the saved catalogue inventory or its recorded F1-2 alternative; every listed lesson/review ID exists in the manuscript; all explicitly cited sign codes are included. Of the selected identifiers, 261 have local inventory entries and two are missing. Local presence is not a source, reuse or image-quality approval.

**Handoff:** 4B must verify current official pages, exact variants and reuse conditions. No assets were downloaded, final captions written, or visual layouts designed. Step 4 remains in progress; 4B–4F are not started.

### Step 4B — Verify official sources and reuse

**Completed:** 1 October 2026, following the user's request to execute 4B.

- Saved [sign-sources.json](sign-sources.json) with all 263 selected identifiers and 235 additional linked variant pages: 498 unique official sign pages retrieved successfully, with HTML hashes, dates, page titles, image/download links and variant associations.
- Saved [sign-reuse.md](sign-reuse.md), recording Transportstyrelsen’s sign-file permission, the scope interpretation for other catalogue families, project attribution and all eight 4A gap dispositions.
- Located both F1 variants. F1-2 has no linked EPS file; Y2 has an embedded GIF without a separate print download. The other 261 selected pages link EPS files.
- Recorded five held graphic requests: unverified arrow variants, exact parking/time composites, crossing-ID close-ups, non-sign imagery and unsupported static representations of sound/movement. Official source candidates are ready for 4C inspection, not publication.

**Verification:** All selection IDs match; all 498 source IDs and cached HTML hashes checked; source/image/download URLs use the official domain; linked variant references resolve; all pages have a title and image candidate; EPS counts and held statuses checked. No image-file integrity or print-quality claim is made before 4C.

**Handoff:** The source/reuse criterion for 4B is satisfied, including explicit holds for unsupported graphics. Step 4C must download and inspect the actual files. No official sign image files were downloaded in 4B, and no final captions, design or app changes were produced.

### Step 4C — Collect and inspect official image files

**Completed:** 1 October 2026. **Status:** Collection and quality inspection complete; 17 candidates held from layout use. These holds remain part of step 4's outstanding work.

- Downloaded 498 official raster images and 495 original EPS files covering the 263 selected identifiers and their linked alternatives. Retained original bytes, official URLs, dates and SHA-256 hashes.
- Decoded all raster images, recorded dimensions, transparency and 300 ppi size limits, and rendered all 495 EPS files successfully. Installed Ghostscript through Homebrew for this verification.
- Inspected 11 original-image and 11 rendered contact sheets, plus focused contrast and mismatch proofs. Saved 495 technical PNG renders without redrawing the artwork.
- Recorded 481 usable page candidates and 17 held candidates. Holds cover faint/outline artwork and web/EPS mismatches for T8, C45-7/8/9 and A29-17; T8 overlaps both groups. No held item has a recommended layout file.
- Both F1 variants are now local. F1-2, F8-2 and Y2 lack linked EPS files; their raster limits are recorded. Y2 is a static sound icon. Recorded duplicate web bytes for C45-6/C45-7 and preferred web images where EPS canvas or outline treatment is unsuitable.

**Deliverables:** [Asset package/readme](sign-assets/README.md), [structured manifest](sign-asset-manifest.json) and [validation results](sign-asset-checks.json). Original files total approximately 392 MB, plus generated renders and proof sheets.

**Verification:** All 993 original file sizes/hashes and 495 render hashes pass; official download domains, all 498 source-page relationships and preferred-file references resolve; raster decoding and EPS rendering have no failures. Every page candidate has a recorded quality status and visual-review reference.

**Handoff:** 4D must verify final labels and explanations and review content discrepancies; 4E must use only eligible images or explicitly record remaining gaps. Required held examples must be resolved or revised before 4F can declare the package complete. The final PDF must still be checked at actual size. No app assets, lessons, practice questions or PDF design were changed.

### Step 4D — Verify labels, explanations and accessibility text

**Completed:** 2 October 2026, following the user's request to execute 4D. **Status:** Caption requirements satisfied for usable assets; all 17 image holds remain.

- Saved official Swedish names, clearly marked editorial English labels, original teaching explanations and official-source references for 498 records: 263 selected identifiers and 235 additional linked pages.
- Added variant-specific alternative text and exact asset bindings for all 481 eligible images. Held images have no approved alternative text or preferred layout asset.
- Checked important exceptions and distinctions, including C6 trailers, C27 overtaking, speed recommendations, T20 free tickets, T24 charging capability, signal indications and the distinct M19a/M20a meanings. Rechecked visual details against the official-artwork proofs.
- Retrieved the five discrepancy pages again. They still link the conflicting artwork URLs; no official clarification resolved those issues. Preserved the original 4C manifest and all holds.

**Deliverables:** [Readable captions](sign-captions.md), [structured captions](sign-captions.json), [review and handoff](sign-caption-review.md), [validation results](sign-caption-checks.json).

**Verification:** Record and selection coverage, exact Swedish names, official source references and cached hashes, preferred asset hashes, readable/structured parity, required caption/alt fields and unchanged hold eligibility checked. English wording is editorial and has not been approved by an authority. No app tests were needed for this documentation-only step.

**Handoff:** 4E is next and has not started. Use only eligible image/caption pairs, retain size limits and record unresolved required examples. Step 4 remains in progress; 4F and final PDF verification are still required. No design, PDF generation, lesson placement or app changes were performed.

### Step 4E — Map verified signs to manuscript locations

**Completed:** 2 October 2026, following the user's request to execute 4E. **Status:** Editorial placement requirements satisfied, with unresolved images and contextual needs explicitly recorded.

- Mapped all 263 selected codes to 24 proposed Appendix B reference groups, with one primary entry per code and cross-references for repeated teaching uses. Retained all 18 catalogue families.
- Specified 54 lesson/review placements across 24 manuscript sections, each anchored to an exact paragraph and line in the unchanged manuscript. Recorded learning purposes, comparison instructions and related panels or variants.
- Chose 58 additional comparison variants. Bound 321 codes to their verified captions: 308 have eligible image paths, hashes, size limits and alternative text; 13 selected codes remain explicit image gaps. Four additional held optional variants are excluded. All 498 catalogue records have a placement/omission disposition.
- Wrote eight contextual illustration briefs for later design work. Preserved the exact parking-time composite and crossing-ID limitations, equipment text-only decisions and all original G01–G08 gap dispositions. No diagram or sign assembly was implemented or approved.
- Refined initial lesson associations to match the actual prose: weight/route limits belong with loading, service information with navigation, and rest-area recognition with fatigue planning. All selected codes remain in the reference.

**Deliverables:** [Readable placement map](sign-placement-map.md), [structured placement map](sign-placement-map.json), [placement checks](sign-placement-checks.json).

**Verification:** Passed selection coverage, unique reference entries, exact passage anchors, caption/asset hashes, bidirectional placement links, all 18 families, all 498 variant dispositions, retained holds and local document links. Input hashes confirm that manuscript, captions, assets and plan are unchanged. This is placement validation, not the broader 4F review or final print verification.

**Handoff:** 4F is next and has not started. Thirteen selected image gaps must be resolved or the selection explicitly revised before the whole package can be cleared. Four held optional variants remain excluded. Diagram briefs await step 5 previews and explicit design approval; PDF accessibility and actual-size legibility remain later checks. No manuscript, app or PDF changes were made.

### Step 4F — Verify the complete sign package

**Review performed:** 2 October 2026, following the user's request to execute 4F. **Completion gate:** Not met; step 4 remains in progress.

- Cross-checked 263 selected codes, 498 official page/caption records, reuse-policy links, 993 original assets, 495 saved EPS renders, 321 placement bindings, 54 lesson placements and 24 reference groups.
- All local integrity checks passed: files, sizes, hashes, decoded dimensions, source/asset/caption relationships, manuscript anchors, input versions and hold exclusions. Confirmed the known C45-6/C45-7 web-image duplicate without merging their identities.
- Consulted the current official reuse paragraph and re-inspected the saved contrast and variant-mismatch proofs. No evidence cleared the existing quality/identity holds.
- Recorded 13 selected image blockers. Four held optional variants remain excluded. Kept the existing text-only decisions and eight future-design briefs distinct from unresolved required artwork.

**Deliverables:** [Verification report](sign-verification.md), [structured checks](sign-verification-checks.json), [rerunnable verifier](verify-sign-package.py).

**Outcome:** The review ran successfully, but 4F is not marked completed because the plan requires all selected image requirements to be satisfied. Resolve or explicitly revise the 13 requirements, update dependent records and rerun the gate. No selected requirement was silently removed. Step 5, manuscript changes, app work and PDF production were not started.

### Step 5A — Design brief and readiness check

**Completed:** 2 October 2026, following the user's request to execute 5A.

- Saved [pdf-design-brief.md](pdf-design-brief.md) with audience, provisional A4 format, hierarchy, reading and accessibility targets, navigation, disclaimer and credit locations.
- Selected manuscript lessons, reference groups and placements for 5B–5E previews; carried forward all eight contextual diagram briefs and text-only restrictions.
- Reviewed existing 4F findings: 13 selected image gaps still block 5B; four optional held variants remain excluded. No new asset or factual verification is claimed.
- Preserved imagegen and explicit-approval checkpoints for later visual previews. No visual design, PDF or app implementation was performed.

**Verification:** Checked local brief links and referenced lesson, placement and reference-group identifiers against saved inputs; confirmed the exact disclaimer and all 13 blocker codes are included. The brief is complete under 5A's allowance to document unresolved step 4 gaps.

**Handoff:** Resolve the selected image requirements, update dependent records and rerun 4F before a separately requested 5B. Design and manuscript approval are not implied by completion of this brief.

### Step 5B — Cover and opening-page preview

**Prepared:** 2 October 2026. **Status:** Awaiting approval.

Saved [version 1 and review](pdf-design/5b/review.md) and the exact generation prompt. Visually checked the cover, full disclaimer and opening guidance. The user requested 5B after the blocker notice; this limited preview uses no held sign assets. All 13 required image gaps remain. No finished PDF, implementation or 5C work was started.

### Step 5E — Illustration and sign-layout previews

**Prepared:** 3 October 2026. **Status:** In progress, not complete.

- Saved a Swedish illustration style sheet, sign-reference layout, illustrated lesson/self-assessment samples and an exact-scenario parking timeline; retained exact generation prompts.
- Audited all 40 lessons and 10 reviews in the [coverage register](pdf-design/5e/illustration-register.md), with exact anchors and source links. Four sections retain text-only treatment with reasons; other scene briefs extend coverage to D30.
- Recorded each D01–D08 disposition, including deferred complex scenes. Checked 13 eligible sign-file hashes and saved asset/caption bindings and print-size constraints.
- Recorded current official police uniform evidence for the appearance study, visual corrections and limits. This is not approval of generated insignia or traffic gestures.

**Verification:** Coverage IDs and manuscript anchors checked; local sign-file hashes and documentation links verified. All 13 selected sign-image gaps remain. No claim that all required illustrations have been generated or approved.

**Handoff:** Review the [preview direction](pdf-design/5e/review.md), then resolve scene corrections, finish deferred required previews and obtain explicit approvals. 5D illustrated revision remains pending; 5F and production have not started.

### Step 5F — Consolidate design and review completion

**Performed:** 3 October 2026. **Status:** Deliverables saved; completion gate remains open.

Saved the [PDF design specification](pdf-design-spec.md), [completion review](pdf-design-review.md) and [verification snapshot](pdf-design-review-checks.json). Consolidated templates, typography, palette, page spacing, navigation, disclaimer, references, official-asset constraints and illustration decisions. Recorded the user's acceptance of the 5E illustration direction without clearing its known corrections or unproduced scenes.

**Verification:** Local links, current preview index, all 50 coverage IDs, exact disclaimer and reviewed input hashes checked. This is a consolidation review, not a new full legal or sign-asset audit.

**Outstanding:** Blockers F01–F08 cover the 13 required sign images, unproduced scene variants, parking geometry, timeline treatment, illustrated template completion, identity details and final complete-package approval. No new visual treatment or PDF implementation was produced. Step 5 stays in progress and step 6 has not started.

### Planning decisions recorded

- Saved the ten-step implementation plan with independent deliverables and approval checkpoints.
- Updated the curriculum approach so lesson objectives and factual support map to official sources only. Secondary reading is background, not the evidential basis for the curriculum.
- Required original structure, explanations and scenarios, with no third-party book references or source-book page numbers in learner-facing material.
- Added a requirement for a prominent introduction disclaimer: the book is a learning aid, is not an official source and cannot replace current official information and applicable rules.

The step 3 manuscript applies these requirements. App changes remain future work. Internal background records are not cited as evidence in the curriculum, source map or manuscript.

## Approval register

| Checkpoint | Status | Evidence / date |
|---|---|---|
| Execute step 1 | Authorised and completed | User explicitly requested step 1; completed 1 October 2026 |
| Execute step 2 | Authorised and completed | User explicitly requested step 2 and tracker update; 1 October 2026 |
| Curriculum outline | Approved | User explicitly approved version 1.0 on 1 October 2026: “yes approved” |
| Execute step 3 | Authorised and completed | User requested continuation: “yes go ahead”; completed 1 October 2026 |
| First-aid scope | Authorised | User permitted a brief 1177 reference with limited detail; 1 October 2026 |
| Manuscript | Prepared for review | Editable text completed; no separate user approval recorded |
| Execute step 4A | Authorised and completed | User requested “ok execute 4A”; completed 1 October 2026 |
| Execute step 4B | Authorised and completed | User requested “Go ahead with 4B”; completed 1 October 2026 |
| Execute step 4C | Authorised and completed | User requested “yes go ahead with 4C execution”; collection and inspection completed with recorded holds on 1 October 2026 |
| Execute step 4D | Authorised and completed | User requested “Go ahead with execution 4D”; completed 2 October 2026 with all 17 image holds retained |
| Execute step 4E | Authorised and completed | User requested “OK start execustion 4E step”; editorial map completed 2 October 2026 with explicit gaps |
| Execute step 4F | Authorised; review performed, completion blocked | User requested “OK go ahead with execution 4F”; reviewed 2 October 2026; 13 selected image gaps prevent sign-off |
| Execute step 5A | Authorised and completed | User requested “Go ahead and execute 5A”; brief completed 2 October 2026 |
| Execute step 5B | Preview prepared | User requested “OK go ahead with 5B”; sign-free preview prepared 2 October 2026 despite the prior sequencing gate; sign gaps remain |
| PDF design 5B | Approved | Version 4 and shared direction approved 2 October 2026: “OK, approved and go ahead 5C” |
| PDF design 5C | Approved | Navigation v1 approved 2 October 2026: “OK approved, go ahead with execution 5D” |
| Execute 5D | Authorised; previews submitted | [Lesson and companion-page previews](pdf-design/5d/review.md), awaiting explicit approval |
| Execute 5E | Authorised; in progress | User requested “OK great go ahead with 5E” on 3 October 2026; representative previews submitted, no approval inferred |
| 5E illustration direction | Accepted | User said “Looks great, go ahead with 5F” on 3 October 2026; known corrections and unseen scene approvals remain open |
| Execute 5F | Authorised; consolidation performed | [Specification and completion review](pdf-design-review.md) saved 3 October 2026; complete-package approval remains pending |
| Finished curriculum PDF | Approved screen edition | User: “OK approve 6N and move forward to 7C”, 14 October 2026; print masters explicitly deferred |
| App design | Complete package explicitly approved | User: “yes approved”, 15 October 2026; [8O final approval](app-design-review.md) |

Design revisions require renewed explicit approval before implementation, as specified in the plan.

## Outstanding handoff items

- **Step 2:** Complete. Preserve approved outline version 1.0 as the basis for step 3.
- **Step 3:** Complete. Preserve the manuscript and its evidence register; consult the [verification report](manuscript-verification.md) for all V01–V14 dispositions and scope limits.
- **Step 4:** Complete. All required sign gaps resolved; 321 bindings pass verification. Four optional mismatches remain excluded. Honour vector minimum reviewed sizes.
- **Step 5:** Prior cover/navigation approvals retained. Revised template, style, diagrams and chapter previews are indexed in the gap-resolution package; new design approval pending. Do not treat generated preview text or signs as production assets.
- **Step 6:** Preserve and visually verify the manuscript’s learning-aid disclaimer; obtain the required approvals and recheck dated requirements before release.
- **Steps 7–10:** Replace page-based app links and verify the final learner experience against the approved curriculum.

## Activity log

| Date | Update |
|---|---|
| 1 October 2026 | Completed step 1 and saved the source inventory, coverage records and sign inventory. |
| 1 October 2026 | Revised the plan to require an original curriculum supported by official sources only. |
| 1 October 2026 | Saved `implementation-plan.md` and added the required book disclaimer. |
| 1 October 2026 | Created this progress tracker. Steps 2–10 were not started at that point. |
| 1 October 2026 | Executed step 2: saved outline v1.0 and readable/structured official-source maps; verified links and reference coverage; submitted the outline for approval. Steps 3–10 remain not started. |
| 1 October 2026 | User approved outline version 1.0. Marked step 2 complete and recorded approval in the outline and source-map metadata. Step 3 awaits a separate execution request. |
| 1 October 2026 | Executed step 3 following user authorisation: saved the complete manuscript, 66-source manifest, 96-record evidence register and passing structural checks. Recorded the brief 1177 scope and V01–V14 dispositions. Steps 4–10 remain not started. |
| 1 October 2026 | Divided step 4 into independently requestable substeps 4A–4F, with inputs, deliverables and completion criteria. No sign-preparation substep was executed. |
| 1 October 2026 | Completed 4A: saved sign selection, lesson associations, variant needs and eight explicit gaps; verified selection against saved inventory and manuscript IDs. Step 4B is next. |
| 1 October 2026 | Completed 4B: retrieved 263 selected pages and 235 additional variants, recorded official reuse evidence and five held graphic requests, and verified register consistency. Step 4C is next. |
| 1 October 2026 | Executed 4C: collected 993 original files, rendered 495 EPS files, inspected artwork, saved size limits and integrity checks, and recorded 481 usable candidates plus 17 holds. Step 4D is next. |

| 2 October 2026 | Completed 4D: saved 498 officially sourced caption records, alternative text for 481 eligible images, reviewed exceptions and variant details, rechecked five discrepancy pages and retained all 17 image holds. Step 4E is next. |

| 2 October 2026 | Completed 4E: mapped 263 selected codes and 58 comparison variants into 24 reference groups and 54 lesson placements; wrote eight later-design briefs, retained 13 selected image gaps and four excluded optional holds, and passed placement validation. Step 4F is next. |

| 2 October 2026 | Executed the 4F review: all local integrity and relationship checks passed; saved the report and rerunnable verifier. Kept 4F and step 4 incomplete because 13 selected image gaps remain. Four optional held variants stay excluded; step 5 has not started. |

| 2 October 2026 | Executed 5A: saved the PDF design brief, representative preview content and readiness checklist; recorded the 13 sign blockers before 5B. Updated the 5A–5F tracker; no preview or implementation started. |

| 2 October 2026 | Prepared 5B cover/opening preview using imagegen following the direct execution request. Saved prompt and review, retained all sign holds and submitted v1 for explicit approval. |

| 2 October 2026 | Applied the user-requested KörkortGo name to the manuscript, brief and plan; generated cover/opening preview v2 and saved its prompt. Version 2 awaits explicit approval. Refreshed placement input bindings after the title-only manuscript change; historical validation snapshots remain dated evidence. |

| 2 October 2026 | Revised 5B to version 3 using both supplied app mockups as brand references: forest green, sage, off-white and a car on a Swedish lakeside road. Saved revised prompt and preview; updated the brief. Explicit approval remains pending. |

| 2 October 2026 | Prepared 5B version 4: retained the driving-cover direction and restored the opening page’s first-draft navy, cream/gold and muted icon colours at the user’s request. Updated brief and review; approval pending. |

| 2 October 2026 | Documented the shared [KörkortGo design guide](../../design/brand/README.md), colour/type tokens and light/dark Material roles following user acceptance. Recorded the restricted muted-on-sage pair and verified darker replacement. No app theme or PDF implementation; 5C not started. |

| 2 October 2026 | Recorded 5B v4/design-direction approval and executed 5C. Saved contents, module opener and running-navigation preview with illustrative folios, source destinations and review notes. 5C awaits approval; 5D not started. |

| 2 October 2026 | Recorded 5C approval and executed 5D: saved two imagegen boards covering three lesson excerpts, reflection, glossary and practice record. Documented source/navigation corrections and illustration placeholder scope. Awaiting 5D approval; 5E not started. |

| 2 October 2026 | Added mandatory illustration instructions for lesson and self-assessment scenarios, official signs and consistent Swedish vehicles, roads, police and people. Updated the design guide, brief and plan; 5D requires illustrated revisions before approval. No new artwork or book implementation in this update. |

| 3 October 2026 | Executed 5E preview work: saved style, sign layouts, scenario v2 and parking timeline; audited all 50 curriculum sections and recorded every D01–D08 disposition. Step remains in progress with required diagrams, corrections, approvals and 13 sign holds outstanding. |

| 3 October 2026 | Accepted 5E direction and executed 5F consolidation. Saved design specification, approval index, F01–F08 blockers and review snapshot. Step 5 remains incomplete; no PDF production started. |

| 3 October 2026 | Divided step 6 into independently requestable substeps 6A–6N, including one build per chapter (6B–6K). Added chapter inputs, deliverables and verification criteria plus the matching tracker. Existing approval/blocker requirements remain; no production executed. |

| 3 October 2026 | Started 6A at the user’s request. Checked entry requirements and saved readiness review, shared chapter/navigation manifest and integrity preflight. Required design/asset work and final approvals remain unresolved; no PDF generated, 6A not complete. |

| 3 October 2026 | Resolved all 13 selected sign gaps using exact official poster vectors at reviewed sizes; refreshed captions, bindings and verifier. All checks pass; step 4 completed. Continuing illustration revisions under the user’s request; new previews still require approval. |

| 3 October 2026 | Recorded explicit approval of M02-v3 (chapter 2 board). Sequential illustration review moved to M03-v3; parking-v3 and chapters 3–10 remain unapproved. |

| 3 October 2026 | M03-v3 reviewed by the user: corrections requested for the L02 junction scene and the M03-R queue panel (direction separation, consistent lane count, stop line before the junction). Saved the v4 edit prompt; revised preview pending generation. |

## Keeping this tracker current

After work on a step, update its status, completion details, deliverable links, verification results and outstanding issues. Record user approvals with the date and approved version or artifact. Append a dated activity entry and update the current position and next action. Use “Awaiting approval” when a deliverable is ready but its approval checkpoint has not been met; do not infer approval from elapsed time or an unrelated request.

## Gap-resolution update — 3 October 2026

Resolved all 13 selected sign assets using official vectors; verified all 321 bindings and pixel-identical cleaned extracts. Prepared revised illustration boards across the ten chapters, corrected parking geometry and timeline assessment separation, and added the illustrated official-advice template. Updated all 50 section mappings, retaining four text-only sections. [Review the current package](pdf-design/gap-resolution/README.md). New previews await explicit approval; no production book PDF has been created. Earlier dated blocker entries are retained as history.

**M10 preview revision 3:** Separated the motorway and tunnel scenario cards after user feedback. Updated preview links; approval remains pending.

**M10 preview revision 4:** Removed the fence obstructing the emergency exit in panel C; open doorway and clear walking route now visible. Updated current preview references. Awaiting approval before implementation.

**Sequential illustration review — M01 revision 2:** Replaced paper map in M01-L04 with a tablet map. Current chapter 1 preview awaits user comments/approval before the next preview. Companion F06 template must also use digital maps when reviewed.

**Chapter 1 v2 approved:** User explicitly approved M01-v2. Companion illustrated lesson template remains under review and must replace its paper map with a digital map before approval.

**Companion F06 v3:** Applied digital-map preference and corrected both people’s gaze toward the tablet after user feedback. Preview awaits approval; sequential review remains on this layout.

**Companion F06 v4:** Corrected physically reversed tablet presentation using an over-the-shoulder camera angle; screen faces both people. Awaiting user approval before advancing the sequential review.

**Companion F06 v4 approved:** User explicitly approved the corrected over-the-shoulder tablet layout. Chapter 1 board and companion template now approved. Sequential review advances to Chapter 2 M02-v2; no approval inferred for that preview.

**M02 v3 review revision:** Corrected rear seats to face the vehicle front, included empty child restraint with child outside, and clarified left-hand-drive cabin and driver position. Awaiting approval before next sequential preview.

**Chapter 2 v3 approved:** User explicitly approved M02-v3 on 3 October 2026 (“Approved, go ahead with the next preview M03”). The approval covers the chapter 2 board only; the companion parking-v3 scene is still awaiting approval. Sequential review advances to Chapter 3 M03-v3; no approval inferred for that preview.

**M03 v3 review feedback (3 October 2026):** Not approved. The user asked for corrections to M03-L02 and the matching M03-R queue panel: separate the learner's direction from oncoming traffic, keep the number of lanes consistent through the scene, and place the stop line correctly before the junction with the car behind it. The v4 edit prompt is saved as [prompt-M03-v4.md](pdf-design/gap-resolution/prompt-M03-v4.md); the revised image has not yet been generated.

**M02 v3 approved:** User approved rear-seat orientation, child-restraint context and left-hand-drive cabin revision. Next preview: parking-v3, shared by M02 review and M05-L04.

**Parking v3 approved:** User approved the parking/reversing preview. Sequential review advances to Chapter 3 M03-v3; approval for that board remains pending.

**M03 v4:** Corrected opposing-flow separation, consistent lane counts and near-side stop-line placement in both lesson and review scenes. Sequential review remains on Chapter 3 pending approval.

**M03 v4 approved:** User approved corrected lesson and review road geometry. Sequential review advances to D01-v2; its approval remains pending.

**D01 v2 approved with additional example planned:** Existing junction board approved; user authorised a separate priority-road illustration. New B4 priority-road scene remains required and must be previewed before implementation. Sequential review now presents D02-v2 crossings.

**D02 v3:** Reframed panel D to show roadway around the smaller roundabout island and adequate exit road space. Sequential review stays on this preview pending user approval.

**D02 v4:** Revised panel D again after feedback on unrealistic connecting roads. Approach widths now consistent with the exit and compact roundabout; approval remains pending.

**D02 v4 approved:** User approved the crossing comparison and corrected roundabout geometry. Sequential review advances to D04-v1, lane changes and joining traffic; approval pending.

**D04 v3:** Corrected blocked right turn and interrupted cycle path in panel 4; aligned cyclist with continuous passage. Sequential review remains on D04 pending approval.

**D04 v3 approved:** User approved lane situations and corrected right-turn/cyclist panel. Sequential review advances to D05-v2 roundabout preview; approval pending.

**D05 v3:** Added give-way and roundabout signs to picture 1. Placement preview pending approval; final sign faces must use exact official assets.

**D05 v3 approved:** User approved roundabout approach sign placement. Sequential review advances to M04R-v3 shared-space self-assessment; approval pending.

**M04R v3 approved:** User approved Chapter 4 shared-space self-assessment. Sequential review advances to Chapter 5 M05-v1; approval pending. Additional priority-road preview remains outstanding.

**M05 v2:** Added realistic lane space beside the bus and matched the review scene. Learner stays behind the bus; approval pending.

**M05 v2 approved:** User approved the revised busy-streets chapter board. Sequential review advances to D03-v1 stopping restrictions and distance boundaries; approval pending.

**D03 v1 approved:** User approved stopping-restriction distance boundaries. Sequential review advances to timeline-v3 parking-time exercise and worked review; approval pending.

**Timeline sign addition authorised:** User approved the proposal to add matching parking signs to exercise and worked answer. Revised verified sign assembly and image review remain outstanding. Sequential review advances to Chapter 6 M06-v1.

**M06 v1 approved:** User approved Chapter 6 illustrations. Sequential review advances to Chapter 7 M07-v1; approval pending.

**M07 v1 approved:** User approved Chapter 7 illustrations. Sequential review advances to Chapter 8 M08-v1; approval pending.

**M08 v2:** Corrected left red/yellow roadwork marker orientation toward the road. Sequential review remains on Chapter 8 pending approval.

**M08 v2 approved:** User approved Chapter 8 illustrations with corrected marker orientation. Sequential review advances to Chapter 9 M09-v2; approval pending.

**M09 v2 approved:** User approved Chapter 9 illustrations. Sequential review advances to Chapter 10 M10-v4; approval pending.

**M10 v4 approved:** User approved Chapter 10 illustrations. Sequential review advances to shared style-v2; additional priority-road and parking-sign visuals still require generation and review.

**Style v2 approved:** User approved shared illustration style. Preparing the additional priority-road preview; parking-sign preview also remains outstanding.
 
**D01 priority road preview prepared (v3):** Generated [D01-priority-v3](pdf-design/gap-resolution/D01-priority-v3.png) matching Swedish traffic law: B4 Priority Road sign positioned after the intersection in the direction of the blue car; B1 Give Way sign and M1 shark's teeth at the head of the side road where the yellow car stops; clean corner before the junction. Awaiting user approval; parking-sign timeline preview remains outstanding.

**4 October — priority-road v3:** Saved added priority-road scene, corrected side-road lanes and moved B4 after the junction following user feedback. Awaiting approval. Parking-sign timeline revision remains outstanding.

**4 October — priority-road v3 approved:** User explicitly approved B4 placement after the junction. Next review: parking timeline with signs.

**4 October — timeline v4 prepared:** Added parking sign and combined 2 tim / 9–18 plate to both pages, checked against official T18/T6 guidance. New visual awaiting approval; final production retains exact E19 artwork and clearly labelled illustrative conditions.

**4 October — timeline v4 approved:** User approved the added parking signs. All chapter/scenario previews presented in the sequential review, including the priority-road addition, have now received visual approval. Next shown for review: existing sign-reference layout (5E sign-layouts-v1), whose direction was previously accepted. Production asset, typography and accessibility checks remain.

**4 October — sequential visual review completed:** User approved sign-layouts-v1. All 21 current illustration/layout boards in the versioned approval record now have explicit approval. No further unseen chapter preview is queued. Final production checks and 6A PDF generation remain; later chapters are separate steps.

**4 October — 6A executed:** Built four opening pages using the approved design and complete manuscript introduction; bundled four exact fonts with OFL licences, shared editable templates, navigation/asset manifests and reproducible build instructions. Rendered all pages and checked source fidelity, embedded fonts, glyphs, five links, four bookmarks/destinations and deterministic output. Sign verification passes 321/321 bindings. Screen review only: print-resolution cover artwork and full accessibility certification remain release work. Stopped before 6B.

**4 October — 6B executed:** Built Chapter 1 with all four complete lessons, four approved scene crops, self-assessment, reflection space and separately placed answers. Rechecked all 11 official references; no manuscript changes needed. Inspected all 15 rendered pages; fidelity, embedded fonts, 34 internal links, 16 destinations, answer separation and deterministic-build checks pass. Source, asset and verification records saved beside the chapter PDF. No sign artwork is required in M01. Print-resolution masters and full release accessibility remain later work. Stopped before 6C.

**4 October — 6C executed:** Built Chapter 2 with four complete lessons, six approved illustration placements, self-assessment, reflection space and separate answers. Rechecked 11 official references, including child-restraint exceptions/advice, lighting and vehicle-control requirements. Preserved the corrected rear-seat orientation, child outside the vehicle, left-hand driver and separated parking/footway/access-lane geometry. All 15 pages inspected; text fidelity, font embedding, 34 internal links, 16 destinations, answer separation and reproducibility checks pass. No road signs are required for M02. Print masters, final global navigation and full accessibility certification remain later release work. Stopped before 6D.

**4 October — 6D executed:** Built Chapter 3 with all four lessons, the five-family comparison table, seven approved scene placements, self-assessment, reflection and separate answers. Included all 14 required sign groups: 100 official placements using 96 distinct assets, plus review cross-links; ten vector placements retain reviewed minimum widths. Rechecked the seven chapter reference targets and reused verified individual official sign captions/artwork with hash and size checks. All 50 pages inspected; 42 content blocks, font embedding, 60 internal links, 56 destinations, answer separation and deterministic-build checks pass. Approved scene print masters and final accessibility/global assembly remain later work. Stopped before 6E.

**4 October — 6E executed:** Built Chapter 4 with four complete lessons, the crossing-duty table, 20 approved scene placements, self-assessment, reflection and separate answers. Included all eight required groups with 46 official reference placements (44 distinct assets), plus nine exact official scene sign insertions. Preserved the priority-road sign after the junction, open cyclist/right-turn passage and approved roundabout geometry. Labelled the single-lane review preview as a companion detail and added the approved two-lane scene to support the unchanged manuscript. Rechecked seven chapter reference targets. All 42 pages inspected; 38 manuscript blocks, embedded Unicode fonts, 50 internal links, 49 destinations, answer separation and reproducible-build checks pass. Print masters and final accessibility/global assembly remain later work. Stopped before 6F.

**5 October — 6F executed:** Built Chapter 5 with all four lessons, the stopping/parking table, nine approved scene placements, the parking-time exercise and separate worked timeline, self-assessment and reflection. Included all 12 required groups: 62 official reference placements using 57 distinct assets, plus two scene insertions and two E19 example placements. T6/T8 retain official vectors at reviewed widths. Preserved the bus lane width and separated parking-bay/footway/access-lane layout. Both time examples use the same explicitly illustrative 2 tim / 9–18 plate; the 12:00 answer is absent from the question page. Rechecked seven chapter references plus T6/T18. All 44 pages inspected; 42 manuscript blocks, disclaimer, font embedding, 52 internal links, 53 destinations, answer separation and deterministic rebuild checks pass. Print masters and final accessibility/global assembly remain later work. Stopped before 6G.

**5 October — 6G executed:** Built Chapter 6 with all four lessons, 13 approved scene placements, self-assessment, reflection and separate answers. Included all nine required groups with 76 exact official reference assets. Preserved the approved motorway-entry/exit details and rural/railway/roadwork scenes; approved lesson crops complete the written review scenario while the ordinary junction remains clearly labelled. Rechecked all seven chapter reference targets, including railway emergency distinctions and current vehicle-limit provisions. All 48 pages reviewed; 40 manuscript blocks, exact disclaimer, font embedding, 55 internal links, 54 destinations, answer separation and deterministic rebuild checks pass. Print masters and final accessibility/global assembly remain later work. Stopped before 6H.

**5 October — 6H executed:** Built Chapter 7 with all four lessons, eight approved scene placements, self-assessment, reflection and separate answers. Included all four placement groups with six exact official reference assets. Preserved the parked left-hand-seat attention scene and neutral departure/rain/darkness/delay review sequence. Rechecked all ten chapter references, including lighting, ordinary light-vehicle tyre rules, friction/ABS limitations and communication-equipment restrictions. All 23 pages reviewed; 39 manuscript blocks, exact disclaimer, font embedding, 30 internal links, 27 destinations, answer separation and deterministic rebuild checks pass. Print masters and final accessibility/global assembly remain later work. Stopped before 6I.

**7 October — 6I completed:** Built Chapter 8 with all four lessons, four approved scene placements, the weight-definition table, self-assessment, reflection and separate answers. Included all three required groups with nineteen exact official reference assets, including six poster vectors, and eight official marker-face insertions preserving the approved roadwork directions. Eighteen chapter reference targets were checked on 5 October, as recorded in the source checks. All 29 pages visually reviewed; 42 manuscript blocks, exact disclaimer, font embedding, 36 internal links, 30 destinations, answer separation and deterministic rebuild checks pass. Print masters and final accessibility/global assembly remain later work. Stopped before 6J.

**7 October — 6J completed:** Built Chapter 9 with all four lessons, four approved scene placements, self-assessment, reflection and separate answers. Included both required groups with ten exact official reference assets and one official class-2 zone-sign insertion. Rechecked all nine chapter reference targets. All 22 pages visually reviewed; 37 manuscript blocks, exact disclaimer, embedded fonts, 29 internal links, 25 destinations, answer separation and deterministic rebuilding pass. Print masters and final accessibility/global assembly remain later work. Stopped before 6K.

**7 October — 6K completed:** Built Chapter 10 with all four lessons, eight approved scene placements, five native journey-review frames, reflection and separate answers. Included both required groups with ten exact official reference assets and two official scene insertions. Preserved separated A/B/C breakdown situations and the open tunnel exit. Rechecked ten chapter reference targets; first aid remains a brief 1177 referral. All 23 pages visually reviewed; 43 manuscript blocks, exact disclaimer, embedded fonts, 30 internal links, 24 destinations, answer separation and deterministic rebuilding pass. All ten individual chapters are now complete for screen review. Print masters, reference material, final accessibility and book assembly remain later work. Stopped before 6L.

**7 October — 6L completed:** Built all four appendices, all 24 required sign-reference groups with 321 unique exact official entries (including 13 vector placements), the 23-term glossary, nine practice prompts and all 66 manuscript official references. Preserved source-check dates, editorial-translation labels, artwork credit and the learning-aid disclaimer. Checked 388 distinct link targets: 386 HTTP successes and two successful browser fallbacks. All 183 pages visually reviewed; manuscript/asset coverage, font embedding, 554 internal links, 505 destinations and deterministic rebuilding pass. Added a linked RB06 overview to preserve vector size. Updated only the production snapshot’s obsolete statement that the illustrated reference was still pending. Full-book navigation, final folios, tagged accessibility and publication approval remain 6M–6N. Stopped before 6M.

**7 October — 6M completed:** Assembled the front matter, all ten chapters and complete reference material into one 498-page screen-review book. Replaced the provisional contents and all standalone footers with book-wide folios, Contents/Sources access and previous/next links. Added 589 lesson/sign cross-links, 914 named destinations and nested bookmarks. All 40 lessons, ten self-assessments and four appendices occur once in the assembled page sequence; question/answer separation remains at least two pages. Verified all 1,633 original body links, 3,037 internal links, 389 external URL targets, font embedding and byte-identical rebuilding. Rendered all 498 pages; the 497 preserved page bodies match source renders pixel for pixel, with the new contents and 31 opening/boundary/reference pages visually inspected. Source PDFs and assets remain unchanged. Final full-book publication, factual and accessibility checks remain 6N. Stopped before 6N.


## G1 amendment — 12 October 2026

Chapter 1 adds verified teaching for situation-062, 068, 069 and 129. Exact evidence, fallbacks and scope limits: [G1 evidence](question-book-review/g-step-changes.json#/records/G1~1evidence.md). Existing verification dates remain historical. Final assembly and whole-book audit await G11/G12.


## G2 amendment — 12 October 2026

M02-L01–L03 add ten driving-situation questions, with twelve essential claims. Exact evidence, fallbacks and applicability limits: [G2 evidence](question-book-review/g-step-changes.json#/records/G2~1evidence.md). Original check dates remain historical. Final assembly and whole-book audit await G11/G12.


## G3 amendment — 12 October 2026

M03-L04 adds the fixed-point timing method, tailgater response and qualified squared-speed braking relationship for situation-106, 107 and 138. Exact evidence, searches and hypothetical arithmetic: [G3 evidence](question-book-review/g-step-changes.json#/records/G3~1evidence.md). Original checks retain their dates. Final assembly/audit await G11/G12.


## G4 amendment — 13 October 2026

M04-L02 adds waiting-to-turn wheel position, rear-impact reasoning, an example and an answered check for situation-104. Classified as safety advice. [Evidence and fallback](question-book-review/g-step-changes.json#/records/G4~1evidence.md). M06-L01 cross-reference only; G6 teaching not implemented. Final assembly/audit await G11/G12.


## G5 amendment — 13 October 2026

M05-L01 adds the bus road-limit comparison, guide-dog interaction advice and bicycle-as-vehicle definition for situation-013, 119 and 135. Five essential claims verified. [Evidence and scope](question-book-review/g-step-changes.json#/records/G5~1evidence.md). Original bus example extended; other lessons unchanged. Final assembly/audit await G11/G12.


## G6 amendment — 13 October 2026

M06-L01 adds conditional rural turn planning and wildlife cues; M06-L03 adds speed-perception adaptation and a motorway transition example, for situation-075, 105 and 126. Three claims checked with explicit scope. Rural return-right routing is an editorial application of a Trafikverket example and current Swedish rules. [Evidence](question-book-review/g-step-changes.json#/records/G6~1evidence.md). Other lessons and review unchanged. Final assembly/audit await G11/G12.


## G7 amendment — 13 October 2026

M07-L01 adds explicit lighting combination, visual roles and single-light width caution. M07-L02 adds bridge/ice/first-rain mechanisms, rear tyre stability, grip-loss handling definitions and aquaplaning response. Short attention cross-link in M07-L03; M07-L04/review unchanged. Twelve questions and thirteen claims checked with stated scope. [Evidence](question-book-review/g-step-changes.json#/records/G7~1evidence.md). Final assembly/audit await G11/G12.


## G8 amendment — 13 October 2026

M08-L01 adds light/heavy lorry speed comparison; L02 adds coupling-force/front-axle explanation and load example; L03 adds automatic inspection ban, restricted trips and deadline example. Three questions/claims checked. M08-L04/review unchanged. [Evidence](question-book-review/g-step-changes.json#/records/G8~1evidence.md). Whole-book assembly/audit await G11/G12.


## G9 amendment — 13 October 2026

M09-L01 adds fossil-carbon/catalyst and pollutant comparison, powertrain types and washing; L02 adds heater/cooling/gear/deceleration/cargo examples; L04 adds stud particles/local restrictions. Fifteen questions and 22 claims checked. L03/review unchanged. [Evidence](question-book-review/g-step-changes.json#/records/G9~1evidence.md). Whole-book assembly/audit await G11/G12.


## G10 amendment — 13 October 2026

M10-L01 adds hot-coolant pressure/burn mechanism, closed-cap precaution and overheating decision integrated with road/tunnel scene safety. One question/claim verified; L02–L04/review unchanged. [Evidence](question-book-review/g-step-changes.json#/records/G10~1evidence.md). G11/G12 assembly and final audit pending.


## G11 assembly — 13 October 2026

Verified 540-page revised assembly (+42: 24 chapter, three glossary, 15 central references). Original 498-page copy retained. All approved chapter teaching preserved; 55 questions mapped to actual assembled pages, pending G12 independent audit. [Completion](question-book-review/g-step-changes.json#/records/assembly-completion.md).


## G12 coverage audit — 13 October 2026

All 1000 questions reviewed: 772 covered, 158 missing exact sign entries, 70 prompt-only calculations. All 55 assigned gaps/68 claims verified; 20 additional braking exercises gained support. No regressions or PDF/bank changes. [Final audit](question-book-review/g-step-changes.json#/records/final-coverage-review.md). Minor wildlife cross-reference observation recorded for later correction.

**14 October — 7A audit performed:** Recorded 163 source/evidence input hashes and all 343 bundled asset hashes, the matching 578-page source/delivery PDF identity, 1,000 unique question IDs, 500 concepts and 39 legacy chapter ranges. JSON/generated Kotlin parity and sign/coverage hashes pass. README chapter count is stale; no durable learner progress or bookmarks exist in audited source. No 6N final verification/approval is recorded, so the baseline is provisional and 7A remains in progress. App sources, question bank and PDFs were unchanged; 7B was not started.

**14 October — 7B planning performed:** Following the request to proceed, preserved exact titles and stable IDs for 10 modules, 40 lessons and 10 reviews, registered four appendices, 24 sign groups and all 1,123 published book destinations. Defined versioned content, question relationships, source classification, asset and navigation fields, with required app model/import changes. Verified frozen inputs and source-destination resolution. No legacy chapter structure adopted, question mapping, app implementation or design performed. Final release verification/approval remains pending; 7C not started.

**14 October — 6N review and correction:** Verified the 578-page book, 3,525 internal links, 1,123 destinations, 571,819 text characters within page bounds, embedded Unicode fonts, exact disclaimer and legacy-book-name exclusion. Revalidated all 1,000 H7 teaching-evidence records and hashes for 729 sign placements (400 unique files); all 517 external URLs have successful responses or content fallbacks. Corrected page 193 wildlife-collision reference to M10-L02, rebuilt Chapter 6 and the complete book deterministically, and saved a screen-review candidate and verification report. Missing semantic tagging/assistive reading-order validation and low-resolution scene/cover print masters remain holds. No final approval recorded. 7A–7B old release hashes are explicitly superseded pending refresh; no further app migration performed.

**14 October — candidate approved:** User explicitly replied “OK approved” to the 578-page 6N review candidate. Recorded its exact SHA-256 in [approval-record.json](pdf-production/final-review/approval-record.json). Accessibility/print requirements were not waived or marked passed; 6N remains in progress. No subsequent step was started.

**14 October — 6N accessibility continuation:** Produced a separate 578-page tagged candidate with semantic heading/list/table/figure/link structure. veraPDF PDF/UA-1 machine validation and independent parent/navigation checks pass; all 578 pages retain the approved rendered appearance. Representative macOS Preview accessibility and link-activation checks recorded, with no exhaustive VoiceOver claim. Original approval identity retained. Cover preview awaits approval and is below the 300 ppi print target; print/outline proof requirements remain open. 6N remains in progress; 7C not started. [Current evidence](pdf-production/accessibility/verification.json).

**14 October — cover direction approved and print work scoped:** Recorded “ok cintinue” as approval of the presented cover's visual direction. Audited all 83 recorded scene placements / 79 distinct source crops against the 300 ppi target and saved minimum replacement dimensions. All remain below target; cover also below target. Asked whether to finish a screen edition with print deferred or continue full print production. No PDF artwork replacement or next migration step performed. [Print work](pdf-production/print-masters/README.md).

**14 October — screen edition selected:** User explicitly chose “Finish the screen edition; defer print masters”. Recorded print work as deferred and promoted the verified tagged bytes to the release filename and output copy. Exact rebuild/delivery parity passes. Original untagged approval copy preserved. 6N is **Awaiting approval** of the finished tagged screen candidate; print work is not certified, and app migration has not resumed. [Release scope and identity](pdf-production/final-review/screen-release.json).

**14 October — 6N approved; 7C completed:** User explicitly said “OK approve 6N and move forward to 7C”. Closed 6N for the tagged screen edition, with print work deferred. Refreshed 7A–7B release/input bindings and retained original snapshots. Mapped all 1,000 unchanged question IDs to primary lessons, supporting passages and source evidence; all destination/hash/passage checks pass. No unmatched or ambiguous mappings. Preserved 616 exact sign questions, 55 reviewed claim associations and four fuel-rounding qualifications. Three lessons lack primary bank questions (M01-L01, M07-L04, M10-L03); M07-L04 is related once. No question/app/PDF changes; 7D not started. [Review](app-migration/question-map-review.md), [checks](app-migration/question-map-checks.json).

**14 October — 7D completed:** Reviewed all 178 scenarios and option explanations, 308 sign codes in both question directions, all 206 arithmetic/rule instances and ten paired asset sheets. Assigned 336 retain, 626 rewrite, 38 replace, zero remove. Saved concrete patches/briefs and source-backed acceptance criteria. Sign revisions remove pre-answer code cues, separate assessment descriptions from study captions and align exact-code feedback. Nineteen faint-outline codes require replacement delivery for 38 questions before scored use. Four fuel questions propose exact unrounded keys; 30 load prompts define driver-inclusive tjänstevikt; eight scenario and six singular-unit edits are recorded. Current numeric keys agree with the printed model/convention, with the four qualifications retained. Targeted official checks and frozen-input/asset/proposal validation pass. No live bank, app, asset or PDF changes; 7E not started. [Review](app-migration/question-actions.md).

**14 October — 7E completed:** Mapped all 1,000 question links, 39 old chapter aliases, the 361-integer legacy page span, 178 unused generated topics, 343 sign records, five categories, eight navigation states and 22 transient/progress contracts. Exact question IDs override old pages; multi-topic aliases use canonical choices and unknown routes never open the first chapter. Preserved quiz categories/quotas and defined versioned session/answer rules without inventing a durable learner store. 340 sign codes resolve exactly; SIG16–18 have explicit unavailable/official-source fallback policies for 7F. Recorded learner-facing book/publisher/page label replacement and synthetic retained/changed/replaced/retired examples; zero real question removals/tombstones. Frozen-input, destination, compatibility and deterministic rebuild checks pass. App, questions, assets and PDF unchanged; 7F not started. [Review](app-migration/link-and-progress-map.md).

**14 October — 7F completed:** Prepared 15 dependency-ordered step 9 work items with affected files, outputs and acceptance criteria. Assigned every baseline question to one content owner with exact 7C/7D pointers and batches of at most 50; preserved 336 retain, 626 rewrite, 38 replace and zero remove. Covered all 1,123 published destinations, 7D issues/coverage briefs and 7E route/state/label rules. Chose the existing explicit unavailable internal policy for SIG16–18, retaining recorded official links and related teaching without adding unverified entries. Saved exact library, M03-L02 reader, retained/proposed answer-review, B1 reference, classified-source and legacy/fallback fixtures for future step 8. Specified ten future step 10 verification cases. All 68 local handoff checks pass, including protected baseline/asset hashes and deterministic rebuild. No live app/question/asset/PDF changes; no visual design generated. 7G remains next; step 8 still requires imagegen and explicit approval. [Backlog](app-migration/implementation-backlog.md), [preview handoff](app-migration/preview-handoff.md), [checks](app-migration/handoff-checks.json).

**14 October — 7G passed; step 7 complete:** Freshly reran the 7C–7F validators and independently checked cross-stage input identities, release copies, canonical structure/folios/source locations, all 1,000 question IDs and original payloads, 500 concepts, dispositions, exact teaching/source routes, 400 sign bindings, 2,464 proposed sign-option asset/source bindings, 83 lesson scene placements, 329 chapter sign placements, 404 question URL evidence records, 22 state contracts, backlog dependencies/ownership and preview fixtures. All 60 cross-stage checks pass; the current 7F checks also pass 68/68. All 177 frozen baseline input records and 343 bundled asset records match; current app source inventory remains covered. No blocking migration-planning issues remain. The 626 rewrites and 38 replacements remain unapplied; intended-size/accessibility proof, time-sensitive source rechecks and implementation/device acceptance remain future work. SIG16–18 retain the explicit unavailable/official-link/related-teaching policy; no sign substitution or new approval. No app, question, asset or approved PDF changes. Step 8 is next, separately requested, with imagegen previews and explicit design approval required. [Verification report](app-migration/verification.md), [results and input manifest](app-migration/verification.json).


**14 October — 8A completed:** Prepared the app-preview brief from the verified migration handoff, exact fixtures, current shared app source, brand tokens and historical mockups. Bound every 8B–8M preview to exact copy/assets or approved production/legacy records, including the M03-L04 calculation excerpt and page-46 chooser targets. All 466 stored 7G input-manifest hashes and the explicit preview input/reader/B1 bindings match. Recorded approval workflow, accessibility/reflow requirements, 626 rewrite/38 replacement limits, SIG16–18 policy and remaining implementation/device checks. No imagegen preview, new visual design, approval, app/question/asset/PDF change or 8B execution. [Brief](app-design/brief.md), [readiness](app-design/readiness.json).


**14 October — 8B v1 generated:** Used the built-in imagegen tool to produce wide and phone learning-library previews with exact module-3 titles, canonical numbering, teaching totals and Sources/reference actions. Saved the prompt, exact fixture/output bindings and visual review. Recorded the stray header mark and unbound menu/language controls as generated deviations, with no new functionality inferred. Awaiting explicit user feedback/approval; 8B is not complete and 8C has not started. No implementation, question, official asset or approved PDF changes. [Preview/review](app-design/8b/review.md).


**14 October — 8B v1 approved:** User explicitly said “Looks great, approved”. Recorded approval against the saved v1 preview and content bindings; 8B is complete. Header rendering deviations remain documented, with no new unbound menu/language functionality inferred. 8C is next only when separately requested; no implementation started. [Approval record](app-design/8b/review.md).


**14 October — 8C v1 generated:** Saved built-in imagegen boards for Traffic safety filtering and empty search, each with wide/phone layouts. Verified module 3 matches M03-L02–L04 in canonical order against category and lesson tags. Saved exact fixtures, action/reset contracts, prompts, output hashes and review notes. Awaiting explicit user approval; 8D remains unstarted. No app, question, official asset or PDF changes. [Review](app-design/8c/review.md).


**14 October — 8C v1 approved:** User explicitly said “yes looks great, approved”. Recorded approval for both filter and empty-search boards in the review and exact bindings; 8C is complete. Documented runtime/accessibility requirements remain future checks. 8D is next only when separately requested; no implementation started. [Approval record](app-design/8c/review.md).


**14 October — 8D v1 generated:** Saved a built-in imagegen wide/phone lesson-reader preview using exact M03-L02 goal, opening requirements, citation and M03-L01/M03-L03 navigation. Frozen source hash matches. Saved prompt, exact content/navigation bindings and review, including the opening-only preview boundary and actual reading-width/reflow requirements. Awaiting explicit approval; 8E unstarted. No implementation, question, official asset or PDF changes. [Preview/review](app-design/8d/review.md).


**14 October — 8D v1 approved:** User explicitly said “approved”. Recorded approval against the saved lesson-reader preview and exact content bindings; 8D is complete. The opening-only boundary and full-content/runtime requirements remain documented. 8E is next only when separately requested; no implementation started. [Approval record](app-design/8d/review.md).


**14 October — 8E v2 generated:** Prepared built-in imagegen before/after answer-reveal reader details for wide and phone layouts. Corrected the initial phone proportions before presenting v2. Exact M03-L02 question/answer and frozen source hash checked; saved prompt, bindings and reveal/focus/accessibility requirements. Hidden answers must be excluded from assistive reading until deliberate reveal; actual semantics remain future verification. Awaiting explicit approval; 8F unstarted. No implementation, question, official asset or PDF changes. [Preview/review](app-design/8e/review.md).


**14 October — 8E v2 approved:** User explicitly said “approved”. Recorded approval against the saved wide/phone reveal preview and exact bindings; 8E is complete. Accessibility/reveal behaviour remains subject to actual implementation verification. 8F is next only when separately requested; no implementation started. [Approval record](app-design/8e/review.md).


**14 October — 8F v1 generated:** Saved a built-in imagegen long-content/calculation preview at wide regular, phone regular and phone enlarged text. Used M03-L04 Example B with rough equations and scope sentences; source hash and independent 21/19.6/40.6 m arithmetic pass. Saved complete original context blocks, prompt, bindings and review, retaining font/viewport/scale deviations and runtime reflow requirements. Awaiting explicit approval; 8G unstarted. No implementation, questions, official assets or PDF changes. [Preview/review](app-design/8f/review.md).


**14 October — 8F v1 approved:** User explicitly said “approved”. Recorded approval against the saved long-content/enlarged-text preview and exact bindings; 8F is complete. Documented font/viewport/scale deviations and actual reflow/full-content checks remain future implementation requirements. 8G is next only when separately requested; no implementation started. [Approval record](app-design/8f/review.md).


**14 October — 8G v1 generated:** Saved built-in imagegen wide/phone answered situation-001 review. Verified exact shuffled A-selected/B-correct identities and recorded main/per-option explanations, M03-L02 and scoped source binding. Saved prompt and review with both feedback modes and unfinished-test guard requirements; unbound generated phone menu documented. Awaiting explicit approval; 8H unstarted. No implementation, live question, official asset or PDF changes. [Preview/review](app-design/8g/review.md).


**14 October — 8G v1 approved:** User explicitly said “approved”. Recorded approval against the saved standard answer-review preview and exact bindings; 8G is complete. Documented quiz guard/runtime checks and unbound-menu limitation remain. 8H is next only when separately requested; no implementation started. [Approval record](app-design/8g/review.md).


**15 October — 8H v1 generated:** Saved built-in imagegen wide/phone calculation answer-review previews using the exact proposed fuel-saving-150-0.5 fixture. Decimal result 0.75 litres, shuffled A-selected/B-correct mapping and related-lesson source hash pass. Saved prompt, exact bindings, content-status limitation and conditional historical-score/version notice without adding history functionality. Awaiting explicit design approval; proposed item remains unapplied/unaccepted for scoring. 8I unstarted; no app, live question, official asset or PDF changes. [Preview/review](app-design/8h/review.md).


**15 October — 8H v1 approved:** User explicitly said “approved”. Recorded approval against the saved calculation answer-review preview and exact bindings; 8H is complete. The proposed fuel question remains unapplied and unaccepted for live scoring; historical compatibility and runtime checks remain required. 8I is next only when separately requested; no implementation started. [Approval record](app-design/8h/review.md).


**15 October — 8I v1 generated:** Saved built-in imagegen directory/detail source previews in wide/phone layouts. Retained actual legislation, Trafiko and Volvo attribution/dates/scopes, editorial-arithmetic distinctions and exact source URL bindings. Specified lesson entry, directory/detail navigation and return to validated reading position, without implying global examples all support the origin lesson. No fresh source-currency claim. Awaiting explicit approval; 8J unstarted. No implementation, live question, official asset or PDF changes. [Preview/review](app-design/8i/review.md).


**15 October — 8I v1 approved:** User explicitly said “approved”. Recorded approval for both source-directory/detail boards and exact bindings; 8I is complete. Retained source dates/scopes, reading-position return contracts and future runtime/currency verification remain documented. 8J is next only when separately requested; no implementation started. [Approval record](app-design/8i/review.md).


**15 October — 8J v1 generated:** Saved built-in imagegen wide/phone B1 study/reference and zoom layout with labelled placement placeholders; exact official asset inspected/hash-verified and bound separately with CAP-B1. Recorded source/credit actions, aspect-fit, proposed size and accessible zoom/return requirements. No sign artwork generated or modified; all 38 faint-outline delivery holds remain open for actual tests. Awaiting explicit approval; 8K unstarted. No implementation, live question, official asset or PDF changes. [Preview/review](app-design/8j/review.md).


**15 October — 8J v1 approved:** User explicitly said “approved”. Recorded approval against the B1 reference/zoom layout and exact asset bindings; 8J is complete. All 38 delivery holds and actual asset/size/accessibility checks remain open; no unbound-menu functionality inferred. 8K is next only when separately requested; no implementation started. [Approval record](app-design/8j/review.md).


**15 October — 8K previews generated:** Saved built-in imagegen chooser v2 and moved-passage v1 boards, each wide/phone. Verified exact page-46 canonical choice order, situation-017/M04-L03 versus situation-103/M04-L01 precedence and known-parent missing-block policy. Production M03-L04 source hash matches. Saved prompts, bindings and review; initial chooser header corrected internally. Awaiting explicit approval; 8L unstarted. No implementation, live questions, official assets or PDF changes. [Preview/review](app-design/8k/review.md).


**15 October — 8K approved:** User explicitly said “OK approved”. Recorded approval for chooser v2 and moved-passage v1 in review and exact bindings; 8K is complete. Routing/quiz-guard/runtime requirements remain documented. 8L is next only when separately requested; no implementation started. [Approval record](app-design/8k/review.md).


**15 October — 8L v1 generated:** Saved built-in imagegen signal/generic unavailable states, each wide/phone. Verified exact SIG16–18 messages, null internal entries, distinct recorded official URLs and optional M03-L02 relationship. Generic state offers library without guesses; no signal substitutions or new entries. Saved prompts, bindings and review including external failure/quiz-guard requirements. Awaiting explicit approval; 8M unstarted. No implementation, live questions, official assets or PDF changes. [Preview/review](app-design/8l/review.md).


**15 October — 8L v1 approved:** User explicitly said “approved”. Recorded approval for both unavailable-state boards and exact bindings; 8L is complete. Signal URL/no-substitution, quiz-guard and runtime requirements remain documented. 8M is next only when separately requested; no implementation started. [Approval record](app-design/8l/review.md).


**15 October — 8M v1 generated:** Saved built-in imagegen missing-results/setup recovery wide/phone preview with exact message and setup action. Saved prompt, input hashes and reviewed missing-session/setup preference/validation contracts. No invented results/history or auto-start. Awaiting explicit approval; 8N unstarted. No implementation, live question, official asset or PDF changes. [Preview/review](app-design/8m/review.md).


**15 October — 8M v1 approved:** User explicitly said “approved”. Recorded approval against the saved missing-results/setup-recovery preview and exact bindings; 8M is complete. State/validation/runtime requirements remain documented. 8N is next only when separately requested; no implementation started. [Approval record](app-design/8m/review.md).


**15 October — 8N completed:** Consolidated all twelve individually approved preview tasks/sixteen boards into the app design specification and hashed package index. Recorded typography/colour/spacing constraints, responsive/large-text intent, exact content/source/asset/route bindings, accessibility/session rules and step 9/T01–T10 acceptance ownership. All recorded preview and applicable input/source/asset identities and local links pass the bounded consolidation checks. Existing chip/icon variants, large-text limitations and 38 delivery holds remain explicit; no new common visual was silently chosen. No new image generation or app/question/asset/PDF change. 8O final review/approval remains separately requested; implementation has not started. [Specification](app-design-spec.md), [index/checks](app-design/8n/package-index.json).


**15 October — 8O verification performed:** Passed 681 stored identity/fixture/route/copy/link checks; twelve individual approval records and sixteen boards retained, all 466 saved 7G input-manifest files unchanged. Reinspected recorded visual variants and presented state-specific chip/icon retention, documented unbound-control omissions and typography/reflow/exact-artwork implementation requirements without a new design. Saved final report and reproducible checker. Awaiting explicit complete-package approval; 8O/step 8 not complete. All question acceptance/38 delivery/device/source-currency holds remain future work; no app/question/asset/PDF changes or implementation. [Final review](app-design-review.md), [results](app-design/8o/verification.json).


**15 October — 8O and step 8 approved:** User explicitly said “yes approved”, approving the complete specification/indexed preview package and final-review dispositions. Recorded final approval; 8O and step 8 complete. Existing content/scoring, source-currency, exact-artwork/38 delivery holds and device/runtime requirements remain unchanged. No implementation started; step 9 requires a separate request. [Final approval](app-design-review.md).


**15 October — 9A1 completed:** Compared 1,174 retained input bindings across the source/app baseline, bundled assets, migration package, design records and approved release copies; every identity matches. Saved 1,055 unique file identities and 21 passing readiness checks. Confirmed the final design approval and retained all question/delivery/source/device holds. Corrected stale tracker summaries for 7G (60/60) and app-design approval. No live app/question/asset/PDF or prior approval/audit edits. 9A2 remains separately requested. [Readiness](app-migration/implementation-evidence/9A1/readiness.md), [execution review](app-migration/implementation-evidence/9A1/review.md).


**15 October — 9A2 completed:** Added typed common Kotlin content, source/asset, manifest, assessment/eligibility and snapshot models; documented schema roots, field mappings and non-circular manifest hashing. Incoming 9A1 verification passed before edits; the existing Quiz.kt implementation prefix and all other protected app/content/source/asset/approval inputs remain unchanged. Final JDK 17 offline desktop build and all 11 tests pass (five contract tests plus six existing quiz tests). No runtime import, bank edit, design, new persistence or UI integration. 9A3 remains separately requested. [Schema](app-migration/implementation-evidence/9A2/content-contract.md), [review](app-migration/implementation-evidence/9A2/review.md).


**15 October — 9A3 completed:** Extended the content tool with an explicit schema-1 compile command, typed/cross-record and frozen-source validation, deterministic staged Kotlin parts and exact source/output trace. Preserved the historical generation body behind an explicit legacy command, with import/no-argument safety. The partial unscored M03/B1/question/source fixture passes 44 compiler tests and 12 configured Kotlin/desktop tests; repeated generation is byte-identical. Reviewed and preserved incoming Quiz.kt import/formatting changes; live bank, assets, PDF and prior approvals/audits remain unchanged. No full import or release/device acceptance claimed. 9B1 remains separately requested. [Usage/fixture](app-migration/implementation-evidence/9A3/README.md), [review](app-migration/implementation-evidence/9A3/review.md).


**15 October — 9B1 completed:** Imported all approved opening text, the exact disclaimer and the 60-node reading skeleton into content/curriculum.json, retaining 10 modules/40 lessons/10 reviews and all category tags. Four published front-matter IDs remain separate from module cards/reading order; all chapter bodies are explicitly pending in the build-time import ledger. All four opening pages match fresh approved-PDF extraction; source PDF unchanged and rendered pages inspected. All 86 checks and 14 configured Kotlin/desktop tests pass; repeated staged generation is byte-identical. Cover/reference delivery and complete module bodies remain assigned future work. No live bank/UI/asset or earlier approval/audit edits. 9B2 remains separately requested. [Review](app-migration/implementation-evidence/9B1/review.md), [checks](app-migration/implementation-evidence/9B1/verification.json).


**15 October — 9B2 completed:** Imported M01 introduction, four complete lessons and review with 41 exact production paragraphs, five hidden answers, four approved illustration windows and sixteen scoped sources. All 216 PDF/source parity checks, 59 Python regression tests and 14 configured Kotlin/desktop tests pass; generation is byte-identical. Preserved other 58 documents and prior evidence; 54 reading bodies remain pending. Added typed contextual crop regions and parliamentary-material classification, and validated four curriculum-only licensing URLs against frozen source scopes/evidence. No live bank, UI, learner state, artwork or PDF changes. Source-directory/resource delivery/runtime work remains later; 9B3 separately requested. [Review](app-migration/implementation-evidence/9B2/review.md), [parity](app-migration/implementation-evidence/9B2/module-parity.json).


**15 October — 9B3 completed:** Imported M02 introduction, four complete lessons and review: 46 source blocks including the full symptom/action table, five hidden answers, six approved illustrations with two typed polygon masks and nineteen source scopes. All 243 PDF/source parity checks, 74 Python regression tests and 15 configured Kotlin/desktop tests pass; generation is byte-identical. Preserved other 58 documents, all M01 assets/source evidence, prior audits and incoming JvmInline/BlockId formatting. Forty-eight reading bodies remain pending. No live bank/UI/learner-state/artwork/PDF changes; 9B4 separately requested. [Review](app-migration/implementation-evidence/9B3/review.md), [parity](app-migration/implementation-evidence/9B3/module-parity.json).


**15 October — all remaining 9B steps completed:** User authorized all 9B work. Imported M03–M10, appendices A–D, all 24 reference groups and all published supporting anchors. Completed 9C1–9C4 as explicit prerequisites of 9B17: exact source/caption bindings and artwork bundles. All 1,123 destinations resolve uniquely; the complete reading package retains 50 hidden answers, 400 signs, 116 source destinations, 516 URL records and 484 artwork bindings. All 2,538 parity/identity/generation checks, 83 Python tests and 15 configured Kotlin/desktop tests pass. Fresh approved-PDF extraction matches all 578 pages; every production character on pages 41–578 is accounted for once, including the page-193 wildlife correction and 729 shared sign examples. Preserved prior teaching/evidence, original PDF/artwork and the live question bank. No new design, learner state or question acceptance; runtime/device/source-currency and 38 delivery holds remain open. 9D1 is next. [Review](app-migration/implementation-evidence/9B17/review.md), [verification](app-migration/implementation-evidence/9B17/import-parity.json).


**16 October — all 9D steps completed:** User authorized 9D1–9D15. Implemented authored question/option identity through generated values, selection, shuffle, confirmation, semantic-revision snapshots and scoring. Added assessment presentation/components with neutral image semantics, answer-gated feedback and focus handoff. Reviewed 308 physical descriptions in all 616 exact proposed question contexts, covering 1,540 image occurrences across the 13 backlog batches. All 91 Python tests and 21 Kotlin/desktop tests pass, including all 24 permutations and actual merged semantics/Space/Tab/Enter checks in both feedback modes. Retained all 38 delivery-held question targets; no active-bank rewrite, curriculum/PDF change or device acceptance. 9E is next, separately requested. [Execution review](app-migration/implementation-evidence/9D1/review.md), [reproduction and evidence](app-migration/implementation-evidence/9D1/README.md).


**16 October — 9E1 completed:** Applied the exact 50 A1–A25 sign rewrites with authored identity, `rewrite-r2`, source/feedback metadata and 125 reviewed neutral-image bindings. Twelve question records include approved distractor changes; paired directions remain consistent. The other 950 question rows are unchanged. All 98 Python tests, 23 Kotlin/desktop tests and full typed package checks pass. All 50 rewritten questions remain held pending image-delivery/integration acceptance and are excluded from legacy/new scoring. Retained per-ID before/after diffs and original bank/JSON snapshots. No 9E2+ work or 9F hold release. [Review and reproduction](app-migration/implementation-evidence/9E1/README.md). Next: 9E2, separately requested.

**16 October — all 9E steps completed:** Completed 9E2–9E12 (528 additional rewrites), preserving 9E1. All 578 assigned rewrites now retain authored identity, `rewrite-r2`, exact 7D options/feedback/keys and 1,445 accepted neutral-image bindings; 422 other question records are unchanged. All 128 overlapping distractor-change records and 289 paired directions are checked. Generated metadata is split by batch after the combined Kotlin class hit the JVM size limit. All 113 Python and 23 Kotlin/desktop tests pass. All 578 rewritten questions remain delivery-held; no 9F replacement holds are released. Per-batch before/after evidence is retained, with full package and test reproduction in [9E evidence](app-migration/implementation-evidence/9E/README.md). Next group: 9F, separately requested and subject to its delivery prerequisites.


**16 October — 9F1–9F19 reviewed; acceptance open:** Implemented 9K1–9K4 canonical/legacy resolution and guarded returns, plus approved 9L9–9L10 reference/viewer components. Exact PDF vector decoding preserves source geometry; fixed zero-height artwork in scrolling assessment cards. All 119 Python and 39 desktop tests pass, along with Android/Wasm/iOS simulator builds. Retained 76 Android captures and all 19 simulator/Wasm renders. User chose simulator instead of physical iPhone. All 38 originals remain unchanged and are excluded from scoring; 12 previews remain faint and full reader/delivery acceptance remains open. No hold released, replacement applied or route activation claimed. [Detailed results and replay](app-migration/implementation-evidence/9F/README.md).


**17 October — 9L isolated views:** Implemented the approved 9L1–9L13 components and a verification-only learning route. Complete compiled teaching parity retains all document/answer/artwork metadata; canonical library search/filter and 60-node reading navigation, reveal semantics, shuffled standard/fuel reviews, source details/return, exact sign/viewer reuse and recovery states are covered by focused checks. 137 Python and 68 desktop tests pass; Android, iOS simulator and WebAssembly compilation pass. No new design, live-bank change, scoring acceptance or production activation. 9L14 remains blocked by 9J/9M prerequisites; mobile assistive and complete delivery acceptance remain open. [Evidence and reproduction](app-migration/implementation-evidence/9L/README.md).


**17 October — 9M1–9M3 execution:** Added a pure transient owner and session-keyed assessment wrapper, exact draft identity, pinned review/filter/expansion state, atomic guarded discard, missing-context recovery, default/reset and accepted-capacity checks. The production start rejects the held 9J candidate; fixture checks cover all lengths 1–70 without held questions. All 22 contracts have explicit results; final 9M3 acceptance remains blocked until 9J passes. 140 Python and 77 desktop tests pass; Android, iOS simulator and WebAssembly compilation pass. No app activation, durable state, content change or earlier receipt recertification. [Evidence and reproduction](app-migration/implementation-evidence/9M/README.md).


**17 October — joint 9J/9M delivery checkpoint:** Added a verification-only host for real held candidate records and an exhaustive desktop matrix: 616 revisions × four surface/text settings, with 6,160 exact-image zoom/returns, neutral pre-answer projection, authored selection preservation and trigger focus. Native simulator AX/modal/selection evidence covers two actual S5 contexts. A per-question report separates 24 questions using known faint assets from 592 without them. Candidate 9M3 checks proceed alongside delivery work; final release verification still awaits real acceptance. No artwork, question, eligibility or production route changed. [Readiness, limits and next executable checks](app-migration/implementation-evidence/9J-followup/README.md).


**17 October — native reader/route checkpoint:** Fixed retained library context and accessible search naming, sign-to-catalogue back navigation and touch-mode focus return. Five Android native and five iOS simulator UI checks pass; real Android TalkBack traversal is captured separately from instrumentation. Scoped iOS description/trait audits pass; no simulator VoiceOver listening claim. All 80 desktop and 144 Python checks, generator checks and target compilation pass. The twelve faint assets, final 9J acceptance/9M3 rerun and 9L14 remain the next ordered stages. [Evidence and reproduction](app-migration/implementation-evidence/native-reader-routes/README.md).


**17 October — requested 9J finalization / 9M3 rerun:** Reran deterministic assembly/readiness/sign checks, direct structural and release validation, 41 focused desktop tests and three report-generator tests. Structural/parity/state checks pass; release validation rejects the unchanged 384-accepted/616-held manifest. The fresh 22-contract 9M3 result is bound to that exact manifest (18 current passes, four future-store conditional cases). Accepted-release finalization remains blocked by unresolved per-ID delivery acceptance, including the twelve faint assets and unapplied replacements. [Fresh results and remaining prerequisites](app-migration/implementation-evidence/9J-finalization/README.md).


**17 October — faint-asset presentation preview:** Prepared an imagegen layout proposal with larger equally sized image-choice areas, unchanged white-backed official artwork in both themes and accessible viewer controls. Verified all twelve original/bundled asset identities and recorded the 24 affected question/slot bindings. **Awaiting explicit preview approval before implementation.** No artwork, question, eligibility or release decision changed; layout approval alone will not establish actual-size legibility. [Preview and review](app-design/faint-assets-v1/review.md).


**17 October — faint-asset layout approved:** User explicitly approved the saved larger-artwork preview. Implementation and exact-artwork delivery verification may proceed within that scope; no asset substitution, semantic revision, eligibility change or release approval follows from layout approval alone. [Approval record](app-design/faint-assets-v1/review.md).

**17 October — approved presentation implemented:** Added full-width 3:2 artwork frames with a 220 dp minimum and equal sizing for all assessment image options; retained official artwork bytes, neutral descriptions and existing zoom/return behavior. All 80 desktop and 144 Python tests pass. Six Android tests include 48 asset/theme/text contexts; the iOS 48-context artwork matrix and five repaired scrolling-harness route checks pass. Captured 48 browser contexts and matched four passing shared rows for each of the 24 affected questions. Original fine strokes remain thin; question-level native/legibility acceptance and all 616 scoring holds are retained. [Implementation, captures, test phases and limits](app-migration/implementation-evidence/faint-assets-approved/README.md).
