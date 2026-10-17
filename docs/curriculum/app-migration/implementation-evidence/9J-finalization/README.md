# 9J finalization attempt and fresh 9M3 rerun

17 October 2026. Requested after the native reader/route checkpoint. **9J cannot yet be finalized as an accepted release.** A fresh direct release-profile validation rejects the exact current manifest: `release: unaccepted/retired questions or unapproved tombstones block release`. No acceptance decision, question replacement, release flag or production route was changed.

## Executed results

- Deterministic 9J assembly check, saved delivery-readiness check and sign-delivery check pass. The complete package still has 1,000 questions / 500 concepts: 384 accepted and 616 held.
- Structural validation passes. [Fresh release-validation result](package-validation.json) binds the exact manifest identity and records every held revision and its existing conditions.
- **41 focused desktop tests pass**: `QuestionPackage9JTest`, `TransientQuizStateTest`, `TransientPractice9MTest`, `NavigationTest`, `LearningViewsTest` and `LearningViewsSemanticsTest`. These rerun compiled package parity, quota/capacity/shuffle checks, all supported practice sizes, pinned selection/review state, reset/missing-context recovery, guarded exits and relevant reader route regressions. [Saved XML and build log](tests/).
- **All 22 frozen 7E contracts are recorded again**: 18 current transient checks pass; four future-store cases remain conditional. The fresh [9M3 result](state-contract-results.json) explicitly binds the same exact manifest. All three report-generator negative/coverage tests also pass. This is a completed candidate rerun, not final accepted-package verification.

Earlier 9J and 9M evidence is retained unchanged. This checkpoint does not reinterpret the representative native tests as complete per-ID delivery acceptance.

## Remaining prerequisites

The twelve faint assets affect 24 held questions. Their official exact-code rendition or presentation decision and actual-size delivery proof are unresolved. A changed presentation must receive an imagegen preview and explicit user approval before implementation. The other 592 held questions still need their delivery/acceptance conditions reconciled per question; they cannot be accepted solely because they do not use a known faint asset. The 38 approved replacement proposals still need their exact-code delivery conditions met before application; their original live questions remain unchanged.

After those conditions pass: apply the exact approved replacements, record per-ID acceptance, regenerate 9J, pass the release profile, and rerun the 9M state/selection/review/guard checks against the resulting accepted manifest. Only then can final 9M3 acceptance and 9L14 integration proceed. No physical-iPhone requirement is introduced; the user's iOS simulator scope is retained.

## Reproduce this checkpoint

```sh
python3 tools/assemble_question_package_9j.py --check
python3 tools/report_delivery_readiness_9j.py --check
python3 tools/check_sign_delivery.py --check
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest --tests 'se.korkort.QuestionPackage9JTest' --tests 'se.korkort.TransientQuizStateTest' --tests 'se.korkort.TransientPractice9MTest' --tests 'se.korkort.NavigationTest' --tests 'se.korkort.LearningViewsTest' --tests 'se.korkort.LearningViewsSemanticsTest' --offline --no-daemon
python3 -m unittest discover -s tools -p 'test_verify_transient_state_9m.py'
```

The fresh state report is `verify_transient_state_9m.generate(saved_tests_directory)` plus the exact manifest identity and file hash. It is saved here rather than overwriting the historical 9M report. Direct package validation uses `Validator(source_authority='docs/curriculum/app-migration/implementation-evidence/9J/source-authority.json').package(payloads, manifest, profile)` for both `fixture` and `release`, loading the non-asset payloads listed by the manifest. [Fingerprints](verification.json) bind current inputs and saved evidence. Text logs have trailing whitespace trimmed.
