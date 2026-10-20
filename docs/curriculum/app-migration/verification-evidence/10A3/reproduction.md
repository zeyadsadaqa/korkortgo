# 10A3 — Execution and reproduction

This package freezes the verification work; it does **not** pass the app. Candidate commit `aa4f0e18fbd0e1ebcfd3246c15063c85831ab3ac`, accepted manifest SHA-256 `ba91c96975c39b5f6db552c6bead17c0e0474c11dd590f811a7eeb1e1ae54a21`, package digest `d9ba2f0261dc9c908146676f903a5ee7fd9c73b50231cd10c2182ecf5d87f82a`. The runtime/content/build fingerprint and all inputs are retained in [10A1](../10A1/candidate-baseline.json).

## Check these preparation artifacts

Run from the repository root:

```sh
python3 docs/curriculum/app-migration/verification-evidence/10A1/verify_baseline.py --check
python3 docs/curriculum/app-migration/verification-evidence/10A3/build_case_index.py --check
python3 docs/curriculum/app-migration/verification-evidence/10A3/verify_preparation.py
```

The first command compares the frozen entry inputs; plan/progress-only drift is reported for review. The second compares exact prepared JSON against the same deterministic recipe and bound inputs. The third resolves every oracle pointer, validates record hashes, unique case IDs, exhaustive memberships and acyclic dependencies; it writes only this task's results. None builds the application, runs its suites, opens external sources or rewrites historical acceptance. The scope builder in 10A2 reconstructs its matrix from **saved** observations; it does not refresh live availability.

## Use the case files

- [verification-case-index.json](verification-case-index.json): 42 checkable clauses covering all ten original gates, all 36 original coverage families, immutable oracle files and all 70 task dependencies. Expected outcomes come from approved source/route/state/decision records, independent arithmetic and approved visual revisions. Current candidate snapshots pin identity and are not proof that their contents are correct.
- [data-cases.json](data-cases.json): 6,848 exhaustive content/source/route/state/design cases, including 1,557 source-located teaching blocks, 1,123 destinations, 24 reference groups, 1,921 compatibility routes, eight states, twelve entry rules, sixty reading nodes, all 22 state contracts, five filters, forty tags and fourteen copy rules. Four absent-store cases are explicitly conditional. Some families intentionally overlap; these are test cases, not counts of distinct app records.
- [question-batches.json](question-batches.json): each of 1,000 exact IDs/revisions has an owner and pointers to original/approved decision, current accepted snapshot and acceptance evidence. Twelve 9E batches are 11×50 + 28 = 578; nineteen 9F pairs total 38. Keep all 134 overlapping distractor IDs and twelve faint assets/24 question-slot bindings.
- [runtime-matrix.json](runtime-matrix.json): 616 sign questions × four settings on the shared desktop renderer (2,464 contexts), plus every 38-replacement × four settings on Android/iOS simulator/browser (152 each). Each context enumerates exact stem/option zoom slots and accepted revision. Eight additional representative IDs cover 32 supplementary contexts per native/browser target, including the oversized M17a raster regression. These are future runs, not reused historical captures.
- [defects.json](defects.json): severity, required finding fields, bounded fix/invalidation/retest workflow, one closed preparation-tool diagnostic and retained limitations. No open preparation blocker or new verified product defect is claimed.

## Runtime procedure

Use light/dark × 100%/160% text with the same font and measured viewport. Shared replay starts at 390×844 logical pixels; Android uses the observed emulator and iOS the original iPhone 17 simulator. Record actual native insets/density/bounds rather than assuming preview pixels equal device dimensions. A separate 320/390/1280-wide desktop/browser matrix checks six states at four settings (144 contexts); it does not invent minimum supported widths. Preserve the approved 220 dp assessment/lesson/review frames and 380 dp wide-reference frame, source geometry, equal option sizes and white artwork backing.

For each full-question artwork context: load the pinned accepted revision in a labelled harness; record normal/proof identity; inspect fit and all options; select an authored option without confirming; open every exact image slot, zoom to 150%, pan, reset, close; assert the same selection, accessible trigger and source artwork identity. Inspect the inline question at actual size as well as the enlarged image. Neutral pre-answer text must not reveal code/name/key. Shared semantics or a thumbnail/contact sheet alone cannot certify native legibility.

Run the 132 specified production journey/settings cases. Android/iOS/browser production journeys use the normal integrated owner and real accepted bank, both feedback modes, wrong-answer score, guards, filters, teaching/source and context return; record random IDs and displayed option order for reproduction. Do not change the production bank to force a desired item. The desktop UI fixture is explicitly separate from actual full-bank model/parity tests because no desktop launcher is configured. Fixed-case replay uses a labelled verification harness, not a claimed random production run.

Run lengths 1–70 × seeds 0–19 × two feedback modes (2,800 engine cases). Calculate the quota oracle independently using exact integer largest remainders and stable category order VEHICLE, ENVIRONMENT, SAFETY, RULES, PERSONAL, RANDOM; use 7/5/16/32/5 plus 5 at 70, check post-quota concept capacity and residual selection. Cover all four key positions, invalid counts, held/retired/insufficient capacity fixtures and old rounded-fuel snapshots. Never derive expected values by calling the production allocator/scorer.

The six frozen source examples cover law, foreign guidance, research, commercial teaching, manufacturer limits and editorial variable-time arithmetic. The arithmetic case keeps its contextual research URL; it has no invented editorial publisher/URL. 10C1 independently confirms scope before the 6×4 targets×3 states = 72 source-detail/dispatch/unreachable-return cases. Desktop intercepts URI dispatch; native/browser checks actual callbacks. A remote site outage is distinct from failure to dispatch or preserve app context.

Only Android has a required fresh TalkBack listening/navigation case in the existing scope; native node assertions are separate evidence. TalkBack is installed but currently disabled, so record/restore its original setting. iOS simulator checks native description/trait/focus without claiming VoiceOver listening. Browser/desktop retain their documented speech/bridge limits. See [scope matrix](../10A2/scope-matrix.json) for each required/excluded row.

## Ordering, results and reruns

10B module reviews and 10E batches can be requested independently once prerequisites pass. The valid completion order in the index is a dependency graph, not authorization to execute every node. Platform-dependent source/design/state tasks prepare their cases before 10K and close after its observations; this avoids a dependency cycle. Stop after the user's requested sequence.

The normal builds omit `-PreferenceProof`; proof builds use separate identities and must be restored afterward. Exact historical platform command recipes are in 9O3–9O7 and the content build guide; rerun them for the current candidate and record any changed output path. iOS CLI paths that skip the Kotlin build phase must explicitly copy verified resources before installation. Recheck service/tool availability at execution and restore devices, network settings, normal app and temporary servers/tabs.

Save actual results under the owning task, using stable case IDs, candidate/runtime hashes, commands, target, expected/observed, status and attachments. All current T cases are `not_run`, with only the four future-store cases conditional and platform exclusions explicit. Changes invoke 10L: record the affected IDs/files and gates, retain failures, invalidate impacted evidence, obtain required preview approval for new visual design, rerun original failure and dependent checks, then close. Do not edit this prepared index to turn a failed case into an exclusion.

**Next separately requested work after 10A: 10B1.** No 10B–10M task has executed here, and no commit, push or publication is part of this preparation run.
