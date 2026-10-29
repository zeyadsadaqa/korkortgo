// Node 22+; uses only built-in modules and an isolated Chrome profile.
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const output = resolve(root, 'build/proof/browser');
await mkdir(output, { recursive: true });
const chrome = process.env.PROBE_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
const servers = [
  spawn('python3', [resolve(root, 'tools/serve.py')], { stdio: 'ignore' }),
  spawn('python3', [resolve(root, 'tools/serve.py'), '--port', '18766', '--no-isolation'], { stdio: 'ignore' }),
];

class CDP {
  constructor(socket) {
    this.socket = socket;
    this.serial = 0;
    this.pending = new Map();
    socket.addEventListener('message', ({ data }) => {
      const message = JSON.parse(data);
      const request = this.pending.get(message.id);
      if (!request) return;
      this.pending.delete(message.id);
      clearTimeout(request.timer);
      if (message.error) request.reject(new Error(JSON.stringify(message.error)));
      else request.resolve(message.result);
    });
  }
  static async connect(url) {
    const socket = new WebSocket(url);
    await once(socket, 'open');
    return new CDP(socket);
  }
  call(method, params = {}) {
    const id = ++this.serial;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`CDP timeout: ${method}`));
      }, 15000);
      this.pending.set(id, { resolve, reject, timer });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }
  close() { this.socket.close(); }
}

async function startChrome() {
  const child = spawn(chrome, [
    '--headless=new', '--remote-debugging-port=0', '--no-first-run',
    '--no-default-browser-check', '--disable-background-networking',
    `--user-data-dir=${resolve(output, 'profile')}`, 'about:blank',
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let stderr = '';
  const endpoint = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`Chrome startup timed out: ${stderr}`)), 15000);
    child.stderr.on('data', chunk => {
      stderr += chunk;
      const match = stderr.match(/DevTools listening on (ws:\/\/[^\s]+)/);
      if (match) { clearTimeout(timer); resolve(match[1]); }
    });
    child.once('error', error => { clearTimeout(timer); reject(error); });
    child.once('exit', code => { clearTimeout(timer); reject(new Error(`Chrome exited ${code}: ${stderr}`)); });
  });
  const browser = await CDP.connect(endpoint);
  return { child, browser, endpoint };
}

async function stopChrome(instance) {
  const exited = once(instance.child, 'exit');
  await instance.browser.call('Browser.close');
  instance.browser.close();
  await exited;
}

async function runPage(instance, action, port = 18765) {
  const { targetId } = await instance.browser.call('Target.createTarget', { url: 'about:blank' });
  const http = instance.endpoint.replace(/^ws:/, 'http:').replace(/\/devtools\/browser\/.+$/, '');
  const pages = await (await fetch(`${http}/json/list`)).json();
  const page = await CDP.connect(pages.find(page => page.id === targetId).webSocketDebuggerUrl);
  try {
    await page.call('Page.navigate', { url: `http://127.0.0.1:${port}/?action=${action}` });
    const deadline = Date.now() + 40000;
    while (Date.now() < deadline) {
      const { result, exceptionDetails } = await page.call('Runtime.evaluate', {
        expression: `({result:document.body?.dataset.probeResult,text:document.body?.textContent,isolated:crossOriginIsolated})`,
        returnByValue: true,
      });
      if (!exceptionDetails && result.value?.result) {
        const value = { action, port, ...result.value };
        assert.equal(value.result, port === 18765 ? 'pass' : 'fail', JSON.stringify(value));
        return value;
      }
      await sleep(100);
    }
    throw new Error(`Probe page timed out: ${action}`);
  } finally {
    page.close();
    await instance.browser.call('Target.closeTarget', { targetId });
  }
}

let instance;
try {
  for (const port of [18765, 18766]) {
    let ready = false;
    for (let n = 0; n < 50; n++) {
      try { ready = (await fetch(`http://127.0.0.1:${port}/`)).ok; } catch {}
      if (ready) break;
      await sleep(100);
    }
    assert(ready, `Proof server unavailable on ${port}`);
  }
  instance = await startChrome();
  const version = await instance.browser.call('Browser.getVersion');
  const results = [await runPage(instance, 'write'), await runPage(instance, 'verify')];
  await stopChrome(instance);
  instance = await startChrome(); // Same disk profile, entirely new browser process.
  results.push(await runPage(instance, 'verify'));
  results.push(await runPage(instance, 'verify', 18766));
  await writeFile(resolve(output, 'result.json'), JSON.stringify({ version, results }, null, 2) + '\n');
  console.log('PASS: browser write, new tab, browser restart, and missing-header rejection.');
} finally {
  if (instance?.child.exitCode === null) await stopChrome(instance);
  for (const server of servers) server.kill();
}
