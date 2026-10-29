# Worker provenance

`worker.js` is adapted from the AndroidX SQLite web-worker example:

- Source: https://github.com/androidx/androidx/blob/26a52f3b9e3664150571cc69bc3d20c38cfd027a/sqlite/sqlite-web-worker-test/web-worker/worker.js
- Retrieved: 29 October 2026.
- Copyright: 2026 The Android Open Source Project.
- License: Apache 2.0; see `LICENSE-AndroidX.txt`. Original source header retained.
- Adaptation: replace the npm-module import with the locally packaged `sqlite3-bundler-friendly.mjs` asset. The messaging protocol is otherwise unchanged.
- Original retrieved source SHA-256: `07b37281c10a8d89047f091af87204ce90cf39a938cbcddaab9a0379371d9eec`.
- Adapted worker SHA-256: `d1b75362b900c9575e7c9a9f468d7d502b756f3287680aadb8a49ccde0e6c701`.

SQLite's Wasm distribution is supplied by `@sqlite.org/sqlite-wasm` version `3.50.1-build1`, pinned with package integrity in `package-lock.json`. Preserve its source/license headers when copying the generated runtime assets. Package source and license: https://github.com/sqlite/sqlite-wasm.

The checked-in probe and server are development artifacts. Shipping this worker in the app requires the remaining integration and browser acceptance checks described in the phase-1 report.
