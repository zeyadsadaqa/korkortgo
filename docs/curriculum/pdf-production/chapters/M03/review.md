# Step 6D · Chapter 3 review

**Completed:** 4 October 2026. **Artifact:** [chapter.pdf](chapter.pdf), 50 pages. **Status:** Chapter screen-review build complete; final publication approval remains in 6N.

## Complete content

The chapter introduction, four lessons M03-L01–M03-L04 and review M03-R come directly from the unchanged manuscript. All goals, explanations, the five-family table, worked decisions, questions, reminders, answers and reflection instructions are present. The verifier checks 42 lesson/review blocks plus the introduction. Official references remain linked beside the relevant statements. The chapter retains the required learning-aid disclaimer and KörkortGo typography/colours. No third-party book names, source pagination or generated instructional text appear.

## Illustrations and official signs

Seven native PDF clipping windows use the approved M03-v4 board without changing the original image. They cover the narrow bridge, green-signal queue, early lane choice, continuing after a missed turn, response space and two separate self-assessment scenes. Captions explain illustrative scope and avoid presenting the images as measured road geometry. The approved separation of opposing traffic and stop lines before the junction remain visible. Generated labels and the empty official-sign placeholder are excluded.

All 14 required placement groups are covered. LP001–LP013 contain 100 exact official asset placements (96 distinct assets); LP014 links back to the F1-1, SIG3 and T11 examples. Groups follow their manuscript anchors. Independent examples are clearly labelled, not assembled into fictional roadside instructions. Lane-control and public-transport signals are separately headed. Flashing amber is explicitly outside the ordinary cycle. Paired-line captions identify the driver's side. The self-assessment does not combine unrelated official examples into a purported verified junction.

Ten placements use the exact official-poster vector extracts, including the repeated S8. They retain their reviewed 80 or 110 mm minimum width, aspect ratio, white background and outline treatment. These unusually large examples account for part of the chapter length. Unused font-selection operators and font resources are removed only from the in-memory vector placement after asserting there is no text-painting or external-object operation; the original official asset files stay unchanged. Raster official signs remain within recorded 300 ppi size limits. Each example includes its official Swedish name, editorial English explanation and a link to Transportstyrelsen. Artwork credit and translation status appear with the references.

The [illustration record](illustrations.json) records image hashes, crop geometry, effective scene resolution and every official placement's page, dimensions and source hash. Selectable captions and ActualText descriptions accompany images; these do not constitute full tagged-PDF certification.

## Assessment separation

The lesson questions are on pages 9, 26, 36 and 45. The module scenario and prompt are on page 46, followed by a full reflection/writing page. All answers and the review guide are on page 48. Every question therefore has an intervening page before its answer, regardless of chapter parity during assembly. Contents links, named destinations and nested bookmarks support navigation.

## Sources and verification

The seven chapter reference targets were opened and relevant passages inspected on 4 October 2026. They support the instruction hierarchy, amber exception, lane restrictions, safe speed/defaults, response/braking distinction and self-assessment. The existing individual sign-caption register was reused with exact asset/hash checks; this does not claim that all 96 individual sign-description pages were fetched again. See [source checks](source-checks.json).

All 50 pages were rendered and visually inspected. The family-table column width was increased to avoid splitting the restriction label, the public-transport heading was kept with its first example, and vector backgrounds were made white. Checked scene meaning, legibility, image aspect ratios, clipped artwork, text spacing, footer clearance and response lines. The verifier checks content completeness, asset eligibility and dimensions, font embedding/Unicode mapping, page bounds, working internal targets, official external links, assessment separation and deterministic rebuilds. See [verification.json](verification.json).

## Reproduce and remaining release work

```sh
python3 docs/curriculum/pdf-production/chapters/M03/build_chapter.py
python3 docs/curriculum/pdf-production/chapters/M03/verify_chapter.py
pdftoppm -scale-to 1600 -png docs/curriculum/pdf-production/chapters/M03/chapter.pdf tmp/pdfs/6d/page
```

Use the pinned shared dependencies/fonts in [the build README](../../README.md). `chapter-source.md` is the generated editable snapshot; change authoritative teaching text in the manuscript and rebuild. `build_chapter.py` controls composition. The identical delivery copy is `output/pdf/korkortgo-chapter-03.pdf`.

No chapter-specific blocker remains for screen review. Higher-resolution approved scene masters remain necessary for print publication. Final global folios/navigation, appendix integration and complete tagged-PDF accessibility are later assembly/release work in 6M–6N. This step does not approve publication or start 6E.
