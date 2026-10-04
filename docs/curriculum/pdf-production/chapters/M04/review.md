# Step 6E · Chapter 4 review

**Completed:** 4 October 2026. **Artifact:** [chapter.pdf](chapter.pdf), 42 pages. **Status:** Chapter screen-review build complete; final publication approval remains in 6N.

## Content and sources

The chapter introduction, four lessons M04-L01–M04-L04 and review M04-R preserve the manuscript. All goals, explanations, crossing-duty table, worked decisions, questions, reminders, answers and reflection instructions are present. The verifier checks 38 lesson/review blocks plus the introduction. The chapter retains KörkortGo typography/colours and the learning-aid disclaimer. No third-party book names or source pagination appear.

All seven chapter reference targets were opened and relevant passages inspected on 4 October 2026. They cover right-hand priority, exit and turning duties, merging, pedestrian and cycle crossings, roundabouts and self-assessment. A short acceleration-lane companion explanation cites Traffic Regulation chapter 3 §23. Individual sign captions/artwork reuse the verified register with hash and size checks; this does not claim that all individual sign-description pages were fetched again. See [source checks](source-checks.json).

## Approved illustrations and official signs

Twenty native PDF clipping windows use six approved boards, retaining the original image files. The scenes cover ordinary junctions, exits, priority roads, stops, lane changes, merging, acceleration lanes, turning beside a cyclist, crossing distinctions and roundabout decisions. Separate panels remain separated. The priority-road sign remains after the junction; the right turn and cyclist passage remain open; roundabout approaches retain the approved road geometry.

Nine exact official sign/marking insertions replace generated or reserved faces in the PDF composition. Selectable captions identify the scene's meaning and limits. White reference cards in the crossing comparison identify the depicted control; they are explicitly not fictional roadside sign assemblies. The small priority-road callout is labelled B4 to prevent clipping; the full meaning remains in the caption.

All eight required groups LP015–LP022 are present, with 46 reference placements using 44 distinct official assets. Examples follow their manuscript anchors and retain official Swedish names, editorial English explanations and official links. Pedestrian and vehicle signals have separate headings. Raster signs stay within their recorded 300 ppi size limits. Artwork credit and translation status appear with the references.

The approved M04-R preview contains a single-lane roundabout while the manuscript specifies two lanes. Its entry panel is explicitly labelled as a companion detail. The approved two-lane circulation scene is added on the following page to support the unchanged written scenario, without selecting a route or revealing the answer.

The [illustration record](illustrations.json) records approval hashes, crop geometry, scene resolution and official asset placement details. Captions and ActualText accompany illustrations; these do not constitute full tagged-PDF certification.

## Assessment and navigation

Lesson questions are on pages 11, 21, 29 and 35. Review scenes and prompts occupy pages 36–38, followed by reflection on page 39. All answers and the review guide are on page 40. Each question has at least one intervening page before its answer. The chapter provides contents links, nested bookmarks, 50 internal links and 49 named destinations. Official references occupy pages 41–42.

## Verification and reproduction

All 42 rendered pages were visually inspected for scene meaning, legibility, aspect ratios, table wrapping, caption placement, footer clearance and response space. The clipped B4 callout was corrected and the final page rechecked. The verifier passes content fidelity, approved-image hashes, exact official assets and dimensions, embedded Unicode fonts, page bounds, internal targets, 51 distinct official external URLs, answer separation and deterministic rebuilding. See [verification.json](verification.json).

```sh
python3 docs/curriculum/pdf-production/chapters/M04/build_chapter.py
python3 docs/curriculum/pdf-production/chapters/M04/verify_chapter.py
pdftoppm -scale-to 1600 -png docs/curriculum/pdf-production/chapters/M04/chapter.pdf tmp/pdfs/6e/page
```

Use the pinned dependencies/fonts in [the build README](../../README.md). `chapter-source.md` is the generated editable snapshot; change authoritative teaching text in the manuscript and rebuild. `build_chapter.py` controls composition. The identical delivery copy is `output/pdf/korkortgo-chapter-04.pdf`.

No chapter-specific blocker remains for screen review. Higher-resolution approved scene masters remain necessary for print publication. Final global folios/navigation, appendix integration and complete tagged-PDF accessibility remain in 6M–6N. This step does not approve publication or start 6F.
