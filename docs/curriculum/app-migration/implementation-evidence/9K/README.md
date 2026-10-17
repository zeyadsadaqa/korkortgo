# 9K1–9K4 — navigation prerequisites for reference delivery

Implemented one typed canonical resolver for all 1,123 published destinations and exact block/anchor checks, plus all 1,921 frozen compatibility lookups. Question identity takes precedence over old pages. Unknown IDs/namespaces/gaps stay unavailable; ambiguous aliases preserve all reviewed choices. Chapter titles are normalised only for compatibility matching; sign codes stay case-sensitive. Production tombstones remain empty; synthetic tests cover none/one/many replacement offers.

`content/legacy-aliases.json` preserves the exact 7E records. The three SIG16–18 official-description URLs were absent from the reading source payload. `content/legacy-sources.json` retains them separately with exact frozen-7E origins, no invented check/retrieval/publication dates, and no internal sign substitutes. Runtime navigation combines this supplement with the approved sources. 9J now includes these compatibility sources in the held candidate package; this is not an accepted scored release manifest.

The shared quiz guard covers all eight states, session validation, related-reading restrictions, source exits and in-place zoom. Every direct legacy Page action now calls the shared exit guard; legacy source actions use the same discard prompt and retain their pending URL. The typed controller retains the full pending content/block/return target. Cancel preserves the session and reading context; discard never invents a new session. Validated return handling restores only existing parents/blocks and known focus IDs. Removed blocks fall back to their known parent with a moved notice; unknown parents remain unavailable.

Canonical view activation and replacement of the remaining legacy reader/summary UI are still 9L14/earlier view tasks, as planned. No new public platform URI parser, persistent history, completion credit or data migration was introduced.

## Reproduce

```sh
python3 tools/build_navigation.py --check
python3 -m unittest discover -s tools -p 'test_*.py' -v
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest --offline --no-daemon
```

[Shared implementation evidence and target limitations](../9F/README.md).

## 17 October 2026 — completion review and hardening

Rechecked 9K1–9K4 against the now-assembled 9J candidate. 9J includes the three compatibility-only signal URLs and rejects using them as teaching evidence. All canonical and frozen alias imports remain byte-identical.

Fixed missing-session recovery for current quiz/results/review states; recovery offers setup without manufacturing a result. Moved-block requests now store the validated parent target rather than the obsolete block, and preserve the moved notice through discard confirmation. Pending actions bind the exact session they were approved against: session replacement clears pending state, and a stale confirmation cannot discard a new session. Cancellation preserves the prior session, destination and return context.

Typed source requests carry an exact registered source-reference ID. Unknown references or a source reference disguised as general navigation are denied. During an unfinished test, source opening remains pending until deliberate discard; cancellation never exposes an open-source effect. The full source reference and return context survive confirmation. Discarding a quiz for a source exit recovers to setup rather than leaving a quiz screen without its session. This supplements the existing legacy source exit guard; no raw-URL guessing is introduced into the typed controller.

Return tests cover valid and moved blocks, unknown parents, conflicting anchors, valid/invalid focus IDs, negative-offset rejection and none/one/many retired replacement outcomes. Retirement offers never invent a reading position or choose a replacement automatically. Production tombstones remain empty.

[All twelve entry-point rules and exact scope](entry-point-checks.json) records which foundation checks cover each contract and which screen callbacks remain in 9L. This is completion of the navigation foundation, not activation of the canonical UI or acceptance of the held 9J release. Existing library/reader summaries and legacy integer reader adapters are still removed/replaced in the planned 9L tasks; no new screen design was implemented here.

Final validation: **137 Python tests and 52 desktop tests passed**, including 11 navigation tests. Alias generation and 9J reproduction pass; all 9F holds remain. [Verification receipt](verification.json) · [Saved test results](tests/).
