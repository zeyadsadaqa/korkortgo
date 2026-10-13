# Step 6M assembly review

Completed for screen review on 7 October 2026. This is the complete book assembly; final publication verification and approval remain step 6N.

## Composition and navigation

The 498-page book combines the four opening pages, 311 chapter pages and 183 reference pages. Each input page is included once, with the provisional contents replaced in place. All ten chapters, 40 lessons, ten self-assessments and appendices A–D remain present. No blank padding or content reflow was needed: every question retains at least a two-page separation from its answer, so questions and answers do not share a facing spread.

The contents now lists the book’s own final folios. Printed page numbers and PDF page labels agree throughout; the cover has no visible folio. Every interior page provides Contents, Sources and Previous page links, with Next page except on the last page. Nested bookmarks cover chapters, lessons, reviews, answers, chapter sources, appendices and sign groups. Printed lesson IDs and chapter sign codes link to their full-book destinations where applicable. External official links remain usable.

The editable [builder](build_book.py) uses the approved shared styles and verified component PDFs. [Inputs](inputs.json) record hashes, page counts and offsets; [navigation](navigation.json) records 914 destinations and 589 new cross-links. Text-geometry candidates are cached against component hashes and can be regenerated with `--refresh-navigation`.

## Fidelity and verification

[Verification](verification.json) passes with 498 pages, 3,037 valid internal links, 389 distinct external URL targets, four embedded Unicode fonts and deterministic rebuilding. All 1,633 original non-footer links retain their destination or external URL. All preserved source-page text remains present and in its original sequence. Every source file still matches its pre-assembly hash. The output copy and production PDF have identical bytes.

The merge library emitted warnings while remapping direct links in the first build. The final builder instead reconstructs each original body link explicitly using the component offset and original page target. Verification checks every remapped target against its original; the final build produces no such warnings.

All 498 assembled pages and all component pages were rendered at a 1,000-pixel longest edge. Excluding only the replaced footer region, all 497 preserved page bodies match their source render pixel for pixel, including the cover. Page 4 is the newly generated contents. See [render comparison](render-comparison.json).

The new contents was inspected separately at 1,600 pixels. Thirty-one opening, chapter-boundary, appendix/reference and final pages were inspected visually for layout consistency, headers, folios and section transitions. No assembly defects remain. The existing illustrations, exact sign artwork, captions, source dates, credits and learning-aid disclaimer are preserved.

SHA-256: `5007914b3b7f4d18472f283c3cd29efc302a6ab1cd7eb36190ea2984cf1a84b0`.

## Remaining stage

Step 6N still requires the final complete-book factual, publication and accessibility review, including tagged reading order and release approval. The approved illustrations remain at their existing screen-review resolution; this assembly does not claim print-ready masters or accessibility certification. Link target preservation is verified here; it does not claim a new factual review of every official webpage. The 6L availability checks and individual chapter source checks remain the dated evidence until 6N.
