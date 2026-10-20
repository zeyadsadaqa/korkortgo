# 10C sequence / T02 review — 20 October 2026

The requested sequence was executed through its available verification work. **T02 remains open.** No accepted content, runtime source, historical receipt or production source date changed.

| Task | Executed result | Acceptance still required |
| --- | --- | --- |
| 10C1 | 19,115/19,121 checks pass; exact 404 URL, 116 destination, 519 compiled reference and 8,166 question/option source-use bindings resolve | Six publisher/jurisdiction/type classification corrections and retests |
| 10C2 | 29 selected claim checks and all three 9N briefs: 22 scoped supports, six confirmed classification defects, one blocked handbook currency check | Fresh direct Volvo handbook inspection or explicit bounded disposition; unchecked claims retain original dates |
| 10C3 | 18 shared desktop matrix passes, plus missing-source recovery, actual LearningRoute reader return/focus and answer-review component identity/focus | 54 native/browser matrix cases and fresh 10K production-owner/platform observations |

[Source runtime results](source-runtime-results.json) map the frozen six classes × four targets × three states to [72 executable cases](source-cases.json). Every case carries its exact URL, frozen oracle, available lesson/question origins and action/check sequence. Desktop evidence uses actual shared Compose/Skia components at 1280×2048 with injected callbacks; this follows the approved desktop dispatch policy. It does not prove an OS browser launched, an external page loaded, or offline/network failure was observed. The successful callback receives the original exact URL; rejected dispatch shows a polite recovery message, preserves return controls and clears on successful retry.

Fresh `SourceRuntimeVerification10CTest` passed. Detail tests assert title/publisher/classification note, every original evidence date (including “Not recorded”), scope, finding and limitations. The missing-source control recovers without inventing a source. The actual `LearningRoute` opens the M01-L01 source and restores its focused source row after rejected dispatch. Actual `LearningAnswerReview` plus `SourceDetail`, hosted by a verification owner, preserve `reaction-20-0.5` revision, prompt/options/explanation and score and restore source focus. That component test does not claim production `CurriculumApp` owner coverage. Native URI errors, review filter/row and platform return behaviour remain in the 10K handoff.

Eight unique captures retain nine observed renders: the research and editorial-arithmetic failure captures were byte-identical and share `captures/research-failure.png`. [Cleanup record](cleanup.json) retains the removed capture hash and mapping. The captures cover the six class failures, missing-source recovery, reader focus and review focus. Visual inspection of the manufacturer failure, reader return and answer-review return captures confirms the recovery controls and focused source row; automated semantics cover the remaining cases. These are shared desktop captures, not device screenshots or assistive listening evidence.

[Defect register](defects.json) continues 10B14 without altering its historical results. Six open P2 metadata defects block their required source-record cases; one currency blocker and the 10K runtime dependency are recorded separately. 10L1 must choose the bounded source-classification correction, regenerate derived metadata through the accepted pipeline and invalidate/retest the affected evidence before closure. Passing 10B parity describes the current unchanged candidate; it does not excuse the independently discovered classifications.

Reproduce from repository root:

```sh
python3 docs/curriculum/app-migration/verification-evidence/10C1/audit_sources.py
python3 docs/curriculum/app-migration/verification-evidence/10C2/record_review.py
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest --offline --no-daemon --init-script docs/curriculum/app-migration/verification-evidence/10C3/jvm-test-init.gradle --tests se.korkort.SourceRuntimeVerification10CTest
python3 docs/curriculum/app-migration/verification-evidence/10C3/reconcile_runtime.py
python3 docs/curriculum/app-migration/verification-evidence/10A1/verify_baseline.py --check
```

The first command intentionally exits 1 until the six product metadata defects are fixed. `record_review.py` records the dated curated primary-content review and recomputes coverage/math; it is not an automated fresh source verifier. `probe_primary.py` makes a separate new network observation, which requires another content review. Do not overwrite these historical observations to claim a different candidate passed. No 10D–10M work is claimed by this run.
