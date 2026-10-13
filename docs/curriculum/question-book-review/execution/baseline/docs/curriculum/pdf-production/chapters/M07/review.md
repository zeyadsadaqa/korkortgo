# Step 6H · Chapter 7 review

**Completed:** 5 October 2026. **Artifact:** [chapter.pdf](chapter.pdf), 23 pages. **Status:** Chapter screen-review build complete; final publication approval remains in 6N.

## Content and official evidence

The chapter introduction, all four lessons M07-L01–M07-L04 and review M07-R preserve the authoritative manuscript. Goals, requirements, explanations, worked decisions, questions, reminders, answers and reflection are included. The verifier checks 39 lesson/review blocks plus the introduction and exact learning-aid disclaimer. KörkortGo typography and colours remain. No third-party book names or source pagination appear.

All ten chapter reference targets were opened and relevant passages inspected on 5 October 2026, covering visibility and lighting, friction and ABS limitations, ordinary light-vehicle tyre requirements, communication equipment, fatigue and journey planning. The original manuscript's 1 October tyre-check date remains unchanged; those claims were rechecked on 5 October. Individual sign captions/artwork reuse the verified register with hash and size checks; this does not claim all individual sign pages were fetched again. See [source checks](source-checks.json).

## Approved illustrations

Eight native PDF clipping windows use the explicitly approved M07-v1 board without editing the source image. Four lesson scenes show rain/darkness, changing grip before a winter bend, a parked left-hand-seat driver and indoor replanning. Four neutral review scenes retain departure, rain, darkness and delay in sequence. Selectable captions replace the preview's raster labels, and writing space contains no selected response or answer.

The lighting scene does not claim to identify a particular lamp mode or stopping distance. Surface appearance is not treated as a friction measurement or tyre guarantee. The attention scene is explicitly a stopped discussion in a parking area, not permission for distracting equipment use while driving. The clock does not imply a prescribed rest interval. Indoor planning remains a companion illustration to the manuscript's en-route worked decision.

The [illustration record](illustrations.json) records crop geometry, approval hashes, effective scene resolution and exact official asset placements. Captions and ActualText support interpretation; they do not constitute full tagged-PDF certification.

## Official sign coverage

All four placement groups LP044–LP047 appear at their manuscript anchors, with six exact official assets: A24, A24-2, A10, A11, C44 and H13. Crosswinds remain a separately labelled changing-condition reference, not a fog or lighting instruction. Slippery-road and loose-chippings warnings retain their separate meanings. C44 preserves the class II moped qualification and distinguishes local restrictions from seasonal studded-tyre permission. H13 supplies a rest-area destination without certifying fitness to continue.

All raster assets respect their recorded 300 ppi size limits. Official Swedish names, English editorial explanations, Transportstyrelsen credits and official description links accompany them. No official sign is fabricated or redrawn.

## Assessment separation and navigation

Lesson questions are on pages 5, 9, 13 and 16. Review scenes occupy pages 17–18, followed by reflection on page 19. Answers and review guidance are on page 20. Every question has at least one intervening page before its answer, independent of final chapter parity. The PDF provides 30 internal links, 27 named destinations and nested bookmarks. Ten official references occupy pages 21–23.

## Verification and reproduction

All pages were rendered and inspected for wrapping, scene meaning, sign legibility, caption placement, writing space and footer clearance. A one-paragraph overflow page was removed by keeping the unchanged grip learning approach with its illustration. The resulting page was re-rendered and inspected; other page bodies were compared against the reviewed renders, excluding changed folios. The verifier passes manuscript/disclaimer completeness, approved scene and official asset hashes, asset dimensions, embedded Unicode fonts, page bounds, internal targets, 16 official external URLs, answer separation and deterministic rebuilding. See [verification.json](verification.json).

```sh
python3 docs/curriculum/pdf-production/chapters/M07/build_chapter.py
python3 docs/curriculum/pdf-production/chapters/M07/verify_chapter.py
pdftoppm -scale-to 1400 -png docs/curriculum/pdf-production/chapters/M07/chapter.pdf tmp/pdfs/6h/page
```

Use the pinned dependencies/fonts in [the build README](../../README.md). `chapter-source.md` is the generated editable snapshot; change authoritative teaching text in the manuscript and rebuild. `build_chapter.py` controls composition. The identical delivery copy is `output/pdf/korkortgo-chapter-07.pdf`.

No chapter-specific blocker remains for screen review. Higher-resolution approved scene masters remain necessary for print publication. Global folios/navigation, appendix integration and complete tagged-PDF accessibility remain in 6M–6N. This step does not approve publication or start 6I.
