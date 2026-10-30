# Phase 4: navigation and Learning

Implemented 30 October 2026 using the selected [v2 preview](../../../../design/progress-dashboard/preview-v2.png). This phase covers navigation and Learning; the Exercise hub and Home dashboard remain phases 5 and 6.

## Delivered behavior

- Home / Learning / Exercise bottom navigation on compact windows; a navigation rail from 840dp. Both expose icons, text, selected state, and safe-area spacing.
- Each tab retains its current destination. Learning retains search, topic selection, chapter expansion, library scroll, reader positions, and source/reference routes. Exercise retains the current question, unconfirmed selection, review state, and scroll positions while changing tabs.
- Android Back follows the active tab's internal route, then returns to Home from a tab root. Nested screens also expose a Back control; Escape follows the same route on keyboard platforms.
- Learning observes committed database records. Counts include only current teaching-lesson revisions; module reviews and old revisions do not count. Chapters show Not started, In progress, or Read. Lessons expose Read, Continue, or Not started.
- The first incomplete chapter expands on initial database load. Later expansion choices are retained. Search remains prominent; topic filters are available through an explicit control. Sources, signs, supporting documents and existing reader completion controls remain available.
- Android window, orientation and font configuration changes are handled without discarding the active Compose UI. Process restart restores persisted reading progress and the saved exercise; transient tab, search, navigation history and unconfirmed drafts are not process-persistent.

## Verification

The final build command is recorded in [build.txt](build.txt):

```sh
./gradlew :composeApp:desktopTest :progress-data:desktopTest :composeApp:assembleDebug :composeApp:compileKotlinIosArm64 :composeApp:compileKotlinIosSimulatorArm64 :composeApp:wasmJsBrowserDistribution --console=plain
```

95 application tests and 7 repository tests pass, with no failures or skips. New checks cover tab ownership, current-revision reading counts, source Back restoration, and navigation placement/click behavior at widths 320, 390, 840 and 1280dp with font scales 1.0 and 1.6. Existing application-flow tests now use the new tab labels and expect Learning to retain its related-reading destination when returning to that tab. Legacy fixture-only discard guards remain tested.

Android runtime checks used emulator-5554 and its existing synthetic progress profile; no learner database was cleared:

1. Restarting the updated APK restores **1 of 40 lessons read**, from the previously completed lesson, and the saved exercise with **1 of 10 answered**. See [Learning after restart](learning-after-restart.json).
2. Opened “Your route into driving,” switched Home → Learning, and returned to the same lesson. Reader restoration uses the persisted block position; pixel placement can change when the reader is remeasured. See [before](reader-before-tab-switch.json) and [after](reader-after-tab-switch.json). Android Back returned to the chapter list.
3. Resumed Question 2 of the saved end-feedback exercise, selected an answer without confirming, switched Home → Exercise, and verified the same question and checked draft. See [retained draft](exercise-draft-after-tab-switch.json). No new answer was published.
4. Rotated the active exercise to landscape: the rail appeared and Question 2 remained active. See [rotation hierarchy](exercise-after-rotation.json).
5. Visually checked the final Learning layout in portrait, landscape, and at 160% text. Chapter titles wrap, the library scrolls independently, and all three navigation labels remain visible. Display settings were restored afterward.

Screenshots below contain synthetic test progress:

- [Phone](learning-phone.png)
- [160% text](learning-large-text.png)
- [Wide window / rail](learning-wide.png)

Android runtime and desktop Compose tests were exercised in this phase. iOS device/simulator and Wasm production artifacts compile; iOS runtime, browser navigation, screen-reader journeys, 200% text and dark-mode acceptance were not newly exercised here. Existing browser storage qualifications remain in the phase-1/phase-3 reports. The app retains its established light theme.
