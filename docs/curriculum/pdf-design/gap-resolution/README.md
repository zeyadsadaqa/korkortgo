# KörkortGo — revised design review package

**Prepared 3 October 2026. Status: previews ready for feedback; explicit approval pending.** These are imagegen design previews, not finished book pages or approved instructional artwork. The earlier cover/opening v4 and navigation v1 approvals remain valid.

All 13 required sign-image gaps are resolved. The [official-vector evidence](../../sign-assets/official-poster/README.md) records the untouched official artwork, source hashes and 80/110 mm minimum reviewed widths. All 321 placement bindings pass verification. Four optional mismatched variants remain excluded. Removing hidden poster text left all 13 rendered proof pages pixel-identical.

## Start here

- [Illustrated lesson and review template](F06-v4.png): official advice is visually distinguished from KörkortGo study guidance.
- [Shared illustration style](style-v2.png): Swedish road setting, consistent vehicle palette and neutral police presentation.
- [Corrected parking scene](parking-v3.png): a clear access lane beyond the rear footway; no answer path in the assessment.
- [Corrected timeline](timeline-v4.png): explicitly not to scale; separate unanswered exercise and worked review. In the book, put the exercise before the answer, never on a simultaneously visible facing page.

## Chapter preview index

Each chapter links to its current boards. Superseded versions in this folder are retained only as history. The [50-section register](../5e/illustration-register.md) gives section-level mapping; its structured companion preserves official evidence and manuscript anchors.

| Chapter | Current previews |
|---|---|
| M01 | [M01-v2](M01-v2.png), [F06-v4](F06-v4.png) |
| M02 | [M02-v3](M02-v3.png), [parking-v3](parking-v3.png) |
| M03 | [M03-v4](M03-v4.png) |
| M04 | [D01-v2](D01-v2.png), [D01-priority-v3](D01-priority-v3.png), [D02-v4](D02-v4.png), [D04-v3](D04-v3.png), [D05-v3](D05-v3.png), [M04R-v3](M04R-v3.png) |
| M05 | [M05-v2](M05-v2.png), [D03-v1](D03-v1.png), [timeline-v4](timeline-v4.png), [parking-v3](parking-v3.png) |
| M06 | [M06-v1](M06-v1.png) |
| M07 | [M07-v1](M07-v1.png) |
| M08 | [M08-v2](M08-v2.png) |
| M09 | [M09-v2](M09-v2.png) |
| M10 | [M10-v4](M10-v4.png) |

## Factual and production review

The revised junction, cycle-crossing and roundabout boards distinguish approach from exit lanes and use Swedish right-hand traffic. Stop-line scenes place the whole vehicle behind the line. The tunnel board distinguishes motorway, non-urgent tunnel and urgent/fire situations; emergency escape refers to a marked emergency exit. The readiness lesson remains learning evidence, not an invented emergency-equipment checklist. First aid remains a brief reference to 1177, not expanded clinical teaching.

Current official references used for the traffic distinction review: [cycle crossings and passages](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/trafikregler/generella-trafikregler/cykeloverfart/) and [roundabouts](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/trafikregler/generella-trafikregler/cirkulationsplats/). Other source bindings remain in the manuscript evidence and illustration register.

These previews establish composition and visual direction. Final production must typeset the authoritative manuscript using Source Serif 4 and Source Sans 3, insert exact verified official signs wherever a sign or placeholder appears, remove incidental generated emblems, retain realistic right-hand traffic geometry and verify every cropped image at its actual print size. Tiny generated lettering and shortened board headings are not source text. Do not infer universal child-seat fitting, vehicle controls, police gestures or a real tunnel escape route from an illustrative scene. The child-passenger scene uses neutral interior context; exact fitting instructions require an appropriate official or manufacturer reference.

The four text-only sections are M01-L01, M08-L03, M09-L01 and M10-L04. Their deliberate treatment is retained, not an illustration gap. Captions and alt text remain drafts until approved artwork is cropped and bound to the final page.

The exact book disclaimer remains mandatory: “This material is a learning aid to help you understand Swedish driving theory. It is not an official source and cannot replace official information from Trafikverket and Transportstyrelsen. Always consult their current guidance and the applicable rules.”

## Approval scope

Requested approval covers the current preview versions linked above and the listed production requirements. No approval is inferred from “continue”. F01 is closed; F02–F07 now have review material and remain open for explicit design approval and final production checks. F08 is the complete-package approval gate. Step 6A has not rendered a production PDF.

Generation prompts and revision instructions are preserved in this directory. Built-in imagegen produced the previews; original generated files are retained.

### M10 revision 3

User feedback identified ambiguity between motorway occupants in A and the adjacent tunnel scene B. Version 3 separates A, B and C with wide white gutters through images and captions. The family remains entirely in A behind its guardrail. This revised image awaits explicit approval. Built-in imagegen edit; see [saved prompt](prompt-M10-v3.md).

### M10 revision 4

Panel C now shows an open, lit emergency doorway with an unobstructed approach. The protective railing remains only along the traffic side. Visually reviewed; explicit approval pending. Built-in imagegen edit; [prompt](prompt-M10-v4.md).

### M01 revision 2

M01-L04 now uses a tablet displaying a digital route map instead of a paper map, at the user’s request. Built-in imagegen edit; [prompt](prompt-M01-v2.md). Visually reviewed; awaiting approval in the one-at-a-time review. Apply the same digital-map preference when revising the companion F06 template.

**Approval recorded:** M01-v2 explicitly approved. This approval does not extend to the companion F06 template or other chapter boards.

### F06 revision 3

The companion layout now uses a digital tablet map, and both people look down at the route. Built-in imagegen edits: [digital-map prompt](prompt-F06-v2.md), [gaze correction](prompt-F06-v3.md). Current preview awaiting explicit approval; chapter board M01-v2 remains approved.

### F06 revision 4

Corrected tablet orientation with an over-the-shoulder view: both people face the display, and the reader looks past them at the route. Visually reviewed; awaiting explicit approval. Built-in imagegen [edit prompt](prompt-F06-v4.md).

**Approval recorded:** F06-v4 explicitly approved after the tablet-perspective correction. Next sequential preview: M02-v2.

### M02 revision 3

Corrected rear-bench orientation and added an empty forward-facing high-back child restraint, with child and adult outside preparing. Reframed observation scene from the rear centre to clearly show driver and wheel on the vehicle’s left. Generic preparation context, not restraint fitting instructions. Built-in imagegen [prompt](prompt-M02-v3.md).

**Approval recorded:** M02-v3 explicitly approved on 3 October 2026. This approval does not extend to the companion parking-v3 scene or other chapter boards. Next sequential preview: M03-v3.

### M03 revision 4 (requested)

User review of M03-v3 found the L02 junction scene geometrically unclear: the two directions were not separated, the lane count changed within the scene and the stop line was not clearly before the junction. The same applies to the green-signal queue panel in M03-R. Revision 4 corrects both scenes to a two-way street with two lanes per direction, continuous centre separation, consistent lane count and a solid stop line with the whole car behind it. Edit prompt saved as [prompt-M03-v4.md](prompt-M03-v4.md). The revised image is pending generation; M03-v3 remains the current linked preview until v4 exists. Not approved.

**Approval recorded:** M02-v3 explicitly approved. The separate parking/reversing preview remains pending and is next in sequential review.

**Approval recorded:** parking-v3 explicitly approved, including the shared parking observation and reversing review treatment. Next sequential preview: M03-v3.

### M03 revision 4

Revised both M03-L02 and its M03-R thumbnail with one lane per direction, a physical central divider separating opposing traffic before and beyond the junction, and an approach stop line before the cross street. Learner car remains fully behind the line. Actual image uses a planted divider rather than the prompted centre marking. Visually reviewed; explicit approval pending. Built-in imagegen [prompt](prompt-M03-v4.md).

**Approval recorded:** M03-v4 explicitly approved. Next sequential preview: D01-v2, Chapter 4 junction priority and stop location.

**D01 approval and addition:** Current D01-v2 approved. User also approved adding a separate priority-road comparison using official B4 and a side-road vehicle. That new image has not been generated or visually approved; return it for review before production. Next sequential preview: D02-v2.

### D02 revision 3

Panel D now uses a smaller island and wider framing to reveal circulating roadway and the exit approach to the cycle passage. Revised preview visually checked; explicit approval pending. Built-in imagegen [prompt](prompt-D02-v3.md).

### D02 revision 4

Redrew panel D with consistent two-way approach widths, smoother kerb connections and a compact single-lane roundabout. Revised preview awaiting explicit approval. Built-in imagegen [prompt](prompt-D02-v4.md).

**Approval recorded:** D02-v4 explicitly approved after roundabout approach-width corrections. Next sequential preview: D04-v1.

### D04 revision 3

Rebuilt panel 4 as an open right-hand side-road junction with continuous cycle-route connections. Corrected cyclist alignment within the cycle passage after inspecting v2. New preview awaits explicit approval. Built-in imagegen prompts: [v2](prompt-D04-v2.md), [v3](prompt-D04-v3.md).

**Approval recorded:** D04-v3 explicitly approved after right-turn and cycle-path corrections. Next sequential preview: D05-v2.

### D05 revision 3

Added B1 give-way above D3 roundabout at the approach in panel 1, using verified official images as imagegen references. Preview sign faces remain generated approximations, particularly small D3 arrows; production must substitute exact B1 and D3 artwork from the sign manifest. Placement preview awaiting approval. [Prompt](prompt-D05-v3.md).

**Approval recorded:** D05-v3 sign placement explicitly approved. Exact official B1/D3 artwork remains required in production. Next sequential preview: M04R-v3.

**Approval recorded:** M04R-v3 explicitly approved. Next sequential preview: M05-v1. The additional D01 priority-road scene remains required and pending generation/review.

### M05 revision 2

Widened the adjacent forward lane beside the stopped bus in M05-L01 and the matching review scene. Opposing flow stays on the far left; learner remains behind the signalling bus. No overtaking instruction is implied; manuscript bus-departure duties remain authoritative. Preview awaiting approval. Built-in imagegen [prompt](prompt-M05-v2.md).

**Approval recorded:** M05-v2 explicitly approved after bus-lane spacing revision. Next sequential preview: D03-v1.

**Approval recorded:** D03-v1 explicitly approved. Next sequential preview: timeline-v3.

**Timeline review decision:** User approved adding parking signs directly to both pages: parking sign, two-hour condition and black 9–18 hours. Revised assembly must be verified and previewed; this is approval of the concept, not unseen artwork. Next sequential preview: M06-v1.

**Approval recorded:** M06-v1 explicitly approved. Next sequential preview: M07-v1.

**Approval recorded:** M07-v1 explicitly approved. Next sequential preview: M08-v1.

### M08 revision 2

Corrected left roadworks marker bands in M08-L04 to slope downward toward the open roadway; right markers retain opposite orientation. Preview checked; explicit approval pending. Final marker artwork remains subject to exact official-asset substitution. Built-in imagegen [prompt](prompt-M08-v2.md).

**Approval recorded:** M08-v2 explicitly approved after roadwork marker correction. Next sequential preview: M09-v2.

**Approval recorded:** M09-v2 explicitly approved. Next sequential preview: M10-v4, including earlier separation and open-exit corrections.

**Approval recorded:** M10-v4 explicitly approved, including separated scenario cards and open emergency exit. Next sequential preview: style-v2. Additional priority-road and parking-sign previews remain outstanding.

**Approval recorded:** style-v2 explicitly approved. Next review: additional D01 priority-road illustration.

### D01 priority road (additional preview — v3)

Generated single-page companion illustration showing driving on a priority road at a Swedish T-junction following Swedish traffic law (Vägmärkesförordningen 2 kap. 5 § B4):
- **Priority Road (vertical):** Northbound blue car. The B4 Priority Road sign (`B4 · Priority road`) is positioned **after the intersection in the direction of travel** on the right-hand sidewalk verge north of the side road. The bottom-right corner before the junction has no sign.
- **Side Road (horizontal):** Westbound yellow car stopped behind white give-way shark's teeth (M1) at the head of the side road. The B1 Give Way sign (`B1 · Give Way`) stands directly on the curb at the give-way line.
Caption: "Traffic from the side road gives way. Keep observing and be ready to respond." Saved as [D01-priority-v3.png](D01-priority-v3.png); explicit approval pending.

### Priority-road addition — v3, 4 October 2026

[Current preview](D01-priority-v3.png) moves B4 after the junction as requested; B1 remains at the side-road entry. New scene awaiting explicit approval. Exact official signs required in production. [Edit prompt](prompt-D01-priority-v3.md).

**4 October — priority-road v3 approved:** User explicitly approved B4 placement after the junction. Next review: parking timeline with signs.

### Timeline v4 — 4 October 2026

Added matching parking signs to exercise and worked answer, with 2 tim and black 9–18 on the same supplementary plate. This is an illustrative condition assembly, not archived official T6 artwork relabelled. Source semantics checked against Transportstyrelsen T18 and T6, linked in the [prompt](prompt-timeline-v4.md). Visually checked: identical conditions, arrival 10:00, answer 12:00 only on worked page. Explicit visual approval pending. Final book places exercise before answer on separate non-facing pages.

**4 October — timeline v4 approved:** User approved the added parking signs. All chapter/scenario previews presented in the sequential review, including the priority-road addition, have now received visual approval. Next shown for review: existing sign-reference layout (5E sign-layouts-v1), whose direction was previously accepted. Production asset, typography and accessibility checks remain.

## Sequential visual review completed — 4 October 2026

User approved the sign-reference layout, the last remaining preview presented. All current chapter, scenario, style and supplemental preview designs are approved; exact filenames and hashes are in [approval-record.json](approval-record.json). Earlier pending statements are historical. No production PDF has been built. Next plan task is completing 6A: shared templates and cover/introduction/contents, followed by render checks. Final production must honour exact official assets, fonts, captions and accessibility requirements.
