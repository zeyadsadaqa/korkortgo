# Step 6J · Chapter 9 review

**Completed:** 7 October 2026. **Artifact:** [chapter.pdf](chapter.pdf), 22 pages. **Status:** Chapter screen-review build complete; publication approval remains in 6N.

## Content and evidence

All four lessons M09-L01–M09-L04 and M09-R preserve the authoritative manuscript, including 37 checked lesson/review blocks, introduction and exact learning-aid disclaimer. The established KörkortGo fonts and palette are retained. No third-party book names or source pagination appear.

All nine chapter reference targets were opened and checked on 7 October 2026. [Source checks](source-checks.json) record environmental measures, anticipatory driving, journey choices, plug-in-hybrid weighting and environmental-zone criteria. Class 3 light-vehicle eligibility follows the exact legal provisions, without extending the separate heavy-vehicle plug-in-hybrid permission. STFS effective-date and amendment lookup is explained without asserting a named city's current boundary. No fixed energy saving is invented. Existing verified sign captions/artwork are reused; not every sign web page was fetched again.

## Approved illustrations and signs

Four native clipping windows retain the approved M09-v2 board. M09-L01 remains deliberately text-only. M09-L02 retains the right-side queue approach and clear crossing; its caption avoids claiming a measured distance. M09-L03 retains the separate and combined schematic journeys, with all route labels transcribed into a selectable caption. The M09-R crop retains the four travel-mode scenes; native blank writing lines replace the preview's errands box.

M09-L04 replaces the reserved placeholder with unchanged official E31-2 class-2 artwork. Visual review caught and corrected an initial class-3 asset/caption mismatch before delivery; the verifier now asserts the class-2 binding. The displayed sign is a recognition example, not a real boundary or permission for the pictured car. Original illustration and sign files are unchanged.

Both required placement groups LP051–LP052 appear at their manuscript anchors: ten official reference assets cover zone starts/ends and charging/parking distinctions. Each reference has the official Swedish name, editorial English caption and official URL. Raster dimensions respect the recorded limits. [Illustrations](illustrations.json) records approval hashes, clips, captions, effective resolution and official placements.

## Assessment and verification

Questions are on pages 3, 6, 9 and 16; self-assessment is on page 17, reflection on page 18 and all answers on page 19. Each answer is separated from its question by at least one intervening page. Official references occupy pages 20–22. Navigation includes 29 internal links and 25 named destinations.

All 22 rendered pages were inspected for clipping, overflow, sign legibility, illustration composition, spacing and footer clearance. The corrected page 15 was rendered and inspected again. [Verification](verification.json) passes manuscript/disclaimer preservation, approved image hashes, exact official asset hashes and sizes, embedded Unicode fonts, page bounds, 19 official external URLs, internal targets, answer separation and deterministic rebuilding.

```sh
python3 docs/curriculum/pdf-production/chapters/M09/build_chapter.py
python3 docs/curriculum/pdf-production/chapters/M09/verify_chapter.py
pdftoppm -scale-to 1400 -png docs/curriculum/pdf-production/chapters/M09/chapter.pdf tmp/pdfs/6j/page
```

Use the dependencies in [the build README](../../README.md). `chapter-source.md` is the generated editable snapshot; revise authoritative teaching content in the manuscript and rebuild. `build_chapter.py` controls composition. The identical delivery copy is `output/pdf/korkortgo-chapter-09.pdf`.

No chapter-specific screen-review blocker remains. Approved high-resolution scene masters remain print-release work. Global folios, final navigation and full tagged-PDF accessibility remain in 6M–6N; ActualText and captions alone do not certify accessibility. This step does not approve publication or start 6K.
