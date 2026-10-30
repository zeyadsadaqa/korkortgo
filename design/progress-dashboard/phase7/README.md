# Phase 7 data controls design review

30 October 2026. Approved by the user on 30 October 2026; the approved flows are implemented. Generated with the built-in image generation tool, matching the selected [v2 design](../preview-v2.png).

- [Data controls preview](preview-data-v1.png)
- [Exact generation prompt](prompt-data-v1.md)
- [Implementation and release gates](../../../docs/plans/progress-release-checklist.md)

The six panels cover Your data, export, validated import review, invalid import, reset confirmation and reset completion. Figures are illustrative. No learner data was exported, imported, deleted or reset. The designs were subsequently approved and implemented; see [implementation and verification](../../../docs/plans/evidence/progress-integration/README.md).

## Interaction contract

- Enter Your data from Home below the main dashboard actions. Keep it inside the Home tab. Use one shared Back control; duplicate back/wordmark rows in the generated export/import panels are illustrative artifacts, not an additional navigation requirement.
- Export opens the platform's save/share flow and never changes progress. Cancellation is neutral. Announce success only when the platform confirms the operation; when it confirms only a handoff/download request, describe that state accurately.
- Import first picks and validates a file. Only a checked file reaches the review page. Show record counts and the replacement scope, offer an export of current progress, and require the explicit Replace progress action. Cancel or validation failure leaves current records unchanged. Import is replacement, not synchronization or merging.
- Reset opens the consequence screen, offers export, and requires the explicit Reset progress action. Clear reading, history, answers, unfinished sessions and derived learner state together. Keep curriculum, question assets and externally exported files. Show the empty success state only after commit.
- Failures use the established contained retry treatment and retain current data. Busy controls prevent duplicate mutation. Export/import/reset outcomes must be announced accessibly and keyboard focus returned to the relevant action.
- Large text must wrap and scroll while preserving accessible action targets. The generated confirmation panel is a visual proposal, not proof of 160–200% runtime accessibility. The current light-theme design does not establish dark-mode acceptance.

## Status

Phase 5 Exercise, phase 6 Home and the approved phase-7 data controls are implemented. Phase 7's full release gate remains open until the outstanding platform/accessibility matrix passes. Approval of these designs is not permission to reset an actual learner's current data during development.
