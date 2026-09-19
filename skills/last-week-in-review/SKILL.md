---
name: last-week-in-review
description: Use when the user wants a weekly newsletter-style digest of interesting things from their archivore reading feed published to taude.xyz — e.g. "/last-week-in-review", "write this week's newsletter", "what should go in this week's roundup". Triggers on requests for a digest/roundup/newsletter of recently captured articles, not a single-article writeup.
---

# Last Week in Review

Turns archivore's captured reading (Hacker News, X, and whatever other
sources it's watching) into a Substack-style newsletter: roughly 15
picks, each with a short blurb in Todd's voice on why it's worth reading.
Publishes to taude.xyz's dedicated `/newsletter/` section.

## 1. Gather candidates

```bash
uv run <this skill's dir>/gather_candidates.py --days 7 --target 15 > /tmp/newsletter_candidates.json
```

**Redirect stdout only — never `2>&1`.** On its first run in a fresh
environment, `uv` prints an "Installed N packages" line; with `2>&1` that
lands ahead of the JSON in the same file and breaks parsing. Read the
result with a real JSON parser, not by eyeballing it.

Contains: every non-junk, non-empty capture from the last 7 days (path,
title, id, source URL, author, published, created, discussion link, word
count), sorted newest-first. If fewer than 15 qualify, it automatically
doubles the lookback window and retries until it hits 15 or exhausts the
vault — `window_days` in the output tells you how far back it actually
had to go. It already drops known capture failures ("Welcome to Reddit"
placeholders, HTTP-error notes, empty JS-rendered pages) — you don't need
to re-filter those.

## 2. Shortlist from metadata first

Don't open all 15–40 files yet — that's expensive and most of the
judgment call can be made from title, source domain, author, and word
count alone. From the JSON, pick roughly 15–20 that look genuinely worth
a reader's time:

- **Skip near-duplicates.** A week can produce 3–4 posts on the same
  narrow topic (e.g. the same person's X thread split across several
  captures) — pick the single best one, not all of them.
- **Skip pure announcements with nothing to say.** A one-line "X 2.0 is
  out" with a 20-word body rarely earns a blurb; a launch post with real
  reasoning behind it does.
- **Favor substance over hype.** A concrete technical teardown, a
  contrarian argument, or a real "I learned this" post beats generic
  AI-industry-news that everyone's newsletter will also cover this week.
- Aim for topic variety across the final list — not 10 LLM-release posts
  and nothing else, even if that's most of what got captured.

If the window had to expand past 7 days to reach 15, keep that in mind:
the newsletter's date range and framing should reflect what it actually
covers, not "the last week."

## 3. Read each shortlisted item, then write its blurb

Open the file at its `path`. Archivore's HTML→Markdown conversion often
leaves site-nav boilerplate at the top (breadcrumbs, header links, tag
lists) — skip past that to the actual content. Read enough to state the
real point, not just reword the title.

Write one blurb per item, 2–4 sentences, in first person as Todd,
covering **why it's worth reading** — the interesting claim, the
surprising detail, the practical takeaway — not a neutral restatement of
what the article is about. **REQUIRED SUB-SKILL:** run every blurb
through `economist-style` — clarity, precision, brevity, active voice.

**Voice note:** no tweet-derived voice profile exists yet. Until Todd
provides a Twitter/X data export (`tweets.js`) to build one, match tone
against his existing `content/posts/` and `content/til/` — direct, a
little dry, not marketing copy. If a voice-profile file later appears at
`skills/last-week-in-review/voice-notes.md`, read and apply it here too.

## 4. Assemble the post

Title: `Last Week in Review: <date range>` — using the actual span of
dates the picks cover (e.g. `Sep 12–19, 2026`), not a fixed phrase, since
the window can expand.

Opening: 2–3 sentences framing the week — a theme if one emerged, or just
a plain "here's what was worth reading" if not. If the lookback window
expanded, say so plainly (e.g. "a quiet week meant reaching back to
Sept 5 to fill this out") — don't silently pretend it was a normal week.

Each pick, in a single numbered list:

```markdown
1. **[Title](source-url)** — Blurb (2–4 sentences). [Discuss →](discussion-url)
```

Omit the `[Discuss →]` link when an item has no `discussion` URL, or when
`discussion` is identical to `source` — self-posts (Ask HN, Show HN text
posts) often have both fields pointing at the same HN thread, and a
second identical link is just noise. Order picks however reads best — chronological is fine;
grouping by theme is fine too if a natural grouping emerged in step 2.

## 5. Save as a draft

Write to the vault at:
```
~/Library/Mobile Documents/com~apple~CloudDocs/Todd's Obsidian Vault/1 Projects/taude.xyz Blog/newsletter/<Title>.md
```
(title used verbatim as the filename — this is its own vault folder,
separate from `ai-drafted/`, since it maps to the dedicated `newsletter`
section, not `posts`.)

Front matter:
```yaml
---
title: <Title>
date: <today, YYYY-MM-DD>
draft: true
tags:
  - ai-drafted
  - newsletter
---
```
`ai-drafted` is what triggers the site's "Drafted with Claude" disclosure
banner regardless of which section the post lives in — keep it even
though this isn't going into `posts/`. Write real values directly; this
note isn't created through Obsidian's template flow, so there's no
Templater syntax to worry about leaving unevaluated.

## 6. Build, review, and publish

1. `cd ~/dev/taude.xyz && ./scripts/publish.sh --preview "<commit message>"` —
   syncs the vault into `content/`, opens a local preview server so you
   can check the rendered post before anything ships.
2. Show the user the diff and the rendered picks; get their explicit
   go-ahead in chat before pushing — the script's own y/N prompt isn't a
   substitute for that.
3. Flip `draft: false` in the vault file once approved (edit the synced
   `content/newsletter/<Title>.md` too, or re-sync after editing the
   vault copy — either way both must agree before publish).
4. Push, then confirm the GitHub Actions deploy actually completed —
   see `publish-taude-blog` for the exact `gh run list` polling commands.
   Don't declare success on the push alone.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Picking items purely by recency, ignoring quality | Shortlist by substance (step 2) before opening any files |
| Reconstructing a filename from the title to open it | Use the `path` field from the JSON verbatim — archivore's filename sanitization doesn't round-trip cleanly from the title alone |
| Landing-page or marketing-site captures counted as substantive (high word count, no real content) | Word count isn't a quality signal by itself — read enough to check there's an actual argument, not just nav/marketing copy |
| `[Discuss →]` link duplicates the title link | Self-posts (Ask HN, Show HN text posts) have `source == discussion` — omit the second link when they're identical, not just when discussion is missing |
| Several near-duplicate items in the final 15 | Dedupe by topic — pick the best one per topic, not every one |
| Blurb just restates the title | State the actual interesting claim or takeaway instead |
| Skipping the economist-style pass | Always run every blurb through it before saving |
| Saving to `ai-drafted/` | This skill's own dedicated `newsletter/` vault folder — different section, different mapping |
| Dropping the `ai-drafted` tag because it's not going into `posts/` | Keep it — the AI-banner logic is tag-based, not section-based |
| Silently narrowing to 7 days when candidates run short | Expand the window (the script already does); reflect the real span in the title/opening |
| Declaring the newsletter "published" right after `git push` | Poll `gh run list` and confirm the deploy actually succeeded |
