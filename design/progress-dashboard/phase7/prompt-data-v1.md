# Phase 7 data controls preview

30 October 2026. Built-in image generation tool. Pending explicit design approval. Supplements the selected v2 design. All data is illustrative; no learner data was exported, imported or reset. Expected output: `preview-data-v1.png`.

## Prompt

Use case: ui-mockup.
Asset type: Phase7 data-management design review board for KörkortGo, an English-language Swedish driving theory app.
Input image: chosen preview-v2, STYLE REFERENCE ONLY. Preserve the original. Extend its quiet Home design into the "Your data" subpage without redesigning the app.
Create SIX equal mobile screens in THREE COLUMNS by TWO ROWS on a tall high-resolution board. Flat straight-on UI, same390x844 logical proportions, no device frames or perspective. Small labels above each phone, board footer "Phase 7 · Your data · Illustrative scenarios". Four or more lines of small text must not become illegible; keep hierarchy restrained and bodies scrollable. Fixed bottom nav Home / Learning / Exercise with icons and words; Home selected in all panels. Back "Home" or "Your data" as appropriate, compact KörkortGo wordmark.
Style: paper #F7F8F3, forest #173E32, sage #E7EEE5, white cards, fine #D5DED5 borders, ink #172C29. Source Serif4 headings, Source Sans3 body. 20px margins,16px corners,48px+ touch targets. Dark red #9A332F and pale #FFEDEA only for real destructive actions or errors. No gradients, no new purple palette, no illustrations, confetti, jargon, accounts, automatic sync, or readiness scores. Primary controls must not overlap nav. These are independent examples, not one sequence of actual user changes. All values are illustrative.

TOP LEFT label "01 / YOUR DATA".
Heading "Your data". Body "Keep a copy of your progress or restore a saved file." Compact white summary list "10 lessons marked as read", "16 completed or ended exercises", "1 unfinished exercise". Three clearly separated icon-and-text rows: "Export progress" / "Save a backup file"; "Import progress" / "Review a file before replacing progress"; and lower separated restrained red-text "Reset progress" / "Clear progress on this device". Neutral sage note "Progress is stored on this device. Keep exported files somewhere safe." No claim a backup already exists or that data automatically syncs. Entry point from the Home footer is implied; no fourth nav tab.

TOP MIDDLE label "02 / EXPORT".
Back Your data. Heading "Save a backup". White card with neutral document icon and filename "korkortgo-progress.json". Label "Includes" and three short rows "Reading progress and positions", "Exercise history and confirmed answers", "Unfinished exercise". A sage note "Choose where to save the file. Exporting does not change your progress." Full-width forest button "Save backup file". Secondary text action "Cancel". No preemptive "Export complete" badge before the platform file save finishes. No technical schema details, no bundled-artwork download, no email.

TOP RIGHT label "03 / REVIEW IMPORT".
Back Your data. Heading "Review import". White file card "korkortgo-progress.json", small neutral "File checked". Summary "8 lessons marked as read", "6 completed or ended exercises", "No unfinished exercise". Contained warning pale red with restrained dark red icon, heading "Replace current progress?", body "This replaces your reading progress, exercise history and unfinished exercise on this device." Secondary outlined full-width button "Export current progress first". Forest full-width button "Replace progress". Text action "Cancel". Import is explicit replacement, never a merge. Record counts are summaries of a validated hypothetical file. No replacement happens at file selection alone. Keep both export and replace actions fully visible above the nav with comfortable spacing.

BOTTOM LEFT label "04 / INVALID IMPORT".
Back Your data. Heading "Import progress". Contained pale error panel with alert icon, heading "This file can't be imported", body "Choose a supported KörkortGo progress file." Below reassuring ordinary text "Your current progress has not changed." Forest full-width "Choose another file", outlined "Back to Your data". No exposed parser error, JSON blob, reset suggestion, partially imported data, or zeroed progress. This is the state after rejecting validation before any write.

BOTTOM MIDDLE label "05 / CONFIRM RESET".
Back Your data. Heading "Reset progress?". Large readable text with natural wrapping; this panel demonstrates enlarged-text-friendly layout. Pale warning card "This clears:" then concise plain rows "Reading progress and saved positions", "Exercise history and answers", "Your unfinished exercise". Separate neutral note "The lessons and question bank stay available. Exported files are not deleted." Secondary outlined full-width "Export progress first". Forest full-width "Keep my progress". Restrained dark-red full-width "Reset progress" with white label. Clear consequence text "You can't undo this without an exported backup." This is an explicit confirmation screen after opening Reset, not an automatic reset. Make destructive action unambiguous and all buttons reachable through scrolling; no typed-password or checkbox requirement.

BOTTOM RIGHT label "06 / RESET COMPLETE".
Back Home. Heading "Your data". Small green check and sage status panel "Progress reset", text "You can start again with chapter 1." Three truthful white summary rows "0 lessons marked as read", "0 completed or ended exercises", "No unfinished exercise". Primary forest "Start learning" button. Secondary text link "Import a saved file". Bottom nav unchanged. No claim that backup files were erased or that the curriculum was removed. Show this only after the reset transaction succeeds, not while saving.

Keep labels and consequences clear in the established v2 product language. This board is a proposal for approval, not a screen capture or proof of implemented data handling. All6 screens light-theme; runtime accessibility, platform pickers and release acceptance are separate engineering checks.
