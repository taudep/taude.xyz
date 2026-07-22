---
title: Publishing from Obsidian
date: 2026-07-22T09:00:00+03:00
draft: false
tags: ["hugo", "obsidian"]
slug: "publishing-from-obsidian"
---

Wired up a script that rsyncs markdown out of my taude.xyz Blog vault
folder straight into the Hugo repo's content directory, then builds and
pushes. Turns out Hugo slugifies filenames automatically, so Obsidian's
spaces-and-caps note titles turn into clean URLs for free.
