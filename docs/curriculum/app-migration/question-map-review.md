# 7C — Question-to-teaching and source mapping

**Completed:** 14 October 2026. All 1,000 baseline questions appear exactly once, in bank order, with canonical lesson targets, approved-book passage evidence and source associations. No unmatched or ambiguous mapping remains. Question quality/dispositions remain 7D; this step does not edit the bank or implement the app.

**Approved release:** tagged screen edition, 578 pages, SHA-256 `78a89d8ffbb83b6e9eec6193396871ac2fb9feccf245b85112809646dd595581`. The user explicitly approved 6N and authorised 7C; print masters/proof are deferred. [Release approval](../pdf-production/final-review/screen-release.json).

## Deliverables

- [Question map](question-map.json): primary/related lessons, sign/reference targets, source IDs, passage evidence, retained claim limits, arithmetic assumptions and findings for every question.
- [Approved-page extraction](question-map-evidence.json): exact text, page hashes and actual external-link targets for every cited page.
- [Independent acceptance checks](question-map-checks.json): complete IDs/order, frozen input hashes, destination resolution, passage/page identity and retained qualifications.
- [Refreshed 7A baseline](baseline.json) and [7B registry](curriculum-map.json), with their provisional snapshots retained under history/.

## Evidence transfer and mapping decisions

Reused H7 keyed-answer-selection decisions only after confirming the unchanged question-bank hash and prompt/options/key parity, then comparing every saved teaching passage against freshly extracted approved PDF text. All historical passages match after whitespace normalization except the two records citing page 193 (`situation-105` and `situation-126`). Those now carry the exact approved correction from “actions after a collision … M10-L01” to “actions after a wildlife collision … M10-L02”; no unrelated text difference is accepted. All 55 reviewed claim/source associations retain their scope limits.

For ordinary questions, actual teaching-page headers identify lessons. Six curated exceptions select the more specific teaching topic: overtaking (`situation-039`), road workers (`108`), trapped-on-tracks response (`112`), snow-cloud visibility (`115`), Vision Zero (`129`) and pre-journey checks (`168`). Original H7 primary folios and all supporting pages remain evidence. Answer/review pages do not become substitute app lesson IDs.

All 616 sign questions retain exact `sign-<code>` destinations for 308 codes and their canonical reference groups. Where the supporting sign appears inside a lesson, that lesson is primary; otherwise its reference group selects a reviewed decision-topic lesson. Related lessons retain useful teaching connections. Exact official caption sources, source-register IDs and provenance are carried with each record; English bank labels are not silently substituted for official Swedish captions.

App navigation uses `primary_lesson_id`, `related_lesson_ids` and `reference_ids`. PDF folios remain supporting evidence. `source_ids` resolve through 7B, while `source_reference_ids` resolve through the map’s URL registry; these evidence references are not invented app destinations. Legacy bank page fields and the old chapter model are reserved for 7E.

## Totals and qualifications

| Measure | Result |
|---|---:|
| Baseline questions, unique and ordered | 1,000 |
| Covered under retained keyed-answer criterion | 1,000 |
| Unmatched / ambiguous mappings | 0 / 0 |
| Sign questions / exact codes | 616 / 308 |
| Scenario questions / retained claim-linked questions | 178 / 55 |
| Calculation/rule application questions | 206 |
| Lessons with primary questions | 37 of 40 |
| Distinct source URLs | 404 |
| Fuel-rounding qualifications carried to 7D | 4 |

The four qualified IDs are `fuel-saving-150-0.5`, `fuel-saving-150-1.5`, `fuel-saving-250-0.5` and `fuel-saving-250-1.5`. Page 299 discloses the one-decimal ties-to-even keyed answers; the prompts still omit the precision/convention. Coverage is not a finding that those prompts are unambiguous.

No question-quality decision is inferred from coverage. Official references retain their recorded dates and scope; 7C did not refetch external sites or independently revalidate current law. Manufacturer technical cautions, foreign guidance, hosted research and the commercial stopping shortcut retain their separate classifications. Exact/rough reaction equations, squared-speed braking, supplied delays, fuel arithmetic and load conventions remain editorial applications with their printed assumptions. Agency context is not an assertion that an authority prescribed an editorial formula.

## Coverage by lesson

Primary counts partition all 1,000 questions; related counts overlap. A zero count is a bank sampling gap, not missing teaching or an unmatched question. M01-L01 and M10-L03 have no mapped questions; M07-L04 appears as a related lesson once but has no primary question. Carry these into 7D/7F when considering future question coverage.

| Lesson | Exact title | Primary | Related | Bank sampling gap |
|---|---|---:|---:|---|
| M01-L01 | Your route into driving | 0 | 0 | No primary questions |
| M01-L02 | Am I ready today? | 9 | 0 | — |
| M01-L03 | Pressure is a driving risk | 5 | 0 | — |
| M01-L04 | Plan the journey before the ignition | 2 | 0 | — |
| M02-L01 | Know what the controls tell you | 8 | 1 | — |
| M02-L02 | A check before moving | 4 | 0 | — |
| M02-L03 | Protect everyone inside | 6 | 0 | — |
| M02-L04 | Move with control | 1 | 0 | — |
| M03-L01 | Recognise what a sign asks | 57 | 40 | — |
| M03-L02 | Combine the instructions | 66 | 4 | — |
| M03-L03 | Find your way without rushing | 148 | 14 | — |
| M03-L04 | Leave room to respond | 127 | 7 | — |
| M04-L01 | Decide who goes first | 22 | 13 | — |
| M04-L02 | Turn with a complete picture | 18 | 5 | — |
| M04-L03 | Crossings belong to people | 25 | 12 | — |
| M04-L04 | Choose a safe path through a roundabout | 9 | 14 | — |
| M05-L01 | See the person behind the movement | 21 | 4 | — |
| M05-L02 | When the street changes purpose | 35 | 0 | — |
| M05-L03 | Choose a lawful place to stop | 94 | 8 | — |
| M05-L04 | Manoeuvre where people may appear | 2 | 2 | — |
| M06-L01 | Read the rural road | 40 | 9 | — |
| M06-L02 | Is passing worth the risk? | 8 | 8 | — |
| M06-L03 | Join faster traffic calmly | 20 | 8 | — |
| M06-L04 | Expect an interrupted route | 49 | 2 | — |
| M07-L01 | Drive within what you can see | 7 | 1 | — |
| M07-L02 | Grip is a changing resource | 24 | 1 | — |
| M07-L03 | Protect your attention | 4 | 5 | — |
| M07-L04 | Change the plan when risk grows | 0 | 1 | No primary questions |
| M08-L01 | Understand what you may drive | 17 | 30 | — |
| M08-L02 | Make the load part of the safety check | 67 | 5 | — |
| M08-L03 | Keep the car legally ready | 6 | 0 | — |
| M08-L04 | Know what assistance cannot do | 1 | 2 | — |
| M09-L01 | Look beyond the exhaust | 11 | 0 | — |
| M09-L02 | Use energy with foresight | 49 | 2 | — |
| M09-L03 | Choose the journey as well as the car | 1 | 0 | — |
| M09-L04 | Check where the vehicle can go | 11 | 2 | — |
| M10-L01 | When the car cannot continue | 18 | 2 | — |
| M10-L02 | When someone may be hurt | 6 | 2 | — |
| M10-L03 | Explain a whole journey | 0 | 0 | No primary questions |
| M10-L04 | Make a realistic readiness plan | 2 | 2 | — |

## Reproduce and verify

From the repository root (use the documented bundled interpreter for PDF extraction):

```sh
python3 docs/curriculum/app-migration/build_question_map.py
python3 docs/curriculum/app-migration/verify_question_map.py
```

To independently refresh the saved teaching-page extraction, run the builder with `--extract` using pypdf 6.10.0 in the bundled Python environment, then rerun the verifier. Changing the extraction version can change whitespace/text hashes and requires review. The builder never changes the bank, app or PDF.

The acceptance checker passed against all frozen inputs and all 1,000 records. Rebuilding the mapping is deterministic. No Gradle/runtime tests were required for this planning-data change. Step **7D** is next and has not started.
