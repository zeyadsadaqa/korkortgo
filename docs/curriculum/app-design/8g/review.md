# 8G — Standard answer review

**Prepared:** 14 October 2026. **Revision:** v1. **Status:** Explicitly approved on 14 October 2026; 8G complete.

[Wide/phone preview](answer-review-v1.png) · [Exact prompt](prompt-v1.txt) · [Question/options/route bindings](content-bindings-v1.json) · [Preview handoff](../../app-migration/preview-handoff.md)

## Proposal and fixture

An answered situation-001 review in wide and phone layouts. Incorrect selected A and correct B use icons and explicit labels as well as colour. Feedback includes the exact main explanation, a related lesson action and a scoped Sources action. This board depicts completed-test review; it does not authorise those outbound actions during an unfinished test.

Exact shuffled order:

- A. Follow the green light — selected, incorrect.
- B. Stop as directed by the officer. — correct.
- C. Continue if the road looks clear.
- D. Stop only if there is a stop sign.

The source fixture’s original option order is mapped through [1, 0, 3, 2]. Selected original index 1 becomes display A; correct original index 0 becomes display B. These identities were checked independently before saving. Full original options and their explanations remain in the bindings; the preview shows the main explanation as required for 8G and does not authorise deleting per-option explanations in implementation.

The prompt and main explanation match the unchanged reviewed fixture. Related teaching is M03-L02, Combine the instructions. The exact source reference is REF-9f4b74a976fa03fb; use retained actual legislation title/publisher/date/scope when opened, not a generic official-source badge. No assessment illustration is added: the question fixture has an empty image field.

## Feedback and navigation contract

- IMMEDIATE: reveal key/explanation only after answer confirmation. Preserve the existing unfinished-test guard and current restriction on related-reading escape. Reusing this feedback treatment must not make the completed-review outbound actions an unguarded immediate-mode action.
- AT_END: withhold answer correctness/explanations until completion; then use the same evaluated review treatment.
- Completed review: related lesson and Sources open validated destinations and return to the same question, filter and session context. No integer-page fallback, first-chapter guess or synthetic saved history.
- Preserve the pinned shuffled answer/option identity and version. Review rows do not accept a new answer or regrade an old selection. No new completion credit or persistence.

## Visual review and limits

Built-in imagegen produced v1 following the existing reader brand direction and inspected historical practice/review mockup. No reference image was passed to generation. Conceptual frames are 1280/390 logical pixels, with output dimensions/hash recorded. Both views retain exact question/options/main explanation, selected/correct positions and related title. Phone status labels stack under answer text. No invented score/question totals, page labels, progress, signs or source publishers appear.

The generator added a phone hamburger with no action binding, as in an earlier historical preview. This is a documented unbound detail, not approval for a new menu. Omit it unless a later approved preview defines its behaviour. The evaluated feedback and related-reading presentation are the scope of this approval.

Actual focus, assistive announcement of selected/correct state, reading order, key hiding before reveal, touch size, text scaling, fonts, platform navigation and quiz guards remain implementation/device checks. Static images do not prove them. No live question, app code, official asset or PDF changed; all existing implementation holds remain open.

## Approval record

The user explicitly said “approved” on 14 October 2026, approving v1’s standard answer-review visual direction. The documented quiz guards, source/answer bindings and unbound-menu limitation remain in effect. Future visual changes require an imagegen revision and renewed approval. 8H has not started and requires a separate request. Step 9 remains gated on the complete approved design package.
