#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""List archivore vault articles as newsletter candidates.

Reads archivore's own config (~/.config/archivore/config.yaml) for
output_dir, falling back to its packaged default if unset. Parses each
article's YAML front matter, drops known capture-failure/junk items, and
prints the result as JSON — expanding the lookback window (doubling each
time) until at least --target items are found or the whole vault has been
scanned.

This script only gathers and filters candidates mechanically. Picking the
most interesting --target items from the result, and writing about them,
is a judgment call for whoever reads this output — see SKILL.md.

Usage:
    python3 gather_candidates.py [--days 7] [--target 15]
"""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

DEFAULT_OUTPUT_DIR = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs"
    / "Todd's Obsidian Vault/Archivore/Raw"
)
ARCHIVORE_CONFIG = Path.home() / ".config/archivore/config.yaml"

# Titles that are always a capture failure, never real content.
JUNK_TITLES = {"welcome to reddit"}

# Substrings from archivore's own skip/fallback notes (see
# archivore/clients/fetcher.py and hn.py) — if one of these appears near
# the top of the body, the capture has no real content to write about.
JUNK_BODY_SNIPPETS = (
    "_article unavailable",
    "_skipped: non-html content",
    "_content requires javascript or x login",
)


def resolve_output_dir() -> Path:
    """Read output_dir from archivore's config, else its packaged default."""
    if ARCHIVORE_CONFIG.is_file():
        data = yaml.safe_load(ARCHIVORE_CONFIG.read_text(encoding="utf-8")) or {}
        if data.get("output_dir"):
            return Path(data["output_dir"]).expanduser()
    return DEFAULT_OUTPUT_DIR


def parse_front_matter(text: str) -> dict | None:
    """Split a file into its YAML front matter (parsed) plus body text."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    try:
        fm = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict):
        return None
    fm["_body"] = text[end + 4 :].lstrip("\n")
    return fm


def is_junk(fm: dict) -> bool:
    title = (fm.get("title") or "").strip().lower()
    if title in JUNK_TITLES:
        return True
    body_head = fm.get("_body", "")[:400].lower()
    return any(snippet in body_head for snippet in JUNK_BODY_SNIPPETS)


def extract_authors(fm: dict) -> str | None:
    """author: is a list of "[[Name]]" wikilink strings, or absent."""
    raw = fm.get("author")
    if not raw:
        return None
    names = [str(a).strip("[]").strip() for a in raw] if isinstance(raw, list) else []
    return ", ".join(n for n in names if n) or None


def load_candidates(output_dir: Path, min_words: int) -> list[dict]:
    items = []
    for f in output_dir.glob("*.md"):
        if f.name == "index.md":
            continue
        fm = parse_front_matter(f.read_text(encoding="utf-8", errors="replace"))
        if not fm or not fm.get("created") or is_junk(fm):
            continue
        word_count = len(fm.get("_body", "").split())
        if word_count < min_words:
            # Too thin to write anything real about — usually a JS-rendered
            # page that yielded an empty capture (no fetch_note either).
            continue
        items.append(
            {
                "path": str(f),
                "title": fm.get("title"),
                "id": str(fm.get("id")) if fm.get("id") is not None else None,
                "source": fm.get("source"),
                "author": extract_authors(fm),
                "published": (
                    str(fm["published"]) if fm.get("published") else None
                ),
                "created": str(fm["created"]),
                "discussion": fm.get("hackernews-discussion")
                or fm.get("reddit-discussion"),
                "word_count": word_count,
            }
        )
    items.sort(key=lambda i: i["created"], reverse=True)
    return items


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=7, help="initial lookback window")
    ap.add_argument("--target", type=int, default=15, help="minimum candidates wanted")
    ap.add_argument(
        "--min-words",
        type=int,
        default=40,
        help="drop captures with fewer words than this (usually empty JS-rendered pages)",
    )
    args = ap.parse_args()

    output_dir = resolve_output_dir()
    if not output_dir.is_dir():
        sys.exit(f"output_dir not found: {output_dir}")

    all_items = load_candidates(output_dir, args.min_words)

    days = args.days
    selected = [
        i for i in all_items if i["created"] >= (date.today() - timedelta(days=days)).isoformat()
    ]
    while len(selected) < args.target and len(selected) < len(all_items) and days < 3650:
        days *= 2
        selected = [
            i
            for i in all_items
            if i["created"] >= (date.today() - timedelta(days=days)).isoformat()
        ]

    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "window_days": days,
                "candidate_count": len(selected),
                "total_vault_items": len(all_items),
                "candidates": selected,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
