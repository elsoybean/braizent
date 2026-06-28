#!/usr/bin/env python3
"""
bring-sync: push CookCLI's recipe-derived shopping list into a shared Bring! list.

Reads the recipes currently on the CookCLI shopping list (cook/.shopping-list),
runs `cook shopping-list -f json` with the aisle + pantry configs, and adds each
resulting item to ONE Bring! list. The store channel (the aisle.conf section, e.g.
Knuspr / Rewe / Hand-pick) is written into Bring's item specification after the
quantity, so a single shared list carries everything:

    Pointed cabbage        400 g · Knuspr
    Chicken leg quarters   2 · Rewe

Ad-hoc and voice-added items live natively in Bring and are never touched.

Config via environment or tools/.env (see .env.example). Always preview with
--dry-run first; it prints what would be added and never contacts Bring.
"""
import argparse
import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path


def load_env(path):
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


load_env(Path(__file__).with_name(".env"))

COOK_DIR = Path(os.environ.get("COOK_DIR", "/home/pi/meal-planning/cook"))
AISLE_CONF = Path(os.environ.get("AISLE_CONF", str(COOK_DIR / "config" / "aisle.conf")))
PANTRY_CONF = Path(os.environ.get("PANTRY_CONF", str(COOK_DIR / "config" / "pantry.conf")))
BRING_EMAIL = os.environ.get("BRING_EMAIL")
BRING_PASSWORD = os.environ.get("BRING_PASSWORD")
BRING_LIST = os.environ.get("BRING_LIST")


def recipe_refs_from_shopping_list():
    """Read recipe references (lines starting with ./) from cook/.shopping-list,
    converting the convention's {multiplier} into CookCLI's name:multiplier form."""
    f = COOK_DIR / ".shopping-list"
    if not f.exists():
        return []
    refs = []
    for raw in f.read_text().splitlines():
        line = raw.split("--", 1)[0].strip()
        if not line.startswith("./"):
            continue
        ref = line[2:]
        mult = None
        if ref.endswith("}") and "{" in ref:
            ref, _, m = ref.partition("{")
            mult = m.rstrip("}").strip()
        refs.append(ref + ":" + mult if mult else ref)
    return refs


def run_cook_shopping_list(recipes):
    cmd = ["cook", "shopping-list", "-f", "json"]
    if AISLE_CONF.exists():
        cmd += ["-a", str(AISLE_CONF)]
    if PANTRY_CONF.exists():
        cmd += ["-p", str(PANTRY_CONF)]
    cmd += recipes
    proc = subprocess.run(cmd, cwd=str(COOK_DIR), capture_output=True, text=True)
    if proc.returncode != 0:
        print("cook shopping-list failed:")
        print(proc.stderr)
        sys.exit(1)
    return json.loads(proc.stdout)


def fmt_qty(q):
    if isinstance(q, list):
        parts = []
        for item in q:
            if isinstance(item, dict):
                val = item.get("value", item.get("quantity", ""))
                unit = item.get("unit", "")
                piece = str(val)
                if unit:
                    piece = piece + " " + str(unit)
                parts.append(piece.strip())
            else:
                parts.append(str(item))
        return ", ".join(p for p in parts if p)
    if isinstance(q, dict):
        return fmt_qty([q])
    return str(q) if q is not None else ""


def parse_items(data):
    """Normalise CookCLI JSON into [(name, quantity_str, channel), ...].

    The exact JSON shape can vary by CookCLI version; this handles the common
    aisle-grouped shapes. If --dry-run shows empty/odd output, run
    `cook shopping-list -f json <recipe>` and adjust this function.
    """
    results = []

    def add(name, qty, channel):
        if name:
            results.append((str(name).strip(), fmt_qty(qty), str(channel or "").strip()))

    if isinstance(data, dict) and "categories" in data:
        for cat in data["categories"]:
            channel = cat.get("category") or cat.get("name") or ""
            for it in cat.get("items", []):
                add(it.get("name"), it.get("quantity"), channel)
    elif isinstance(data, dict):
        for channel, items in data.items():
            if isinstance(items, list):
                for it in items:
                    if isinstance(it, dict):
                        add(it.get("name"), it.get("quantity"), channel)
    elif isinstance(data, list):
        for it in data:
            if isinstance(it, dict):
                add(it.get("name"), it.get("quantity"), it.get("category", ""))
    return results


def spec_for(qty, channel):
    return " · ".join(b for b in (qty, channel) if b)


async def push_to_bring(items, dry_run):
    if dry_run:
        for name, qty, channel in items:
            print("  " + name.ljust(30) + " " + spec_for(qty, channel))
        print()
        print("[dry-run] " + str(len(items)) + " item(s) would be added; Bring not contacted.")
        return

    import aiohttp
    from bring_api import Bring

    if not (BRING_EMAIL and BRING_PASSWORD):
        sys.exit("Set BRING_EMAIL and BRING_PASSWORD (see tools/.env).")

    async with aiohttp.ClientSession() as session:
        bring = Bring(session, BRING_EMAIL, BRING_PASSWORD)
        await bring.login()
        lists = (await bring.load_lists())["lists"]
        if BRING_LIST:
            target = next((l for l in lists if l.get("name") == BRING_LIST), None)
            if target is None:
                names = [l.get("name") for l in lists]
                sys.exit("Bring list not found: " + BRING_LIST + " (have: " + str(names) + ")")
        else:
            target = lists[0]
        list_uuid = target["listUuid"]

        have = set()
        try:
            existing = await bring.get_list(list_uuid)
            for it in existing["items"]["purchase"]:
                have.add(str(it["name"]).lower())
        except (KeyError, TypeError):
            pass

        added = 0
        skipped = 0
        for name, qty, channel in items:
            if name.lower() in have:
                skipped += 1
                continue
            await bring.save_item(list_uuid, name, spec_for(qty, channel))
            added += 1
        print("Bring list " + str(target.get("name")) + ": " + str(added) + " added, " + str(skipped) + " already present.")


def main():
    ap = argparse.ArgumentParser(description="Push CookCLI shopping list into Bring!")
    ap.add_argument("recipes", nargs="*", help="recipe refs/names; default: read cook/.shopping-list")
    ap.add_argument("--dry-run", action="store_true", help="print items without contacting Bring")
    args = ap.parse_args()

    recipes = args.recipes or recipe_refs_from_shopping_list()
    if not recipes:
        sys.exit("No recipes given and cook/.shopping-list is empty.")

    data = run_cook_shopping_list(recipes)
    items = parse_items(data)
    if not items:
        sys.exit("Parsed an empty shopping list; check the JSON shape in parse_items().")

    asyncio.run(push_to_bring(items, args.dry_run))


if __name__ == "__main__":
    main()
