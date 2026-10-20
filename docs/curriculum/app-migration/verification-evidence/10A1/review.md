# 10A1 — Candidate reconciliation

**20 October 2026 — complete; nine baseline checks pass.** The candidate at `aa4f0e18fbd0e1ebcfd3246c15063c85831ab3ac` matches the step 9 handoff for all accepted content, approved PDF, generated/runtime/test code, assets, approvals and delivery policy. The working tree was clean at task entry; subsequent untracked files are this verification evidence.

- 1,065 of 1,067 indexed files match; the two documentation-only differences are fully traced in [input-drift.md](input-drift.md).
- All 932 accepted file/hash references and 968 original/bundled checks for 484 artwork bindings match.
- Fingerprinted all 7,461 tracked inputs, including runtime, tests, build configuration, design approvals and supporting evidence.
- Counts match: 1,000 accepted questions / 500 concepts / zero holds; 336 retained, 626 rewritten, 38 replaced; 10 modules / 40 lessons / 10 reviews, four appendices, 24 reference groups, 1,123 destinations and 400 official entries.
- Accepted manifest SHA-256: `ba91c96975c39b5f6db552c6bead17c0e0474c11dd590f811a7eeb1e1ae54a21`; package digest: `d9ba2f0261dc9c908146676f903a5ee7fd9c73b50231cd10c2182ecf5d87f82a`; approved PDF SHA-256: `78a89d8ffbb83b6e9eec6193396871ac2fb9feccf245b85112809646dd595581`.

[Baseline](candidate-baseline.json) contains every fingerprint, comparison and input identity. [Results](results.json), [commands](commands.json) and [run log](baseline-run.txt) retain observations. The initial historical-commit-locator diagnostic is preserved; it was a verifier issue, not candidate drift. No unresolved input blocker remains.

Recheck without replacing the snapshot:

```sh
python3 docs/curriculum/app-migration/verification-evidence/10A1/verify_baseline.py --check
```

This establishes identity/readiness only. It does not independently pass T01–T10, inspect PDF rendering, refresh source dates, build binaries or exercise app/runtime accessibility. 10A2 is next within the user's authorized 10A sequence.
