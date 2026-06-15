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
- Bring login: a gitignored `tools/.env` (used by `bring-sync.py`)

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

## bring-sync — CookCLI → Bring feeder (next)

Pushes CookCLI's generated shopping list (recipes scaled, `pantry.conf` subtracted, `aisle.conf` routed) into the shared Bring! list via the `bring-api` package. Ad-hoc and voice items stay native in Bring. Needs `tools/.env` with Bring `email`/`password` — if you signed up with Google/Apple/Facebook, set a password first (Bring app: Profile → More settings → Change password).
