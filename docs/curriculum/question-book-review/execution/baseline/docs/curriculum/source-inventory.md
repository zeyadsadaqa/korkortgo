# Step 1 — Curriculum source inventory

**Completed: 1 October 2026. Scope: Swedish category B driving theory, written for English-speaking learners.**

This inventory is the research handoff for step 2. It accounts for the supplied book, identifies relevant official sources, and records gaps and updates before the curriculum is rewritten. It does not propose a new lesson sequence or change the app.

## Deliverables

- [Book coverage checklist](book-coverage.md): all 39 source sections, their topics, and matching official references.
- [Book coverage data](book-coverage.json): book identity, checksum, section ranges, and an inventory of all 367 PDF pages.
- [Official source index](official-source-index.md): readable links and retrieval status for 125 source records.
- [Official source data](official-sources.json): stable source IDs, URLs, retrieval dates, checksums, headings, and further official links.
- [Road-sign inventory](road-sign-inventory.json): 343 existing assets, local integrity checks, catalogue comparison, missing variants, and reuse source.

These files are internal research documents. Book titles and original page numbers belong here for traceability; they are not proposed learner-facing labels.

## Scope and method

“All information” is interpreted as all relevant category B learning coverage from the supplied book and the two requested authorities. Neither authority's entire website is a category B curriculum: aviation, shipping, procurement, road design standards, professional-driver training and unrelated administrative material are outside this inventory. Information about other road users is included where a car driver needs it. B96/BE boundaries are relevant; complete B96/BE courses are outside scope.

The supplied PDF is **Theory Book — Driving Licence Book 2026**, edition **2026-1**, published **1 January 2026**, by **Hagberg Media AB / Körkortonline.se**, ISBN **978-91-991023-1-3**. It contains 367 PDF pages and 39 table-of-contents sections. Its SHA-256 checksum is recorded in the coverage data.

All pages were text-extracted and classified, including section dividers, questions, explanations, signs, court examples and the final advertisement. The topic review covers every section. Representative visual checks covered the contents, junction diagrams, crossings, the vehicle-speed table, a registration-document example, signs, signals and court-case diagrams. This is an inventory-level review, not a complete diagram-by-diagram verification or a validation of every factual claim.

Printed page numbering agrees with PDF positions from page 3 onward in the inspected samples. Source chapter ranges exclude the following chapter's divider; those divider pages are explicitly assigned in the page inventory. No page is silently discarded.

Official pages were discovered through current web searches, links from the authorities' topic hubs, and existing project references, then checked afresh. Of 125 source records, **121 were retrieved successfully**, **two old/discovery URLs failed and have working replacements**, **one background hub needs manual content inspection**, and **one eco-driving background PDF was located through a search excerpt but did not download successfully**. The latter two are not needed to establish the curriculum's core scope; the official syllabus and driving-test guide independently cover environmentally responsible driving.

“Retrieved” means the source was accessible and its topic scope was inventoried on the stated date. It does not mean every linked document or every claim has been verified. Publication dates, rule commencement dates and retrieval dates must stay distinct. Working copies are in `tmp/pdfs/source-inventory/`; the durable handoff is in this directory and does not depend on those temporary copies.

## The official foundation

The curriculum needs two complementary coverage checks:

1. **Education objectives:** Transportstyrelsen's [category B syllabus, TSFS 2011:20](https://www.transportstyrelsen.se/TSFS/TSFS%202011_20.pdf) covers vehicle control and environment, different traffic environments, journey circumstances, and personal influences. It includes both knowledge/practical ability and self-assessment. Use it to check what learners should be able to explain, apply and assess about themselves.
2. **Examination domains:** Trafikverket's [category B test guide](https://www.trafikverket.se/korkort/ta-korkort/personbil-och-latt-lastbil/) identifies vehicle knowledge/manoeuvring, environment, road safety, traffic rules and personal factors. Use these domains as coverage tags, not necessarily as the new curriculum's module names.

The [practical-test guide](https://www.trafikverket.se/korkort/ta-korkort/personbil-och-latt-lastbil/sa-gar-korprovet-till/) supplies a bridge from theory to observation, manoeuvring, safety checks and decisions in real traffic. A PDF supports this learning; it does not replace driving practice or mandatory training.

For rule statements, use current official guidance and the applicable underlying provisions, including exceptions and commencement dates. For teaching examples and explanations, use independently written scenarios. Do not treat the book's interpretation of a rule as authoritative merely because it quotes or mentions an authority.

## Coverage established

The detailed 39-row checklist preserves the following source coverage:

| Coverage family | Source sections | Main content |
|---|---:|---|
| Traffic situations and rules | 12 | General duties, lanes, junctions, crossings, roundabouts, parking, rural roads, motorways, overtaking, railways, special streets and seasonal conditions |
| People and risk | 7 | Learning, judgement, alcohol/drugs/distraction, fatigue, observation, disability/ageing, children and incidents |
| Vehicle use and ownership | 15 | Vehicle classes, distances, tyres, steering, brakes, protection, child restraints, dimensions, loads/trailers, lights, checks, inspections, maintenance, documents and insurance |
| Environment | 3 | Climate/pollution/noise, efficient driving, fuels/powertrains and environmental zones |
| Signs and other instructions | 1 | All sign families, panels, markings, traffic signals, railway signals, police and traffic-guard directions |
| Applied judgement | 1 | Court-case subject matter and practical interpretation issues; independently sourced examples required before reuse |

The book's practice questions are included in the coverage review. Their wording, answer options, photographs and distinctive scenarios are not a reusable question bank for the new curriculum.

## Additions to carry into step 2

These are coverage requirements, not approved lesson titles or a proposed teaching order.

| Requirement | Why include it | Source |
|---|---|---|
| Learner self-assessment throughout | Learners must evaluate capability, limits and choices, not just recall facts | [Official syllabus](https://www.transportstyrelsen.se/TSFS/TSFS%202011_20.pdf) |
| Journey planning and alternatives | Cover route, timing, passengers, weather, rest and choice of transport | [Official syllabus](https://www.transportstyrelsen.se/TSFS/TSFS%202011_20.pdf) |
| The route to a B licence | Permit, eligibility, supervised practice, risk training, test readiness and automatic-transmission conditions | [Transportstyrelsen B guide](https://www.transportstyrelsen.se/sv/vagtrafik/korkort/ta-korkort/valj-behorighet/personbil-och-latt-lastbil/b-personbil-och-latt-lastbil/) |
| Accessible examination preparation | Explain that language options and approved support exist; link to current arrangements | [Test support](https://www.trafikverket.se/korkort/ta-korkort/teoriprov-och-yrkesprov-med-stod/), [languages](https://www.trafikverket.se/korkort/ta-korkort/personbil-och-latt-lastbil/teoriprovet-pa-annat-sprak/) |
| Practical application | Include observation, reversing, turning, hill starts and vehicle checks in theory scenarios | [Practical-test guide](https://www.trafikverket.se/korkort/ta-korkort/personbil-och-latt-lastbil/sa-gar-korprovet-till/) |
| Breakdown and tunnel decisions | Distinguish exposed roads, non-urgent tunnel stops and immediate danger/fire | [Roadside breakdowns](https://www.trafikverket.se/resa-och-trafik/trafiksakerhet/sakerhet-pa-vag/om-du-far-stopp-pa-bilen--varna-lamna-och-larma/), [tunnels](https://www.trafikverket.se/resa-och-trafik/trafiksakerhet/sakerhet-pa-vag/sakerhet-i-vagtunnlar/) |
| Vehicle-dependent advice | Separate general principles from controls, maintenance and energy-saving techniques specific to a car or powertrain | [Syllabus](https://www.transportstyrelsen.se/TSFS/TSFS%202011_20.pdf), [practical-test guide](https://www.trafikverket.se/korkort/ta-korkort/personbil-och-latt-lastbil/sa-gar-korprovet-till/) |
| Local rules and dated information | Teach how national rules interact with signs and local restrictions; attach dates to statistics | [Environmental zones](https://www.transportstyrelsen.se/sv/vagtrafik/miljo/miljozoner/), [road-safety statistics](https://www.transportstyrelsen.se/sv/om-oss/statistik-och-analys/statistik-inom-vagtrafik/olycksstatistik/statistik-over-vagtrafikolyckor/) |

## Updates and issues for the rewrite

These findings are a verification queue for step 3. A “needs verification” item is not a claim that the entire source section is wrong.

| ID | Finding | Required treatment |
|---|---|---|
| V01 | The book predates a change to theory-test validity. [TSFS 2026:47](https://www.transportstyrelsen.se/TSFS/TSFS%202026_47.pdf) takes effect on 19 August 2026; the new validity is one year, with earlier tests subject to transitional rules. | Add the current rule and its applicable date to licensing guidance. Do not apply it retroactively to every test. |
| V02 | [Supervisor guidance](https://www.transportstyrelsen.se/sv/vagtrafik/korkort/ta-korkort/handledarskap-och-ovningskorning/handledare/) states that the introductory-training requirement ended on 1 August 2026. Supervisor approval still applies. | Use current requirements when writing the learner pathway; keep this separate from mandatory risk training. |
| V03 | Book p. 110 advises attempts to move a failed vehicle on the track, including pushing it. Current [railway-crossing guidance](https://www.trafikverket.se/contentassets/e9665c2ef2134eb68306c0c45338f1ef/sakra-plankorsningar.pdf) prioritises evacuating a disabled vehicle, moving away and calling 112 with the crossing ID. | Rewrite this emergency scenario directly from official guidance. Distinguish a moving vehicle trapped by barriers from an immobilised vehicle. |
| V04 | Book p. 179 gives a 50–100 m triangle guideline. Trafikverket's [motorway/2+1 breakdown guidance](https://www.trafikverket.se/resa-och-trafik/trafiksakerhet/sakerhet-pa-vag/om-du-far-stopp-pa-bilen--varna-lamna-och-larma/) recommends at least 100 m, preferably farther, with personal safety precautions. | Use context-specific guidance and separate a recommendation from a statutory requirement. |
| V05 | Book p. 175 contains first-aid instructions involving pulse checks. The sources inventoried here establish the topic but are not a sufficient clinical reference for rewriting that procedure. | Before step 3 finalises first aid, obtain current Swedish emergency/first-aid guidance and verify the sequence. Retain the learning requirement; do not silently omit or repeat the procedure. |
| V06 | Book p. 133 interprets good judgement as sometimes departing from traffic rules. | Replace this broad framing with safe cooperation and verified applicable rules/exceptions. Check merging and yielding examples against the actual provisions. |
| V07 | The book gives fixed visual-field percentages, age-risk multipliers, accident proportions and visibility distances (notably pp. 144, 150, 154, 163, 179–182, 268). | Verify provenance and conditions or teach the underlying safety principle without unsupported precision. Date any retained statistics and distinguish preliminary from final figures. |
| V08 | Child-restraint wording needs to separate legal minimums, recommendations and equipment fit. The two authorities' guidance differs in detail, including recommended rear-facing age and manufacturer qualifications. | Reconcile [Transportstyrelsen](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/trafikregler/i-fordonet/sa-skyddar-du-barnen---regler-och-tips/) with [Trafikverket](https://www.trafikverket.se/resa-och-trafik/trafiksakerhet/sakerhet-pa-vag/sakerhet-i-bil/barn-i-bil/). Do not equate reaching 135 cm with universal optimal safety. |
| V09 | Book pp. 292–293 mention an authority app for ownership/status services. Current [ownership guidance](https://www.transportstyrelsen.se/sv/vagtrafik/fordon/aga-kopa-eller-salja-fordon/agarbyte/) directs private users to Mina sidor and explains restrictions. | Rewrite the workflow from the current service pages, and avoid embedding a soon-stale sequence of interface actions. |
| V10 | Book pp. 204–208 cover winter tyres; the official page includes marking transitions and vehicle/trailer distinctions. | Verify each light-vehicle and trailer rule against [current winter-tyre guidance](https://www.transportstyrelsen.se/vinterdack), including applicable dates. Do not generalise heavy-vehicle rules to B cars. |
| V11 | Maintenance, brake-servo checks, gear/RPM advice and hybrid behaviour are sometimes described universally (pp. 218–227, 272–285, 312–319). | Separate conventional manual-car examples from automatic, electric and hybrid vehicles. Validate procedures and refer to manufacturer instructions where necessary. |
| V12 | Court examples on pp. 362–366 do not provide case identifiers sufficient for independent checking. | Preserve the legal-learning topics. Locate the judgments before presenting them as verified case law, or write fresh hypothetical scenarios supported by current rules. |
| V13 | Detailed exceptions for parking, signals, lane changes, buses, dimensions and overtaking are not all substantiated by the short official overview pages. | During claim validation follow the underlying legal provisions, official brochures and relevant sign descriptions. Source identification is complete at topic level, not at every exception. |
| V14 | Engine-braking assumptions, emissions explanations and optional insurance coverage can be oversimplified. | Explain assumptions and policy/vehicle variation; use the current environment and compulsory-insurance sources. Verify any numerical savings before publication. |

## Road-sign source and asset handoff

The authoritative starting point is [Transportstyrelsen's sign catalogue](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/). Its 19 category pages were inventoried, covering A, B, C, D, E, the two F groups, G, H, I, J, M, P, S, T, SIG, V, X and Y.

- The supplied PDF contains **343 distinct sign/signal codes**, extracted independently from pages 324–357.
- The project's old `book-sign-index.json` contains only **325 codes**: it omits the P, V and Y groups. It must not be treated as complete source coverage.
- The current category listings contain **344 codes**, including **F1-1**. This count does not include every alternative graphic; **F1-2** was separately located on its detail page.
- The project contains **343 existing official sign assets**. All local files match their previously recorded SHA-256 hashes. Their recorded download date is **26 September 2026**; this inventory did not redownload or relicense them individually.
- The existing asset set is missing the F1 direction-sign family. Map book **F1** to official **[F1-1](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-vagvisning/orienteringstavla2/)** and **[F1-2](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/lokaliseringsmarken-for-vagvisning/orienteringstavla2/orienteringstavla2/)**. The old scraper's code matcher excludes hyphens.
- **F31a** appears in the official catalogue and existing assets but not in the supplied PDF. Step 4 should assess its relevance and label it accurately.

Transportstyrelsen's [reuse statement](https://www.transportstyrelsen.se/sv/om-oss/pressrum/pressbilder/) specifically allows its road-sign files to be downloaded and used for different purposes without prior approval, and requests that they be used in their proper context. This is distinct from the page's restrictions on ordinary press photographs. It does not establish reuse permission for the book's photos, bespoke diagrams or publisher branding.

Step 4 should inspect each required detail page and graphic variant, prefer print-suitable official files where available, preserve colours/proportions/orientation, verify English labels independently, and record source URLs and hashes. Flashing, moving and audible signals need explanatory sequences or captions in the PDF; a still frame alone is insufficient. Sign selection and placement remain future work.

## Handoff and completion check

Step 1 is complete as a source and coverage inventory:

- All 367 source pages and all 39 source sections have an inventory entry.
- All five examination domains and the syllabus's self-assessment requirements have source coverage.
- Both requested authorities are represented across rules, licensing, safety, vehicle use and environment.
- Official road-sign categories, reuse guidance and existing-asset gaps are recorded.
- Source dates, retrieval limitations and unresolved factual questions are explicit.

**Next authorised-by-request step:** step 2, draft the original curriculum outline and objectives. Use the coverage IDs to ensure nothing is lost; do not copy the source's chapter order or names by default. Bring the outline back for approval. The manuscript, design preview, finished PDF and app changes have not started.
