# Question coverage review

Reviewed all 1000 questions against the supplied 498-page curriculum PDF.

- Covered by book study: **697**.
- Missing required knowledge/illustrations: **233**.
- Solvable from the question’s numbers/formulas alone, but not taught in the book: **70**.
- Total without adequate book support: **303**.

| Question family | Covered | Missing knowledge | Prompt-only |
|---|---:|---:|---:|
| situation | 123 | 55 | 0 |
| sign | 458 | 158 | 0 |
| reaction | 36 | 0 | 0 |
| stopping | 0 | 0 | 30 |
| braking | 0 | 20 | 0 |
| gap | 20 | 0 | 0 |
| disc | 30 | 0 | 0 |
| load | 30 | 0 | 0 |
| fuel | 0 | 0 | 20 |
| fuel-saving | 0 | 0 | 20 |

## Files

- `question-page-map.json`: only supported questions, retaining prompts, options, answers, IDs and exact supporting pages.
- `question-coverage-gaps.json`: every unsupported question, with a specific reason and prompt-only distinctions.
- `all-question-coverage.json`: complete 1,000-record audit in original order.

Page numbers are one-based PDF positions, including the cover. The existing `page` in the bank belongs to the original source book and is retained only as `original_source_page`. `book_pages` lists actual support; `primary_book_page` is the first useful lesson page. Sign records also contain extracted entry evidence.

A broad chapter on a topic, a bibliography link or a code lookup does not establish answer coverage. Reasonable applications are labelled separately. Some supported questions have more detailed explanations than the PDF; the criterion is selecting the keyed answer, not reproducing every explanation.

The audit evaluates this PDF only. It does not verify the law, medical claims, the bank’s answer accuracy or external source content. Representative sign and calculation pages were visually inspected; this is not a visual inspection of every illustration.

## Scenario gaps

| ID | Missing teaching |
|---|---|
| situation-013 | The 50 km/h threshold is taught, but the bus yielding duty above it is not explained. |
| situation-045 | The book refers to prohibited lighting combinations without naming dipped headlights plus front fog lights. |
| situation-062 | Stimulant drugs masking fatigue and producing overconfidence are not explained. |
| situation-068 | Microsleep is not defined. |
| situation-069 | Fatigue and stopping/rest planning are covered, but restorative sleep as the remedy for sleep deprivation is not taught. |
| situation-070 | Central vision and its role in reading fine detail are not explained. |
| situation-071 | Peripheral vision and movement detection are not explained. |
| situation-073 | The single-headlight illusion and the possibility of a wider vehicle with a failed lamp are not taught. |
| situation-075 | Speed adaptation after prolonged high-speed driving and the speedometer check are not taught. |
| situation-076 | The mechanism linking fossil carbon, carbon dioxide and climate change is not explained. |
| situation-077 | Catalytic-converter warm-up and cold-start effectiveness are not taught. |
| situation-078 | The distinction between catalytic pollutant removal and remaining fossil CO2 emissions is not taught. |
| situation-079 | Engine heaters and timer use are not covered. |
| situation-082 | Air-conditioning energy demand and its safe, economical use are not taught. |
| situation-083 | Car washing, wastewater treatment and preferred wash facilities are not covered. |
| situation-084 | Carbon monoxide and its effect on oxygen transport are not explained. |
| situation-085 | Nitrogen oxides, acidification, airway irritation and ground-level ozone are not explained. |
| situation-086 | Wear particles are mentioned, but respiratory health effects are not explained. |
| situation-088 | The high suitable gear principle for a conventional manual car is not taught; vehicle instructions are deferred to. |
| situation-090 | Engine braking in a conventional manual car is not defined. |
| situation-092 | The electric-car distinction between no tailpipe exhaust and production/energy-supply impacts is not taught explicitly. |
| situation-094 | Plug-in hybrids are mentioned, but external charging versus a non-plug-in hybrid is not explained. |
| situation-098 | Local studded-tyre restrictions and wear particles are mentioned separately; the specific studs/road-wear/air-quality link is not taught. |
| situation-099 | Removing roof equipment is taught, but unnecessary carried mass and its energy cost are not explained. |
| situation-104 | Keeping front wheels straight while waiting for a left turn is not taught. |
| situation-105 | The safer country-road left-turn alternative of continuing, turning around and returning for a right turn is not taught. |
| situation-106 | A timed gap is mentioned without the fixed-point counting method or the three-second guideline. |
| situation-107 | Increasing the forward gap to manage a tailgater and avoiding sudden braking are not taught. |
| situation-114 | Bridge cooling from above and below, and earlier freezing, are not explained. |
| situation-116 | Freezing rain forming a nearly invisible ice layer is not explained. |
| situation-117 | First rain after a dry spell mixing with road residues is not explained. |
| situation-119 | Guide dogs and avoiding distraction of a working dog are not covered. |
| situation-126 | Wildlife risks at dusk/dawn, habitats and fence openings are not taught. |
| situation-129 | Vision Zero and its no-death/no-serious-injury goal are not defined. |
| situation-131 | Head-restraint adjustment is mentioned without explaining neck protection or rear-impact head movement. |
| situation-132 | Rear-facing seats are recommended without explaining young children’s head/neck support and crash-force distribution. |
| situation-135 | The general definition of a bicycle as a vehicle is not taught explicitly. |
| situation-136 | The road-speed-limit treatment of a light lorry versus the heavy-lorry cap is not taught. |
| situation-138 | The square-of-speed braking-distance relationship is not taught. |
| situation-145 | Wheel imbalance as a cause of speed-dependent steering vibration is not covered. |
| situation-146 | Temporary spare-wheel use and its speed/distance/pressure limits are not taught. |
| situation-148 | Best-grip tyres are recommended at the rear, but the reason involving rear grip loss and the tail swinging out is not explained. |
| situation-149 | Oversteer and rear-axle loss of grip are not defined. |
| situation-150 | Understeer and front-axle loss of grip are not defined. |
| situation-152 | Aquaplaning and water separating tyre contact from the road are not defined. |
| situation-153 | The aquaplaning response is not taught; generic smooth-input advice does not establish the specific recovery action. |
| situation-154 | Separate brake circuits and retained braking after a circuit failure are not explained. |
| situation-156 | ABS pedal pulsation and maintaining firm pressure during an emergency stop are not taught. |
| situation-157 | A sinking brake pedal and hydraulic leaks/faults are not explained. |
| situation-158 | Air in a hydraulic brake system and a springy/spongy pedal are not explained. |
| situation-159 | Controlled deformation/crumple zones and crash-energy absorption are not explained. |
| situation-165 | Excess towball load unloading the front axle and reducing steering grip is not explained. |
| situation-172 | Inspection intervals are taught, but automatic prohibition following a missed deadline is not stated. |
| situation-173 | Electrical fuses and protection against excessive current are not explained. |
| situation-174 | Hot pressurised coolant and the burn risk from opening its cap are not explained. |

## Missing sign entries

79 sign codes are absent; each affects both a meaning and a recognition question:

A6, A7, A12, A17, A23, A32, A33, C4, C5, C7, C8, C9, C10, C11, C12, C13, C14, C15, C29, C30, C33, C34, D8, D9, D12, E23, E24, E25, F12, F22, F28, F29, F30, F31, F31a, F32, F33, G1, G3, G5, G10, G12, H4, H5, H6, H8, H9, H10, H11, H12, H15, H16, H17, H18, H19, H20, H21, H22, H23, H24, H25, H26, H28, J3, M17, M17a, M28, M29, M30, M31, M32, M34, S5, S6, S7, S11, S13, T23, T25

## Calculation gaps

All braking-factor questions need a square-of-speed explanation. All rough stopping-distance questions supply their own formulas but attribute them to a book that does not contain them. Fuel and fuel-saving questions are ordinary proportional arithmetic, with no teaching page in this PDF.

Suggested curriculum additions: the missing sign entries; vision, perception and fatigue details; environment and powertrain explanations; vehicle faults and braking/steering behaviour; specific winter-surface mechanisms; selected safety-system and crash-protection explanations; and worked braking, stopping and fuel calculations. The JSON lists each affected question individually.
