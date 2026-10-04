# Verification · 26 September 2026

- Shared JVM tests: 6 passed, 0 failures. Includes 700 seeded samples covering every allowed test length, concept uniqueness, exact full-test allocation, answer shuffling, content integrity and session transitions.
- Android debug APK: assembled successfully.
- iOS: complete SwiftUI host and Kotlin framework built successfully for ARM64 iOS Simulator with Xcode. Physical-device signing and native on-device interaction have not been tested.
- Web: production WebAssembly distribution built successfully. Browser interaction verified setup, the exact 70-question allocation, one-question practice, incorrect-answer explanations for all four options, score calculation, another-test navigation, and withholding correctness in end-of-test mode.
- Responsive UI inspected at desktop width and 390px phone width. Official sign images loaded in questions.

Content includes 1,000 question records across 500 distinct concepts. Sign recognition in two directions and numeric scenario variants contribute to the total. See `content/quality-report.json` for the breakdown. This validation checks software and structural content quality; it is not an independent expert review of every theory statement.
