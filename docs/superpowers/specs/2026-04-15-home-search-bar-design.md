# Design: Home Page Search Bar

## Goal

Replace the two CTA buttons ("Trouver un speaker" / "Explorer les talks") on the home page with a large, prominent search bar. Hide the nav search bar on the home page only, since the home search bar takes its role.

## Approach

Reuse the existing Pagefind JS infrastructure without modification. The JS in `search.html` binds to `#search-container`, `#search-input`, and `#search-panel` on `DOMContentLoaded`. Since these IDs are conditionally rendered (nav on all pages except home, home bar only on home), they never coexist in the DOM — no conflict.

## Changes

### `themes/brownbaglunch/layouts/_partials/nav.html`

Wrap the existing `#search-container` div with `{{ if not .IsHome }}` / `{{ end }}` so the nav search is hidden on the home page only. No other change.

### `themes/brownbaglunch/layouts/home.html`

Remove the two CTA buttons (`home_cta_speakers`, `home_cta_talks`). In their place, render a large search bar:

- Container: `max-w-xl mx-auto`, `mt-8`, `relative`, `id="search-container"`, `data-section="all"`
- Input: full-width, rounded-full, `py-3 text-base pl-12 pr-4`, white background, `border-2 border-warm-border`, focus state `border-terracotta`
- Search icon: `w-5 h-5` (larger than the nav's `w-4 h-4`), `text-warm-brown/40`
- Results panel (`#search-panel`): same hidden dropdown as nav, anchored `left-0 right-0 top-full mt-2`, same classes as nav version

Light color scheme (white input on cream background) vs. nav's dark scheme (cream/20 on warm-brown).

`data-section="all"` ensures all sections (speakers, talks, cities) are searched by default, same as the nav when on the home page.

## What Does NOT Change

- `search.html` (JS) — no modification needed
- All other pages — nav search remains visible as today
- The stats section (speakers / topics / cities) — stays below the search bar
