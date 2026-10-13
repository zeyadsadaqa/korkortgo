# Sign package verification — step 4F

**3 October 2026 re-verification:** All integrity checks pass and all 263 selected codes have eligible artwork. The 13 gaps were resolved using [official poster vectors](sign-assets/official-poster/README.md). All 321 placement bindings are eligible; four optional mismatches remain excluded. Step 4F and step 4 are complete for asset preparation. Final page legibility and design approval remain later checks. The earlier report below is historical.

**Reviewed:** 2 October 2026. **Result:** Review performed; completion gate blocked. **Step 4 remains in progress.**

All local integrity and relationship checks passed. However, **13 selected sign images still lack an eligible asset and approved image alternative text**. The plan requires every required sign to be ready before 4F can clear the package. This report does not mark 4F or step 4 complete.

This material is a learning aid to help understanding. It is not an official source and cannot replace current official information or applicable rules.

## What was verified

| Area | Evidence and result |
|---|---|
| Selection | All 263 unique 4A codes match the source register and have exactly one primary reference entry. |
| Sources | All 498 official detail-page snapshots and the saved reuse-policy snapshot exist and match their hashes. Source identities and caption citations resolve. |
| Original assets | All 993 original files match recorded sizes and hashes. Download URLs resolve in their recorded source-page relationships. No missing or unmanifested original/render files were found. |
| Raster and render integrity | All 498 raster images and 495 saved EPS renders decode at recorded dimensions. EPS headers and recorded positive bounding boxes pass. The renders were not regenerated. |
| Captions | All 498 records preserve official Swedish names and editorial English wording. All 481 usable catalogue candidates have caption and alternative text. Readable and structured caption content match. |
| Placements | All 321 mapped codes match their caption and preferred-asset bindings: 308 eligible images and 13 explicit selected gaps. All 54 lesson placements and 24 reference groups have valid manuscript anchors. |
| Variants | All 498 records have explicit dispositions. Held variants cannot enter a ready placement; no code or asset-ID collisions were found. |
| Input versions | The source-register, manifest, captions, manuscript and placement input hashes remain consistent. Existing upstream content and artwork were not changed. |

Detailed machine results are in [sign-verification-checks.json](sign-verification-checks.json). The [verification script](verify-sign-package.py) can be rerun with Python and Pillow:

```sh
python3 docs/curriculum/verify-sign-package.py
```

Exit code **2** means that integrity checks passed but required image gaps remain; **1** means an integrity failure; **0** means the automated readiness conditions pass. These checks supplement editorial review and cannot certify legal accuracy or final PDF quality. This run used the bundled Python runtime with Pillow.

## Reuse and source review

The current [Transportstyrelsen road-sign reuse paragraph](https://www.transportstyrelsen.se/sv/om-oss/pressrum/pressbilder/) was consulted on 2 October. It remains consistent with the saved 4B evidence: sign files may be used for different purposes, with a request to respect their meaning and context. The distinct press-photo restrictions are not a licence for other artwork. The existing interpretation covering the linked catalogue's markings, signals and authorised directions remains documented in [sign-reuse.md](sign-reuse.md); it is not an agency endorsement or a separate licence statement for each family.

All asset reuse-policy IDs resolve. Retain the project artwork credit, official URLs and verification dates in the final references. No third-party book is used as evidence in the sign package. English labels remain editorial translations.

This review reconciled the 4D factual evidence and checked source/variant associations; it did not repeat a full legal review of every caption or download every remote file again. Original sign retrieval dates remain 1 October. The five conflicting-page link rechecks recorded in 4D remain dated 2 October. A new review date is not a claim of new remote-image verification.

## Blocking selected images

The focused [contrast proof](sign-assets/proofs/contrast-check.jpg) and [variant comparison](sign-assets/proofs/variant-differences.jpg) were inspected again. They support retaining the existing holds; no artwork was recoloured, redrawn or substituted to pass the gate.

| Code | Official name | Required locations | Blocking issue |
|---|---|---|---|
| S1 | Tung lastbil | RB22; LP048 | No approved readable image at teaching scale; no approved image alternative text. |
| S10 | Gående | RB08; LP010 | No approved readable image at teaching scale; no approved image alternative text. |
| S12 | Personbil klass II | RB22; LP048 | No approved readable image at teaching scale; no approved image alternative text. |
| S2 | Tung lastbil med tillkopplad släpvagn | RB22; LP048 | No approved readable image at teaching scale; no approved image alternative text. |
| S3 | Personbil | RB06; LP008, LP050 | No approved readable image at teaching scale; no approved image alternative text. |
| S4 | Personbil med tillkopplad släpkärra | RB06; LP008, LP050 | No approved readable image at teaching scale; no approved image alternative text. |
| S8 | Cykel och moped klass II | RB06; LP008, LP010 | No approved readable image at teaching scale; no approved image alternative text. |
| S9 | Släpkärra | RB22; LP048 | No approved readable image at teaching scale; no approved image alternative text. |
| T1 | Vägsträckas längd | RB06; LP008 | No approved readable image at teaching scale; no approved image alternative text. |
| T2 | Avstånd | RB06; LP008 | No approved readable image at teaching scale; no approved image alternative text. |
| T22 | Text | RB06; LP008 | No approved readable image at teaching scale; no approved image alternative text. |
| T6 | Tidsangivelse | RB06; LP008, LP031 | No approved readable image at teaching scale; no approved image alternative text. |
| T8 | Symboltavla | RB06; LP008, LP031 | Outline/faint artwork and conflicting truck/wheelchair content between formats. |

Every code above is still selected, so a text-only placeholder does not satisfy its current image requirement. The source-linked teaching text is retained, and the map correctly prevents the images from entering layout.

**Required resolution:** Find a readable, matching official asset for each selected requirement and verify its identity, meaning and reproduction quality. If a requirement is instead removed or replaced, make an explicit editorial selection revision and record the teaching consequence. Neither route was silently applied during this audit. A generic S symbol and a T8 panel are not interchangeable assets merely because both depict a vehicle.

After resolution, update the asset manifest, captions/alternative text and placement bindings together, refresh their dependent hashes/checks, then rerun 4F. Keep the original source evidence and record the new verification evidence.

## Excluded optional variants and duplicates

**A29-17 and C45-7/8/9 remain held and excluded** by the 4E map. Their four holds do not add four required-image blockers, because no selected placement depends on them. They must remain excluded unless their official identity is resolved.

One identical-byte group was found among originals: the web images for **C45-6 and C45-7**. This is the previously recorded source duplicate, not an accidental duplicate code. C45-7 remains held; C45-6 retains its independently recorded matching source/render. Do not deduplicate the two semantic records or treat the same bytes as proof of the same restriction.

T12's preferred web image remains an intentional choice over its outline EPS rendition. Raster-only F1-2, F8-2 and Y2 retain their recorded size limits. Y2 remains a sound icon, not an audio or animation demonstration.

## Remaining illustration decisions

| Item | Current treatment | Completion consequence |
|---|---|---|
| Exact two-hour / black unbracketed 09–18 parking example | Manuscript text retained; E19 and T18 available as separate components. No verified complete assembly. | Do not insert T17's 8–17 or E30's different duration as this example. D06 remains a later design brief; T6's selected image gap is still a blocker. |
| Railway crossing-ID close-up | Text only; no invented identifier or claim that the supplied crossbuck depicts one. | Existing 4E omission is explicit. A future close-up needs its own official source and reuse review. |
| Additional signal arrows, flashing, sounds and hand movements | Supplied examples and explanations only. | Do not invent missing variants or claim that a still image demonstrates motion/audio. |
| Warning triangle, wildlife marker, practice sign, tyres, cargo lamps and dashboard graphics | Text only under G05/G06. | Outside the sign package; any later illustration needs separate sourcing/design review. |
| Contextual road scenes D01–D08 | Content briefs only. | Step 5 requires imagegen previews and explicit user approval before implementation. No scene is approved by this review. |
| Final page sizes and PDF accessibility | Recorded size limits and alt text available. | Actual-size visual inspection, reading order and embedded alternative text must be checked in step 6. |

The explicit text-only and deferred-design decisions are distinct from the 13 still-required held images. No missing diagram was claimed to be an approved official illustration.

## Handoff

The **verification activity is finished**, but the **4F completion criterion is not met**. Keep step 4 in progress and address the 13 selected image requirements before signing off its package. Step 5 has not started. The manuscript, app and PDF design remain unchanged.

Preserve the source HTML working caches alongside the manifest evidence if the project is moved or cleaned: the verifier uses their recorded paths and hashes. Earlier check reports are dated snapshots; a historical progress-file checksum is not expected to match a subsequently updated tracker.
