#!/usr/bin/env node
// Zombies on Fire local server. Node.js 18+, no dependencies.
//
//   node server.js                  serve this folder, pick a free port, open the browser
//   node server.js --port 9000      start looking for a free port at 9000
//   node server.js --no-open        don't open a browser      --dir <folder>   serve another folder
//
// It serves the game and forwards the game's AI calls (Ollama, LM Studio, vLLM, OpenAI, Anthropic, ...),
// so the browser never needs CORS permission from any of them. Keys can stay out of the browser entirely:
// set OPENAI_API_KEY (with OPENAI_BASE_URL for a non-OpenAI server) or ANTHROPIC_API_KEY before starting.
//
// Locked down: listens on 127.0.0.1 only; refuses other Host headers (DNS rebinding) and other origins;
// forwarding needs a random per-run token that only this page can read; no CORS headers are ever sent.
'use strict';
const http = require('node:http'), fs = require('node:fs'), path = require('node:path'), crypto = require('node:crypto');
const { exec, spawn } = require('node:child_process');

const args = process.argv.slice(2);
const flag = n => args.includes(n);
const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 && args[i + 1] ? args[i + 1] : d; };
const ROOT = path.resolve(opt('--dir', __dirname));
const START_PORT = Number(opt('--port', process.env.PORT || 8737));
const OLLAMA_URL = (process.env.OLLAMA_URL || 'http://127.0.0.1:11434').replace(/\/+$/, '');
const OPENAI_BASE = (() => {      // a malformed OPENAI_BASE_URL is reported once at start, not on every AI call
  const v = (process.env.OPENAI_BASE_URL || 'https://api.openai.com/v1').replace(/\/+$/, '');
  try { new URL(v); return v; } catch (e) { console.error(`  OPENAI_BASE_URL isn't a URL (${v}); using https://api.openai.com/v1`); return 'https://api.openai.com/v1'; }
})();
const TOKEN = crypto.randomBytes(24).toString('hex');
const MAX_BODY = 2 * 1024 * 1024;
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.json': 'application/json', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml',
  '.ttf': 'font/ttf', '.woff2': 'font/woff2', '.ico': 'image/x-icon', '.md': 'text/markdown; charset=utf-8', '.txt': 'text/plain; charset=utf-8' };
const FORWARD_HEADERS = ['content-type', 'authorization', 'x-api-key', 'anthropic-version', 'anthropic-beta', 'accept'];

if (Number(process.versions.node.split('.')[0]) < 18) { console.error('Zombies on Fire needs Node.js 18 or newer: https://nodejs.org'); process.exit(1); }
if (!fs.existsSync(ROOT)) { console.error(`No such folder: ${ROOT}`); process.exit(1); }
let port = 0;
const PAGE = ['zombies-on-fire.html', 'index.html'].find(f => fs.existsSync(path.join(ROOT, f))) || '';

function send(res, code, body, type, extra) {
  res.writeHead(code, { 'Content-Type': type || 'application/json', 'X-Content-Type-Options': 'nosniff',
                        'Referrer-Policy': 'no-referrer', 'Cache-Control': 'no-store', ...(extra || {}) });
  res.end(typeof body === 'string' || Buffer.isBuffer(body) ? body : JSON.stringify(body));
}
const sameHost = req => [`127.0.0.1:${port}`, `localhost:${port}`].includes(req.headers.host || '');
const sameOrigin = req => {
  const o = req.headers.origin, site = req.headers['sec-fetch-site'];
  if (o && ![`http://127.0.0.1:${port}`, `http://localhost:${port}`].includes(o)) return false;
  return !site || site === 'same-origin' || site === 'none';
};
const tokenOk = req => {
  const t = Buffer.from(String(req.headers['x-zof-token'] || '')), want = Buffer.from(TOKEN);
  return t.length === want.length && crypto.timingSafeEqual(t, want);
};
function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = []; let size = 0;
    req.on('data', c => {
      size += c.length;
      if (size <= MAX_BODY) return chunks.push(c);
      req.removeAllListeners('data'); req.resume();          // drain the rest, then answer 413 instead of cutting the line
      reject(new Error('too large'));
    });
    req.on('end', () => resolve(Buffer.concat(chunks))); req.on('error', reject);
  });
}

// ---------- the AI proxy ----------
async function forward(req, res) {
  let target;
  try { target = new URL(String(req.headers['x-zof-target'] || '')); } catch (e) { return send(res, 400, { error: 'zof-proxy: bad target' }); }
  if (!['http:', 'https:'].includes(target.protocol)) return send(res, 400, { error: 'zof-proxy: http and https only' });
  const headers = {};
  for (const h of FORWARD_HEADERS) if (req.headers[h]) headers[h] = req.headers[h];
  // Keys from the environment go only to the server they belong to.
  if (!headers['x-api-key'] && process.env.ANTHROPIC_API_KEY && target.hostname === 'api.anthropic.com') headers['x-api-key'] = process.env.ANTHROPIC_API_KEY;
  if (!headers.authorization && process.env.OPENAI_API_KEY && target.origin === new URL(OPENAI_BASE).origin) headers.authorization = `Bearer ${process.env.OPENAI_API_KEY}`;
  let body;
  try { body = req.method === 'GET' ? undefined : await readBody(req); } catch (e) { return send(res, 413, { error: 'zof-proxy: request too large (2 MB at most)' }, null, { Connection: 'close' }); }
  // The answer is passed on as it arrives, so the game can show a local model writing and stop waiting only when it
  // goes quiet. If the game cancels (or the page closes), the request to the model is cancelled too.
  const ctl = new AbortController();
  const cap = setTimeout(() => ctl.abort(), 30 * 60 * 1000);
  res.on('close', () => { if (!res.writableEnded) ctl.abort(); });
  try {
    const r = await fetch(target, { method: req.method, headers, body, signal: ctl.signal });
    res.writeHead(r.status, { 'Content-Type': r.headers.get('content-type') || 'application/json', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff',
      ...(r.headers.get('retry-after') ? { 'Retry-After': r.headers.get('retry-after') } : {}) });
    if (r.body) for await (const chunk of r.body) { if (!res.write(chunk)) await new Promise(ok => res.once('drain', ok)); }
    res.end();
  } catch (e) {
    if (res.headersSent) return res.destroy();          // cut off mid-answer: the game sees the stream end and reports it
    send(res, 502, { error: `zof-proxy: couldn't reach ${target.origin}`, detail: e.cause ? e.cause.code || e.cause.message : e.message });
  } finally { clearTimeout(cap); }
}

// ---------- static files ----------
function serveFile(req, res, urlPath) {
  let rel;
  try { rel = decodeURIComponent(urlPath.split('?')[0]); } catch (e) { return send(res, 400, 'Bad request', 'text/plain'); }   // "/%" and friends
  if (rel.includes('\0')) return send(res, 400, 'Bad request', 'text/plain');
  if (rel === '/' && PAGE) rel = `/${PAGE}`;
  const file = path.normalize(path.join(ROOT, rel));
  if (!file.startsWith(ROOT + path.sep) && file !== ROOT) return send(res, 403, 'Forbidden', 'text/plain');
  fs.stat(file, (err, st) => {
    if (err || !st.isFile()) return send(res, 404, 'Not found', 'text/plain');
    res.writeHead(200, { 'Content-Type': MIME[path.extname(file).toLowerCase()] || 'application/octet-stream',
                         'Content-Length': st.size, 'X-Content-Type-Options': 'nosniff', 'Cache-Control': 'no-cache' });
    if (req.method === 'HEAD') return res.end();
    fs.createReadStream(file).on('error', () => res.destroy()).pipe(res);
  });
}

const server = http.createServer((req, res) => {
  handle(req, res).catch(e => {      // one bad request must never take the game's server down
    console.error(`  Request failed: ${req.method} ${String(req.url).slice(0, 80)}: ${e.message}`);
    if (!res.headersSent) send(res, 500, { error: 'zof-server: internal error' }); else res.destroy();
  });
});
async function handle(req, res) {
  if (!sameHost(req)) return send(res, 403, 'Forbidden: wrong host', 'text/plain');
  const url = req.url || '/';
  if (url.startsWith('/proxy/')) {
    if (req.method === 'OPTIONS' || !sameOrigin(req)) return send(res, 403, { error: 'zof-proxy: other origins are not allowed' });
    if (url === '/proxy/session' && req.method === 'GET')
      return send(res, 200, { token: TOKEN, ollama: OLLAMA_URL, keys: { openai: !!process.env.OPENAI_API_KEY, openaiBase: OPENAI_BASE, anthropic: !!process.env.ANTHROPIC_API_KEY } });
    if (url === '/proxy/forward') return tokenOk(req) ? forward(req, res) : send(res, 403, { error: 'zof-proxy: missing or wrong token' });
    return send(res, 404, { error: 'zof-proxy: unknown route' });
  }
  if (req.method !== 'GET' && req.method !== 'HEAD') return send(res, 405, 'Method not allowed', 'text/plain');
  serveFile(req, res, url);
}

function listen(p, tries) {
  server.once('error', e => {
    if (e.code === 'EADDRINUSE' && tries > 0) return listen(p + 1, tries - 1);
    if (e.code === 'EADDRINUSE') return listen(0, 0);   // let the OS pick any free port
    console.error(`Couldn't start: ${e.message}`); process.exit(1);
  });
  server.listen(p, '127.0.0.1', started);
}
function openBrowser(url) {
  const fail = () => console.log(`Open ${url} in your browser.`);
  try {
    if (process.platform === 'win32') exec(`start "" "${url}"`, e => e && fail());
    else { const c = spawn(process.platform === 'darwin' ? 'open' : 'xdg-open', [url], { stdio: 'ignore', detached: true }); c.on('error', fail); c.unref(); }
  } catch (e) { fail(); }
}
async function started() {
  port = server.address().port;
  const url = `http://127.0.0.1:${port}/${PAGE}`;
  console.log(`\n  Zombies on Fire is running at ${url}\n`);
  try {
    const r = await fetch(`${OLLAMA_URL}/api/tags`, { signal: AbortSignal.timeout(1500) });
    const models = (await r.json()).models || [];
    console.log(`  Ollama: running with ${models.length} model(s)${models.length ? ': ' + models.slice(0, 4).map(m => m.name).join(', ') : '. Try: ollama pull llama3.1:8b'}`);
  } catch (e) { console.log('  Ollama: not running (optional). Install from https://ollama.com, then: ollama pull llama3.1:8b'); }
  if (process.env.OPENAI_API_KEY) console.log(`  OpenAI-compatible key: from the environment, used only for ${new URL(OPENAI_BASE).origin}`);
  if (process.env.ANTHROPIC_API_KEY) console.log('  Anthropic key: from the environment, used only for api.anthropic.com');
  console.log('\n  AI calls go through this server, so no CORS setup is needed. Press Ctrl+C to stop.\n');
  if (!flag('--no-open')) openBrowser(url);
}
process.on('SIGINT', () => { console.log('\n  Stopped.'); process.exit(0); });
// Last resort: log and keep serving. Players mid-game lose nothing if one request goes wrong.
process.on('uncaughtException', e => console.error(`  Unexpected error (still running): ${e.message}`));
process.on('unhandledRejection', e => console.error(`  Unexpected error (still running): ${e && e.message ? e.message : e}`));
listen(START_PORT, 50);
