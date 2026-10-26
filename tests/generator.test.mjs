// Level generator checks (run: npm test). Fails the build when a level cannot be solved or is inconsistent.
import { loadGenerator } from './lib.mjs';

const G = loadGenerator();
const LEVELS = (process.env.LEVELS || '0,1,2,3,4,7,8,10,12,13,15,16,19,21,24,28,29,39,49,59,79,99,149,199')
  .split(',').map(Number);
let failed = 0;
const fail = (L, msg) => { failed++; console.log(`  ✗ level ${L + 1}: ${msg}`); };

// every embedded picture decodes to a full 40x40 grid
for (const [key, , rle] of G.EMO) {
  const g = G.emoDecode(rle);
  if (g.length !== 1600) fail(-1, `picture "${key}" decodes to ${g.length} cells`);
}
console.log(`pictures: ${G.EMO.length} emoji + ${Object.keys(G.DESIGNS).length - G.EMO.length} drawn designs`);

let seqWins = 0, total = 0;
for (const L of LEVELS) {
  const t0 = Date.now();
  let lv;
  try { lv = G.makeLevel(L); } catch (e) { fail(L, 'generator threw: ' + e.message); continue; }
  const ms = Date.now() - t0;
  const lock = lv.lockCol >= 0 ? { col: lv.lockCol, cell: lv.keyCell } : null;
  const sim = (slots, mode) => G.simulateReal(lv.cells, lv.nb, lv.columns, slots, lock, mode, 0, lv.box, lv.gate);
  if (!lv.cells.length || !lv.columns.some(c => c.length)) fail(L, 'empty level');
  // bees match the hexagons to collect
  const bees = lv.columns.flat().reduce((a, b) => a + b.n, 0);
  const cells = lv.cells.filter(c => !c.box).length + (lv.box ? lv.box.seq.length : 0);
  if (bees !== cells) fail(L, `bees ${bees} != hexagons ${cells}`);
  // the level can be solved with the slots the player gets
  if (!sim(lv.slotsBase, false)) fail(L, `not solvable with ${lv.slotsBase} slots`);
  if (ms > 20000) fail(L, `generation took ${ms} ms`);
  const seq = sim(5, 'seq'); total++; if (seq) seqWins++;
  console.log(`  ✓ level ${String(L + 1).padStart(3)} ${lv.name.padEnd(22)} tier ${lv.tier} cols ${lv.ncols} ${lv.fb ? 'FALLBACK ' : ''}left-to-right(5) ${seq ? 'wins' : 'loses'}  ${ms} ms`);
}
console.log(`left-to-right tapping wins ${seqWins}/${total} sampled levels (5 slots)`);
if (failed) { console.log(`${failed} problem(s)`); process.exit(1); }
console.log('all generator checks passed');
