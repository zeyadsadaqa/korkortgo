# Tagged screen candidate

The approved source remains `../korkortgo-curriculum-review.pdf`, SHA-256 `ae872daf5b21feab0ec565294ad3275a0e2c08505a6c7007c13b2bde5352b69a`. Its approval record is unchanged. The separate tagged candidate is `../korkortgo-curriculum-tagged.pdf`; its current identity is recorded in tagging-manifest.json and verification.json. It adds semantic headings, paragraphs, lists, tables, figure alternatives, links, language and reading-order structure without changing the approved page appearance.

From the repository root, with the documented bundled Python environment:

```sh
python3 docs/curriculum/pdf-production/accessibility/tag_pdf.py
```

Validate the resulting PDF using veraPDF 1.30.3's PDF/UA-1 profile, saving XML to this directory's verapdf.xml, then run:

```sh
python3 docs/curriculum/pdf-production/accessibility/verify_tagged.py
```

The verifier checks structure and parent associations, preserved navigation, validator results and saved render evidence. Rendering requires the separate all-page comparison evidence; a structure check alone does not regenerate it. The temporary local validator installation is under `/tmp/korkort-verapdf/runtime`, and is not a committed dependency. Obtain the official distribution and follow [veraPDF CLI validation documentation](https://docs.verapdf.org/cli/validation/).

Machine PDF/UA-1 validation passed. Representative native reader checks are documented in reader-review.md; full listening/usability testing remains outside this evidence. verapdf-initial.xml records an earlier failed attempt and is historical, not the current result. The user explicitly approved the finished tagged screen edition on 14 October 2026. Its verified bytes are now delivered as ../korkortgo-curriculum.pdf; see ../final-review/screen-release.json. Print masters/proof are explicitly deferred. The cover proposal is not inserted.
