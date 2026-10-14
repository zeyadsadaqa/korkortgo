# 8A — App-preview brief and readiness

**Prepared:** 14 October 2026. **Status:** Complete preparation; ready for a separately requested 8B. No visual preview generated, design approval recorded or implementation started.

## Purpose and content authority

Prepare small, individually reviewable previews of KörkortGo’s revised learning library, complete lesson reader and answered-question review, with sources, official signs and recovery states. The audience is English-reading category B learners studying Swedish driving theory. Preserve the approved teaching meaning, requirements, exceptions and distinction between law, advice and exercise assumptions.

Use the [7F exact fixtures](../app-migration/preview-content.json) as the copy/asset authority and [preview handoff](../app-migration/preview-handoff.md) for interpretation. Use the final editable production content rather than importing only the earlier manuscript. The approved tagged screen book has 578 pages and SHA-256 `78a89d8ffbb83b6e9eec6193396871ac2fb9feccf245b85112809646dd595581`. Print masters remain deferred.

[7G verification](../app-migration/verification.md) passed 60 cross-stage checks; 7F passed 68 handoff checks. The [8A readiness record](readiness.json) freshly compares all 466 files in the saved 7G input manifest and the exact preview input/reader/sign hashes. This confirms stored package identity, not fresh legal currency, runtime behaviour or device accessibility.

## Current app and visual references reviewed

Reviewed the shared screen implementation in [App.kt](../../../composeApp/src/commonMain/kotlin/se/korkort/App.kt), the [baseline audit](../app-migration/baseline.md), existing [learn/prepare mockup](../../../design/mockups/01-learn-and-prepare.png) and [practice/review mockup](../../../design/mockups/02-practise-and-review.png). The mockups are historical visual references, not screenshots of the current running app; no runtime inspection was performed for 8A.

| Surface | Current source behaviour | Required preview change |
|---|---|---|
| Shared shell | Light Paper surface, Forest actions, serif headings, Overview/Theory library/Practice navigation; max-width shared layout | Use KörkortGo spelling and approved canonical learning labels; retain a coherent connection to practice |
| Library | 39 summary chapters, category/title search, old book-page ranges, sign catalogue action | 10 modules, 40 lessons, reviews, canonical numbering and titles, many-to-many category tags, sources/reference access |
| Reader | Chapter summary paragraphs, old book/folio label, chapter-position navigation | Complete lesson block hierarchy, goal, requirements/advice, checks/reveal, sources and canonical previous/next |
| Answer feedback/review | Immediate and end modes, selected/correct options, expandable review, integer-page related reading | Stable lesson links and scoped sources after answering; preserve shuffled answer identity and unfinished-test guard |
| Reference/recovery | Road-sign cards and external links; unknown pages currently choose first chapter; missing-session screens lack recovery content | Exact registered reference content; explicit chooser, moved/unavailable states and setup recovery |

The existing light theme and generic fonts do not prove the documented font files, dark scheme or all brand roles are integrated. Historical mockup statistics, old name, source-book references and chapter navigation must not be copied as current content.

## Visual constraints for future previews

Follow the existing [brand guide](../../../design/brand/README.md), [tokens](../../../design/brand/tokens.json) and [Material roles](../../../design/brand/material-roles.md). Retain Forest `#173E32`, Paper `#F7F8F3`, Sage `#E7EEE5`, Ink `#172C29` and restrained Ochre accents; light surfaces dominate. Source Serif 4 headings and Source Sans 3 supporting text are the documented direction, with bodyLarge 16/24 sp. Exact font files/rendering remain implementation checks. No new palette, layout or component design is selected by this brief.

Use the approved role pairs. Small secondary text on Sage uses onSurfaceVariant `#495A52`, not Muted `#61706B` (4.40:1 on Sage). Correctness needs words/icons as well as colour; pre-evaluation selection remains neutral. Essential focus/control boundaries must not rely on the pale decorative Line colour. Keep official signs in their original colours and geometry.

For each preview, propose a narrow phone view and a wider companion view where the same state needs reflow; use approximately 390 and 1280 logical pixels as review frames, not implementation breakpoints. Show large-text reflow explicitly in 8F. Other states reuse the approved visual direction, with only the minimum frames needed to show their behaviour. Dark-surface sign delivery and actual supported-device/keyboard/screen-reader checks remain 9F and step 10 requirements. Do not imply these static images verify those behaviours.

Preserve reading order, selectable text intent, descriptive actions, visible focus intent, legible wrapping, adequate touch targets and return context. No shrinking teaching text to fit a preview. Long lessons scroll; examples/calculations retain units and scope. Hide answer content from assistive reading until deliberate reveal. Sources and sign references must return to the originating lesson and reading position. These are requirements to demonstrate and later test, not claims of implemented semantics.

## Bounded preview queue and exact bindings

JSON pointers below refer to `app-migration/preview-content.json` unless another authority is named. Each row is one separately requested task, inherits the shared preview workflow, and must be approved before proceeding to another design task. Technical IDs/legacy folios belong in review notes, not automatic learner labels.

| Step | Small review scope | Exact fixture / binding | Future implementation owners |
|---|---|---|---|
| 8B | Library overview; module 3 expanded with four lessons and review; Sources/reference actions | `/library/module`, `/library/children`, `/library/learner_copy`; titles remain in approved order | 9B, 9L |
| 8C | One filtered result and one empty search | `/library/category_filters`, `/library/lesson_tags`, `/library/learner_copy/empty_search`; use Traffic safety as representative filter, retaining module 3 numbering and matching lessons; no invented query-result counts | 9K, 9L, 9N |
| 8D | Reader opening and previous/next | `/lesson_reader`: M03-L02, exact goal and first requirements paragraph; previous M03-L01, next M03-L03 | 9B, 9K, 9L |
| 8E | One check before and after reveal | `/lesson_reader/approved_markdown` amber question and exact answer; `/lesson_reader/knowledge_check_visibility` | 9B, 9L |
| 8F | One long calculation excerpt at regular and enlarged text | M03-L04 in `pdf-production/chapters/M03/chapter-source.md`, heading “Worked approximate examples · Calculate both parts”, Example B, with rough-equation and source/assumption context; 70 km/h, one second, R=21 m, B=19.6 m, S=40.6 m. Use the calculation option in the plan; do not invent a table | 9B, 9L |
| 8G | Answered police-direction item with related lesson; note both feedback modes | `/answer_reviews/0`, situation-001: selected incorrect A; correct display B; exact shuffled order and explanation; M03-L02 | 9D, 9K, 9L, 9M |
| 8H | Answered exact-result calculation | `/answer_reviews/1`, fuel-saving-150-0.5: selected incorrect A; correct B, 0.75 litres; M09-L02. Proposed revision, not live scoring acceptance | 9I, 9L, 9M |
| 8I | Source list, one detail and return context | `/sources`: REF-9f4b74a976fa03fb law, REF-0f011d29fdd9c97f Trafiko shortcut, REF-8994a6a11921a063 Volvo model guidance; reader `/lesson_reader/source_ids` | 9C, 9K, 9L |
| 8J | B1 study/reference entry and framing/zoom concept | `/sign_reference`: sign-B1, Väjningsplikt, CAP-B1, editorial English; exact asset `sign-assets/rendered/ASSET-7671a42456af532b.png`, SHA-256 `4c006030d1ffaa641df7e62f23b08187d545f9f777e1fe99afb2e98a6f5b6f5b` | 9C, 9F, 9L |
| 8K | One canonical chooser and moved-passage notice | `/auxiliary_copy/chooser_title`; `link-and-progress-map.json` → `legacy_page_aliases`, legacy_page 46 in namespace `legacy-app-4768933c3d9a`: M04-L01, M04-L02, M04-L03, M05-L01 in curriculum order. Resolve exact titles from curriculum-map. `/legacy_examples` same-old-page-a/b and missing-block; `/auxiliary_copy/moved_passage_notice` | 9K, 9L |
| 8L | Exact signal unavailable and generic unavailable | `/signal_unavailable_cases` for SIG16–18; show SIG16 visually and bind all three official URLs in notes. `/auxiliary_copy/unavailable_title`, `/library_action`; `/legacy_examples` gap-page and retired-question | 9K, 9L |
| 8M | Missing results/review context and setup action | `/auxiliary_copy/missing_result`, `/setup_action`; `link-and-progress-map.json` → `state_rules` and `navigation_routes` | 9K, 9L, 9M |

All five existing filter titles remain: Vehicle knowledge & maneuvering, Environment, Traffic safety, Traffic rules, Personal conditions. M01-L01, M07-L04 and M10-L03 stay discoverable despite lacking primary bank questions. Module/lesson totals describe teaching, not learner completion. The overview must not show unconditional “1,000 active questions”.

For 8F, the complete M03-L04 remains the import requirement; the small excerpt only bounds this preview. Use approved source prose without changing arithmetic or dropping its hypothetical/commercial scope. For 8K, question context overrides page: situation-017 → M04-L03, situation-103 → M04-L01. Page alone opens the four-choice chooser. No first-chapter guessing, automatic completion or claimed PDF equivalence.

For 8J, the exact registered B1 is study/revealed content, not a held-item delivery proof. Pair intended-size framing and zoom with a plainly marked faint-outline placement placeholder if needed; do not introduce an unreviewed assessment description or generated substitute. All 38 replacement holds stay open for actual exact-code delivery tests. Exact original artwork must be bound in notes even if imagegen cannot preserve it and a later verified placement/composite is needed.

## Copy, source and state rules

- Preserve exact approved module/lesson titles, question wording, shuffled options, keys and explanations from the fixtures. Correct display position is B in both answer samples. Record any imagegen text errors for revision; generated text is not a new content authority.
- Replace source-book folios and borrowed labels with useful lesson names and canonical navigation. No third-party book names in learner copy. Legitimate publishers remain visible in sources/credits.
- Sources show retained actual title, publisher, date, classification and scope. Trafiko constants are exercise assumptions; the Volvo example applies to its recorded model/year, not every car. Editorial arithmetic stays labelled. Unknown dates are explicit; do not invent a fresh check date.
- Preserve immediate/end-of-test feedback and the outbound unfinished-test guard. Do not expose study material as an unanswered-test escape. Return navigation preserves validated context.
- No new bookmark, durable progress, completion counter, saved-attempt store, public deep-link scheme or hot replacement. The historical-attempt notice is conditional compatibility content in 8H notes, not a new history screen. Synthetic retired cases do not mean any baseline question was removed.
- Keep KörkortGo’s independent learning-aid status clear and avoid official-endorsement styling. Preserve the approved learning-aid disclaimer as an implementation requirement; do not invent a newly approved shortened replacement.

## Approval and artifact checklist

For 8B–8M save `app-design/8x/` with versioned imagegen output, exact copy/asset notes and `review.md`. Before generating each visual, read/apply the imagegen skill and inspect the relevant existing visual references. Each review records the prompt, reference paths, output revision, frame sizes, exact fixture pointers, copy/artwork deviations, behaviour still awaiting implementation proof, user feedback and approval status. Do not mark approval from silence or from approval of this preparation step.

Before presenting a preview, check: correct fixture/title/order; no invented progress/counts; no answer leak; genuine publisher distinctions; exact sign binding or labelled placeholder; canonical routes and permitted recovery actions; required narrow/wide or large-text state; readable hierarchy and approved brand role pairs. These review checks do not replace rendered/device testing.

8N assembles the approved revisions and specification without silently changing visuals. 8O verifies complete coverage and obtains explicit approval of the whole package. A changed visual requires another imagegen preview and approval. Step 9 requires both explicit design approval and a separate execution request.

## Readiness and outstanding limits

| Requirement | 8A result |
|---|---|
| 7G passed and approved release identified | Ready; recorded PASS and release binding reviewed |
| Stored verification inputs unchanged | Ready; 466/466 manifest file hashes match in this run |
| Exact representative copy/assets and additional legacy/long-content bindings | Ready; every 8B–8M task bound above |
| Existing app and brand constraints reviewed | Ready; shared source and historical visual references reviewed |
| Small tasks, save locations and approval checklist | Ready; one focused state family per task |
| New visual preview or user design approval | Not started; 8B is next only when requested |

**Blocking issues for 8B:** None found in the stored package/brief checks.

**Retained future acceptance work:** 626 proposed rewrites and 38 replacements remain unapplied; 38 image-delivery holds require actual device/accessible-equivalent proof; SIG16–18 have no exact approved internal entries; three lessons need separate assessment briefs; legal/source currency must be rechecked when applying affected edits; platform, dark/light, font, keyboard, screen-reader and large-text behaviour require runtime checks. Print is deferred. None of these is certified or cleared by 8A.
