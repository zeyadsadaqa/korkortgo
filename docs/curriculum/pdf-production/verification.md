# 6N — Complete-book verification and release candidate

**Reviewed:** 14 October 2026.

**Status:** 6N complete for the screen edition. The user explicitly approved the finished tagged screen PDF on 14 October 2026: “OK approve 6N and move forward to 7C”. Print masters/proof are deferred by explicit scope decision, not certified as passed.

**Approved release:** [578-page curriculum PDF](korkortgo-curriculum.pdf), identical to its delivery copy. Accessibility machine checks, representative reader checks and all-page appearance verification pass within the stated scopes. The original untagged review source remains separately preserved.

**Current SHA-256:** `78a89d8ffbb83b6e9eec6193396871ac2fb9feccf245b85112809646dd595581`. See [screen-release.json](final-review/screen-release.json).

The initial audit below describes the untagged `ae872daf…` source and its then-open holds. Later sections record tagging, screen-only scope and their resolution; they are retained as audit history.

## Result

The complete book contains all ten original modules, 40 lessons, ten self-assessments and four appendices. Verified continuous page labels, named destinations, embedded Unicode fonts, selectable text, exact introduction disclaimer and absence of the old supplied book's names/publisher references. Existing original-content/evidence records support the curriculum; this audit does not certify copyright status or independently re-prove every factual sentence.

Corrected one production defect: the wildlife-collision paragraph in M06-L01 referred to M10-L01. It now explicitly points to M10-L02. Updated the manuscript and generated chapter source, rebuilt Chapter 6, verified it deterministically, and reassembled both review-book copies. Chapter 6 remains 50 pages and the book remains 578 pages. The exact changed text and its clickable target are on final page 193; all other page text is unchanged. The rendered pixel difference is confined to the corrected passage. No visual design, official artwork, question-bank content or answer was changed.

## Checks and evidence

| Check | Result |
|---|---|
| Content and navigation | 10 modules, 40 lessons, 10 reviews, four appendices; 3,525 valid internal links; 1,123 named destinations; own folios/PDF labels 1–578. |
| Question coverage | All 1,000 H7 evidence records revalidated against the corrected book. Historical H7 records retain their original hash; current evidence transfer is saved separately. Four fuel-rounding qualifications remain explicit. |
| Exact official files | 729 recorded sign placements, covering 400 unique source files, match recorded hashes. Existing caption/variant/reuse/placement reviews retained; original vector outline artwork remains unchanged at reviewed geometry. |
| Text and fonts | Four embedded Source Sans/Serif fonts with Unicode maps; 571,819 characters checked; zero out-of-page character boxes or replacement glyphs. Minimum recorded text size 9 pt. |
| Disclaimer and legacy labels | Exact disclaimer present on page 2; no Theory Book/Körkortonline/Hagberg naming in extracted book text. Curriculum titles match the canonical original structure. PDF/official-source page citations remain legitimate evidence, not legacy app routing. |
| External references | 517 distinct URLs enumerated: 504 successful HEAD/GET responses, 12 web-tool content fallbacks and one native-browser content fallback. No certificate validation bypass. Reachability is not factual endorsement. |
| Current requirements | Targeted publisher rechecks for B eligibility/practice, August 2026 changes, risk training, winter tyres, child protection, inspection intervals and limited first-aid reference. No new inconsistency found in that scope; retained claim-level source limits remain. |
| Shared text contrast | Approved foreground/page/panel colour pairs all exceed 4.5:1; minimum 7.99:1. This does not certify photo/sign pixels. |
| Render fidelity | Pre-correction full render: all 577 preserved bodies matched components. Fresh corrected full render: all 578 pages rendered, all 577 preserved source bodies match current components, zero unexpected differences. Contents/footer inspected separately. |
| Reproducibility | Corrected Chapter 6 and full final assembly rebuild byte-identically. Editable manuscript, build sources, pinned fonts/licences, component sources and current build manifest retained. |
| Accessibility | Document language and selectable Unicode text pass; 373 pages include ActualText spans. **Fail:** no StructTreeRoot or marked-document structure. This does not establish semantic headings/tables, tagged image/link alternatives or verified assistive-technology reading order. |
| Print resolution | **Held:** cover about 95 ppi; approved scene placements go as low as 67.6 ppi. Official sign geometry/file checks are separate. Existing screen-review images are not high-resolution print masters. |

All page layouts were inspected in 13 overview sheets, with the unchanged book's earlier full component and H6 review retained. The corrected page 193 and the thin outlined-panel example on page 59 were inspected at 1,600-pixel rendering. The latter is exact approved official outline artwork, readable at the reviewed full size but faint in reduced-size overview views; retain its width constraints and require reduced-size/print proof. A visual correction or replacement artwork must go through the requested imagegen preview/approval workflow before implementation. No such replacement is silently approved here.

## Release holds and completion criteria

- **6N-A11Y:** Produce semantic document tagging in the editable export path, validate heading/list/table/figure/link structure and reading order, and test representative module, review, sign and glossary pages with assistive technology. Adding only a language flag, metadata or empty structure tree would not fix this finding. Current selectable text/ActualText spans are useful but insufficient.
- **6N-PRINT:** Obtain approved high-resolution cover/scene masters and proof the official outline/white-symbol examples at intended reproduction size before a print release. The current candidate remains a screen-review edition. A decision to approve only that scope must be explicit; this audit does not silently relax the plan's print/readability requirements.
- **6N-APPROVAL:** The user approved this exact candidate on 14 October 2026. See [approval record](final-review/approval-record.json). This records approval without treating the outstanding technical requirements as passed or waived. Any revised candidate must retain its own verification and approval identity.

6N and step 6 remain in progress. No app implementation or question-to-lesson mapping started. The new manuscript, Chapter 6 and PDF hashes invalidate the provisional 7A–7B release bindings; their original records are retained as audit history, with a [release-change notice](../app-migration/release-change-notice.json). Refresh them against the approved finished release before 7C.

## Saved evidence and reproducible commands

- [Structural/content/geometry results](final-review/checks.json)
- [Current question-evidence revalidation](final-review/coverage-revalidation.json)
- [Official asset checks and scene resolution](final-review/asset-checks.json)
- [HTTP link results](final-review/external-link-checks.json) and [browser fallbacks](final-review/browser-link-fallbacks.json)
- [Current-source rechecks](final-review/source-rechecks.md)
- [Palette contrast](final-review/palette-contrast.json)
- [Fresh final render comparison](final-review/render-comparison.json)
- [Reproducibility result](final-review/reproducibility.json)

From the repository root, use the bundled Python interpreter documented in [README.md](README.md), or a matching pinned environment:

```sh
python3 docs/curriculum/pdf-production/chapters/M06/build_chapter.py
python3 docs/curriculum/pdf-production/chapters/M06/verify_chapter.py
python3 docs/curriculum/pdf-production/assembly/build_book.py
python3 docs/curriculum/pdf-production/final-review/check_release.py
python3 docs/curriculum/pdf-production/final-review/check_external_links.py
python3 docs/curriculum/pdf-production/final-review/check_render.py
```

Run builds and rendering sequentially: a render must not read a PDF while it is being rewritten. The render checker uses component renders under tmp/pdfs/h6/rendered; regenerate those with the assembly compare_book_renders.py utility if absent. The network link checker needs network access. Browser fallbacks are dated human/tool evidence, not automatically reproduced by the HTTP checker. Recreate candidate copies from the verified review PDF only after its hash is confirmed; copying to a release filename does not approve it.

## Approval recorded — 14 October 2026

User statement: “OK approved”, responding to the presented 578-page candidate and disclosed accessibility/print limits. The approved SHA-256 is recorded above and in final-review/approval-record.json. This closes the candidate-approval question; it does not certify missing tags, print quality or completion of 6N, and does not automatically execute 7C.

## Tagged candidate continuation — 14 October 2026

The earlier missing-structure finding above describes the approved untagged source. A separate [tagged candidate](korkortgo-curriculum-tagged.pdf) now has semantic headings, paragraphs, lists, 13 tables, 815 figure descriptions and associated link structure. Current SHA-256: `78a89d8ffbb83b6e9eec6193396871ac2fb9feccf245b85112809646dd595581`.

veraPDF 1.30.3 PDF/UA-1 machine validation passes. Parent-tree/annotation associations and original navigation pass the independent checker. All 578 pages render pixel-identically to the approved source; the final accessible link-name refinement leaves every page painting stream unchanged. Representative macOS Preview accessibility checks expose heading/figure/table reading order and working Contents/glossary links. This is not exhaustive VoiceOver listening or certification of every human accessibility requirement. See [verification](accessibility/verification.json), [reader review](accessibility/reader-review.md) and [reproduction instructions](accessibility/README.md).

6N-PRINT remains held. A [cover preview](print-masters/cover/cover-art-v1.png) generated from the approved visual direction is awaiting explicit design approval. Its native 1254 × 1254 pixels yield 167.6 ppi at 190 mm, below the 300 ppi target; it is not a print-ready master and has not been inserted. The built-in generator returned that size despite the larger prompt request. CLI/API fallback requires explicit confirmation under the imagegen skill, and no API key is currently configured.

The approved untagged candidate and its approval record remain unchanged. The tagged candidate awaits final approval; print resolution and intended-size outline proof remain outstanding. 6N stays in progress, and 7C has not started.

### Cover direction approved; print scope pending

The user replied “ok cintinue” to the cover visual-direction question. The exact preview's visual direction is now recorded as approved; its resolution shortfall remains. The [print inventory](print-masters/inventory.json) identifies 83 scene placements (79 distinct source crops), all below the 300 ppi target, in addition to the cover. Minimum replacement dimensions are saved without modifying the approved page layouts. The user has been asked to choose screen-edition completion with print deferred, or continued full print production. No scope waiver is inferred from visual approval.

## Current screen-release candidate — awaiting approval

The user explicitly chose “Finish the screen edition; defer print masters”. The scope of this release is now screen use; print masters and intended-size print proofs are deferred, not marked passed. The verified tagged bytes are copied to `korkortgo-curriculum.pdf` and `output/pdf/korkortgo-curriculum.pdf`, SHA-256 `78a89d8ffbb83b6e9eec6193396871ac2fb9feccf245b85112809646dd595581`. The original approved untagged source remains unchanged at `korkortgo-curriculum-review.pdf`.

The tagged export rebuilds byte-identically; its existing machine validation, representative reader review and 578-page pixel comparison apply to these exact bytes. The historical source approval is not silently transferred to the revised export. All recorded screen-edition production checks pass within their stated scope; final user approval of this candidate remains. 6N status: **Awaiting approval**. App migration has not resumed. See [screen release identity and scope](final-review/screen-release.json).

## Final screen approval recorded

The user explicitly approved 6N and authorised 7C on 14 October 2026. The tagged screen identity above is approved; 6N is complete within the chosen screen scope. Print work stays deferred. Original approval and earlier findings remain historical evidence.
