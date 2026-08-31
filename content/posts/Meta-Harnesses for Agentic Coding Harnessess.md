---
title: <% tp.file.title %>
date: 2026-08-31T10:56:10-04:00
original_date: 08/17/2026
draft: true
tags:
  - ai-coding-tools
  - ai-coding
slug: "meta-harnesses-for-agentic-coding-harnessess"
---
Misc Notes and thoughts on the state of the coding harness harness.  Have to be a cowboy and roundup all my agents running in the wild....
# Current Agent Control Center
I'm currently MacOs and running [CMUX](https://cmux.com/), one of the earlier tools for controlling multiple agentic sessions at the same time.  I lost my TMUX config a long time ago, and didn't really need the remove session connectivity aspect, so I'm just fine managing windows/tabs/panes locally, and CMUX makes that dead easy.   It's built on my favorite terminal Ghostty, and it's been my workhorse for several months.  I have several custom scripts I run for resuming  sessions, finding orphaned sessions, etc....

I do want to work towards an OS-independent solution, it could involve customized raw TMUX, as I have a Arch dev machine being built....

Some key things for me:
- rehydrates after system updates and reboots
- easy to find
- works with my custom directory structure and integrates naturally to my worktree flow
- scriptable
- Custom hooks (I have .session-resume) hooks for continuing my coding sessions for when Claude/Copilot/Pi.DEV/OpenCode start back up.  
- 


However, I'm open to evolving my kit.  Here's some interesting other tools that keep popping up over on Hacker News.

# To Try
- [Saggar](https://saggar.marginalutility.dev/) - A native Mac terminal that keeps projects, sessions, and attention organized.  What's cool about this one is that there's a Companion app to control all the different terminal sessions. I haven't gotten to play much, but it looks pretty polished. I like the nice command palette interfice (similar to a lot of tools, like VSCode, Obsidian, etc.)
- [https://github.com/terhechte/Cormac](Cormac) - Another lib Ghostty implementation.  Supports VIM bindings. 
- [Captian Miao]](https://github.com/terhechte/Cormac) - A terminal dashboard for all your coding agents.  Fast iterating through waiting sessions.  Control remote machine sessions.   This isn't a terminal, but just software running in your terminal. 
- herdr
- Zellij
- TMUX - With custom 

<% tp.file.move("1 Projects/taude.xyz Blog/posts/" + tp.file.title) %>
