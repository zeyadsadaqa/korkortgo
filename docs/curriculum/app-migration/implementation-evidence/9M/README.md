# 9M — transient session, review and setup state

17 October 2026. **9M1–9M2 model/component implementation and checks pass. 9M3 has a complete 22-contract report, but final release verification awaits accepted 9J content; candidate checks proceed alongside delivery acceptance.** The candidate still has 384 accepted and 616 held questions. Its production start is rejected; no hold, release gate or learner route was activated.

## 9M1 — session and review identity

`TransientQuizState` owns one same-process `PinnedPractice`. The existing `AssessmentSession` retains the full question/revision, content-package identity, authored option order, selection, correct key, feedback mode, index, finished flag and pinned score. No score or feedback consults the current bank during review.

A draft token includes session ID, question ID/revision, package identity and exact displayed option IDs. Selection alone does not confirm or reveal. Confirmation rejects stale/foreign tokens; advancing clears the draft. `PinnedAssessmentCard` keys the existing assessment/viewer component by that entire token. An actual Compose test reuses the same question and shuffle in a different attempt and verifies that the first attempt's unconfirmed radio selection disappears; the next confirmation carries the new session token and authored option ID.

Review retains All/Incorrect/Correct, filtered row and expanded question revisions for the same pinned attempt. Filtered rows map explicitly to original snapshot indices through `reviewSnapshotPosition()` / `reviewPresentation()`. An empty filter has no presentation or guessed question. Teaching/source visits and explicit return preserve the cursor, expansion and score. Explicit review question IDs are validated; new sessions clear review state.

All exits use the shared 9K guard. Related teaching is denied before permitted reveal; other unfinished exits retain the exact pending request for confirmation. Cancellation preserves draft/answers/context. Discard is bound to the full original pinned attempt, clears it atomically and never discards replacement answers. Source effects remain withheld until approval and can be consumed once using `takeSourceToOpen()`. A stale session route cannot silently abandon a different valid attempt. In-place zoom preserves the attempt.

## 9M2 — setup, recovery and restart

Fresh state retains the audited defaults: Home, 70 questions, IMMEDIATE feedback, empty library query, All categories and no session/result. Valid same-process count/feedback preferences survive missing-context recovery. Invalid counts recover to 70. Missing results/review never manufacture a session, score or question; `showSetup()` is deliberate recovery and does not start a test. An unfinished valid attempt still requires the shared discard guard before setup.

`practiceStartCheck()` validates 1–70, accepted question IDs, duplicate IDs, per-category distinct-concept quotas and total concept capacity including residual random slots. It does not lower quotas or silently shorten the test. Concepts spanning categories are rejected because the existing category-first selector could otherwise consume later quotas for some seeds. This does not change the actual candidate's category allocation or eligibility.

The production `startPractice()` checks the release decision. `candidatePracticeBank9M` is bound to the actual 9J identity/questions/release flag, which is false. The internal `startPracticeFixture()` is used only by tests, still enforces eligibility/capacity and is not wired to an app route. Candidate-backed tests exercise every length 1–70, complete each attempt and verify original snapshot identity and scores. No held question enters a session.

Session IDs come from an in-memory attempt serial that survives same-process discard/new-start transitions, preventing an old token from matching a reused question/order. It is not an attempt-history store. A real process restart recreates state and loses transient data as before; the reset helper models that boundary. There is no saved-state, database, cloud sync, bookmark, completion or legacy-answer import API.

## 9M3 — exact contract coverage and remaining gate

[State contract results](state-contract-results.json) records all 22 frozen 7E fields, their original rules and named test evidence. Eighteen current transient contracts pass fixture/candidate checks; four future-store contracts remain explicitly conditional (bookmarks, completion, durable question history and storage schema). Existing snapshot tests preserve old outcomes when a separate revised bank is constructed; this does not introduce hot replacement, historical import or current-mastery transfer.

The report generator rejects missing/failed test cases, mismatched contract coverage and any claim that the current held candidate is an accepted release. Three negative/coverage tests exercise that reporting boundary. **9M3 is not complete against an accepted package.** After 9J release acceptance, rerun the state/selection/review/guard checks against that accepted package, review the candidate-specific gate assertions and update the report explicitly. Then finish 9L14 production wiring and integrated 9O acceptance.

## Integration scope

The existing `App.kt`, `QuizSession`, `AssessmentSession`, generated bank and content files remain unchanged. The new owner and keyed component are prerequisites for 9L14, not activation of a second learner flow. That integration must hoist library/setup/review state into the owner, render filtered snapshot positions, keep the quiz composed beneath discard confirmation, route all actions through the owner, and consume only approved source effects. Platform assistive and integrated UI acceptance remain 9O. iOS scope remains the user's selected simulator.

Earlier 9J/9K/9L receipts remain historical checkpoints; they have not been regenerated as new approvals merely because the plan advanced.

## Reproduce

```sh
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest :composeApp:compileDebugKotlinAndroid :composeApp:compileKotlinIosSimulatorArm64 :composeApp:compileKotlinWasmJs --offline --no-daemon
python3 -m unittest discover -s tools -p 'test_*.py'
python3 tools/verify_transient_state_9m.py
python3 tools/verify_transient_state_9m.py --check
```

Saved test logs/XML and the verification receipt record this execution. The report can also be checked against the saved test directory with `--reports docs/curriculum/app-migration/implementation-evidence/9M/tests`.

## Final validation

**144 Python tests and 78 desktop tests pass**, including seven new common state tests, one candidate-backed all-size lifecycle test and one actual Compose session-key reset test. Android debug, iOS simulator and WebAssembly compilation pass. Reader/navigation/9J reproduction checks pass. [Verification receipt](verification.json) · [All 22 state contracts](state-contract-results.json) · [Saved results](tests/).

Final release verification awaits accepted 9J content. The isolated delivery host and candidate checks can run before production activation. Compilation and fixture/candidate checks do not activate production, establish mobile assistive acceptance or clear any of the 616 delivery holds.

Saved build/test text logs have trailing whitespace and surplus final blank lines removed; diagnostic content is unchanged.
