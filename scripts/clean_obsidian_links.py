#!/usr/bin/env python3
"""Normalize Obsidian-flavored markdown into plain Hugo-friendly markdown.

Run over freshly-synced .md files: flattens [[wikilinks]] to plain text,
turns ![[embeds]] into standard image syntax, and fixes the quoted
draft: "true" / "false" strings Obsidian Templater emits into real
YAML booleans so Hugo's buildDrafts setting actually takes effect.
"""
import re
import sys
from pathlib import Path

WIKILINK_EMBED = re.compile(r"!\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
DRAFT_STRING = re.compile(r'^(draft:\s*)"(true|false)"\s*$', re.MULTILINE)


def clean_text(text: str) -> str:
    text = WIKILINK_EMBED.sub(lambda m: f"![{(m.group(2) or m.group(1))}]({m.group(1)})", text)
    text = WIKILINK.sub(lambda m: m.group(2) or m.group(1), text)
    text = DRAFT_STRING.sub(lambda m: f"{m.group(1)}{m.group(2)}", text)
    return text


def main(paths: list[str]) -> None:
    for root in paths:
        for path in Path(root).rglob("*.md"):
            original = path.read_text(encoding="utf-8")
            cleaned = clean_text(original)
            if cleaned != original:
                path.write_text(cleaned, encoding="utf-8")
                print(f"cleaned: {path}")


if __name__ == "__main__":
    main(sys.argv[1:])
