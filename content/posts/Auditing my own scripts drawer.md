---
title: Auditing my own scripts drawer
date: 2026-09-03T17:53:00-04:00
draft: true
tags:
  - ai-drafted
  - ai-slop
  - claude-code
  - tooling
slug: auditing-my-own-scripts-drawer
---
Every developer has a `~/dev/tools/scripts` folder. Mine has run for years
without an index. I asked Claude Code to read every file in it and write
one.

The brief was simple: read the whole directory, then produce an `INDEX.md`
with three columns — tool, how to run it, what it does. 

It scanned roughly 40 files: Python CLIs built on `uv`, shell wrappers, one-off
Snowflake key-rotation scripts, a tmux session launcher, a Hacker News
summarizer. Some had docstrings. Several had none, and their purpose was
recoverable only by reading the `argparse` block or the hardcoded constants
at the top.

The audit paid for itself twice over. It caught two problems I'd have kept
carrying otherwise:

**A script that has been broken for a while.** `disc_admin_checks.py`
references a variable, `message`, before it's ever assigned, and calls a
function that reads `formatted_sebs` and `totalSEBs` without defining
either. Run it and it raises `NameError`, every time. It's a near-duplicate
of a working script, `domain_sebs.py`, so I'd stopped noticing it. Worse:
it has a live Slack webhook URL hardcoded in the source. That's now on my
list to delete or rotate.

**A script with placeholder values I'd forgotten to fill in.**
`set_snowflake_user_public_key.py` still lists its target accounts as
`account1`, `account2`, `account3` — scaffolding I never finished. Harmless
until the day I run it assuming it's real.

Neither bug was subtle. Both were invisible until something forced a
close read of code I hadn't opened in months. That's the actual value
here: not the table, but the excuse to look.

The index itself is now grouped by what the tools are for — Claude Code
workflow helpers, DISC infrastructure reporting, Snowflake key management —
with a separate section for stubs and known-broken scripts, so the next
person (probably me, in six months) sees the warnings before running
anything.

## What's in the drawer

For anyone curious what four years of "I'll just script this" produces,
here's the full list. Names of internal tools, accounts, and endpoints
are omitted or generalised — this is the shape of the collection, not a
runbook.

| Script | What it does |
|---|---|
| `claude-sessions.py` | Lists resumable Claude Code sessions with a ready-to-paste resume command |
| `which-session` | Finds past Claude Code / Copilot sessions run from a given directory |
| `install-claude-skill` | Installs a Claude skill from a GitHub folder URL into the local skills directory |
| `aitx.py` | TUI browser/installer for an internal AI tool exchange |
| `jira_history.py` | Ranks JIRA tickets visited in browser history, enriched via the JIRA CLI |
| `dev-session.sh` | Spins up a tmux session with preset windows for a project |
| `dev-worktree.sh` / `dev-rm-worktree.sh` | Creates and tears down git worktrees, with an `fzf` repo picker |
| `delete-gone-branches.sh` | Deletes local branches whose remote has disappeared |
| `git-pull-all.sh` | Fetches and pulls every repo under a parent directory, in parallel |
| `hn-summary.sh` | Summarizes a Hacker News thread's comments via an LLM |
| `disc-postgres-azure-flexpg.py` | Reports CPU/memory/storage/connection metrics for a set of prod Postgres instances |
| `disc-postgres-pgo-connections.py` | Reports connection utilization across a set of prod Postgres clusters |
| `bits_parse_tenants.sh` | One-line `jq`/`column` filter that formats tenant build data as a table |
| `stacks.py` | Prints a static reference table of internal environment/region codes |
| `etl_jobs.py` / `etl-jobs` | Reads ETL job config files from a data-platform repo and prints selected fields |
| `prm` | Fuzzy-search browser for an internal data model catalog (symlinked from another repo) |
| `domain_sebs.py` / `sebs` | Walks a config repo and tallies event-bus definitions per domain |
| `disc_admin_checks.py` | **Broken** — near-duplicate of `domain_sebs.py`, raises `NameError` on run |
| `make_snowflake_key_pair.sh` | Generates RSA key pairs per environment and prints the matching SQL |
| `create_rsa_keys.py` | Python equivalent of the above, plus a YAML summary of generated keys |
| `set_snowflake_user_public_key.py` | Sets a user's public key across a list of accounts — **placeholder values, unfinished** |
| `upload_keys.py` | Uploads a generated private key to a secrets manager, with a confirmation prompt per secret |
| `test_snowflake_connection_with_rsa_key.py` | Smoke test: connects with a key file and runs a version check |
| `data-mesh-sf.py` | Stub — renders a "Hello, World" template and does nothing else |
| `publish-gist.sh` | Empty file — a placeholder that was never written |

## Session stats

Real numbers from this session's transcript, not estimates:

- **21** assistant turns carried usage data
- **22,428** output tokens generated
- **155,639** tokens written to cache
- **1,159,344** tokens read from cache
- **42** tokens of fresh, uncached input
- **42 minutes**, start to finish

Cache-read tokens are billed at a fraction of the rate of fresh input, so
summing all four categories into "1.3m tokens" overstates the cost by a
wide margin — most of that figure is cheap re-reads of context already
paid for earlier in the session, not new work.
