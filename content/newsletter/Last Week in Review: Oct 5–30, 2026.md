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

1. **[AI promised less work. I've never worked more](https://oioannou.com/blog/ai-promised-less-work/)** — A VP of Technology charts his GitHub history and finds he is as busy as when coding was his whole job. August 2026 was his busiest month on record, with 427 contributions. His explanation: cheap implementation removes the friction that used to stop him saying yes. [Discuss →](https://news.ycombinator.com/item?id=50257325)

2. **[Cisco gives engineer unlimited AI tokens to rewrite 98% of the company's code](https://www.tomshardware.com/tech-industry/big-tech/cisco-gives-27-year-old-engineer-unlimited-ai-tokens-to-rewrite-98-percent-of-the-companys-legacy-code-in-24-months-president-plucks-former-startup-founder-telling-him-to-go-nuts)** — Cisco's president, Jeetu Patel, gave a 27-year-old ex-startup founder, hired through an acquisition and previously stuck in a role five levels down, unlimited tokens and 24 months to refactor 98% of the company's legacy code. A four-week proof of concept comes first. The skeptic's case, from a reader comment: testing and fixing regressions across thousands of products would outlast the two years. [Discuss →](https://news.ycombinator.com/item?id=50304122)

3. **[Anthropic Cracking Down on Video Game Rewrites](https://twitter.com/chasmmmmmmmmmmm/status/2116062991686721968)** — A widely shared X post says Claude Code picked up a server-side rule around Oct 27 against recreating specific existing games, with no setting to turn it off. Nobody in the Hacker News thread confirms it from a primary source. One commenter reports "recreate it in Rust" refused while "rewrite it in Rust" went ahead, which suggests prompt guidance sensitive to wording, not a hard block. [Discuss →](https://news.ycombinator.com/item?id=50304358)

4. **[Codex Desktop continuously generates Crashpad pending dumps](https://github.com/openai/codex/issues/25921)** — One user's Crashpad directory grew to 4.9 GB and 54,504 files in a day. The app kept working; it just never stopped writing dumps. A good reminder to check what your agent tools leave on disk. [Discuss →](https://news.ycombinator.com/item?id=50133231)

5. **[Meta and Microsoft take steps to reduce employee usage of Claude AI](https://www.rswebsols.com/news/meta-and-microsoft-take-steps-to-reduce-employee-usage-of-claude-ai/)** — Citing The Information, the report says both companies are steering staff to their own coding tools. Customer access to Claude through Microsoft's products is reportedly unaffected. Neither company is quoted, and the thread's explanations (dogfooding, token costs, security) are speculation. [Discuss →](https://news.ycombinator.com/item?id=49997161)

6. **[OpenAI annualised revenues $20B less than previously signalled](https://www.cnbc.com/2026/10/08/open-ai-revenue-nvidia-oracle-coreweave.html)** — OpenAI told investors about $50 billion in annualized revenue at the end of September, against the $68 billion widely reported a month earlier. The pressure is the $852 billion valuation and a likely 2027 IPO. The same piece notes one analyst called Anthropic's coming offering "the most ridiculous IPO of 2026". [Discuss →](https://news.ycombinator.com/item?id=50008187)

7. **[Character.ai has initiated voluntary Chapter 11 bankruptcy](https://blog.character.ai/an-update-on-character-ai/)** — The company is seeking a court-supervised sale. If no bid arrives, it will wind the platform down. The service stays up for now. [Discuss →](https://news.ycombinator.com/item?id=50068036)

8. **[Cloudflare acquires Deno](https://deno.com/blog/cloudflare)** — Deno's founder frames the deal as finishing what Deno Deploy started: compute, storage and communication working together without each app assembling its own infrastructure. Worth reading for what he says Deploy taught the team about the complexity underneath. [Discuss →](https://news.ycombinator.com/item?id=50019911)

9. **[Our $445M Series D](https://oxide.computer/blog/our-445m-series-d)** — Oxide paid income tax this spring, which almost no startup does, and has an order backlog larger than its cash can fill. The post explains why a profitable hardware company still needs a huge raise. [Discuss →](https://news.ycombinator.com/item?id=50020014)

10. **[What ArtCraft's Vibe-Coded Apps Say About Adobe](https://tedium.co/2026/10/08/artcraft-vibe-coding-creative-cloud-remake/)** — Ernie Smith uses a project that rebuilds Creative Cloud tools with AI to ask what happens when a company ignores its power users. The Adobe grievances are familiar, but the argument that AI lowers the cost of building a replacement is the interesting part. [Discuss →](https://news.ycombinator.com/item?id=50010170)

11. **[The Deeply Impersonal Personalized Recruiter Mail](https://blog.pentlander.com/the-deeply-impersonal-personalized-recruiter-mail/)** — Recruiters now open with an LLM paragraph summarizing your career back to you, then paste a job description that has little to do with it. Short and funny, and accurate about how personalization fails. [Discuss →](https://news.ycombinator.com/item?id=50008685)

12. **[Don't Put Tilde In Your Path](https://disconnect3d.pl//2026/10/02/dont-put-tilde-in-your-path/)** — `export PATH="$PATH:~/.local/bin/"` does not expand the tilde, because expansion happens only in unquoted words. You end up with a literal `./~/.local/bin` on your PATH. Use `$HOME` instead. [Discuss →](https://news.ycombinator.com/item?id=50042425)

13. **[How to engineer an AI harness for game development](https://kylekukshtel.com/ai-harness-engineering-game-development-claude-code)** — Kyle Kukshtel turns a conference talk into a post on making a game legible to AI agents so iteration is faster. He covers everyday development, not one-shot demos, and wrote it entirely by hand. [Discuss →](https://news.ycombinator.com/item?id=50072120)

14. **[Solar surpasses nuclear power globally for first time](https://www.pv-magazine.com/2026/09/29/solar-surpasses-nuclear-power-globally-for-first-time/)** — Per WNISR 2026, solar generation overtook nuclear in 2025. The report points to nuclear's slow growth, long build times and limited small modular reactor deployment. [Discuss →](https://news.ycombinator.com/item?id=50131256)

15. **[Everybody's home. No one's coming over](https://www.derekthompson.org/p/the-death-of-the-american-host)** — The share of adults who regularly have friends over has fallen 70 percent since 1975. Derek Thompson argues the decline in hosting is steeper than the much-lamented drop in church attendance. [Discuss →](https://news.ycombinator.com/item?id=49891295)
