# Phase 5 Exercise hub review

30 October 2026. Pending explicit design approval. Generated with the built-in image generation tool, using the selected [v2 board](../preview-v2.png) as the style reference. The existing [phase-3 resume and save-failure controls](../phase3/preview-v1.png) remain the selected interaction design.

## Previews

- [Setup, targeted small pool, history and first use](preview-flows-v1.png) · [generation and refinement prompts](prompt-flows-v1.md)
- [All questions answered, empty review pool with large text, loading and load failure](preview-states-v1.png) · [generation prompt](prompt-states-v1.md)

All values and dates are illustrative. The boards show independent learner states. The example with three eligible questions and two learning points is hypothetical, not a measurement of the current accepted bank. The implementation must derive actual capacities. Preview geometry is a design reference; layout, accessibility, scrolling and text scaling require runtime verification.

The all-answered state's unanswered row is informational, without a start action; the generated chevron does not authorize starting an empty pool. Empty review actions must also reflect whether unanswered questions actually remain. Loading must not show fake zero counts. Ended exercises show confirmed-answer counts without a completed score. The large-text example is a layout direction rather than evidence of runtime font scaling.

## Implementation after approval

1. Project current, published question progress into coverage and targeted pools. Deferred answers remain excluded until completion. Authenticate the full accepted package before deriving a pool; never pass a filtered bank through the full-bank validator.
2. Add mixed, unanswered and review modes, with chapter/category selection backed by accepted question relationships. Preserve the existing mixed distribution. Targeted modes use their own capacity checks, one question per distinct concept, and a maximum of the smaller of 70 or available concepts. Prefer unanswered variants within a concept across sessions so every question remains reachable.
3. Persist mode and filter identity alongside exact session snapshots. Resume with the same selection, option order and feedback rules. Existing sessions without new labels retain an honest legacy/mixed label. Replacing an active exercise continues to require finishing or explicitly ending it.
4. Connect the approved hub to actual summary data, resume state, setup and recent history. Provide paginated history, dates, completed scores and unscored ended entries. Reopen completed snapshots through the existing results, explanation and source navigation; unavailable historical content receives an honest unavailable state.
5. Verify empty and small pools, stale revisions, mixed selection, repeated question coverage, concept deduplication, deferred reveal boundaries, history restoration and cross-platform builds. Exercise Android navigation, font scaling and restart behavior; report remaining platform runtime gaps explicitly.

No application source is changed in this preview stage. Home dashboard work remains phase 6. The established light theme remains in scope; dark-mode implementation is not included in phase 5.
