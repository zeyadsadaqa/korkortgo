# Step 6K · Chapter 10 review

**Completed:** 7 October 2026. **Artifact:** [chapter.pdf](chapter.pdf), 23 pages. **Status:** Chapter screen-review build complete; final publication approval remains in 6N.

## Content and evidence

All four lessons M10-L01–M10-L04 and M10-R preserve the approved manuscript. Checks cover 43 lesson/review blocks, the five numbered whole-journey decisions, chapter introduction and exact learning-aid disclaimer. KörkortGo fonts and colours remain consistent. No third-party book name or source pagination appears.

Ten reference targets were checked on 7 October 2026, with same-day legal/syllabus evidence reused where stated in [source-checks.json](source-checks.json). Coverage includes accident duties, breakdown warnings, distinct motorway and tunnel advice, wildlife precautions, category B test content and format, practical tests, languages and support approval. The original 1 October date label for theory-test figures is retained; the current official page confirms the same figures. The 100 m triangle recommendation is agency advice, not a universal legal distance. Wildlife guidance is explicitly distinguished from species-specific statutory reporting duties.

First aid stays within the user's authorised scope: a brief 1177 referral and preparation advice. No clinical procedure, pulse-check sequence or additional medical illustration has been added. Individual road-sign captions and artwork reuse the verified official register; not every sign page was fetched again.

## Approved artwork and native worksheet

Eight native clipping windows retain the approved M10-v4 artwork. A and B are independent images with a clear gutter; the motorway occupants stay entirely in A behind the guardrail. C is on a separate page with the open, lit doorway and unobstructed approach preserved. The protective railing stays on the traffic side. Exact official E28-2 artwork replaces the generated exit sign; its reference is linked. The motorway puncture worked decision appears beside the motorway scene, separate from the fire illustration.

M10-L02 retains the protected caller and a selectable caption carrying the key call information. Four M10-L03 scenes cover the residential street, roundabout, rain and urban traffic. Exact D3 replaces its placeholder, within the asset's recorded size limit. The urban traffic detail is labelled as a companion illustration rather than a depiction of the written rural-bend scenario. The complete original mixed-journey exercise is retained.

M10-L04 remains text-only as approved. M10-R implements the approved Start, Traffic, Conditions, Unexpected stop and Reflection frames as selectable native text with blank writing lines, rather than a raster form. This is a writing worksheet, not an interactive AcroForm.

Both required sign groups LP053–LP054 appear at their manuscript anchors, with ten official reference placements. E26's 2.0 km and E29's 100 m remain sample values, not prescribed emergency distances. Accident warnings do not imply authority for a learner to direct traffic. Each reference retains official Swedish naming, editorial English explanation and an official link. Original artwork files remain unchanged; hashes, crops, captions and dimensions are recorded in [illustrations.json](illustrations.json).

## Verification and navigation

Lesson questions occupy pages 8, 12, 15 and 17. Self-assessment is on page 18, reflection on page 19 and all answers on page 20. At least one intervening page separates every question from its answer. References occupy pages 21–23. There are 30 internal links, 24 named destinations and nested bookmarks.

All 23 rendered pages were visually inspected, including paragraph/list wrapping, sign quality, scenario separation, clear exit access, worksheet writing space and footer clearance. Pages 6–7 were rendered and inspected again after the final caption and worked-decision placement adjustments. [Verification](verification.json) passes manuscript/disclaimer fidelity, embedded Unicode fonts, page bounds, exact official asset and approval hashes, recorded raster-size limits, 21 external reference URLs, navigation targets, answer separation and deterministic rebuilding.

```sh
python3 docs/curriculum/pdf-production/chapters/M10/build_chapter.py
python3 docs/curriculum/pdf-production/chapters/M10/verify_chapter.py
pdftoppm -scale-to 1400 -png docs/curriculum/pdf-production/chapters/M10/chapter.pdf tmp/pdfs/6k/page
```

Use the dependencies in [the build README](../../README.md). `chapter-source.md` is the generated editable snapshot; update authoritative teaching content in the manuscript and rebuild. `build_chapter.py` controls composition. The identical delivery copy is `output/pdf/korkortgo-chapter-10.pdf`.

No chapter-specific screen-review blocker remains. Print-resolution scene masters, full tagged-PDF accessibility, global pagination and cross-chapter navigation remain later release work. This completes all ten individual chapter builds; it does not assemble or approve the finished book and does not start 6L.
