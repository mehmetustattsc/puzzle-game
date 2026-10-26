# Emoji picture pipeline

Turns Microsoft Fluent Emoji (flat, MIT) into the 40×40 palette grids the game draws on its hexagon board.
Names in Turkish, English and German come from the Unicode CLDR emoji annotations.

```bash
mkdir -p work && cd work
git clone --depth 1 --filter=blob:none --sparse https://github.com/microsoft/fluentui-emoji fe
(cd fe && git sparse-checkout set --no-cone '/assets/*/Flat/*.svg' '/assets/*/Default/Flat/*.svg' '/assets/*/metadata.json' '/LICENSE')
git clone --depth 1 --filter=blob:none --sparse https://github.com/unicode-org/cldr-json cldr
(cd cldr && git sparse-checkout set --no-cone '/cldr-json/cldr-annotations-full/annotations/tr/annotations.json' \
  '/cldr-json/cldr-annotations-full/annotations/de/annotations.json' '/cldr-json/cldr-annotations-full/annotations/en/annotations.json')
python3 ../select.py        # 1. candidates          -> cands.json
node ../quant.js            # 2. render + quantise   -> quant.json   (needs Playwright)
python3 ../build.py         # 3. filter, name, sort  -> final.json + contact sheets sh_*.png
python3 ../export.py        # 4. data for index.html -> emo_gen.js, emo_names.js, emo_albums.js
```

Look through the `sh_*.png` contact sheets before exporting: pictures that do not read well on the board are dropped
with the name filters in `build.py` / `export.py`. Bump `LV_VER` in `index.html` whenever the picture list changes.
