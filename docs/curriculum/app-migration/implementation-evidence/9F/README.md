# 9F1–9F19 — delivery review and prerequisites

All 19 code tasks have been reviewed. **Delivery acceptance remains open; no replacement is activated.** The user explicitly selected iOS simulator instead of a physical iPhone on 16 October 2026. Physical-device absence is therefore not a blocker for this run. Simulator captures are not physical-device or VoiceOver evidence.

Implemented the required canonical resolver, 1,921 frozen legacy aliases, session exit/return guards (9K1–9K4), approved reference detail and shared accessible viewer components (9L9–9L10). Full application route activation remains 9L14. Three frozen legacy signal URLs live in a separately identified compatibility source supplement; release source-authority integration remains 9J. No source currency is inferred.

The renderer verifies original resource hashes and decodes the 18 retained PDFs into exact vector paths with original clips, colours and strokes. X8 uses its original PNG. No artwork was thickened, recoloured or substituted. All 18 independent PDF/Compose geometry comparisons pass; antialiasing differences are recorded in [vector fidelity](vector-fidelity.json). An actual scrolling-card failure was fixed; the regression requires painted artwork at 105px, not merely a semantic image node.

The 38 exact proposed replacements were checked against their frozen originals, four alternatives, authored keys/feedback, paired distractors and accepted neutral descriptions. Their original question records remain unchanged. Both random selection and direct sessions now exclude all 38 delivery-held legacy IDs; the 578 earlier held rewrites remain excluded too. This leaves 384 legacy eligible rows, not a newly accepted release package.

## Evidence and limits

- [Per-code summary](delivery-summary.json): 19 reviews, 38 unchanged questions, 38 exact target-image occurrences; 95 image occurrences across complete candidate contexts.
- [Android](android/complete.json): 76 native window captures, all 19 codes on light/dark surfaces at text scale 1.0/1.6, 180dp stem and 105dp option. Both exact resources must load before capture. [Build identity](android/capture-build.json), [analytical contact sheets](android-review/).
- [iOS simulator](ios-simulator/captures.json): all 19 codes, light/default text, neutral descriptions exposed. X8 additionally exercised native modal open, 150% zoom, Reset and Close to the same fixture. Screenshots include the Simulator window and are rescaled, not native-pixel physical-device proof.
- [Wasm](wasm/captures.json): all 19 codes, light/default text. Browser captures follow a render-frame check. This is not a complete surface/text/reader matrix.
- [Tests](tests/): 119 Python and 39 desktop tests pass; Android, Wasm and iOS simulator framework builds pass; Xcode simulator app builds. Desktop scene tests cover neutral semantics, keyboard zoom/pan/reset/close, pending-choice preservation, focus restoration, minimum control bounds and actual painted pixels. Headless viewer-core tests do not certify native-modal readers.
- [Verification receipt](verification.json) and [replay verifier](verify_delivery_work.py).

Twelve smallest previews retain faint details: S5, S6, S7, S11, S12, S13, T1, T2, T6, T8, T22 and X8. They require an official legible exact-code rendition or a separately approved presentation/content-ID decision. All codes still need representative platform reader checks and complete per-question zoom/return/focus and surface/text evidence. Existing implementation tests and screenshots do not replace that acceptance. The explicit decision is to retain IDs and scoring holds; no proposed replacement is applied before its proof passes.

## Reproduction

Run `python3 tools/build_navigation.py --check`, `python3 tools/prepare_delivery_fixtures.py --check` and `python3 tools/check_sign_delivery.py --check`. Install the pinned dependency from `tools/requirements-vector-decoder.txt` into an isolated environment, then run `python3 tools/extract_official_vectors.py --check`. Run `python3 -m unittest discover -s tools` and `./gradlew :composeApp:desktopTest --offline --no-daemon` with Java 17.

Verification binaries only: build `:composeApp:assembleDebug`, `:composeApp:wasmJsBrowserDevelopmentExecutableDistribution`, `:composeApp:linkDebugFrameworkIosSimulatorArm64` and `:composeApp:iosSimulatorArm64AggregateResources` with `-PreferenceProof`. Android uses the separate `se.korkort.study.verification` package and `DeliveryProofActivity`; `captureAll=true` writes the 76 captures inside its own files directory. The Wasm fixture accepts `#CODE/delivery` (optional `/dark/1.6`). iOS fixture uses `PROOF_CODE` and `PROOF_MODE`; bundle the current aggregated Compose resources in `compose-resources/composeResources`. The ordinary app excludes these fixture sources; fixture release/publish tasks are forbidden.

Earlier 9D/9E acceptance receipts remain historical and untouched. This work changes runtime/navigation and records a later execution context; it does not re-certify an earlier fingerprint or declare a release manifest accepted.
