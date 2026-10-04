> **6A update — 4 October 2026:** All current visual previews are approved and the renewed execution request authorises the established design. The opening-page build is complete; see [readiness/render review](pdf-production/readiness-review.md). Historical pending-preview statements below are superseded. Chapter-specific artwork, sign substitution and final release checks remain mandatory.

# KörkortGo PDF design specification

**Version:** 1.0 · **Prepared:** 3 October 2026 · **Step:** 5F.  
**Status:** Consolidated design direction; not cleared for production. See the [completion review](pdf-design-review.md) for approvals and blockers.

## Authority and approved direction

Use the [manuscript](manuscript.md) for all teaching text, the [brand guide](../../design/brand/README.md) and [tokens](../../design/brand/tokens.json) for colour/type values, and the [illustration instructions](../../design/brand/illustration-guide.md) for visual content. Preview images communicate design; they are not text masters, official sign files or a finished PDF.

The user approved cover/opening v4 and the shared brand direction, then navigation v1. On 3 October the user accepted the 5E illustration/page direction and requested 5F. That acceptance does not remove the documented factual corrections or approve illustrations not yet produced. This specification consolidates the existing direction without introducing a new visual treatment. Required visual corrections remain in the review queue and need imagegen previews and approval before implementation.

## Page system

Use A4 portrait (210 × 297 mm), single-page reading and a single main text column. Start with 20 mm margins, allowing 170 × 257 mm of page area including header/footer; reserve approximately 10 mm at the top and bottom for navigation. Maintain separation between running elements and main content. These measurements implement the brief's provisional range and must be tested with real text; they are not measured properties of the imagegen boards.

Use approximately 4 mm spacing within related blocks, 6–8 mm between paragraphs or card groups and 10–12 mm before major sections. Give panels approximately 4–5 mm internal padding. Keep borders fine and corner rounding restrained. Avoid fixed-height text boxes, clipped captions, orphan headings and oversized decorative frames. Continue a lesson or table on another page rather than reducing its type size. Repeat table headers across page breaks.

Keep individual sign/caption units together. Let wide illustrations span the text width when their verified resolution permits. In denser reference pages, use two columns only if each sign's caption and identifying details remain legible. Do not force a fixed number of signs onto every page.

## Typography and colours

Source Serif 4 supplies headings; Source Sans 3 supplies body text, controls, captions and references. These are the chosen reproducible font pairing, not exact identification of fonts in the generated mockups. Before production, pin actual files/versions, preserve licences, verify embedding and inspect Swedish glyphs. Do not use generic platform serif as the final font specification.

| Role | Font / weight | Size / line height |
|---|---|---|
| Cover title starting point | Source Serif 4 / 700 | 40 / 44 pt; adjust to approved cover composition |
| Module title | Source Serif 4 / 700 | 28 / 34 pt |
| Lesson title | Source Serif 4 / 600 | 20 / 26 pt |
| Body | Source Sans 3 / 400 | 12 / 17 pt |
| Caption | Source Sans 3 / 400 | 10 / 14 pt |
| Source note | Source Sans 3 / 400 | 9.5 / 13 pt |

Use Forest `#173E32` for brand/navigation, Paper `#F7F8F3` for the light digital page, Ink `#172C29` for main text and Sage `#E7EEE5` for quiet panels. Navy `#102B46` supports editorial headings and the opening page. Cream `#F5EDDF`, Gold `#A47D3B`, Mist `#C5D7DF` and Sand `#E8DCCB` provide restrained editorial accents. Exact values and app light/dark mappings remain in the shared tokens, not inferred from image pixels.

Use `#495A52` for supporting text on Sage; Muted `#61706B` on Sage fails the normal-text contrast target. Gold rules and pale boundaries are decorative. Never rely on colour alone for requirements, answers or safety meaning. Do not recolour official signs. The book uses the light palette; the documented dark scheme is for app use. A print edition may use white paper, subject to proofing; sRGB hex values are not universal CMYK recipes.

## Template requirements

| Template | Required treatment | Reference |
|---|---|---|
| Cover | KörkortGo title, category B subtitle, learning-aid designation, Swedish road/car illustration | [5B v4](pdf-design/5b/cover-opening-v4.png) |
| Opening guidance | Prominent full disclaimer, short study guidance, navy type and cream/gold panel | [5B review](pdf-design/5b/review.md) |
| Contents | Ten original module titles, appendix/reference destinations and own-book folios | [5C v1](pdf-design/5c/navigation-v1.png) |
| Module opener | Original introduction, four stable lesson IDs and review ID, useful references | [5C review](pdf-design/5c/review.md) |
| Lesson | ID, title, goal, labelled explanation, scenario/illustration, check then separate answer, reminder | [5D boards](pdf-design/5d/review.md), supplemented by [5E scenarios](pdf-design/5e/scenarios-v2.png) |
| Self-assessment | Neutral scenario image/sequence, question and response space before review guidance | [5E M02-R sample](pdf-design/5e/scenarios-v2.png) and [5D reflection](pdf-design/5d/reflection-reference-v1.png) |
| Sign reference | Decision-based RB01–RB24 groups, exact codes, Swedish names, editorial English labels, full checked captions | [5E sign layout](pdf-design/5e/sign-layouts-v1.png) |
| Glossary | Swedish term, meaning and stable lesson reference; repeated headers | [5D companion board](pdf-design/5d/reflection-reference-v1.png) |
| Practice record | All nine manuscript prompts, adequate blank writing space and continuation if needed | [5D companion board](pdf-design/5d/reflection-reference-v1.png) |
| Official references | Identifiable labels, official links, checking dates and artwork credit | Manuscript references and asset/caption records |

The 5D boards are earlier template studies. Their illustrated revision is represented only in part by 5E; do not treat every 5D page or every 5E scene as independently approved production artwork.

## Teaching hierarchy

Keep written labels for Requirements, Official recommendations/advice, Learning approaches, Worked decisions, Knowledge checks, Answers and Reminders. Distinguish official advice from legal duties and original teaching material. Name the authority beside advice. Use a Mist panel with Navy text when recommendation emphasis is needed; this specified variant still needs a representative visual preview before final template approval.

Preserve assumptions and limits beside calculations. Do not portray a response-distance conversion as total stopping distance. Give assessment readers the neutral situation before the question; move solution arrows, highlights and timelines to a separate review panel. Keep the full manuscript text, including exceptions and source citations; do not transcribe condensed generated excerpts as the final lesson.

## Illustrations and assets

Use the [50-section coverage register](pdf-design/5e/illustration-register.md) and its exact anchors. Four sections retain documented text-only treatment; all other required scenes remain tracked even when not yet drawn. Follow the [D01–D08 dispositions](pdf-design/5e/diagram-dispositions.md) and D09–D30 extensions. The [Swedish style sheet](pdf-design/5e/style-reference-sheet.md) establishes vehicle/people/environment direction; it is not a verified technical reference for every detail.

Keep cars, clothing and perspective consistent within each scenario. Show credible Swedish road context, right-hand travel and relevant controls. Refine generated grille emblems and police insignia before final use. Instructional police gestures require their own official meaning check; the neutral appearance study does not approve gestures.

Use only eligible preferred assets from the [sign placement map](sign-placement-map.json), with the associated [captions](sign-captions.json), recorded source links, hashes, reuse status and maximum print dimensions. The smaller [5E bindings](pdf-design/5e/asset-bindings.json) cover preview examples only. No generated sign pixels may substitute for official artwork. F1-2's 300 ppi maximum is 71.9 × 23.6 mm; Y2's is 10.2 × 5.1 mm. Check every other chosen asset's own limit rather than applying a universal size.

The 13 formerly held selected codes now use verified official poster vectors at minimum reviewed widths of 80 or 110 mm; see sign-assets/official-poster/README.md. Keep the four optional mismatched variants excluded. Do not silently remove a selected sign or substitute a similar symbol. The exact parking example remains a text/timeline treatment until its assembly is verified; T6 now has a verified official poster vector; its sample times differ from the learning example, so do not relabel it.

## Navigation and attribution

Give the PDF its own continuous page labels and printed folios, with no visible cover folio if desired. All preview numbers are illustrative. Generate the contents and destinations after final composition. Provide nested bookmarks for modules, lessons, reviews, appendices and references; clickable contents; Contents access on every interior page; and meaningful previous/next labels.

The preview arrows that repeat the current lesson ID must be corrected to actual destinations. After M03-L04, go to M03-R; after the first lesson, go to the second. At boundaries, name the destination rather than an ambiguous arrow. Use stable lesson IDs and sign codes in cross-references; final PDF pages may supplement those identifiers.

Keep official references adjacent to supported claims. The sign catalogue and appendix links must resolve to their intended anchors. Preserve full source URLs and retrieval/checking dates in the reference section; a later design review date is not a new factual-check date. Do not include third-party book titles, chapter labels or source-book page numbers. Keep 1177 limited to the existing brief first-aid passage and reference.

Place the following prominently before the lessons:

> This material is a learning aid to help you understand Swedish driving theory. It is not an official source and cannot replace official information from Trafikverket and Transportstyrelsen. Always consult their current guidance and the applicable rules.

Retain this credit in the sign-reference introduction and final references:

> Road-sign illustrations: Transportstyrelsen. Source links and verification dates are recorded in the official references.

Label English sign names as editorial translations. Do not imply official endorsement.

## Production acceptance requirements

Before step 6, clear the [5F blocker list](pdf-design-review.md), obtain approval of corrected/new visual previews and complete package approval. Step 6 then requires a separate execution request.

During production, use selectable text, logical headings, document language, correct reading order, meaningful links and verified image alternative text. Inspect each rendered page at actual size, ensure text contrast and sufficient writing space, check signs against exact variants, validate bookmarks and every internal/external reference, and recheck time-sensitive manuscript claims. Do not embed approval notes, illustrative folios or placeholder boxes in the learner-facing book. Preserve editable source. Submit the finished PDF for its separate approval before app migration.
