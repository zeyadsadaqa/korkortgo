# 7G — Complete app-migration planning verification

**Verified:** 14 October 2026. **Result: PASS — step 7 planning complete.**

[Machine-readable results and input hashes](verification.json) · [Implementation backlog](implementation-backlog.md) · [Preview handoff](preview-handoff.md)

Freshly ran 7C, 7D, 7E and 7F acceptance procedures, then checked the relationships across the full package. **60/60 cross-stage checks pass.** The current 7F checker also reports 68/68. These are planning/evidence checks, not runtime app or design acceptance.

## Verified package

| Area | Result |
|---|---|
| Approved input | Tagged 578-page screen release; all stages agree on SHA-256 `78a89d8ffbb83b6e9eec6193396871ac2fb9feccf245b85112809646dd595581`; explicit 6N approval retained. |
| Frozen input integrity | All 177 baseline input records and 343 bundled asset records match, as do recorded cross-stage hashes. Protected bytes and prior planning artifacts unchanged during verification. |
| Curriculum | 10 modules, 40 lessons, 10 reviews, four appendices, 24 reference groups. All 1,123 published destinations unique, source-located and matched to approved navigation folios. |
| Questions | All 1,000 baseline IDs in order across 7A–7F, 500 concepts, correct scoped teaching/source routes and unchanged original bank. |
| Decisions | 336 retain, 626 rewrite, 38 replace, zero remove. Every changed item has evidence, acceptance criteria and a bounded implementation owner. Four exact fuel revisions remain proposals. |
| Sources/assets | 116 canonical source destinations, 404 exact question URL records, 400 sign/caption/asset bindings and 2,464 proposed sign-option bindings checked against retained evidence; all 83 lesson scene placements and 329 chapter sign placements retain their approved source hashes. |
| Legacy navigation | 39 chapters, 361 numeric page entries including 38 gaps, 178 topic identities and 343 catalogue records accounted for. 340 exact sign routes; three explicit unavailable policies. |
| Learner state | Eight navigation states, 12 entry-point rules, 22 state contracts, original option-order/score preservation. No durable store or real data migration exists. |
| Implementation/design handoff | 15 dependency-ordered work items, exhaustive question ownership/batches, all issue/state/label coverage, exact preview fixtures and ten future step 10 procedures. |

## Planning blockers and implementation limits

No blocking migration-planning issues remain.

The following are explicit future work or scope limits, not evidence that implementation acceptance has passed:

- **IMPLEMENTATION-ACCEPTANCE** — 626 rewrites require per-item acceptance; 38 replacements additionally require exact official geometry, intended-size/zoom and accessible-equivalent proof. All remain unapplied. No silent omissions or quota changes.
- **SIG16-18** — Retain explicit unavailable_exact_entry policy for SIG16–18; exact official URLs and optional M03-L02 related teaching from 7E. No approved destination or asset is added.
- **ASSESSMENT-COVERAGE** — M01-L01 and M10-L03 have no primary or related questions; M07-L04 has no primary and one related. Keep teaching discoverable and prepare separately reviewed briefs.
- **SOURCE-CURRENCY** — 7G verifies exact stored source/evidence bindings, not current availability or every legal claim. Recheck time-sensitive affected rules when applying edits and refresh records if changed.
- **DESIGN-AND-DEVICE-PROOF** — Step 8 must use imagegen and obtain explicit design approval. Real app builds/device/accessibility runs remain future evidence; planning checks do not certify runtime behaviour.
- **PRINT** — Print masters and print-resolution remediation were deferred by user scope; this audit does not reopen or certify them.

The 38 exact question holds, their 19 sign codes and 9F ownership are retained individually in the JSON report. If official delivery cannot meet acceptance, return an explicit alternative-item/ID decision. No removal or similar-signal alias is authorised by this audit.

## Interpretation and reproducibility

7A–7E include historical “next step not started” statements and historical review-book hashes. They describe their own execution time, not current blockers. This report binds the current approved tagged release and current frozen package without rewriting historical evidence. The former 39-chapter app is compatibility input only; it is not the curriculum to import.

Rerun from the repository root:

```sh
python3 docs/curriculum/app-migration/verify_migration_package.py
```

The script runs upstream validators sequentially, independently checks cross-stage counts/IDs/inputs/links/evidence/assets/state/backlog and writes these two reports. It fails with a nonzero exit code on any blocking check. Its input manifest includes the verifier itself, prior artifacts and referenced sign/scene assets, excluding these output reports to avoid circular hashes.

**Next:** 8 — generate app previews with imagegen, then wait for explicit design approval; request separately. No app code, live question, official asset or approved PDF was changed.
