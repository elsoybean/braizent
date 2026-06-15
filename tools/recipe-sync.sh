#!/usr/bin/env bash
# Two-way git sync for the meal-planning recipe repo served by CookCLI.
# Lives in the braizent repo (tools/), deployed to the Pi, but operates on the
# meal-planning clone (set REPO_DIR). Commits local CookCLI web-UI edits, pulls
# remote (Claude) commits, then pushes. Halts and flags on a real conflict.
set -uo pipefail

REPO_DIR="${REPO_DIR:-/home/pi/meal-planning}"
CONFLICT_FLAG="${CONFLICT_FLAG:-/home/pi/recipe-sync.conflict}"

cd "$REPO_DIR" || exit 1
[ -f "$CONFLICT_FLAG" ] && exit 0

if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "pi: kitchen edits $(date -u +%FT%TZ)" --quiet
fi

if ! git pull --rebase --autostash --quiet; then
  git rebase --abort 2>/dev/null
  { date -u +%FT%TZ
    echo "Sync paused: a file was edited both in the CookCLI UI and via Claude."
    echo "Resolve in $REPO_DIR, then: rm $CONFLICT_FLAG"
  } > "$CONFLICT_FLAG"
  exit 1
fi

git push --quiet
