#!/usr/bin/env python3
"""Normalize Obsidian-flavored markdown into plain Hugo-friendly markdown.

Run over freshly-synced .md files: resolves [[wikilinks]] that point at
known published pages (see KNOWN_PAGES) into real links and flattens
everything else to plain text (cross-linking to other private vault
notes doesn't make sense once published), turns ![[embeds]] into
standard image syntax, fixes the quoted draft: "true" / "false" strings
Obsidian Templater emits into real YAML booleans so Hugo's buildDrafts
setting actually takes effect, injects an explicit `slug` derived from
the filename so Hugo's default urlize can't leak stray punctuation
(observed: a trailing "." in an Obsidian title produced a URL ending in
a literal period) into a URL, and - when `original_date` is set, for
backfilled content that predates this blog - overwrites `date` with it
so the post sorts and displays with its true historical date rather
than whenever it happened to be synced.
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
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
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
HAS_SLUG = re.compile(r"^slug:\s*\S", re.MULTILINE)
ORIGINAL_DATE = re.compile(r"^original_date:\s*(.*)$", re.MULTILINE)
DATE_LINE = re.compile(r"^date:\s*.*$", re.MULTILINE)


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


def _is_blank(raw: str) -> bool:
    v = raw.strip()
    return v in ("", '""', "''")


# Unambiguous formats only - deliberately no bare "%m/%d/%Y" / "%d/%m/%Y",
# since which is which can't be inferred and a silent misread (e.g. day 3
# read as March) is worse than requiring an unambiguous format.
DATE_INPUT_FORMATS = (
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S%z",
    "%Y-%m-%d",
    "%Y/%m/%d",
)


def normalize_date(raw: str) -> str | None:
    for fmt in DATE_INPUT_FORMATS:
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def apply_original_date(text: str, path: Path) -> str:
    m = FRONTMATTER.match(text)
    if not m:
        return text
    fm = m.group(1)
    od = ORIGINAL_DATE.search(fm)
    if not od or _is_blank(od.group(1)):
        return text
    raw = od.group(1).strip()
    value = normalize_date(raw)
    if value is None:
        # A quoted-but-unparsable date would break the whole `hugo` build,
        # not just this page - leave `date` alone and flag it instead of
        # guessing.
        print(f"warning: {path}: original_date {raw!r} isn't in a recognized "
              f"format (try YYYY-MM-DD), leaving date unchanged", file=sys.stderr)
        return text
    new_fm, n = DATE_LINE.subn(f"date: {value}", fm, count=1)
    if n == 0:
        # No existing `date:` line (e.g. a clipper template that only sets
        # `published`/`created`) - add one rather than silently doing
        # nothing, since Hugo's fallback to those fields would ignore
        # original_date entirely if it ever disagreed with them.
        new_fm = fm + f"\ndate: {value}"
    fm_start, fm_end = m.start(1), m.end(1)
    return text[:fm_start] + new_fm + text[fm_end:]


def slugify(stem: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", stem.lower())
    return slug.strip("-")


def ensure_slug(text: str, stem: str) -> str:
    m = FRONTMATTER.match(text)
    if not m or HAS_SLUG.search(m.group(1)):
        return text
    slug = slugify(stem)
    if not slug:
        return text
    fm_end = m.end(1)
    return f'{text[:fm_end]}\nslug: "{slug}"{text[fm_end:]}'


def main(paths: list[str]) -> None:
    files = []
    for arg in paths:
        p = Path(arg)
        files.extend([p] if p.is_file() else p.rglob("*.md"))

    for path in files:
        if path.name == "_index.md":
            continue
        original = path.read_text(encoding="utf-8")
        cleaned = clean_text(original)
        cleaned = apply_original_date(cleaned, path)
        cleaned = ensure_slug(cleaned, path.stem)
        if cleaned != original:
            path.write_text(cleaned, encoding="utf-8")
            print(f"cleaned: {path}")


if __name__ == "__main__":
    main(sys.argv[1:])
