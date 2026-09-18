---
title: AI Removed the Cost of Asking, Not the Cost of Answering
date: 2026-09-18
draft: true
tags:
  - ai-drafted
slug: "ai-removed-the-cost-of-asking-not-the-cost-of-answering"
---
*Prompted by an HN thread: [Don't be a meat proxy](https://news.ycombinator.com/item?id=49151933)*

One engineer's complaint: colleagues, including seniors responsible for the code in question, hand him 300-line Claude explanations and ask him to check whether they're right, because they don't understand the explanations themselves. That is the "meat proxy" problem, named for [the blog post](https://gruhn.me/blog/2026-08-03/) that started a 741-comment Hacker News thread: a person relaying an AI's output without doing the work of understanding it first. The more useful finding, once the thread settles, is why this keeps happening. It isn't laziness so much as a broken cost structure. AI made asking free. It didn't make answering free, and somebody still has to pay.

## What a meat proxy looks like

The pattern shows up at two scales. At small scale, a colleague pastes a Claude response into a chat instead of just asking the question directly. At large scale, one commenter described a person "spearheading AI across the enterprise" who generated thousands of lines of AI-written documentation, then required hundreds of product owners and business analysts to review it for correctness — work that didn't exist before the documentation did.

In both cases the generating step got cheaper and the verifying step didn't. That gap is where the thread's complaints live.

## Two theories for why

Commenters split on the cause. One camp reads it as psychological: constant validation from an AI ("you're absolutely right!") is more comfortable than the friction of asking a person, so people route around colleagues even when it's slower for everyone else. A commenter with customer-support experience made the same point about helplines generally: easy access to an answer erodes the habit of working through a problem first, and awareness of that tendency is most of the fix.

The other camp reads it as skill stratification, not psychology. On this account, AI mainly helps two groups: people already skilled enough to know when to trust it and when to check it, and people who were struggling anyway and now have a floor under them. Everyone in between — competent enough to take pride in the work, not skilled enough to audit AI output quickly — is most likely to lean on it without verifying, and most likely to resent being asked to.

## The actual mechanism: broken back-pressure

Underneath both theories is a simpler explanation, and it's the thread's sharpest point. Asking a question used to cost the asker something: time spent framing it, and a small social debt for making someone else stop and help. That cost was a back-pressure mechanism — it kept casual, half-formed questions from reaching other people's inboxes. AI removed the cost of generating a question, an answer, or 300 lines of documentation. It didn't remove the cost of *verifying* that output; it just moved that cost to whoever receives it. As one commenter put it, it now takes someone a minute to take an hour of somebody else's life, with no mechanism pushing back.

Two commenters independently reached for the same comparison: using AI to feel more productive is like using amphetamines to feel more productive. The number of things produced rises. Whether the value produced rises too is a separate question — and confidence on that point seems to track dosage more than evidence.

## The defense, and where it holds

AI-as-intermediary isn't always indefensible. One commenter pushed back directly on the documentation example: if a subject-matter expert prompts the AI once, reviews the output carefully, and publishes it, that's better than dozens of people independently asking their own questions and getting unreviewed answers each time. The distinction that matters isn't whether AI touched the output — it's whether anyone with real expertise checked it before it reached other people. A different commenter made a narrower version of the same point about debugging: an AI that catches and diagnoses an issue faster than he could even read the stack trace is a legitimate use of the tool, distinct from forwarding unread output.

The failure mode in the original complaints isn't AI use. It's AI use with the verification step skipped and handed to someone else.

## The one countermeasure that actually restores the cost

Most of the thread's advice is exhortation: pay attention, don't get lazy, be self-aware. One commenter described something more concrete. When asked to review raw, unread AI output, he runs it through an AI himself before responding — if the sender isn't going to read the output either way, there's no reason he should spend more effort than they did. He said explicitly that he doesn't recommend this as a team norm; it's retaliation, not a fix. But it does something the exhortations don't: it puts the missing back-pressure right back where it was removed, on the person who skipped the verification step in the first place.

## The upshot

The friction that AI removed — the cost of asking, drafting, or generating — was never pure waste. It did real work: keeping the volume of unverified output roughly matched to someone's willingness to check it. Fix that mismatch and the psychology and skill-stratification arguments mostly become moot. The fastest way to do it isn't a policy memo. It's making sure whoever generates the output can still explain it.
