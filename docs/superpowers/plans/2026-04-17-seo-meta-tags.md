# SEO Meta Tags Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Open Graph, Twitter Cards, canonical URLs, hreflang, JSON-LD, and robots.txt to improve Google indexing and social sharing for brownbaglunch.org.

**Architecture:** A dedicated `seo.html` partial handles all SEO meta and is called from `head.html`. Site-level parameters live in `hugo.toml` under `[params.seo]`. JSON-LD is injected conditionally based on page type.

**Tech Stack:** Hugo templates, Hugo `dict`/`jsonify`/`merge` builtins, Schema.org JSON-LD.

---

## File Map

| Action | File | Purpose |
|--------|------|---------|
| Modify | `hugo.toml` | Fix `baseURL`, add `[params.seo]` block |
| Modify | `themes/brownbaglunch/layouts/_partials/head.html` | Add `<link rel="canonical">` + call `seo.html` |
| Create | `themes/brownbaglunch/layouts/_partials/seo.html` | All SEO meta: OG, Twitter Cards, hreflang, JSON-LD |
| Create | `static/robots.txt` | Allow-all + sitemap pointer |

---

## Task 1: Fix baseURL and add [params.seo] in hugo.toml

**Files:**
- Modify: `hugo.toml`

- [ ] **Step 1: Verify the current build passes**

```bash
hugo --gc --minify
```
Expected: `Total in XXX ms` with no errors.

- [ ] **Step 2: Fix baseURL**

In `hugo.toml`, change line 1:
```toml
baseURL = 'https://brownbaglunch.org/'
```

- [ ] **Step 3: Add [params.seo] block**

In `hugo.toml`, after the `[params.utterances]` block, append:
```toml
[params.seo]
  description = "Annuaire de speakers pour vos Brown Bag Lunch — conférences gratuites le temps d'un déjeuner."
  ogImage     = "/og-default.png"
  xAccount    = "@bbl_fr"
```

- [ ] **Step 4: Rebuild and verify params are accessible**

```bash
hugo --gc --minify
```
Expected: build succeeds. No warnings about unknown params.

- [ ] **Step 5: Commit**

```bash
git add hugo.toml
git commit -m "🔧 Fix baseURL and add [params.seo] config block"
```

---

## Task 2: Create seo.html with Open Graph and Twitter Cards

**Files:**
- Create: `themes/brownbaglunch/layouts/_partials/seo.html`

- [ ] **Step 1: Create the partial with OG and Twitter Cards**

Create `themes/brownbaglunch/layouts/_partials/seo.html` with this content:

```html
{{/*
  SEO partial — Open Graph, Twitter Cards, hreflang, JSON-LD
  Called from head.html for every page.
*/}}

{{/* ---- Description ---- */}}
{{ $desc := .Site.Params.seo.description }}
{{ if .Description }}
  {{ $desc = .Description }}
{{ else if or .IsPage .IsSection }}
  {{ with .Summary }}{{ $desc = . | plainify | truncate 160 }}{{ end }}
{{ end }}

{{/* ---- OG image (must be absolute URL) ---- */}}
{{ $img := .Site.Params.seo.ogImage | absURL }}
{{ if eq .Params.layout "speaker" }}
  {{ $coverSrc := partial "cover-url.html" . }}
  {{ with $coverSrc }}
    {{ if strings.HasPrefix . "http" }}
      {{ $img = . }}
    {{ else }}
      {{ $img = . | absURL }}
    {{ end }}
  {{ end }}
{{ end }}

{{/* ---- OG type ---- */}}
{{ $ogType := "website" }}
{{ if eq .Params.layout "speaker" }}{{ $ogType = "profile" }}{{ end }}

{{/* ---- Title ---- */}}
{{ $title := .Site.Title }}
{{ with .Title }}{{ $title = . }}{{ end }}

<!-- Open Graph -->
<meta property="og:title" content="{{ $title }}">
<meta property="og:description" content="{{ $desc }}">
<meta property="og:image" content="{{ $img }}">
<meta property="og:url" content="{{ .Permalink }}">
<meta property="og:type" content="{{ $ogType }}">
<meta property="og:site_name" content="{{ .Site.Title }}">

<!-- Twitter Cards -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="{{ .Site.Params.seo.xAccount }}">
<meta name="twitter:title" content="{{ $title }}">
<meta name="twitter:description" content="{{ $desc }}">
<meta name="twitter:image" content="{{ $img }}">
```

- [ ] **Step 2: Wire the partial into head.html**

Open `themes/brownbaglunch/layouts/_partials/head.html`. Add two lines after the existing `<meta name="description">` line and before the `{{ $css := ... }}` line:

```html
<link rel="canonical" href="{{ .Permalink }}">
{{ partial "seo.html" . }}
```

The file should look like:
```html
<meta charset="UTF-8">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="alternate icon" href="/favicon.ico">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ if .Title }}{{ .Title }} — {{ end }}{{ .Site.Title }}</title>
<meta name="description" content="{{ with .Description }}{{ . }}{{ else }}{{ .Site.Title }}{{ end }}">
<link rel="canonical" href="{{ .Permalink }}">
{{ partial "seo.html" . }}
{{ $css := resources.Get "css/main.css" | css.PostCSS }}
{{ if hugo.IsProduction }}
  {{ $css = $css | minify | fingerprint }}
{{ end }}
<link rel="stylesheet" href="{{ $css.RelPermalink }}"{{ if hugo.IsProduction }} integrity="{{ $css.Data.Integrity }}"{{ end }}>
```

- [ ] **Step 3: Build and verify OG tags appear on the homepage**

```bash
hugo --gc --minify && grep -A1 'og:title\|og:type\|og:image\|twitter:card' public/index.html
```
Expected output includes:
```
<meta property="og:title" content="Brown Bag Lunch">
<meta property="og:type" content="website">
<meta property="og:image" content="https://brownbaglunch.org/og-default.png">
<meta name="twitter:card" content="summary_large_image">
```

- [ ] **Step 4: Verify OG tags on a speaker page**

```bash
grep -r 'og:type.*profile' public/speakers/ | head -1
```
Expected output contains:
```
<meta property="og:type" content="profile">
```

- [ ] **Step 5: Commit**

```bash
git add themes/brownbaglunch/layouts/_partials/seo.html \
        themes/brownbaglunch/layouts/_partials/head.html
git commit -m "✨ Add Open Graph and Twitter Card meta tags"
```

---

## Task 3: Add hreflang alternate links

**Files:**
- Modify: `themes/brownbaglunch/layouts/_partials/seo.html`

- [ ] **Step 1: Append hreflang block to seo.html**

At the end of `themes/brownbaglunch/layouts/_partials/seo.html`, after the Twitter Cards block, add:

```html

<!-- hreflang (multilingual: fr / en / de) -->
{{ range .AllTranslations }}
<link rel="alternate" hreflang="{{ .Language.Lang }}" href="{{ .Permalink }}">
{{ end }}
{{ $frVersion := index (where .AllTranslations "Language.Lang" "fr") 0 }}
{{ with $frVersion }}
<link rel="alternate" hreflang="x-default" href="{{ .Permalink }}">
{{ end }}
```

- [ ] **Step 2: Build and verify hreflang on the homepage**

```bash
hugo --gc --minify && grep 'hreflang' public/index.html
```
Expected (3 alternate + 1 x-default):
```
<link rel="alternate" hreflang="fr" href="https://brownbaglunch.org/">
<link rel="alternate" hreflang="en" href="https://brownbaglunch.org/en/">
<link rel="alternate" hreflang="de" href="https://brownbaglunch.org/de/">
<link rel="alternate" hreflang="x-default" href="https://brownbaglunch.org/">
```

- [ ] **Step 3: Commit**

```bash
git add themes/brownbaglunch/layouts/_partials/seo.html
git commit -m "✨ Add hreflang alternate links for fr/en/de"
```

---

## Task 4: Add JSON-LD for speaker pages

**Files:**
- Modify: `themes/brownbaglunch/layouts/_partials/seo.html`

- [ ] **Step 1: Append JSON-LD speaker block to seo.html**

At the end of `themes/brownbaglunch/layouts/_partials/seo.html`, after the hreflang block, add:

```html

{{/* ---- JSON-LD ---- */}}
{{ if eq .Params.layout "speaker" }}
  {{ $speaker := .Params }}
  {{ $coverSrc := partial "cover-url.html" . }}
  {{ $sameAs := slice }}
  {{ with $speaker.contacts.x }}
    {{ $sameAs = $sameAs | append (printf "https://x.com/%s" .) }}
  {{ end }}
  {{ range $speaker.websites }}
    {{ $sameAs = $sameAs | append .url }}
  {{ end }}
  {{ $ldJson := dict
    "@context" "https://schema.org"
    "@type" "Person"
    "name" (printf "%s %s" $speaker.firstname $speaker.lastname)
    "description" $desc
    "url" .Permalink
  }}
  {{ with $coverSrc }}
    {{ $ldJson = merge $ldJson (dict "image" .) }}
  {{ end }}
  {{ with $sameAs }}
    {{ $ldJson = merge $ldJson (dict "sameAs" .) }}
  {{ end }}
<script type="application/ld+json">{{ $ldJson | jsonify }}</script>
{{ end }}
```

- [ ] **Step 2: Build and verify JSON-LD on a speaker page**

```bash
hugo --gc --minify && grep -r 'application/ld+json' public/speakers/ | head -3
```
Expected: lines containing `<script type="application/ld+json">` with `"@type":"Person"`.

- [ ] **Step 3: Validate the JSON is well-formed**

```bash
python3 -c "
import re, glob, json
f = glob.glob('public/speakers/r/romain-*/index.html')[0]
html = open(f).read()
m = re.search(r'<script type=\"application/ld\+json\">(.*?)</script>', html, re.DOTALL)
json.loads(m.group(1))
print('Valid JSON:', f)
"
```
Expected: `Valid JSON: public/speakers/r/romain-.../index.html`

- [ ] **Step 4: Commit**

```bash
git add themes/brownbaglunch/layouts/_partials/seo.html
git commit -m "✨ Add JSON-LD Person schema for speaker pages"
```

---

## Task 5: Add JSON-LD for homepage

**Files:**
- Modify: `themes/brownbaglunch/layouts/_partials/seo.html`

- [ ] **Step 1: Append JSON-LD homepage block to seo.html**

In `themes/brownbaglunch/layouts/_partials/seo.html`, locate the `{{ if eq .Params.layout "speaker" }}` block added in Task 4. Change it to add an `{{ else if .IsHome }}` branch:

```html
{{ if eq .Params.layout "speaker" }}
  {{/* ... existing speaker block unchanged ... */}}
{{ else if .IsHome }}
  {{ $ldJson := dict
    "@context" "https://schema.org"
    "@type" "WebSite"
    "name" .Site.Title
    "url" .Site.BaseURL
    "description" $desc
    "potentialAction" (dict
      "@type" "SearchAction"
      "target" (dict
        "@type" "EntryPoint"
        "urlTemplate" (printf "%s?q={search_term_string}" (.Site.BaseURL | strings.TrimSuffix "/"))
      )
      "query-input" "required name=search_term_string"
    )
  }}
<script type="application/ld+json">{{ $ldJson | jsonify }}</script>
{{ end }}
```

The full JSON-LD section at the end of `seo.html` should be:

```html
{{/* ---- JSON-LD ---- */}}
{{ if eq .Params.layout "speaker" }}
  {{ $speaker := .Params }}
  {{ $coverSrc := partial "cover-url.html" . }}
  {{ $sameAs := slice }}
  {{ with $speaker.contacts.x }}
    {{ $sameAs = $sameAs | append (printf "https://x.com/%s" .) }}
  {{ end }}
  {{ range $speaker.websites }}
    {{ $sameAs = $sameAs | append .url }}
  {{ end }}
  {{ $ldJson := dict
    "@context" "https://schema.org"
    "@type" "Person"
    "name" (printf "%s %s" $speaker.firstname $speaker.lastname)
    "description" $desc
    "url" .Permalink
  }}
  {{ with $coverSrc }}
    {{ $ldJson = merge $ldJson (dict "image" .) }}
  {{ end }}
  {{ with $sameAs }}
    {{ $ldJson = merge $ldJson (dict "sameAs" .) }}
  {{ end }}
<script type="application/ld+json">{{ $ldJson | jsonify }}</script>
{{ else if .IsHome }}
  {{ $ldJson := dict
    "@context" "https://schema.org"
    "@type" "WebSite"
    "name" .Site.Title
    "url" .Site.BaseURL
    "description" $desc
    "potentialAction" (dict
      "@type" "SearchAction"
      "target" (dict
        "@type" "EntryPoint"
        "urlTemplate" (printf "%s?q={search_term_string}" (.Site.BaseURL | strings.TrimSuffix "/"))
      )
      "query-input" "required name=search_term_string"
    )
  }}
<script type="application/ld+json">{{ $ldJson | jsonify }}</script>
{{ end }}
```

- [ ] **Step 2: Build and verify JSON-LD on the homepage**

```bash
hugo --gc --minify && grep -A3 'application/ld+json' public/index.html
```
Expected: a `<script>` block containing `"@type":"WebSite"` and `"potentialAction"`.

- [ ] **Step 3: Commit**

```bash
git add themes/brownbaglunch/layouts/_partials/seo.html
git commit -m "✨ Add JSON-LD WebSite schema with SearchAction for homepage"
```

---

## Task 6: Create robots.txt

**Files:**
- Create: `static/robots.txt`

- [ ] **Step 1: Create static/robots.txt**

Create `static/robots.txt`:

```
User-agent: *
Allow: /

Sitemap: https://brownbaglunch.org/sitemap.xml
```

- [ ] **Step 2: Build and verify robots.txt is in the output**

```bash
hugo --gc --minify && cat public/robots.txt
```
Expected:
```
User-agent: *
Allow: /

Sitemap: https://brownbaglunch.org/sitemap.xml
```

- [ ] **Step 3: Verify sitemap.xml also exists**

```bash
ls public/sitemap.xml
```
Expected: file exists (Hugo generates it automatically).

- [ ] **Step 4: Commit**

```bash
git add static/robots.txt
git commit -m "🤖 Add robots.txt with sitemap reference"
```

---

## Post-Implementation Checklist

- [ ] Run a full build: `hugo --gc --minify && npx pagefind --site public`
- [ ] Check the homepage has: canonical, og:*, twitter:*, hreflang, JSON-LD WebSite
- [ ] Check a speaker page has: canonical, og:type=profile, JSON-LD Person
- [ ] Add `static/og-default.png` (1200×630 px) — not automated, must be done manually
- [ ] Submit updated sitemap to Google Search Console
