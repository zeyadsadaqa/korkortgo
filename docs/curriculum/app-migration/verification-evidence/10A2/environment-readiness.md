# 10A2 — Environment readiness

**20 October 2026:** Required toolchains and targets are available or bootable. This is a readiness inventory, not a new build/runtime pass.

| Target | Observed readiness | Required follow-up |
|---|---|---|
| Common/JVM | Python 3.14.7, Microsoft JDK 17.0.16, Gradle 8.14.3; macOS 26.3 ARM64 | Run fresh suites/generation checks in 10K1; cached historical test output is not fresh evidence |
| Android | API 36 SDK/build tools installed; `emulator-5554` running; 1280×2856 physical pixels, density override 408 dpi | Build/install normal APK, record logical bounds, run native/runtime cases and restore settings |
| Android assistive | TalkBack package installed; enabled-accessibility-services is `null` | Fresh representative listening/navigation observation is required; enable temporarily and restore. Native node assertions alone do not pass it |
| iOS simulator | Xcode 26.6, iOS simulator SDK 26.5; original iPhone 17 `F6E93C4B-958D-4CBB-B95E-537B4FB8070C` available, shutdown | Boot the existing simulator during 10K4; build/test normal and labelled proof outputs; no erase/replacement needed |
| iOS device target | iOS 26.5 SDK and configured `iosArm64` framework available | Build/resources required; signing/install/physical runtime/VoiceOver excluded by the existing simulator-only policy |
| Desktop | Existing JVM/Compose library/test harness; no standalone app launcher | JAR/resources, real raster/keyboard/semantics tests required; native window/OS browser/VoiceOver bridge excluded |
| Web | In-app browser provider available with zero tabs; Gradle Wasm target configured | Fresh normal distribution/local host/browser run required; no cold-offline, cross-engine or speech-listening claim |

The initial sandbox queries could not reach CoreSimulator or start the ADB service. Host-permitted read-only retries succeeded. Both attempts remain in [environment-commands.json](environment-commands.json), with raw logs. No device application was installed/launched, no iOS simulator booted, no connectivity/service preference changed and no browser tab opened for these checks. ADB service access was established by the inventory query.

The [54-row scope matrix](scope-matrix.json) distinguishes 37 required future checks from 17 excluded/non-surface rows. All future required checks remain `not_run`. Four absent-store contracts remain `conditional_future_scope`. If later execution reveals unavailable required functionality, open a blocker rather than silently excluding it.

## Viewport interpretation

The approved [design specification](../../../app-design-spec.md) explicitly calls its approximately 390/1280-wide preview frames conceptual, not minimum supported widths. The phrase “smallest approved size” in the verification plan therefore refers to approved component constraints and actual narrow-window behaviour, not a newly invented 390 px minimum. Retain the 390×844 logical replay baseline; add a 320-wide reflow diagnostic and the desktop-wide view, recording actual native sizes separately. Verify the approved artwork frame height of at least 220 dp, equal options, aspect ratio and 100%/160% text without widening the viewport to hide overflow. This clarification changes no design or support policy.
