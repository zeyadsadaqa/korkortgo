# 10L1–10L3 — DEF-10H-001 correction and retest

**This bounded 10L cycle passes. DEF-10H-001/P1 is closed for the corrected candidate; 18 other product findings and step 10 remain open.** The plan permits one issue or coherent batch per request. All 19 findings were triaged in [10L1](../../10L1/DEF-10H-001/defect-triage.md); this cycle selected the reading → B1 → sign catalogue → Return to reading failure.

The catalogue flag previously stayed active after the saved reading target was restored. Its branch therefore continued to render the catalogue. [10L2](../../10L2/DEF-10H-001/fix-review.md) clears that transient flag before the existing validated return. This changes no layout, design, content, legal claim, source date, accepted identity or feature. The new permanent UI regressions cover repeated actual annotated-link returns at 390/1280 widths and 100%/160% font scale, plus catalogue recovery without a reading origin.

| Verification | Actual result |
|---|---|
| New regression before correction | One test fails at the return-to-passage wait; failure retained |
| Selected shared reader/source/reference/navigation/session and accepted parity/state suites | 38 tests pass, no failures/errors/skips |
| Original historical 10H assertion | One test passes with the original expectation and new output location |
| Android native touch route | Retained 10K proof APK reproduces the failure; corrected proof APK opens B1 and restores the original passage |
| iOS native touch route | One XCTest passes; B1 touch, sign, catalogue and restored hittable passage; eight screenshots/trees retained |
| Browser actual input | Both labelled proof and normal production builds restore the linked passage through the catalogue |
| Normal configured builds | Android APK, desktop JAR, simulator framework/shared Korkort app, device ARM64 framework and production Wasm succeed |
| Packaged/served bytes | Eight normal/proof resource packages ×490 checks pass; installed normal iOS adds490; all783 served normal web files match |
| Restoration | Corrected normal native binaries installed and hashes checked; normal homes visually inspected; original off/Shutdown states restored, Simulator app quit, temporary tabs/servers closed |

[Retest results](retest-results.json), [updated defects](defects.json), [impact map](evidence-invalidation-map.json), [commands](commands.json) and [integrity](integrity-results.json) retain exact scope. Native tests use labelled proof hosts; the browser also executes the exact route from the normal production home/library. These are targeted route observations, not a full font/theme/assistive or 132-journey acceptance matrix. Physical iPhone runtime remains excluded/unperformed. No TalkBack/VoiceOver listening, desktop installer or cross-engine/offline browser claim is made.

The simulator computer-use swipe attempts did not move the reader; no product failure or pass is inferred from those attempts. Two native XCTest diagnostics positioned the passage using real slow swipes. Their passing driver results are not counted as route acceptance. The final separate XCTest uses the inspected inline B1 location relative to a stable native text frame and asserts the actual returned passage. Its exact temporary test method is retained; the original repository Swift test source is restored byte-for-byte. The first explicit simulator shutdown reported it was already Shutdown after the Simulator app quit; actual SDK/device/server cleanup state is verified in [cleanup results](cleanup-results.json).

The source/runtime fingerprint changes from `ac0d4e6b6b226b1f87f8d09521b4c334cccecd6cb7827c1bbd3889127402973c` to `5e102de5de291b5e976dd6a206bb8ba3b8b57800d4af2e5b7c7c9bf45269dabd`, accounting for exactly the route source and permanent regression test. Accepted content version and manifest identity remain unchanged. The original baseline checker correctly reports those two changed source files; it is preserved, not resealed around the fix. No historical receipt is rewritten. Older target executables/runtime observations remain historical; unchanged content/resource inputs remain useful input evidence. Fresh builds and the bounded route receipts apply to the new candidate.

T07 and T10 remain open for other required cases; this correction does not clear all dependent gates. The selected issue closes only after its original and affected bounded route checks pass. The other 18 findings, source-currency disposition, presentation/design requirements and uncompleted matrices remain explicit. No 10M final acceptance, commit, push or publication occurred during the verification run. Subsequent repository cleanup and sequential commits are separately authorized by the user.

Reconcile saved receipts with `python3 docs/curriculum/app-migration/verification-evidence/10L3/DEF-10H-001/finalize.py`, then run `verify_integrity.py` in this folder. These do not rerun the UI. A new platform run must use new log/result paths: `run.py` refuses to overwrite existing command logs. Build/test arguments and the isolated original-case harness are retained; temporary native-method injection must restore its source in a finally block as this run did.

Next separately requestable task: **10L1 for another bounded issue**, such as the nonvisual DEF-10F-001 identity rejection defect. A visual correction requires an imagegen preview and explicit approval first.

Repository cleanup retains all logical before/after captures while removing three byte-identical PNG copies. [Capture storage](capture-storage.json) resolves the original paths, including the unmodified native attachment manifest, to hash-checked retained files. [Cleanup record](repository-cleanup.json) records the space recovered.
