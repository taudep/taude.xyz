#!/usr/bin/env bash
# Sync markdown from the Obsidian taude.xyz Blog folder into content/,
# build the site to make sure nothing's broken, then commit and push.
#
# Usage: ./scripts/publish.sh [--no-preview] [commit message]
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VAULT_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Todd's Obsidian Vault/1 Projects/taude.xyz Blog"

PREVIEW=1
COMMIT_MSG=""
for arg in "$@"; do
  case "$arg" in
    --no-preview) PREVIEW=0 ;;
    *) COMMIT_MSG="$arg" ;;
  esac
done

cd "$REPO_DIR"

TARGETS=(content/til content/posts content/quotes content/about.md)

# vault_folder:content_dest — multiple vault folders can feed the same
# content/ section (e.g. ai-drafted/ notes still publish as posts/).
SECTION_MAP=(til:til posts:posts quotes:quotes ai-drafted:posts)

for pair in "${SECTION_MAP[@]}"; do
  section="${pair%%:*}"
  dest_name="${pair##*:}"
  src="$VAULT_DIR/$section"
  dest="content/$dest_name"
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

if [ "$PREVIEW" -eq 1 ]; then
  pkill -f "hugo server.*$REPO_DIR" 2>/dev/null || true
  hugo server -D -p 1313 > /tmp/taude-xyz-preview.log 2>&1 &
  PREVIEW_PID=$!
  sleep 1
  echo
  echo "Preview running at http://localhost:1313/ (drafts included)."
  read -r -p "Take a look, then press Enter here to continue... " _
  kill "$PREVIEW_PID" 2>/dev/null || true
fi

read -r -p "Commit and push these changes? [y/N] " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
  git add "${TARGETS[@]}"
  msg="${COMMIT_MSG:-Publish from Obsidian $(date '+%Y-%m-%d %H:%M')}"
  git commit -m "$msg"
  git push origin master
  echo "Pushed. GitHub Actions will build and deploy to taude.xyz shortly."
else
  echo "Skipped commit/push. Changes are synced into content/ but not committed."
fi
