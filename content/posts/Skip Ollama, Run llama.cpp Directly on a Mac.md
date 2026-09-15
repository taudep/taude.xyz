---
title: Skip Ollama, Run llama.cpp Directly on a Mac
date: 2026-09-15
draft: false
tags:
  - ai-drafted
slug: "skip-ollama-run-llama-cpp-directly-on-a-mac"
---
*Prompted by an HN thread: [The Local LLM Ecosystem Doesn't Need Ollama](https://news.ycombinator.com/item?id=47788385)*

Ollama is built on llama.cpp. For more than 400 days it ignored a GitHub issue asking it to say so. That's the headline complaint in a recent Hacker News thread — but the more useful finding, buried underneath, is that llama.cpp no longer needs a wrapper at all. On a Mac it's now the simpler choice, not the harder one.

## The Case Against Ollama

| Complaint        | Detail                                                                                                                     |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------- |
| No credit        | An issue requesting MIT-licence attribution went unanswered for over 400 days before Ollama added a single line.           |
| Slower           | Commenters reported llama.cpp running identical models faster than Ollama, with lower memory use.                          |
| Lock-in          | Ollama stores models as hashed blobs that only Ollama can read. A `.gguf` file works in any tool that supports the format. |
| Broken templates | Ollama's Go templating engine cannot fully render Jinja chat templates, which has garbled prompts for some models.         |

Some commenters defended Ollama: a venture-backed company must monetise, and no open-source project is perfectly virtuous. That argument held up better before llama.cpp closed the gap in usability that justified the wrapper in the first place.

## Why the Gap Has Closed, on a Mac Specifically

- `llama-server` now includes a web interface, an OpenAI-compatible API, MCP support and model hot-swapping — the features people cited to justify Ollama.
- Hugging Face model pages now publish a one-line `llama-server` command for each GGUF release.
- LM Studio bundles both llama.cpp and Apple's MLX backend and picks whichever runs faster for a given model.
- LlamaBarn, a macOS menu-bar app, wraps `llama-server` and stores models in the standard Hugging Face cache, so other tools can read them too.

## Running It

**Install:**

```bash
brew install llama.cpp
```

**Run a model straight from Hugging Face:**

```bash
llama-server -hf unsloth/Llama-3.2-3B-Instruct-GGUF
```

This starts an OpenAI-compatible API on `localhost:8080` with Metal acceleration and a built-in chat UI, using the open `.gguf` format.

**Choose a quantisation level:**

| Mac RAM | Quantisation |
|---|---|
| 16–24GB | Q4_K_M |
| 32GB or more | Q5_K_M or Q8_0 |

A rough guide: memory use in gigabytes is roughly the parameter count in billions, multiplied by bits per weight, divided by 8. Apple's unified memory removes the VRAM ceiling that limits discrete-GPU machines, so higher-precision quantisations are worth trying once RAM allows.

**Stay current.** New architectures — Gemma was one example raised in the thread — need a recent llama.cpp build to run. `brew upgrade llama.cpp` is the first troubleshooting step, not a last resort.

**Want a GUI?** LM Studio picks the faster backend automatically and keeps models in an open format.

## The Upshot

Ollama's advantage was ease of use. Llama.cpp has largely matched it: a web UI, an API server and one-line model downloads, without the lock-in. On a Mac, where Metal and unified memory already make single-machine inference fast, running `llama-server` directly — or through LM Studio — gets the same convenience, an open format, and, on the thread's evidence, better speed.
