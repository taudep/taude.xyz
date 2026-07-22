#!/usr/bin/env bash
# Sync markdown from the Obsidian taude.xyz Blog folder into content/,
# build the site to make sure nothing's broken, then commit and push.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VAULT_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Todd's Obsidian Vault/1 Projects/taude.xyz Blog"

cd "$REPO_DIR"

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

python3 "$REPO_DIR/scripts/clean_obsidian_links.py" content/til content/posts content/quotes

echo
echo "Building site to verify..."
rm -rf public resources
hugo --minify

echo
echo "Changes to publish:"
git status --short content/til content/posts content/quotes

if git diff --quiet --cached -- content/til content/posts content/quotes && \
   git diff --quiet -- content/til content/posts content/quotes && \
   [ -z "$(git ls-files --others --exclude-standard content/til content/posts content/quotes)" ]; then
  echo "Nothing new to publish."
  exit 0
fi

read -r -p "Commit and push these changes? [y/N] " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
  git add content/til content/posts content/quotes
  msg="${1:-Publish from Obsidian $(date '+%Y-%m-%d %H:%M')}"
  git commit -m "$msg"
  git push origin master
  echo "Pushed. GitHub Actions will build and deploy to taude.xyz shortly."
else
  echo "Skipped commit/push. Changes are synced into content/ but not committed."
fi
