---
title: taude, the command centre for too much work
date: 2026-11-11T09:55:00-05:00
draft: false
tags:
  - ai-drafted
  - ai-slop
  - claude-code
  - agents
  - obsidian
slug: taude-bot-a-quiet-command-centre-for-too-many-agents
---
This one's ai-slop, as advertised on the [about page](/about/).

My work laptop has about 35 CMUX workspaces open. Each one is an agent session,
a worktree, or a half-finished thought. I had stopped knowing which ones had
uncommitted changes, which had PRs waiting, and which the agent considered
finished. My browser was worse: a hundred tabs, each one a task I meant to do
or an article I meant to read, none of them findable.

There is now a [product page for taude-bot](/product/) listing every feature.

So I sat down with Claude to design the thing I wanted instead. It is called
Taude (it rhymes with Claude, duh). The brief was one word
long: quiet. It should keep track of everything without a lot of fanfare.

## The ten main ideas

1. **Mission control for AI coding sessions.** One screen shows every Claude
   Code, pi and opencode session for each laptops: what each built, uncommitted
   changes, PRs waiting to merge, and what the agent thinks is still left to
   do.
2. **Close anything, reopen it later.** Every session writes a short wrap-up
   when it ends. One keypress reopens it in the right coding workspace with the
   agent's memory intact.
3. **Tab bankruptcy, automated.** Daily and at Friday shutdown it sweeps
   Chrome and Firefox tabs into lists. Jira tickets and Confluence pages I was
   editing become TODOs; pages I was only reading become follow-ups; Hacker News
   becomes reading (article and comments paired); YouTube goes to watch. Then it
   closes everything except pinned tabs, with a one-key "reopen all". No tabs
   survive the weekend.
4. **A homemade browser extension.** `⌥M` on any page sends it to my personal
   LLM wiki, with an optional note on why it caught my eye.
5. **Agent workflows on a schedule.** Daily shutdown, weekly shutdown, writing
   the newsletter, processing my reading archive into wiki pages: all run in the
   background. Anything public waits in a review pile for approval.
6. **It suggests content.** It notices what I shipped and offers to draft the
   blog post, newsletter or LinkedIn post, using what
   [archivore](/posts/how-archivore-turns-browsing-into-a-wiki/) captured.
7. **Plain markdown in Obsidian.** Plans, session logs, task lists and a
   handbook live in the vault, synced by iCloud. Each machine writes only its
   own files, so nothing ever conflicts.
8. **Keyboard everything.** Number keys switch apps (Work, Handbook, Tasks,
   Mngr, Inbox), `[` and `]` flip sub-tabs, `j`/`k` move, `/` searches
   everything. Dark, dense and fast; [Orca](https://www.onorca.dev/) was the
   visual inspiration.
9. **Fast, native, local.** A Go backend in a lightweight Wails window, which
   runs on Mac, Windows and Linux. A SQLite database per machine. Nothing in the
   cloud.
10. **Plug in any tool.** One ticket view over whichever tracker each machine
    uses (Jira at work, Linear at home). One self-documenting YAML config with
    shared and per-machine sections. One install script, one GitHub repo.

## What the mockups look like

Claude built these as throwaway HTML files with working hotkeys and fake data.
The data is invented and the employer details are scrubbed.

The Work app. Sessions on both laptops on the left, the selected session's
wrap-up on the right:

![taude-bot Work app mockup](/posts/taude-bot-work.png)

The Inbox app, where triaged tabs land. Select a batch with the space bar and
send it to Obsidian, mark it done, or drop it:

![taude-bot Inbox app mockup](/posts/taude-bot-inbox.png)

The browser extension and the notifications. One quiet banner on Friday
afternoon, no sounds, no modal windows:

![taude-bot browser extension and notification mockups](/posts/taude-bot-extension.png)

And what actually lands in the vault: one commented YAML config, one markdown
file per triage run, one per session:

![taude-bot vault files mockup](/posts/taude-bot-vault.png)

## How it fits together

Reduced to its essentials: every source of mess reports into a small local
service on each machine. Each service writes its own files into the vault,
iCloud carries them to the other laptop, and each window reads both.

<pre class="mermaid">
flowchart TD
  E[browser extension] --> S[local Go service]
  H[agent session hooks] --> S
  G[git, gh, CMUX] --> S
  S --> DB[(SQLite, per machine)]
  S --> V[TAUDE folder in the vault]
  V <--> O[other laptop]
  DB --> W[Wails window]
</pre>

## Decisions worth noting

A few came out of the conversation rather than the brief:

- **SQLite stays out of iCloud.** I wanted SQLite for persistence. Claude
  pointed out that syncing a live database file through iCloud invites
  corruption, so each machine keeps its own database locally and the markdown
  in the vault is what travels between machines.
- **An extension, because the alternatives cannot close tabs safely.**
  Archivore reads Chrome tabs through AppleScript, which cannot see pinned
  tabs, and Firefox's session file is read-only. "Close everything except
  pinned" needed a real extension.
- **The daily sweep has two modes.** `log` records tabs; `wipe` records and
  closes them. It starts on `log` until I trust it.
- **Phase 1 is the boring part.** Tab triage, the extension and a skeleton
  service come first. Session tracking, the full dashboard, workflows and
  ticket systems each get their own design pass later.

## Session stats

The session ran on November 11th, 2026, from 11:02 to 15:06 UTC, a little over
four hours. Across 106 assistant turns it used 340 fresh input tokens, 181,366
output tokens, 299,818 cache-creation tokens and 8,696,262 cache-read tokens,
about 9.2 million in all. That total overstates the cost: cache reads are
billed at a fraction of fresh input, and most of them are Claude re-reading
context it had already built up. The figures come from parsing Claude Code's
transcript format, which is not a stable public API, so treat them as
best-effort.
