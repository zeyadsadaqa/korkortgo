# 10L2 — restore the reading route after catalogue return

DEF-10H-001 is corrected by clearing the transient reference-catalogue flag before restoring the existing validated reading context. The catalogue branch previously masked the restored lesson target. No layout, label, design, accepted content, source date, generated input or persistent feature changed.

The permanent UI regression exercises the actual annotated B1 callback, sign detail, catalogue and return twice at 390/1280 widths and 100%/160% font scale. It failed at the return-to-passage wait on the pre-fix source and passes with the correction. A second case preserves no-origin catalogue recovery to the library. All 38 selected shared route/reader/source/reference/session/parity checks and the original historical assertion pass; native and browser scope is recorded by 10L3. This implements a correction, not blanket gate acceptance.

[Candidate fingerprint](candidate-fingerprint.json) identifies the changed runtime/test sources while retaining the exact accepted content identity. [Changed files and IDs](changed-files-and-ids.json) bounds the impact.
