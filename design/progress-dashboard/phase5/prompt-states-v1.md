# Phase 5 Exercise state preview

30 October 2026. Built-in image generation tool. Pending design approval. Independent illustrative scenarios, not production defaults or a shared learner timeline. Existing approved resume and save-failure controls remain the phase-3 design.

Expected preview: `preview-states-v1.png`.

## Prompt

Use case: ui-mockup.
Create a second supplementary phase-5 design approval board for KörkortGo, matching the supplied approved preview-v2 and flow board. Both inputs are STYLE REFERENCES ONLY; do not alter them. Four equal mobile screens side by side, flat straight-on UI, realistic 390x844 proportions, high-resolution landscape review board. Neutral paper background, no hardware frames, no perspective. Consistent forest #173E32 primary actions, paper #F7F8F3 background, sage #E7EEE5 highlights, white cards with fine gray-green #D5DED5 borders, ink #172C29, Source Serif 4-style editorial headings and Source Sans 3 body. Same compact wordmark and bottom nav Home / Learning / Exercise, Exercise selected. Exact counts matter. No gradients, no decorative illustrations, no purple accents, no readiness score or streak. Generous touch targets and safe areas, readable text, no primary button clipped by nav. Footer "Phase 5 · Empty and recovery states · Independent illustrative scenarios". These are four independent learner states, not one timeline.

SCREEN1 label "01 / ALL QUESTIONS ANSWERED".
The approved Exercise hub with heading "Exercise", subheading "Keep building your understanding." White summary card showing "1,000 / 1,000", label "Unique questions answered", full progress100%. Two values "900 correct on latest attempt" and "100 to revisit". Primary button "Start an exercise" (mixed practice remains available). A muted but readable "Practise unanswered" row with text "All current questions answered" and a check icon; no start action for an empty pool. Active "Review mistakes" row with "100 questions to revisit". A calm sage note "You can revisit any topic with mixed, chapter or category practice." No claim that coverage equals mastery. Section "Recent exercises", single row "Mixed practice", "16 / 20 correct", "Today". Fixed bottom nav.

SCREEN2 label "02 / EMPTY POOL · LARGE TEXT".
A targeted empty-state page rendered at approximately160% body text, larger text wrapping naturally with a scrollable body and fully visible nav labels. Back "Exercise"; heading "Review mistakes". Simple neutral outlined check icon on sage circle, heading "No mistakes to review", body "None of your latest published answers need review." This independent example has no eligible review pool; do not show a numeric field or a disabled Start button. Two stacked full-width buttons: forest "Practise unanswered", outlined "Choose another mode". Small note "An unfinished end-feedback exercise updates progress only when completed." No scores, no confetti, no claim that the entire bank has been answered. Larger text should reduce how much content fits, never scale down to squeeze it all in. Ensure both actions can be reached above the fixed bottom navigation through scrolling.

SCREEN3 label "03 / LOADING".
Heading "Exercise". White coverage-shaped panel with restrained gray skeleton lines where count and labels belong, a small neutral progress spinner, and actual readable label "Loading your progress…". Skeleton rows for recent exercises, no numeric values, no 0/1000 default, no fake history, no accuracy or correctness text. Start/targeted actions unavailable until data is ready; keep bottom nav visible and active. Calm light theme matching other screens; no technical database terminology.

SCREEN4 label "04 / LOAD FAILURE".
Heading "Exercise", subtitle "Your progress is unavailable". A contained light error card using pale #FFEDEA and dark red #9A332F, unobtrusive alert icon, heading "Couldn't load your progress", body "Try again to continue with your saved progress." Full-width forest "Try again" button within the card. Below calm explanatory text "No new exercise has started." Do not display fabricated zero totals, old results as current, destructive reset, or database implementation details. Navigation stays available. Maintain exactly the same spacing and material style as the phase3 save-failure preview, and use error color only for this actual error.

