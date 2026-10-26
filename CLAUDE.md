# Notes for Claude

Owner: Mehmet (Germany). Talk to him in **Turkish**. Goal: a Colony-Flow-like hybrid-casual mobile puzzle earning ~1–2k €/month.

## The game
- Everything is in `index.html` (single file). The script has two parts:
  - **Generator** (from `<script>` up to the marker `/* ================= save, lives, daily`): designs, `buildBoard`,
    `Peeler`, `simulateReal` (real-time replay solver), `routeSearch`, `makeLevel`. This part also runs in a Web Worker
    (`GEN_SRC`) and in the tests, so it must stay free of DOM access.
  - **Game/UI** after the marker: save/lives, i18n (`I18N` TR/EN/DE, `t()`, `nameOf()`), drawing, input, home pages,
    album, team page, shop, audio, cloud save (claude.ai artifact `db`) + save code, analytics (`GC_CODE`, GoatCounter `mehmetusta`),
    error reports (`SENTRY_DSN`, Sentry org `usta-jb`, project `petek-ustasi`, EU region https://de.sentry.io; use the Sentry
    connector to read issues). Analytics and Sentry only run on the GitHub Pages host (`ON_WEB`).
- Levels are deterministic per level number (`mulberry32(4242+L*7919)`). Any generator change: bump `LV_VER`.
- Acceptance rules in `makeLevel` (smart wins; careless / left-to-right (`'seq'`) players must lose depending on tier),
  with a deterministic work budget (`W_STRICT`, `W_SEQ`). Keep generation under ~5 s per level on a laptop.
- Max two special mechanics per level (`allow` set); a mechanic always appears on its intro level (`FIRST`).
- New UI text needs all three languages. Tutorials: `TUT_KEYS`, `tutArt`, `tutsFor`.

## Checks before pushing
`npm test` (generator, ~1 min) and `npm run test:smoke` (browser). CI runs both and deploys to GitHub Pages from `main`.

## Also published as claude.ai artifacts
Dev page and a shareable copy are published from this file via the Artifact tool (capabilities `db` + `user`
for the cloud save). Re-publish both after changes when asked.
