# Design: GitHub-backed Comments via utterances

**Date:** 2026-04-15
**Status:** Approved

## Overview

Add a comment section to speaker and talk pages using [utterances](https://utteranc.es), a lightweight widget that stores comments as GitHub issues in a dedicated repository.

## Requirements

- Comments appear on both speaker profile pages and individual talk pages.
- Comments are shared across all language variants of a page (FR/EN/DE map to the same issue).
- Comments are stored in a dedicated GitHub repository, separate from the main site repo.

## GitHub Repository

A new public repository `brownbaglunch.org/public-comments` will be created to host the utterances issues.

- Must be **public** (utterances requirement).
- Contains no code — only auto-generated issues.
- The utterances GitHub App must be installed on this repository once by an org admin.

### Manual Prerequisites (one-time, before deployment)

1. Create `brownbaglunch.org/public-comments` on GitHub (public, empty).
2. Install the utterances app at [utteranc.es](https://utteranc.es) → "Install" → select only `public-comments`.

## Architecture

### New partial: `themes/brownbaglunch/layouts/_partials/comments.html`

Computes a canonical path by stripping the `/en/` or `/de/` language prefix from `.RelPermalink`, then renders the utterances script tag.

```html
{{ $term := .RelPermalink | replaceRE "^/(en|de)/" "/" }}
<div class="max-w-3xl mx-auto mt-12 pt-8 border-t border-warm-border">
  <h2 class="text-2xl font-bold mb-6">{{ i18n "comments" }}</h2>
  <script src="https://utteranc.es/client.js"
    repo="brownbaglunch.org/public-comments"
    issue-term="{{ $term }}"
    label="comment"
    theme="github-light"
    crossorigin="anonymous"
    async>
  </script>
</div>
```

- `label="comment"` — all utterances issues get this label for easy filtering.
- `theme="github-light"` — matches the site's light `cream` background.
- The partial receives the full page context so `.RelPermalink` is available.

### Layout changes

- `themes/brownbaglunch/layouts/speakers/speaker.html` — append `{{ partial "comments.html" . }}` after the talks section.
- `themes/brownbaglunch/layouts/speakers/talk.html` — append `{{ partial "comments.html" . }}` after the speaker attribution block.

### i18n additions

| Key | `i18n/fr.yaml` | `i18n/en.yaml` | `i18n/de.yaml` |
|-----|---------------|---------------|---------------|
| `comments` | Commentaires | Comments | Kommentare |

## Canonical path logic

| Page URL | Canonical term |
|----------|---------------|
| `/speakers/david-pilato/` | `/speakers/david-pilato/` |
| `/en/speakers/david-pilato/` | `/speakers/david-pilato/` |
| `/de/speakers/david-pilato/` | `/speakers/david-pilato/` |
| `/speakers/david-pilato/talks/elasticsearch/` | `/speakers/david-pilato/talks/elasticsearch/` |

The regex `^/(en|de)/` strips the language prefix; the default French language has no prefix, so it passes through unchanged.

## Files Changed

| File | Change |
|------|--------|
| `themes/brownbaglunch/layouts/_partials/comments.html` | New file |
| `themes/brownbaglunch/layouts/speakers/speaker.html` | Add partial call |
| `themes/brownbaglunch/layouts/speakers/talk.html` | Add partial call |
| `i18n/fr.yaml` | Add `comments` key |
| `i18n/en.yaml` | Add `comments` key |
| `i18n/de.yaml` | Add `comments` key |
