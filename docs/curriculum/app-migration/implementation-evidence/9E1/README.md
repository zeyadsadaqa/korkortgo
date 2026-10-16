# 9E1 — A1–A25 sign rewrites

Completed the exact first 9E backlog batch: 50 questions. [Per-ID before/after and acceptance](batch-acceptance.json) · [Readable diff](before-after.diff) · [Content review](content-review.json) · [Verification](verification.json).

Applied the exact approved 7D prompts, meanings, all four option explanations, authored option IDs and correct keys. Both directions retain their question/concept IDs and use semantic revision `rewrite-r2`. Twelve question records include approved distractor changes. The 125 stem/option image occurrences use exact bundled artwork and the physical descriptions reviewed in 9D3.

`content/questions.json` retains its legacy array structure and adds the typed `assessment` object only to these 50 rows. The generated Bank.kt carries the same typed object alongside the legacy facade. All other 950 question records and their generated constructor lines remain unchanged. The existing source records, curriculum and official art are reused without changes.

**Content checks pass; all 50 questions remain held from scoring.** Intended-size/zoom/light-dark/accessibility delivery checks and runtime assessment integration are still required in 9L/9O. The eligibility guard applies to legacy selection/direct sessions as well as the new assessment engine. The facade does not activate or render these questions in the legacy card. No device proof, new layout or release acceptance is claimed. The pre-existing 38 held replacements remain 9F work.

The pre-9E1 bank and JSON are saved as `incoming-bank.kt.txt` and `incoming-questions.json`. Historical compiler tests resolve their retained question origins against this exact old-byte snapshot in temporary test payloads; prior evidence/source authority is not rewritten. Historical verification receipts describe their original execution state and should not be regenerated against the changed live bank.

## Reproduce from the repository root

```sh
python3 tools/apply_sign_rewrite_9e1.py --check
python3 docs/curriculum/app-migration/implementation-evidence/9E1/validate_package.py
python3 -m unittest discover -s tools -p 'test_*.py' -v
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' \
  ./gradlew :composeApp:desktopTest --offline --no-daemon
python3 docs/curriculum/app-migration/implementation-evidence/9E1/verify_batch.py --check
```

Omitting `--check` from the rewrite tool writes the saved exact before/after transformation. It refuses to overwrite any other live-bank state. It does not apply 9E2 or later batches. The package validator checks these typed questions against all 1,123 destinations, 484 assets and the retained full source/alias package without activating a scored release.

Next: 9E2, separately requested.
