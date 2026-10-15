# 8H — Calculation answer review

**Prepared:** 15 October 2026. **Revision:** v1. **Status:** Explicitly approved on 15 October 2026; 8H complete.

[Wide/phone preview](calculation-review-v1.png) · [Exact prompt](prompt-v1.txt) · [Question/source/version bindings](content-bindings-v1.json) · [Approved 8G direction](../8g/review.md)

## Proposal and content status

The approved answered-review treatment now shows the exact proposed fuel-saving-150-0.5 fixture, selected incorrect A and correct B, a calculation explanation, M09-L02 Use energy with foresight and Sources. **This is the 7D proposed revision, not a live question or accepted scored item. Approval of this design does not accept its content for scoring or apply it to the bank.**

Exact displayed order: A 0.375 litres (selected/incorrect), B 0.75 litres (correct), C 1.5 litres, D 1.125 litres. The full prompt explicitly requests an exact result with no rounding. Independent Decimal arithmetic gives 150 × 0.5 ÷ 100 = 0.75 litres. Original indices [1, 0, 3, 2] were checked against the selected/keyed identities. Full per-option explanations are preserved in bindings even though this bounded preview shows the main explanation only.

Both frames retain the complete prompt, choices, exact result, hypothetical supplied-assumption limitation and no-real-world-guarantee qualification. Related teaching’s source hash matches its frozen production location. Sources binds REF-a7adb547fef9f80c and the scoped lesson records; arithmetic is editorial, not an official guaranteed saving. No generic official-source badge is used.

## Historical-score compatibility — notes only

If historical snapshots are separately supported in future, an earlier 0.8-litre attempt keeps its original question version, original shuffled option identity/order, keyed answer, selection and original score. Never regrade it against the proposed 0.75-litre key. A same-ID content revision is not sufficient to reconstruct old grading from an unversioned display index.

Use the exact conditional notice: “This attempt used an earlier question version. Its original answer and score are shown.” This belongs only to a supported historical snapshot, not the current proposed-item review. No saved-attempt/history store exists in the audited app, and this task adds neither a store nor a history screen. Normal restart continues to clear existing transient state. The note is a compatibility requirement, not a new user feature.

## Modes, visual review and limits

Reuse 8G’s reveal contract: IMMEDIATE feedback follows answer confirmation; AT_END hides correctness/explanations until completion. Outbound lesson/source actions in the preview depict completed-session review. Preserve the unfinished-test guard and existing immediate-mode reading restriction; the diagram does not authorise a new test escape. Source/lesson return keeps validated question/session context.

Built-in imagegen generated v1 after inspection of the approved 8G image; no reference image was supplied to generation. Conceptual widths are 1280/390 logical pixels; raster dimensions/hash are recorded. Phone statuses stack, text wraps and full explanation/actions remain visible. Correctness uses words/icons plus colour. The previously unbound phone menu is absent. Card grouping differs slightly from 8G but keeps the same content hierarchy and palette; it is part of this proposal. No core fixture discrepancy was observed by visual inspection.

Static imagery does not certify exact fonts/colours, mathematical-symbol accessibility, focus, text scale, touch targets, guard logic or content-version behaviour. Verify these during implementation/device checks. No app code, live question, official asset or PDF changed; all content/asset acceptance holds remain open.

## Approval record

The user explicitly said “approved” on 15 October 2026, approving v1’s calculation answer-review visual direction. This approval does not accept the proposed question for live scoring or apply it to the bank. Historical-score compatibility, quiz guards and runtime verification requirements remain in effect. Future visual changes require imagegen and renewed approval. 8I has not started and requires a separate request. Step 9 remains gated on the complete approved design package.
