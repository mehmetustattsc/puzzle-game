// Shared helpers for the tests: load the level generator straight out of index.html (the same code the game runs).
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const INDEX = path.join(ROOT, 'index.html');
const MARKER = '/* ================= save, lives, daily';

export function loadGenerator(file = INDEX) {
  const html = fs.readFileSync(file, 'utf8');
  const a = html.indexOf('<script>') + '<script>'.length;
  const b = html.indexOf(MARKER);
  if (a < 8 || b < 0) throw new Error('generator section not found in index.html');
  const ctx = { console };
  vm.createContext(ctx);
  vm.runInContext(html.slice(a, b) + '\n;globalThis.__gen={makeLevel,simulateReal,tierOf,cycleOf,designFor,EMO,emoDecode,DESIGNS,INTRO};', ctx, { filename: 'index.html#generator' });
  return ctx.__gen;
}
