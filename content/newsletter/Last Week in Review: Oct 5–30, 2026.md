---
title: "Last Week in Review: Oct 5–30, 2026"
date: 2026-10-30
draft: false
tags:
  - ai-drafted
  - newsletter
slug: "last-week-in-review-oct-5-30-2026"
---
A quiet capture stretch meant reaching back to early October to fill this out, so this issue covers four weeks, not one. The theme that kept surfacing: AI makes building cheap, and everyone from solo engineers to Cisco and Anthropic is working out what that does to the rest of the job.

1. **[AI promised less work. I've never worked more](https://oioannou.com/blog/ai-promised-less-work/)** — Orestis Ioannou leads engineering and should be writing less code than ever. Their GitHub history says otherwise: August 2026 was the busiest month since 2019, at 427 contributions. The diagnosis rings true. Cheap implementation removes the friction that used to stop a yes, and review and context switching become the new bottleneck. [Discuss →](https://news.ycombinator.com/item?id=50257325)

2. **[Cisco gives engineer unlimited AI tokens to rewrite 98% of the company's code](https://www.tomshardware.com/tech-industry/big-tech/cisco-gives-27-year-old-engineer-unlimited-ai-tokens-to-rewrite-98-percent-of-the-companys-legacy-code-in-24-months-president-plucks-former-startup-founder-telling-him-to-go-nuts)** — The token budget is the hook. The more interesting part is the argument from Cisco's president, Jeetu Patel, for hiring early-career people while AI cuts entry-level jobs: "If you don't hire the early-in-career [workers]... where do fresh ideas get injected?" A 27-year-old ex-founder, previously buried five levels down after an acquisition, now has 24 months to refactor 98% of the legacy code. A reader comment on the article makes the skeptic's case: testing thousands of products would outlast the deadline. Originally reported by [Fortune](https://fortune.com/2026/10/30/cisco-president-jeetu-patel-gen-z-27-year-old-unlimited-ai-tokens-rewrite-legacy-code-entry-level-jobs/). [Discuss →](https://news.ycombinator.com/item?id=50304122)

3. **[Anthropic Cracking Down on Video Game Rewrites](https://twitter.com/chasmmmmmmmmmmm/status/2116062991686721968)** — A widely shared X post says Claude Code picked up a server-side rule around Oct 27 against recreating specific existing games. Nobody in the Hacker News thread confirms it from a primary source, though one commenter found the wording matters: "recreate it in Rust" was refused, "rewrite it in Rust" went ahead. Read the thread for what's at stake if it's real: the retro preservation community, whose decomps, ports and fan translations have leaned heavily on LLM help. [Discuss →](https://news.ycombinator.com/item?id=50304358)

4. **[Codex Desktop continuously generates Crashpad pending dumps](https://github.com/openai/codex/issues/25921)** — One user's Crashpad directory grew to 4.9 GB and 54,504 files in a day. The app kept working; it just never stopped writing dumps. A good reminder to check what your agent tools leave on disk. [Discuss →](https://news.ycombinator.com/item?id=50133231)

5. **[OpenAI annualised revenues $20B less than previously signalled](https://www.cnbc.com/2026/10/08/open-ai-revenue-nvidia-oracle-coreweave.html)** — OpenAI told investors about $50 billion in annualized revenue at the end of September, against the $68 billion widely reported a month earlier. The pressure is the $852 billion valuation and a likely 2027 IPO. The same piece notes one analyst called Anthropic's coming offering the "most ridiculous IPO of 2026". [Discuss →](https://news.ycombinator.com/item?id=50008187)

6. **[Character.ai has initiated voluntary Chapter 11 bankruptcy](https://blog.character.ai/an-update-on-character-ai/)** — The post cites "legal, regulatory, and operational headwinds" and says the platform will be wound down if no buyer appears. Worth reading if you build on a single AI vendor: the user-facing promise is that everything stays up for now, and nothing more. [Discuss →](https://news.ycombinator.com/item?id=50068036)

7. **[Cloudflare acquires Deno](https://deno.com/blog/cloudflare)** — Deno's founder, Ryan Dahl, frames the deal as finishing what Deno Deploy started: compute, storage and communication working together without each app assembling its own infrastructure. The candid part is the admission that running Deploy exposed how much complexity sat under its simple developer experience. [Discuss →](https://news.ycombinator.com/item?id=50019911)

8. **[Our $445M Series D](https://oxide.computer/blog/our-445m-series-d)** — Oxide paid income tax this spring, which almost no startup does, and has an order backlog larger than its cash can fill. The post explains why a profitable hardware company still needs a huge raise. [Discuss →](https://news.ycombinator.com/item?id=50020014)

9. **[What ArtCraft's Vibe-Coded Apps Say About Adobe](https://tedium.co/2026/10/08/artcraft-vibe-coding-creative-cloud-remake/)** — Ernie Smith uses a project that rebuilds Creative Cloud tools with AI to ask what happens when a company ignores its power users. The Adobe grievances are familiar, but the argument that AI lowers the cost of building a replacement is the interesting part. [Discuss →](https://news.ycombinator.com/item?id=50010170)

10. **[The Deeply Impersonal Personalized Recruiter Mail](https://blog.pentlander.com/the-deeply-impersonal-personalized-recruiter-mail/)** — Recruiters now open with an LLM paragraph summarizing your career back to you, then paste a job description that has little to do with it. Short and funny, and accurate about how personalization fails. [Discuss →](https://news.ycombinator.com/item?id=50008685)

11. **[Don't Put Tilde In Your Path](https://disconnect3d.pl//2026/10/02/dont-put-tilde-in-your-path/)** — `export PATH="$PATH:~/.local/bin/"` does not expand the tilde, because expansion happens only in unquoted words. You end up with a literal `./~/.local/bin` on your PATH. Use `$HOME` instead. [Discuss →](https://news.ycombinator.com/item?id=50042425)

12. **[How to engineer an AI harness for game development](https://kylekukshtel.com/ai-harness-engineering-game-development-claude-code)** — Kyle Kukshtel turns a conference talk into a practical guide to making a game legible to AI agents so iteration gets faster. It covers eight-hours-a-day development, not one-shot demos. Written entirely by hand, as the post notes. [Discuss →](https://news.ycombinator.com/item?id=50072120)

13. **[Solar surpasses nuclear power globally for first time](https://www.pv-magazine.com/2026/09/29/solar-surpasses-nuclear-power-globally-for-first-time/)** — Per WNISR 2026, solar generation overtook nuclear in 2025. The useful context is why: small modular reactors, the usual answer to nuclear's long build times, have barely been deployed, while solar and batteries keep scaling. [Discuss →](https://news.ycombinator.com/item?id=50131256)

14. **[Everybody's home. No one's coming over](https://www.derekthompson.org/p/the-death-of-the-american-host)** — The share of adults who regularly have friends over has fallen 70 percent since 1975. Derek Thompson argues the decline in hosting is steeper than the much-lamented drop in church attendance. [Discuss →](https://news.ycombinator.com/item?id=49891295)
