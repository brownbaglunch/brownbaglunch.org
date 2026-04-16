# SEO Meta Tags — Design Spec

**Date:** 2026-04-17
**Status:** Approved

## Goal

Add comprehensive SEO meta tags to improve Google indexing and social sharing for brownbaglunch.org. All site-level parameters are stored in `hugo.toml` under `[params.seo]`.

## Hugo Config Changes

### `hugo.toml`

Two changes:

1. Correct `baseURL` from `https://v2.brownbaglunch.org/` to `https://brownbaglunch.org/`

2. Add `[params.seo]` block:

```toml
[params.seo]
  description = "Annuaire de speakers pour vos Brown Bag Lunch — conférences gratuites le temps d'un déjeuner."
  ogImage     = "/og-default.png"
  xAccount    = "@bbl_fr"
```

- `description` — fallback meta description for pages without their own content
- `ogImage` — path in `static/` to the default OG image (1200×630 px recommended); must be added manually
- `xAccount` — official X (Twitter) account, injected into `twitter:site`

## New File: `themes/brownbaglunch/layouts/_partials/seo.html`

A dedicated partial handling all SEO meta. Called from `head.html`. Contains four blocks:

### Open Graph (all pages)

| Tag | Value |
|-----|-------|
| `og:title` | `.Title` or site title |
| `og:description` | `.Description`, or speaker bio excerpt, or `params.seo.description` |
| `og:image` | Speaker cover URL if available, else `params.seo.ogImage` |
| `og:url` | `.Permalink` |
| `og:type` | `profile` for speaker pages, `website` elsewhere |
| `og:site_name` | `Brown Bag Lunch` |

### Twitter Cards (all pages)

| Tag | Value |
|-----|-------|
| `twitter:card` | `summary_large_image` |
| `twitter:site` | `params.seo.xAccount` |
| `twitter:title` | Same as `og:title` |
| `twitter:description` | Same as `og:description` |
| `twitter:image` | Same as `og:image` |

### hreflang (all pages)

One `<link rel="alternate" hreflang="...">` per language (fr, en, de) via `.Translations`, plus `x-default` pointing to the FR version.

### JSON-LD (conditional)

- **Speaker pages** (`layout: speaker`) → `Person` schema:
  - `name`, `image`, `description` (bio excerpt), `url` (.Permalink)
  - `sameAs`: X profile URL and `websites[]` URLs from front matter
- **Homepage** → `WebSite` schema with `SearchAction` (Pagefind search)
- **All other pages** → no JSON-LD

## Changes to `head.html`

Add two lines before the CSS `<link>`:

```html
<link rel="canonical" href="{{ .Permalink }}">
{{ partial "seo.html" . }}
```

## New File: `static/robots.txt`

```
User-agent: *
Allow: /

Sitemap: https://brownbaglunch.org/sitemap.xml
```

Hugo already generates `sitemap.xml` automatically at build time.

## Out of Scope

- Adding the `static/og-default.png` image (must be provided manually)
- JSON-LD for city or talk pages
- Google Search Console setup
