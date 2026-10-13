# PDF design brief — step 5A

**Prepared:** 2 October 2026. **Version:** 1.0.  
**Status:** Brief complete; visual design not yet proposed or approved. **5B is blocked by the 4F sign-package gate.**

## Purpose and audience

Prepare an approachable English-language learning book for learners of ordinary Swedish category B driving. Use the platform name **KörkortGo** as the book title and subtitle **Swedish category B learning guide**, based on the manuscript. The book should help readers understand, explain and practise decisions; it must not resemble an official publication or promise examination success.

Support sequential study, quick return to a lesson, and comparison of road signs. Readers may be unfamiliar with Swedish terminology, so retain official Swedish sign names alongside editorial English labels. Avoid assuming fluent legal English or prior driving experience.

This brief defines requirements and provisional production choices, not approved visual designs. Visual proposals begin with imagegen in 5B; each preview requires explicit approval before the next substep. No PDF implementation starts before complete design approval and a separate step 6 request.

## Inputs and authority

| Saved input | Use |
|---|---|
| [Implementation plan](implementation-plan.md) | Scope, sequence and approval gates |
| [Manuscript](manuscript.md) | Original title, 10 modules, 40 lessons, 10 reflections, appendices and references |
| [Approved outline](curriculum-outline.md) | Curriculum order and objectives |
| [Manuscript verification](manuscript-verification.md) and [evidence register](manuscript-evidence.md) | Claim support, limitations and release checks |
| [Sign selection](sign-selection.md) and [source register](sign-sources.json) | Required sign identities and official provenance |
| [Asset manifest](sign-asset-manifest.json) and [captions](sign-captions.json) | Exact eligible artwork, alternative text, caption text and maximum print sizes |
| [Placement map](sign-placement-map.json) and [readable map](sign-placement-map.md) | 54 lesson placements, 24 reference groups and eight contextual diagram briefs |
| [Reuse record](sign-reuse.md) and [4F verification](sign-verification.md) | Recorded reuse evidence and outstanding holds |

Use factual content from the saved, officially supported manuscript and caption records. This planning step performs no new legal review or remote-source verification. Before release, step 6 must recheck dated requirements. Internal background reading is not a learner-facing source; do not carry over its titles, chapter structure or page references.

## Page format and reading requirements

Propose **A4 portrait, 210 × 297 mm**, for a single PDF suitable for ordinary printing and desktop/tablet reading. Treat phone use as zoomed reading; do not compress the book to fit a phone screen. Use single pages rather than requiring facing spreads to understand a lesson. Do not set a fixed total page count before composition.

Provisional targets for the previews and later specification:

- One main text column, with approximately 18–20 mm margins; increase the inner margin if a bound edition is later required.
- Body text approximately 11.5–12 pt with 1.35–1.5 line spacing. Aim for 55–80 characters per line and avoid shrinking text to force a lesson onto one page.
- Source notes approximately 9.5–10 pt; captions and instructional labels should remain comfortably readable at actual A4 size.
- Clear levels for book title, module, lesson, section label, caption and source note. Keep headings with following text and avoid splitting short worked examples or sign-caption units unnecessarily.
- A restrained palette with ample light background, dark body text and limited accents. Preserve official sign colours. Colour must never be the sole indicator of meaning.
- Select fonts with Swedish characters and appropriate PDF embedding permissions during design specification. No font family or colour palette is approved by this brief.

These are editorial targets to test, not claims of measured accessibility or a finished layout.

## Page templates and hierarchy

| Template | Required content and behaviour |
|---|---|
| Cover | Original title, category B scope, restrained learning-aid identity; no agency crest, logo or endorsement styling |
| Opening guidance | Prominent full disclaimer, intended audience, how to study, content categories and dated-source explanation |
| Contents | All 10 modules; lesson-level navigation through linked contents or a secondary detailed listing; appendices and official references |
| Module opener | Original module title, short introduction and lesson overview; preserve the curriculum sequence |
| Lesson | Stable lesson ID and title, goal, explanation, worked decision, knowledge check, answer and reminder |
| Module reflection | Existing review prompts with room to write or think; no invented exam score or pass prediction |
| Sign reference | Decision-based RB01–RB24 grouping, exact code, Swedish name, editorial English label, verified artwork, caption and source connection |
| Checklist/glossary/practice record | Readable list or table, repeated table headers when needed, suitable writing space for the existing practice record |
| Official references | Clickable official links, identifiable reference labels, source-check dates and illustration credit |

Distinguish **Requirements**, **Official recommendations/advice**, and **Learning approaches / worked decisions** with written labels and consistent treatment. Do not make editorial advice look like legislation. Keep answers in a separately labelled block after each knowledge check, preserving manuscript order while visually encouraging the reader to attempt the question first.

## Navigation and references

Preserve all stable IDs such as M03-L01 and M04-R. Use the PDF's own continuous page numbering, matching PDF page labels to printed folios; the cover may suppress its visible folio. Preview folios are illustrative and must not be treated as final references. Running headings should show module context and the current lesson when useful.

In step 6, provide clickable contents, nested bookmarks, links to references and sign entries, and return links where helpful. Cross-references should identify lessons or sign codes as well as any final page number. Keep one primary reference entry per selected sign, with cross-references for repeats and a code/family lookup. Do not duplicate entries simply to fill a page.

Retain traceable official references beside factual passages through readable reference labels; put full URLs and recorded checking dates in the official-references section. Preserve the distinction between original source retrieval dates and later editorial review dates. Sources remain Trafikverket, Transportstyrelsen and the manuscript's primary-legislation references; keep 1177 limited to the existing brief first-aid passage and link. Do not expand it into a clinical chapter.

## Required disclaimer and credit locations

Place this full text prominently on the opening guidance page, before the substantive lessons:

> This material is a learning aid to help you understand Swedish driving theory. It is not an official source and cannot replace official information from Trafikverket and Transportstyrelsen. Always consult their current guidance and the applicable rules.

The cover should include a short learning-aid designation. The reference section should repeat the need to consult current official guidance and identify English sign labels as editorial translations.

Retain this project credit in the sign-reference introduction and the final references:

> Road-sign illustrations: Transportstyrelsen. Source links and verification dates are recorded in the official references.

Follow the recorded reuse evidence and any asset-specific conditions. Credit is not an endorsement. Do not introduce third-party book names or source-book page numbers.

## Accessibility and illustration constraints

Design for selectable text, logical heading structure and reading order, meaningful link labels, tagged illustrations with the verified alternative text, and a document language of English with Swedish terms identified where supported. Target at least 4.5:1 contrast for normal editorial text and 3:1 for large editorial text; check actual colours during production. Do not recolour official artwork to meet an editorial palette. Verify grayscale usability without treating grayscale sign reproduction as equivalent to colour learning.

Use only an eligible bound preferred asset from the placement map. Preserve aspect ratio and meaningful borders, arrows and symbols. Use the recorded 300 ppi maximum dimensions for saved raster/render files; if an image needs more space, obtain and verify an appropriate official file or conversion rather than upscale it. Do not assume an EPS is usable merely because it is vector artwork. T12's preferred web image remains deliberate; F1-2, F8-2 and Y2 have raster-only limits. Y2 is a static sound icon, not an audio demonstration.

Keep labels and captions beside their images and distinguish comparison sets from actual roadside assemblies. Generated sign imagery in future imagegen previews is only a layout placeholder; the final PDF must use verified official files. Each contextual diagram needs its own content review and explicit preview approval. Step 6 must inspect actual-size rendered pages, small sign details, selectable text, links, reading order and alternative text; no accessibility certification is implied here.

## Representative preview content

These choices test different content demands without changing the manuscript. Use exact excerpts from the named sections when preparing each preview; record any shortened preview excerpt and never transfer generated text into the manuscript unchecked.

| Substep | Content to preview | What it tests |
|---|---|---|
| 5B | Working cover; opening disclaimer and “How to use the book” | Identity, typography direction and prominent non-official status |
| 5C | Contents; module 3 “Read the road before acting”; navigation to Appendix B and official references | Long titles, lesson IDs, hierarchy, bookmarks/links and illustrative folios |
| 5D | M01-L01 “Your route into driving” | Dense requirements, dated guidance and multiple sources |
| 5D | M03-L04 “Leave room to respond” | Worked explanation and numerical example treatment |
| 5D | M04-L01 “Decide who goes first” and M04-R | Rule/advice distinctions, illustration area, answered check and reflection |
| 5D | Appendix C glossary and Appendix D practice record samples | Bilingual terms, tables and writing space |
| 5E | M03-L01 placements LP001–LP002; RB02 | Separate sign functions; yield/stop and marking comparisons |
| 5E | RB06 and M03-L02 “Combine the instructions” | Related plates and vehicle symbols; blocked assets must be resolved first |
| 5E | RB07 and RB19 | Wide direction signs, raster size limits and text equivalents for sound/motion |
| 5E | M05-L03 “Choose a lawful place to stop” | Exact parking context and D06 restrictions |

In 5E address every saved diagram brief: D01 priority/stop; D02 crossing versus passage; D03 parking distances/bus stop; D04 lane changes/joining; D05 roundabout; D06 exact parking times; D07 reversing observation; D08 tunnel emergency. Use the original placement-map briefs for exact content. Record each as approved, requiring revision or explicitly deferred; a design preview alone does not establish factual correctness.

The exact two-hour, black unbracketed 09–18 parking example remains text until its assembly is properly resolved. Do not substitute the 8–17 T17 artwork or E30's different duration. Railway crossing-ID close-ups and non-sign equipment illustrations remain text-only under the existing decisions; do not invent identifiers or silently add unsourced graphics.

## Readiness checklist and handoff

| Check | Status on 2 October 2026 | Required action |
|---|---|---|
| Curriculum and representative text | Ready for design briefing | Preserve approved outline and original manuscript; separate manuscript approval remains unrecorded |
| Page format, hierarchy, navigation and accessibility goals | Defined provisionally | Test through 5B–5F previews and record explicit approvals |
| Disclaimer, source notes and credits | Locations and exact disclaimer defined | Preserve visibly in previews and final PDF |
| Required sign package | **Blocked: 13 selected images** | Resolve S1, S2, S3, S4, S8, S9, S10, S12, T1, T2, T6, T8 and T22; refresh dependent records and rerun 4F |
| Optional held variants | Excluded | Keep A29-17 and C45-7/8/9 excluded unless independently resolved |
| Sign captions/placements | Available with explicit holds | Preserve exact bindings and print limits; no placeholder counts as resolution |
| Contextual diagrams | Briefs only | Preview and review individually in 5E |
| Design approvals | None recorded | Obtain explicit approval at each preview checkpoint; revisions need renewed approval |
| Final PDF and release checks | Future step 6 | Implement only after approved complete design and a separate request |

**5A completion:** The brief and readiness checklist are complete. No images, visual previews or PDF layouts were generated, and no sign holds were cleared. The authorised work was requirements preparation. As specified in 5A, resolve the required sign blockers and rerun 4F before starting 5B; this is an existing plan dependency, not a new approval request.


**Sequencing update — 2 October 2026:** Following the 5A blocker notice, the user directly requested execution of 5B. A limited cover/opening-page preview without sign artwork was prepared under that instruction and is [awaiting approval](pdf-design/5b/review.md). The 13 required sign gaps and 4F completion gate remain unresolved; this exception does not clear sign-dependent layouts or final PDF production.

## Brand direction update — 2 October 2026

The user specified [learn-and-prepare](../../design/mockups/01-learn-and-prepare.png) and [practise-and-review](../../design/mockups/02-practise-and-review.png) as the visual identity references. Follow their deep forest green, pale sage, off-white surfaces, fine borders, editorial serif headings and clean supporting type. Use the current name **KörkortGo**, not the older name visible in those references. Use the mockups for visual style only; do not import their source-book citations, page labels, statistics or other text. Replace the abstract cover with a recognisable car/road scene in a Swedish landscape. [5B version 3](pdf-design/5b/review.md) presents that direction for approval; exact fonts and colour tokens remain to be specified.

**Opening-page palette revision — 2 October 2026:** The user requested the first draft colours for the opening page while retaining the driving cover. Use navy typography, warm ivory, a cream/gold disclaimer panel and muted blue/sage/sand icon accents for this page. This specific preference supersedes the uniform green opening-page treatment. See [version 4](pdf-design/5b/review.md); approval remains pending.

## Shared design guide — 2 October 2026

Use the [KörkortGo design guide](../../design/brand/README.md), [colour/type tokens](../../design/brand/tokens.json) and [Material role mappings](../../design/brand/material-roles.md) for future previews. The user accepted documenting this shared direction. Source Serif 4 and Source Sans 3 are the chosen reproducible font pairing, not identified original raster fonts. Retain the driving cover and opening-page editorial palette. Individual layout approvals remain separate; this does not start 5C.

## Illustration requirement — 2 October 2026

The user requires illustrations within lessons and self-assessment, especially scenarios and signs, with consistent Swedish cars, police, roads and people. Apply the [illustration instructions](../../design/brand/illustration-guide.md) before producing the illustrated book. Audit all lessons/reviews, revise representative 5D previews, extend the 5E scene register and obtain explicit visual approval. Existing placeholder-only pages do not constitute the final illustrated treatment. The manuscript already exists; these requirements govern visual development and production without changing its factual content.

## 5E preview handoff — 3 October 2026

The [illustration package](pdf-design/5e/review.md) contains the Swedish style sheet, sign-layout proposals, lesson/self-assessment samples, timeline and full 50-section coverage register. Use its per-scene dispositions and asset bindings for continuation. This is a representative preview package, not a complete approved illustration set.
