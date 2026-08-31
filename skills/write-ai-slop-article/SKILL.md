---
name: write-ai-slop-article
description: Use this skill when the user wants a recap blog post written and published about what was built or accomplished in the current (or a specific past) Claude Code session - e.g. "write an ai-slop article about this", "summarize what we did as a post", "/write-ai-slop-article". Writes a taude.xyz post tagged ai-slop covering what was built plus real session stats (tokens used, message count, duration) pulled from the session transcript, then publishes it through the same Obsidian sync flow as the publish-taude-blog skill.
---

# Write an ai-slop session recap article

Generates a new taude.xyz post — tagged `ai-slop`, per the About page's
promise to label AI-assisted writing — recapping what got built in a
Claude Code session, with real usage stats from that session's
transcript, not estimates.

## 1. Identify the session

Don't guess. Claude Code session transcripts live at
`~/.claude/projects/<slug-of-cwd>/<session-id>.jsonl`, and a project
directory can hold more than one `.jsonl` with the *same* mtime (e.g. a
bridged/companion session running alongside the main one) — "pick the
newest file" is not reliable, confirmed by testing it against this exact
project directory.

The current session's id is reliable from one place: your own system
prompt's "Scratchpad Directory" section, which looks like
`/private/tmp/claude-<uid>/<slug-of-cwd>/<session-id>/scratchpad`. Pull
the session id out of that path. If the user wants a recap of a
*different*, earlier session instead of the live one, ask them for that
session's id (or help them find it by timestamp in
`~/.claude/projects/<slug-of-cwd>/`) rather than guessing.

## 2. Get the stats

```bash
python3 <path-to-this-skill>/session_usage.py <session-id>
```

(When this skill is invoked from `~/.claude/skills/write-ai-slop-article`,
that's the real path — it's a symlink to this file's actual location in
the taude.xyz repo, so it works either way.) This prints total
input/output/cache-creation/cache-read tokens, how many assistant
messages carried usage data, and the session's wall-clock span.

Treat it as best-effort: it parses Claude Code's internal transcript
format, which isn't a stable public API and could change between Claude
Code versions. If it errors, or the numbers look clearly wrong, say so
in the post rather than either failing silently or publishing a number
you don't trust.

## 3. Write the recap

Don't re-derive "what happened" from the transcript — you already know,
it's this conversation. Write a first-person (Todd's voice) recap: what
got built, key decisions and why, anything surprising or hard-won.
Match the tone and length of prior ai-slop posts in `content/posts/` —
direct, a little dry, not marketing copy.

Fold the stats from step 2 into their own section near the end (e.g.
"Session stats") rather than burying them — the point is transparency
about what a session like this actually costs, not just that it
happened. If you state a token total or estimated cost, note that
cache-read tokens are billed far cheaper than fresh input tokens, so a
raw sum of all categories overstates cost if read as-is.

## 4. Add an architecture diagram, if one earns its place

If the session built or changed something with a real shape — a
pipeline, a client/server split, a data flow across a few components —
a small Mermaid flowchart usually communicates it faster than a
paragraph. Skip it for posts that don't have that shape (a config
tweak, a one-off fix); not every recap needs one.

The site already has Mermaid wired in (`layouts/_partials/extend_head.html`
in the taude.xyz repo) — it renders in the site's own colors, follows
light/dark theme toggling automatically, and needs no per-post setup.
Just write the diagram straight into the post's markdown as raw HTML:

```html
<pre class="mermaid">
flowchart TD
  A[browser history] --> B[archivore run]
  B <--> C[archivore-queue D1]
  B --> D[output_dir vault]
</pre>
```

**Must be `<pre class="mermaid">`, not a ` ```mermaid ` fence.** Hugo's
Chroma highlighter has no mermaid lexer, so a fenced code block
collapses to a generic `language-fallback` class that can't be targeted
reliably — raw HTML is the only form that survives intact. (This is why
`markup.goldmark.renderer.unsafe = true` is set in `hugo.toml` — raw
HTML passthrough, safe here since every post is Todd's own content, not
third-party input.)

Keep the diagram to the same handful of boxes a prose "reduced to its
essentials" sentence would use — this is a recap post, not documentation;
a sprawling diagram works against the terse tone. `flowchart TD`
(top-down) reads best for a short pipeline; reach for `flowchart LR`
only if the shape is genuinely more left-to-right than top-down.

## 5. Publish it

Same flow as the `publish-taude-blog` skill:
1. Write the post as a new file in the Obsidian vault's `ai-drafted/`
   folder (`~/Library/Mobile Documents/com~apple~CloudDocs/Todd's
   Obsidian Vault/1 Projects/taude.xyz Blog/ai-drafted/`) — not `posts/`,
   which is Todd's own writing. `ai-drafted/` maps to the same
   `content/posts/` section in `scripts/publish.sh`'s `SECTION_MAP`, so
   it publishes to the same place, but keeps AI-authored drafts
   physically separate in the vault. The `AI Draft.md` Templater
   template that moves files into this folder defaults `tags` to
   `["ai-drafted"]` — keep that tag, and also add `ai-slop` (this
   skill's specific label for session recaps, per the About page's
   wording), so frontmatter reads `tags: ["ai-drafted", "ai-slop", ...]`
   plus whatever topic tags fit.
2. `cd ~/dev/taude.xyz && ./scripts/publish.sh` to sync, clean up
   Obsidian-specific markdown, and build the site locally.
3. Show the user what changed and get explicit go-ahead in chat before
   pushing (the script's own y/N prompt isn't a substitute for that) —
   unless the user's request already was an explicit instruction to
   publish, in which case that's the go-ahead.
4. After pushing, confirm the GitHub Actions deploy actually completed
   rather than assuming the push did the job — see `publish-taude-blog`
   for the exact `gh run list` polling commands.
