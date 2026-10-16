# 9E — all 12 sign rewrite batches

All 578 assigned sign questions are rewritten. The remaining 422 questions are unchanged from the pre-9E1 bank. This execution completes 9E2–9E12 (528 new rewrites) and preserves 9E1 exactly.

Every rewrite retains authored question/concept/option identity, uses semantic revision `rewrite-r2`, and applies exact approved 7D prompts, English labels, explanations and keys. The 289 concept pairs retain consistent distractors. Across all 12 batches, 128 question records include approved distractor changes and 1,445 image occurrences bind exact bundled art to accepted 9D physical descriptions. Original official art, sources and curriculum are unchanged.

**All 578 rewritten questions remain held from scoring.** Delivery at intended sizes, zoom, light/dark and representative accessibility navigation plus assessment route integration still require 9L/9O acceptance. The separate 38 replacement questions remain 9F work. No new visual design or device acceptance is claimed.

The complete metadata exceeded the JVM constant-pool limit when emitted in Bank.kt. Generated assessment functions now live in `SignRewrite9E1.kt` through `SignRewrite9E12.kt`; Bank.kt retains its legacy facade and calls those functions. Existing selection/direct-session eligibility guards keep every rewritten question out of scored legacy/new sessions.

Each 9E batch has its own typed payload, content-review record, per-ID before/after acceptance and readable diff. The transformer reconstructs batches 3–12 in memory from the exact retained 9E2 input and output. This avoids duplicating every cumulative bank in evidence. Saved historical 9E1 evidence remains byte-exact; its live-bank command describes that historical state. Use the combined verifier for the current bank.

## Reproduce from the repository root

```sh
python3 tools/apply_sign_rewrites_9e.py --check
python3 docs/curriculum/app-migration/implementation-evidence/9E/validate_package.py
python3 -m unittest discover -s tools -p 'test_*.py' -v
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' \
  ./gradlew :composeApp:desktopTest --offline --no-daemon
python3 docs/curriculum/app-migration/implementation-evidence/9E/verify_all.py --check
```

Validation covers all 1,123 destinations, 578 typed questions and 484 assets. All 113 Python tests and 23 Kotlin/desktop tests pass, including actual Compose semantics/keyboard checks and scoring exclusion for all rewritten questions.

[Package validation](package-validation.json) · [Verification and fingerprints](verification.json) · [Python tests](python-tests.txt) · [Desktop tests](gradle-tests.txt).

The rewrite command without `--check` accepts only the exact 9E2/final live-bank states and refuses unrelated edits. Prior 9E tools describe their bounded historical transformations and must not be rerun against the completed live bank.
