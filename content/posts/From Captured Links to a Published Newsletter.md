---
title: From Captured Links to a Published Newsletter
date: 2026-10-30
draft: false
tags:
  - ai-slop
  - archivore
  - automation
slug: "from-captured-links-to-a-published-newsletter"
---
This one's ai-slop too, as advertised on the [about page](/about/) — still
inside [the same long-running session](/how-archivore-turns-browsing-into-a-wiki/)
that built archivore in the first place. That post closed by noting
archivore's "second half" — turning weeks of captured reading into actual
published writing — was still on the roadmap. It isn't anymore, mostly.

## A newsletter that reads the vault for you

The new piece is a skill called `last-week-in-review`. It pulls every
article archivore captured in the last week (or further back, if a week
comes up short), filters out junk and marketing pages by actually reading
them rather than trusting word counts, picks the fifteen most worth a
reader's time, and writes a short blurb on each — in my voice, run through
an Economist style-guide pass for clarity and brevity. Two issues have gone
out so far, at [/newsletter/](/newsletter/).

One of those weeks produced an unplanned bonus: a Hacker News thread about
Bend, a language pitched for AI-assisted coding. The headline blog post the
thread was discussing claimed Bend's author had never heard of formal
verification. Reading the actual thread, not just the blog post it was
about, turned up Bend's own creator in the comments, pointing to a
formal-verification language he'd built back in 2018. The post that got
published covered that correction instead of the original premise, because
the thread's real finding mattered more than the headline it was arguing
with.

## Who actually runs this, and when

A newsletter that reads a shared vault raises an obvious question: on a
setup running archivore on more than one machine, who generates it, and how
often? The answer became a weekly pipeline. One designated machine runs
archivore's own catch-up capture, files everything new into a personal wiki
(a separate skill, `taude`, that classifies each article against a growing
topic list and weaves it into synthesized prose — 24 topics and counting),
generates the week's newsletter, auto-publishes it, and emails a combined
report of all three. Every other machine stays a plain capture satellite: it
only scans its own browser history and feeds the same shared vault,
deliberately kept out of the wiki-ingest and publishing steps so the same
article never gets filed twice, or the same newsletter published twice.

<pre class="mermaid">
flowchart TD
  A[archivore run] --> B[taude ingest]
  B --> C[last-week-in-review]
  C -->|auto-publish| D[taude.xyz/newsletter]
  A --> E[combined report email]
  B --> E
  C --> E
</pre>

It's built and documented, not yet switched on. The two headless steps run
Claude with `--dangerously-skip-permissions` — there's no one at a keyboard
at 7am on a Monday to approve tool calls — and that's a real enough bypass
of Claude Code's own safety check that I'd rather watch its first real run
myself than trust it unattended on the first try. Three things are still
manual on purpose: making the script executable, adding SMTP credentials by
hand rather than ever pasting them into chat, and running the whole thing
once for real before the schedule does.

## Session stats

This is the same session as the first archivore post — it's now run from
July 1st to October 30th, 2026, four months on and off, still one
continuous conversation. Across 2,611 assistant turns it used 5,060 fresh
input tokens, 2,221,383 output tokens, 33,413,000 cache-creation tokens, and
969,049,295 cache-read tokens: just over a billion tokens total. As before,
that last figure overstates cost read as a flat sum — cache reads bill at a
fraction of fresh input, and nearly all of this total is Claude re-reading
context it had already built, not new work.
