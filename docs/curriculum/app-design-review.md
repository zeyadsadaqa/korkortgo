# 8O — Complete app design package review

**Verified:** 15 October 2026. **Technical result:** PASS — 681/681 checks. **Status:** Explicitly approved on 15 October 2026; 8O and step 8 complete. Implementation has not started.

[Design specification](app-design-spec.md) · [Approved preview index](app-design/8n/package-index.json) · [Machine-readable verification](app-design/8o/verification.json) · [Reproducible checker](app-design/8o/verify_design_package.py)

## Package presented for approval

The package contains twelve individually approved preview tasks and sixteen imagegen boards, bound to exact content, sources, official assets and future implementation requirements. These individual approvals are retained. The user explicitly approved the complete package on 15 October 2026: “yes approved”.

| Area | Approved visual records |
|---|---|
| Library overview and navigation | [8B v1](app-design/8b/review.md) |
| Category filtering and empty search | [8C v1, two boards](app-design/8c/review.md) |
| Lesson opening, sources and previous/next | [8D v1](app-design/8d/review.md) |
| Before/after self-study answer reveal | [8E v2](app-design/8e/review.md) |
| Long calculation and enlarged text | [8F v1](app-design/8f/review.md) |
| Standard answered review | [8G v1](app-design/8g/review.md) |
| Proposed calculation answered review | [8H v1](app-design/8h/review.md) |
| Source directory, detail and lesson return | [8I v1, two boards](app-design/8i/review.md) |
| B1 reference/framing/zoom, artwork separately bound | [8J v1](app-design/8j/review.md) |
| Ambiguous-link chooser and moved passage | [8K chooser v2 / moved v1](app-design/8k/review.md) |
| Exact-signal and generic unavailable states | [8L v1, two boards](app-design/8l/review.md) |
| Missing results and setup recovery | [8M v1](app-design/8m/review.md) |

## Verification performed

Fresh checks independently compared the specification/index inputs, approval statements, reviews, prompts and all sixteen image hashes. The complete saved 7G input manifest also still matches: 466 planning/source/app/asset files unchanged. This confirms stored-input identity, not a new external legal/source audit or runtime implementation.

Exact fixture checks cover module/lesson titles and totals, forty category tags, Traffic safety’s M03-L02–L04 membership, zero-primary-question discoverability, reader copy and previous/next, hidden/revealed answer requirements, complete stored M03-L04 calculation context, both shuffled A-selected/B-correct assessments, exact 0.75-litre arithmetic, source fixtures/URLs, B1/CAP-B1/official bytes, legacy chooser order and question precedence, moved notice, all three unavailable signals and missing-session recovery. Local specification/review links resolve. The specification maps every required handoff state to approved previews and step 9/T01–T10 owners.

Learner-facing fixture copy was checked for the known legacy book name/attribution and source-book-folio patterns, with no findings. Existing visual review records cover all sixteen boards; 8O additionally reinspected the two 8C boards, 8F and 8J to examine the remaining visual variants. This is a targeted fixture/text and recorded-visual review, not OCR proof of every raster glyph or verification of the full future app. Legitimate source publishers remain intact. Historical prompts, evidence, IDs and folios stay audit data rather than learner copy.

No new previews were generated during 8O because no changed design is proposed. Exact copy/brand values and the documented requirements govern implementation rather than generated text/colour approximations.

## Disposition of 8N open items

The following dispositions are explicit terms of the complete package now presented for final approval. They do not invent an earlier approval or silently harmonise a design.

| Item | Disposition presented for approval | Remaining proof / owner |
|---|---|---|
| Filter chip shapes and Sources icons differ slightly between approved boards | Retain the individually approved state-specific variants. No new global chip/icon design is selected. A later proposal to harmonise them needs an imagegen revision and approval | 9L/T09 compares each implemented state to its approved reference; no hidden replacement |
| Enlarged-text raster differs in phone width/scale and example font | Accept it as the documented illustration of reflow intent, not a precise measurement. Existing shared body-family and same-viewport/user-scale requirements remain binding | 9L/T09/T10 proves actual font family, scale, equation reading and reflow; changed visual consolidation requires preview/approval |
| Unbound hamburger/language controls, stray marks, OS/device frames and crop annotations | Exclude them as already documented in individually approved reviews. They add no new product functionality. “Lesson continues below” is a crop annotation, not teaching | 9L/T09 verifies no unsupported controls/features or lost lesson blocks |
| Official artwork only bound separately in 8J | Keep the approved placeholder-layout policy; bind the exact verified B1 asset, caption and reuse evidence. No generated artwork is an accepted substitute | 9C/9D/9F validates actual placement, geometry and accessibility; all 38 delivery holds remain open |
| Whole-package approval | Given on 15 October 2026: “yes approved”, including the specification, indexed previews and documented dispositions | 8O/step 8 complete; step 9 not started |
| Proposed questions, current guidance and device/platform behaviour | Remain future implementation/release acceptance work, not design-package failures or waivers | 9D–9J/9O and T01–T10; no active-pool promise or bypass of quotas/holds |

No additional unaddressed design-scope gap was identified. Final approval includes the documented dispositions above; the design-approval gate is satisfied. Any future visual changes, including chip/icon harmonisation, require an affected imagegen revision and renewed approval.

## Requirements that approval does not waive

- Import the complete approved curriculum and production corrections, not only the cropped sample text. Preserve law/advice/assumption distinctions, hidden-answer semantics, full tables/calculations/illustrations and scoped references.
- Keep exact source attribution, retained dates and model/commercial/editorial limits. Recheck time-sensitive affected guidance during implementation. Source approval here does not claim websites were freshly checked.
- Use original official sign bytes/geometry and retained reuse evidence. No recolouring, redrawing, thickening, similar-signal substitution or generated replacement. SIG16–18 retain explicit unavailable exact entries and distinct official actions.
- Preserve both quiz feedback modes, exact shuffled identity/version/score, the unfinished-test guard and valid return context. The proposed fuel question is not accepted for live scoring; historical compatibility does not add a saved-history feature.
- Keep no-primary-question lessons available. No fabricated completion, bookmark/history data, new persistence or public deep-link scheme. Missing results opens setup only after deliberate action, without auto-start or invented score.
- Verify actual rendering, fonts, large text, source/reference return, keyboard/focus, screen-reader behaviour, asset delivery and configured platforms. Existing content/asset/device holds remain open until their own acceptance checks pass. Print remains deferred.

## Approval record and next action

**Final package approval:** Given on 15 October 2026. User statement: “yes approved”. Scope: this complete design package, the specification, exact indexed preview revisions and documented visual-variant dispositions. 8O and step 8 are complete. Content/scoring, source currency, artwork delivery, device/runtime acceptance and the 38 image-delivery holds remain subject to their recorded requirements.

A separate request is required before step 9 implementation. No implementation was started by this approval.

## Reproduce the stored checks

From the repository root:

```sh
python3 docs/curriculum/app-design/8o/verify_design_package.py
```

The checker reads the fixed approved package and source records and writes only `app-design/8o/verification.json`. It does not mutate previous approvals, regenerate images or content, browse sources, run app tests or grant final approval. The independent final-approval record belongs in this report; the machine check deliberately leaves that field unset.
