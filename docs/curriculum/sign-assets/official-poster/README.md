# Official sign-vector resolution

**Reviewed:** 3 October 2026. **Result:** All 13 selected asset gaps resolved with exact vector extracts, subject to their recorded presentation sizes. Final book-page proof remains step 6 work.

The official [Transportstyrelsen poster](https://www.transportstyrelsen.se/globalassets/global/publikationer-och-rapporter/vag/vagmarken/ts_poster70x100_2021-10-01_webb.pdf) supplies these outline references. Its vector strokes reproduce more clearly than the earlier individual-file raster renders. No sign was redrawn, recoloured, filled or substituted by AI. The poster is dated October 2021; it supplies artwork, not a new source-check date for every traffic rule. Each caption retains its existing official detail-page and legislation references.

## Verified treatment

- S1, S2, S3, S4, S8, S9, S10 and T6: retain vectors at the reviewed 80 mm width.
- S12, T1, T2, T8 and T22: retain vectors at the reviewed 110 mm width. Use a full-width reference row rather than shrinking to a thumbnail.
- Keep the white background, original outlines, aspect ratio and source credit. These are catalogue reference forms; do not imply they are complete roadside assemblies.
- T8 now uses the poster's truck panel, matching the main official web example. The mismatched wheelchair EPS remains held in the historical downloads.
- S2 and S4 extend to their official frame edges. That feature is present in the poster and was not introduced by extraction.
- Four optional mismatched variants remain excluded: A29-17 and C45-7/8/9.

[Extraction metadata](vector-extraction.json) records source hash, crop boxes and every vector hash. `extract-vectors.py` reproduces the extracts and technical proof from the unchanged poster using pypdf/pdfplumber/reportlab. Run from the repository root with the bundled Python environment. These extracts contain clipped source-page streams: insert them as PDF vector artwork with their crop preserved, not as page text or a whole poster. Actual page use must maintain correct reading order and supplied image alternatives.

## Verification

Rendered and inspected all 13 pages of `vector-legibility-proof.pdf` at 100 dpi, compared the extracted artwork with the labelled official poster, checked no adjacent sign/label enters the crop, and checked all file hashes and downstream captions/placements. This is a screen proof of known physical sizes, not a physical printer test. The six-page earlier `legibility-proof.pdf` using individual EPS raster renders failed the legibility review and is retained solely as diagnostic evidence; do not use it for publication.

[Reuse guidance](https://www.transportstyrelsen.se/sv/om-oss/pressrum/pressbilder/) was rechecked on 3 October 2026: the separate road-sign paragraph permits use for various purposes and asks that the signs retain their proper context. Only sign artwork was extracted; the agency logo and poster layout are not book artwork. Retain the existing Transportstyrelsen artwork credit and exact source URL in the final book.

The package verifier now checks the supplemental official document and 13 derived vectors as well as all 993 original downloads. `sign-verification-checks.json` reports zero selected image blockers. This does not approve new illustration designs or clear 5F's remaining design gates.
