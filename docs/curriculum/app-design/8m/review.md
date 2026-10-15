# 8M — Missing-results and setup recovery

**Prepared:** 15 October 2026. **Revision:** v1. **Status:** Explicitly approved on 15 October 2026; 8M complete.

[Wide/phone preview](missing-results-v1.png) · [Exact prompt](prompt-v1.txt) · [Copy, route and state bindings](content-bindings-v1.json)

## Proposal

A calm Results recovery state shows the exact message “No saved result is available.” and one explicit action, “Set up a practice test”. Both wide and phone layouts retain the approved light shell, serif heading, Sage information panel and Forest action, with Practice active. The same message/action pattern handles absent answer-review session context; no alternative historical-results screen is invented.

The message describes missing session context, not a zero score, connectivity fault or confirmed deletion. No score, answer, test length, saved attempt, resume/restore action or newly persisted history is fabricated. Results is a presentation heading; the message/action are the exact handoff strings.

## Setup and session contract

The recovery action opens the existing quiz setup. It does not auto-start a test, silently manufacture a session, guess previous answers or retrieve a nonexistent history store. Learners deliberately choose/start a test using the existing setup flow; redesign of that complete screen is outside this small task.

Retain valid same-process count/feedback preferences; on a fresh launch keep the existing 70-question/default feedback behaviour. Validate the 1–70 range and accepted-pool/concept capacity at the ordinary start boundary. Do not coerce invalid text into a running quiz. The preview contains no setup values and does not claim the active pool has passed acceptance.

Missing/new session resets review filtering to All. Valid results/review keep their pinned questions, option order, answers, keys and score. Normal app restart loses existing transient state as before; this design does not add storage, restore, history, hot replacement or new public deep links. Preserve the shared unfinished-test navigation guard rather than discarding another valid session through recovery navigation.

## Generation and review

Built-in imagegen generated v1 after visual inspection of the approved 8L unavailable treatment. No reference image was passed to generation. Conceptual widths are 1280/390 logical pixels, with raster dimensions/hash saved separately. Both frames show the exact message and full action label, no truncation, no false error diagnosis or unsupported statistics. Existing generic info icon is decorative; meaning is conveyed in text.

Actual focus placement, keyboard action, screen-reader announcement, touch sizes, font/colour rendering, large-text reflow and setup/session validation require implementation/device verification. These static images do not certify them. No app, live question, official asset or PDF changed; existing content/asset acceptance holds remain open.

## Approval record

The user explicitly said “approved” on 15 October 2026, approving v1’s missing-results/setup-recovery visual direction. Missing-session, setup validation and runtime verification requirements remain in effect. Future visual changes require imagegen and renewed approval. 8N has not started and requires a separate request. Step 9 remains gated on the complete approved design package.
