---
title: AI Made Doing More Cheap, Not Finishing Easier
date: 2026-10-30
draft: false
tags: ["ai-drafted", "ai-slop", "ai-lifestyle", "agents"]
slug: "ai-made-doing-more-cheap"
---
This one's ai-slop, as advertised on the [about page](/about/). The article
came out of archivore's capture feed, and an AI wrote the recap around it
in a short Claude Code session. So take the opinions below as a
summary of someone else's argument, not a report from my own week.

The source is Orestis Ioannou's
[AI Promised Less Work. I Have Never Worked More](https://oioannou.com/blog/ai-promised-less-work/),
which also had a [Hacker News thread](https://news.ycombinator.com/item?id=50257325).

## The argument

Ioannou is a VP of Technology who, on paper, should be writing less code
than ever. He pulled his GitHub contribution history back to 2019 and found
the opposite. His Principal Engineer years averaged 114 contributions a
month, against 173 as a full-stack engineer. In 2026 he's back at
full-stack pace, with August the busiest month on record at 427. The
median weekday went from 3 or 4 contributions to 7. Weekdays with no
activity fell from 40–46 a year to 18 so far.

His explanation isn't that the tools are slow or bad. He uses agents for
all his engineering work and likes them. The problem is that cheap
implementation removes the friction that used to stop him saying yes. Bugs
he'd have left alone, patterns worth cleaning up and half-formed ideas all
become "just a quick prompt". Agents didn't make his workload faster to
finish; they made it easy to give himself a much bigger one.

## Why it's tiring

He used to hold two or three serious tasks a week, one at a time. Now
several agents run in parallel, and each needs him only sometimes: a
question, a plan to approve, a diff to read. The cost is the context
switch each time, reloading a different problem, repository and set of
decisions. His summary is that capacity to implement ideas has grown much
faster than his capacity to think about them.

He also describes the pattern as bursts. A new model or workflow makes
something possible, he starts more agents and says yes to more experiments,
and a few weeks later reviewing catches up with him and he pulls back. He
counts three of these cycles since January. Even the "low" months now sit
above his old baseline.

## What I'd take from it

Two caveats before taking the data too far. Contribution counts mix
commits, reviews, pull requests and issues, so they're a rough measure of
activity, not of value. And it's one person's calendar. Ioannou says as
much.

Still, the diagnosis seems right to me, and it matches the
[AI Lifestyle](/tags/ai-lifestyle/) theme in my own reading queue. If the
bottleneck moves from writing code to deciding what's worth writing, then
the useful skill is declining work, and the tools do nothing to help with
that. Parallel agents are only as good as the attention available to review
them.

## Session stats

Pulled from the session transcript with `session_usage.py`. The first
version of this post used numbers captured before it was written, which
undercounted the session. These cover the whole session, including the
follow-up work (a newsletter, fact-checking its blurbs and this refresh):

- Assistant messages with usage data: 89
- Input tokens: 232
- Output tokens: 51,638
- Cache-creation tokens: 381,818
- Cache-read tokens: 6,451,559
- Total, all categories: 6,885,247
- Session span: Oct 30, 16:15 UTC to Nov 2, 02:43 UTC

The span is wall-clock time with the session left open between requests,
so it says little about active working time. Cache-read tokens bill far
cheaper than fresh input, so the 6.9 million total overstates the cost if
read as a plain sum. About 94 percent of it is cache reads.
