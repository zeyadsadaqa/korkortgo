# 9H — Driver-inclusive load definitions

Executed 9H1–9H6 sequentially on 16 October 2026, five questions per batch, using the exact 7D drafts and 9D1 authored option IDs. Each stage consumes the preceding bank and produces five revised questions, matching generated Kotlin and a per-question arithmetic/acceptance record.

| Step | Accepted records |
|---|---|
| [9H1](9H1/question-acceptance.json) | load-1200-350 through load-1350-450 |
| [9H2](9H2/question-acceptance.json) | load-1350-550 through load-1650-350 |
| [9H3](9H3/question-acceptance.json) | load-1650-450 through load-1800-550 |
| [9H4](9H4/question-acceptance.json) | load-1950-350 through load-2100-450 |
| [9H5](9H5/question-acceptance.json) | load-2100-550 through load-2400-350 |
| [9H6](9H6/question-acceptance.json) | load-2400-450 through load-2550-550 |

The fresh [primary-source review](source-review.json) confirms that car tjänstevikt includes the driver and maximum passenger/goods load is totalvikt minus tjänstevikt. Every prompt defines this convention; every explanation includes the same calculation and avoids counting the driver twice. This teaches registered maximum load, not actual remaining capacity on a particular trip.

All 30 supplied total/ready weights, option values and numeric keys are unchanged. Each acceptance record independently parses the displayed weights, subtracts them using integer arithmetic, checks all four numeric options and their distance from the result, and retains complete before/after content. Exactly one option equals the result. IDs, concepts and authored option IDs remain stable; changed semantics use `load-r2`. Earlier attempts retain their original revision/snapshot; full persistence and release acceptance remain later work.

The approved backlog stores these 30 IDs as one batch; the implementation plan divides that exact ordered set into six groups of five. No 9I changes or 9F hold approvals are included. Historical 9E/9G receipts are preserved; regression tests scope later changes separately.

Replay/check the completed work:

```sh
python3 tools/apply_load_clarifications_9h.py --check
python3 tools/apply_scenario_corrections_9g.py --check
python3 tools/check_sign_delivery.py --check
python3 -m unittest discover -s tools -p 'test_*.py'
./gradlew :composeApp:desktopTest --offline --no-daemon
```

`--through-batch N` supports forward execution from the preceding stage. Rewinding over later typed batches is rejected to prevent dropping their generated metadata. No original-bank regeneration is required.

Validation: **127 Python tests and 41 desktop tests passed**. Generated outputs reproduce exactly, 9G remains reproducible, and all 38 9F replacement originals remain unchanged and held. [Receipt](verification.json) · [Saved results](tests/).
