# Official sign asset package — step 4C

**3 October 2026 update:** The 13 required page-image holds are resolved by [exact official poster vectors](official-poster/README.md), with 80/110 mm minimum reviewed widths. There are now 494 eligible page candidates and four excluded optional variants. Original downloads and their earlier quality findings remain unchanged. The remainder of this document records the original 4C inspection.

**Collected and checked:** 1 October 2026. **Status:** Collection and quality review completed, with 17 page candidates held from layout use.

## Contents

- `originals/`: 498 original web images and 495 original EPS files, downloaded without altering their bytes.
- `rendered/`: 495 PNGs rendered from official EPS files at 300 ppi. These are technical format conversions, not redrawn signs.
- `proofs/`: 11 web-image contact sheets, 11 EPS-render contact sheets, a contrast check and focused variant comparisons. These are inspection evidence, not PDF design proposals.
- [Asset manifest](../sign-asset-manifest.json): URLs, source-page IDs, parent selections, local paths, SHA-256 hashes, dimensions, transparency, EPS bounding boxes, render results, quality holds and preferred layout candidates.
- [Validation results](../sign-asset-checks.json): integrity and relationship checks for the final package.
- [Reuse record](../sign-reuse.md): official permission evidence and its limits.

The original downloads total **392,448,369 bytes** (about 392 MB); generated renders and proof sheets are additional. CAD files were not collected because the task requires teaching and PDF artwork, not engineering drawings.

## What passed

All 993 downloads succeeded. All 498 raster images decoded, including every frame; each has one frame. All 495 EPS files passed header, positive bounding-box and container-range checks, and rendered successfully using Ghostscript 10.08.0. Every original and render has a checksum. All source references resolve to the 4B register.

All 498 web images and 495 rendered counterparts were inspected in contact sheets; selected faint images and discrepancies were inspected in focused proofs. **481 source-page candidates** have an image recommended for later layout within recorded limits; **17 remain held**. This is not final caption approval or a certification of the rendered PDF.

## Holds and exceptions

| Finding | Affected items | Treatment |
|---|---|---|
| Faint or outline-only artwork at teaching scale | S1, S2, S3, S4, S8, S9, S10, S12, T1, T2, T6, T8, T22 | Originals and EPS renders retained; no preferred layout image. Other checked T8 variants may illustrate particular vehicle groups, but must not silently replace generic S/T definitions. |
| Web/EPS content differs | T8, C45-7, C45-8, C45-9, A29-17 | Hold both files for these page variants pending resolution. Do not trust extension or filename as proof of matching artwork. |
| Identical web-image bytes | C45-6 and C45-7 | Recorded as an official-source duplicate. C45-7 is held; C45-6 has a matching EPS rendition. |
| No linked EPS | F1-2, F8-2, Y2 | Retain original raster with its size limit. F1-2 is 849×279 px (71.9×23.6 mm at 300 ppi); F8-2 is 1111×175 px (94.1×14.8 mm). |
| Sound cannot be shown by the asset | Y2 | The 120×60 px GIF is a single-frame speaker icon, not an animation or audio sample. At 300 ppi its limit is 10.2×5.1 mm; explanation is required. |
| Excess canvas or colour/outline differences in some EPS files | Individual records in Q05 of the manifest | Prefer the intact web image within its recorded limit. No artwork was cropped or recoloured to force a match. |

The 17 held candidates are the union of the first two rows, with T8 counted once. These holds prevent step 4F from declaring the entire illustration package ready until the required examples are resolved or explicitly revised.

The detailed comparison found that the T8 EPS depicts a wheelchair symbol while the web image depicts a truck. C45-7/8/9 have different restriction symbols between formats. A29-17 has a different junction shape in its EPS. These are observations about the supplied artwork; the correct legal variant and final caption must be checked in 4D. See [comparison proof](proofs/variant-differences.jpg).

## Use in the next steps

Use `pages[].preferred_for_layout`, never a blind filename lookup. A null value means **held**. Each candidate links to its original source asset and records a maximum width/height at 300 ppi. Preserve aspect ratio. These are resolution ceilings, not guaranteed readable sizes; small text and thin lines still need final-page inspection. EPS itself is a scalable source, but its colours, canvas and actual rendered appearance must still be respected.

Both F1-1 and F1-2 are now present locally. The requested C31 speed examples (30, 40, 50, 70, 80, 110 and 120) are visible in the verified variants. SIG1–4 and SIG13 include multiple directional examples within single images; captions must identify those examples and explain changing indications separately.

The exact 09–18/two-hour parking assembly is still not an official collected composite. T18 supplies “2 tim”, while the T6 artwork uses different times and outline treatment. The first-aid and other non-sign illustrations remain outside this asset package.

**Next:** 4D verifies names, English labels, explanations and the held content issues. 4E maps eligible assets to passages. Steps 5–6 handle approved design and final PDF readability. No lessons, practice questions, app assets or PDF layout were changed in 4C.

## Reproduction notes

Ghostscript was installed through Homebrew for EPS verification. Renders use `-dSAFER -dBATCH -dNOPAUSE -dEPSCrop -sDEVICE=pngalpha -r300 -dTextAlphaBits=4 -dGraphicsAlphaBits=4`. Original EPS and web-image bytes remain intact. Embedded EPS preview extraction was not used for the deliverable; actual PostScript rendering was verified instead. Preserve the source/reuse records and the book’s learning-aid disclaimer when these files are used.
