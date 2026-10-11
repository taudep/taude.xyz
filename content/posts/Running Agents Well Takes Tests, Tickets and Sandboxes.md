---
title: Running Agents Well Takes Tests, Tickets and Sandboxes
date: 2026-10-11
draft: false
tags:
  - ai-drafted
slug: "running-agents-well-takes-tests-tickets-and-sandboxes"
---
*Prompted by an HN thread: [Docker Agent](https://news.ycombinator.com/item?id=49996259)*

Docker Agent, a YAML-driven runtime for teams of AI agents, drew 304 points and 145 comments on Hacker News, most of them sceptical. Commenters doubted that another orchestration framework was needed. Their better point was that wiring agents together is the easy part. Keeping them coherent over long runs, proving their work is finished, coordinating several at once and limiting the damage they can do are harder, and the thread offered a technique for each.

## What Docker Agent Is

It reads an agent definition from YAML: a model, instructions and a list of tools. Tools can be built in or come from any MCP server, and a root agent can delegate to specialists. It supports OpenAI, Anthropic, Gemini, Bedrock, Mistral, xAI and local models, offers retrieval (BM25, embeddings, reranking) and shares agents through OCI registries, as container images are shared. It runs as a `docker agent` subcommand or as a standalone binary. Its maintainer said it began as "compose for agents" (the original name was cagent) and that YAML can be swapped for HCL or Go code.

The reception was cool. Commenters asked what it has to do with Docker, compared the glut of agent harnesses with the JavaScript framework churn of the 2010s, and groaned at more YAML. One user found sessions broke repeatedly when Docker Agent drove Codex through its harness integration: output over 10,000 characters killed the session. The maintainers replied that the integration is an uncommon use case and pointed to the ACP route.

## Four Problems That Matter More Than Orchestration

| Problem | Technique from the thread |
|---|---|
| Drift over long runs | Give agents written standing rules and a shared, durable record of work. `Olscore`, who wrote Pullboard, uses a forum-like board where agents post progress under a developer-written doctrine and a checkable specification. |
| Knowing the work is done | Define work as executable specifications. `smashed` writes a pytest suite first, resists natural-language todo lists, and runs the specs against the built binary. |
| Running many agents | Chat handles concurrency badly. `pea` argued for asynchronous, Jira-style task tracking, which also solves the multi-person case that chat does not. Podium and Epiq take the same approach with Linear-style and git-synced trackers. |
| Limiting damage | Run harnesses in sandboxes and keep real credentials out of reach. Docker's `sbx` CLI, praised by `genghisjahn`, gives the model a sentinel value; outbound calls are looked up and the real secret is substituted on the way out. |

## Smaller Techniques Worth Stealing

- **Pair implementers with reviewers.** `mgw` (Podium) tells the system in plain English that every Codex implementer gets an OpenCode reviewer, and that a finished subtree gets a final review from a stronger model. The system then enforces the rule. Their reason for avoiding a configuration UI: any interface for prescribing how agents coordinate felt too clunky.
- **Gate shipping on a second agent.** In Pullboard, nothing merges until another agent verifies it. When the README badge showed a failing gate, the author explained that one agent fixes, another verifies, then the change merges.
- **Route, don't chain.** `magnusokik` found that tracking many concurrently invoking agents is exhausting, and keeps a single orchestration agent that routes work by capability.
- **Snapshot every step.** `verdverm`'s harness runs in a Dagger environment where each tool call and file change creates a new container layer, giving session time travel and forking.
- **Ask for permissions at run time.** `tonymet` wants sudo-style ACLs for commands and credentials, scoped by OAuth scope, so an agent starts with tight limits and requests more when it needs them.
- **Keep the thinking.** `ogou` uses Backlog.md, where finished tasks record the reasoning and experiment results that git history does not capture.
- **Give agents an existing CLI.** `Zambyte` found Atlassian's `jira-cli` made Jira pleasant for AI tooling to drive. `alemanek` used a session-start hook to prune most of the skills an Atlassian tool loaded.
- **Manage network access centrally.** `sbx` supports global and per-sandbox network allow-lists, which spares hand-edited YAML for each sandbox.

## The Jira Irony

Several builders noted that developers who hate Jira are now building Jira for agents. The consensus was that people hate their company's configuration of it, or its slow interface, rather than issue tracking itself. One commenter said that simpler trackers would keep tickets truer to reality. Another asked whether anyone would really use Jira for agents; the reply was that nobody would, because an agent can build a tracker in ten minutes. One comment summed up the mood: you either die a software engineer or live long enough to become the project manager.

## Cautions

- **Data handling.** One commenter warned that Docker now collects inputs and outputs. Check retention terms before routing prompts through any vendor runtime.
- **Sandbox claims.** Two commenters could find nothing about attack vectors in Docker's sandbox documentation. Docker Agent's sandbox mode runs in a Docker sandbox, which is a VM; without it, it presumably runs in a container.
- **Differentiation.** Commenters asked how it differs from hosted sandboxes such as modal.com, e2b and Cloudflare's, and why one cannot choose the harness. The thread produced no clear answer.
- **Is it needed at all?** `ravenstine` argued that an agent working inside a Linux VM can work out container orchestration unaided, which makes much of the documentation obsolete. `woah` asked why "no code required" is a selling point when agents write code on demand.
- **Unanswered.** `gerwim` asked how agents find the right posts on a forum-style board, and how drift or changing specifications are handled. The thread did not say.

## The Upshot

Treat the framework as the least important choice. Write the rules agents must follow and make them log their work. Make passing tests the definition of done, and have a second agent, ideally from a different model, verify before anything ships. Track tasks asynchronously, as one would for human colleagues. Run everything in a sandbox where the agent never sees a real secret. A YAML file that wires agents together matters only after those are in place.
