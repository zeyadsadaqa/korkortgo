# 7D — Practice-question dispositions

**Completed:** 14 October 2026. Every baseline question has one disposition, a rationale and teaching/source evidence. Proposed changes have concrete acceptance criteria; visual replacement holds are explicit. This is a planning review: the live question bank, generated Kotlin, app sources, official assets and approved PDF remain unchanged. 7E has not started.

## Decisions

| Disposition | Questions | Meaning |
|---|---:|---|
| Retain | 336 | Keep assessed prompt/options/key/explanations; migrate links and content metadata separately. |
| Rewrite | 626 | Preserve the learning outcome/IDs; apply the recorded wording, feedback, precision or assessment-semantics changes later. |
| Replace | 38 | Replace faint-outline image-question delivery for 19 exact sign codes; keep meaning/code identity and hold scored use until proof passes. |
| Remove | 0 | No baseline question requires retirement on the reviewed evidence. |

The large rewrite count is mainly a shared sign-question revision, not 626 incorrect keyed answers. There are 578 sign rewrites and 48 other rewrites: eight scenarios, 30 load prompts, four fuel-precision tasks and six singular-unit fixes. The 38 replacements are the remaining sign questions.

- [All 1,000 decisions and reviewable proposals](question-actions.json)
- [Acceptance checks](question-actions-checks.json)
- [Independent arithmetic audit](question-review/arithmetic.json)
- [Asset/variant review and proof-sheet index](question-review/asset-review.json)
- [Targeted primary-source rechecks](question-review/source-rechecks.json)

## Review scope

Reviewed all 178 scenario stems, all four choices and their option-specific explanations; all 308 sign codes in both meaning/recognition directions; and all 206 calculation/rule instances. All ten paired bank/approved-art sheets were inspected. No code/family mismatch or exact duplicate option bitmap was found in those checks; overview inspection is not actual-device legibility proof. The 7C teaching/claim decisions and dates are retained as evidence, with current targeted primary-page checks for flagged rules. This is not a claim that all 404 source URLs were independently revalidated in 7D.

The record for each question carries its original content, disposition, rationale, 7C evidence pointer, proposed patches or replacement brief, acceptance criteria, applicable arithmetic review and any hold. Disposition is separate from the earlier finding that all questions have teaching coverage.

## Sign-question changes

All 616 sign tasks need assessment-specific copy and image semantics. The current recognition stem includes the target code and image accessibility labels include option codes, allowing a matching-code answer without recognition. Meaning-question images have only a generic description. The study-caption alternatives include meanings and therefore cannot simply be copied into a pre-answer question.

Proposals remove source codes from pre-answer prompts and option labels, retain them in metadata/revealed feedback, align concise answer labels and explanations with the exact approved caption, and require physical descriptions of the visible illustration. This also replaces ambiguous or overly broad terminology such as E3 “Clearway”, C6’s blanket trailer prohibition, S7’s incomplete vehicle category and T24’s generic “Charging station”. Of the 308 labels, 220 differ from the approved editorial label; many differences are synonyms, not factual errors.

Each proposed option has an exact official asset/hash, caption/source binding and revealed explanation. The JSON contains briefs, not a ready-to-import question payload: neutral physical descriptions still need authoring and intended-size/accessibility acceptance. Display letters must be assigned after option shuffling. Distinct option IDs/assets must replace any validator reliance on code-bearing text. A study/reference card may continue to reveal code and meaning; the assessment must distinguish pre-answer and revealed states.

The following 19 target codes have faint outline details in the inspected artwork: `S1`, `S10`, `S11`, `S12`, `S13`, `S2`, `S3`, `S4`, `S5`, `S6`, `S7`, `S8`, `S9`, `T1`, `T2`, `T22`, `T6`, `T8`, `X8`. Their two directions total 38 replacements with explicit asset/display holds. Current image options are allocated 105 dp and question images 180 dp on white surfaces in App.kt; a contact sheet cannot certify these at device size. The approved PDF remains unchanged.

Do not redraw, thicken or recolour official signs as an unverified substitute. Use a legible exact official rendition or approved framing of the preserved geometry and prove intended-size display/zoom and accessible equivalents. If this cannot be achieved, bring back an alternate-item/ID decision. The proposal also swaps faint **distractor** illustrations for distinct verified alternatives, keeping the paired question directions consistent; 134 records include that option-set change. New visual presentation follows step 8’s preview/approval workflow.

## Scenario corrections

| Question | Correction |
|---|---|
| `situation-032` | Feedback drops the weekday condition from the parenthesised-times rule. |
| `situation-045` | The unqualified lighting question omits the daylight-motorcycle exception; scope the task to the intended car audience. |
| `situation-105` | The alternative route needs the approved lesson’s explicit legality, safety and no-suitable-return limits. |
| `situation-107` | Avoid sudden braking needs an emergency exception and gradual gap adjustment. |
| `situation-125` | State the prompt notification duty without suggesting an extended owner-search delay. |
| `situation-162` | Unladen is an ambiguous translation without the Swedish ready-weight convention. |
| `situation-172` | The keyed statement vaguely describes the ban’s end and omits the distinction between ordinary driving and limited permitted trips. |
| `situation-178` | Clarify that compulsory insurance includes driver/passenger personal injury while excluding own-car damage. |

Exact draft field patches and the resulting full question are saved for all eight rows in question-actions.json. In particular, the fog-light question now specifies an ordinary passenger car; rural-turn advice retains legality/safety and no-suitable-return limits; following-driver advice does not delay emergency braking; and unattended-property notification is prompt.

## Arithmetic and terminology

All 206 displayed numerical/rule prompts were independently parsed and recalculated with Decimal arithmetic. All current keys agree with the printed model/display convention; four fuel midpoint keys require the already disclosed qualification. No erroneous numeric key is asserted merely because an exact value differs from a rounded display. All four options were checked for numeric distinctness.

For those four prompts, the proposed task asks for the **exact result without rounding**, with consistent replacement choices and explanations:

| Question | Current displayed key | Proposed exact key |
|---|---|---|
| `fuel-saving-150-0.5` | 0.8 litres | 0.75 litres |
| `fuel-saving-150-1.5` | 2.2 litres | 2.25 litres |
| `fuel-saving-250-0.5` | 1.2 litres | 1.25 litres |
| `fuel-saving-250-1.5` | 3.8 litres | 3.75 litres |

These are substantive answer-value revisions: retain IDs/concepts with a new content revision, and specify treatment of earlier answers/history in 7E. Do not rewrite the approved book solely to erase its historical rounding explanation; it also teaches the exact results.

All 30 load tasks now propose an explicit definition of tjänstevikt as the stated ready-for-service weight already including the driver. Their numeric answers remain unchanged. This prevents the English term “unladen” from implying a driver-excluding base. Six fuel items need only “1 litre” agreement; values and keys remain unchanged. Rough stopping equations remain labelled as supplied exercise models; braking scaling retains model assumptions, and time gaps are arithmetic inputs rather than universal safety guarantees.

## Holds and follow-on work

The 38 asset/display holds must be resolved before the replacement questions enter scored use. They do not dispute the verified sign meanings or reopen 6N. No unrecorded answer ambiguity or factual research hold remains; future implementation acceptance is still required for every draft. No question is approved for immediate bank modification by this document.

The three 7C sampling gaps remain explicit future assessment briefs: M01-L01 administrative preparation, M07-L04 combined-risk plan changes, and M10-L03 whole-journey explanation/reflection. A reflection task may suit the last objective better than a forced MCQ. Do not retire unrelated questions simply to fill these gaps or invent baseline IDs. Carry them into 7F.

The source bank stores every correct answer at index zero, but QuizEngine.select calls Question.shuffled and remaps the key. This is not a reason to rotate stored keys. Preserve concept-based deduplication and verify shuffled-answer/semantics behaviour in implementation. Empty/old source and page fields are handled through the 7C map and 7E link rules; they are not a reason to preserve the old book structure.

## Current official checks

These targeted checks supplement the retained local source/claim evidence. They do not upgrade foreign guidance, manufacturer cautions or commercial shortcuts into Swedish law.

- [7D-SRC-LAW](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/trafikforordning-19981276_sfs-1998-1276/) — Chapter 2 §§2–4,8; chapter 3 §49a,71. Rechecked instruction precedence, prompt notification after unattended property damage, parking-disc rule and lighting. Motorcycles in daylight are an explicit exception to the lighting-combination prohibition; scope question 045 to a car. No blanket legal revalidation of every chapter is claimed.
- [7D-SRC-TIME](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/tillaggstavlor/tidsangivelse/) — T6 explanation. Parenthesised times concern weekdays before Sundays/public holidays. Preserve the weekday restriction in question 032 feedback.
- [7D-SRC-WEIGHTS](https://www.transportstyrelsen.se/sv/vagtrafik/fordon/fordonsregler/vikter/) — Tjänstevikt bil, Totalvikt bil, Maximilast. Ready-for-service car weight includes the driver; maximum load is totalvikt less tjänstevikt. Define the English term in the 30 load prompts and question 162; do not subtract the driver again.
- [7D-SRC-INSPECTION](https://www.transportstyrelsen.se/sv/vagtrafik/fordon/aga-kopa-eller-salja-fordon/fordonsbesiktning/besiktningsregler/personbil-och-lastbil-som-inte-overstiger-3500-kg-i-totalvikt/) — Vehicle class and 36/24/14-month bullets. Confirmed ordinary light-vehicle inspection intervals for questions 170–171; no date/key change proposed.
- [7D-SRC-BAN](https://www.transportstyrelsen.se/sv/vagtrafik/fordon/aga-kopa-eller-salja-fordon/fordonsbesiktning/) — Vad händer om jag inte besiktar i tid? — Körförbud. Missed-deadline ban differs from dangerous-condition ban. Permitted limited trips depend on registration/vehicle conditions. Clarify question 172 feedback without implying that addressing paperwork permits ordinary driving.
- [7D-SRC-INSURANCE](https://www.transportstyrelsen.se/sv/vagtrafik/fordon/aga-kopa-eller-salja-fordon/trafikforsakring/) — Vad är en trafikförsäkring?. Confirmed own-car damage exclusion; personal-injury cover includes the driver and passengers. Clarify question 178 feedback.
- [7D-SRC-TYRES](https://www.transportstyrelsen.se/sv/vagtrafik/fordon/fordonsregler/dack/vinterdack/) — Light vehicles, seasonal dates, trailer studs and best tyres rear. Current light-vehicle tyre scope still supports the keyed seasonal/depth/stud relationships; heavy-vehicle rules are separate. No replacement key proposed.
- [7D-SRC-ALCOHOL](https://www.trafikverket.se/resa-och-trafik/trafiksakerhet/sakerhet-pa-vag/alkohol-och-narkotika-i-vagtrafiken/vad-sager-lagen-om-rattfylleri/) — Numerical limits and aggravated-offence criteria. Confirmed blood numerical thresholds and that aggravated assessment has other criteria. Retain questions 057–058.
- [7D-SRC-C6](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/forbudsmarken/forbud-mot-trafik-med-motordrivet-fordon-med-tillkopplad-slapvagn/) — C6 explanation. Retain trailer-type exceptions and supplementary-panel scope; replace the bank’s blanket trailer wording with approved caption wording.
- [7D-SRC-E3](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/anvisningsmarken/motortrafikled/) — E3 identity and advance-information condition. Use the approved expressway/motortrafikled terminology rather than ambiguous English clearway.
- [7D-SRC-T24](https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/vagmarken/tillaggstavlor/laddplats/) — T24 under E19. Retain the approved distinction between externally chargeable-vehicle parking qualification and a separate requirement to be actively charging.

## Reproduce

From the repository root:

```sh
python3 docs/curriculum/app-migration/audit_question_arithmetic.py
python3 docs/curriculum/app-migration/build_question_actions.py
python3 docs/curriculum/app-migration/verify_question_actions.py
```

The checker validates every decision/ID, proposal evidence and criteria, exact fuel keys, sign/source/asset bindings, proof hashes and all upstream frozen files. Rebuilds are deterministic. Gradle/runtime tests are reserved for implementation; this step changed planning artifacts only.

**Next:** 7E — plan link replacement, aliases and learner-state/version handling. It has not started.
