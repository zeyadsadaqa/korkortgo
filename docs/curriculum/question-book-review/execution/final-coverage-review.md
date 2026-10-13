# G12 final question coverage review

Completed 13 October 2026. All **1000 records** were rechecked against the verified **540-page revised PDF**. All **55 targeted driving-situation gaps** have actual printed teaching and **68 source-linked essential claims**. No question-bank or PDF changes were made by G12.

| Result | Original 498-page book | Revised 540-page book | Change |
|---|---|---|---|
| Covered by book study | 697 | **772** | +75 |
| Missing teaching/illustration | 233 | **158** | −75 |
| Prompt-only calculations | 70 | **70** | 0 |
| Total without adequate book teaching | 303 | **228** | −75 |

The gain includes **55 situation questions plus 20 braking-factor exercises** supported by G3's printed square-of-speed explanation. All 178 situation questions are supported under the stated criterion. No previously covered question lost support.

## Deliverables and numbering

- [Covered questions with final book pages](../question-page-map.json): 772 records, retaining prompts, options, keyed answers, category and evidence.
- [Remaining gaps](../question-coverage-gaps.json): all 228 missing/prompt-only records with precise reasons.
- [Complete audit](../all-question-coverage.json): all 1000 questions in original order.
- [55-target printed evidence and claim links](G12/target-coverage-review.json).
- [Reviewed scenario decisions](G12/scenario-decisions.json), [arithmetic verification](G12/arithmetic-validation.json), [coverage changes](G12/coverage-changes.json) and [validation](G12/validation.json).

`book_pages` and `primary_book_page` use one-based physical PDF pages, including the cover; continuous visible folios and PDF labels agree. `original_source_page` preserves the old bank field and is not a page in this book. All generated decisions are bound to the final PDF/bank hashes. The reusable audit script now checks evidence and actual component placement rather than reusing old hard-coded scenario statuses and page numbers.

## Target pages

| Question | Primary lesson | Teaching book page(s) |
|---|---|---|
| situation-013 | M05-L01 | 141, 142 |
| situation-045 | M07-L01 | 234 |
| situation-062 | M01-L02 | 9 |
| situation-068 | M01-L02 | 9 |
| situation-069 | M01-L02 | 9 |
| situation-070 | M07-L01 | 234 |
| situation-071 | M07-L01 | 234 |
| situation-073 | M07-L01 | 234 |
| situation-075 | M06-L03 | 205 |
| situation-076 | M09-L01 | 291 |
| situation-077 | M09-L01 | 291 |
| situation-078 | M09-L01 | 291 |
| situation-079 | M09-L02 | 295 |
| situation-082 | M09-L02 | 295 |
| situation-083 | M09-L01 | 292 |
| situation-084 | M09-L01 | 291 |
| situation-085 | M09-L01 | 291 |
| situation-086 | M09-L01 | 291 |
| situation-088 | M09-L02 | 295 |
| situation-090 | M09-L02 | 295 |
| situation-092 | M09-L01 | 292 |
| situation-094 | M09-L01 | 292 |
| situation-098 | M09-L04 | 305 |
| situation-099 | M09-L02 | 295 |
| situation-104 | M04-L02 | 110 |
| situation-105 | M06-L01 | 191 |
| situation-106 | M03-L04 | 84 |
| situation-107 | M03-L04 | 85 |
| situation-114 | M07-L02 | 239 |
| situation-116 | M07-L02 | 239 |
| situation-117 | M07-L02 | 239 |
| situation-119 | M05-L01 | 141 |
| situation-126 | M06-L01 | 191 |
| situation-129 | M01-L03 | 5, 11 |
| situation-131 | M02-L03 | 29 |
| situation-132 | M02-L03 | 29 |
| situation-135 | M05-L01 | 141 |
| situation-136 | M08-L01 | 259 |
| situation-138 | M03-L04 | 85 |
| situation-145 | M02-L02 | 26 |
| situation-146 | M02-L02 | 26 |
| situation-148 | M07-L02 | 240 |
| situation-149 | M07-L02 | 240 |
| situation-150 | M07-L02 | 240 |
| situation-152 | M07-L02 | 240 |
| situation-153 | M07-L02 | 240 |
| situation-154 | M02-L01 | 24 |
| situation-156 | M02-L01 | 24 |
| situation-157 | M02-L01 | 24 |
| situation-158 | M02-L01 | 24 |
| situation-159 | M02-L03 | 29 |
| situation-165 | M08-L02 | 272 |
| situation-172 | M08-L03 | 276 |
| situation-173 | M02-L01 | 24 |
| situation-174 | M10-L01 | 321 |

All targets passed fresh printed-phrase checks, individual required-claim linkage and full relevant-page review. The original claims' legal, vehicle and condition limits remain. Independent audit checks were not replaced by simply marking all target IDs covered.

## Remaining gaps

**79 absent sign codes** cause **158 meaning/recognition gaps**. Existing illustrated entries were verified by exact code, caption text and official asset placement; a family overview, code lookup or external link is insufficient. [Missing-code and question list](G12/missing-signs.json).

**30 rough stopping-distance questions** supply their own reaction formula and 0.4 braking coefficient. The new book teaches exact unit conversion, speed-squared scaling and a different explicitly assumed deceleration example, not those rough-model coefficients. They remain prompt-only. **40 fuel/use-savings questions** likewise supply enough numbers for proportional arithmetic without a taught fuel-calculation method. These families require separate teaching additions if all 1000 questions must be answerable from study.

## Checks and practical limits

All 178 scenarios reviewed against actual supporting pages, with six remapped/expanded-page cases inspected specifically. Stronger explicit passages were selected where appropriate, including the railway emergency answer p.228 and new hybrid teaching p.292. All 616 sign records checked by exact illustrated entries; all 206 numerical instances independently recalculated from the actual prompt figures and checked against keyed answers. Every ID occurs once, all page references exist, the covered/gap partition is disjoint and complete, and all question fields/original order remain.

The criterion is **selecting the keyed answer**, not reproducing every explanation or every clause of a keyed answer. Questions 081, 087, 151 and 175 explicitly record applications of core printed principles and limits on extra keyed detail (for example, individual-wheel braking is not itself explained, although stability control's stabilising function distinguishes the correct choice). This is a curriculum coverage audit, not a new legal/medical certification.

One non-blocking editorial correction: M06-L01 on p.191 points wildlife-collision actions to M10-L01; those actions are in **M10-L02, p.326**. Q126's prevention teaching and q127's collision response remain supported by their correct mapped passages. [Observation](G12/editorial-observations.json). The G11 PDF is preserved; no extra editorial changes were folded into G12.

Reproducible replay passes. Representative full-size pages 84, 85 and 443 reviewed; G11's full-page component comparison and affected-page visual checks remain evidence. Question bank, book, delivery copy and ten chapter PDFs stayed byte-identical; all **154 G0 snapshots** verified. Original audit files remain in those snapshots, and the original audit code is also saved in G12.

Book SHA-256: `c21ea3887b3f67bfd40a5683908df990187432a035d025898e7f0700380fa299`.

Question-bank SHA-256: `303519698e564c9fb9aa835a29acd743d2038bca54be87cc71efd11951c4a3bb`.

## Plan completion

**G0–G12 complete for the approved 55-gap plan.** Remaining 228 bank records are explicitly listed; filling them is a further curriculum scope, not part of the completed chapter-gap plan. Publication/app migration, print masters and full tagged-PDF accessibility approval remain separate.
