# 10A2 — Verification scope

**20 October 2026 — complete; five readiness/scope checks pass.** Built a 54-row matrix covering six target layers and nine dimensions: build, packaged bytes, runtime, offline/local delivery, external links, visual legibility, keyboard, semantics/focus and actual screen-reader listening. Of these, 37 are required future checks and 17 are explicitly excluded or assigned to another surface. Four future-store contracts remain conditional.

The existing iOS simulator, desktop-harness and static-web boundaries are preserved. Required tools and targets were observed available/bootable; no unresolved availability blocker remains at this checkpoint. The iPhone simulator is currently shut down and TalkBack currently disabled; the matrix records setup/restoration work. Product runtime, source-link and assistive checks have not run.

[Scope matrix](scope-matrix.json) · [Readiness and exact limits](environment-readiness.md) · [Results](results.json) · [Command/log index](environment-commands.json) · [Browser readiness](browser-readiness.json).

Rebuild the matrix from the saved observations (does not refresh environment probes or run app tests):

```sh
python3 docs/curriculum/app-migration/verification-evidence/10A2/build_scope.py
```

Live readiness must be rechecked when the later platform task runs. Initial sandbox service failures and successful host-permitted retries are retained. No historical receipt, delivery policy, production code/content or design approval changed. Continue to 10A3 within the requested sequence.
