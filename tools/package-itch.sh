#!/usr/bin/env bash
# Builds the zip to upload to itch.io (HTML game, index.html at the root of the zip).
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p dist
rm -f dist/petek-ustasi-itch.zip
zip -q -r dist/petek-ustasi-itch.zip index.html manifest.webmanifest icons
echo "dist/petek-ustasi-itch.zip ($(du -h dist/petek-ustasi-itch.zip | cut -f1))"
