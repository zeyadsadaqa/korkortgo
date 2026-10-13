# G0 build constraints

Structural review only: no chapter was rebuilt and no extra-page layout was tested.

| Chapter | Target questions | Baseline pages | Added-page budget | Text pagination | Minimum local answer gap |
|---|---:|---:|---:|---|---:|
| M01 | 4 | 15 | 1–2 | Explicit pages | 2 |
| M02 | 10 | 15 | 3–4 | Explicit pages | 2 |
| M03 | 3 | 50 | 2–2 | Continuation pages | 2 |
| M04 | 1 | 42 | 1–1 | Continuation pages | 2 |
| M05 | 3 | 44 | 1–1 | Continuation pages | 2 |
| M06 | 3 | 48 | 1–2 | Continuation pages | 2 |
| M07 | 12 | 23 | 3–4 | Continuation pages | 2 |
| M08 | 3 | 29 | 1–2 | Continuation pages | 2 |
| M09 | 15 | 22 | 4–5 | Continuation pages | 2 |
| M10 | 1 | 23 | 1–1 | Continuation pages | 2 |

The 18–24-page estimate is provisional. Text continuation, additional references and assessment separation may change it. No numerical spare capacity can be established from source inspection alone.

## Constraints for later execution

- M01/M02 verifiers hard-code 15 pages and 16 destinations, plus artwork page positions. New teaching pages need explicit builder changes and corresponding justified checks.
- All chapter source parsers expect recognised worked-decision/check/answer/reminder blocks. Additional independent checks need a deliberate parser/verification extension.
- M03–M10 support continuation pages; oversized indivisible panels still hit the shared overflow guard. M09 does not currently render Markdown tables as tables, so its proposed pollutant/powertrain tables need an approved presentation and builder handling.
- Chapter references are batched four per page. New aliases can add reference pages. Existing source-check dates are historical, not verification of new claims.
- Sign placements use exact manuscript quotes; preserve anchors or revise placement records and validate artwork.
- Existing navigation records have at least two local pages between each recorded question and its answer. This is a read-only metadata check, not fresh visual verification. Preserve spacing and recheck global page parity after assembly.
- Assembly verification hard-codes 498 pages, labels, map size and footer boundary. Update all affected checks during G11 without weakening text/link fidelity checks.
- The coverage generator stores reviewed decisions and page numbers in code; an unchanged rerun cannot independently assess added teaching. G12 must use freshly reviewed evidence.

See [machine-readable inspection](build-constraints.json) for individual chapter constraints.
