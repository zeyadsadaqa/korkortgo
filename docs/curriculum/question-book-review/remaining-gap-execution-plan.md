# Remaining 228-question teaching-gap execution plan

Status: H0–H4 approved and completed on 13 October 2026; H5–H7 not started. Prepared 13 October 2026. This remains the execution/progress document. H0 added a canonical source register, compressed source snapshots, verification artwork and a reproducible verifier; it did not change teaching, question content, production assets or PDFs.

## Scope and completion criterion

Current book: 540 pages. Current coverage: 772/1,000. Remaining: 158 sign questions (79 exact codes, two questions each), 30 stopping-model questions, and 40 fuel arithmetic questions (20 consumption, 20 savings).

Target: 1,000/1,000 covered under the existing criterion: the printed book provides the illustration, principle or calculation method required to choose the keyed answer. This is not a claim that every distractor explanation is taught, or that these 1,000 questions exhaust the Swedish driving curriculum. External links alone do not count as teaching.

No additional chapters are needed. Expand Appendix B, M03-L04 and M09-L02 using the existing approved presentation. Keep question content unchanged; report any discovered answer/source inconsistency instead of forcing a coverage pass.

## Source policy

Use Transportstyrelsen or Trafikverket where they support the actual claim. Do not add another authority for the same supported claim. Separate agency guidance, editorial arithmetic and the supplementary approximate stopping model.

- Signs, markings, symbols and panels: [Transportstyrelsen catalogue](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/). H0 must resolve and verify each of the 79 exact detail pages, meaning and illustration variants. Preserve official artwork and Swedish names; identify English wording as editorial translation. Recheck the existing agency reuse terms before adding assets.
- Stopping principles: [Trafikverket: speed and stopping distance](https://www.trafikverket.se/resa-och-trafik/trafiksakerhet/sakerhet-pa-vag/hastighetsgranser-pa-vag/stoppstracka/). Retain the already recorded Trafikverket braking-equation reference in M03-L04. These support the underlying principles, not the question bank's particular shortcut constants.
- Exact stopping shortcut: this research did not locate the combination `(speed/10) × time × 3` and `(speed/10)² × 0.4` in Transportstyrelsen/Trafikverket guidance. [Trafiko's own explanation](https://trafiko.se/faktabank/stoppstracka-reaktionsstracka-bromsstracka) documents the one-second reaction shortcut and the 0.4 dry-asphalt braking shortcut. Cite it only for that approximate method; it is a commercial teaching source, not an official authority. Generalisation to a supplied reaction time is editorial proportional arithmetic. Do not import unrelated claims from that page.
- Fuel context: [Transportstyrelsen: economical driving](https://www.transportstyrelsen.se/sv/vagtrafik/miljo/klimat-och-energi/sparsam-korning/). The equations below follow from the stated litres-per-100-km unit; explain them as editorial arithmetic, not as an agency-prescribed formula. Supplied savings figures are exercise assumptions, not guaranteed benefits of smoother driving.

## Teaching additions and estimated length

| Location | Questions | Proposed teaching | Additional pages |
|---|---:|---|---:|
| Appendix B, existing sign groups | 158 | 79 exact illustrated caption entries, official Swedish name, English meaning, decision/use, and comparisons where needed | 36–42 |
| M03-L04: Leave room to respond | 30 | Distinguish exact unit conversion from rough shortcuts; teach both model equations, variable reaction time, addition, assumptions, rounding, worked examples and self-check answers | 3–4 |
| M09-L02: Use energy with foresight | 40 | Litres/100 km interpretation; journey consumption and savings calculations; worked examples, units, decimals and self-check answers | 2–3 |
| Contents, indexes and source references | — | Added anchors and source entries, index growth and any pagination spill | 2–4 |
| **Total** | **228** | **Estimated final book: 583–593 pages** | **43–53** |

These are planning estimates, not a rendered page count. Existing Appendix B places 321 illustrated entries on 145 pages (about 2.2 entries/page). That supports approximately 36 pages for 79 more entries before extra group/continuation space. Use this density as the basis; do not shrink artwork or captions to force a lower estimate. Reusing space may reduce the net increase; long captions or references may increase it. Confirm after component rendering.

### Stopping-model content

- Define `v` in km/h and `t` in seconds.
- Exact constant-speed reaction calculation: `(v / 3.6) × t`. Existing teaching remains useful.
- Rough exercise reaction estimate: `(v / 10) × t × 3`.
- Rough exercise braking estimate: `(v / 10)² × 0.4`.
- Total in that exercise model: sum the two rough estimates. Do not silently mix exact reaction values with rough-model keyed answers.
- Explain that the reaction shortcut overestimates the exact conversion by about 8%; 0.4 is the shortcut's assumed coefficient, not a universal real-world braking result. Its good-brake/good-tyre/dry-asphalt assumptions do not make it a reliable prediction for an actual car or road.
- Provide at least three independently calculated examples covering 0.5, 1 and 2 seconds, plus questions that require combining the parts. Teach the transferable process rather than copying all 30 bank answers.
- Example: 50 km/h and 2 seconds gives reaction 30 m, braking 10 m, total 40 m in the rough exercise model. Compare separately with exact reaction conversion (about 27.8 m).

### Fuel arithmetic content

- `journey litres = distance in km × consumption in litres/100 km ÷ 100`.
- `litres saved = distance in km × reduction in litres/100 km ÷ 100`.
- If two consumption rates are given, calculate their difference first. Retain units and round only at the requested final precision.
- Consumption example: 120 km at 6.5 litres/100 km uses 7.8 litres.
- Savings example: a supplied reduction of 1.5 litres/100 km over 300 km saves 4.5 litres.
- Explain that consumption varies with real conditions and that exercise rates are supplied/measured assumptions. Do not claim a fixed saving from any technique.

## Execution steps

Each step is separately executable following approval. Maintain progress, decisions and validation in this one plan instead of creating another G-step report tree. Canonical source/asset/build files and final coverage JSONs remain necessary outputs.

| Step | Scope and deliverable | Acceptance gate |
|---|---|---|
| H0 | Freeze baseline hashes and 228 target IDs; verify exact sign detail pages/artwork and scoped source claims; record per-code source URLs and any conflicts here | All 228 IDs assigned once; 79 official sign entries resolved; shortcut provenance/assumptions explicit; no false official attribution |
| H1 | Add A/C/D/E entries to existing Appendix B groups: 28 codes, 56 questions | Exact variants, names and meanings checked against official detail pages; assets and readable captions verified |
| H2 | Add F/G/H/J entries: 36 codes, 72 questions | Direction/public/service/information signs distinguished; no invented duties for informational symbols |
| H3 | Add M/S/T entries: 15 codes, 30 questions; update code lookup and cross-links | Markings, symbols and supplementary qualifications taught in context; all 79 entries present |
| H4 | Extend M03-L04 with the clearly labelled approximate calculation method | All 30 answers recomputed from their actual inputs; model taught in the book; existing exact conversion and braking comparison retained |
| H5 | Extend M09-L02 with consumption and savings arithmetic | All 40 answers recomputed; both methods taught, including decimal inputs and correct units |
| H6 | Rebuild affected components and assemble the complete book; update contents, printed folios, PDF labels, bookmarks and source references | Affected pages visually checked for readable artwork, clipping and layout; links and continuous page numbering pass; delivery/source PDFs identical |
| H7 | Repeat complete 1,000-question audit; regenerate all-question coverage, question-page map, gaps JSON and review | 1,000 covered / 0 not-covered / 0 prompt-only expected; each question maps to actual final teaching pages; no loss of previous 772; bank unchanged |

Reuse the existing approved layout. If implementation requires a new visual design, apply the user's design workflow: imagegen preview and explicit approval before implementing that design. This text plan does not request or implement a new design.

The expected 1,000/1,000 outcome is conditional on source and answer verification. If an exact sign variant or keyed answer cannot be supported, preserve the finding and present the discrepancy; do not mark it covered merely to meet the target.

## Exact target inventory

The following inventory is generated from the final gaps JSON. Family links are discovery starting points; H0 must verify individual detail URLs, not treat this plan as completed per-sign research.

### H1 sign targets

| Family | Codes | Questions | Official discovery source |
|---|---|---:|---|
| A: Warning signs | A6, A7, A12, A17, A23, A32, A33 | 14 | [Transportstyrelsen catalogue](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/) → family A |
| C: Prohibition signs | C4, C5, C7, C8, C9, C10, C11, C12, C13, C14, C15, C29, C30, C33, C34 | 30 | [Transportstyrelsen catalogue](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/) → family C |
| D: Mandatory signs | D8, D9, D12 | 6 | [Transportstyrelsen catalogue](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/) → family D |
| E: Instruction signs | E23, E24, E25 | 6 | [Transportstyrelsen catalogue](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/) → family E |

Each listed code covers the exact IDs `sign-meaning-CODE` and `sign-recognise-CODE`.

### H2 sign targets

| Family | Codes | Questions | Official discovery source |
|---|---|---:|---|
| F: Direction signs | F12, F22, F28, F29, F30, F31, F31a, F32, F33 | 18 | [Transportstyrelsen catalogue](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/) → family F |
| G: Public facilities | G1, G3, G5, G10, G12 | 10 | [Transportstyrelsen catalogue](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/) → family G |
| H: Service facilities | H4, H5, H6, H8, H9, H10, H11, H12, H15, H16, H17, H18, H19, H20, H21, H22, H23, H24, H25, H26, H28 | 42 | [Transportstyrelsen catalogue](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/) → family H |
| J: Information signs | J3 | 2 | [Transportstyrelsen catalogue](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/) → family J |

Each listed code covers the exact IDs `sign-meaning-CODE` and `sign-recognise-CODE`.

### H3 sign targets

| Family | Codes | Questions | Official discovery source |
|---|---|---:|---|
| M: Road markings | M17, M17a, M28, M29, M30, M31, M32, M34 | 16 | [Transportstyrelsen catalogue](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/) → family M |
| S: Symbols | S5, S6, S7, S11, S13 | 10 | [Transportstyrelsen catalogue](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/) → family S |
| T: Supplementary panels | T23, T25 | 4 | [Transportstyrelsen catalogue](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/) → family T |

Each listed code covers the exact IDs `sign-meaning-CODE` and `sign-recognise-CODE`.

### H4 calculation targets

- `stopping-20-0.5`
- `stopping-20-1`
- `stopping-20-2`
- `stopping-30-0.5`
- `stopping-30-1`
- `stopping-30-2`
- `stopping-40-0.5`
- `stopping-40-1`
- `stopping-40-2`
- `stopping-50-0.5`
- `stopping-50-1`
- `stopping-50-2`
- `stopping-60-0.5`
- `stopping-60-1`
- `stopping-60-2`
- `stopping-70-0.5`
- `stopping-70-1`
- `stopping-70-2`
- `stopping-80-0.5`
- `stopping-80-1`
- `stopping-80-2`
- `stopping-90-0.5`
- `stopping-90-1`
- `stopping-90-2`
- `stopping-100-0.5`
- `stopping-100-1`
- `stopping-100-2`
- `stopping-110-0.5`
- `stopping-110-1`
- `stopping-110-2`

### H5 calculation targets

- `fuel-40-5`
- `fuel-40-6`
- `fuel-40-7`
- `fuel-40-8`
- `fuel-60-5`
- `fuel-60-6`
- `fuel-60-7`
- `fuel-60-8`
- `fuel-80-5`
- `fuel-80-6`
- `fuel-80-7`
- `fuel-80-8`
- `fuel-100-5`
- `fuel-100-6`
- `fuel-100-7`
- `fuel-100-8`
- `fuel-120-5`
- `fuel-120-6`
- `fuel-120-7`
- `fuel-120-8`
- `fuel-saving-100-0.5`
- `fuel-saving-100-1`
- `fuel-saving-100-1.5`
- `fuel-saving-100-2`
- `fuel-saving-150-0.5`
- `fuel-saving-150-1`
- `fuel-saving-150-1.5`
- `fuel-saving-150-2`
- `fuel-saving-200-0.5`
- `fuel-saving-200-1`
- `fuel-saving-200-1.5`
- `fuel-saving-200-2`
- `fuel-saving-250-0.5`
- `fuel-saving-250-1`
- `fuel-saving-250-1.5`
- `fuel-saving-250-2`
- `fuel-saving-300-0.5`
- `fuel-saving-300-1`
- `fuel-saving-300-1.5`
- `fuel-saving-300-2`

## Baseline binding

- Book SHA-256: `c21ea3887b3f67bfd40a5683908df990187432a035d025898e7f0700380fa299`
- Question bank SHA-256: `303519698e564c9fb9aa835a29acd743d2038bca54be87cc71efd11951c4a3bb`
- Input inventory: `question-coverage-gaps.json`, 228 records.
- Existing approved G0–G12 history: `g-step-changes.json`; do not recreate deleted execution folders.


## H0 execution record — completed 13 October 2026

**Authorisation:** User approved H0 only. **Acceptance gate:** passed with the rounding and caption/print qualifications below explicitly preserved. H1–H7 remain unexecuted; no claim of new book coverage is made. Existing approved presentation remains the design basis.

### Frozen inputs and target assignments

The [H0 source register](remaining-gap-h0-sources.json) freezes the book, delivery PDF, question bank, gaps JSON, sign inventory/source/asset/caption/placement registers, manuscript and source register, relevant reference/chapter/assembly builders, and retained G-step history. All recorded hashes were rechecked after H0. The two current PDFs remain byte-identical at the recorded book hash. Existing workspace PDF changes/deleted legacy execution snapshots were present before H0 and were left alone.

- Book and delivery PDF SHA-256: `c21ea3887b3f67bfd40a5683908df990187432a035d025898e7f0700380fa299`.
- Question bank SHA-256: `303519698e564c9fb9aa835a29acd743d2038bca54be87cc71efd11951c4a3bb`.
- Gaps SHA-256: `3dab3c2a1ea25188102be14221e10bd1cfa52a111257f990c2a8cc7307a5ed52`.
- Every one of the 228 actual gap IDs is bound once to its existing bank record and one execution step: H1 56, H2 72, H3 30, H4 30, H5 40. These are 79 exact sign codes × two IDs, 30 stopping exercises, 20 consumption exercises and 20 savings exercises. No additional targets or duplicate assignments.
- Baseline remains 540 pages and 772/1,000 covered; 158 not-covered and 70 prompt-only.

### Exact sign source and artwork verification

Retrieved all 79 current individual official detail pages. Every official page code and Swedish name agrees with the bank sign inventory. Each question's current local illustration is byte-identical both to its live inventory image link and to an image explicitly displayed by its exact official detail page. No substituted or generated artwork. Main-page variants and all directly linked alternative detail pages were also retrieved; see the per-code table below. Contact-sheet inspection confirmed the question illustrations and multiple-image variants, including mirrored directions, changed text, vehicle types, gas abbreviations and tunnel letters.

The register stores exact official meaning text, editorial English labels, main/alternative URLs, preferred matching artwork hashes, dimensions where available, and EPS/DWG links where published. Blank descriptive paragraphs mean the official heading supplies the identity; they do not justify invented additional duties. Source HTML is preserved losslessly as compressed evidence, alongside retrieved PNG/JPEG bytes, in [remaining-gap-source-evidence](remaining-gap-source-evidence/). The scratch cache is not the only evidence copy. Print-size/quality and final captions are H1–H3 gates, not an H0 approval to print every raster.

**Reuse recheck:** The current [Transportstyrelsen road-sign-file paragraph](https://www.transportstyrelsen.se/sv/om-oss/pressrum/pressbilder/) remains consistent with the prior record: sign files may be used for different purposes, with proper context requested. Retain official artwork, agency/source credit and editorial-translation labelling. The existing interpretation covering other catalogue families remains an interpretation, not a separate family licence or agency endorsement. The distinct restrictions on ordinary press photographs are outside this permission.

### Scoped calculation sources and findings

- [Trafikverket stopping guidance](https://www.trafikverket.se/resa-och-trafik/trafiksakerhet/sakerhet-pa-vag/hastighetsgranser-pa-vag/stoppstracka/) supports reaction plus braking and dependence on speed, tyres, road/weather and braking. Its illustrated 50 km/h total is 35 m, whereas the exercise shortcut at one second gives 25 m. These are distinct examples/models; do not attribute the bank constants to this page or mix their outputs.
- [Trafiko's own method](https://trafiko.se/faktabank/stoppstracka-reaktionsstracka-bromsstracka) explicitly documents the one-second reaction shortcut and 0.4 braking shortcut under good-brake/good-tyre/dry-asphalt assumptions. It is commercial teaching provenance only. Extension to a supplied reaction time is editorial proportional arithmetic. No unrelated ABS, weight or typical-reaction-time claims are adopted. The reaction shortcut is exactly 8% above constant-speed conversion; the braking coefficient is not a universal real-world prediction.
- Existing M03-L04 source `G3-braking-model`, Trafikverket VGU 2024:148, printed p.9(58), remains retained with its original retrieval limitation and scope. Its fixed-denominator squared-speed derivation does not establish the 0.4 shortcut. H0 did not claim a new direct-PDF download or fresh legal re-audit of that retained reference.
- [Transportstyrelsen economical-driving guidance](https://www.transportstyrelsen.se/sv/vagtrafik/miljo/klimat-och-energi/sparsam-korning/) supports fuel-use context. Distance × rate ÷ 100 is editorial unit arithmetic. Neither fuel equation nor the supplied savings rates are represented as agency prescriptions or guaranteed technique benefits.
- H0 independently parsed actual prompt inputs and recomputed all 70 numerical targets. All 30 stopping and 20 consumption keys equal their exact model/arithmetic results. Sixteen savings keys equal the exact result. Four savings keys use one-decimal ties-to-even rounding, with no precision or convention in their prompts:

| Question | Exact litres saved | Current key | Finding for H5 |
|---|---:|---:|---|
| `fuel-saving-150-0.5` | 0.75 | 0.8 | Rounded result; precision unstated |
| `fuel-saving-150-1.5` | 2.25 | 2.2 | Ties-to-even; conventional half-up would give 2.3 |
| `fuel-saving-250-0.5` | 1.25 | 1.2 | Ties-to-even; conventional half-up would give 1.3 |
| `fuel-saving-250-1.5` | 3.75 | 3.8 | Rounded result; precision unstated |

**Disposition:** Bank preserved. H5 must explicitly disclose the exercise convention and the distinction from exact results, or present the bank discrepancy for an authorised correction. Do not teach ordinary half-up rounding and silently mark these questions passed. H7 must retain this finding when assessing answer selection; the 1,000/1,000 outcome remains conditional. The stopping prompts' phrase “book’s rough dry-road model” is not true of the current printed teaching; H4 is the planned resolution, and these questions remain prompt-only until then.

### Caption and production qualifications carried into H1–H3

These are teaching precision requirements, not evidence that the exact sign illustration is missing from the official catalogue. Short English bank labels often identify an illustration but do not express its full official scope; preserve the bank and write fuller captions.

- A32/C12 cover draught animals generally, not horses exclusively. A7 warns that a road ends at water; A33's pictured snowmobile must not be replaced with a generic road scooter.
- C8 includes supplementary-panel qualifications for tractor b/class I equipment; C10/C11 can extend to class I mopeds by panel; C13/C14 also have explicit panel qualifications. C9/D12 concern orange-plate hazardous loads; D12's letter condition must be explained when that variant is shown.
- C29 has the two-wheeled moped/motorcycle-without-sidecar exception. C34's current question artwork says `STOPP SIGNAL`; teach the red-signal/stop-line meaning as well as the general stated-purpose heading. C33's current artwork is bilingual `TULL/TOLD`.
- D8/D9 also allow walking. E23 marks the far end, in the direction of travel, of the taxi standing place; it is more specific than a generic taxi symbol.
- F28 is a parking garage. F31 indicates a suitable route/bypass for the depicted class; F32 is recommended hazardous-goods routing, distinct from mandatory D12 and prohibitory C9. F33 identifies a numbered rescue location at works or similar, not a general hospital or emergency-parking place.
- H22 is a sight of national interest; “National heritage” must not become a claim of legal heritage designation. H25 is a farm shop for locally made/grown products; “Shop” is too broad for a full caption. H4's question illustration is CNG; do not label LPG/LNG/H₂ variants as CNG. H11/H12/H28 distinguish tents plus living-space vehicles, living-space vehicles only, and motor homes only.
- M17 includes humps, depressions or similar obstacles. M28 indicates a lane for scheduled-service vehicles and others, not an unconditional bus-only claim. M32 reinforces B2; M34's `SKOLA` is one information example, not the definition of the whole code.
- S7 includes two-wheeled motorcycles **and class I mopeds**, both without sidecars. S11 is a mobility-disability symbol; S13 refers to passenger ferry, not an arbitrary boat. Symbols acquire context from the containing sign and do not independently impose invented duties.
- T23 is used under C9 and the B/C/D/E letter matters; the question variant is B. T25 qualifies H5/H6 serving/restaurant facilities, not all businesses.
- S5/S6/S7/S11/S13 official question PNGs contain pale/white symbols that lose contrast on a light page. Identity is verified, but H3 must use an appropriate existing approved presentation/backing or verified official print asset and check it at print size. Do not redraw pixels or mark them print-ready from byte equality alone.

### Per-code official detail URLs and frozen question variants

All links below are exact retrieved individual pages. “Images / alternatives” counts the main detail page's displayed artwork and directly linked alternate detail pages; it does not assert that every allowed real-world configuration is pictured. Full alternative URLs and their own descriptions are in the register. English wording in the bank is editorial translation.

| Step | Code and official Swedish name | Exact official question artwork | Images / alternatives |
|---|---|---|---:|
| H1 | [A6 — Varning för bro](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/varningsmarken/varning-for-bro/) | `a6-1.png` | 1 / 0 |
| H1 | [A7 — Varning för kaj](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/varningsmarken/varning-for-kaj/) | `a7-1.png` | 1 / 0 |
| H1 | [A12 — Varning för stenras](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/varningsmarken/varning-for-stenras/) | `a12-1.png` | 2 / 1 |
| H1 | [A17 — Varning för skidåkare](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/varningsmarken/varning-for-skidakare/) | `a17-1.png` | 1 / 0 |
| H1 | [A23 — Varning för lågt flygande flygplan](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/varningsmarken/varning-for-lagt-flygande-flygplan/) | `a23-1.png` | 2 / 1 |
| H1 | [A32 — Varning för fordon med förspänt dragdjur](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/varningsmarken/varning-for-fordon-med-forspant-dragdjur/) | `a32-1.png` | 3 / 2 |
| H1 | [A33 — Varning för terrängskotertrafik](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/varningsmarken/varning-for-terrangskotertrafik/) | `a33-1.png` | 1 / 0 |
| H1 | [C4 — Förbud mot trafik med motordrivet fordon med fler än två hjul](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/forbud-mot-trafik-med-motordrivet-fordon-med-fler-an-tva-hjul/) | `c4-1.png` | 1 / 0 |
| H1 | [C5 — Förbud mot trafik med motorcykel och moped klass I](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/forbud-mot-trafik-med-motorcykel-och-moped-klass-i/) | `c5-1.png` | 1 / 0 |
| H1 | [C7 — Förbud mot trafik med tung lastbil](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/forbud-mot-trafik-med-tung-lastbil/) | `c7-1.png` | 1 / 0 |
| H1 | [C8 — Förbud mot trafik med traktor och motorredskap klass II](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/forbud-mot-trafik-med-traktor-och-motorredskap-klass-ii/) | `c8-1.png` | 1 / 0 |
| H1 | [C9 — Förbud mot trafik med fordon lastat med farligt gods](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/forbud-mot-trafik-med-fordon-lastat-med-farligt-gods/) | `c9-1.png` | 1 / 0 |
| H1 | [C10 — Förbud mot trafik med cykel och moped klass II](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/forbud-mot-trafik-med-cykel-och-moped-klass-ii/) | `c10-1.png` | 1 / 0 |
| H1 | [C11 — Förbud mot trafik med moped klass II](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/forbud-mot-trafik-med-moped-klass-ii/) | `c11-1.png` | 1 / 0 |
| H1 | [C12 — Förbud mot trafik med fordon förspänt med dragdjur](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/forbud-mot-trafik-med-fordon-forspant-med-dragdjur/) | `c12-1.png` | 1 / 0 |
| H1 | [C13 — Förbud mot trafik med terrängmotorfordon och terrängsläp](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/forbud-mot-trafik-med-terrangmotorfordon-och-terrangslap/) | `c13-1.png` | 1 / 0 |
| H1 | [C14 — Förbud mot ridning](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/forbud-mot-ridning/) | `c14-1.png` | 1 / 0 |
| H1 | [C15 — Förbud mot gångtrafik](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/forbud-mot-gangtrafik/) | `c15-1.png` | 1 / 0 |
| H1 | [C29 — Förbud mot omkörning med tung lastbil](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/forbud-mot-omkorning-med-tung-lastbil/) | `c29-1.png` | 1 / 0 |
| H1 | [C30 — Slut på förbud mot omkörning med tung lastbil](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/slut-pa-forbud-mot-omkorning-med-tung-lastbil/) | `c30-1.png` | 1 / 0 |
| H1 | [C33 — Stopp vid tull](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/stopp-vid-tull/) | `c33-1.png` | 4 / 3 |
| H1 | [C34 — Stopp för angivet ändamål](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/stopp-for-angivet-andamal/) | `c34.png` | 4 / 3 |
| H1 | [D8 — Påbjuden ridväg](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/pabudsmarken/pabjuden-ridvag/) | `d8-1.png` | 1 / 0 |
| H1 | [D9 — Påbjuden led för terrängmotorfordon och terrängsläp](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/pabudsmarken/pabjuden-led-for-terrangmotorfordon-och-terrangslap/) | `d9-1.png` | 1 / 0 |
| H1 | [D12 — Påbjuden körriktning för fordon lastat med farligt gods](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/pabudsmarken/pabjuden-korriktning-for-fordon-lastat-med-farligt-gods/) | `d12-1.png` | 2 / 1 |
| H1 | [E23 — Taxi](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/anvisningsmarken/taxi2/) | `e23-1.png` | 1 / 0 |
| H1 | [E24 — Automatisk trafikövervakning](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/anvisningsmarken/automatisk-trafikovervakning/) | `e24-1.png` | 1 / 0 |
| H1 | [E25 — Betalväg](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/anvisningsmarken/betalvag/) | `e25-1.png` | 1 / 0 |
| H2 | [F12 — Vattendrag](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-vagvisning/vattendrag/) | `f12-1.png` | 1 / 0 |
| H2 | [F22 — Riksmärke](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-vagvisning/riksmarke/) | `f22-2.png` | 2 / 1 |
| H2 | [F28 — Parkeringshus](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-vagvisning/parkeringshus/) | `f28-1.png` | 1 / 0 |
| H2 | [F29 — Infartsparkering](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-vagvisning/infartsparkering/) | `f29-1.png` | 3 / 2 |
| H2 | [F30 — Lokal slinga](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-vagvisning/lokal-slinga/) | `f30-1.png` | 1 / 0 |
| H2 | [F31 — Lämplig väg eller förbifart för visst fordonsslag eller trafikantgrupp](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-vagvisning/lamplig-vag-eller-forbifart-for-visst-fordonsslag-eller-trafikantgrupp/) | `f31-1.png` | 11 / 10 |
| H2 | [F31a — Färdväg för långa fordonståg](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-vagvisning/fardvag-for-langa-fordonstag/) | `f31a.png` | 1 / 0 |
| H2 | [F32 — Farligt gods](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-vagvisning/farligt-gods/) | `f32-1.png` | 1 / 0 |
| H2 | [F33 — Räddningsplats](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-vagvisning/raddningsplats/) | `f33-1.png` | 1 / 0 |
| H2 | [G1 — Post](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-allmanna-inrattningar-med-mera/post/) | `g1-1.png` | 1 / 0 |
| H2 | [G3 — Radiostation för vägtrafikinformation](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-allmanna-inrattningar-med-mera/radiostation-for-vagtrafikinformation/) | `g3-1.png` | 1 / 0 |
| H2 | [G5 — Industriområde](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-allmanna-inrattningar-med-mera/industriomrade/) | `g5-1.png` | 1 / 0 |
| H2 | [G10 — Handelsområde](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-allmanna-inrattningar-med-mera/handelsomrade/) | `g10.png` | 1 / 0 |
| H2 | [G12 — Personfärja](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-allmanna-inrattningar-med-mera/personfarja/) | `g12.png` | 1 / 0 |
| H2 | [H4 — Gas för fordonsdrift](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/gas-for-fordonsdrift/) | `h4-1.png` | 4 / 3 |
| H2 | [H5 — Servering](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/servering/) | `h5-1.png` | 1 / 0 |
| H2 | [H6 — Restaurang](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/restaurang/) | `h6-1.png` | 1 / 0 |
| H2 | [H8 — Vandrarhem](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/vandrarhem/) | `h8-1.png` | 1 / 0 |
| H2 | [H9 — Stugby](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/stugby/) | `h9-1.png` | 1 / 0 |
| H2 | [H10 — Stuga](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/stuga/) | `h10-1.png` | 1 / 0 |
| H2 | [H11 — Campingplats](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/campingplats/) | `h11-1.png` | 1 / 0 |
| H2 | [H12 — Husvagnsplats](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/husvagnsplats/) | `h12-1.png` | 1 / 0 |
| H2 | [H15 — Badplats](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/badplats/) | `h15-1.png` | 1 / 0 |
| H2 | [H16 — Friluftsområde](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/friluftsomrade/) | `h16-1.png` | 1 / 0 |
| H2 | [H17 — Vandringsled](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/vandringsled/) | `h17-1.png` | 1 / 0 |
| H2 | [H18 — Stollift](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/stollift/) | `h18-1.png` | 1 / 0 |
| H2 | [H19 — Släplift](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/slaplift/) | `h19-1.png` | 1 / 0 |
| H2 | [H20 — Golfbana](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/golfbana/) | `h20-1.png` | 1 / 0 |
| H2 | [H21 — Försäljningsställe för fiskekort](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/forsaljningsstalle-for-fiskekort/) | `h21-1.png` | 1 / 0 |
| H2 | [H22 — Sevärdhet](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/sevardhet/) | `h22-1.png` | 1 / 0 |
| H2 | [H23 — Förberedande upplysning om vägnära service](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/forberedande-upplysning-om-vagnara-service/) | `h23.png` | 1 / 0 |
| H2 | [H24 — Rum och frukost](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/rum-och-frukost/) | `h24-1.png` | 1 / 0 |
| H2 | [H25 — Gårdsbutik](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/gardsbutik/) | `h25.png` | 1 / 0 |
| H2 | [H26 — Hantverk](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/hantverk/) | `h26.png` | 1 / 0 |
| H2 | [H28 — Anläggning som enbart tillhandahåller platser för bilar med bostadsutrymme](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-upplysning-om-serviceanlaggningar-med-mera/anlaggning-tillhandahaller-plats-for-bil-med-bostadsutrymme/) | `h28.png` | 1 / 0 |
| H2 | [J3 — Livsfarlig ledning](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/upplysningsmarken/livsfarlig-ledning/) | `j3-1.png` | 2 / 1 |
| H3 | [M17 — Farthinder](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/vagmarkeringar/farthinder/) | `m17-1.png` | 1 / 0 |
| H3 | [M17a — Cykelbox](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/vagmarkeringar/cykelbox/) | `m17a-cykelbox.png` | 1 / 0 |
| H3 | [M28 — Buss](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/vagmarkeringar/buss/) | `m28-1.png` | 1 / 0 |
| H3 | [M29 — Hastighet](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/vagmarkeringar/hastighet/) | `m29-1.png` | 1 / 0 |
| H3 | [M30 — Vägnummer](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/vagmarkeringar/vagnummer/) | `m30.png` | 1 / 0 |
| H3 | [M31 — Ändamålsplats](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/vagmarkeringar/andamalsplats/) | `m31-1.png` | 1 / 0 |
| H3 | [M32 — Stopp](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/vagmarkeringar/stopp/) | `m32-1.png` | 1 / 0 |
| H3 | [M34 — Information](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/vagmarkeringar/information/) | `m34-1.png` | 1 / 0 |
| H3 | [S5 — Buss](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/symboler/buss/) | `s5-1.png` | 1 / 0 |
| H3 | [S6 — Traktor och motorredskap klass II](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/symboler/traktor-och-motorredskap-klass-ii/) | `s6-1.png` | 1 / 0 |
| H3 | [S7 — Motorcykel](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/symboler/motorcykel/) | `s7-1.png` | 1 / 0 |
| H3 | [S11 — Rörelsehindrade](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/symboler/rorelsehindrade/) | `s11-1.png` | 1 / 0 |
| H3 | [S13 — Personfärja](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/symboler/personfarja/) | `s13-1.png` | 1 / 0 |
| H3 | [T23 — Tunnelkategori](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/tillaggstavlor/tunnelkategori/) | `t23-1.jpg` | 4 / 3 |
| H3 | [T25 — Öppet dygnet runt](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/tillaggstavlor/oppet-dygnet-runt/) | `t25-1.png` | 1 / 0 |

### H0 validation and next step

- 228 unique targets, exact gaps-set equality; assignments H1/H2/H3/H4/H5 = 56/72/30/30/40.
- 79 official code/name matches and 79 exact question-artwork byte matches; 110 displayed official images and 31 linked alternate detail pages recorded.
- 66 exact numerical results and four explicitly recorded rounding qualifications; no bank changes and no fabricated official shortcut attribution.
- Compressed source evidence and frozen inputs pass offline SHA-256 verification. Run `python3 tools/verify_remaining_gap_baseline.py --offline` from the repository root; it needs only the standard library. A new online capture needs BeautifulSoup, available in the existing `tmp/python` environment; retain this register as the approved baseline rather than overwriting it later.

**Next executable scope:** H1, the 28 A/C/D/E codes and 56 questions, using these verified sources and the existing approved Appendix B presentation. No new design was required or implemented in H0.


## H1 execution record — completed 13 October 2026

**Authorisation:** User approved H1. **Acceptance gate:** 28 A/C/D/E entries added and verified, supplying the illustrated caption units for H1's 56 question IDs in the reference component. No new visual design was needed; the approved card, font, column, spacing and artwork-size rules were reused.

### Changes

Added the seven A, fifteen C, three D and three E codes to eight existing Appendix B groups. Each card preserves the official Swedish name, contains an editorial English meaning and use/decision explanation, identifies the exact question variant, and carries the individual official URL and a 13 October caption-check date. Canonical source, asset, caption and placement JSON registers and their Markdown views are updated. The original 498 caption records and 321 placement bindings are unchanged, checked against the pre-H1 repository versions.

Artwork is the exact H0-verified official PNG for each question; source/asset hashes agree with the frozen H0 register. All 28 files decoded successfully. Print dimensions stay within their own 300 ppi maxima; the renderer's existing larger-artwork caps remain in effect. No artwork was redrawn, replaced with a similar code, or enlarged beyond its limit. The asset and caption registers retain the H0 detail-page snapshots and variant/reuse evidence.

Caption checks explicitly retain draught-animal scope, C8/C10/C11/C13/C14 panel qualifications, C9/D12 orange-plate scope, C29's exception and C30 endpoint, pedestrian permission on D8/D9, E23's far-boundary meaning, and the broader monitoring/charging meanings of E24/E25. C34's actual `STOPP SIGNAL` illustration is explained as a signal-related stop instruction rather than replaced with a generic stop-sign duty. C33's actual bilingual `TULL/TOLD` artwork is distinguished from the other official customs-text variants.

The [updated reference component](../../../output/pdf/korkortgo-reference-material.pdf) contains **211 pages and 349 unique illustrated entries**, up from 201 pages and 321 entries: **10 additional pages**. The source component and output copy are byte-identical. The full 540-page book, delivery book, question bank and final gaps/coverage files remain at the H0 hashes. This component is ready for later H6 assembly; these standalone page numbers are not final full-book teaching-page mappings, and H7 has not recalculated whole-book coverage.

### H1 code-to-component-page mapping

For each code below, both `sign-meaning-CODE` and `sign-recognise-CODE` map to the same exact illustrated caption unit. The reference verification JSON records all 56 IDs individually. H6/H7 must replace these component pages with final assembled-book pages.

| Code | Existing group | Reference component page |
|---|---|---:|
| E24 | RB11 | 66 |
| C4 | RB12 | 76 |
| C5 | RB12 | 77 |
| C8 | RB12 | 77 |
| C10 | RB12 | 77 |
| C11 | RB12 | 78 |
| C12 | RB12 | 78 |
| C13 | RB12 | 78 |
| C14 | RB12 | 79 |
| C15 | RB12 | 79 |
| C34 | RB12 | 79 |
| D8 | RB12 | 80 |
| D9 | RB12 | 80 |
| A17 | RB13 | 89 |
| E23 | RB16 | 108 |
| A6 | RB17 | 117 |
| A7 | RB17 | 117 |
| A12 | RB17 | 118 |
| A23 | RB17 | 118 |
| A32 | RB17 | 118 |
| C29 | RB17 | 119 |
| C30 | RB17 | 119 |
| A33 | RB21 | 146 |
| C7 | RB22 | 154 |
| C9 | RB22 | 155 |
| C33 | RB22 | 155 |
| D12 | RB22 | 156 |
| E25 | RB23 | 158 |

### Validation and handoff

- Reference verifier passes all 349 exact placements, complete caption/variant/Swedish-name text, original appendix/glossary/practice/source text, artwork SHA-256 and 300 ppi size limits, font embedding, accessible text equivalents, internal destinations and external source links. No duplicate entries or missing H1 codes.
- 610 internal links and 561 named destinations pass; all 24 existing groups remain. The reference builder automatically retains code-lookup links for every added entry.
- Rebuilding produces the same SHA-256. The source and delivery reference PDFs are identical: `4111f4a1546633fca53a7dbba0efe75cd63760df311a47ea00dacf1365211bbb`.
- All **16 pages containing H1 additions** were rendered at 110 dpi and inspected, including older entries sharing those pages: 66, 76–80, 89, 108, 117–119, 146, 154–156 and 158. Artwork, Swedish names, caption text, URLs, separators, headers and folios are readable with no overlap or clipping. The four code-lookup pages (166–169) and updated artwork-credit page (211) were also rendered and inspected: 21 pages in total. All-page text-bound checks pass. Temporary review renders are in `tmp/pdfs/h1`; validation is recorded here and in the existing reference `verification.json`, not a new execution-report tree.
- Full-book/delivery, bank and gaps hashes still match H0. The baseline verifier now supports `python3 tools/verify_remaining_gap_baseline.py --offline --allow-teaching-changes` for H1–H5: it checks the frozen book/bank/gaps and all saved evidence/artwork while allowing authorised canonical teaching-register/build changes. The original frozen hashes are preserved, not overwritten.
- H0 rounding findings are unchanged and remain for H5. Full assembly, final folios and full-book coverage remain H6/H7; no 828/1,000 final-book coverage claim is made from a standalone component.

**Next executable scope:** H2, the 36 F/G/H/J codes and 72 questions. H2–H7 have not started.


## H2 execution record — completed 13 October 2026

**Authorisation:** User approved H2. **Acceptance gate:** All 36 F/G/H/J codes have exact illustrated caption entries for their 72 target IDs in the reference component. The existing approved Appendix B presentation was reused; no new design was requested or implemented.

### Changes and source decisions

Added nine F direction entries, five G public-facility entries, 21 H service entries and J3. These extend existing groups RB07, RB09, RB10, RB22 and RB24. Canonical source, asset, caption and placement JSON registers and their Markdown views are updated, with exact official Swedish names, individual URLs, editorial English wording, exact-variant descriptions and 13 October checks. The previous 526 caption records and 349 placement bindings, including all H1 entries, are unchanged; verified against snapshots taken before H2.

The 36 original PNGs are byte-identical to the H0-verified question variants. For **F30 and F31**, the original PNGs would permit only about 12 mm print width at 300 ppi. Their officially linked `f30-1.eps` and `f31-1.eps` were retrieved from Transportstyrelsen and rendered at 300 ppi using Ghostscript with EPS cropping and no artwork edits. Comparison against the original question PNGs confirmed the exact local-loop and left-facing lorry variants. Original EPS/PNG bytes, derived-image hashes, official EPS URLs and [the comparison proof](../sign-assets/proofs/h2-f30-f31.png) are retained in the asset/caption/placement records. The reference uses these clearer EPS renders; all other H2 entries use their exact official PNGs. Every placement obeys its own 300 ppi maximum and the existing renderer's artwork caps.

Teaching qualifications carried forward from H0:

- F28 identifies a parking garage; F29 identifies parking connected to public transport, with the transport type read from the symbol. F30 is local-loop guidance; F31 indicates a suitable route/bypass for the pictured class, not a blanket access prohibition. F31a identifies long-combination routing without claiming general permission for every combination.
- F32 is recommended routing for orange-plate dangerous-goods loads, compared with mandatory D12 and prohibitory C9. F33 identifies a numbered rescue location at works or similar, distinct from general medical/emergency-parking facilities.
- G12 is passenger-ferry information without a promise that a car can board. G3's station/frequency details are illustration examples, not instructions to operate a radio while driving.
- H4's exact CNG artwork is distinguished from LPG/LNG/H₂ variants. H9/H10 distinguish many/few cottages; H11/H12/H28 distinguish tents plus living-accommodation vehicles, living-accommodation vehicles only, and motor homes only. H18/H19 distinguish seated chair lift from a ski tow.
- H22 identifies a sight of national interest without inventing legal heritage status. H25 is a farm shop for local products, more precise than the bank's broad “Shop” label. H23's distance is to the exit/junction, not a promise that all services are immediately beside the sign. Service/public-facility symbols provide information; captions do not invent independent traffic duties or guarantee availability.
- J3 explains a dangerous overhead electrical line. The exact wider warning is shown and the narrower official variant is identified; no numerical safe clearance is invented.

The [updated reference component](../../../output/pdf/korkortgo-reference-material.pdf) now has **225 pages and 385 unique illustrated entries**, up from H1's 211 pages and 349 entries: **14 additional pages**. It remains a standalone component for H6 assembly. The full 540-page book, delivery book, bank and gaps files retain the H0 hashes; final whole-book coverage is not recalculated in H2.

### H2 code-to-component-page mapping

Both `sign-meaning-CODE` and `sign-recognise-CODE` map to the exact illustrated caption unit below. The existing reference verification JSON records all 72 IDs and refreshes the 56 H1 mappings to their current component pages. The H1 table above records the earlier H1 build; final assembled-book page mappings remain H6/H7 work.

| Code | Existing group | Reference component page |
|---|---|---:|
| F12 | RB07 | 46 |
| F22 | RB07 | 46 |
| F28 | RB07 | 47 |
| F29 | RB07 | 47 |
| F30 | RB07 | 48 |
| F31 | RB07 | 48 |
| G1 | RB09 | 63 |
| G3 | RB09 | 63 |
| G5 | RB09 | 63 |
| G10 | RB09 | 64 |
| G12 | RB09 | 64 |
| H4 | RB09 | 65 |
| H5 | RB09 | 65 |
| H6 | RB09 | 65 |
| H8 | RB09 | 66 |
| H9 | RB09 | 66 |
| H10 | RB09 | 66 |
| H11 | RB09 | 67 |
| H12 | RB09 | 67 |
| H15 | RB09 | 67 |
| H16 | RB09 | 68 |
| H17 | RB09 | 68 |
| H18 | RB09 | 68 |
| H19 | RB09 | 69 |
| H20 | RB09 | 69 |
| H21 | RB09 | 69 |
| H22 | RB09 | 70 |
| H23 | RB09 | 70 |
| H24 | RB09 | 71 |
| H25 | RB09 | 71 |
| H26 | RB09 | 71 |
| H28 | RB09 | 72 |
| J3 | RB10 | 75 |
| F31a | RB22 | 169 |
| F32 | RB22 | 170 |
| F33 | RB24 | 178 |

### Validation and handoff

- Reference verification passes all **385** placements, artwork hashes and print-size limits, complete teaching/variant/Swedish-name text, source links, appendix/glossary/practice/source fidelity, font embedding, text equivalents and all-page text bounds. All 24 existing groups remain; no duplicate or missing H2 entries.
- **660 internal links** and **611 named destinations** pass. All 72 H2 IDs map to their actual component teaching pages; all 56 H1 target mappings remain valid.
- Deterministic rebuild and identical source/delivery PDFs pass. Current reference SHA-256: `b09da416bfd362cc8d87a45ca4fa42eb76523951b523dbe6e0ae1016ab5eec07`.
- Visually inspected **22 rendered pages**: 17 containing H2 entries, four lookup pages and the updated artwork-credit page. Review pages: 46, 47, 48, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 75, 169, 170, 178, 180, 181, 182, 183, 225. All inspected artwork, Swedish names, captions, wrapped URLs, separators, headers and folios are readable with no overlap or clipping. F30/F31 official print renders were separately checked against the question variants. Scratch review renders are in `tmp/pdfs/h2`; this plan and the existing reference verification/source-checks JSONs retain the results, with no new execution-report tree.
- `python3 tools/verify_remaining_gap_baseline.py --offline --allow-teaching-changes` passes the frozen book/bank/gaps and all saved H0 evidence/artwork checks. Source-text whitespace checks pass. Prior H0 rounding findings remain for H5; no bank changes or manufactured coverage pass.

**Next executable scope:** H3, the 15 M/S/T codes and 30 questions, including the recorded white-symbol contrast issue. H3–H7 have not started. Full-book assembly/folios and final 1,000-question audit remain H6/H7.


## H3 execution record — completed 13 October 2026

**Authorisation:** User approved H3. **Acceptance gate:** All 15 M/S/T codes have exact illustrated caption entries for their 30 target IDs; all 79 planned codes from H1–H3 are present. The existing approved raster and full-width vector-card formats were reused. No new visual design, symbol recolouring or invented sign assembly was required.

### Changes and artwork decisions

Added eight markings (M17, M17a, M28–M32, M34), five symbols (S5–S7, S11, S13) and two panels (T23, T25) across existing groups RB02, RB05, RB06, RB07, RB09, RB11, RB13, RB16 and RB22. Canonical source, asset, caption and placement JSON registers and their Markdown views are updated. Each entry retains the official Swedish name, exact individual source URL, an editorial English caption, the exact question variant, and a 13 October check date. All previous **562 caption records and 385 placement bindings** remain unchanged, checked against snapshots taken before H3.

The 15 original question-artwork files are byte-identical to H0; their unchanged bytes are retained. The H0 symbol-contrast finding was refined by inspecting the actual pixels: these five PNGs contain faint, partly transparent black outlines, rather than solid white silhouettes. A dark background would worsen their contrast. The exact officially linked EPS files were retrieved and converted to vector PDFs, with paths, colours and stroke widths preserved. They use the already approved full-width vector-card treatment on white, with minimum reviewed widths **80 mm** for S5/S6/S7/S11 and **110 mm** for S13. The larger sharp outlines and full captions make the symbols readable without altering the agency artwork. [Original/rendered symbol comparisons](../sign-assets/proofs/h3-symbol-variants.png) retain exact-variant evidence.

Rendering also exposed a separate size limitation: the original PNGs for **M17, M28, M29, M31, M32 and M34** permit only about **5 mm** width at 300 ppi. Their exact officially linked EPS files were retrieved and rendered at 300 ppi for the normal existing raster-card format. [Original/rendered marking comparisons](../sign-assets/proofs/h3-marking-variants.png) confirm the same patterns, numbers and words. The preliminary tiny-artwork render was rejected and rebuilt before final validation. M17a, M30, T23 and T25 retain their exact official original PNG/JPEG files. No pixel enlargement beyond the recorded raster limits or artwork editing is used. Original EPS hashes, derived-image hashes, official URLs and both comparison proofs are recorded in the canonical manifests.

### Teaching and cross-links

- M17 includes humps, depressions or similar obstacles. M17a indicates suitable placement for cyclists and class II moped riders without inventing priority. M28 is for scheduled-service vehicles and others; its BUSS wording is not treated as an unconditional bus-only restriction.
- M29's 30 is maximum-speed information, contrasted with M30's E4 route number. M31's LASTPLATS is one stated-purpose example. M32 reinforces B2 and does not invent a separate stop position. M34's SKOLA is one information example, not the definition of every M34 marking.
- S5/S6/S7/S11 acquire their actual duties or qualifications from the containing sign/panel. S7 explicitly includes two-wheeled motorcycles and class I mopeds, both without sidecars. S11 does not create a complete parking entitlement by itself. S13 concerns a passenger ferry without promising that a car may board.
- T23 is taught below C9, including the B/C/D/E category meaning; the exact question panel is **B**. T25 qualifies **H5/H6** refreshments/restaurant opening information and is not a parking-duration limit.
- The code lookup includes every new entry. Added working group cross-links from RB05 to M17a/M29/M30/M31/M32, RB06 to S13/T23/T25, RB11 to M30, and RB24 to T23. The reference verifier checks those destinations. These are separate comparison entries, not fabricated combined road signs.

The [updated reference component](../../../output/pdf/korkortgo-reference-material.pdf) now has **234 pages and 400 unique illustrated entries**, up from H2's 225 pages and 385 entries: **nine additional pages**. All 79 planned sign codes and their 158 question IDs now have component teaching-page mappings. The full 540-page book, delivery book, bank and gaps files retain the H0 hashes; assembled-book page mappings and coverage totals remain H6/H7 work.

### H3 code-to-component-page mapping

Both `sign-meaning-CODE` and `sign-recognise-CODE` map to the same exact illustrated caption unit. The existing reference verification JSON stores the 30 H3 mappings and refreshed mappings for all 128 H1/H2 target IDs. Earlier H1/H2 tables are historical build records.

| Code | Existing group | Reference component page |
|---|---|---:|
| M32 | RB02 | 16 |
| M17 | RB05 | 30 |
| M28 | RB05 | 31 |
| M34 | RB05 | 31 |
| S5 | RB06 | 41 |
| S6 | RB06 | 42 |
| S7 | RB06 | 43 |
| S11 | RB06 | 44 |
| M30 | RB07 | 56 |
| S13 | RB09 | 79 |
| T25 | RB09 | 80 |
| M29 | RB11 | 87 |
| M17a | RB13 | 110 |
| M31 | RB16 | 129 |
| T23 | RB22 | 178 |

### Validation and handoff

- Reference verification passes all **400** placements, complete caption/variant/Swedish-name text, artwork/source hashes, raster size limits and vector minimum widths, font embedding, text equivalents, all-page text bounds and preserved appendix/glossary/practice/source text. All 24 groups remain; the component has 18 vector placements. All 79 planned sign codes are present once, with no missing H1/H2/H3 targets.
- **698 internal links** and **635 named destinations** pass, including the new comparison links and every new code-lookup link. All 158 target sign-question IDs map to actual component teaching pages.
- Final deterministic rebuild and source/delivery PDF equality pass. Reference SHA-256: `142953ea992d5285a9b96fd26f00595ef3cbb737a56fb0dc9096ccb50fdf8abf`.
- **23 final rendered pages** inspected at 110 dpi: 14 with H3 entries, affected cross-reference pages, four lookup pages and the artwork-credit page. Pages: 16, 30, 31, 32, 41, 42, 43, 44, 46, 56, 79, 80, 87, 90, 110, 129, 178, 188, 189, 190, 191, 192, 234. The final markings and enlarged symbol outlines, Swedish names, captions, source URLs, links, separators, headers and folios are readable without overlap or clipping. Temporary inspection renders are in `tmp/pdfs/h3`; comparison proofs are canonical assets. Validation remains in this plan and the existing reference verification/source-checks JSONs, with no new execution-report tree.
- The baseline verifier with `--offline --allow-teaching-changes` passes frozen book/bank/gaps and H0 evidence/artwork checks. All prior caption/binding records are preserved and source-text whitespace checks pass. H0's four fuel-rounding findings remain unchanged for H5. No full-book coverage pass is claimed from this standalone component.

**Next executable scope:** H4, teaching the clearly labelled approximate stopping calculation in M03-L04 for 30 questions. H4–H7 have not started; full assembly/folios and final coverage auditing remain H6/H7.


## H4 execution record — completed 13 October 2026

**Authorisation:** User approved H4. **Acceptance gate:** M03-L04 now teaches both clearly labelled approximate exercise equations, variable reaction time, addition, assumptions, final-only rounding, independently calculated examples and separated practice answers. All 30 target keys and explanation breakdowns recompute from their actual prompt inputs. No new visual design was required; existing lesson typography and page structure were reused.

### Teaching and source changes

Added two dedicated teaching pages: “A rough calculation method” and “Apply the rough model”. Define v in km/h and t in seconds; teach R = (v ÷ 10) × t × 3, B = (v ÷ 10)² × 0.4 and S = R + B, with metres throughout. Decimal working is preserved and rounding is only at a requested final precision. The time input changes reaction, not this model's braking part.

Three worked examples cover 0.5, 1 and 2 seconds, with reaction, braking and total shown separately:

| Supplied inputs | Rough reaction | Rough braking | Rough total |
|---|---:|---:|---:|
| 40 km/h, 0.5 s | 6 m | 6.4 m | 12.4 m |
| 70 km/h, 1 s | 21 m | 19.6 m | 40.6 m |
| 50 km/h, 2 s | 30 m | 10 m | 40 m |

Three further practice calculations have separate lesson answers: 30 km/h/0.5 s gives 8.1 m; 80 km/h/1 s gives 49.6 m; 100 km/h/2 s gives 100 m. The lesson knowledge check now asks for these calculations and why exact reaction conversion must be kept separate. This teaches a transferable method rather than listing all 30 bank answers.

The prior exact conversion illustration, following-gap advice, tailgater guidance and VGU braking-distance comparison remain. The new comparison gives exact constant-speed reaction at 50 km/h/2 s as about 27.8 m versus rough reaction of 30 m, explains the exact 8% reaction overestimate, and warns that mixing exact reaction with rough braking yields a different model answer.

Canonical manuscript/source/claim registers and Chapter 3 source-checks are updated using the same-day H0 source evidence. Trafiko is explicitly a **commercial teaching source** for the one-second reaction and 0.4 dry-asphalt braking shortcuts; variable-time multiplication and the 8% comparison are editorial arithmetic. Good-brake/good-tyre/dry-asphalt assumptions do not make the coefficient universal or predict an actual stop. Trafikverket supports the underlying reaction-plus-braking and conditions principles, not those constants. No unrelated claims from the commercial page were imported. The existing `G3-braking-model` source and its retrieval limitation remain unchanged.

Chapter source pages are now titled **Sources and references**, with the commercial source identified in the teaching and source notes. The canonical final reference list adds Trafikverket's principles and a separately labelled supplementary commercial-teaching subsection. That reference component will be rebuilt in H6; H4 rebuilt only the affected Chapter 3 component.

### Component output and validation

The [updated Chapter 3 component](../../../output/pdf/korkortgo-chapter-03.pdf) has **54 pages**, up from 52: **two added pages**. This is below the planning estimate of 3–4 because the existing answer/reference pages accommodate the additions; fonts, spacing and artwork were not reduced to fit. All 100 prior sign placements remain. Approximate equations and assumptions are on component page **46**, worked examples and practice prompts on **47**, and answers on **51**. Exact conversion remains on **44**, and the separate braking comparison on **45**. H6/H7 must map these to final full-book pages.

- The chapter verifier independently parsed all 30 actual speed/time prompts, recomputed reaction as 0.3 × speed × time and braking as 0.004 × speed², and checked every keyed total and explanation's reaction/braking/total values. All 30 pass; individual inputs, results and component teaching pages are recorded in the existing chapter verification JSON.
- Manuscript fidelity, all 100 official placements/asset hashes, embedded fonts, text equivalents, all-page text bounds, source URLs, 64 internal links and 60 named destinations pass. Practice answers remain non-facing and separate from prompts.
- Deterministic rebuild and source/delivery PDF equality pass. Chapter SHA-256: `78dec79ed9507fae0fee3dbb45019918e6e2f5c65c5564c69fedac2068ef362c`.
- Ten relevant final pages rendered and visually inspected at 115 dpi: 1, 44–48 and 51–54. Equations, superscripts, decimal values, examples, answer separation, source labelling, wrapped URLs, headers and folios are readable without clipping or overlap. Scratch renders are in `tmp/pdfs/h4`; this plan and existing chapter/source verification JSONs retain the results, with no new execution-report tree.
- Frozen full book/delivery, bank and gaps remain at their H0 hashes. The baseline verifier with `--offline --allow-teaching-changes` and source-text whitespace checks pass. H0's fuel-rounding findings remain for H5. The current 540-page assembled book is unchanged; no final-book coverage increase is claimed until H6/H7.

**Next executable scope:** H5, consumption and savings arithmetic in M09-L02 for 40 questions, explicitly preserving/resolving the recorded four midpoint-rounding qualifications. H5–H7 have not started.
