# Pi tools

Operational tooling for the kitchen recipe system, run on the Raspberry Pi that hosts CookCLI. These scripts aren't part of the braizent Claude Code plugin — they live here because braizent is the code repo (meal-planning stays data-only).

## Pi layout assumed

```
/home/pi/braizent/        # this repo (plugin + these tools)
/home/pi/meal-planning/   # recipe DATA repo; CookCLI serves cook/ from here
```

## Secrets — never commit

Bring credentials and the GitHub deploy key are secrets; they live on the Pi only:

- GitHub push auth: an SSH deploy key in `~/.ssh/`
- Bring login: a gitignored `tools/.env` (copy from `.env.example`)

`.env` and `*.conflict` are gitignored here.

---

## recipe-sync — two-way git sync

Keeps the meal-planning clone in sync both directions: commits edits made in the CookCLI web UI, pulls commits made by Claude, then pushes. On a real conflict (same file edited in the UI and via Claude within one ~60s window) it halts and writes `/home/pi/recipe-sync.conflict` instead of guessing a winner.

### Setup

1. Push access to the private meal-planning repo via an SSH deploy key:

```
ssh-keygen -t ed25519 -f ~/.ssh/meal-planning-deploy -N ""
# Add the .pub to GitHub: meal-planning > Settings > Deploy keys (Allow write access)
# Point the clone's remote at the SSH URL and use this key via ~/.ssh/config
cd /home/pi/meal-planning && git push   # must succeed without prompting
```

2. Git identity for the Pi's commits:

```
cd /home/pi/meal-planning
git config user.name "Kitchen Pi"
git config user.email "pi@kitchen.local"
```

3. Install and start the timer:

```
chmod +x /home/pi/braizent/tools/recipe-sync.sh
sudo cp /home/pi/braizent/tools/recipe-sync.service /etc/systemd/system/
sudo cp /home/pi/braizent/tools/recipe-sync.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now recipe-sync.timer
systemctl list-timers recipe-sync.timer
journalctl -u recipe-sync.service -f
```

It syncs whatever branch the clone has checked out (currently `main`).

### Conflicts

When paused, `/home/pi/recipe-sync.conflict` explains what to do. Resolve in `/home/pi/meal-planning` with normal git, then `rm /home/pi/recipe-sync.conflict`.

---

## bring-sync — CookCLI -> Bring feeder

Pushes CookCLI's recipe-derived shopping list into a single shared Bring! list. The store channel (the `aisle.conf` section — Knuspr / Rewe / Asian market / Hand-pick) is written into Bring's item **specification** after the quantity, so one list carries everything:

```
Pointed cabbage        400 g · Knuspr
Chicken leg quarters   2 · Rewe
```

Ad-hoc and voice-added items stay native in Bring and are never touched.

### Requirements

```
pip install bring-api aiohttp
```

`cook` must be on PATH.

### Config

Copy `.env.example` to `.env` (gitignored) and fill in `BRING_EMAIL`, `BRING_PASSWORD`, `BRING_LIST`, and paths. If you signed up for Bring with Google/Apple/Facebook, set a password first (Bring app: Profile -> More settings -> Change password); you can still sign in with Google afterward.

### Usage

```
python3 bring-sync.py --dry-run            # preview using cook/.shopping-list
python3 bring-sync.py                       # push to Bring
python3 bring-sync.py sarmale.cook flan.cook   # explicit recipes
```

**Always run `--dry-run` first** after any change — it prints exactly what would be added and never contacts Bring.

### Notes

- **JSON shape:** the parser targets CookCLI's documented `-f json` output, but the exact schema can vary by version. If `--dry-run` is empty or odd, run `cook shopping-list -f json <recipe>` once and adjust `parse_items()` — it's isolated for that.
- **Config location:** the CookCLI web server discovers `aisle.conf`/`pantry.conf` at the **root of the served recipe folder** (`cook/aisle.conf`, `cook/pantry.conf`), so that's where they live and what `bring-sync` defaults to. (The `cook shopping-list`/`cook pantry` CLI commands also look in a `config/` subdir, but the server doesn't pick them up there — root is the working location.) Override `AISLE_CONF`/`PANTRY_CONF` only if your layout differs.
- **Scheduling:** run on demand, or wrap in a systemd timer like `recipe-sync` if you want it periodic.
