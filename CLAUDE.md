# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install Node dependencies (required before first build)
npm install

# Development server with live reload
hugo server

# Production build
hugo --gc --minify

# Build Pagefind search index (run after hugo build)
npx pagefind --site public

# Full production build sequence
hugo --gc --minify && npx pagefind --site public
```

Hugo requires version ≥ 0.157.0 (extended build). Node.js ≥ 18 is required for Tailwind/PostCSS.

## Architecture

This is a Hugo static site for the Brown Bag Lunch France community — a directory of speakers, talks, and cities.

### Tech Stack

- **Hugo** (SSG) + custom theme `brownbaglunch` in `themes/brownbaglunch/`
- **Tailwind CSS 3** processed via Hugo Pipes (PostCSS). Config in `tailwind.config.js` / `postcss.config.js`
- **Pagefind** for full-text search, run post-build; the `public/pagefind/` directory is mounted back into `static/pagefind/` via `hugo.toml` module mounts
- **GitHub Actions** deploys to GitHub Pages on push to `main`

### Content Model

Three content types, each organized as Hugo sections:

**Speakers** (`content/speakers/<letter>/<slug>/`)
- `_index.md` — speaker profile with front matter: `name`, `city`, `cities[]`, `cover`, `contacts` (mail, x), `websites[]`, `since`, `layout: speaker`
- A speaker's `cities` field holds slash-separated country/city codes (e.g. `fr/nantes`) or wildcards (`fr/*`, `*/*`)

**Talks** (`content/speakers/<letter>/<slug>/talks/<talk-slug>/index.md`)
- Front matter: `layout: talk`, `tags[]`, `versions[]` (each version has `label`, `flag`, `title`, `abstract`)
- Talks live nested under the speaker directory; `site.Pages` traversal aggregates them

**Cities** (`content/cities/<country>/<city>/`)
- `_index.md` — city profile with front matter: `title`, `country`, `city`, `lat`, `lng`
- Cover image at `cover.jpg|png` alongside the `_index.md`

Speakers are cross-referenced to cities via the `cities` field — the partial `speakers-for-city.html` resolves this including wildcard matching.

### Theme Layouts (`themes/brownbaglunch/layouts/`)

Key layout files:
- `_default/baseof.html` — outer shell (nav, main, footer, search modal)
- `speakers/speaker.html` — speaker profile page
- `speakers/list.html` / `speakers/letter.html` — alphabet-indexed speaker list
- `cities/list.html` — city list and individual city pages (same template, branched on `country` param)
- `talks/list.html` — all talks aggregated
- `tags/term.html` — talks filtered by tag

Partials of note:
- `speaker-card.html` — card used in grids
- `session-card.html` — talk card
- `speakers-for-city.html` — filters speakers for a given city with wildcard support
- `cover-url.html` — resolves speaker/city cover image (Gravatar URL or local file)

### Styling

Custom Tailwind colors (defined in `tailwind.config.js`):
- `terracotta` (#e07b39) — primary accent
- `cream` (#fdf6ee) — page background
- `warm-brown` (#3d2b1f) — text
- `warm-border` (#f0e4d0) — borders
- `warm-light` (#fff8f0) — card backgrounds

Utility classes `.btn-primary`, `.badge`, `.card` are defined as Tailwind components in `themes/brownbaglunch/assets/css/main.css`.

### i18n

Translation strings live in `i18n/fr.yaml` and `i18n/en.yaml`. The site defaults to French (`defaultContentLanguage = 'fr'`).

### URL Structure

Defined in `hugo.toml` permalinks:
- Speakers: `/speakers/<slug>/`
- Talks (tags): `/talks/<tag-slug>/`
