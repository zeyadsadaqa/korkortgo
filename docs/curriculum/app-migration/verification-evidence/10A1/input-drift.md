# 10A1 input drift

Only the implementation plan and progress tracker differ from the 1,067-file handoff index. Their indexed hashes exactly match commit `4270d58`, which records the handoff completion. The current hashes are explained by commits `6808445` (step 10 breakdown) and `aa4f0e1` (tracker). Reviewed their diffs in this chat; no application, content, asset, approval or policy change is included. The source fingerprint independently includes current runtime, test, content and build inputs.

| File | Indexed hash | Current entry hash |
|---|---|---|
| `docs/curriculum/implementation-plan.md` | `304ea2a8dc47d081cdc24dc55c5f34827f4ff424fd265ccaa8f541502d4cd51d` | `51c99df7e0f73eaa90b27295580ef4e99fae3fa58a6762ff38b5a01bb032395e` |
| `docs/curriculum/progress.md` | `e44b4684330b16b0e527975ce5ebe48743850bfebc3603f00ad5ef1220493c5f` | `89cd949cd64810ddae8a980f979f1dccea7a0c2c656abfe1ddf98fc597f84208` |

The initial verifier used the preceding index-creation commit `657fef8` as the document-blob anchor. That produced a diagnostic failure, retained in [initial-diagnostic.json](initial-diagnostic.json). Git history identified `4270d58` as the exact matching blob anchor; the corrected verifier passes. Historical index and acceptance receipts were not changed.

The 9O8 index already documents four differences from the older closure snapshot (README, plan, progress, Android selector). Those are inherited historical differences, not four additional current mismatches. All indexed current runtime/test inputs match.

The user-requested cleanup removed only ignored metadata/Python caches and a temporary planning script. None of the 7,461 tracked files or 932 accepted-reference hash pairs is missing. Ignored local builds are not accepted input evidence; fresh builds and installed-resource/runtime checks remain later work.

This task's new reports and subsequent progress/status edits are verification documentation. The frozen entry baseline is retained; future `--check` reports plan/progress drift separately and rejects other changed or missing baseline files. Documentation drift must still be reviewed rather than interpreted as a fresh acceptance result.
