# 9I — Exact fuel calculations and litre-unit wording

Applied 9I1–9I5 sequentially on 16 October 2026. Each stage consumes the preceding bank, exact 7D drafts and 9D1 authored option identities, and outputs the revised records, matching Kotlin and complete before/after arithmetic acceptance evidence.

| Step | Question | Old key | Exact key |
|---|---|---|---|
| [9I1](9I1/question-acceptance.json) | fuel-saving-150-0.5 | 0.8 litres | 0.75 litres |
| [9I2](9I2/question-acceptance.json) | fuel-saving-150-1.5 | 2.2 litres | 2.25 litres |
| [9I3](9I3/question-acceptance.json) | fuel-saving-250-0.5 | 1.2 litres | 1.25 litres |
| [9I4](9I4/question-acceptance.json) | fuel-saving-250-1.5 | 3.8 litres | 3.75 litres |

All four prompts explicitly request an exact result without rounding. Python Decimal independently multiplies the displayed distance by the supplied measured rate reduction and divides by 100. All four option values, their differences from the result and every explanation are checked. A separate test uses exact rational arithmetic. Each question has exactly one correct choice; supplied assumptions are not a guaranteed real-world saving.

[9I5](9I5/question-acceptance.json) applies only the six exact grammar drafts: fuel-40-5, fuel-saving-100-0.5, fuel-saving-100-1, fuel-saving-100-2, fuel-saving-200-0.5 and fuel-saving-200-1. Every numeric option, key, distance and rate is unchanged. Only approved field patches are applied. The exact drafts leave existing “1 litres” in some stems/general explanations; this limitation is recorded in [content-review.json](content-review.json), without silently expanding the wording changes.

IDs, concepts and authored option IDs remain stable. Numeric-answer changes use `fuel-exact-r2`; grammar changes use `fuel-unit-r2`. Snapshot scoring rejects a `legacy-r1` answer against the new revision. Earlier attempts must retain their original snapshot/key; they must not be reinterpreted using the current bank. Full persistence and accepted release-package integration remain later work. Acceptance here is per-question content acceptance, not release approval or clearance of the 9F sign holds.

Replay/check:

```sh
python3 tools/apply_fuel_corrections_9i.py --check
python3 tools/apply_load_clarifications_9h.py --check
python3 tools/apply_scenario_corrections_9g.py --check
python3 tools/check_sign_delivery.py --check
python3 -m unittest discover -s tools -p 'test_*.py'
./gradlew :composeApp:desktopTest --offline --no-daemon
```

`--through-step N` supports forward execution from the preceding stage and rejects rewinding over later typed stages. Historical 9E/9G/9H evidence is preserved; regression tests separately account for these ten later records.

Validation: **131 Python tests and 43 desktop tests passed**. All generated outputs reproduce exactly; 9G/9H reproduction and 9F hold checks pass. [Receipt](verification.json) · [Saved results](tests/).
