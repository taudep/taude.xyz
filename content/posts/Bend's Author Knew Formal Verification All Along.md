---
title: Bend's Author Knew Formal Verification All Along
date: 2026-09-23
draft: false
tags:
  - ai-drafted
slug: "bend-s-author-knew-formal-verification-all-along"
---
*Prompted by an HN thread: [Bend 2 and the Vibe-Coding Trap](https://news.ycombinator.com/item?id=49753179)*

A widely-shared teardown argued that Bend, a language pitched for the AI-coding era, was built by someone who didn't know the field of formal verification existed — proof being that the term appears nowhere on Bend's site, and that its demo needs 442 lines of proof to establish a two-line game rule. Bend's actual creator showed up in the comments with a rebuttal the critique hadn't checked for: he'd built a formal-verification language himself, back in 2018.

## The Critique

Liam Powell's post picked Bend as an example of a "vibe-coding trap": build something elaborate before you've read enough to know a simpler, existing solution would do. His evidence:

- Bend's demo requires 58 lines to state that a player can never touch a flag, and 442 lines for an LLM to prove it — a lot of code for a small claim.
- Bend represents strings as linked lists rather than arrays, which he read as a performance oversight.
- Neither "formal verification" nor any adjacent term appears in Bend's codebase or website, which he took as evidence the field was unknown to its author.
- He recreated the same demo in SPARK, an existing formal-verification language, to show it could be done more directly — by his own account, "completely vibe-coded" with no further guidance.

## The Rebuttal

Bend's creator, posting as LightMachine, pointed to Formality — a language he built in 2018 specifically for formal verification. A five-year-old project in that exact field rules out the specific claim that he didn't know it existed.

The linked-list choice had a specific, numeric justification too: Bend evaluates programs on GPUs via interaction nets, where splitting a linked list's head from its tail is an O(1) operation. Splitting an array the same way is O(n) — it has to copy the remainder. For a design built around massive parallelism, that difference isn't cosmetic. The proof verbosity wasn't ignorance of inference or unification either, per the author — it was a deliberate choice to prioritize evaluation performance over compact proofs.

## SPARK Isn't the Universal Answer Either

Other commenters pushed back on the premise that SPARK was simply the correct tool Bend's author had missed. SPARK verifies against SMT solvers, which excel at the bounded, decidable properties mission-critical systems need — the fifty-year-old approach that's earned its reputation. But interactive theorem provers like Lean and Rocq can express a broader class of statements than SMT solvers can decide, and dependent typing lets you write conditions directly into a type in ways SPARK's contracts don't support. Recent progress on mixing LLMs with theorem provers has shifted the field toward that broader style. Which approach is "correct" depends on what you're trying to prove, not just on which one is more established.

## The Upshot

The critique's most quotable claim — that Bend's author didn't know formal verification existed — was wrong, and correctable with five minutes of looking at his own project history. The linked-list choice it cited as evidence of that ignorance turns out to be exactly the kind of tradeoff a systems-level performance decision produces: O(1) instead of O(n), on the operation the whole architecture depends on. None of that means Bend's verbose proofs are a good user experience, or that its choices are beyond criticism. It means a public critique of someone's technical decisions is worth checking against their actual track record before it goes out — and that "this person clearly didn't know X" is a much easier claim to make than to verify.
