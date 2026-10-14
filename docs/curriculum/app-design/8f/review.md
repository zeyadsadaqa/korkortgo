# 8F — Long-content and large-text reading

**Prepared:** 14 October 2026. **Revision:** v1. **Status:** Explicitly approved on 14 October 2026; 8F complete.

[Three-view preview](long-content-v1.png) · [Exact prompt](prompt-v1.txt) · [Production content/context bindings](content-bindings-v1.json) · [Brief](../brief.md)

## Proposal and content

Wide regular, phone regular and phone enlarged excerpts show M03-L04, Leave room to respond. The approved serif/Forest/Paper reader direction continues, with a Sage worked-example panel, reflowable equations and scope notes. Enlarged text represents user/system font scaling, not a proposed app settings feature. This is a long reading excerpt with a calculation, as permitted by 8F; it does not invent a table.

The example is the approved Example B: 70 km/h and one second. Reaction R = 7 × 1 × 3 = 21 m; braking B = 7² × 0.4 = 19.6 m; total S = 40.6 m. These were independently recomputed, and the production source hash matches the frozen fixture. All three views retain the complete Example B prose, formula symbols/units, commercial-source classification and the statement that shortcuts are not a safe-distance guarantee or actual-hazard prediction. Visual inspection found no core arithmetic/copy omission from the requested excerpt.

The context bindings preserve the exact original source paragraphs, including definitions of v/t, good-brake/good-tyre/dry-asphalt assumptions, the separate exact conversion and the full source-scope distinction. The preview samples formula lines, Example B and two exact scope sentences from that longer sequence; it does not replace complete teaching or reorder the full lesson import. All omitted context must remain in the implemented reader around the example. Sources is bound to the lesson’s scoped source records, including source-stopping-shortcut and source-stopping-principles, with a return to the same reading position. Trafiko must not be relabelled as an official agency.

## Generation and visual limits

Built-in imagegen generated v1 from the saved prompt after visual inspection of the approved 8D reader. No reference image was passed to generation. Requested conceptual reading frames were a wide excerpt and two equal-width phones; regular/enlarged body targets were illustrative 16/24 and 24/36 sp.

The raster shows larger phone text and additional wrapping. It does not exactly enforce equal phone widths or the requested 150% scale; the enlarged example paragraph also appears more serif-like than the regular body. These are documented generation deviations, not approval to vary font family by text scale. Actual implementation must use the same body font and fixed viewport width while respecting user scaling; increasing height/scroll is the response to larger text. If visual consolidation changes the approved direction, generate a revised preview and obtain approval again.

These tall content strips are not one-screen fit promises. Readable body text, normal reading order, no horizontal page overflow, operator-safe equation wrapping, selectable text and predictable vertical scrolling must hold on actual viewports. Keep labels/source links reachable; do not shrink text or clamp it to conceal overflow. Exact fonts/colours, actual scale ratios, accessibility reading of mathematical symbols, focus, touch sizes and device reflow remain implementation verification. Wider or more complex tables elsewhere in the curriculum still require meaningful import/device checks.

No new artwork, question bank, app code, official asset or PDF changes occurred. No completion/progress/bookmark/history feature is proposed; no existing implementation hold is cleared.

## Approval record

The user explicitly said “approved” on 14 October 2026, approving v1’s long-content and enlarged-text visual direction. Documented generation deviations, full-content requirements and runtime reflow checks remain in effect. Future visual changes require an imagegen revision and renewed approval. 8G has not started and requires a separate request. Step 9 remains gated on the complete approved design package.
