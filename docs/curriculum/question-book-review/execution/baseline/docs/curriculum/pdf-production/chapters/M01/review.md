# Step 6B · Chapter 1 review

**Completed:** 4 October 2026. **Artifact:** [chapter.pdf](chapter.pdf), 15 pages. **Status:** Chapter screen-review build complete; final publication approval remains in 6N.

## Coverage and text fidelity

The unchanged manuscript supplies the original title, introduction, M01-L01–M01-L04 and M01-R. All four goals, explanations, worked decisions, knowledge checks, answers and reminders are included. The review scenario, prompt, review guide and reflection instruction are complete. Automated comparison verifies 40 lesson/review text blocks plus the chapter introduction; only markdown presentation and reference syntax are converted. Source labels remain beside their claims as clickable official links. No third-party book titles, original page references or generated instructional lettering appear.

The chapter opener includes a local contents list and the exact learning-aid disclaimer. Contents links return to this chapter's opener in the standalone PDF. Sixteen named destinations, nested chapter/lesson bookmarks and 34 internal links resolve to actual pages. Final global contents links and folios remain assembly work.

## Illustrations and Swedish context

Four approved scenes are placed using non-destructive PDF clipping, with generated headings excluded and editable text restored:

- M01-L02: tired learner beside a stationary teal car, companion and keys on bench; no medication clearance or diagnosis implied.
- M01-L03: belted occupants, driver on the vehicle's left (viewer right in the facing view); rear road view shows right-hand travel behind a van. The caption explicitly states the scene is not a scale diagram of following distance.
- M01-L04: approved F06-v4 view over the readers' shoulders; the digital tablet faces them. Rain outside provides general planning context, not a literal depiction of the separate forecast-snow example.
- M01-R: neutral sequence of tiredness, time pressure and weather before the question; no solution highlighted.

The approved crops show no identifiable vehicle branding or official sign artwork. M01-L01 remains text-only as specified. The official placement map requires no signs in this chapter; a fabricated learner-practice sign was not added. Captions describe the final crops, and matching ActualText descriptions are embedded around the image placements. Exact source files, hashes, crop windows and effective resolution are in [illustrations.json](illustrations.json).

## Questions and answers

Knowledge checks are on pages 3, 5, 7 and 9. The module scenario/prompt is on page 10, followed by the writing/reflection page 11. All four answers and the module review guide appear on page 12. At least one page intervenes between every question and its answer, so none are on facing pages, including after a change in book-start parity. Worked decisions remain teaching examples; they are not removed from the lessons.

## Official source review

All 11 referenced official URLs were opened and relevant passages checked on 4 October. The key 2026 licensing transitions, supervised practice, risk training, fitness, alcohol/drug rules, care/speed requirements and syllabus objectives support the manuscript. The original 1 October manuscript label is preserved; the new check date is shown in the chapter references and [source record](source-checks.json). No substantive content change was needed. No first-aid detail is introduced in chapter 1.

## Render and technical checks

Rendered and inspected all 15 pages: consistent 12/17 pt body text, embedded Source Sans 3 and Source Serif 4, readable captions and links, full-width scene crops, generous response space, no clipped/overlapping text or missing glyphs. The PDF is selectable, en-GB, and reproducible byte-for-byte with the pinned runtime. All 11 external link targets match the official reference set. Machine results and output checksum are in [verification.json](verification.json).

## Reproduce and scope

```sh
python3 docs/curriculum/pdf-production/chapters/M01/build_chapter.py
python3 docs/curriculum/pdf-production/chapters/M01/verify_chapter.py
pdftoppm -scale-to 1600 -png docs/curriculum/pdf-production/chapters/M01/chapter.pdf tmp/pdfs/6b/page
```

Use the pinned shared dependencies/fonts from [the build README](../../README.md). `chapter-source.md` is the generated editable chapter snapshot; update the authoritative manuscript and rebuild to change teaching text. `build_chapter.py` is the editable composition source. A matching delivery copy is saved under `output/pdf/korkortgo-chapter-01.pdf`.

No blocking chapter issue remains for this screen-review build. Artwork is approximately 103–118 ppi at full text width; higher-resolution approved masters are needed for a print release. ActualText and captions do not constitute full tagged-PDF/PDF-UA certification; full accessibility checks remain in 6N. Final book pagination/navigation are verified in 6M. Step 6C was not started.
