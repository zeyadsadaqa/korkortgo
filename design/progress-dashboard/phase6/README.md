# Phase 6 Home dashboard review

30 October 2026. Pending explicit design approval. Generated with the built-in image generation tool. The selected [v2 Home layout](../preview-v2.png) remains the visual direction; this board supplements it without replacing the original.

- [Six Home states](preview-states-v1.png)
- [Exact generation prompt](prompt-states-v1.md)

The board shows first use, an unfinished exercise taking priority, a newly read chapter, all lessons read with stacked summary cards, loading, and load failure. Each panel is an independent illustrative scenario. The chapter-practice example assumes an accepted linked question pool; it must fall back to a valid recommendation when none exists. The large-text panel illustrates stacking and wrapping, not measured runtime accessibility.

## Current scope and dependency

Phases 1–4 are implemented. Phase 5 currently contains design previews and an implementation outline only. Phase 6 requires the targeted question pools and routes from phase 5 for chapter practice, review and unanswered recommendations. These previews do not imply that either phase's implementation is complete or approved. The existing mixed-practice setup alone cannot satisfy those shortcuts.

Keep the established light theme. Export/import/reset and full release acceptance remain phase 7; do not add placeholder data-management actions. Preserve the unrelated root README and migration edits.

## Implementation after design approval

1. Finish phase 5's approved Exercise implementation and expose typed destinations for mixed, chapter, category, unanswered and review setup. Start/resume must use the durable coordinator; Home must not create a second active exercise.
2. Build one coherent database-backed dashboard projection: current lesson progress, chapter completion, published question coverage, revisit count, valid active exercise, reading recency and eligible practice actions. Use a consistent transaction or versioned snapshot so cards and recommendations describe the same committed state.
3. Add the missing persisted reading/event ordering needed for reliable last-opened lesson, last-completed chapter and recommendation suppression. Current lesson rows contain completion and position but no opening timestamp; recording only a block is insufficient to identify the most recent lesson. Preserve existing progress with a migration if schema changes are needed. Reading-position writes must not repeatedly reorder genuine lesson-opening events.
4. Implement the deterministic next-step rules from the main plan: resume valid active exercise; continue most recently opened incomplete lesson; offer eligible practice for a newly completed chapter; offer an appropriate review set; start the first unread lesson; after all lessons are read, offer review, then unanswered, then mixed practice. Use stable ordering and record completed recommendation scope/revision so suggestions do not repeat immediately. No empty pools, fabricated mappings or pending deferred-answer leaks.
5. Replace Home's promotional content with the approved summary cards and next-step card. Chapters open Learning, question coverage opens Exercise, last-completed chapter opens that chapter, and each recommendation carries its exact typed target. At narrow widths or large fonts, stack summary cards; at wide widths retain the existing rail and use the available space. Keep every primary action reachable with scrolling and keyboard focus.
6. Support honest first-use, loading and retry states. Load failure suppresses unverified totals and recommendations. Navigation fallback actions must not start an exercise or claim progress was saved. Resume validates the stored snapshot and follows the established unavailable-exercise flow when content cannot be restored.
7. Verify recommendation priority and ties, mark/unmark chapter transitions, revision changes, stale suggestions, repeated attempts, deferred publication boundaries, exact CTA destinations, restart recovery and database failures. Run existing tests and platform builds, plus Android journeys at phone/wide widths and enlarged text. Document runtime gaps rather than treating successful compilation as device acceptance.

No application source was changed for this design review. Implementation remains pending the user's approval under the supplied design workflow.
