---
name: publish-taude-blog
description: Use this skill when the user wants to publish, sync, or push new content for taude.xyz (Todd's Hugo blog) from his Obsidian vault - e.g. "publish my blog", "sync my TILs", "push my new post", "republish my about page". Handles running the sync script, reviewing what changed, committing, pushing to GitHub, and confirming the GitHub Pages deploy succeeded.
---

# Publish taude.xyz from Obsidian

taude.xyz is a Hugo site (theme: PaperMod) in the repo at
`~/dev/taude.xyz`, deployed to GitHub Pages via GitHub Actions on every
push to `master`. Content is written in Obsidian and synced into the repo
by `scripts/publish.sh` — see that repo's `README.md` for the full
architecture writeup if more background is needed than what's here.

## Where content lives

Obsidian vault, under:
```
~/Library/Mobile Documents/com~apple~CloudDocs/Todd's Obsidian Vault/1 Projects/taude.xyz Blog/
├── til/         → content/til/     (Today I Learned, custom topic-pill layout)
├── posts/       → content/posts/   (long-form posts)
├── quotes/      → content/quotes/  (short quotes, custom layout)
├── About.md     → content/about.md (standalone page, not a section)
└── templates/   (Obsidian Templater templates: TIL.md, Blog Post.md, Quote.md)
```

## How to publish

1. `cd ~/dev/taude.xyz`
2. Run `./scripts/publish.sh`. This:
   - rsyncs `.md` files from each vault section folder into the matching
     `content/` folder (one-way, additive only — it never deletes files
     from `content/`, even if a note is removed from the vault)
   - copies the standalone `About.md` into `content/about.md`
   - cleans up Obsidian-specific syntax via `scripts/clean_obsidian_links.py`:
     flattens `[[wikilinks]]`, converts `![[embeds]]` to standard markdown
     image syntax, and fixes `draft: "true"/"false"` (a quoted string,
     which is what Obsidian Templater emits) into real YAML booleans so
     Hugo's `buildDrafts = false` actually takes effect
   - builds the site locally with `hugo --minify` to catch broken
     templates or bad frontmatter before anything is pushed
   - prints a `git status --short` of what changed
   - prompts `Commit and push these changes? [y/N]`
3. **Follow the repo's git safety norms even though the script has its own
   prompt**: show the user what changed (the diff/status) and get an
   explicit go-ahead in chat before answering that prompt with `y` — don't
   treat running the script as implicit permission to push. If the user's
   request already was an explicit instruction to publish/push (e.g. "yes
   push it", "republish my about"), that counts as the go-ahead — no need
   to ask a second time.
4. After pushing, confirm the deploy actually succeeded rather than
   assuming the push did the job:
   ```bash
   until [ "$(gh run list --repo taudep/taude.xyz --limit 1 --json headSha -q '.[0].headSha')" = "$(git rev-parse HEAD)" ]; do sleep 3; done
   until [ "$(gh run list --repo taudep/taude.xyz --limit 1 --json status -q '.[0].status')" = "completed" ]; do sleep 5; done
   gh run list --repo taudep/taude.xyz --limit 1
   ```
   Report success/failure, not just "pushed."

## Notes and gotchas

- `content/`, not the vault, is what actually ships — if a file needs to
  be pulled *back* out of publication, delete it from `content/` directly
  (the sync is one-way and additive, so removing it from the vault alone
  does nothing).
- Drafts (`draft: true`) never build (`buildDrafts = false` in
  `hugo.toml`) — safe to sync/commit/push a draft, it just won't be live
  until flipped to `false`.
- If `hugo --minify` fails inside the script, stop — don't force a push.
  Diagnose the template/frontmatter error first.
- Fresh clone of the repo needs `git submodule update --init --recursive`
  before `hugo` will find the PaperMod theme.
- Adding a fourth Obsidian-synced section: create the matching vault
  folder, add it to the `for section in til posts quotes` loop in
  `scripts/publish.sh`, add a menu entry in `hugo.toml`, and decide if it
  needs a custom layout under `layouts/<name>/` or can use PaperMod's
  defaults.
