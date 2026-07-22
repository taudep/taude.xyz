#!/usr/bin/env bash
# Sync markdown from the Obsidian taude.xyz Blog folder into content/,
# build the site to make sure nothing's broken, then commit and push.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VAULT_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Todd's Obsidian Vault/1 Projects/taude.xyz Blog"

cd "$REPO_DIR"

TARGETS=(content/til content/posts content/quotes content/about.md)

for section in til posts quotes; do
  src="$VAULT_DIR/$section"
  dest="content/$section"
  mkdir -p "$dest"
  if [ -d "$src" ]; then
    rsync -av --include="*.md" --exclude="*" "$src"/ "$dest"/
  else
    echo "warning: $src does not exist, skipping" >&2
  fi
done

# Standalone single pages (not a section folder) live at the vault root.
if [ -f "$VAULT_DIR/About.md" ]; then
  cp "$VAULT_DIR/About.md" content/about.md
else
  echo "warning: $VAULT_DIR/About.md does not exist, skipping" >&2
fi

python3 "$REPO_DIR/scripts/clean_obsidian_links.py" "${TARGETS[@]}"

echo
echo "Building site to verify..."
rm -rf public resources
hugo --minify

echo
echo "Changes to publish:"
git status --short "${TARGETS[@]}"

if git diff --quiet --cached -- "${TARGETS[@]}" && \
   git diff --quiet -- "${TARGETS[@]}" && \
   [ -z "$(git ls-files --others --exclude-standard "${TARGETS[@]}")" ]; then
  echo "Nothing new to publish."
  exit 0
fi

read -r -p "Commit and push these changes? [y/N] " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
  git add "${TARGETS[@]}"
  msg="${1:-Publish from Obsidian $(date '+%Y-%m-%d %H:%M')}"
  git commit -m "$msg"
  git push origin master
  echo "Pushed. GitHub Actions will build and deploy to taude.xyz shortly."
else
  echo "Skipped commit/push. Changes are synced into content/ but not committed."
fi
