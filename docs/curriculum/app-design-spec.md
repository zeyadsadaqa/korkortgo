# 8N — App design specification

**Prepared:** 15 October 2026. **Status:** 8N consolidation complete; complete-package verification and final approval remain 8O. No implementation authorised or started by this document.

This specification binds the independently approved 8B–8M previews to exact teaching, assets, routes and future implementation acceptance. It preserves their visual direction and recorded limitations; no new visual design or image revision was created during consolidation. The [package index](app-design/8n/package-index.json) records approved revisions, approval statements, image hashes, exact content bindings and implementation/verification owners. The [brief](app-design/brief.md), [exact fixtures](app-migration/preview-content.json), [migration contract](app-migration/curriculum-map.json) and [implementation backlog](app-migration/implementation-backlog.md) remain authoritative inputs.

## Authority and approval scope

Use canonical titles and complete final editable production content bound to the approved tagged 578-page screen edition, SHA-256 `78a89d8ffbb83b6e9eec6193396871ac2fb9feccf245b85112809646dd595581`. The root manuscript alone omits later approved production corrections. Technical IDs and legacy folios are routing/audit metadata, not default learner labels.

Exact copy/assets and recorded scope take precedence over imagegen raster approximations. Brand tokens define exact values; each review records generated deviations. Approval of a preview is approval of its documented visual direction, not proof of runtime accessibility, exact asset delivery, source currency or acceptance of proposed questions for scoring. Do not silently resolve incompatible visual details by redesigning them. Use imagegen and obtain renewed approval if a consolidated treatment changes an approved visual.

The completed-preview set has 12 approved task records and 16 boards. Historical review statements such as “next task has not started” describe the time of that approval; the progress tracker and current index determine current status. 8O still verifies the whole package and obtains explicit final approval; step 9 additionally needs a separate execution request.

## Approved state index and acceptance ownership

Links below open the review, which links exact images, prompts, bindings and approval. Every row is an implementation requirement, not a claim the behaviour already works. Work-item and T-case identifiers refer to the step 7F backlog.

| State | Approved revision / date | Exact content/interaction binding | Implementation owners | Required future checks |
|---|---|---|---|---|
| Library overview | [8B v1](app-design/8b/review.md), 14 Oct | `/library/module`, `/children`, `/learner_copy` in preview fixtures; M03 and five reading rows | 9B, 9K, 9L | T01, T07–T09 |
| Category filter and empty search | [8C v1, two boards](app-design/8c/review.md), 14 Oct | `/library/category_filters`, `/lesson_tags`, empty-search copy; filter/query reset contracts in 8C bindings | 9K, 9L, 9N | T07–T09 |
| Reader opening/navigation | [8D v1](app-design/8d/review.md), 14 Oct | `/lesson_reader`; M03-L02, M03-L01 previous, M03-L03 next | 9B, 9K, 9L | T01, T02, T07, T09 |
| Deliberate knowledge-check reveal | [8E v2](app-design/8e/review.md), 14 Oct | M03-L02 exact amber question/answer; hidden/revealed semantics | 9B, 9L | T01, T07, T09, T10 |
| Long calculation/large text | [8F v1](app-design/8f/review.md), 14 Oct | Final M03-L04 production source, Example B and full context blocks in bindings | 9B, 9L | T01, T08–T10 |
| Standard answered review | [8G v1](app-design/8g/review.md), 14 Oct | `/answer_reviews/0`; situation-001, selected A/correct B; M03-L02 and REF-9f4b74a976fa03fb | 9D, 9K–9M | T02, T05, T07, T09 |
| Calculation answered review | [8H v1](app-design/8h/review.md), 15 Oct | `/answer_reviews/1`; proposed fuel-saving-150-0.5, selected A/correct B; M09-L02 and REF-a7adb547fef9f80c | 9I–9M | T02, T04, T05, T07, T09 |
| Source directory/detail/return | [8I v1, two boards](app-design/8i/review.md), 15 Oct | `/sources`, retained evidence, exact URLs and origin M03-L04 return contract | 9C, 9K, 9L | T02, T07, T09, T10 |
| Sign reference/framing/zoom | [8J v1](app-design/8j/review.md), 15 Oct | `/sign_reference`; sign-B1/CAP-B1, exact asset hash, study semantics and viewer controls | 9C, 9F, 9K, 9L | T01–T03, T07, T09, T10 |
| Ambiguous-link chooser | [8K chooser v2](app-design/8k/review.md), 15 Oct | Frozen namespace/page-46 four-target alias; question context overrides page | 9K, 9L | T06, T07, T09 |
| Known parent/moved passage | [8K moved v1](app-design/8k/review.md), 15 Oct | M03-L04 missing-block synthetic case; exact notice and approved parent opening | 9B, 9K, 9L | T01, T06, T07, T09 |
| Exact-signal unavailable | [8L v1](app-design/8l/review.md), 15 Oct | `/signal_unavailable_cases`; SIG16–18 exact URLs, no internal target, optional M03-L02 | 9K, 9L | T02, T06, T07, T09 |
| Generic unavailable | [8L v1](app-design/8l/review.md), 15 Oct | Exact unavailable/library copy; unknown target and synthetic no-replacement policies | 9K, 9L | T06, T07, T09 |
| Missing results/review and setup recovery | [8M v1](app-design/8m/review.md), 15 Oct | Exact missing-result/setup strings; absent-session and setup contracts | 9K–9M | T05, T07, T09 |

The related source/reference return behaviour is specified across 8D, 8G–8J; long text and tables outside the sampled calculation remain full-content import requirements. Retired one/many/none routes are synthetic compatibility policies: unavailable is represented by 8L, multiple validated choices by 8K, and single reviewed offers reuse the validated destination/notice treatment. No real retirement is approved or invented. Home, setup, unanswered quiz and results with valid session retain existing behaviour except the audited label/content migration; these previews do not authorise an unrelated redesign.

## Shared visual language

Use the existing [brand guide](../../design/brand/README.md), [token definitions](../../design/brand/tokens.json) and [Material roles](../../design/brand/material-roles.md). All shown app states use the light Paper shell, dark Forest wordmark and active-navigation treatment. Spell KörkortGo with ö and capital K/G. Existing shell actions are Overview, Learning library and Practice. Learning/reference/fallback states select Learning library; assessed review and missing results select Practice.

| Use | Existing token/value | Constraint |
|---|---|---|
| Background | Paper `#F7F8F3` | Light surfaces dominate, including header |
| Primary action/link | Forest `#173E32`; onPrimary white | Pair text/background correctly; do not raster-sample an approximation |
| Main text | Ink `#172C29` | Real selectable text |
| Quiet grouping | Sage `#E7EEE5` | Secondary text uses onSurfaceVariant `#495A52` |
| Secondary text on Paper/white | Muted `#61706B` | Not small text on Sage: retained ratio is only 4.40:1 |
| Decorative separators | Line `#D5DED5` | Essential focus/control outlines use stronger existing outline role |
| Incorrect feedback | Error `#9A332F` / errorContainer `#FFEDEA` | Explicit Incorrect/Your answer and icon, not colour alone |
| Correct feedback | Approved Forest/Sage treatment | Explicit Correct answer and icon; pre-evaluation selection stays neutral |

All other pairs and dark values remain defined by tokens; light boards do not approve an unpreviewed dark-screen redesign. Sign delivery on relevant light/dark surfaces is still required evidence. No dynamic-colour, new palette, crest, logo or endorsement is introduced. Official artwork must not be recoloured to the theme.

Use Source Serif 4 for editorial/display headings and Source Sans 3 for interface/body roles as documented, with actual font files/version/licences pinned during implementation. Core existing app roles: headlineLarge 32/40 sp bold; headlineMedium 28/36 sp bold; headlineSmall 24/32 sp semibold; titleLarge 22/28 sp semibold; bodyLarge 16/24 sp; bodyMedium 14/20 sp; labelLarge 14/20 sp semibold. Full fifteen-role scale is in tokens. Enlarge using user font scaling and consistent font family; never imitate generated font-family drift. Test KörkortGo, Å Ä Ö/å ä ö, numeric decimals and × ÷ ² § glyphs.

Spacing follows the approved generous whitespace, inset content, separated block hierarchy, subtle borders and restrained rounded cards. There is no approved numeric spacing/radius token scale in the preview records. Use the actual approved compositions as reference; do not invent measured values by treating raster pixels as dp. Existing implementation constraints (24 dp outer padding and 1160 dp maximum shell width) are audited starting points, not new design approvals. Record any necessary new layout tokens during implementation review; materially changed layout requires preview/approval.

## Responsive reading and accessibility

Review frames are conceptual: most boards use about 1280/390 logical widths; reveal-detail boards use an approximately 800-wide content detail. They are not fixed breakpoints or minimum supported sizes. Use available width and natural reflow. Stack source/actions/navigation on narrow windows; wrap full lesson titles and the long Vehicle knowledge & maneuvering filter. Never shrink teaching text, clip it, ellipsize required copy or widen a phone viewport to conceal overflow.

Long lessons scroll vertically; constrain wide reading to the brief’s comfortable approximately 65–75-character measure where possible using actual fonts. Complete tables, equations, illustrations, scenarios, checks, answers and source context must remain available. 8F’s 16/24-sp versus 24/36-sp intent is illustrative, not measured 150% proof. Preserve operator/unit association and selectable mathematical text; assess real tables separately. A tall preview strip does not mean a one-screen fit or proof that system navigation/IME never obscures controls.

Use semantic headings, document reading order, meaningful link/action labels, visible keyboard focus, accessible selected/expanded/correctness states and usable targets. Neutral document icons never mean completion. Announce relevant result/notice changes without surprising focus jumps. Verify touch, pointer, keyboard, platform assistive technology, scrolling and text scaling on supported targets. Decorative info icons carry no unique meaning.

Hidden knowledge-check answers must be absent from accessibility reading until deliberate reveal. Keep question visible; toggle Show answer/Hide answer, associate its answer region and expose expanded state. Restore toggle focus before collapse if focus is in the answer. This is self-study, not a new score/history/completion system.

## Library and complete reader

The canonical library contains ten modules, forty lessons and ten reviews, with required references/appendices separately discoverable. Keep approved module numbers/order under filters, and exact original titles. Module 3’s overview includes M03-L01–L04 then M03-R. Teaching totals do not describe completion or filtered count. No unconditional active-1,000 claim before accepted-package checks.

All five existing categories and forty lesson-tag records come from 7E/fixtures; modules do not replace quiz categories. Traffic safety’s representative module-3 matches are M03-L02, L03 and L04. Category filters intersect canonical teaching search; preserve order. Clear search/X clears query only; Clear filters/All topics clears category only. With All already selected, clearing filters cannot cure an unmatched query. No-primary-question lessons M01-L01, M07-L04 and M10-L03 remain discoverable; no assessment is invented to fill their gaps.

Reader import uses complete final production blocks. M03-L02’s exact goal/requirements, police/guard instructions and green-light qualification stay intact. Previous/next uses canonical reading order, not old chapter/page ranges; the full 60-node reading order remains governed by 7E. “Lesson continues below” and placeholder labels are review annotations and must not become teaching. The 8D crop does not put end-of-lesson navigation before the rest of its content. Table/calculation scope and limited 1177 first-aid scope remain unchanged.

## Answer review, score identity and transient state

Preserve immediate and end-of-test feedback. IMMEDIATE reveals only after answer confirmation; AT_END withholds feedback until completion. Completed review can enter related teaching/sources and return to its same question/filter/session. Unfinished-quiz navigation uses the shared existing guard and existing related-reading restriction; a new review action must not create a bypass.

Both exact fixtures are shuffled [1, 0, 3, 2], selected original option 1 → display A and correct original option 0 → display B. Pin question revision, displayed order, selection, key and explanations; never reinterpret a shuffled index using bank order. Main explanation appears in the sampled card; retain all per-option explanations in full implementation. Show actual source records rather than blanket official badges.

8H’s exact 0.75-litre fuel revision is proposed/unapplied and unaccepted for scoring despite design approval. Historical 0.8-litre attempts, only if separately supported with complete snapshots, retain original key/order/score/version and the exact version notice. No durable attempt-history feature is added. Preserve existing selection capacity/category quotas/concept uniqueness and acceptance gates from 9J, not an invented smaller active pool to bypass holds.

Existing state is transient. Missing results/review context shows No saved result is available. and Set up a practice test. Open setup, never auto-start or fabricate results. Preserve valid same-process count/feedback preferences; normal fresh default remains 70 and existing feedback default. Validate 1–70 and accepted-pool/concept capacity at deliberate start. Missing/new session resets review filtering to All. No new database, restore, bookmark/completion history, hot replacement, analytics or public deep-link scheme.

## Sources, exact assets and zoom

Source directory examples retain actual title/publisher, distinct checked/retrieved/publication dates, classification and scope from evidence. Swedish legislation, Trafiko shortcut and Volvo model guidance are not all Transportstyrelsen. Do not present passage-specific checks as a whole-statute audit or update dates to design approval date. Commercial constants are exercise assumptions; variable-time arithmetic is editorial. Manufacturer handbook limits are model-specific. Unknown dates remain unknown.

8I is a global representative directory, not a claim every card supports its origin M03-L04. Lesson-scoped source lists use exact bindings. Keep origin content/block/position/focus through directory/detail/external visits; Back Sources restores directory, return restores the validated lesson position. Library-origin visits return to library. External URLs remain exact registered URLs; failure must not remove usable internal recovery. Stale blocks use reviewed known-parent/moved policy without invented offsets.

B1 uses sign-B1/CAP-B1, Väjningsplikt, exact caption and editorial-English notice. Bind `sign-assets/rendered/ASSET-7671a42456af532b.png`, SHA-256 `4c006030d1ffaa641df7e62f23b08187d545f9f777e1fe99afb2e98a6f5b6f5b`. The 8J placeholders do not verify a composite or replace artwork. Use unchanged bytes, original geometry/colours, contain/aspect-fit and white framing. Bind retained reuse/credit/source evidence. Meaning-bearing study captions are not pre-answer assessment descriptions; 9D supplies reviewed neutral physical descriptions.

180 dp is 8J’s candidate reference width for later intended-size review, not a proven universal minimum. Viewer starts fit; labelled Zoom in/Zoom out/Reset, keyboard/pointer pan and Close must work without pinch-only access. Close restores sign-detail context and Enlarge image focus. Preserve aspect ratio, no crop/mask/thickening/redraw/recolour. All 38 faint-outline delivery holds remain open for exact-code device/light-dark/accessibility proof; B1 layout approval clears none.

## Canonical routes and recovery

Known question identity precedes a frozen legacy-page alias. Old page 46 with situation-017 → M04-L03, with situation-103 → M04-L01. Page alone in legacy-app-4768933c3d9a opens the approved four-choice chooser: M04-L01, M04-L02, M04-L03, M05-L01. Unknown question/namespace/page never guesses first/nearest content. Choices require deliberate activation; no completion credit or PDF-equivalence claim.

Missing block with valid M03-L04 parent opens that parent with the exact moved notice; no recovered exact position is implied. Unknown parent stays unavailable. SIG16–18 retain no exact internal destination and distinct recorded official URLs, optional M03-L02 and library action; never substitute SIG1/SIG5/Y1 or add unverified entries. Generic unavailable offers library only when no validated replacement exists. Preserve actual source/lesson return context and all unfinished-test guards. Retired-content examples remain synthetic; zero real question removals/tombstones.

## Content wording and learning-aid status

No learner-facing third-party book names, borrowed legacy chapter labels or source-book folios. Keep legitimate source publishers and required artwork credits. Preserve exact official references and original teaching; removing attribution is not a content-reuse method. No official endorsement styling.

The approved learning-aid disclaimer remains: “This material is a learning aid to help you understand Swedish driving theory. It is not an official source and cannot replace official information from Trafikverket and Transportstyrelsen. Always consult their current guidance and the applicable rules.” It remains prominent in the approved book introduction; app import must preserve the corresponding approved introductory content. The previews do not approve a new disclaimer modal/banner or shortened rewrite. If new app placement/treatment is required beyond imported content, preview it and obtain approval before implementation.

## Open decisions and retained limits for 8O

| Item | Evidence / owner | Required disposition |
|---|---|---|
| Chip curvature and Sources icon consistency | 8B–8C approved variants; 9L | 8O must acknowledge the accepted variants or obtain a narrow imagegen revision for a changed common treatment; do not silently standardise visuals |
| Large-text geometry/font drift | 8F review; 9L, T09–T10 | Same body family/viewport and real user scaling are binding; raster is illustrative. Repreview if changed visual consolidation is needed |
| Stray marks, menu/language controls and OS/device framing | 8B/8G/8I/8J reviews; 9L | Already documented as unbound/decorative; omit unsupported functionality and preview-only marks, not new features |
| Exact B1 placement/legibility and 38 faint-outline holds | 8J; 9C/9D/9F | Place verified bytes and prove actual delivery; no generated substitute or hold clearance by approval |
| Complete-package acceptance | 8O | Cross-check exact fixtures/approved revisions/copy and present whole package for explicit approval; not yet performed |
| Question/source/platform acceptance | 9D–9J/9O, T01–T10 | 626 rewrites/38 replacements unapplied, three assessment briefs, source currency, all configured platforms and assistive checks remain future work |

These are explicit decisions/acceptance requirements, not permission to skip checks. No new image was necessary for this textual consolidation because it does not choose a changed common visual. 8O must not declare an unresolved design decision clear without its disposition. Print remains deferred. The final package approval field is unset in the index.

## 8N completion evidence

All twelve approved binding records were read and indexed, all sixteen preview-image hashes compared successfully, saved input/source/official-asset bindings checked, local specification/review links checked, and required handoff states mapped to approved revisions and future owners. See the [machine-readable consolidation record](app-design/8n/package-index.json) for exact inputs, checks and known issues. These are bounded documentation/identity checks; they do not rerun 7G, implement the app or constitute 8O’s independent final review. Stop after saving/updating progress; 8O requires a separate request.
