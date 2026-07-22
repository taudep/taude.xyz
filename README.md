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
- **Search**: PaperMod's built-in Fuse.js search (`content/search.md` +
  `themes/PaperMod/layouts/index.json`) indexes every page on the site
  automatically — nothing to maintain when adding new sections.
- **Deploy**: `.github/workflows/hugo.yml` builds the site with Hugo on every
  push to `master` and deploys straight to GitHub Pages (no `gh-pages` branch,
  no manual `public/` commits). `public/` and `resources/` are gitignored —
  CI regenerates them every time.

## Writing content in Obsidian

Notes live in the Obsidian vault under:

```
1 Projects/taude.xyz Blog/
├── til/
├── posts/
├── quotes/
└── templates/
    ├── TIL.md
    ├── Blog Post.md
    └── Quote.md
```

Each vault subfolder maps 1:1 to a `content/` section of the same name. Use
the matching Templater template (via Obsidian's "Create new note from
template" command) to start a new note — it stamps in the right frontmatter
and moves the file into the correct folder automatically:

- **TIL.md** → `til/` — needs `tags` (topics, e.g. `["hugo", "git"]`).
- **Blog Post.md** → `posts/` — needs `tags`.
- **Quote.md** → `quotes/` — needs `author` and `source` (a URL); the quote
  text itself is the body, written as a markdown blockquote (`> ...`).

All three templates default to `draft: true`. Flip it to `draft: false` when
a note is ready to go out — `buildDrafts = false` in `hugo.toml` means drafts
never appear on the live site even if they get synced and pushed by mistake.

Obsidian wikilinks (`[[Note]]`, `[[Note|alias]]`) and embeds (`![[image.png]]`)
are fine to leave in your notes — the publish script flattens them
automatically (see **What the sync script does**, below). Actual image
*files* are not copied anywhere yet; if you start embedding images, say so
and we'll wire up copying attachments into `static/`.

## Publishing

From the repo root:

```bash
./scripts/publish.sh
```

This:

1. Rsyncs `.md` files from each vault folder into the matching `content/`
   folder (one-way, vault → repo, and **non-destructive** — it only adds/
   updates files, it never deletes anything from `content/`, even if a note
   is removed from the vault. Delete the file in `content/` yourself if a
   note should come down.)
2. Cleans up Obsidian-specific syntax in the copied files
   (`scripts/clean_obsidian_links.py`) — see below.
3. Runs `hugo --minify` locally so a broken template or bad frontmatter
   fails here, not in CI.
4. Shows you a `git status` of what changed under `content/`.
5. Prompts before doing anything else — answer `y` to commit and push, or
   `N`/Enter to leave the synced files staged-but-uncommitted for you to
   review or amend by hand.

Pushing to `master` is what actually publishes: GitHub Actions picks up the
push, builds, and deploys to taude.xyz, usually within about a minute. Check
progress with:

```bash
gh run list --repo taudep/taude.xyz --limit 1
```

### What the sync script does to your markdown

`scripts/clean_obsidian_links.py` runs over every synced file and:

- Turns `![[image.png]]` into `![image.png](image.png)`.
- Flattens `[[Note]]` → `Note` and `[[Note|alias]]` → `alias` (plain text,
  no link — cross-linking to other private vault notes doesn't make sense
  once published).
- Rewrites `draft: "true"` / `draft: "false"` (a quoted string, which is what
  Obsidian Templater's insertion syntax produces) into the real YAML booleans
  `draft: true` / `draft: false`. This matters: a quoted string doesn't
  reliably get treated as a boolean by Hugo, so without this fix a note could
  silently stay in draft (or silently escape draft status) regardless of what
  you intended.

## Local preview

```bash
hugo server -D
```

`-D` includes drafts, so you can preview unpublished notes at
`localhost:1313` before flipping `draft: false`.

## Maintenance notes

- **Adding a fourth section**: create `content/<name>/`, add a menu entry in
  `hugo.toml`, decide whether it needs a custom layout (`layouts/<name>/`) or
  can just use PaperMod's defaults, add an archetype at
  `archetypes/<name>.md` for `hugo new` scaffolding, and add the section name
  to the `for section in til posts quotes` loop in `scripts/publish.sh` (plus
  a matching Obsidian vault folder and Templater template, if it's going to
  be written there too).
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
