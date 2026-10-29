// Optional engine coverage. Chrome restart coverage is in browser-proof.mjs.
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { firefox, webkit } from '../web/node_modules/playwright/index.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const output = resolve(root, 'build/proof/browser-matrix');
await mkdir(output, { recursive: true });
const server = spawn('python3', [resolve(root, 'tools/serve.py')], { stdio: 'ignore' });
const results = [];
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));

try {
  let ready = false;
  for (let n = 0; n < 50; n++) {
    try { ready = (await fetch('http://127.0.0.1:18765/')).ok; } catch {}
    if (ready) break;
    await pause(100);
  }
  assert(ready, 'Proof server unavailable');
  for (const [name, engine] of [['webkit', webkit], ['firefox', firefox]]) {
    let context;
    // macOS may deny a browser access to a profile located on Desktop.
    const profile = await mkdtemp(resolve(process.env.PROBE_PROFILE_ROOT || tmpdir(), `korkort-${name}-proof-`));
    const result = { engine: name, checks: [] };
    async function check(action) {
      const page = await context.newPage();
      try {
        await page.goto(`http://127.0.0.1:18765/?action=${action}`);
        await page.waitForFunction(() => document.body.dataset.probeResult, null, { timeout: 40000 });
        const value = await page.evaluate(() => ({
          result: document.body.dataset.probeResult,
          text: document.body.textContent,
          isolated: crossOriginIsolated,
          userAgent: navigator.userAgent,
        }));
        result.checks.push({ action, ...value });
        assert.equal(value.result, 'pass', JSON.stringify(value));
      } finally { await page.close(); }
    }
    try {
      context = await engine.launchPersistentContext(profile, { headless: true });
      result.version = context.browser()?.version();
      await check('write');
      await check('verify');
      await context.close();
      context = await engine.launchPersistentContext(profile, { headless: true });
      await check('verify');
      result.status = 'pass';
    } catch (error) {
      result.status = 'fail';
      result.error = error.message;
    } finally {
      await context?.close();
      await rm(profile, { recursive: true, force: true });
    }
    results.push(result);
    console.log(`${name}: ${result.status}`);
  }
  await writeFile(resolve(output, 'result.json'), JSON.stringify(results, null, 2) + '\n');
  assert(results.every(result => result.status === 'pass'), 'Some browser engines failed; see result.json');
} finally { server.kill(); }
