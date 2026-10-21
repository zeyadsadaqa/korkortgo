# 10K5 — normal iOS device framework and existing physical exclusion

Executed21October2026. The normal iosArm64 framework and resource-aggregation build succeeds without -PreferenceProof. Unchanged compile/link/resource outputs are reused as explicitly shown by Gradle's up-to-date results; configuration executes. The current framework archive is ARM64 and all2,837 inspected object build-platform records are Mach-O platform2(iOS device),not platform7(simulator). inspect_device.py records its binary hash and metadata.

The device resource aggregation passes490 byte checks:484 artwork bindings/419 physical files,four fonts and two complete licences. This is build/packaging verification,not a physical runtime claim.

The unchanged content/delivery-targets.json policy records the user's simulator-only iOS choice. Signing,physical installation,runtime,VoiceOver listening and physical legibility remain excluded and unperformed. They are not described as passed,and no new exclusion or scope reduction is invented. Other target matrix failures do not invalidate this scoped normal device build/resource observation; overallT10 remains open.
