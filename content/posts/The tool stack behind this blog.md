---
title: "The tool stack behind this blog"
date: 2026-07-22T16:00:00+03:00
draft: false
tags: ["ai-slop", "hugo", "obsidian", "claude-code"]
slug: "the-tool-stack-behind-this-blog"
---

This one's ai-slop, as advertised on the [about page](/about/) — I paired
with Claude Code to build this site's entire publishing pipeline, and it
seemed only right to have it write up its own plumbing.

Here's what's actually running under the hood.

## Hugo, with PaperMod

The site is a static [Hugo](https://gohugo.io/) build using the
[PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme,
installed as a proper git submodule (not vendored — `git submodule update
--remote themes/PaperMod` pulls upstream changes when I want them). Two
sections get custom layouts instead of PaperMod's defaults:

- **TIL** gets a topic-pill row up top (tag names with counts, sorted by
  frequency) above a compact chronological list — lifted straight from the
  look of [til.simonwillison.net](https://til.simonwillison.net/).
- **Quotes** skips the usual title/breadcrumbs/table-of-contents entirely
  and just renders a blockquote plus author, source link, and date.

Everything else — Posts, the About page, tag pages, search — uses
PaperMod's stock layout.

## GitHub Actions, not a `gh-pages` branch

Deploys go through GitHub's "Pages via Actions" workflow: push to
`master`, a GitHub Actions job builds the site with Hugo and deploys the
result directly. No `public/` folder committed to the repo, no
`gh-pages` branch to keep in sync — `public/` and `resources/` are
gitignored, and CI is the only thing that ever generates them.

## Search

PaperMod ships a client-side Fuse.js search that indexes every page on
the site via a generated `index.json`. I didn't have to configure
anything for TIL or Quotes to show up in search results — it's automatic
for any section, present and future.

## Writing in Obsidian

The actual writing happens in Obsidian, in a vault folder with one
subfolder per content type:

```
til/     → short "today I learned" notes
posts/   → long-form posts (like this one)
quotes/  → quotes worth remembering
```

plus a standalone `About.md` for the about page. Templater templates for
each type stamp in the right frontmatter and file it into the right
folder automatically, so starting a new TIL or quote is just "new note
from template," not "remember the exact frontmatter schema."

## The sync script

A [`scripts/publish.sh`](https://github.com/taudep/taude.xyz/blob/master/scripts/publish.sh)
script is the bridge between "notes in Obsidian" and "live on taude.xyz."
It rsyncs markdown out of each vault folder into the matching `content/`
folder in the Hugo repo, cleans up a few
[Obsidian-isms](https://github.com/taudep/taude.xyz/blob/master/scripts/clean_obsidian_links.py)
along the way — flattens `wikilinks`, converts `![embeds](embeds)` to
normal markdown image syntax, and fixes the quoted `draft: "true"`
string Templater writes into a real YAML boolean, since a quoted string
doesn't reliably behave like a boolean to Hugo — then
builds the site locally with `hugo --minify` so a broken template fails
on my machine instead of in CI. If the build's clean, it shows me what
changed and asks before committing and pushing.

It's one-way and additive on purpose: deleting a note from the vault
doesn't delete it from the published site. If something needs to come
down, that's a deliberate edit to `content/`, not a side effect of vault
housekeeping.

## Making it repeatable

The last piece was turning all of that into a
[Claude Code skill](https://github.com/taudep/taude.xyz/blob/master/skills/publish-taude-blog/SKILL.md) —
a markdown file describing the whole flow (where content lives, how to
run the sync, how to verify the GitHub Actions deploy actually
succeeded) that lives in this repo and is symlinked into
`~/.claude/skills`. So "publish my blog" is now a thing I can just say,
in any session, and have it done the same way every time — instead of
re-explaining the pipeline from scratch.
