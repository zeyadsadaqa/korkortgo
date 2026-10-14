# 8E — Lesson knowledge-check reveal

**Prepared:** 14 October 2026. **Revision presented:** v2. **Status:** Explicitly approved on 14 October 2026; 8E complete.

[Before/after wide and phone preview](knowledge-check-v2.png) · [Exact prompt](prompt-v2.txt) · [Copy and interaction bindings](content-bindings-v2.json) · [Approved reader](../8d/review.md)

## Proposal

Four focused reader excerpts show the same M03-L02 knowledge check before and after deliberate reveal, at wide and narrow widths. Before reveal, only the question and Show answer control appear. After reveal, the question remains and Hide answer precedes a quiet Sage answer panel. No correctness colour, submitted response, scoring or completion is implied.

Exact question: **Does amber mean accelerate to beat red?**

Exact answer: **No. The rule is to stop; the exception concerns an unsafe stop after the change, not a wish to save time.**

The source hash matches the frozen fixture. The module context, title, question and complete answer were visually checked; before panels contain no visible answer/hint. Narrow panels wrap the title, question and answer without clipping. These are conceptual 800-wide reader details and 390-wide phone details, not measured implementation breakpoints or full-screen device screenshots. Surrounding lesson content and shell remain as approved in 8D; these focused crops do not replace them.

Built-in imagegen was used, following the inspected 8D visual direction and brand constraints described in the saved prompt. No reference image was passed to generation. The initial v1 draft rendered phone panels too wide; an internal generation revision corrected their proportions. Only v2 is proposed for approval. Exact raster dimensions/hash are recorded. Imagegen does not prove exact font files or colours.

## Required reveal behaviour

- Initially collapse the answer. Hidden content must be absent from accessibility reading, not merely transparent, offscreen or visually concealed.
- A deliberate touch/pointer/keyboard action on Show answer reveals it. Keep the question visible; set the toggle’s expanded state and relationship to the answer region. Keep focus predictable, without forcing navigation or a scroll jump.
- Hide answer reverses visibility and accessibility exposure. If focus is inside answer content when collapsing, restore focus to the toggle first. Controls remain reachable and labelled at large text sizes.
- Self-study reveal adds no score, completion credit, history, bookmark or durable store. It is separate from assessed-question feedback modes and the unfinished-test guard.

“Show answer” and “Hide answer” are proposed interface labels; question and answer are approved teaching copy. Reveal state is a presentation requirement, not a new knowledge check or alteration of teaching.

## Verification limits and approval

Static imagery cannot verify the accessibility tree, expanded state, screen-reader reading order, keyboard activation/focus, actual touch sizes, viewport scrolling, text scaling or hidden-content exclusion. Validate those behaviours during implementation/device checks. No new sign artwork, app code, question-bank, official-asset or PDF changes occurred. All existing implementation holds remain open.

The user explicitly said “approved” on 14 October 2026, approving v2’s wide/phone before-and-after reveal direction. The documented reveal, accessibility and implementation requirements remain in effect. Future visual changes require another imagegen revision and approval. 8F has not started and requires a separate request. Step 9 remains gated on the complete approved design package.
