---
title: Pick a Model That Works and Stop There
date: 2026-09-18
draft: false
tags:
  - ai-drafted
slug: "pick-a-model-that-works-and-stop-there"
---
*Prompted by an HN thread: [Qwen 3.8 Omni Flash](https://news.ycombinator.com/item?id=49747925)*

New AI models ship every week, and testing each one is not worth the time it takes. That is the real lesson in a Hacker News thread that started out about announcing Qwen 3.8 Omni Flash: pick a model that works, keep it, and switch only when it actually fails or the bill spikes.

## Most Comparison Shopping Is Optional

One commenter, Systemerror7A69, described a simple rule: pick a cheap model, such as GLM-5.3 Flash, and use it. Improve the prompt or the surrounding tooling before blaming the model. Switch only if it fails the task outright or the bill becomes a problem. Another commenter, epolanski, has run Gemini Flash 2.0 for summarisation and translation with no urge to upgrade: "this chase of the latest LLM is a bit pointless" once something works. A third, bmordue, gave the pattern a name: satisficing instead of optimising.

One reply added a sharper point: model vendors have reason to dislike this conclusion, since a market of users who stop upgrading once something works is a market that stops paying for the next release.

## When Comparison Actually Pays Off

Some tasks do call for testing candidates. The efficient version of that, per the thread, is narrow, not exhaustive:

- Run two or three real candidates on your actual task and compare cost and output directly, rather than reading marketing copy or a leaderboard. One commenter described doing exactly this with a simple loop over OpenRouter's API.
- OpenRouter's auto-router picks a model per prompt for cost, which works as a default when you have no strong preference.
- Sorting OpenRouter's catalogue by recent popularity, price, or context window turns other users' choices into a first filter, not a final answer.
- A pure price-comparison site (one commenter named costgoat.com) narrows the field before you touch a single API.

## The Real Cost Is Not the Sticker Price

Gemini charges $1.50 per million input tokens and $9 per million output tokens. Qwen 3.8 charges $0.15 and $0.47. Read as a per-token rate, that looks like a decisive win for Qwen. It is not decisive, because per-token price ignores how many tokens a model needs to finish the job. One commenter's example: Qwen 3.8 Max, priced under $6 per million output tokens, can cost more per completed task than Astra 6, priced at $50 per million, if Astra finishes in far fewer tokens.

Caching adds a second trap. One commenter described a single 80-million-token session on OVH costing $30, because OVH billed the cache misses at full price rather than the discounted rate it advertised. Before trusting a cheap headline rate, check how the provider actually bills a cache miss.

## Do Not Trust the Leaderboard Either

Benchmarks do not reliably predict performance on your workload, one commenter argued: "it's simply unknown ... unless you just try them." Another compared model selection to buying a car or a set of clothes — you read a little, then you try it on.

## The Upshot

A workable recipe for a market that will not stop shipping new models: default to a competent, cheap model and stay there until it fails your task or the bill spikes. When you do need to compare, test two or three real candidates on your actual work rather than trusting a benchmark or a per-token rate, and check what a completed task costs end to end, including cache billing, not just the headline number. Keeping up with rapid model releases stops being a burden once keeping up no longer means evaluating everything that ships.
