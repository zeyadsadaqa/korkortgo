# Sign caption review — step 4D

**3 October 2026 update:** Added exact official poster vectors and descriptive alternative text for the 13 previously held selected codes. Current totals: 494 eligible images, four optional holds. Teaching meanings were preserved. See the [resolution review](sign-assets/official-poster/README.md) and current package verification; the earlier review below remains historical.

**Completed:** 2 October 2026. **Result:** Captions complete for the usable package; 17 image holds retained.

This material is a learning aid to help understanding. It is not an official source and cannot replace current official information or applicable rules.

## Deliverables and evidence

[Readable captions](sign-captions.md) and [structured captions](sign-captions.json) cover all 263 selected identifiers and 235 additional linked pages. All 498 records preserve the official Swedish page name and include an editorial English label, original teaching explanation and official evidence. The 481 eligible image records include variant-specific alternative text and the exact preferred asset path and hash. The other 17 have no approved alternative text or placement asset.

Meaning checks used Transportstyrelsen's saved official page explanations and artwork, with [Vägmärkesförordning (2007:90)](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/vagmarkesforordning-200790_sfs-2007-90/) for the sign definitions and [Trafikförordning (1998:1276)](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/trafikforordning-19981276_sfs-1998-1276/) for associated road-user duties. Both consolidated legislation pages were consulted on 2 October. Sign-page retrieval dates remain 1 October except the five discrepancy rechecks below. Review date does not imply that all pages or images were downloaded again.

Each record links the exact detail page and parent explanation where applicable, with source hashes from [the source register](sign-sources.json). Captions use official sources only. English wording is editorial, not agency-approved. Practical reminders are teaching advice rather than additional statutory obligations. These concise captions do not enumerate every exception or replace the manuscript's fuller treatment.

## Important distinctions checked

- C6: the default trailer restriction excludes semi-trailers and centre-axle trailers unless qualified; it is not a blanket prohibition of every trailer.
- C27: retain the two-wheeled moped/motorcycle exception and the C28 endpoint. C31 is a legal maximum; E11/E13 are recommendations.
- T20: a ticket is required despite parking being free. T24 identifies externally chargeable vehicles; its symbol alone does not require active charging.
- T6: distinguish ordinary weekdays, days preceding Sundays/public holidays, red times, named days and periods crossing midnight.
- M16: marking alone does not distinguish a cycle crossing from a cycle passage. M19a and M20a have separate explanations from M19 and M20.
- SIG11: the horizontal bar is a stop indication with the stated late-change exception. SIG codes are website identifiers, not statutory paragraph numbers.
- Y2/Y3: sound and barrier movement have their own stopping implications. A still image is not a demonstration of sound, flashing or motion.
- Visual review corrected junction branches, priority-route diagrams, lane merges and direction arrows. Numerical variants retain their actual displayed speeds, weights, lengths, times and environmental-zone classes. Variant suffixes were not treated as a universal meaning code.

## Unresolved image holds

| Candidates | Issue | Disposition |
|---|---|---|
| S1, S2, S3, S4, S8, S9, S10, S12, T1, T2, T6, T8, T22 | Faint/outline source artwork | Keep out of layout until a suitable official image is verified. Textual meanings are available. |
| T8 | Web truck versus EPS wheelchair | No definitive variant-specific caption or alt text approved for this asset pair. |
| C45-7, C45-8, C45-9 | Web/EPS restriction symbols disagree | Generic C45 meaning is recorded, but no exact variant interpretation is approved. |
| A29-17 | Web/EPS junction geometry differs | Generic A29 meaning is recorded, but no exact junction diagram interpretation is approved. |

The two groups contain **17 unique held candidates**, because T8 appears in both. The five discrepancy pages were retrieved again on 2 October and still linked the previously recorded conflicting image/download URLs. This does not prove that remote image bytes were unchanged: the recheck concerned HTML links, not a new image download. No official clarification resolved the identity issues. Recheck dates, cache paths and hashes are in the structured captions. The 4C manifest and its holds remain unchanged.

## Handoff to 4E and 4F

Step 4E may select only records with `eligible_for_placement: true`, use their exact bound asset and respect its recorded size limits. Required held examples must be resolved with verified official artwork or explicitly replaced/omitted with the teaching consequence recorded. Do not silently use a parent image for a held variant. Accessibility text may need context-specific shortening during layout, but must retain the meaningful arrow, number, group or condition.

The original five held graphic requests in [the source/reuse report](sign-reuse.md) also remain applicable: captions do not authorise invented sign combinations, unverified arrow variants or substitute official artwork. Step 4F must reconcile remaining requirements before declaring the whole sign package complete. Final PDF reading order, alternative-text integration and visual quality at actual size belong to the later PDF work.

[Recorded checks](sign-caption-checks.json) cover record counts, source/asset bindings, hashes, naming, required fields, hold preservation and readable/structured parity. No app content, PDF design or lesson-placement map was changed in 4D.
