# Revised question coverage review

Reviewed all **1000 questions** against the **540-page G11 revised book** on 13 October 2026.

| Result | Original book | Revised book |
|---|---:|---:|
| Covered by book study | 697 | 772 |
| Missing knowledge/illustration | 233 | 158 |
| Prompt-only arithmetic/model | 70 | 70 |

**55/55 target situation gaps verified**, with 68 claim links. The square-of-speed addition also covers **20 braking-factor questions**, making **75 newly covered** records. No previously covered question lost support.

| Family | Covered | Missing | Prompt-only |
|---|---:|---:|---:|
| situation | 178 | 0 | 0 |
| sign | 458 | 158 | 0 |
| reaction | 36 | 0 | 0 |
| stopping | 0 | 0 | 30 |
| braking | 20 | 0 | 0 |
| gap | 20 | 0 | 0 |
| disc | 30 | 0 | 0 |
| load | 30 | 0 | 0 |
| fuel | 0 | 0 | 20 |
| fuel-saving | 0 | 0 | 20 |

## Remaining scope

**228 records still lack sufficient book teaching:** 79 missing sign codes affect 158 meaning/recognition records; 30 rough stopping-model and 40 fuel/savings records are prompt-only. The current book does not teach the rough reaction factor/0.4 braking coefficient or the fuel proportion calculation. No further teaching changes were made in G12.

Missing codes: A12, A17, A23, A32, A33, A6, A7, C10, C11, C12, C13, C14, C15, C29, C30, C33, C34, C4, C5, C7, C8, C9, D12, D8, D9, E23, E24, E25, F12, F22, F28, F29, F30, F31, F31a, F32, F33, G1, G10, G12, G3, G5, H10, H11, H12, H15, H16, H17, H18, H19, H20, H21, H22, H23, H24, H25, H26, H28, H4, H5, H6, H8, H9, J3, M17, M17a, M28, M29, M30, M31, M32, M34, S11, S13, S5, S6, S7, T23, T25.

## Evidence and files

- `question-page-map.json`: covered questions, actual pages, original prompts/options/answers and extracted evidence.
- `question-coverage-gaps.json`: every remaining unsupported/prompt-only record with precise reason.
- `all-question-coverage.json`: all 1000 records in original order.
- [G12 target review](execution/G12/target-coverage-review.json): actual printed anchors and source/claim linkage for all 55 targets.
- [G12 scenario decisions](execution/G12/scenario-decisions.json): reviewed decisions for all 178 scenarios; bound to actual PDF and bank hashes.
- [Arithmetic verification](execution/G12/arithmetic-validation.json): 206 independent calculations.

Book-page numbers include the cover and match verified continuous PDF labels. `original_source_page` retains the old bank’s page, not this book’s folio. No bibliography, code lookup or external link is accepted as teaching/illustration coverage.

## Coverage limits

The criterion is selecting the keyed answer from book study and reasonable application, not reproducing every keyed-answer detail or every distractor explanation. Entries 081, 087, 151 and 175 explicitly distinguish the taught core principle from more detailed keyed wording. Scope limits in all 55 target passages remain applicable. This is not a new legal/medical audit of the bank or a certification for publication, print or accessibility.

One non-blocking cross-reference issue: M06-L01 p.191 directs wildlife-collision actions to M10-L01; the correct section is M10-L02, p.326. Target q126 and collision q127 remain supported at their correctly mapped pages. [Observation](execution/G12/editorial-observations.json). G12 preserves the G11 PDF.

Question bank stayed byte-identical. Baseline audit files remain in the verified G0 snapshots. Book SHA-256: `c21ea3887b3f67bfd40a5683908df990187432a035d025898e7f0700380fa299`. Bank SHA-256: `303519698e564c9fb9aa835a29acd743d2038bca54be87cc71efd11951c4a3bb`.
