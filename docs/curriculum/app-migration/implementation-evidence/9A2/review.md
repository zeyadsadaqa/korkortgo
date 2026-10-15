# 9A2 — Typed content contract execution review

**Executed:** 15 October 2026. **Status:** Complete. **Authorization:** “ok next” after completed 9A1 selects the next planned task, 9A2.

[Schema and field mapping](content-contract.md) · [Verification results](verification.json) · [Scope/evidence checker](verify_contract.py) · [Incoming baseline](../9A1/input-baseline.json)

## Changes

Added the standard-library common Kotlin contract in [Curriculum.kt](../../../../../composeApp/src/commonMain/kotlin/se/korkort/Curriculum.kt) and an appended assessment section in [Quiz.kt](../../../../../composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt). The models cover canonical IDs, full structured teaching/answer blocks, exact source scopes/evidence/dates, sign/caption/asset/reuse bindings, manifest identity, legacy aliases/tombstones, authored option IDs, semantic revisions, eligibility and versioned option-order snapshots. The existing Quiz.kt implementation prefix is byte-identical to 9A1; generated Bank.kt, the live question JSON and current session/selection behaviour are unchanged.

Documented exact JSON file roots, type discriminators, field mappings, canonical manifest hashing without self-reference, source-to-block provenance and the explicit refinement of 7B planning fields. The schema requires retained original titles/order/content and separates question feedback from pre-answer image semantics. It keeps app-content identity separate from the approved PDF and app binary versions.

Added [CurriculumContractTest.kt](../../../../../composeApp/src/commonTest/kotlin/se/korkort/CurriculumContractTest.kt) with five meaningful checks:

- Reject duplicate/unknown option IDs and incomplete feedback while permitting equal learner labels.
- Reject accepted questions with missing content review, open holds, removed disposition or unreviewed stem/distractor images.
- Preserve revision/package/option-order snapshots and reject invalid permutations without consulting revised bank order.
- Represent deliberate-reveal answers separately from visible knowledge-check body blocks.
- Preserve rectangular table structure and distinct source scopes/unknown date kinds.

These are local model tests, not proof that future reader or assistive-technology output hides answers. Actual content acceptance, neutrality review, conditional delivery proof, rendering and platform behaviour remain assigned later work.

## Verification performed

Before edits, ran:

```sh
python3 docs/curriculum/app-migration/implementation-evidence/9A1/verify_inputs.py --check
```

Result: exit 0; all 1,174 retained bindings match, all 21 readiness checks pass and the saved snapshot matches exactly. This confirms the incoming package before intentional implementation changes.

Built the final models and ran common tests on desktop with the installed JDK 17:

```sh
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest --offline --no-daemon
```

Result: **BUILD SUCCESSFUL; 11 tests, zero failures/errors/skips**: five new contract tests and all six existing quiz tests. The final build took 15 seconds. Retained the exact JUnit reports as [contract results](TEST-se.korkort.CurriculumContractTest.xml) and [quiz regression results](TEST-se.korkort.QuizTest.xml). No new dependency or Gradle configuration was needed.

The first sandboxed attempt stopped before Gradle could acquire its existing cache lock. After cache access was granted, the Android Studio JDK 25 attempt stopped during build setup (`25.0.4`); switching to the installed JDK 17 produced successful builds. These setup attempts did not run the tests and are not reported as test results.

Ran the local scope/evidence verification:

```sh
python3 docs/curriculum/app-migration/implementation-evidence/9A2/verify_contract.py
```

It compares current inputs with the frozen 9A1 snapshot, allows only the authorised Quiz.kt extension and execution-plan record, checks the old Quiz.kt prefix hash, limits new source files to the declared model/test files, checks retained test XML, validates local document links and writes verification.json. All other frozen source, question, manuscript, production correction, asset, design/approval and audit identities remain unchanged. The evidence checker does not rebuild or overwrite any earlier audit.

Checked `git diff --check` and the final file inventory. Existing user PDF changes remain preserved. Plan/progress records now show 9A2 complete and 9A3 separately requested.

## Completion and boundary

The typed contract can represent the complete approved 7B–7E content/assessment requirements. Both file roots and manifest hashing are documented, constructor checks cover local structural invariants, and the unchanged live quiz regression suite passes. No blocking contract issue remains.

9A1 expected hashes are preserved as the pre-implementation record. This task saves intended before/after identities and records its changed/additional source files; future tasks use the accepted output chain instead of rewriting that original baseline. No runtime JSON loader, populated curriculum, bank rewrite, source refresh, new UI, persistence or history feature was introduced.

**Next:** 9A3 — implement deterministic generation and validation, only when separately requested. Full cross-package validation, import parity, per-item acceptance, device/platform checks and step 10 remain future work.
