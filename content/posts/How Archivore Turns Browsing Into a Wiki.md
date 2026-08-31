---
title: How Archivore Turns Browsing Into a Wiki
date: 2026-08-31T10:26:41-04:00
draft: false
tags:
  - ai-slop
  - archivore
  - obsidian
  - claude-code
slug: "how-archivore-turns-browsing-into-a-wiki"
---
This one's ai-slop, as advertised on the [about page](/about/) — built with
Claude Code over a couple of months of on-and-off sessions.

Most people who read a lot online never see any of it again. Someone
opens an article, skims it, closes the tab, and forgets it — buried
inside browser history nobody searches. [Archivore](https://github.com/taudep/archivore),
a small command-line tool, exists to fix that one habit at a time.

The idea is simple: capture everything worth keeping, automatically.
Archivore scans browser history since its last run, picks out links from
Hacker News, Reddit, and X, downloads the linked article, and converts
it to Markdown. Nothing requires manual saving or tagging. Opening a
link in a browser is enough.

What happens to that Markdown is the useful part. Every file lands in an
Obsidian vault with proper front matter — title, source, author, the
date it was actually read — so a capture becomes part of a personal
wiki rather than an orphaned text file. An index tracks everything
gathered, and a semantic-search tool called [qmd](https://github.com/tobi/qmd)
indexes the whole vault, so old reading can be found by meaning, not
just keyword.

Running archivore on more than one machine used to mean duplicate
downloads, since each kept its own local queue. A small, free-tier
Cloudflare Worker backed by a D1 database fixed that: every machine now
claims and completes items against one shared queue, so nothing gets
fetched twice. Four network calls per run keep every machine in sync,
regardless of how many articles were captured.

Reduced to its essentials, the architecture is a straight line: browser
history feeds `archivore run`, which coordinates against the shared
queue, writes Markdown into the vault, and hands the result to qmd for
search.

None of it publishes anything yet. Archivore's second half — turning
weeks of captured reading into actual essays, using Claude — stays on
the [roadmap](https://github.com/taudep/archivore#roadmap). For now it
does the unglamorous part well: it remembers, so its owner doesn't have
to.

## Session stats

The session behind this post ran from July 1st to August 31st, 2026 —
two months, on and off, in one continuous conversation. Across 1,779
assistant turns, it used 3,402 fresh input tokens, 1,632,727 output
tokens, 22,040,856 cache-creation tokens, and 661,622,906 cache-read
tokens. That last figure looks alarming until you account for pricing:
cache reads cost a fraction of fresh input, and most of that total is
Claude re-reading context it had already built up, not new work.
