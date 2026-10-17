# Joint 9J delivery and 9M3 verification checkpoint

17 October 2026. Delivery and transient-state verification now proceed together. Production activation is not needed to collect candidate delivery evidence. Final 9J release acceptance and the accepted-package 9M3 rerun remain open.

## Completed in this checkpoint

- Added `candidate` mode to the build-time-only verification host. Pass a real question ID as `PROOF_CODE` / Android `code` / the first Wasm hash segment. It projects the actual candidate snapshot with fixed seed 9, without constructing a scored session, changing eligibility or exposing feedback. Ordinary builds exclude this host. The iOS host now accepts `PROOF_FONT_SCALE`.
- Rendered every one of the 616 held question revisions at 390×844 logical pixels in light/dark and 100%/160% text: **2,464 question runs and 6,160 image zoom/return checks**. Every image resource passed its existing exact-byte loader. Each question retained four radio options, hid answer feedback before confirmation, preserved a pending authored option through each modal, supported keyboard zoom/pan/reset/close, restored keyboard focus to its exact trigger and confirmed the selected authored ID. The test uses the actual generated candidate, not the earlier 38 replacement-only fixtures.
- Added a deterministic [readiness report](readiness.json), joined by exact question revision and package identity. It rejects incomplete/duplicate surface/text rows, foreign package/revisions and missing image checks. It keeps every scoring hold and native/route acceptance requirement explicit.
- Exercised two actual S5 candidate contexts on the iPhone 17 / iOS 26.5 simulator: recognise at dark/160% text and meaning at light/100%. [Native accessibility trees and window captures](ios-simulator/) show neutral descriptions, selected options, modal controls, 100%→150%→Reset and preserved selection after Close. No answer was confirmed. The native capture binary precedes the later verification-toolbar navigation fix; its host-source snapshot and binary identity are recorded separately. The final toolbar fix was compiled for all targets. The recognise case enlarged option A, an actual distractor; the meaning case enlarged the exact S5 stem.
- Re-ran the 9M transient contracts alongside delivery checks. The status is **awaiting final release verification**, rather than implying all candidate verification must wait for 9J. No preferences store, release activation or live question edit was added.

**Validation:** 144 Python tests and 78 desktop tests pass. The normal and verification build results are recorded separately in the receipt.

[Desktop delivery rows](desktop-delivery.json) · [Verification and fingerprints](verification.json) · [Saved test/build logs](tests/).

## Remaining acceptance, separated by cause

The twelve previously recorded faint assets occur in **24 held questions**. The other **592 held questions do not use those twelve assets**; they should proceed through native reader and complete question/route acceptance independently. The report identifies every affected slot, including distractors.

Desktop semantic actions are not native touch/reader evidence. The exhaustive test does not certify visual legibility, viewport visibility of every scrolled trigger, spoken reading order, native accessibility-focus return or all supported-platform combinations. Simulator AX output establishes exposed labels and selection state, not a VoiceOver listening run. The two simulator contexts do not constitute the full matrix. All 616 questions therefore retain their original holds.

The existing official-vector resolution requires larger full-width presentation for some codes; its book-size approval does not validate a 105dp option preview. The S5 modal capture still shows a thin outline. Preserve exact official paths, colour, crop and proportions. A changed presentation needs a preview and explicit approval under the user's design workflow; do not silently thicken or replace the art. The earlier 9F/9J receipts remain historical and untouched.

Next executable inputs/outputs:

1. Use the readiness rows and real-candidate host to collect supported-platform full-question and representative native reader evidence. Output per-question/native route receipts; do not depend on production activation.
2. For the 24 faint-asset questions, resolve an official legible exact-code rendition or prepare a narrowly scoped presentation preview for explicit approval. Output an approved asset/presentation decision followed by actual-size delivery proof. Preview approval alone does not clear a scoring hold.
3. Once per-ID holds actually pass, apply the exact approved replacement proposals, update acceptance records and regenerate 9J; verify unchanged retained fields, package parity, quotas and shuffling.
4. Repeat 9M3 against that accepted package, then activate 9L14 and run the integrated 9O checks. No release flag or eligibility is inferred from this checkpoint.

## Reproduction

```sh
./gradlew :composeApp:desktopTest --offline --no-daemon
python3 tools/report_delivery_readiness_9j.py --check
python3 tools/verify_transient_state_9m.py --check --reports docs/curriculum/app-migration/implementation-evidence/9M/tests
```

The delivery test writes `composeApp/build/verification/9J-followup/desktop-delivery.json`; copy a successful run into this evidence directory before intentionally refreshing the report. For a new report, use `--delivery` to identify the saved evidence file. Use Java 17. Build the candidate host with `-PreferenceProof`; release/publish remains prohibited. Example iOS environment: `PROOF_CODE=sign-meaning-S5`, `PROOF_MODE=candidate`, `PROOF_DARK=false`, `PROOF_FONT_SCALE=1`.

Saved build/test text logs have trailing whitespace and surplus final blank lines removed; diagnostic content is unchanged.
