# Step 6C · Chapter 2 review

**Completed:** 4 October 2026. **Artifact:** [chapter.pdf](chapter.pdf), 15 pages. **Status:** Chapter screen-review build complete; final publication approval remains in 6N.

## Complete content

The original title, chapter introduction, M02-L01–M02-L04 and M02-R come directly from the unchanged manuscript. All goals, explanations, worked decisions, checks, answers, reminders, self-assessment and reflection instructions are present. The verifier compares 38 lesson/review text blocks plus the introduction. Official reference labels stay alongside the relevant claims as working links. No third-party book name, borrowed page number or generated instructional typography is used.

## Approved illustrations

Six placements use the approved M02-v3 and parking-v3 boards through native PDF clipping, with original files unchanged:

- M02-L01: a person consults the handbook beside the parked car. The illustration establishes preparation context; it is not a literal portrait of the named learner or a universal dashboard diagram. The clipping window preserves the person's head while excluding generated labels.
- M02-L02: direct observation of a stationary trailer's rear lamps. The caption does not imply red lens colour proves electrical operation.
- M02-L03: forward-facing rear bench and empty booster; child and adult stand outside. This approved scene does not teach installation or belt routing. The full text preserves legal minimums, distinct agency recommendations and the actual child/restraint/vehicle compatibility requirement.
- M02-L04: the corrected cabin view shows a driver on the vehicle's left. A separate parking illustration supports the observation scenario: distinct bays, footway, access lane and pedestrian, with no guaranteed camera coverage or safe path drawn. It illustrates the observation principle, not a time sequence of the pedestrian disappearing.
- M02-R: neutral unfamiliar-car, child-passenger and parking sequence before the prompt. Generated diagram labels are excluded; selectable captions describe the geometry. No chosen action is highlighted.

All final crops were visually checked, including seat direction, child presence, left-hand controls, open space and pedestrian context. Captions and embedded ActualText descriptions match the visible artwork; file hashes, clip geometry and effective resolution are saved in [illustrations.json](illustrations.json). The official placement map requires no road signs in M02. No manufacturer-specific dashboard symbols or child-restraint instructions were invented.

## Assessment separation

Lesson questions appear on pages 3, 5, 7 and 9; the module scenario and prompt appear on page 10. Reflection/writing space is on page 11. Answers and the review guide appear on page 12, with at least one intervening page after every question, so they cannot face one another even if the chapter's starting parity changes during assembly. The chapter opener links to the lessons, review, answers and references.

## Source verification

All 11 official reference targets were inspected on 4 October 2026: Trafikverket practical-test/safety pages, Transportstyrelsen rules/advice, the Traffic Regulation and syllabus. The already-cited VTI report is hosted by Transportstyrelsen and supports the limited explanation of shared braking/steering friction. The restraint-height rule, short-journey exceptions, agency rear-facing advice and active-airbag cautions are correctly distinguished. See [dated source checks](source-checks.json). No manuscript changes were needed.

## Render and technical verification

All 15 pages were rendered and inspected. Checked body/caption readability, clipping, scene layout, spacing, response lines and headers/footers. All four fonts are embedded with Unicode mapping; text is selectable and document language is en-GB. All 34 internal links and 16 named destinations resolve; nested bookmarks preserve chapter/lesson structure. External links match the 11 official targets. The build reproduces identical bytes. See [verification.json](verification.json).

## Reproduce

```sh
python3 docs/curriculum/pdf-production/chapters/M02/build_chapter.py
python3 docs/curriculum/pdf-production/chapters/M02/verify_chapter.py
pdftoppm -scale-to 1600 -png docs/curriculum/pdf-production/chapters/M02/chapter.pdf tmp/pdfs/6c/page
```

Use the pinned shared dependencies/fonts from [the build README](../../README.md). `chapter-source.md` is a generated editable snapshot; teaching-text changes belong in the authoritative manuscript, then rebuild. `build_chapter.py` controls composition. The delivery copy is `output/pdf/korkortgo-chapter-02.pdf`.

No chapter-specific blocker remains for screen review. Higher-resolution approved artwork remains necessary for print publication. Captions and ActualText are provided, but complete tagged-PDF/accessibility certification remains in 6N. Global book folios, cross-chapter links (including M07-L02) and final Contents destinations are assembly work in 6M. Step 6D has not started.
