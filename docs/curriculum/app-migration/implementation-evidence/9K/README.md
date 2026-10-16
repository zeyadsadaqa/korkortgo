# 9K1–9K4 — navigation prerequisites for reference delivery

Implemented one typed canonical resolver for all 1,123 published destinations and exact block/anchor checks, plus all 1,921 frozen compatibility lookups. Question identity takes precedence over old pages. Unknown IDs/namespaces/gaps stay unavailable; ambiguous aliases preserve all reviewed choices. Chapter titles are normalised only for compatibility matching; sign codes stay case-sensitive. Production tombstones remain empty; synthetic tests cover none/one/many replacement offers.

`content/legacy-aliases.json` preserves the exact 7E records. The three SIG16–18 official-description URLs were absent from the reading source payload. `content/legacy-sources.json` retains them separately with exact frozen-7E origins, no invented check/retrieval/publication dates, and no internal sign substitutes. Runtime navigation combines this supplement with the approved sources. 9J must include these compatibility sources when assembling the release package; this is not a new scored release manifest.

The shared quiz guard covers all eight states, session validation, related-reading restrictions, source exits and in-place zoom. Every direct legacy Page action now calls the shared exit guard; legacy source actions use the same discard prompt and retain their pending URL. The typed controller retains the full pending content/block/return target. Cancel preserves the session and reading context; discard never invents a new session. Validated return handling restores only existing parents/blocks and known focus IDs. Removed blocks fall back to their known parent with a moved notice; unknown parents remain unavailable.

Canonical view activation and replacement of the remaining legacy reader/summary UI are still 9L14/earlier view tasks, as planned. No new public platform URI parser, persistent history, completion credit or data migration was introduced.

## Reproduce

```sh
python3 tools/build_navigation.py --check
python3 -m unittest discover -s tools -p 'test_*.py' -v
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest --offline --no-daemon
```

[Shared implementation evidence and target limitations](../9F/README.md).
