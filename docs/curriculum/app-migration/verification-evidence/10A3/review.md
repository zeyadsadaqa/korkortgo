# 10A3 — Verification cases and defect register

**20 October 2026 — complete.** Prepared independently owned cases for all ten original verification gates; no functional app test has run or passed in this task.

| Preparation output | Coverage |
|---|---|
| Gate/clause index | 42 observable clauses, all 36 original 7F coverage families and all 70 step-10 task dependencies; completion graph is acyclic |
| Data cases | 6,848 cases with bound source/registry/route/state/design oracles, including 1,557 source-located teaching blocks and all legacy aliases |
| Question cases | All 1,000 IDs/revisions: 336 retained, 626 rewritten, 38 replaced; exact twelve 9E batches and nineteen 9F pairs |
| Sign risk inventory | All 134 distractor changes; twelve faint assets and 24 affected question/slot bindings |
| Artwork runtime matrix | 2,920 future contexts: 2,464 shared renderer plus 152 each on Android, iOS simulator and browser; every image slot enumerated |
| Other runtime cases | 2,800 deterministic engine combinations, 132 production journey/settings cases, 96 supplementary representative contexts, 72 scoped-source contexts and 144 narrow/wide reflow contexts |
| Defects | Required severity/reproduction/fix/invalidation/retest fields; no open preparation blocker. One closed historical-locator verifier diagnostic retained, plus explicit known scope/editorial/coverage limits |

[Case index](verification-case-index.json) · [Data cases](data-cases.json) · [Question batches](question-batches.json) · [Runtime matrix](runtime-matrix.json) · [Defect register](defects.json) · [Execution/reproduction guide](reproduction.md) · [Preparation checks](results.json).

The integrity verifier checks unique IDs, frozen source hashes and 9,921 record locators, exhaustive memberships, conditional dispositions, runtime counts and dependency order. Rebuilding the case files with `--check` proves deterministic preparation; it does not pass the cases. All 10,942 explicit case IDs remain unrun except four conditional future-store cases; additional Cartesian sets are fully specified without duplicating each combination in JSON. Counts overlap intentionally across gates and must not be added as distinct product records.

The candidate remains the unchanged accepted 9J package. Runtime/content/build inputs and all historical receipts are preserved; only new verification preparation and plan/progress records were added. No current source-date refresh, build/installation, screenshot review, publication or design change occurred. Tool/service availability was checked in 10A2 only.

**10A1 → 10A2 → 10A3 is complete.** Stop here; 10B1 is the next separately requestable task.
