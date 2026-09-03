---
title: <% tp.file.title %>
date: 2026-09-01
original_date: 2026-09-01
draft: false
tags:
  - ai-drafted
  - cli-tip
slug: "local-dev-secret-management-with-1password-and-bitwarden"
---
Most developers have a graveyard of dotfiles, `.env` files, and Slack DMs containing tokens that were supposed to be temporary. This post describes the pattern I use to keep all local dev secrets in a password manager and inject them into my shell on demand — nothing sensitive ever touches disk.

The full setup lives in my [dot-local repo on GitHub](https://github.com/taudep/dot-local), including the helper functions and new-machine setup guide.

## The Problem

I work across multiple machines: a work Mac that uses 1Password and a personal Mac that uses Bitwarden. I needed a single pattern that worked on both without maintaining two separate codebases or hardcoding tool-specific logic everywhere.

## How It Works

Two pieces:

1. **A password manager note** containing all environment variable definitions in `KEY=value` format — one note per machine (or shared, if you want).
2. **Shell helper functions** ([`zsh/pm-env`](https://github.com/taudep/dot-local/blob/master/zsh/pm-env)) that auto-detect which password manager CLI is available, read the note at runtime, and export each variable into the current session.

The helpers are safe to commit — they contain no secrets, only the logic to fetch them.

## Prerequisites

- **1Password** (work Mac): `brew install 1password-cli` + enable CLI integration in Settings → Developer → Connect with 1Password CLI
- **Bitwarden** (personal Mac): `brew install bitwarden-cli` + `brew install jq`

## Password Manager Note Format

Create a Secure Note in 1Password or a note item in Bitwarden. The body should have one env var per line:

```text
# Lines starting with # are ignored
# Blank lines are also ignored

GITHUB_TOKEN=your-token-here
ANTHROPIC_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
JIRA_API_TOKEN=your-token-here

# 'export' prefix is optional — it gets stripped automatically
export JFROG_ACCESS_TOKEN=your-token-here
```

## The Shell Helpers

The full source is in [`zsh/pm-env`](https://github.com/taudep/dot-local/blob/master/zsh/pm-env). Here's how it breaks down:

### Backend detection

```zsh
# Detects 'op' or 'bw' from PATH, or reads PM_BACKEND if set.
_pm_backend() {
  if -n "$PM_BACKEND"; then
    echo "$PM_BACKEND"
    return
  fi
  command -v op &>/dev/null && { echo "op"; return; }
  command -v bw &>/dev/null && { echo "bw"; return; }
  echo "none"
}
```

### Note reader

```zsh
# Reads the plaintext notes field from the active password manager.
_pm_read_note() {
  local note="$1"
  local vault="${PM_OP_VAULT:-Employee}"
  case "$(_pm_backend)" in
    op)
      op read "op://${vault}/${note}/notesPlain"
      ;;
    bw)
      if -z "$BW_SESSION"; then
        echo "error: BW_SESSION not set. Run: bw-unlock" >&2
        return 1
      fi
      bw get item "$note" --session "$BW_SESSION" | jq -r '.notes // empty'
      ;;
    *)
      echo "error: no password manager CLI found." >&2
      return 1
      ;;
  esac
}
```

### The main function

```zsh
# Load env vars from a password manager note.
# Usage: op-env                    (uses $PM_NOTE_NAME)
#        op-env MY-NOTE-NAME       (override for this call)
#        op-env op://Vault/I/field (legacy 1Password URI)
op-env() {
  local arg="${1:-${PM_NOTE_NAME}}"
  if -z "$arg"; then
    echo "error: no note name given. Set PM_NOTE_NAME or pass a note name." >&2
    return 1
  fi
  local content line varname
  if "$arg" == op://*; then
    content=$(op read "$arg") || return 1
  else
    content=$(_pm_read_note "$arg") || return 1
  fi
  while IFS= read -r line; do
    | "$line" == \#* && continue
    line="${line#export }"
    if [[ "$line" =~ ^([A-Za-z_][A-Za-z0-9_]*)=(.+)$ ]]; then
      varname="${match[1]}"
      export "$line"
      echo "  exported: $varname"
    fi
  done <<< "$content"
}

# Convenience wrapper: sets TAUDE_SECURE, loads secrets, re-sources prompt config.
taude-secure() {
  export TAUDE_SECURE=true
  op-env
  source ~/.p10k.zsh
}

# Bitwarden only: unlock vault and export session key.
bw-unlock() {
  export BW_SESSION=$(bw unlock --raw) && echo "Bitwarden session unlocked."
}
```

## Per-Machine Configuration

The helpers live in the repo and are the same on every machine. The only machine-specific piece is a `~/.zshrc.local` file that sets a few env vars — this file is **not** tracked in git.

**Work Mac (`~/.zshrc.local`)**
```zsh
export PM_NOTE_NAME=WORK-DEV-SECRETS
# PM_BACKEND=op is auto-detected when 1Password CLI is installed
```

**Personal Mac (`~/.zshrc.local`)**
```zsh
export PM_BACKEND=bw
export PM_NOTE_NAME=personal-dev-secrets
```

The tracked `~/.zshrc` just sources it at the end:

```zsh
-f ~/.zshrc.local && source ~/.zshrc.local
```

## Daily Usage

**Work Mac (1Password)**
```zsh
taude-secure
# Touch ID prompt appears if the CLI session has expired
#   exported: GITHUB_TOKEN
#   exported: ANTHROPIC_API_KEY
#   ...
```

**Personal Mac (Bitwarden)**
```zsh
bw-unlock      # enter master password once per session
taude-secure    # reads the note and exports all env vars
```

## Security Properties

**No plaintext on disk.** Secrets live only in your password manager. Every file in the repo is safe to make public.

**Session-scoped.** Exported variables exist only in the current shell process and disappear when the terminal closes.

**Biometric-gated.** The 1Password CLI requires Touch ID (or password) each time the session expires. Bitwarden requires your master password once per terminal session via `bw-unlock`.

**Single source of truth.** Rotating a token means editing one note in your password manager — no dotfiles to hunt down, no commits to make.

**Audit trail.** 1Password logs every CLI read in the item's activity history.

## Rotating or Adding a Secret

1. Open your password manager and edit the note.
2. Add or update the `KEY=value` line.
3. In any open terminal, run `op-env` again.

No code changes. No commits. Done.

## Setting Up a New Machine

Full steps are in the [dot-local README](https://github.com/taudep/dot-local#new-machine-setup). The short version:

```zsh
# 1. Clone the repo
git clone https://github.com/taudep/dot-local ~/dev/projects/taudep/dot-local

# 2. Symlink the helpers
ln -sf ~/dev/projects/taudep/dot-local/zsh/pm-env ~/.pm-env

# 3. Source it from your shell config
echo 'source ~/.pm-env' >> ~/.bash_aliases

# 4. Create your machine-local config (not tracked in git)
echo 'export PM_NOTE_NAME=your-note-name' >> ~/.zshrc.local
# Add: export PM_BACKEND=bw   (if you're on Bitwarden)
```

## Onboarding a Teammate

1. Point them to the [dot-local repo](https://github.com/taudep/dot-local) and the [secret management docs](https://github.com/taudep/dot-local/blob/master/docs/secret-management.md).
2. Share the relevant password manager item with them through your password manager's sharing feature.
3. They create their `~/.zshrc.local` with `PM_NOTE_NAME` pointing to their copy of the note.

## Why Not direnv or dotenv?

Those tools are great, but they still write secrets to a file on disk (`.envrc`, `.env`). If that file ends up in a repo, gets synced to cloud storage, or sits on a lost laptop, or Claude slurps it up, the secrets are exposed. This approach keeps the canonical secret store entirely inside your password manager — the only thing on disk is the shell function that knows *where* to look.
