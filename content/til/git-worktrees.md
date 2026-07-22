---
title: "Using git worktrees to avoid stashing"
date: 2026-07-20
draft: false
tags: ["git"]
slug: "git-worktrees"
---

`git worktree add ../hotfix main` checks out a second working copy of the
repo in a sibling directory, sharing the same `.git` history. Handy for
jumping onto a hotfix without stashing whatever you're mid-way through.
