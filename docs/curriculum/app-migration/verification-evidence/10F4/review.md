# 10F sequence / T05 review

**10F1–10F4 have been executed sequentially. T05 remains open** for DEF-10F-001 and the 32 original platform journeys assigned to 10K. The accepted package and runtime sources are unchanged. The candidate is entry commit `44462b4`, manifest file SHA `ba91c96975c39b5f6db552c6bead17c0e0474c11dd590f811a7eeb1e1ae54a21`; its declared accepted identity remains separate from that file hash.

| Task | Actual evidence | Result |
| --- | --- | --- |
| 10F1 | 70 lengths × 20 deterministic seeds, independent Fraction allocation oracle, per-selection IDs/concepts/revisions/categories/options; 15 boundary rejections and mixed-held exclusion | Pass |
| 10F2 | 1,000 accepted questions × four key positions × two modes; 70 lengths × 20 seeds × two modes; 99,400 confirmed answer transitions and 198,800 review rows | Pass |
| 10F3 | Eight reconstructed historical rounded-fuel snapshots; 13 invalid-input cases | Historical checks and ten rejection cases pass; three required identity rejection cases fail |
| 10F4 | Four actual `App()` journeys using all 1,000 accepted questions, sizes 1 and 3, both modes; forty separate 70-question engine runs | Shared scope passes; all 32 original platform journeys remain pending 10K |

[Machine summary](results.json), [production results](production-quiz-results.json), [defect handoff](defects.json).

## Required rejection failure

**DEF-10F-001 / P2:** with `releaseAccepted=true`, an injected copy of the accepted bank can start a scored session when its content version is blank, its version is unrelated, or its manifest digest is wrong. `practiceStartCheck` checks release acceptance, duplicate identities, eligibility, category capacity and distinct topics, but does not authenticate the supplied identity against the payload/accepted release. [Exact observations](../10F3/invalid-input-observations.json) retain all three counterexamples. The required assertion failed: the 10F3 Gradle run correctly exits 1, with one failed test out of two. It is not relabelled as a passing rejection test.

This is an injected **conditional model-contract gap**. `App()` is statically wired to `acceptedPracticeBank9J`; it has no package-injection/import UI. These checks do not demonstrate a user-facing exploit or a wrong score in the fixed release. The bounded 10L correction must distinguish the trusted production boundary from deliberately constructed fixtures. No hot replacement, persistence, new input UI or design change is introduced here. Ten other guards correctly reject foreign options, stale answers, missing/foreign displayed identities, mixed session package identities, held/retired snapshots, an unaccepted release, duplicate bank IDs and the historical held candidate.

## Independent engine and scoring evidence

The allocation oracle uses exact rational shares and explicit priority VEHICLE, ENVIRONMENT, SAFETY, RULES, PERSONAL, RANDOM, without calling `QuizEngine.allocation`. At 70 it preserves 7/5/16/32/5 plus five residual slots. The actual bank has 500 concepts, each confined to one category (45/26/45/355/29 respectively). Every selected category meets its fixed quota, residual counts sum to the expected random slots, every concept/ID is unique and the same seed reproduces the snapshot. Boundary fixtures reject insufficient Rules despite surplus elsewhere, 65 quota topics without residual capacity, all held/retired/unreviewed banks, cross-category concepts, duplicates, invalid counts and the historical release gate. The engine excludes held additions from an otherwise sufficient bank.

10F2 loads authored keys independently from accepted JSON. Four rotations of every actual question cover all four key positions in both modes, including standard questions, image stems, image alternatives and all four exact-fuel revisions. The full seeded session matrix then checks actual shuffled orders, pending-versus-confirmed choice, confirmation locking, next/finish guards, hidden totals, immediate/deferred reveal and all four option explanations. Independent answer-ID comparisons establish scores and All/Correct/Incorrect positions; filtered rows map back to their original snapshot rather than current bank position. All-correct, all-incorrect and alternating answer patterns exercise empty and populated filters. The original immutable session remains unanswered while its copies advance.

10F3 reconstructs the exact four old `before` prompt/options/key/feedback payloads from the immutable 9I receipts. Old package identity and old acceptance/routing context are explicitly synthetic model fixtures, not an imported saved-attempt store or an activated old release. Their original rounded text, revision, order, selection and score survive reading newer teaching. A stronger conditional model with a changed newer key also cannot alter the old score. No real historical score or receipt is rewritten.

## Production and platform limits

The shared journey test composes **`App()`**, with its full accepted bank and normal `Random.Default`; it does not inject a one-question bank, replace image rendering or seed production setup. Exact observed IDs/revisions/order/answers are retained per journey. It checks the displayed 1,000-question count (zero held derived separately from the compiled accepted bank), setup/start, selection/confirmation, next/finish, expected 1/1 or 2/3 totals, all result-filter states, expanded explanation, related lesson, source detail and the registered URI callback, then return to the same expanded review and unchanged results. A URI callback is not external-browser/network success.

The shared surface is 1000×1800, density/font scale 1, production default light styling. These are semantic-action integration checks, not physical pointer hit tests, native lifecycle, OS-dark-mode support or speech/listening evidence. Two representative captures were visually inspected: `immediate-3-results.png` and `at_end-1-returned-review.png`. No exhaustive artwork/legibility signoff is inferred. All 44 logical captures resolve through [capture index](capture-index.json) to 36 stored PNGs; only byte-identical duplicates were removed.

[Original platform requirements](production-quiz-results.json) retain all 32 exact 10A3 production cases on Android, desktop, iOS simulator and wasmJs, both modes and four settings. Their wrong-answer/cancel-leave/return requirements are not replaced by these four supplemental shared flows. Fresh 10K2/10K3/10K4/10K6 observations remain required; physical iOS stays excluded under the existing simulator policy. The forty 70-question runs are model/engine evidence, not forty 70-question native UI runs.

All ten prior 10C/10D/10E product findings remain open, as do T02/T03/T04 and their source/platform limits. T05 remains open even though the 10F1/10F2 matrices and shared 10F4 flows pass. The next planned task is **10G1**; no 10G work was executed.

## Reproduction

Each task retains its actual Gradle log, JUnit XML, proof-class hashes and environment in `commands.json` / `environment.json`. The init script adds verification-only desktop test source directories; production build files are untouched. Run `prepare_oracle.py`, then each `--tests se.korkort.*10FTest` command in order. Reconstructing historical fixtures uses the retained `HistoricalFuel10F.kt` and hash-bound source receipts. The 10F3 run is expected to expose the current candidate's three failures. A later fix must preserve these failed observations and record fresh results.

`verify_evidence.py --check-manifests` checks truthful exhaustive accounting, independent oracles, observed failure classification, capture hashes and historical/protected input integrity. A passing evidence-integrity report verifies the evidence; it does not turn failed acceptance cases into passes.
