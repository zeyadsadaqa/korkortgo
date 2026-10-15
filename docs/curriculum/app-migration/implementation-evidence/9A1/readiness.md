# 9A1 — Input readiness

**Executed:** 15 October 2026. **Status:** Complete. **Blocking drift:** None.

The user requested only 9A1: “ok go ahead with 9A1”. The approved input package is ready for 9A2 when separately requested. No app migration, question edit or new design was performed.

[Baseline](input-baseline.json) · [Execution review](review.md) · [Read-only recheck](verify_inputs.py)

## Identity results

All **1,174 retained hash bindings match**. The consolidated snapshot freezes **1,055 unique files**, including the separately identified current execution context. All **21 readiness checks pass**. Repeated references to one file count as multiple bindings, not multiple files.

| Retained authority | Bindings | Result |
|---|---:|---|
| 7A frozen app/content/production inputs | 177 | Match |
| 7A bundled sign assets | 343 | Match |
| 7G migration-package manifest | 466 | Match |
| 7B–7F cross-stage inputs | 102 | Match |
| Design specification, inputs and index | 9 | Match |
| Approved preview artifacts | 56 | Match |
| Preview content/source bindings | 16 | Match |
| Approved screen delivery copies and corrected review source | 5 | Match |

The approved 578-page screen edition retains SHA-256 `78a89d8ffbb83b6e9eec6193396871ac2fb9feccf245b85112809646dd595581`. All four tagged screen delivery copies match that identity; the earlier corrected review PDF matches its separate recorded hash. Production sources/corrections, manuscript, registries, official artwork, lesson illustrations, app source and question-bank identities remain covered by the retained manifests.

The bank retains 1,000 unique question IDs and 500 concepts; planned dispositions remain 336 retain, 626 rewrite and 38 replace. The current Kotlin/Swift/plist source inventory has no unreviewed additions outside the baseline inventory.

## Approval and evidence interpretation

The final approval in [app-design-review.md](../../../app-design-review.md) explicitly records “yes approved” on 15 October 2026. All twelve indexed preview approvals and sixteen boards retain their recorded identities. The saved 7G result contains 60/60 passing checks and the saved 8O technical result contains 681/681 passing checks. This task rechecked their input identities and approval records; it did not rerun those upstream workflows or claim a fresh 681-check execution.

The 8O machine-readable report deliberately retains its pre-approval status/null approval field. Its documented final human approval is in app-design-review.md; this is not an unresolved approval blocker. The current approval review, execution plan and audit tooling are separately labelled newly frozen context where no prior checksum exists. A new checksum is not proof of an earlier review.

Existing staged/unstaged PDF changes and historical deleted review copies were present at entry. Git status alone is not the approval baseline: the required current release/review files match their retained hashes. This task did not restore, regenerate, stage or remove those user files.

## Remaining acceptance work

No identity mismatch requires an audit refresh now. Any later change to a frozen required input must be reviewed through its recorded authority and dependent package checks; do not simply replace the expected checksum.

Question acceptance, 38 exact-image delivery holds, neutral assessment descriptions, source currency, actual rendering/accessibility and platform/device checks remain future work. SIG16–18 retain explicit unavailable internal routes. The three assessment briefs remain required, and print masters remain deferred. Existing design approval clears none of these implementation gates.

**Next:** 9A2 — define the typed content contract, only after a separate request.
