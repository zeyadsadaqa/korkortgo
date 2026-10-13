# Execution plan: 55 driving-situation coverage gaps

Prepared: 12 October 2026. Status: planning only; chapter execution has not started.

The user requested an execution plan that can be followed chapter by chapter. Creating this document does not execute the content, design, PDF or question-bank changes. Execute only the step subsequently requested by the user, report its result, and leave the next step ready to request.

## Scope and baseline

- Cover the 55 `situation-*` records classified `not_covered` in [the existing audit](question-coverage-gaps.json).
- Keep the 10 chapters and existing module/lesson identifiers. Seven topic packages discussed in chat become additions distributed across those chapters, not seven new chapters.
- Keep `content/questions.json` unchanged. If a keyed answer conflicts with verified evidence, report the discrepancy and propose a separate question correction; do not bend the teaching text to support it.
- Missing sign questions and the 20 braking exercises are separate work. Explaining the squared-speed relationship here may help later exercise coverage, but does not automatically resolve those exercises.
- Current review PDF: `docs/curriculum/pdf-production/korkortgo-curriculum-review.pdf`, 498 pages; SHA-256 `2490db58238ec9765208e8feff5c85d39da028f20cfac61e68ff2e5fdf285393`.
- Current question bank SHA-256: `303519698e564c9fb9aa835a29acd743d2038bca54be87cc71efd11951c4a3bb`. Recheck both hashes before execution; if inputs changed, reconcile the baseline before proceeding.
- Budget: approximately 18–24 additional pages, resulting in about 516–522 pages. This is a planning estimate, including an allowance for teaching examples and references, not a promise about final pagination. Assessment separation and reference overflow can affect the total.

## Execution order and page allocation

G0 establishes the evidence/coverage tracker. G1–G10 can then be requested independently; chapter number order is the default. G11 requires all chapter work. G12 requires G11.

| Step | Chapter | Primary questions | Estimated added pages |
|---|---|---:|---:|
| G0 | Preparation and evidence tracker | 55 | No book changes |
| G1 | M01 · Choose to drive responsibly | 4 | 1–2 |
| G2 | M02 · Prepare a car that is ready | 10 | 3–4 |
| G3 | M03 · Read the road before acting | 3 | 2 |
| G4 | M04 · Negotiate shared space | 1 | 1 |
| G5 | M05 · Make room in busy streets | 3 | 1 |
| G6 | M06 · Travel beyond the town | 3 | 1–2 |
| G7 | M07 · Adapt when conditions change | 12 | 3–4 |
| G8 | M08 · Take responsibility for the vehicle and load | 3 | 1–2 |
| G9 | M09 · Reduce the impact of each journey | 15 | 4–5 |
| G10 | M10 · Respond, reflect and keep learning | 1 | 1 |
| G11 | References, assembly and navigation | — | Included in estimate; report overflow |
| G12 | Final evidence-based coverage audit | All 1,000 | No additional teaching pages |
| Total | 10 existing chapters | 55 unique target questions | 18–24 |

Each question has one primary teaching owner below. Cross-links and reminders in other chapters do not count as duplicate primary assignments or independent gap resolutions.

## Source-selection rule

1. Search Transportstyrelsen and Trafikverket for the exact teaching claim, including relevant reports and current regulations, not just general topic pages.
2. If either provides sufficient support, cite that source alone; do not add another organisation for the same claim.
3. If the exact claim remains unsupported, record the agency searches and use another suitable official source: legislation published by Riksdagen, VTI, SMHI, Naturvårdsverket, Energimyndigheten, Läkemedelsverket, MFD, Elsäkerhetsverket, regional healthcare guidance or a municipality, as appropriate.
4. A manufacturer manual is a primary technical source, but not a government authority. Use it only as a documented fallback for vehicle-specific instructions or technical facts when suitable official evidence is unavailable. Record model/year and avoid universalising that vehicle's limits. The user's permission to mention other sources allows a fallback to be proposed; its suitability still needs verification.
5. A report hosted or funded by Trafikverket is not automatically authored or endorsed by Trafikverket. Record the actual publisher/author.
6. Foreign government guidance may support a physical phenomenon or general technique only after checking applicability. Do not import foreign legal rules or different following-distance recommendations into Swedish instruction.
7. Mark an unresolved claim `pending` or `blocked`; do not label its question covered. A general link or bibliography entry is not teaching coverage.

The source register at the end records research starting points from the preceding discussion. It is not a completed evidence ledger. Reopen sources, verify the exact passage and current applicability during execution.

## Shared chapter workflow

Each G1–G10 step uses the following substeps, which can also be requested individually, for example “Execute G7-A”.

### A — Verify evidence and settle wording

- Read the exact question, keyed answer and distractor explanations from the audit/bank.
- Locate evidence for every essential part of the answer; record URL, actual publisher, document version/date, retrieval date and section/PDF page. Retain a short supporting excerpt or source snapshot internally.
- Classify each claim as legal requirement, official recommendation, technical fact, medical explanation or editorial example.
- Resolve ambiguities, model-specific limits and assumptions before drafting. Report answer/source conflicts separately.
- Output: `execution/Gxx/evidence.json` and `evidence.md` under this review directory. Include an entry for every assigned question, even unresolved ones.
- Complete when every claim needed for the chapter addition is supported, or the unresolved items are explicitly identified. Partial research may be saved; unresolved items cannot pass into verified teaching content.

### B — Draft the teaching additions

- Write original explanations in the book's existing English style, with useful Swedish terms where appropriate.
- Give each concept an explanation, a practical example and a comprehension check with reasoning; combine related concepts rather than copying all practice questions into the book.
- Keep exact question IDs in the internal evidence/coverage tracker. Learner-facing text teaches the principle and does not expose implementation records.
- Produce `execution/Gxx/proposed-additions.md`, with exact insertion anchors, source aliases and question mappings. Update the authoritative manuscript and evidence records only within the requested execution scope.
- Preserve existing lesson objectives and assessment conventions. Update `manuscript-sources.json`, `manuscript-claims.json`, `manuscript-evidence.md`, `manuscript-verification.md`, `manuscript-checks.json` and curriculum source maps where the addition changes their claims/status. Do not retain stale verification dates or an obsolete source-scope statement.
- Complete when the proposed teaching text itself supplies the knowledge required by every resolved question, with a clear distinction between laws and advice.

### C — Handle visuals and produce the chapter

- Reuse the approved page styles and suitable existing artwork where possible.
- If a new diagram, illustration, page layout or other design is needed, follow the user's design workflow: read/use the imagegen skill, generate a visual preview, and wait for explicit feedback/approval before implementing that design. Revisions need renewed approval. Continue independent evidence/text work while a design decision is pending.
- Do not produce new design previews during this planning request. Do not use generated substitutes for official road signs.
- Update `pdf-production/chapters/Mxx/build_chapter.py` as needed. These builders parse manuscript blocks and also control explicit page breaks; manuscript edits alone may not fit existing pages.
- Preserve the builder's expected `Worked decision`, `Knowledge check`, `Answer` and `Remember` structures, or update parser and checks together if additional examples require an extension.
- Rebuild the chapter and its source snapshot, source checks, navigation, illustrations metadata and delivery copy through the existing pipeline. `chapter-source.md` is generated, not the authoritative editing target.

### D — Verify and report the chapter

- Update the adjacent `verify_chapter.py` only for legitimate changes to page counts, destinations and content structure. Preserve checks for complete manuscript text, sources, fonts, bounds, artwork approval and separated answers.
- Run the chapter verifier. Render and visually inspect every changed page and any newly shifted assessment/answer pages; check all links and new references.
- Assess each target question using the chapter's actual teaching text, not the mere presence of keywords or a linked source. Record supporting excerpts and local chapter pages in `execution/Gxx/coverage.json`.
- Write `execution/Gxx/completion.md`, update the chapter review and relevant progress records, and report questions resolved, any blockers, actual page increase and remaining work.
- A chapter is complete only when its assigned questions have adequate evidence, teaching support and verified rendered output. Final book pages are assigned after G11.

## G0 — Prepare the execution tracker

1. Recheck baseline hashes and preserve the original audit/PDF evidence in a separate execution-baseline directory. Do not overwrite the baseline with a revised-book audit.
2. Create `execution/tracker.json` with all 55 exact IDs, primary chapter/lesson, required teaching claim, source status, design status, text status, chapter status and final coverage status.
3. Create `execution/source-evidence.json` for claim-level evidence. Start each source with its actual verification status; carry discussion findings as leads, not fresh verification.
4. Inspect manuscript and chapter builders for insertion capacity, assessment parity, reference overflow and fixed-count assertions. Record the provisional allocation above.
5. Add execution-scoped progress records. Earlier approved/completed work remains historical; distinguish new gap-resolution status from the original PDF production status.

**Done when:** the tracker contains exactly the 55 target IDs, each assigned once, and all pending evidence/design items are visible. No teaching, question or PDF changes in G0.

## G1 — Chapter 1: Choose to drive responsibly

**Insertion anchors:** M01-L02 “Am I ready today?”, M01-L03 “Pressure is a driving risk”; brief Vision Zero introduction in the chapter opening. Budget: 1–2 pages.

| Question ID | Required addition | Evidence route |
|---|---|---|
| situation-062 | Explain masked fatigue and overconfidence from stimulant drugs; distinguish feeling alert from safe judgement. | R-DRUGS provides background; exact combined claim pending, then Läkemedelsverket if needed. |
| situation-068 | Define brief unintended sleep and show distance travelled during a short lapse. | Agency search first; R-FATIGUE/VTI report as proposed official fallback. Exact definition pending. |
| situation-069 | Explain that adequate sleep addresses sleep deprivation; transient alertness does not replace sleep. | Agency search first; R-SLEEP fallback. |
| situation-129 | Define Vision Zero's no-death/no-serious-injury aim and connect it to driver choices. | R-ZERO. |

**Work:** A: verify physiological and safety claims separately. B: add a fatigue decision example, an explicitly hypothetical time × speed calculation and a short Vision Zero explanation; retain cross-links to M07-L03 without repeating the whole lesson. C/D: build and check that the new concept text fits before the existing scenario/assessment material.

**Acceptance:** 062 is not justified by a generic “drugs impair driving” statement alone; 068 is explicitly defined; 069 distinguishes adequate sleep from music/windows/willpower; 129 states the exact aim.

## G2 — Chapter 2: Prepare a car that is ready

**Insertion anchors:** M02-L01 controls/brakes/fuses, M02-L02 vehicle checks/tyres, M02-L03 occupant protection. Budget: 3–4 pages.

| Question ID | Required addition | Evidence route |
|---|---|---|
| situation-131 | Explain head-restraint purpose and head/neck movement in a collision. | R-HEADREST. |
| situation-132 | Explain rear-facing child-seat support and distribution of collision forces. | R-CHILD. |
| situation-145 | Explain wheel imbalance as a possible cause of speed-dependent steering vibration. | Direct agency technical evidence pending; manufacturer technical fallback if necessary. |
| situation-146 | Explain temporary spare use and checking vehicle-specific speed, distance/use and pressure limits. | Agency evidence first; R-SPARE is a manufacturer fallback example. |
| situation-154 | Explain independent brake circuits and reduced remaining braking after one fails. | Current TS technical requirements pending; an inspection defect table alone does not establish the design purpose. |
| situation-156 | Explain normal ABS pulsation during emergency braking and maintaining firm steady pressure. | Direct agency instruction pending; R-ABS is a manufacturer fallback. |
| situation-157 | Explain a sinking pedal as a serious possible hydraulic leak/fault. | Verify current TS inspection rules; R-BRAKE-LEAD is an older research lead. |
| situation-158 | Explain air in hydraulic brakes as a possible cause of a springy/spongy pedal. | Direct technical evidence pending. |
| situation-159 | Explain controlled deformation absorbing crash energy and reducing occupant forces. | Exact agency explanation pending; manufacturer engineering fallback if necessary. |
| situation-173 | Explain a fuse protecting a circuit from excessive current. | Agency search first; R-FUSE official fallback for the electrical principle. |

**Work:** group additions into protection, tyre checks, and brake/electrical systems. Use a symptom/possible cause/action table without presenting symptoms as a definitive diagnosis. Distinguish normal ABS feedback from abnormal pedal behaviour. Proposed protection/brake diagrams go through design preview approval before implementation. Cross-link handling details to M07-L02 and hot-coolant precautions to M10-L01.

**Acceptance:** no universal spare-wheel speed/distance is invented; no promise of unchanged braking after circuit failure; no repair procedure is introduced; every symptom claim has specific evidence.

## G3 — Chapter 3: Read the road before acting

**Insertion anchor:** M03-L04 “Leave room to respond”. Budget: 2 pages.

| Question ID | Required addition | Evidence route |
|---|---|---|
| situation-106 | Teach selecting a fixed point and counting the time between both vehicles passing it. | Exact TS/TRV three-second method pending; suitable Swedish official fallback to locate. |
| situation-107 | Explain increasing the forward gap when followed too closely, allowing smoother braking. | Exact official behavioural instruction pending. |
| situation-138 | Explain approximately fourfold braking distance at doubled speed under identical grip/braking assumptions. | R-STOP background; exact relation or an authoritative physical derivation pending. |

**Work:** add a fixed-point worked example, a tailgater decision example and the squared-speed relationship. Show 2× speed → 4× braking distance separately from reaction distance and total stopping distance. Use hypothetical arithmetic with explicit assumptions. Preserve existing unit-conversion material.

**Acceptance:** three seconds is a guideline, not a statutory fixed interval or guarantee for every condition; the tailgater response is explained; doubling speed is not claimed to quadruple total stopping distance.

## G4 — Chapter 4: Negotiate shared space

**Insertion anchor:** M04-L02 “Turn with a complete picture”. Budget: 1 page.

| Question ID | Required addition | Evidence route |
|---|---|---|
| situation-104 | Keep front wheels straight while waiting to turn left across oncoming traffic; explain the rear-impact risk. | Exact official technique evidence pending. |

**Work:** add a waiting-to-turn example and explain wheel direction versus intended turn direction. Link the rural alternative to M06-L01, whose primary owner is G6. If a diagram is necessary, preview and approve it before implementation.

**Acceptance:** the waiting position and start of the turn are distinguished; the technique is classified correctly as advice unless a specific legal duty is established.

## G5 — Chapter 5: Make room in busy streets

**Insertion anchor:** M05-L01 “See the person behind the movement”, including the existing bus passage. Budget: 1 page.

| Question ID | Required addition | Evidence route |
|---|---|---|
| situation-013 | Compare the special bus rule at ≤50 km/h with a bus leaving a stop on a 70 km/h road; explain safe entry and cooperation. | Exact agency support pending; R-LAW chapter 3 §§43–45 fallback. |
| situation-119 | Avoid distracting a working guide dog, including attention directed at the dog. | Agency search first; R-GUIDE official fallback. |
| situation-135 | Explicitly identify a bicycle as a vehicle under traffic terminology. | R-LIGHTS identifies bicycles as vehicles; verify the exact definition needed. |

**Work:** extend the existing bus example rather than duplicate it. Add a compact threshold comparison, a guide-dog interaction example and a bicycle terminology sentence beside cyclist duties.

**Acceptance:** no unconditional bus priority is taught; no implication that higher-limit roads excuse obstructive behaviour; the guide-dog and bicycle concepts appear in the teaching body.

## G6 — Chapter 6: Travel beyond the town

**Insertion anchors:** M06-L01 rural roads/turn planning/wildlife, M06-L03 motorway exits. Budget: 1–2 pages.

| Question ID | Required addition | Evidence route |
|---|---|---|
| situation-075 | Explain speed-perception adaptation after prolonged motorway driving and checking the speedometer on a slower road. | Exact agency/VTI evidence pending. |
| situation-105 | Explain continuing to a suitable safe turning place and returning for a right turn when a rural left turn is unsafe. | Direct official support pending; verify route/turn legality and safety conditions. |
| situation-126 | Explain increased wildlife attention around dusk/dawn, habitats and fence openings. | R-WILDLIFE; verify each detail, including fence openings. |

**Work:** add a motorway-to-local-road example, a rural turn decision and wildlife observation cues. Cross-link G4's wheel-position advice and M10's existing post-collision instructions without reproducing them. A route sketch, if needed, requires design approval.

**Acceptance:** feeling slow is not evidence of a faulty speedometer; no turning manoeuvre is suggested at an unsuitable place; wildlife prevention is distinguished from post-collision duties.

## G7 — Chapter 7: Adapt when conditions change

**Insertion anchors:** M07-L01 vision/lighting, M07-L02 grip/weather/handling; short attention cross-link in M07-L03. Budget: 3–4 pages.

| Question ID | Required addition | Evidence route |
|---|---|---|
| situation-045 | Explicitly prohibit dipped headlights plus front fog lights together. | R-LIGHTS. |
| situation-070 | Explain central vision and reading precise sign wording. | Exact agency evidence pending; VTI vision research fallback. |
| situation-071 | Explain peripheral movement/hazard detection and looking directly to inspect it. | Exact agency evidence pending; VTI vision research fallback. |
| situation-073 | Explain that one approaching light may be a wider vehicle with a failed lamp. | R-LIGHTS background; exact hazard explanation pending. |
| situation-114 | Explain bridge cooling from above and below and earlier freezing. | R-BRIDGE background; exact mechanism pending, then SMHI. |
| situation-116 | Explain nearly invisible ice from rain falling onto a sufficiently cold road. | Agency search first; R-WEATHER fallback. |
| situation-117 | Explain first rain mixing with accumulated road residues after dry weather. | Exact Swedish official mechanism pending; R-UK-WEATHER provides partial hazard background only. |
| situation-148 | Explain best-grip tyres on the rear and reducing rear-end grip loss. | R-TYRES. |
| situation-149 | Define oversteer: rear grip loss, turning more than intended. | Exact agency/VTI technical evidence pending. |
| situation-150 | Define understeer: front grip loss, turning less than intended. | Exact agency/VTI technical evidence pending. |
| situation-152 | Define aquaplaning as water disrupting tyre-road contact. | Agency search first; R-UK-WEATHER proposed government fallback. |
| situation-153 | Explain easing off and avoiding abrupt steering/braking during aquaplaning. | Exact full response pending; R-UK-WEATHER supports gradual easing/slowing only. |

**Work:** create compact lighting, visual perception and grip explanations. Pair understeer/oversteer definitions; explain their mechanism without introducing unsupported universal skid-recovery manoeuvres. Distinguish aquaplaning advice from G2's ABS emergency-stop instruction. Proposed bridge, contact-patch and handling diagrams need preview approval.

**Acceptance:** every essential mechanism is taught explicitly; generic “smooth inputs” or “poor visibility” wording alone cannot close these gaps; no foreign lighting law is imported.

## G8 — Chapter 8: Take responsibility for the vehicle and load

**Insertion anchors:** M08-L01 vehicle categories, M08-L02 towball loading, M08-L03 inspection. Budget: 1–2 pages.

| Question ID | Required addition | Evidence route |
|---|---|---|
| situation-136 | Explain the road-limit treatment of a light lorry without a trailer and safe speed adaptation. | R-LORRY. |
| situation-165 | Explain excessive downward towball loading unloading the front axle and impairing steering grip. | Exact agency technical mechanism pending; manufacturer towing evidence if needed. |
| situation-172 | Explain automatic driving prohibition following a missed inspection deadline and applicable conditions for addressing it. | R-INSPECTION. |

**Work:** add a light/heavy lorry comparison with clearly stated conditions, a load-transfer explanation and an inspection-timeline example. Keep numeric limits vehicle-specific and dated. Proposed load-transfer diagram needs approval before implementation.

**Acceptance:** no trailer exception is hidden; towball load is distinguished from total trailer weight; driving-ban exceptions and wording match current official guidance.

## G9 — Chapter 9: Reduce the impact of each journey

**Insertion anchors:** M09-L01 emissions/powertrains/wastewater, M09-L02 economical driving, M09-L04 studded-tyre restrictions. Budget: 4–5 pages.

| Question ID | Required addition | Evidence route |
|---|---|---|
| situation-076 | Explain stored fossil carbon → CO₂ → enhanced greenhouse effect. | R-CLIMATE background; R-CARBON fallback for the exact mechanism if absent in TS/TRV. |
| situation-077 | Explain catalyst temperature and low cold-start effectiveness. | R-CATALYST. |
| situation-078 | Explain pollutant conversion versus remaining fossil CO₂/climate impact. | R-CATALYST plus R-CLIMATE for distinct claims; no redundant other publisher needed if sufficient. |
| situation-079 | Explain an engine-heater timer reducing unnecessary electricity use. | Exact agency evidence pending; R-ENERGY and current municipal guidance as fallback leads. |
| situation-082 | Explain avoiding unnecessary cooling while preserving comfort, alertness and clear windows. | Exact evidence for both energy and safety elements pending. |
| situation-083 | Explain purpose-built washing with collected/treated wastewater. | Agency search first; R-WASH municipal fallback. |
| situation-084 | Explain carbon monoxide interfering with blood oxygen transport. | R-AIR. |
| situation-085 | Explain NOx respiratory effects, acidification and ground-level ozone. | R-AIR first; R-NOX only for effects not supported there. |
| situation-086 | Explain traffic particles and respiratory harm. | R-AIR. |
| situation-088 | Explain a suitably high gear without labouring the engine in a conventional manual car. | Exact agency evidence pending; R-ENERGY fallback, with engine-operation limits verified. |
| situation-090 | Define engine braking with accelerator released and a suitable gear engaged. | Exact agency definition pending; R-ENERGY is a lead, not complete evidence. |
| situation-092 | Distinguish no tailpipe exhaust from production and electricity-supply impacts. | R-EV. |
| situation-094 | Compare externally rechargeable plug-in hybrids with non-plug-in hybrids. | R-EV. |
| situation-098 | Connect studs → road wear → airborne particles → possible local restrictions. | R-AIR plus current TS/local traffic-regulation evidence for the restriction claim. |
| situation-099 | Explain unnecessary carried mass and removing unneeded heavy equipment. | R-ECO covers roof equipment; exact carried-mass evidence pending. |

**Work:** use one compact pollutant table, catalyst warm-up explanation, powertrain comparison and economical-driving examples. Each grouped example may support several questions, but the evidence tracker must map every required concept individually. Preserve the distinction between CO and CO₂. Avoid reusing dated percentage-savings claims. Cross-link AC/clear-window safety to M07-L01 and avoid teaching energy savings that undermine visibility/control.

**Acceptance:** all three NOx effects are supported; no claim of zero lifecycle impact for EVs; no catalyst-as-carbon-capture claim; no universal RPM/heater-time/fuel-cutoff promise; local restrictions are checked rather than implied to apply everywhere.

## G10 — Chapter 10: Respond, reflect and keep learning

**Insertion anchor:** M10-L01 “When the car cannot continue”. Budget: 1 page.

| Question ID | Required addition | Evidence route |
|---|---|---|
| situation-174 | Explain why opening a hot coolant cap can release pressurised hot fluid/steam and cause burns. | Direct agency technical instruction pending; R-COOLANT manufacturer fallback. |

**Work:** add an overheating decision example integrated with location/scene safety. Explain the hazard and following the vehicle handbook, without a generic roadside repair procedure. Cross-link M02-L01's warning indicators and fault recognition.

**Acceptance:** the burn/pressure mechanism appears in the lesson; no unsupported fixed waiting time or advice to open a still-hot cap is introduced.

## G11 — Update references and assemble the revised book

**Prerequisites:** G1–G10 completion records, or an explicit request to assemble a clearly labelled partial review copy with unresolved items listed.

1. Update the source section and relevant glossary entries/cross-links from the verified chapter evidence. Preserve existing cited material; do not remove other sources needed by unrelated lessons. If manufacturer sources are used, distinguish them from official agency/legal references in headings and provenance.
2. Build/verify `pdf-production/reference/build_reference.py` and its adjacent verifier. Adjust source-domain assertions and counts only where the accepted evidence policy requires it; do not disable verification broadly.
3. Rebuild any opening/navigation material whose metadata or links changed. Update manifests and input hashes for the revised component PDFs.
4. Run `pdf-production/assembly/build_book.py` and `assembly/verify_book.py`. Refresh navigation geometry where inputs change.
5. Verify every affected bookmark, contents folio, lesson/source cross-link and assessment/answer separation after assembly. A chapter page increase shifts later chapters even when their body text is unchanged.
6. Render/inspect inserted pages, affected boundary/assessment pages, contents and reference additions. Use the assembly comparison to check unchanged component body content and account for the full assembled output.
7. Record actual final page count, per-chapter page increases and any variance from 18–24 pages. Keep screen-review/print/accessibility limitations honest.

**Outputs:** revised review PDFs in the established source/delivery locations, updated assembly reviews/verification records, and `execution/assembly-completion.md`. Publication/app migration remains separate.

## G12 — Re-audit question coverage and generate final page mapping

**Prerequisite:** G11 assembled revised PDF.

1. Extract the revised PDF text and final navigation. Re-assess all 55 target questions against specific teaching passages and illustrations.
2. Remap every previously covered question against the revised book, because page offsets change. Recheck all 1,000 records for coverage regressions and possible newly covered exercise principles; do not assume a fixed final total.
3. The existing `tools/review_question_book_coverage.py` has hard-coded editorial decisions (`COVERED`, `GAPS`) and page numbers. Running it unchanged cannot discover the new coverage. Update/review those decisions from fresh evidence or introduce an equivalent evidence-driven mapping, then regenerate the audit. Do not simply flip all target statuses to covered.
4. Preserve original audit files in the G0 baseline before regenerating current `question-page-map.json`, `question-coverage-gaps.json`, `all-question-coverage.json` and `review.md`.
5. For every covered target, record question ID, primary lesson, actual one-based PDF page(s), primary page, supporting excerpt/illustration and source-claim linkage. Record the final PDF/bank hashes and numbering convention. The old bank's `page` is not a page number in this book.
6. Confirm all 1,000 IDs appear exactly once across covered/gap outputs; all 55 target IDs are represented; every claimed support page exists and contains sufficient teaching evidence. Save unresolved targets with their precise reason.
7. Verify `content/questions.json` stayed byte-identical unless a later user request separately authorised question changes. Summarise before/after totals and remaining scope.

**Outputs:** final question-page JSONs, `execution/final-coverage-review.md`, updated progress and a self-contained completion report. Target completion is 55/55 verified and taught; if some lack suitable evidence, report the actual achieved count and leave them unresolved.

## Research starting-point register

These links were discussed as evidence leads. “Direct lead” means the preceding research found relevant content; execution still must verify the exact passage and current applicability. “Background/pending” does not establish the full question answer.

| Key | Publisher and starting source | Planning status |
|---|---|---|
| R-DRUGS | [Trafikverket: alcohol/drugs and driving](https://www.trafikverket.se/resa-och-trafik/trafiksakerhet/sakerhet-pa-vag/alkohol-och-narkotika-i-vagtrafiken/alkohol---sa-paverkar-den/) | Background; stimulant-specific combined claim pending |
| R-FATIGUE | [VTI: driver fatigue](https://www.vti.se/forskning/forskningsomraden/transportslag/vagtrafik/trotthet-hos-forare) | Official fallback lead; exact report/passages pending |
| R-SLEEP | [1177: sleep and health](https://www.1177.se/liv--halsa/stresshantering-och-somn/somnen-ar-viktig-for-din-halsa/) | Proposed healthcare fallback |
| R-ZERO | [Trafikverket: Vision Zero](https://www.trafikverket.se/om-oss/vi-gor-sverige-narmare/nollvisionen-ar-var-ledstjarna/) | Direct lead |
| R-HEADREST | [Trafikverket: seats/head restraints](https://www.trafikverket.se/resa-och-trafik/trafiksakerhet/sakerhet-pa-vag/sakerhet-i-bil/saten-och-huvudstod/?accessibilityarea=easyread) | Direct lead |
| R-CHILD | [Trafikverket: children in cars](https://www.trafikverket.se/resa-och-trafik/trafiksakerhet/sakerhet-pa-vag/sakerhet-i-bil/barn-i-bil/) | Direct lead |
| R-SPARE | [Volvo: temporary spare](https://www.volvocars.com/se/support/car/v60/18w17/article/73e14f8cc7f8d151c0a81f6f7932e5d8/45dffbb5c7f91239c0a81f6f36dce48d/c73c954b9380b97ac0a801512086b8d5/) | Manufacturer fallback; model-specific limits |
| R-ABS | [Honda HR-V manual](https://www.honda.se/cars/owners/instruktionsboecker/_jcr_content/par1/textcolumnwithimagem_2138865762/textColumn/richtextdownload_1338937485/file.res/20%20HR-V%20JSS%20%28KE%20KG%29-3ST7A631_SV_web_compressed.pdf) | Manufacturer fallback; locate ABS passage |
| R-BRAKE-LEAD | [Transportstyrelsen TSFS 2010:84 compilation](https://www.transportstyrelsen.se/TSFS/TSFS%202010_84k.pdf) | Older research lead only; check current applicable regulations |
| R-FUSE | [Elsäkerhetsverket: purpose of fuses](https://www.elsakerhetsverket.se/fragor-och-svar/arkiv-fragor/varfor-har-man-sakringar/) | Official fallback for electrical principle |
| R-STOP | [Trafikverket: stopping distance](https://www.trafikverket.se/resa-och-trafik/trafiksakerhet/sakerhet-pa-vag/hastighetsgranser-pa-vag/stoppstracka/) | Background; exact squared relation pending |
| R-LAW | [Riksdagen: Trafikförordningen](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/trafikforordning-19981276_sfs-1998-1276/) | Primary legislation fallback |
| R-LIGHTS | [Transportstyrelsen: vehicle lighting](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/trafikregler/generella-trafikregler/fordonsbelysning/) | Direct lighting lead; single-lamp hazard pending |
| R-GUIDE | [MFD: guide dogs](https://www.mfd.se/nyhetsarkiv/ledarhundens-dag/) | Official fallback |
| R-WILDLIFE | [Trafikverket: wildlife](https://www.trafikverket.se/resa-och-trafik/trafiksakerhet/sakerhet-pa-vag/se-upp-for-vilt-pa-vagarna) | Direct lead; verify all risk-location details |
| R-BRIDGE | [Trafikverket: winter slipperiness work](https://www.trafikverket.se/om-oss/nyheter/lansnyheter/stockholm/2025/2025-11/pa-glid-nej-sa-jobbar-vi-mot-halka-i-stockholmstrakten/) | Background; above/below mechanism pending |
| R-WEATHER | [SMHI: traffic weather](https://www.smhi.se/kunskapsbanken/meteorologi/vaderprognoser/trafikvader) | Proposed official weather fallback |
| R-UK-WEATHER | [UK Department for Transport: adverse-weather driving](https://www.gov.uk/guidance/the-highway-code/driving-in-adverse-weather-conditions-226-to-237) | Government fallback for physical/general advice only; full mechanisms/recovery wording pending |
| R-TYRES | [Transportstyrelsen: tyres](https://www.transportstyrelsen.se/sv/vagtrafik/Fordon/Fordonsregler/Dack/) | Direct best-grip/rear lead |
| R-LORRY | [Transportstyrelsen: lorries](https://www.transportstyrelsen.se/sv/vagtrafik/fordon/fordonsregler/regler-for-olika-fordonsslag/personbil-lastbil-och-buss/lastbil/) | Direct light-lorry speed lead |
| R-INSPECTION | [Transportstyrelsen: vehicle inspection](https://www.transportstyrelsen.se/fordonsbesiktning) | Direct lead; dated conditions require recheck |
| R-CLIMATE | [Transportstyrelsen: climate/energy](https://www.transportstyrelsen.se/sv/vagtrafik/miljo/klimat-och-energi/) | Background/direct climate context |
| R-CARBON | [Naturvårdsverket: carbon cycle](https://www.naturvardsverket.se/amnesomraden/klimatforandringar/darfor-blir-det-varmare/kolets-kretslopp-rubbas/) | Official fallback for fossil-carbon mechanism |
| R-CATALYST | [Transportstyrelsen: vehicle-equipment report](https://www.transportstyrelsen.se/globalassets/global/publikationer-och-rapporter/rapporter/vagtrafik/atgarder-mot-manipulering-av-viss-fordonsutrustning.pdf) | Direct lead; catalyst explanation on PDF page 24 |
| R-AIR | [Trafikverket: road-traffic air pollution](https://bransch.trafikverket.se/for-dig-i-branschen/miljo---for-dig-i-branschen/luftkvalitet/vagtrafikens-luftfororeningar/) | Direct CO/particle lead; verify each NOx effect |
| R-NOX | [Naturvårdsverket: nitrogen oxides](https://www.naturvardsverket.se/amnesomraden/luft/luftfororeningar-och-dess-effekter/fakta-om-kvaveoxider-i-luft/) | Fallback only for missing NOx claims |
| R-ENERGY | [Energimyndigheten: economical-driving guide](https://www.energimyndigheten.se/contentassets/26a7d229ad044a93b9a6c9ebe5bbce0e/kom-langre-som-medveten-bilist.pdf) | Older official lead; exact definitions/timer details and current applicability pending |
| R-ECO | [Transportstyrelsen: economical driving](https://www.transportstyrelsen.se/sv/vagtrafik/miljo/klimat-och-energi/sparsam-korning/) | Direct roof-equipment lead; carried mass pending |
| R-EV | [Trafikverket: electric vehicles explained](https://www.trafikverket.se/om-oss/skydda-klimat-miljo-och-halsa-i-vart-arbete/elfordon--sa-funkar-det/) | Direct EV/hybrid lead |
| R-WASH | [Göteborg municipality: car washing](https://goteborg.se/wps/wcm/connect/03793c30-5618-4c8f-9fcc-e3a533089b48/Tv%C3%A4tta%2Binte%2Bbilen%2Bp%C3%A5%2Bgatan.pdf?MOD=AJPERES) | Municipal official fallback |
| R-COOLANT | [Kia: coolant precautions](https://ownersmanual.kia.com/full_webhelp/MQ4/2022/sv_SE/topics/chapter7_8_1.html) | Manufacturer fallback; pressure/burn warning |

## How to request execution

- “Execute G0” — create the evidence and progress tracker, without book edits.
- “Execute G1” — research, draft, produce and verify Chapter 1 within this scope; pause only for required new design approval or an unresolved dependency.
- “Execute G9-A” — verify Chapter 9 sources only.
- “Execute G9-B” — draft Chapter 9 additions after its evidence is ready.
- “Execute G11” — assemble after chapter completion.
- “Execute G12” — produce the final whole-bank coverage and revised page mapping.

Do not interpret requesting one step as permission to execute every later step. Save concrete reviewable work for the requested step and clearly report the next available action.
