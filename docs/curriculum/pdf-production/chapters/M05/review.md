# Step 6F · Chapter 5 review

**Completed:** 5 October 2026. **Artifact:** [chapter.pdf](chapter.pdf), 44 pages. **Status:** Chapter screen-review build complete; final publication approval remains in 6N.

## Content and official evidence

The chapter introduction, four lessons M05-L01–M05-L04 and review M05-R preserve the authoritative manuscript. All goals, requirements, explanations, the eight-row stopping/parking table, worked decisions, questions, reminders, answers and reflection instructions are present. The verifier checks 42 lesson/review blocks plus the introduction. The required learning-aid disclaimer, KörkortGo typography and brand colours remain. No third-party book names or source pagination appear.

Seven chapter reference targets were opened and their relevant passages inspected on 5 October 2026. Checks cover consideration for road users, horses, bus departures, special-street access and speed, stopping versus parking, distance restrictions, parking-disc/time conditions, permit limits, reversing and self-assessment. Official T6 and T18 descriptions were also checked for the illustrative parking-time assembly. Other individual captions/artwork reuse the verified register with hash and size checks; this does not claim every individual sign page was fetched again. See [source checks](source-checks.json).

## Approved scenes and diagrams

Nine native PDF clipping windows use M05-v2, D03-v1 and parking-v3 without editing the original images. The bus retains the approved full-width middle lane, separately from opposing traffic. Its raster 50 km/h caption is excluded; the typeset caption follows the manuscript's 40 km/h worked decision. Both values are within the rule's threshold, but the lesson presents one consistent example.

The pedestrian-street illustration uses exact official E7 artwork in its reserved reference area. The D03 bus-stop face uses exact E22. The three restriction scenes preserve the original arrows and geometry; selectable 9.5 pt labels identify the crossing's 10 m approach, the junction's two 10 m extents, and the bus stop's 20 m/5 m extent. Captions state direction of travel, schematic scope and that shading is explanatory, not a road marking. The small E22 scene symbol has larger reference examples in the chapter. The parking/reversing scene preserves the separate bays, rear footway and access lane, without a solution path. Review scenes retain neutral bus, cyclist/open-door and crossing details.

The approved timeline-v4 design is reproduced with selectable type and native PDF shapes, not generated page text. Both exercise and worked answer use the identical official E19 sign with one explicitly illustrative white plate containing black `2 tim` and `9–18`. The archived T6 artwork is not relabelled. No parking-disc or fee condition is added. The exercise has no timeline or 12:00 answer. The worked review retains the not-to-scale label, 09:00/10:00/12:00/18:00 ticks, two-hour bracket and 12:00 result.

The [illustration record](illustrations.json) records crop geometry, approval hashes, effective scene resolution, native parking conditions and official asset placements. Captions and ActualText support image interpretation; these do not constitute full tagged-PDF certification.

## Official sign coverage

All 12 groups LP023–LP034 are included at their manuscript anchors, including the groups after worked decisions. There are 62 reference placements using 57 distinct official assets, plus two scene insertions and two E19 placements in the parking-time example. Independent conditions remain labelled examples, not an invented combined instruction. Matched starts/ends, access prohibitions, paths, reserved lanes and parking configurations have distinguishing headings and captions.

T6 and T8 retain the exact official poster vectors at their reviewed minimum widths of 80 mm and 110 mm, including their original outline treatment and sample content. Only unused font-selection/resources are removed from the in-memory placements after checking that they contain no text-painting or external-object operations. Original asset files remain unchanged. Raster reference examples respect recorded 300 ppi size limits. Captions retain official Swedish names, editorial English explanations and links to official descriptions. Credits include the official poster.

## Assessment separation and navigation

Lesson questions are on pages 7, 17, 33 and 37. The parking-time exercise is on page 32; its worked answer is on page 42. The module review occupies pages 38–39, followed by reflection on page 40. Lesson answers and the review guide are on page 41. Every question has at least one intervening page before its answer, independent of chapter parity in final assembly. The PDF provides 52 internal links, 53 named destinations and nested bookmarks, including an exercise-to-worked-answer link. Official references occupy pages 43–44.

## Verification and reproduction

All 44 pages were rendered and visually inspected for text/table wrapping, sign legibility, scene meaning, geometry, caption placement, footer clearance and writing space. Distance labels were enlarged to the source-note size and residual raster lettering covered. Changed pages were re-rendered and inspected; other pages were confirmed pixel-identical to the reviewed render. The verifier passes manuscript completeness, disclaimer fidelity, official asset hashes/dimensions, approved scene hashes, embedded Unicode fonts, page bounds, internal targets, 65 official external URLs, answer separation and deterministic rebuilding. See [verification.json](verification.json).

```sh
python3 docs/curriculum/pdf-production/chapters/M05/build_chapter.py
python3 docs/curriculum/pdf-production/chapters/M05/verify_chapter.py
pdftoppm -scale-to 1600 -png docs/curriculum/pdf-production/chapters/M05/chapter.pdf tmp/pdfs/6f/page
```

Use the pinned dependencies/fonts in [the build README](../../README.md). `chapter-source.md` is the generated editable snapshot; change authoritative teaching text in the manuscript and rebuild. `build_chapter.py` controls composition. The identical delivery copy is `output/pdf/korkortgo-chapter-05.pdf`.

No chapter-specific blocker remains for screen review. Higher-resolution approved scene masters remain necessary for print publication. Global folios/navigation, appendix integration and complete tagged-PDF accessibility remain in 6M–6N. This step does not approve publication or start 6G.
