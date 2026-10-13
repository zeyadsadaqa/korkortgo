# Step 6G · Chapter 6 review

**Completed:** 5 October 2026. **Artifact:** [chapter.pdf](chapter.pdf), 48 pages. **Status:** Chapter screen-review build complete; final publication approval remains in 6N.

## Content and official evidence

The chapter introduction, four lessons M06-L01–M06-L04 and review M06-R preserve the authoritative manuscript. All goals, requirements, learning explanations, worked decisions, questions, reminders, answers and reflection instructions are present. The verifier checks 40 lesson/review blocks plus the introduction and exact learning-aid disclaimer. KörkortGo typography and brand colours remain. No third-party book names or source pagination appear.

All seven chapter reference targets were opened and their relevant passages inspected on 5 October 2026. Checks cover rural observation, meeting and overtaking, motorway/expressway eligibility, joining and exiting, vehicle limits, railway emergencies, roadworks and self-assessment. Current legal provisions are used; the vehicle-limit amendment effective 1 December 2026 is not applied early. Individual sign captions/artwork reuse the verified register with hash and size checks; this does not claim all 76 individual sign pages were fetched again. See [source checks](source-checks.json).

## Approved scenes and assessment coverage

Thirteen native PDF clipping windows use the explicitly approved M06-v1 board without editing its source image. The lesson scenes retain the rural bridge obstruction, hidden bend, separated motorway-entry and exit details, queued traffic beyond the railway and roadworks. Captions distinguish illustrative spacing from measured safe clearances, identify the railway crop as incomplete signage context and avoid presenting the work scene as a verified traffic-management layout. No sign is fabricated or inserted into these scenes.

The four original review details remain. The ordinary rural junction is explicitly distinguished from motorway entry. Three approved lesson crops provide the slower-vehicle, motorway-entry and roadwork companions required by the unchanged written review scenario. They do not include a selected path or the review answer. The railway ID is described with an official reference; no ID number or fictitious sign panel is created.

The [illustration record](illustrations.json) records crop geometry, approval hashes, effective resolution and exact official asset placements. Captions and ActualText support interpretation; they do not constitute full tagged-PDF certification.

## Official reference coverage

All nine required groups LP035–LP043 appear at their manuscript anchors, with 76 placements using 76 distinct official assets. Subheadings distinguish road and animal warnings, overtaking lines, motorway regimes, joining layouts, navigation, railway warnings/countdowns/crossbucks/controls, temporary routes, physical markers and authorised guard instructions. Independent examples are not assembled into an invented road layout.

Exact raster references respect their recorded 300 ppi size limits. Y2 remains a small sound icon at its original permitted size; its readable caption states that it is neither a recording nor a flashing-light instruction. Railway countdowns do not invent fixed metre intervals. Red/yellow diagonal X3 variants remain distinct from the horizontal variant. Official Swedish names, English editorial explanations, credits and links accompany the artwork.

## Assessment separation and navigation

Lesson questions are on pages 12, 17, 25 and 40. The review occupies pages 41–44, followed by reflection on page 45. Answers and review guidance are on page 46. Every question has at least one intervening page before its answer, independent of final chapter parity. The PDF provides 55 internal links, 54 named destinations and nested bookmarks. Official references occupy pages 47–48. The manuscript’s M10-L01 reference remains plain text until the cross-book destination exists in assembly.

## Verification and reproduction

Every page was rendered and inspected for wrapping, sign legibility, scene meaning, caption placement, footer clearance and writing space. A one-paragraph overflow page was removed by keeping the unchanged overtaking learning approach with its illustration. The resulting page was re-rendered and visually inspected; all 47 other page bodies were confirmed pixel-identical to their reviewed renders, excluding changed folio numbers. The verifier passes manuscript/disclaimer completeness, official asset hashes and dimensions, approved scene hashes, embedded Unicode fonts, page bounds, internal targets, 83 official external URLs, answer separation and deterministic rebuilding. See [verification.json](verification.json).

```sh
python3 docs/curriculum/pdf-production/chapters/M06/build_chapter.py
python3 docs/curriculum/pdf-production/chapters/M06/verify_chapter.py
pdftoppm -scale-to 1400 -png docs/curriculum/pdf-production/chapters/M06/chapter.pdf tmp/pdfs/6g/page
```

Use the pinned dependencies/fonts in [the build README](../../README.md). `chapter-source.md` is the generated editable snapshot; change authoritative teaching text in the manuscript and rebuild. `build_chapter.py` controls composition. The identical delivery copy is `output/pdf/korkortgo-chapter-06.pdf`.

No chapter-specific blocker remains for screen review. Higher-resolution approved scene masters remain necessary for print publication. Global folios/navigation, appendix integration and complete tagged-PDF accessibility remain in 6M–6N. This step does not approve publication or start 6H.
