# Design: fogus.me-inspired Typography

**Date:** 2026-08-10  
**Status:** Approved

## Goal

Adopt the dense, terminal-like aesthetic of blog.fogus.me while keeping taude.xyz's existing structure: sidebar, dark mode, AI markers, color accents, and all section layouts.

## Approach

Hybrid: monospace font + tighter typographic settings. No layout files, no Hugo templates, no config changes. Two files only.

## Changes

### `layouts/_partials/extend_head.html`

Add a `<link>` to load JetBrains Mono from Google Fonts, before the existing pre-paint script:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
```

### `assets/css/extended/custom.css`

Add at the top (before existing rules):

```css
/* fogus.me-inspired typographic density */
body {
    font-family: "JetBrains Mono", monospace;
    font-size: 15px;
    line-height: 1.35;
}

h1, h2, h3, h4, h5, h6 {
    text-transform: uppercase;
}

:root {
    --gap: 16px;
    --content-gap: 14px;
}
```

## What stays the same

- All layout files (`baseof.html`, `index.html`, section layouts, partials)
- `hugo.toml` config
- All existing custom CSS component classes (sidebar, TIL, quotes, AI markers)
- Dark/light mode, `--ai-accent` color, social icons
- Font inherits into all components automatically via `body` cascade

## Success criteria

- `hugo --minify` exits 0 with no ERROR lines
- Site renders locally with JetBrains Mono, visibly tighter density
- Dark mode, sidebar, AI markers, and all section pages look correct
- No regressions on mobile (sidebar stacks, font readable at 14px mobile fallback)
