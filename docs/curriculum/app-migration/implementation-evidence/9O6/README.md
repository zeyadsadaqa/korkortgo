# 9O6 — iOS ARM64 build checks and physical-runtime scope

The [scope record](scope.json) binds the unchanged 9O2 accepted manifest and exact [delivery policy](../../../../../content/delivery-targets.json). On 16 October the user selected simulator testing instead of a physical iPhone. The current request to execute 9O6 does not explicitly reverse that decision. Accordingly this task verifies the configured `iosArm64` build/resources and records physical runtime checks as excluded, never passed. The accepted policy is not modified.

**Result — 20 October 2026:** Build/resource checks pass. The normal ARM64 static framework links for the iOS device platform; all 484 generated resource bindings, four fonts and both licences match. Physical installation/runtime/accessibility are not executed and remain excluded by the existing accepted simulator-only policy. This is not a physical-device acceptance pass.

## Reproduction

```sh
JAVA_HOME=/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home ./gradlew :composeApp:linkDebugFrameworkIosArm64 --offline --no-daemon --max-workers=1 -Pkotlin.compiler.execution.strategy=in-process '-Dorg.gradle.jvmargs=-Xmx6g -Dfile.encoding=UTF-8'
JAVA_HOME=/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home ./gradlew :composeApp:iosArm64AggregateResources --offline --no-daemon --max-workers=1
```

`device-framework-build.txt` and `device-resources-build.txt` retain the exact build outcomes. `device-package.json` fingerprints the generated normal framework executable, its Mach-O architecture/platform metadata, framework plist and resource results. `resource-parity.json` compares each of the 484 logical artwork bindings plus all four fonts and both licence files against the generated ARM64 resource bundle. This bundle is a build output; it is not an installed/signed iPhone app package.

Toolchain: Microsoft OpenJDK 17.0.16, Gradle 8.14.3, Kotlin 2.2.20, Compose 1.9.3 and Xcode 26.6 (17F113). Builds omit `-PreferenceProof`; no verification fixture is selected for this device framework. `results.json` records outcomes, excluded runtime checks, exact candidate and retained artifact fingerprints.

## Acceptance boundary

| Check | Treatment |
| --- | --- |
| Configured normal `iosArm64` framework | Build outcome and binary metadata recorded directly. |
| Device-target assembled resources | Exact bytes checked against accepted payload and shared font/licence sources. |
| Physical installation, signing, offline teaching/assets and library/reader/quiz/source/reference/recovery flows | Not executed; outside existing simulator-only runtime authorization. No success inferred from compilation or resource parity. |
| Physical-device accessibility, VoiceOver and image legibility | Not executed; not replaced by simulator audits or shared tests. |
| Simulator runtime | Separately verified in [9O5](../9O5/README.md): six native tests, both production feedback modes and four scoped description/trait audits. This remains simulator evidence only. |

The build/resource portion can be closed within the accepted simulator-only policy. Physical-device validation remains unperformed and would need its own installation, runtime, accessibility and delivery evidence if physical-device support becomes an acceptance requirement later. It is not a current acceptance blocker under the bound policy, and it is not recorded as a physical-device pass. No signing changes, device provisioning, publication or step 10 execution is included. No app content or runtime behavior is changed.
