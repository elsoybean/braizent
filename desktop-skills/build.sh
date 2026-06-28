#!/usr/bin/env bash
#
# build.sh — package the desktop skills into uploadable .zip files.
#
# Consumer Claude skills upload as self-contained folders, so each authoring
# skill references _recipe-saver.md as a FOLDER-LOCAL file. The canonical copy
# lives at desktop-skills/_recipe-saver.md; this script stages each skill, drops
# that contract into the authoring ones, and zips the result. The working skill
# folders stay clean (just SKILL.md) — the copies exist only in build output.
#
# Output: desktop-skills/dist/<skill>.zip   (dist/ is gitignored)
# Requires: zip
#
# Usage:  bash build.sh      (run from anywhere; it locates its own dir)

set -euo pipefail
shopt -s nullglob

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

SAVER="_recipe-saver.md"
DIST_ABS="$HERE/dist"
STAGE="$DIST_ABS/.stage"

# Authoring skills get a bundled copy of the save contract; others don't.
AUTHORING=(kitchen-riff import-recipe research-recipe recipe-variant quick-staple)

command -v zip >/dev/null 2>&1 || { echo "error: 'zip' is not installed" >&2; exit 1; }
[ -f "$SAVER" ] || { echo "error: $SAVER not found next to build.sh" >&2; exit 1; }

is_authoring() {
  local name="$1" a
  for a in "${AUTHORING[@]}"; do [ "$a" = "$name" ] && return 0; done
  return 1
}

rm -rf "$DIST_ABS"
mkdir -p "$STAGE"

count=0
for skill_md in */SKILL.md; do
  skill="$(dirname "$skill_md")"
  staged="$STAGE/$skill"

  mkdir -p "$staged"
  cp "$skill/SKILL.md" "$staged/SKILL.md"

  # Carry along any other resources already in the skill folder (future-proof).
  for extra in "$skill"/*; do
    [ "$(basename "$extra")" = "SKILL.md" ] && continue
    cp -R "$extra" "$staged/"
  done

  # Authoring skills get the canonical save contract, bundled folder-local.
  if is_authoring "$skill"; then
    cp "$SAVER" "$staged/$SAVER"
  fi

  # Zip with files at the archive root (SKILL.md at the top of the zip).
  # If your uploader wants a wrapping folder instead, zip "$skill" from "$STAGE".
  ( cd "$staged" && zip -q -r "$DIST_ABS/$skill.zip" . )
  echo "packaged $skill -> dist/$skill.zip"
  count=$((count + 1))
done

rm -rf "$STAGE"
echo "done: $count skill(s) packaged in dist/"
