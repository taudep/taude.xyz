#!/usr/bin/env python3
"""Normalize Obsidian-flavored markdown into plain Hugo-friendly markdown.

Run over freshly-synced .md files: resolves [[wikilinks]] that point at
known published pages (see KNOWN_PAGES) into real links and flattens
everything else to plain text (cross-linking to other private vault
notes doesn't make sense once published), turns ![[embeds]] into
standard image syntax, and fixes the quoted draft: "true" / "false"
strings Obsidian Templater emits into real YAML booleans so Hugo's
buildDrafts setting actually takes effect.
"""
import re
import sys
from pathlib import Path

# Wikilink targets (case-insensitive) that map to a real page on the site.
# Add an entry here whenever a note that's actually published gets linked
# to by name - everything else just gets flattened to plain text.
KNOWN_PAGES = {
    "about": "/about/",
}

WIKILINK_EMBED = re.compile(r"!\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
DRAFT_STRING = re.compile(r'^(draft:\s*)"(true|false)"\s*$', re.MULTILINE)


def resolve_wikilink(match: re.Match) -> str:
    target = match.group(1).strip()
    label = (match.group(2) or target).strip()
    url = KNOWN_PAGES.get(target.lower())
    return f"[{label}]({url})" if url else label


def clean_text(text: str) -> str:
    text = WIKILINK_EMBED.sub(lambda m: f"![{(m.group(2) or m.group(1))}]({m.group(1)})", text)
    text = WIKILINK.sub(resolve_wikilink, text)
    text = DRAFT_STRING.sub(lambda m: f"{m.group(1)}{m.group(2)}", text)
    return text


def main(paths: list[str]) -> None:
    files = []
    for arg in paths:
        p = Path(arg)
        files.extend([p] if p.is_file() else p.rglob("*.md"))

    for path in files:
        original = path.read_text(encoding="utf-8")
        cleaned = clean_text(original)
        if cleaned != original:
            path.write_text(cleaned, encoding="utf-8")
            print(f"cleaned: {path}")


if __name__ == "__main__":
    main(sys.argv[1:])
