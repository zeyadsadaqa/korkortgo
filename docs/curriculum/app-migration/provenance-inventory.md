# Accepted release provenance and credits — 9O1

**Prepared:** 19 October 2026. This inventory documents the existing accepted package; it does not grant new reuse rights or renew every source check. The [machine inventory](provenance-inventory.json) binds the exact manifest, authoring payloads, brief file and font licences by SHA-256, groups every asset by retained credit/conditions and points to its canonical reuse records.

## Production identity and counts

The [accepted manifest](../../../content/accepted-content-manifest.json) declares content version `screen-2026-10-14-78a89d8ffbb8-accepted-9j`, identity digest `d9ba2f0261dc9c908146676f903a5ee7fd9c73b50231cd10c2182ecf5d87f82a`. This declared digest is calculated by the compiler's manifest identity rule; it is distinct from the complete file's SHA-256 in the inventory.

The manifest-bound payloads supply 1,000 accepted questions, zero holds, 500 concepts, 10 modules, 40 lessons and 400 official sign/marking/signal reference entries. There are 484 asset bindings (400 official and 84 contextual) sharing 419 physical resource files. Package sources contain 519 references and 116 source destinations; these are different units, not interchangeable counts. The three [9N briefs](assessment-coverage-briefs.md) are proposals only; the baseline remains unchanged.

| Material | Authoritative inventory and retained origin |
| --- | --- |
| Accepted assessments | [accepted-assessment-questions.json](../../../content/accepted-assessment-questions.json): per-question `origin`, exact key/revision, option feedback, relationship and acceptance evidence. [Historical candidate](../../../content/assessment-questions.json) and [delivery decisions](implementation-evidence/closure-9j-9m-9l14/delivery-acceptance.json) remain separate. |
| Original curriculum | [curriculum.json](../../../content/curriculum.json): document origins, typed teaching blocks, source links and canonical navigation; [9B17 import](implementation-evidence/9B17/README.md) preserves the approved PDF provenance and complete teaching. |
| Sources and dates | [package-sources.json](../../../content/package-sources.json): exact URL, publisher, classification, editorial-inference flag, evidence origin, check/retrieval/publication dates and scope limits. Null dates remain unknown. These include authorities, legislation and other classified supporting material; not every source is an official authority. |
| Compatibility routes | [legacy-aliases.json](../../../content/legacy-aliases.json) and [7E mapping](link-and-progress-map.json): retained lookup identity and canonical target/chooser/external outcome. Compatibility does not restore deleted summary/catalogue payloads. |
| Official artwork | `curriculum.json` asset records: original and bundled file hashes, source relationships, approval and reuse evidence, caption, alt text and rendering constraints. [Sign reuse assessment](../sign-reuse.md), [source register](../sign-sources.json) and [original catalogue manifest](../../../content/source-manifest.json) retain the acquisition/reuse trail. |
| Editorial illustrations | `curriculum.json` contextual assets: approved original sheet, exact bundled bytes, crop/mask/overlay constraints and review record. [Illustration register](../pdf-design/5e/illustration-register.md) and per-chapter production records retain design provenance; later asset-specific approval records govern the final placement. |

## Credits and conditions to retain

**Official artwork:** “Transportstyrelsen; English labels and explanations are editorial translations.” The project also retains the credit “Road-sign illustrations: Transportstyrelsen. Source links and verification dates are recorded in the official references.” The [recorded reuse basis](../sign-reuse.md#reuse-basis) treats this project credit as a traceability choice, not a mandatory quotation. Preserve the proper teaching context, geometry/colours and exact approved bytes; do not infer permission for unrelated photographs, branding or substitute artwork. Its application to linked markings/signals is a documented catalogue-scope interpretation, not an explicit separate licence for each family.

**Contextual illustrations:** “KörkortGo; built-in imagegen artwork.” Preserve the exact approved scene/sheet and only the recorded production crop, mask and overlays; keep generated typography outside the visible region where required. The machine inventory records all four distinct credit/condition combinations and their asset IDs; full approval and reuse evidence remains in each canonical asset record.

**Fonts:** Source Sans 3 and Source Serif 4 retain the Adobe copyright/reserved-name notices and complete SIL Open Font License 1.1 texts in the bundled [Source Sans licence](../../../composeApp/src/commonMain/composeResources/files/font-licenses/SourceSans3-LICENSE.md) and [Source Serif licence](../../../composeApp/src/commonMain/composeResources/files/font-licenses/SourceSerif4-LICENSE.md). Preserve the complete notices with redistributed fonts; a short credit does not replace the licences. The production PDF font directory retains its own copies.

**Learning-aid disclaimer:** Retain the curriculum notice that this is a learning aid, not an official source or a replacement for current Trafikverket/Transportstyrelsen information. README independently states that the practice app is not an official examination or a reproduction of official exam questions. No official endorsement follows from reuse or source citation.

Credits, dates and classifications remain available through canonical source/reference and teaching records in the app, the bound JSON and retained production references. This inventory makes those records discoverable for maintainers; it introduces no new learner-facing attribution UI or blanket licence for the repository or its dependencies.

## Reproduction and validation scope

[Build guidance](../../development/content.md) distinguishes verification, restoration of unchanged generated outputs, historical compilers and changed-content acceptance. The inventory checks every original/bundled asset hash, each reuse-evidence file hash and the presence of approval/reuse records. It retains all 484 asset IDs grouped by their exact credit/condition text; resolve each `curriculum_reuse_locators` entry against the hash-bound curriculum payload for complete evidence.

9O1 is documentation/provenance work. Full common/platform checks and step 10 handoff are subsequent tasks. Existing accepted [delivery evidence](implementation-evidence/closure-9j-9m-9l14/README.md) and [simulator policy](../../../content/delivery-targets.json) retain their scope; packaging support for physical iOS devices is not a physical-device acceptance claim.
