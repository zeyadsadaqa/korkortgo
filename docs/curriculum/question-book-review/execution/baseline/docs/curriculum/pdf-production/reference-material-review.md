# Step 6L reference-material review

Completed for screen review on 7 October 2026. Complete-book assembly and final publication checks remain steps 6M–6N.

## Delivered coverage

The 183-page reference PDF contains all four manuscript appendices: practical checklists, illustrated sign reference, Swedish–English glossary and personal practice record. The sign reference includes all required groups RB01–RB24, with 321 unique official entries and four links to entries shared across groups. There are 23 glossary terms, nine practice-record prompts and all 66 manuscript official references.

Editable production source is [reference/build_reference.py](reference/build_reference.py), with a generated [manuscript snapshot](reference/reference-source.md), [asset record](reference/assets.json) and [navigation record](reference/navigation.json). The authoritative manuscript and approved asset files remain unchanged. One obsolete Appendix B sentence about waiting for the illustrated reference was replaced with wording appropriate to the completed reference; no teaching claim was changed.

## Artwork and source treatment

All sign artwork uses the verified preferred assets and matches the recorded hashes. The 13 vector placements retain their reviewed minimum widths; raster artwork stays within the recorded 300 ppi size limits. Official outline artwork is intentionally preserved, without recolouring or redrawing. Each caption stays with its artwork, Swedish name, editorial English explanation, official link and actual caption-check date.

The exact Transportstyrelsen artwork credit is present. The prominent learning-aid disclaimer and non-endorsement wording remain. English explanations are identified as editorial translations. The 1177 entry remains a brief referral, with no added clinical teaching. No third-party book names or source-book pagination appear.

[Source checks](reference/source-checks.json) distinguish the manuscript’s 1 October factual checks, 2 October caption review, 3 October resolved asset checks, later individual chapter checks and 7 October link-availability checks. The catalogue and reuse guidance were checked again for this step. All 388 distinct external targets were checked: 386 successful HTTP responses and two Riksdagen targets retrieved successfully through the browser after local certificate-chain failures. No certificate validation was disabled. Full results are in [link-checks.json](reference/link-checks.json); link availability does not imply a new factual review of every page.

## Visual review

All 183 rendered pages were inspected, including every sign group, study table, code index, glossary page, writing area, reference page and credit. No missing required artwork, clipped text, overlapping captions or broken tables remain. Fonts, colours, headers and footers follow the approved production system. The glossary repeats its column headings and the practice record provides writing space beneath each prompt.

RB06 has a linked overview page because the first official vector panel requires more space than the group heading permits. This preserves the approved artwork size and keeps its caption together. The revised page 31 was rendered and inspected again. Other group-ending pages retain intentional whitespace rather than shrinking or splitting caption units.

## Verification

[Machine verification](reference/verification.json) passed:

- All 210 manuscript blocks/table cells checked against extracted PDF text.
- All 321 exact sign assets, 24 groups, four appendices and 66 source references covered.
- Four embedded Unicode fonts, Swedish text, page bounds and exact disclaimer checked.
- 554 internal links and 505 named destinations resolve within the standalone PDF.
- Every sign’s official URL, all manuscript references and the artwork-reuse link are present.
- Rebuilding produces identical PDF bytes; the delivery copy matches the production PDF.

SHA-256: `7bdd9b4aa0991a42abda5b730c62bbafafdf01de927347b173b48f5bce2c8b80`.

## Remaining stages

This is the standalone screen-review edition. Final book folios and chapter-to-reference navigation are assigned during 6M. Full tagged-PDF reading order/accessibility, final factual/publication verification and print-release suitability remain 6N. Completing this review does not execute or approve those stages.
