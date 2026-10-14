# 8C — Library search, filters and empty state

**Prepared:** 14 October 2026. **Revision:** v1. **Status:** Explicitly approved on 14 October 2026; 8C complete.

[Traffic safety preview](library-filter-v1.png) · [Empty-search preview](library-empty-v1.png) · [Exact bindings/action contracts](content-bindings-v1.json) · [Filter prompt](filter-prompt-v1.txt) · [Empty prompt](empty-prompt-v1.txt)

## Proposal and exact content

Two built-in imagegen boards each show a wide and phone view, extending the approved [8B direction](../8b/review.md). Review frames represent approximately 1280 and 390 logical pixels; generated raster sizes are recorded in the bindings. The 8B preview was visually inspected, with its palette/type direction described in both prompts; no reference image was passed to either generation call.

**Filtered:** Traffic safety selected, empty query. Module 3 remains number 3. Its exact matching lessons, verified against both category membership and lesson-tag records, are M03-L02 Combine the instructions, M03-L03 Find your way without rushing and M03-L04 Leave room to respond, in that order. M03-L01 is not a Traffic safety match. The module review is not a category-tagged lesson. Other matching modules continue outside this representative frame; the preview does not restrict the full library to module 3.

**Empty:** query `zzzxq`, All topics selected, exact message “No matching lessons.” No result cards or invented suggestions. Sources and Road signs and reference remain available. Teaching totals remain 10 modules and 40 lessons, not filtered-result counts.

All five existing category labels are retained. Filtering uses the planned many-to-many teaching tags, not question counts or quiz quotas. M01-L01 and M10-L03 remain available under their RULES/PERSONAL tags (and other recorded tags); M07-L04 remains available under SAFETY/PERSONAL. No-primary-question status never excludes a lesson. Search must use canonical imported teaching, retaining canonical module/lesson order.

## Proposed action contracts

- Clear search and the input X clear only the query and keep the category. The X has accessible name “Clear search”.
- Clear filters and All topics reset category selection only, retaining the query. When All topics is already selected, Clear filters cannot recover an unmatched query; Clear search is the primary recovery action. Use the same contract consistently in implementation.
- Search and category selection intersect. Selection must have an accessible selected state; search keeps a persistent accessible label when populated. Announce empty/results changes without moving focus unexpectedly.

“Search lessons”, “All topics”, “Clear search” and “Clear filters” are proposed interface copy, separate from approved curriculum titles. These controls do not add persistence or modify quiz category allocation.

## Visual inspection and limits

Both boards show full category labels, exact matching lesson titles where applicable, canonical number 3 and the exact empty message. Phone filters wrap and recovery actions stack. No invented progress, badges, bookmarks, durations, active-question claims, source-book folios or official sign art appear. Unbound hamburger/language controls and the stray wide-header mark from 8B are absent.

Minor generated styling differences remain: filtered chips are more rectangular than empty-state chips; the Sources icon is a generic document rather than 8B’s book. These are visible proposals for feedback, not a change to content or behaviour. The filtered empty input renders its label as a placeholder; the populated empty-search frame demonstrates the required persistent label. Actual implementation must keep an accessible label in both states and use one approved chip/icon treatment. If visual consolidation changes the approved direction, obtain a revised imagegen preview and approval.

Raster images do not verify precise brand values, fonts, focus, screen-reader announcements, target sizes, search indexing, text scaling or all-module discoverability. Those remain implementation/device checks. No app code, live question, official asset or PDF changed; existing image-delivery holds remain open.

## Approval record

User explicitly said “yes looks great, approved” on 14 October 2026, approving both v1 boards and their visual direction. Recorded styling differences and implementation requirements remain documented; any later visual consolidation that changes the direction requires a revised imagegen preview and approval. 8D has not started and requires a separate request. Step 9 remains gated on the complete approved design package.
