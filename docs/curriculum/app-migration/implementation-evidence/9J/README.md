# 9J — Complete question-package candidate

Later execution: [17 October joint 9J/9M checkpoint](../9J-followup/README.md) adds exhaustive held-candidate desktop delivery checks and two real-candidate simulator contexts. This original assembly receipt remains historical; release acceptance is still open.

Executed 9J1–9J4 in order on 16 October 2026. **This is a structurally valid held candidate, not an accepted release.** Existing sign-delivery holds remain binding.

| Step | Result | Evidence |
|---|---|---|
| 9J1 | Complete: all 1,000 IDs have exact mapped primary/related lessons, reference/source IDs and ordered URL-record references. All canonical targets resolve. | [Relationship parity](relationship-parity.json) |
| 9J2 | Candidate assembled; release acceptance blocked. All 1,000 IDs / 500 concepts accounted for: 336 retained, 626 rewritten, 38 replacement proposals. 384 accepted content records; 616 held. | [Eligibility audit](eligibility-audit.json), [package validation](package-validation.json) |
| 9J3 | Accepted candidate subset tested across lengths 1–70 and 20 fixed seeds per length, without reducing quotas. Release-pool acceptance depends on 9J2. | [Capacity report](capacity-report.json) |
| 9J4 | Complete candidate JSON/Kotlin parity, all key positions and both feedback modes checked. Release sign-off depends on 9J2. | [Compiled parity](compiled-parity.json), [shuffle report](shuffle-report.json) |

The existing `content/questions.json` and `Bank.kt` remain byte-for-byte unchanged. New typed authoring files are `content/assessment-questions.json`, `content/question-relationships.json`, `content/package-sources.json` and `content/content-manifest.json`. The generated `QuestionPackage9J.kt` companion exposes canonical relationships for every legacy question and a separate candidate assessment list. Existing 626 typed records are reused with exact mapped relationships; 336 retained records preserve every prompt, option, key and explanation. The 38 replacement records are proposed candidates with `replacement-candidate-r2`, remain held, and do not replace their live originals. Candidate generation checks all 626 changed live records against their per-ID 9E–9I acceptance receipts.

The manifest binds all candidate payloads, exact asset files, aliases, sources, semantic revisions and eligibility. Its identity is explicitly suffixed `-candidate-9j`; `candidateReleaseAccepted9J` is false. Structural validation runs under the existing non-release profile. The release validator rejects unaccepted questions. No normal app route or persisted history is switched to this candidate.

[Retained-content review](retained-review.json) carries the existing 7D full-question review and claim limits, not a new source-currency certification. [Source authority](source-authority.json) retains the original 9A1 authority and all other frozen identities; only the evolved question-bank hash is refreshed after exact per-ID receipt comparison. Historical 9A/9E–9I receipts are not rewritten.

The merged source payload adds the three exact frozen SIG16–18 compatibility URLs from 7E. Their dates remain unknown. The validator permits them only for unavailable legacy actions and rejects their use as teaching-source or external teaching-link evidence. This does not approve new artwork, legal currency or missing sign entries.

The accepted subset has 384 questions / 192 concepts, with category concept counts 45 vehicle, 26 environment, 45 safety, 47 rules and 29 personal. At length 70 the quotas remain 7/5/16/32/5 plus five random picks. Exhaustive length checks exposed floating-point tie drift in the old largest-remainder calculation (for example at length 14). Allocation now uses integer division and exact integer remainders with the original category-order tie-break. No category quota is weakened.

Compiled-object parity independently serialises every actual Kotlin assessment field and compares a SHA-256 digest against canonical JSON, covering prompts, images, option identities, feedback, relationships, source references, revisions, reviews and holds. It also checks the compiled manifest digest. Shuffling covers 80 fixed seeds for every candidate and all four key positions; both feedback modes are exercised for 384 accepted questions, and scored sessions reject all 616 held candidates.

Reproduce and validate:

```sh
python3 tools/assemble_question_package_9j.py --check
python3 tools/apply_fuel_corrections_9i.py --check
python3 tools/apply_load_clarifications_9h.py --check
python3 tools/apply_scenario_corrections_9g.py --check
python3 tools/check_sign_delivery.py --check
python3 -m unittest discover -s tools -p 'test_*.py'
./gradlew :composeApp:desktopTest --offline --no-daemon
```

The 9J desktop tests refresh the capacity, compiled-parity and shuffle reports. Source generation itself is deterministic. Resolving 9F/9L/9O delivery and route holds and rerunning release validation is required before 9J can be accepted as a release. The user's simulator choice remains in effect; physical iOS availability is not a new blocker here.

Final validation: **137 Python tests and 47 desktop tests passed**. [Verification receipt](verification.json) · [Saved test results](tests/) · [Review](review.md).
