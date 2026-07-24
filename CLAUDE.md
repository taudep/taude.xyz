# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

taude.xyz: a Hugo static site (theme: PaperMod, vendored as a git submodule
at `themes/PaperMod`) deployed to GitHub Pages via GitHub Actions. Content
is written in Obsidian and synced into this repo by `scripts/publish.sh`,
which also builds and pushes. `README.md` has the full architecture
writeup and is the source of truth for the Obsidian/publishing workflow —
read it before making content-pipeline changes; this file only covers
what a coding agent needs that isn't already there or needs emphasis.

## Commands

```bash
./scripts/publish.sh [--preview] [commit message]  # sync Obsidian vault -> content/, build, commit, push
hugo --minify                                      # build only, no sync/commit (use this to verify template/frontmatter changes)
hugo server -D                                     # local preview at localhost:1313, drafts included
python3 scripts/clean_obsidian_links.py <files...>  # run the Obsidian markdown cleanup manually on specific files
gh run list --repo taudep/taude.xyz --limit 1       # check GitHub Actions deploy status after a push
```

There is no test suite and no linter — "does it build" (`hugo --minify`
exits 0, no `ERROR` lines) is the correctness bar for template/config
changes. Always `rm -rf public resources` before a verification build if
a previous build might be stale; a stray `public/` directory left over
from manual testing can also confuse a running `hugo server` (it serves
from that directory on this Hugo version, not purely from memory).

`.hugo_build.lock` is a leftover lockfile Hugo creates/removes automatically;
don't touch it by hand and don't worry if it appears in `git status` as
untracked (it's gitignored).

## Architecture

**Content sections vs. standalone pages vs. vault-only folders** — three
different sync patterns, don't confuse them:
- `content/{til,posts,quotes}/` are real Hugo sections, each 1:1 with a
  vault folder of the same name, synced via rsync per `SECTION_MAP` in
  `scripts/publish.sh`.
- `content/about.md` and `content/experiments.md` are standalone pages (no
  section, no list view), each synced by a direct file copy from a
  same-named vault root file per `STANDALONE_MAP` in the same script.
- The vault's `ai-drafted/` folder is neither: it's purely an Obsidian-side
  organizational folder whose notes still land in `content/posts/` (see
  `SECTION_MAP`'s `ai-drafted:posts` entry) — there is no
  `content/ai-drafted/` section on the Hugo side.

**Layout override strategy**: everything under project-level `layouts/`
shadows a same-path theme file and is a deliberate, targeted override, not
a full fork — check `themes/PaperMod/layouts/` for the original before
editing any of these, since the intent is usually "theme's version plus
one change":
- `layouts/baseof.html` — wraps `<main>` and `layouts/_partials/sidebar.html`
  in a `.page-layout` flex container so every page gets the sidebar.
  Otherwise identical to the theme's `baseof.html`.
- `layouts/index.html` — home page only (Hugo prefers this over the
  theme's `list.html` for `.IsHome`). Renders posts as a tight one-line
  list (date + title, with an AI-drafted icon inline) instead of the
  theme's full-summary cards. Only pulls from the `posts` section — til
  and quotes are intentionally excluded from the homepage.
- `layouts/posts/list.html` and `layouts/posts/single.html` — the `/posts/`
  list page and single-post view, each adding the same AI-drafted marker
  (icon in list, full banner in single) wherever a post's tags intersect
  `["ai-slop", "ai-drafted"]`. Keep this tag-check logic (and the
  `--ai-accent` color) in sync across both files and `layouts/index.html`
  if the AI-marking scheme changes.
- `layouts/_partials/post_meta.html` — adds a "Backdated" banner above the
  normal post meta line whenever `original_date` is set in frontmatter.
  Because list pages also call `partial "post_meta.html"`, this banner
  shows in list-entry footers too, not just single-post view.
- `layouts/_partials/extend_head.html` — hooks the theme's empty
  `extend_head.html` extension point to inject a pre-paint script that
  reads the AI-hide toggle preference from `localStorage` and sets
  `data-hide-ai` on `<html>` before first render (avoids a flash of AI
  content on reload). The actual hide rule lives in
  `assets/css/extended/custom.css` as
  `html[data-hide-ai="true"] .home-entry--ai { display: none }`; the
  toggle UI + its own preference-writing script live inline in
  `layouts/_partials/sidebar.html` (home page only).
- `layouts/til/list.html`, `layouts/quotes/{list,single}.html` — custom
  layouts for those sections' non-default presentation (topic-pill row for
  til, blockquote-only rendering for quotes).

**CSS**: all custom styling lives in `assets/css/extended/custom.css`,
which Hugo auto-concatenates after the theme's core CSS (any
`css/extended/*.css` file gets picked up automatically — see
`themes/PaperMod/layouts/_partials/head.html`). Reuses the theme's CSS
custom properties (`--primary`, `--secondary`, `--border`, `--code-bg`,
`--content-gap`, etc.) rather than hardcoding colors, so it inherits
light/dark theme support for free. `--ai-accent` (`#cc785c`, Anthropic's
Claude terracotta) is the one deliberate custom color, used only for the
AI-drafted icons/banner.

**JS**: no framework, no separate JS files — small inline `<script>` blocks
directly in the relevant partial (`extend_head.html`, `sidebar.html`),
matching the theme's own convention in `_partials/footer.html`
(dark-mode toggle, scroll-to-top, etc. are all inline scripts there too).

**Tags with special meaning** (not just display metadata): a post's tags
are checked against `["ai-slop", "ai-drafted"]` in three layout files (see
above) to decide whether to show the AI-drafted marker; `pinned: true` in
any note's frontmatter adds it to the sidebar's "Pinned" list
(`layouts/_partials/sidebar.html`, which also merges in static
`params.pinnedLinks` from `hugo.toml`); `original_date` in frontmatter
triggers both a `date` overwrite (in `clean_obsidian_links.py`) and the
backdated banner (in `post_meta.html`).

**`clean_obsidian_links.py` internals worth knowing before editing it**:
- `original_date` → `date` normalization only accepts a small set of
  *unambiguous* formats (`YYYY-MM-DD`, `YYYY/M/D`, with optional
  `THH:MM:SS±HH:MM`) — deliberately no bare `%m/%d/%Y` or `%d/%m/%Y`, since
  which is which can't be inferred from the string alone and a silent
  misread is worse than requiring an unambiguous one. An unparsable value
  prints a warning and leaves `date` untouched rather than writing
  something that would break the whole `hugo` build (this happened for
  real with a clipper-imported quote's `2023/1/24`). If the source
  frontmatter has no `date:` line at all (e.g. a clipper template that
  only sets `published`/`created`), one is inserted rather than skipped —
  Hugo's own fallback to those alternate field names would otherwise
  silently ignore `original_date` if it ever disagreed with them.
- `[[wikilinks]]` only resolve to a real link if the target is a key in
  the `KNOWN_PAGES` dict (currently just `about` → `/about/`); anything
  else flattens to plain text. Add an entry there when another actually-
  published page starts getting linked to by name from vault notes.

**Claude Code skills**: `skills/publish-taude-blog/` and
`skills/write-ai-slop-article/` (the latter also ships
`session_usage.py`, which sums token usage from a Claude Code session
transcript — reads `~/.claude/projects/<slug>/<session-id>.jsonl`, and
requires an explicit session id rather than guessing the newest file,
since two transcripts in the same project directory can share an mtime).
Both are symlinked into `~/.claude/skills/`, so keep their `SKILL.md`
instructions in sync with actual script behavior when either changes —
they're a second, easily-forgotten place the same facts (flags, file
paths, section list) get restated.

**Deploy**: `.github/workflows/hugo.yml` builds with a pinned Hugo version
(`HUGO_VERSION` env var — keep roughly in sync with the locally-installed
`hugo version` so local builds predict CI) and deploys straight to GitHub
Pages on every push to `master`. No `gh-pages` branch, no committed
`public/`.
