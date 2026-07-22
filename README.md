# taude.xyz

Hugo site using the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme,
deployed to GitHub Pages via GitHub Actions. Content is written in Obsidian and
published through a sync script.

## How it fits together

- **Theme**: `themes/PaperMod`, installed as a git submodule.
- **Sections**: three content types, each its own top-level section:
  - `content/til/` — short "Today I Learned" notes. Custom layout at
    `layouts/til/list.html` shows a topic-pill row (tags used in TIL, with
    counts) above a compact chronological list, styled after
    [til.simonwillison.net](https://til.simonwillison.net/).
  - `content/posts/` — regular long-form posts. Uses PaperMod's default layout.
  - `content/quotes/` — short quotes. Custom layout at `layouts/quotes/` skips
    the usual title/breadcrumbs/ToC and just renders the blockquote plus
    author/source/date.
- **Standalone pages**: `content/about.md` is a single page, not a section —
  it's synced separately from `About.md` at the vault root rather than from a
  section folder (see `SECTION_MAP` vs. the standalone-file step in
  `scripts/publish.sh`).
- **Search**: PaperMod's built-in Fuse.js search (`content/search.md` +
  `themes/PaperMod/layouts/index.json`) indexes every page on the site
  automatically — nothing to maintain when adding new sections.
- **Deploy**: `.github/workflows/hugo.yml` builds the site with Hugo on every
  push to `master` and deploys straight to GitHub Pages (no `gh-pages` branch,
  no manual `public/` commits). `public/` and `resources/` are gitignored —
  CI regenerates them every time.
- **Claude Code skills**: two skills live in `skills/`, symlinked into
  `~/.claude/skills/` so they're available in any session (see **Claude Code
  skills**, below).

## Writing content in Obsidian

Notes live in the Obsidian vault under:

```
1 Projects/taude.xyz Blog/
├── til/
├── posts/
├── quotes/
├── ai-drafted/
├── About.md
└── templates/
    ├── TIL.md
    ├── Blog Post.md
    ├── Quote.md
    └── AI Draft.md
```

Most vault subfolders map 1:1 to a `content/` section of the same name, but
`ai-drafted/` is an exception — it's an organizational folder only, and its
notes still sync into `content/posts/` (see `SECTION_MAP` in
`scripts/publish.sh`). Use the matching Templater template (via Obsidian's
"Create new note from template" command) to start a new note — it stamps in
the right frontmatter and moves the file into the correct folder
automatically:

- **TIL.md** → `til/` — needs `tags` (topics, e.g. `["hugo", "git"]`).
- **Blog Post.md** → `posts/` — needs `tags`.
- **Quote.md** → `quotes/` — needs `author` and `source` (a URL); the quote
  text itself is the body, written as a markdown blockquote (`> ...`).
- **AI Draft.md** → `ai-drafted/` (publishes as a regular post) — for
  articles where AI wrote most of the content. Defaults to
  `tags: ["ai-drafted"]` so it's transparent on the live site which posts
  had substantial AI authorship.

All templates default to `draft: true`. Flip it to `draft: false` when a
note is ready to go out — `buildDrafts = false` in `hugo.toml` means drafts
never appear on the live site even if they get synced and pushed by mistake.

`About.md`, at the vault root (not inside a section folder, and with no
template — it's a singleton you just edit directly), is the source for the
about page and syncs to `content/about.md`.

Obsidian wikilinks (`[[Note]]`, `[[Note|alias]]`) and embeds (`![[image.png]]`)
are fine to leave in your notes — the publish script resolves or flattens
them automatically (see **What the sync script does**, below). Actual image
*files* are not copied anywhere yet; if you start embedding images, say so
and we'll wire up copying attachments into `static/`.

### Backfilling old content

Every template has an `original_date` field (blank by default). Fill it in
with the true historical publish date when backfilling something written
elsewhere long ago (e.g. an old blog post), and the sync script overwrites
`date` with it — the post sorts, dates, and shows up in RSS/archives at its
real place in the timeline, not wherever `date` (the note's creation date)
happened to land. The single-page view also picks up a "Backdated —
originally published `<date>`, added to this blog later" banner whenever
`original_date` is set, so it's visible to readers that the post predates
this blog rather than looking freshly written. Leave it blank for anything
written now — `date` (auto-filled by Templater) is used as-is.

## Publishing

From the repo root:

```bash
./scripts/publish.sh
```

This:

1. Rsyncs `.md` files from each vault section folder into its mapped
   `content/` folder per `SECTION_MAP` (one-way, vault → repo, and
   **non-destructive** — it only adds/updates files, it never deletes
   anything from `content/`, even if a note is removed from the vault.
   Delete the file in `content/` yourself if a note should come down.)
2. Copies the standalone `About.md` to `content/about.md` the same way
   (a direct copy, not rsync, since it's a single file, not a folder).
3. Cleans up Obsidian-specific syntax in the copied files
   (`scripts/clean_obsidian_links.py`) — see below.
4. Runs `hugo --minify` locally so a broken template or bad frontmatter
   fails here, not in CI.
5. Shows you a `git status` of what changed under `content/`.
6. Prompts before doing anything else — answer `y` to commit and push, or
   `N`/Enter to leave the synced files staged-but-uncommitted for you to
   review or amend by hand.

Pushing to `master` is what actually publishes: GitHub Actions picks up the
push, builds, and deploys to taude.xyz, usually within about a minute. Check
progress with:

```bash
gh run list --repo taudep/taude.xyz --limit 1
```

### What the sync script does to your markdown

`scripts/clean_obsidian_links.py` runs over every synced file (except
`_index.md` section-list pages) and:

- Turns `![[image.png]]` into `![image.png](image.png)`.
- Resolves `[[Note]]` / `[[Note|alias]]` against `KNOWN_PAGES` (currently
  just `about` → `/about/`) into a real markdown link when the target is an
  actually-published page; otherwise flattens it to plain text (`Note` /
  `alias`) — cross-linking to other private vault notes doesn't make sense
  once published. Add an entry to `KNOWN_PAGES` whenever another published
  page starts getting linked to by name.
- Rewrites `draft: "true"` / `draft: "false"` (a quoted string, which is what
  Obsidian Templater's insertion syntax produces) into the real YAML booleans
  `draft: true` / `draft: false`. This matters: a quoted string doesn't
  reliably get treated as a boolean by Hugo, so without this fix a note could
  silently stay in draft (or silently escape draft status) regardless of what
  you intended.
- Overwrites `date` with `original_date` when the latter is set and
  non-blank — see **Backfilling old content**, above.
- Injects an explicit `slug` into frontmatter (derived from the filename,
  lowercased, non-alphanumeric runs collapsed to a single dash) whenever one
  isn't already set. Hugo's own default urlize doesn't strip all stray
  punctuation — a title ending in "." once produced a URL with a literal
  trailing period — so this guarantees a clean URL regardless of what
  Obsidian's filename looks like. Never overrides a `slug` you set yourself.

## Local preview

```bash
hugo server -D
```

`-D` includes drafts, so you can preview unpublished notes at
`localhost:1313` before flipping `draft: false`.

## Claude Code skills

Two skills live under `skills/` and are symlinked into
`~/.claude/skills/`, so they're invocable (by name or naturally, e.g.
"publish my blog") from any Claude Code session, not just one opened in
this repo:

- **`publish-taude-blog`** (`skills/publish-taude-blog/SKILL.md`) —
  documents this whole publish flow (where content lives, how to run
  `scripts/publish.sh`, git safety norms around the push, how to verify
  the GitHub Actions deploy actually completed) so it can be followed
  consistently instead of re-derived each session.
- **`write-ai-slop-article`**
  (`skills/write-ai-slop-article/SKILL.md` +
  `skills/write-ai-slop-article/session_usage.py`) — writes a session
  recap post (what got built, plus real token/message/duration stats
  pulled from the Claude Code session transcript) into the vault's
  `ai-drafted/` folder and publishes it through the same flow. The
  transcript lookup requires an explicit session id rather than
  guessing the most-recently-modified `.jsonl` — two transcripts in the
  same project directory can share an mtime (e.g. a bridged companion
  session), which was confirmed to actually happen, not just a
  theoretical edge case.

Re-symlink after moving either skill's source:

```bash
ln -sf ~/dev/taude.xyz/skills/<name> ~/.claude/skills/<name>
```

## Maintenance notes

- **Adding a new section**: create `content/<name>/`, add a menu entry in
  `hugo.toml`, decide whether it needs a custom layout (`layouts/<name>/`) or
  can just use PaperMod's defaults, add an archetype at
  `archetypes/<name>.md` for `hugo new` scaffolding, and add an entry to
  `SECTION_MAP` in `scripts/publish.sh` (plus a matching Obsidian vault
  folder and Templater template, if it's going to be written there too).
- **Adding a vault-only folder** (organizational, publishes into an
  existing section — e.g. `ai-drafted/` → `content/posts/`): just add an
  entry to `SECTION_MAP` in `scripts/publish.sh` mapping the vault folder
  name to the existing `content/` destination, plus a vault folder and
  Templater template. No `hugo.toml` or layout changes needed.
- **Theme upgrades**: `git submodule update --remote themes/PaperMod`, then
  rebuild locally and check the
  [PaperMod releases](https://github.com/adityatelange/hugo-PaperMod/releases)
  for breaking config changes before pushing.
- **Hugo version**: pinned in `.github/workflows/hugo.yml`
  (`HUGO_VERSION`). Keep it in rough sync with whatever's installed locally
  (`hugo version`) so a local `hugo --minify` is a reliable predictor of what
  CI will do.
- **`public/` and `resources/` are gitignored on purpose** — CI is the only
  thing that should produce `public/`. If either ever ends up tracked again,
  `git rm -r --cached public resources` and confirm they're still in
  `.gitignore`.
