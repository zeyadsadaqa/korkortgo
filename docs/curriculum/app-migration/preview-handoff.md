# 7F — App-preview content handoff

**Prepared:** 14 October 2026. This is exact content and behaviour for future step 8, not a visual design or implementation approval.

[Exact fixtures](preview-content.json) · [Work items](implementation-backlog.md) · [Source registry](curriculum-map.json) · [7F checks](handoff-checks.json)

## Step 8 sequence and required views

When separately requested, use the imagegen skill for library, lesson-reader and answer-review previews. Present the generated previews for explicit feedback/approval and revise/reapprove if requested. Do not start step 9 on the strength of 7F approval. Record the approved preview revision and bind it to the implementation handoff.

The JSON is the content authority: exact source locators/hashes, approved Markdown, unchanged assessment, proposed exact fuel revision, shuffled display order, sign bytes/caption, source evidence and legacy fixtures. Technical IDs and old folios are audit metadata; they are not required learner labels. No layout, colour palette or new design is prescribed here.

## Library preview

Use **Learning library**, with **10 modules** and **40 lessons**, module **3. Read the road before acting**, and these exact approved titles in order:

- Recognise what a sign asks (`M03-L01`).
- Combine the instructions (`M03-L02`).
- Find your way without rushing (`M03-L03`).
- Leave room to respond (`M03-L04`).
- Review and self-assessment (`M03-R`).

Include Sources and Road signs and reference actions. Use the five existing category labels and 7E many-to-many tags from JSON, maintaining canonical module numbering under a filter. Empty search: “No matching lessons.” Do not invent completion badges/bookmark history. M01-L01, M07-L04 and M10-L03 must stay discoverable despite no primary bank questions. Use accepted-package question counts only after acceptance, not an unconditional active-1,000 label.

## Lesson-reader preview

Use M03-L02 **Combine the instructions** under module 3. Preserve approved reading content, requirements and exceptions; show the opening goal and first requirements paragraph below. The full exact lesson is in JSON. Previous: **Recognise what a sign asks**; next: **Find your way without rushing**. Sources: source-traffic-law, source-sign-law and source-panels; return to the same lesson/position after a reference visit.

**Your goal:** Interpret signs, panels, markings and signals together, including authorised directions.

**Requirements.** Follow the traffic instructions that apply to you. Where an instruction differs from a general traffic rule, the instruction governs. A steady traffic-light indication takes precedence over a yield or stop sign; a police officer's direction takes precedence over the rules and ordinary traffic instructions. This is not a rule that a green signal cancels every other restriction. Authorised guards also give traffic directions that must be followed. [Traffic Regulation, chapter 2 §§2–4][traffic-law]


Knowledge check: **Does amber mean accelerate to beat red?** Hide its approved answer until deliberate reveal: **No. The rule is to stop; the exception concerns an unsafe stop after the change, not a wish to save time.** Keep hidden content out of accessibility reading before reveal. Full import must also preserve tables, calculations and longer content, represented by M03-L04 in implementation verification.

## Answer-review previews

Show feedback only after answering, preserving both existing immediate and end-of-test modes. Do not offer related teaching as an unanswered-test escape from the existing guard. Use the exact shuffled fixture orders; the key is display position B in both samples, not the first displayed option.

### situation-001

**Content status:** unchanged reviewed assessment.

A police officer signals you to stop while your traffic light is green. What should you do?

- A. Follow the green light — selected (incorrect)
- B. Stop as directed by the officer. — correct
- C. Continue if the road looks clear
- D. Stop only if there is a stop sign

**Revealed explanation:** A police officer's directions take precedence over traffic signals, signs and general rules.

**Related lesson:** Combine the instructions (`M03-L02`). Exact source-reference IDs are in JSON; publisher/classification must come from those records, not a generic official-source badge.

### fuel-saving-150-0.5

**Content status:** 7D proposed revision; not live or accepted for scoring.

Smoother driving reduces measured consumption by 0.5 litres per 100 km. Over 150 km, how much fuel is saved? Give the exact result in litres; do not round.

- A. 0.375 litres — selected (incorrect)
- B. 0.75 litres — correct
- C. 1.5 litres
- D. 1.125 litres

**Revealed explanation:** 150 × 0.5 ÷ 100 = 0.75 litres exactly from the supplied assumptions. No display rounding is requested; this is not a guaranteed real-world saving.

**Related lesson:** Use energy with foresight (`M09-L02`). Exact source-reference IDs are in JSON; publisher/classification must come from those records, not a generic official-source badge.

The fuel sample is a proposed 7D revision, not an applied change or newly approved scored item. Its old 0.8-litre attempt, if later supported as a historical snapshot, keeps its original score and version notice. Current app has no saved-attempt store; do not turn this compatibility case into a new history feature.

## Reference, source and legacy states

- **B1 study/reference:** use the exact registered Give way artwork, Swedish official name, CAP-B1 caption and editorial-English notice from JSON. Use unchanged asset bytes, not an imagegen approximation. This is revealed/reference content; assessment-specific physical alt text is still future 9D work.
- **Sources:** include Swedish legislation (REF-9f4b74a976fa03fb), commercial stopping shortcut (REF-0f011d29fdd9c97f) and model-specific Volvo guidance (REF-8994a6a11921a063). Display actual title/publisher and retained dates/limits from evidence; never relabel all as Transportstyrelsen. Commercial constants are exercise assumptions, and manufacturer speed limits are not universal rules. Editorial arithmetic remains labelled as such.
- **Ambiguous old link:** old page 46 with situation-017 opens M04-L03; with situation-103 opens M04-L01. Page alone uses reviewed canonical choices, without displaying old chapter names or implying PDF equivalence. JSON contains the complete frozen-namespace examples.
- **Unavailable signal:** SIG16–18 use their exact recorded 7E message and official-description action plus optional Combine the instructions. No exact approved internal entry exists; do not show SIG1, SIG5 or Y1 as its replacement.
- **Other fallbacks:** show canonical chooser, unavailable/library action, moved-passage notice for known parent, and missing-results/setup state from JSON. Retired one/many/none examples are synthetic compatibility tests; no question has actually been removed.

## Constraints to carry into approval

Imagegen establishes visual direction; it does not verify official sign geometry, small-size legibility or assistive semantics. Use the registered B1 image for study/reference content. For faint-outline presentation, preview the proposed intended size, framing and zoom interaction while retaining the original geometry; label all 38 holds uncleared until actual delivery tests. Never generate substitute sign artwork. If imagegen cannot preserve exact assets/text, use a clearly marked placement placeholder for later verified compositing and retain the exact JSON copy alongside the preview.

Include source/reference return, large-text/long-content handling, empty search, multi-target chooser and unavailable state in the review set. No old book names, borrowed chapter labels or source-book folios in learner copy. Legitimate publisher names remain in sources and credits. No invented progress, persistence or deep links. All new presentation still requires explicit user approval.

[traffic-law]: https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/trafikforordning-19981276_sfs-1998-1276/
[sign-law]: https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/vagmarkesforordning-200790_sfs-2007-90/
[panels]: https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/tillaggstavlor/
