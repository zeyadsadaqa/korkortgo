# 9G — Eight scenario corrections

9G1–9G8 applied sequentially on 16 October 2026. Each stage consumes the exact 7D draft, the 9D1 authored option identities and a fresh primary-source review. Its output is one corrected question in `content/questions.json`, matching generated `Bank.kt`/`ScenarioCorrections9G.kt`, and an entry in [question-acceptance.json](question-acceptance.json).

| Step | Question | Correction |
|---|---|---|
| 9G1 | situation-032 | Parenthesised hours retain the weekday restriction and named-day override |
| 9G2 | situation-045 | Lighting prohibition scoped to a passenger car |
| 9G3 | situation-105 | Return route explicitly conditional on permission and safety |
| 9G4 | situation-107 | Gradual forward-gap adjustment; necessary emergency braking retained |
| 9G5 | situation-125 | Notify owner or police as soon as possible |
| 9G6 | situation-162 | Driver included once in tjänstevikt; totalvikt distinct from actual bruttovikt |
| 9G7 | situation-172 | Automatic deadline ban distinct from off-road status and dangerous-condition bans |
| 9G8 | situation-178 | Driver/passenger personal injury included; own-car damage excluded |

[Source review](source-review.json) records verification dates, URLs, locators, scope decisions and all four option verdicts. The historical Trafikverket closure URL now returns no article body. It is not certified as current route advice: the rural-return answer remains an explicit conditional editorial inference constrained by current Swedish law. The Northern Ireland manual contributes general defensive-driving advice only; its taxi law and two-second target are not imported. No proposal required a wording departure.

All IDs, concepts, answer keys and authored option IDs are retained. Revised questions use `scenario-r2`; earlier attempts must retain their original revision/snapshot. The legacy persistence/complete release migration is not certified by this content work. These text-only corrections have accepted content metadata; they do not clear the 616 held sign questions, activate complete curriculum routes, or approve a release.

Reproduce and verify:

```sh
python3 tools/apply_scenario_corrections_9g.py --check
python3 -m unittest discover -s tools -p 'test_*.py'
./gradlew :composeApp:desktopTest --offline --no-daemon
```

The 9E regression tests continue checking their frozen stage and all live sign records, while the 9G tests independently verify exactly eight later changes and the full live typed bank. Historical 9E/9F receipts remain historical and are not regenerated as new approvals.

Validation: **122 Python tests and 40 desktop tests passed**, exact output reproduction passed, and the 9F delivery check confirms all 38 replacement originals remain unchanged and held. [Receipt](verification.json) · [Saved results](tests/).
