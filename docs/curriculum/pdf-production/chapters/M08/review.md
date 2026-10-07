# Step 6I · Chapter 8 review

**Completed:** 7 October 2026. **Artifact:** [chapter.pdf](chapter.pdf), 29 pages. **Status:** Chapter screen-review build complete; final publication approval remains in 6N.

## Content and evidence

All four lessons M08-L01–M08-L04, the chapter introduction and M08-R preserve the authoritative manuscript. The verifier checks 42 lesson/review blocks, the weight-definition table, introduction and exact learning-aid disclaimer. KörkortGo typography and colours remain. No third-party book name or source pagination appears.

The eighteen chapter reference targets were checked on 5 October 2026, with relevant same-day evidence from Chapters 6–7 reused as recorded in [source-checks.json](source-checks.json). Coverage includes licence entitlement versus technical towing limits, registered versus actual weights, securing and projections, trailer speed conditions, ownership, insurance, inspection and assistance limitations. The manuscript's 1 October legal-version label is retained; the future 1 December amendment is not applied early. Finalisation on 7 October does not claim a new source check on that date. Individual sign captions/artwork reuse the verified register; not every sign page was fetched again.

## Approved illustrations and signs

Four native PDF clipping windows use the approved M08-v2 board without changing the original image. M08-L01 and M08-L02 retain the hypothetical 2,200 + 1,500 kg entitlement example and 400 + 500 kg load example with selectable captions. Goods beside the trailer are explicitly a planning scene, not a secured-load demonstration. M08-L03 remains a text checklist, as approved. The review scene supplies no assumed vehicle specifications or selected answers.

M08-L04 preserves the corrected roadwork layout. Eight visible marker faces use the matching member of the exact official X3-2 asset, clipped and fitted into the illustrated faces in the PDF. The left bands slope down towards the roadway; the right bands slope in the opposite direction. The original paired artwork is neither mirrored nor redrawn. Its Transportstyrelsen description is linked beside the scene.

All three placement groups LP048–LP050 appear at their manuscript anchors, with nineteen reference placements. Weight, dimension, bearing-capacity and trailer-access restrictions remain independent examples. Six vehicle symbols use exact official poster vectors at their reviewed minimum widths; the other thirteen reference assets respect the recorded raster-size limits. Captions retain official Swedish names, editorial English explanations and official links. T5 is distinguished from actual gross weight, C6 from speed limits, and standalone symbols from assembled signs.

[illustrations.json](illustrations.json) records crop geometry, approval hashes, effective scene resolution and asset placements. ActualText and captions support interpretation but do not constitute full tagged-PDF certification.

## Assessment, navigation and verification

Lesson questions are on pages 4, 16, 18 and 21. The chapter review is on page 22, reflection on page 23, and all answers on page 24. Every answer has at least one intervening page after its question. Eighteen chapter references occupy pages 25–29. The PDF has 36 internal links, 30 named destinations and nested bookmarks.

All 29 rendered pages were visually inspected, including table wrapping, official vector outlines, marker directions, scenario crops, answer separation, writing space and footer clearance. The verifier passes manuscript/disclaimer completeness, approved image and official asset hashes, reference dimensions, embedded Unicode fonts, page bounds, internal targets, 38 official external URLs and deterministic rebuilding. See [verification.json](verification.json).

```sh
python3 docs/curriculum/pdf-production/chapters/M08/build_chapter.py
python3 docs/curriculum/pdf-production/chapters/M08/verify_chapter.py
pdftoppm -scale-to 1400 -png docs/curriculum/pdf-production/chapters/M08/chapter.pdf tmp/pdfs/6i/page
```

Use the pinned dependencies/fonts in [the build README](../../README.md). `chapter-source.md` is the editable generated snapshot; edit authoritative teaching text in the manuscript and rebuild. `build_chapter.py` controls composition. The identical delivery copy is `output/pdf/korkortgo-chapter-08.pdf`.

No chapter-specific blocker remains for screen review. Higher-resolution approved scene masters remain necessary for print publication. Global folios/navigation, appendix integration and complete tagged-PDF accessibility remain in 6M–6N. This step does not approve publication or start 6J.
