// Browser smoke test (run: npm run test:smoke). Opens the game, walks the menus, plays the first level to the end
// with a simple bot and checks that progress survives a reload. Fails on any page error.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import { ROOT } from './lib.mjs';

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.webmanifest': 'application/manifest+json', '.png': 'image/png', '.json': 'application/json' };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname).replace(/\/$/, '/index.html'));
  if (!p.startsWith(ROOT) || !fs.existsSync(p)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const URL0 = `http://127.0.0.1:${server.address().port}/`;
const exe = process.env.CHROMIUM_PATH || (fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);
const browser = await chromium.launch(exe ? { executablePath: exe } : {});
const page = await browser.newPage({ viewport: { width: 390, height: 820 } });
const errors = [];
page.on('pageerror', e => errors.push(e.message));
const ev = (f, a) => page.evaluate(f, a);
const step = m => console.log('  •', m);

try {
  await page.goto(URL0);
  await page.waitForFunction(() => typeof save === 'object' && document.getElementById('playBtn'), null, { timeout: 15000 });
  await page.waitForTimeout(1500);
  await ev(() => { save.muted = true; save.musicOff = true; closeModal(); });
  for (const i of [0, 2, 1]) { await ev(i => goPage(i, true), i); await page.waitForTimeout(200); }
  step('home, album and team pages render');
  await ev(() => showTuts(Object.keys(TUT_KEYS), closeModal, false));
  for (let i = 0; i < 16; i++) { await ev(() => { const b = document.getElementById('tutOk'); if (b && !modal.hidden) b.click(); }); }
  step('all how-to-play screens open');
  for (const l of ['en', 'de', 'tr']) await ev(l => { save.lang = l; applyLang(); homeHud(); }, l);
  step('languages switch');
  await ev(() => document.getElementById('playBtn').onclick());
  await page.waitForFunction(() => typeof G !== 'undefined' && G && G.state === 'play', null, { timeout: 30000 });
  await ev(() => { save.bank2x = 9999; save.speed2 = true; setInterval(() => {
    const b = document.getElementById('tutOk'); if (b && !modal.hidden) b.click();
    if (!G || G.state !== 'play' || G.mode) return;
    if (G.units.some(u => u.phase === 'out') || G.swarms.some(s => !s.done && s.n > 0 && !s.waiting)) return;
    const free = freeSlots(), expo = {}; G.cells.forEach((c, i) => { if (G.exposed[i]) expo[c.k] = (expo[c.k] || 0) + 1; });
    let best = -1, bs = -1e9;
    G.columns.forEach((c, ci) => { if (ci === G.lockCol || !c.length || free < 1) return; const b = c[0]; const a = expo[b.k] || 0;
      const sc = Math.min(a, b.n) * 2 + (a >= b.n ? 5 : 0) - (a === 0 ? 8 : 0); if (sc > bs) { bs = sc; best = ci; } });
    if (best >= 0) tapColumn(best);
  }, 150); });
  await page.waitForFunction(() => G && (G.state === 'won' || G.state === 'lost'), null, { timeout: 240000, polling: 1000 });
  const state = await ev(() => G.state);
  if (state !== 'won') throw new Error('bot did not finish level 1 (state ' + state + ')');
  step('level 1 played to the end');
  await page.waitForTimeout(500);
  const lvl = await ev(() => save.level);
  await page.reload(); await page.waitForTimeout(1500);
  const after = await ev(() => save.level);
  if (after !== lvl || lvl < 1) throw new Error(`progress lost on reload (${lvl} -> ${after})`);
  step('progress survives a reload');
  if (errors.length) throw new Error('page errors: ' + errors.join(' | '));
  console.log('smoke test passed');
} catch (e) {
  console.log('smoke test FAILED:', e.message);
  process.exitCode = 1;
} finally {
  await browser.close(); server.close();
}
