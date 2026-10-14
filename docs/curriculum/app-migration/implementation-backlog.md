# 7F — Implementation backlog

**Completed:** 14 October 2026. Planning only. The live app, question bank, assets and approved PDF are unchanged. Steps 7G–10 have not been executed.

[Structured tasks and all 1,000 assignments](implementation-backlog.json) · [Preview handoff](preview-handoff.md) · [Exact preview content](preview-content.json) · [7F checks](handoff-checks.json)

Run 7G next. Step 8 remains a separate imagegen design request requiring explicit approval before implementation. Every task below is future step 9 work and inherits that gate. New paths are marked `(new)`; audit records are inputs, not app runtime payloads.

## Scope and decisions

Preserve the baseline 1,000 question IDs / 500 concepts: 336 retain, 626 rewrite, 38 replace, zero remove. The JSON assigns each exact ID to one content owner and its 7C/7D evidence. Sign rewrites are bounded batches of at most 50 IDs; shared semantics applies to all 616 sign questions. The 134 distractor changes are overlapping work, not additional questions.

**SIG16–18 decision:** retain 7E’s explicit unavailable internal route, recorded official-description action and optional M03-L02 related teaching. Do not add a registry entry, asset or similar-signal alias. This resolves the planning choice while keeping the exact-entry gap visible. Adding exact entries later requires the content/asset verification workflow and a refreshed package.

**Release holds:** all 626 rewrites require acceptance; the 38 replacements additionally require exact-code delivery/accessible-equivalent proof. No release may silently omit held questions, fill quotas with unaccepted items or claim all 1,000 are active. Failure returns a bounded content/ID decision. These implementation holds are not cleared by this document.

**Learner data:** no durable store exists to migrate. Implement the audited transient-state contracts; future persistence/hot replacement is conditional separate scope. Do not build a new database or history feature as part of this plan.

## Executable work items

### 9A — Freeze the accepted input package and import schema

**Depends on:** approved planning/design gate.

**Affected files:** `tools/build_content.py`, `content/curriculum.json (new)`, `content/content-manifest.json (new)`, `composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt`, `composeApp/src/commonMain/kotlin/se/korkort/Curriculum.kt (new)`.

**Output:** A typed content contract and deterministic import boundary using 7B fields, stable option IDs, semantic question revisions and asset/source bindings. Freeze all 7A–7F identities before any live generation.

**Acceptance:**

- Fail on changed approved PDF/manuscript/registry, question or asset hashes until the affected audit is refreshed.
- Separate curriculum release from app package version; bind teaching, accepted questions, sources, assets and aliases by manifest digest. PDF hash alone is insufficient.
- Represent block types, hidden/revealed answer blocks, canonical IDs, source scopes, eligibility and pre-/post-answer image semantics. Keep compile-time Kotlin delivery unless a separately reviewed loader change is needed.
- Generator writes deterministically to explicit outputs, fails duplicate/unknown IDs and emits source-to-output traceability. No runtime JSON loader is assumed.

### 9B — Import the complete approved teaching and references

**Depends on:** 9A.

**Affected files:** `tools/build_content.py`, `content/curriculum.json (new)`, `composeApp/src/commonMain/kotlin/se/korkort/Curriculum.kt (new)`, `composeApp/src/commonMain/kotlin/se/korkort/Chapters.kt`.

**Output:** Full independently written curriculum, not old summaries: ten module introductions, forty lessons, ten reviews, four appendices and twenty-four reference groups; preserve all 519 supporting anchors and registry targets.

**Acceptance:**

- Read each 7B source_location and final chapter/reference production corrections, including the page-193 wildlife reference; preserve exact approved titles/order.
- Preserve tables, examples, assumptions, knowledge checks, answer blocks and source/illustration placements. Every imported block has an origin locator; compare normalized content to approved production sources.
- Resolve all 1,123 published IDs (88 curriculum, 400 signs, 116 sources, 519 supporting anchors); supporting/front-matter anchors need not become top-level library cards.
- Keep legacy aliases separately; remove the 39 old summary payloads and unused 178 Topic summaries from learner content without importing court-case narratives.

### 9C — Import scoped sources, sign captions and exact verified assets

**Depends on:** 9A.

**Affected files:** `tools/build_content.py`, `content/curriculum.json (new)`, `content/sources.json (new)`, `composeApp/src/commonMain/composeResources/files/curriculum/ (new)`, `composeApp/src/commonMain/kotlin/se/korkort/Curriculum.kt (new)`.

**Output:** Sources and assets with exact paths/hashes, code/variant/caption bindings, credits and editorial-English notices. Register 404 question URL records alongside 116 canonical source destinations, retaining module-specific URL choices.

**Acceptance:**

- Copy the approved 400 sign bindings and all lesson illustrations with manifest hashes and reuse records; verify bundled-byte parity and all block references.
- Derive source title/publisher/classification/check date/scope from retained evidence, not domain guesses or a blanket official label. Preserve commercial, foreign, research, manufacturer and editorial limits.
- Use exact 7C source_reference_ids to find URL records and canonical source_ids for navigation. Retain per-source dates; unknown date is explicit, never invented.
- Verify F31a case and exact sign variants. Study alt text may explain meaning; do not reuse it as assessment alt text. No sign artwork redrawing or PDF changes.

### 9D — Add assessment identities, neutral descriptions and reveal semantics

**Depends on:** 9A, 9C.

**Affected files:** `tools/build_content.py`, `content/questions.json`, `composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt`, `composeApp/src/commonMain/kotlin/se/korkort/App.kt`, `composeApp/src/commonMain/kotlin/se/korkort/Bank.kt`.

**Output:** Author and review physical descriptions for every image in all 616 sign questions; stable authored option identity replaces code-bearing label uniqueness. Derive display letters after shuffling.

**Acceptance:**

- All sign stems/options use the 7D exact-code proposal and caption/source; remove matching-code cues before answering. Keep code/meaning in metadata and revealed feedback.
- Review every physical description against the visible image, without naming the correct meaning or including a target/option code. Cover keyboard, focus and assistive-technology reading order and equivalent access.
- Assert unique option identity and distinct asset choices, not unique code text. Audit 134 distractor-set changes in both paired directions.
- Check shuffle/key/option-feedback association for all four positions and both feedback modes; hidden feedback and study captions must not leak through accessibility semantics.

### 9E — Apply the 578 sign rewrites

**Depends on:** 9D.

**Affected files:** `content/questions.json`, `tools/build_content.py`, `composeApp/src/commonMain/kotlin/se/korkort/Bank.kt`.

**Output:** Apply the assigned 578 non-held sign rewrites using the exact 7D per-question proposal, sources and reviewed descriptions; preserve question/concept IDs.

**Acceptance:**

- Work in deterministic batches of at most 50 IDs from the assignment manifest; record before/after diff and acceptance evidence for each ID.
- Check all four choices and explanations against exact captions, including C6, E3, S7 and T24 when present; no substitution based on similar code or shape.
- New semantic revisions and acceptance flags are required. The 38 held replacements belong to 9F, not this batch.

### 9F — Resolve 38 faint-outline delivery holds

**Depends on:** 9D.

**Affected files:** `content/questions.json`, `composeApp/src/commonMain/composeResources/files/curriculum/ (new)`, `content/content-manifest.json (new)`, `composeApp/src/commonMain/kotlin/se/korkort/App.kt`, `docs/curriculum/app-migration/implementation-evidence/ (new)`.

**Output:** Nineteen exact codes, two question directions each, with reviewed intended-size delivery, zoom/accessibility and asset evidence. This task also enforces proof for any retained faint image elsewhere in an option set.

**Acceptance:**

- Process the exact 38 assigned IDs and their 7D research_holds. Original 105 dp options / 180 dp stems are baseline constraints, not approved final sizes.
- Use an exact legible official rendition or approved framing with unchanged geometry; never silently thicken, recolour, redraw or use a generated substitute. Record source/hash and pair consistency.
- Prove actual display and accessible equivalent on each supported target, light/dark surfaces and text scaling; include smallest approved image size and zoom return behaviour.
- Until proof passes, item is ineligible for scored use. If proof fails, return an explicit alternative-item/ID decision; do not silently drop an item or weaken quotas to ship.

### 9G — Apply the eight scenario corrections

**Depends on:** 9A.

**Affected files:** `content/questions.json`, `tools/build_content.py`, `composeApp/src/commonMain/kotlin/se/korkort/Bank.kt`.

**Output:** Apply the exact 7D draft patches for situations 032, 045, 105, 107, 125, 162, 172 and 178.

**Acceptance:**

- Review every changed option explanation as well as stem/key: weekday times, car lighting scope, conditional rural return, emergency braking, prompt notification, ready weight, inspection bans and personal-injury cover.
- Compare each full resulting question to question-actions.json; preserve cited limits and IDs/concepts and assign new semantic revisions.
- Recheck time-sensitive rules at implementation against primary sources; record dates/evidence if guidance changed and refresh affected decisions before acceptance.

### 9H — Apply the thirty load definitions

**Depends on:** 9A.

**Affected files:** `content/questions.json`, `tools/build_content.py`, `composeApp/src/commonMain/kotlin/se/korkort/Bank.kt`.

**Output:** Apply all 30 driver-inclusive ready-weight prompt drafts; retain the existing numeric answers.

**Acceptance:**

- Define Swedish tjänstevikt consistently and avoid a driver-excluding interpretation of unladen.
- Recalculate displayed inputs and all four numeric options independently; assert original numeric keys unchanged and each revised prompt has one answer.

### 9I — Apply four exact fuel tasks and six unit fixes

**Depends on:** 9A.

**Affected files:** `content/questions.json`, `tools/build_content.py`, `composeApp/src/commonMain/kotlin/se/korkort/Bank.kt`.

**Output:** Apply the four exact-result draft questions and six 1-litre grammar drafts from 7D.

**Acceptance:**

- Independently recompute Decimal keys 0.75, 2.25, 1.25 and 3.75 litres for the four midpoint questions; verify distinct false alternatives and every explanation.
- Prompts explicitly request no rounding; preserve hypothetical measured-rate assumptions. Six grammar-only fixes keep numeric keys.
- Preserve IDs/concepts; old attempts retain old values/snapshots and scores. Never regrade an earlier rounded answer against a new key.

### 9J — Assemble accepted questions and verify selection capacity

**Depends on:** 9E, 9F, 9G, 9H, 9I.

**Affected files:** `content/questions.json`, `content/content-manifest.json (new)`, `tools/build_content.py`, `composeApp/src/commonMain/kotlin/se/korkort/Bank.kt`, `composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt`.

**Output:** Versioned active question package: 336 retained assessments plus 626 reviewed rewrites and 38 proven replacements. Exact 7C relationships for every baseline ID; zero removals by default.

**Acceptance:**

- Use the machine-readable assignments as an exhaustive partition of 1,000 baseline IDs / 500 concepts; retained assessment fields stay unchanged except relationships/package metadata.
- Active questions must all have completed acceptance; no unreviewed fallback items. Derive visible counts from accepted package, not the old advertised 1,000.
- Preserve five category IDs/labels, 7/5/16/32/5 plus five random at 70, existing largest-remainder allocation for 1–70 and concept uniqueness. Verify per-category capacity and random residual after quota picks for every length.
- Check deterministic generation JSON/Kotlin parity, no missing links or duplicate option identities; selection/shuffle across fixed seeds exercises all key positions. Insufficient accepted capacity is a release blocker.

### 9K — Implement typed routes, aliases and explicit signal fallback

**Depends on:** 9B, 9C.

**Affected files:** `composeApp/src/commonMain/kotlin/se/korkort/App.kt`, `composeApp/src/commonMain/kotlin/se/korkort/Curriculum.kt (new)`, `content/legacy-aliases.json (new)`, `tools/build_content.py`.

**Output:** One validated internal resolver and transition guard covering every 7E route/alias. SIG16–18 keep the explicit unavailable-exact-entry policy; no new approved sign IDs.

**Acceptance:**

- Cover all 1,000 question routes, 39 chapter aliases, 361 integers including 38 gaps, 178 topic identities and 343 sign records using frozen namespace legacy-app-4768933c3d9a.
- Question identity beats page. Known single aliases open exact content; multi-target aliases show canonical choices. Unknown question/namespace/title/page never guesses nearest/first content.
- SIG16, SIG17 and SIG18 have no exact internal destination: show recorded 7E message, recorded official URL action and optional M03-L02 related teaching. Keep them separate from the 340 exact-code entries. External link failure leaves a usable unavailable/library state.
- Known removed-block parent gets moved-passage notice; retired one/many/none use reviewed replacement offer/chooser/unavailable. Production tombstones stay empty.
- All eight navigation states and twelve entry-point rules use the same unfinished-quiz guard and valid return context. No public deep-link parser or new platform URL scheme.

### 9L — Implement approved library, reader, reference and sources views

**Depends on:** 9B, 9C, 9J, 9K.

**Affected files:** `composeApp/src/commonMain/kotlin/se/korkort/App.kt`, `composeApp/src/commonMain/kotlin/se/korkort/Chapters.kt`, `composeApp/src/commonMain/kotlin/se/korkort/Curriculum.kt (new)`.

**Output:** Step 8 approved presentation of canonical library, complete lesson reader, answer/review reveal, sign/reference detail and dedicated sources area.

**Acceptance:**

- Implement only after explicit approval of step 8 imagegen previews; use preview-handoff.md exact fixtures and record approval/version. Revisions to design require another approval.
- Display ten modules/four lessons each/reviews; five category filters use all forty 7E lesson tags, retaining canonical order and all zero-question lessons. Search uses canonical content.
- Previous/next follows all 60 reading nodes; sources/signs/appendices return to validated origin; hide answers until deliberate reveal.
- Apply all fourteen 7E learner-label replacements, actual accepted counts, exact source attribution and official-art/editorial-English notices. No old book titles, chapter labels or source folios in learner views.
- Handle empty search, unavailable content, multi-target chooser, long content, tables, zoom, keyboard focus and large text without losing approved meaning.

### 9M — Preserve quiz sessions and versioned transient state

**Depends on:** 9A, 9J, 9K.

**Affected files:** `composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt`, `composeApp/src/commonMain/kotlin/se/korkort/App.kt`.

**Output:** Implement all 22 state contracts without adding a database or inventing a saved-data migration.

**Acceptance:**

- Preserve immediate/end feedback, answers, score, index and review filters with exact shuffled option identity and package revision. Keep quit confirmation for every outbound target.
- Default compile-time upgrade/restart clears transient remember/session state as before. Missing results/review context shows no saved result and a setup action.
- Do not add hot replacement. If separately chosen later, pin the full old session/option order/keys/feedback/package through finish/quit/review and switch atomically at safe idle.
- No durable bookmarks, completion or answer history currently exists. Future-store compatibility follows 7E: no automatic completion credit, no same-ID regrade, no reinterpretation of unversioned shuffled indices. Treat it as separate authorized scope.

### 9N — Close assessment coverage briefs without changing the baseline bank

**Depends on:** 9B.

**Affected files:** `docs/curriculum/app-migration/assessment-coverage-briefs.md (new)`.

**Output:** Reviewable additional-assessment briefs for M01-L01, M07-L04 and M10-L03; keep the baseline bank at 1,000 and preserve all teaching.

**Acceptance:**

- M01-L01: preparation/entitlement/training checklist, recheck current official requirements before authoring; zero primary and zero related questions today.
- M07-L04: combined-risk decision to adapt/stop/change route; zero primary and one related question today.
- M10-L03: whole-journey explanation/reflection with a rationale/rubric; consider the approved existing practice/reflection format rather than forcing an MCQ; zero primary and zero related questions.
- State objective, source, proposed format, plausible mistakes and acceptance rubric for each brief. Additional scored items/new IDs require a separate explicit content decision and updated counts/coverage; do not replace unrelated baseline IDs.

### 9O — Integrate platform packaging, provenance and release evidence

**Depends on:** 9J, 9L, 9M, 9N.

**Affected files:** `README.md`, `tools/build_content.py`, `composeApp/build.gradle.kts`, `composeApp/src/commonTest/kotlin/se/korkort/ (tests)`, `docs/curriculum/app-migration/implementation-evidence/ (new)`, `content/content-manifest.json (new)`.

**Output:** A reviewable release candidate, accurate learner feature claims and step 10 evidence inventory.

**Acceptance:**

- Replace README stale 37-chapter/supplied-book feature claims using accepted manifest; retain technical provenance/audit history and required artwork/source credits.
- Run meaningful common tests and build/resource checks for Android, desktop, iOS device/simulator and wasm targets configured in composeApp/build.gradle.kts; record exact commands and unavailable tooling honestly.
- Verify packaged files/hashes and offline teaching/assets; official URLs remain external. Do not add persistence, remote loader, analytics, URL schemes or new platforms.
- Record unresolved device/platform checks as release blockers, not successful checks. Step 10 runs the matrix below; step 9 completion alone does not certify the app.

## Step 10 verification specification

These are required future checks, not results. Save actual commands, expected/observed results, release manifest digest, devices and attachments. A missing platform run stays open. Each work item is covered below; the structured coverage map also binds every 7B destination, 7D issue/shared dependency/coverage brief and 7E record family to owners.

- **T01 — Manifest/import parity** (9A, 9B, 9C): Compare complete imported blocks with production-source origins; all 1,123 IDs unique/resolving, 400 exact signs, all illustrations/tables/answer blocks, correct titles/order and approved page-193 correction. Verify deterministic generated Kotlin and packaged hashes.
- **T02 — Scoped sources and references** (9C, 9K, 9L): Exercise official law, foreign guidance, research, commercial shortcut, manufacturer and editorial arithmetic. Compare all exact question source-reference URLs and scoped canonical aliases to retained evidence; actual publisher/date/limits, valid return context, offline/unreachable external URL behaviour.
- **T03 — Assessment visuals and accessibility** (9D, 9E, 9F): Inspect every revised sign asset/variant/physical description, all 134 distractor changes and 38 holds. Test smallest approved size, zoom, light/dark, keyboard/screen reader and large text on supported platforms; no code/answer leak pre-answer, no generated replacement artwork.
- **T04 — Question content and calculations** (9G, 9H, 9I, 9J): Diff all 1,000 assigned IDs, assert 336 assessment payloads unchanged, review all 626 rewrites/38 replacements against per-ID acceptance; independent numeric audit including four exact keys, 30 driver-inclusive definitions, six grammar fixes and eight scoped scenarios. No unaccepted active item.
- **T05 — Quiz engine and answer identity** (9D, 9J, 9M): Check every length 1–70, category quotas/rounding, concept capacity after quota picks, random residual, unique concepts and stable shuffled option identities. Both feedback modes, all key positions, next/end/results/review filters and actual accepted counts; old rounded-answer snapshot retains its own score.
- **T06 — Legacy/unknown routes** (9K): Run all 7E actual/synthetic examples plus full 39/361/178/343 alias tables. Same old page 46 with two question IDs gives different correct lessons; gaps, unknown question, wrong namespace, invalid number and case-sensitive F31a. SIG16–18 unavailable with exact official actions, never SIG1/SIG5/Y1 substitutions.
- **T07 — Navigation and state** (9K, 9L, 9M): All eight states/twelve entry points, 60 reading-node previous/next edges and related/reference return contexts. Exit unfinished test guard, missing session setup, moved block parent notice, retired one/many/none. Restart clears only existing transient state; no fabricated migrated progress or auto-credit.
- **T08 — Library and teaching coverage** (9L, 9N): All ten modules/forty lessons/ten reviews, four appendices and 24 reference groups; all five filters and forty tags preserve canonical order. Search/empty states; zero-question lessons remain available and three additional-assessment briefs explicit, no new baseline IDs.
- **T09 — Design approval and learner copy** (9L, 9O): Compare implemented library/reader/review and fallback/source states with explicitly approved step 8 preview revision. Check every one of fourteen replacement rules across visible copy and accessibility semantics; no old book name/chapter labels/folios. Legitimate source publisher names remain in sources/credits.
- **T10 — Platform/package release** (9C, 9F, 9O): Build/test Android, desktop, iOS device/simulator and wasm as configured; installed resource/offline and source-link smoke checks, image legibility/accessibility on actual supported devices. Save commands, versions, devices and evidence; unsupported execution stays open, no success inferred from compilation.

## Rebuild and local handoff checks

From the repository root:

```sh
python3 docs/curriculum/app-migration/build_implementation_handoff.py
python3 docs/curriculum/app-migration/verify_implementation_handoff.py
```

The builder only writes the four 7F handoff artifacts. The verifier checks input identities, exhaustive question ownership, destination/issue/state coverage, dependency ordering, exact fixtures and protected baseline bytes. This is a bounded 7F handoff check; the independent full-package 7G verification remains pending.
