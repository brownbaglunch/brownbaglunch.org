# Speakers Alphabet Sub-Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the single huge speakers list with a stats overview at `/speakers/` and 26 letter sub-pages at `/speakers/a/` through `/speakers/z/`.

**Architecture:** Three new Hugo templates (`first-letter` normalizing partial, `alphabet-nav` partial, `letter.html` layout) plus 26 `_index.md` section files. The existing `list.html` is rewritten as a stats dashboard. All computation is server-side in Hugo templates — no JavaScript required.

**Tech Stack:** Hugo v0.157, Tailwind CSS (via existing theme), Go templates.

---

## File Map

| Action | Path | Responsibility |
|---|---|---|
| Create | `themes/brownbaglunch/layouts/_partials/first-letter.html` | Return normalized uppercase first letter of a name (accent → ASCII) |
| Create | `themes/brownbaglunch/layouts/_partials/alphabet-nav.html` | Render A-Z badge bar, active letter highlighted, empty letters grayed |
| Create ×26 | `content/speakers/{a..z}/_index.md` | Section pages for each letter; carry `letter` and `layout: letter` params |
| Create | `themes/brownbaglunch/layouts/speakers/letter.html` | List template for letter pages — filters speakers by first letter |
| Rewrite | `themes/brownbaglunch/layouts/speakers/list.html` | Stats dashboard: totals, top-10s, alphabet distribution, latest arrivals |

---

## Task 1 — `first-letter` normalizing partial

**Files:**
- Create: `themes/brownbaglunch/layouts/_partials/first-letter.html`

- [ ] **Step 1: Create the partial**

```html
{{/*
  Returns the normalized uppercase first letter of a speaker name.
  Maps French accented characters to their ASCII equivalents.
  @param . {string} Full speaker name (e.g. "Éric Dupont")
  @returns {string} Single uppercase letter (e.g. "E")
*/}}
{{ $first := substr . 0 1 | upper }}
{{ $first = replace $first "É" "E" }}
{{ $first = replace $first "È" "E" }}
{{ $first = replace $first "Ê" "E" }}
{{ $first = replace $first "Ë" "E" }}
{{ $first = replace $first "À" "A" }}
{{ $first = replace $first "Â" "A" }}
{{ $first = replace $first "Ä" "A" }}
{{ $first = replace $first "Ç" "C" }}
{{ $first = replace $first "Î" "I" }}
{{ $first = replace $first "Ï" "I" }}
{{ $first = replace $first "Ô" "O" }}
{{ $first = replace $first "Ö" "O" }}
{{ $first = replace $first "Ù" "U" }}
{{ $first = replace $first "Û" "U" }}
{{ $first = replace $first "Ü" "U" }}
{{ return $first }}
```

- [ ] **Step 2: Verify build succeeds**

```bash
hugo --quiet
```
Expected: exits 0, no errors mentioning `first-letter`.

- [ ] **Step 3: Commit**

```bash
git add themes/brownbaglunch/layouts/_partials/first-letter.html
git commit -m "✨ feat: add first-letter partial for accent-normalized speaker sorting"
```

---

## Task 2 — `alphabet-nav` partial

**Files:**
- Create: `themes/brownbaglunch/layouts/_partials/alphabet-nav.html`

- [ ] **Step 1: Create the partial**

```html
{{/*
  Renders an A–Z navigation bar for speaker pages.
  @param currentLetter {string} Active letter in UPPERCASE ("A", "B", …) or "" for none
  @param letterCounts  {map}    Map of uppercase letter → speaker count (e.g. dict "A" 3 "B" 1)
  @param showCounts    {bool}   When true, displays the count beneath each letter badge
*/}}
{{ $current    := .currentLetter | upper }}
{{ $counts     := .letterCounts }}
{{ $showCounts := .showCounts }}
{{ $letters    := slice "A" "B" "C" "D" "E" "F" "G" "H" "I" "J" "K" "L" "M" "N" "O" "P" "Q" "R" "S" "T" "U" "V" "W" "X" "Y" "Z" }}

<div class="flex gap-1 flex-wrap mb-2">
  {{ range $letters }}
    {{ $letter := . }}
    {{ $count  := default 0 (index $counts $letter) }}
    {{ $isActive := and (ne $current "") (eq $letter $current) }}
    {{ if gt $count 0 }}
      {{ if $isActive }}
        <span class="badge bg-terracotta text-white font-bold font-mono">{{ $letter }}</span>
      {{ else }}
        <a href="{{ printf "/speakers/%s/" ($letter | lower) | relURL }}"
           class="badge hover:bg-warm-brown hover:text-cream transition-colors font-mono">{{ $letter }}</a>
      {{ end }}
    {{ else }}
      <span class="badge opacity-30 cursor-default font-mono select-none">{{ $letter }}</span>
    {{ end }}
  {{ end }}
</div>

{{ if $showCounts }}
<div class="flex gap-1 flex-wrap mb-6 text-xs text-warm-brown/50 font-mono">
  {{ range $letters }}
    {{ $count := default 0 (index $counts .) }}
    <span class="w-[2.1rem] text-center">{{ $count }}</span>
  {{ end }}
</div>
{{ end }}
```

- [ ] **Step 2: Verify build**

```bash
hugo --quiet
```
Expected: exits 0.

- [ ] **Step 3: Commit**

```bash
git add themes/brownbaglunch/layouts/_partials/alphabet-nav.html
git commit -m "✨ feat: add alphabet-nav partial for speaker letter navigation"
```

---

## Task 3 — 26 letter `_index.md` content files

**Files:**
- Create ×26: `content/speakers/{a..z}/_index.md`

- [ ] **Step 1: Generate all 26 files with a shell loop**

```bash
for letter in {a..z}; do
  upper=$(echo "$letter" | tr '[:lower:]' '[:upper:]')
  mkdir -p "content/speakers/$letter"
  cat > "content/speakers/$letter/_index.md" << EOF
---
title: "Speakers — $upper"
letter: "$letter"
layout: "letter"
---
EOF
done
```

- [ ] **Step 2: Verify the files exist and have correct content**

```bash
cat content/speakers/a/_index.md
cat content/speakers/z/_index.md
```
Expected output for `a`:
```
---
title: "Speakers — A"
letter: "a"
layout: "letter"
---
```

- [ ] **Step 3: Verify Hugo can build (no template for `letter` yet — expect missing template warning, not a crash)**

```bash
hugo --quiet 2>&1 | head -20
```
Expected: build succeeds (exit 0); may warn about missing `letter` layout — that is resolved in Task 4.

- [ ] **Step 4: Commit**

```bash
git add content/speakers/
git commit -m "✨ feat: add _index.md section pages for each alphabet letter under speakers"
```

---

## Task 4 — Letter list template (`letter.html`)

**Files:**
- Create: `themes/brownbaglunch/layouts/speakers/letter.html`

- [ ] **Step 1: Create the template**

```html
{{ define "main" }}
{{ $allSpeakers := where site.RegularPages "Section" "speakers" }}
{{ $currentLetter := .Params.letter | upper }}

{{/* Build per-letter speaker counts for the nav bar */}}
{{ $letterCounts := dict }}
{{ range $allSpeakers }}
  {{ if .Params.name }}
    {{ $first := partial "first-letter.html" .Params.name }}
    {{ $count := add (default 0 (index $letterCounts $first)) 1 }}
    {{ $letterCounts = merge $letterCounts (dict $first $count) }}
  {{ end }}
{{ end }}

{{/* Filter speakers matching the current letter */}}
{{ $filtered := slice }}
{{ range $allSpeakers }}
  {{ if .Params.name }}
    {{ if eq (partial "first-letter.html" .Params.name) $currentLetter }}
      {{ $filtered = $filtered | append . }}
    {{ end }}
  {{ end }}
{{ end }}
{{ $filtered = sort $filtered "Params.name" }}

{{/* Render */}}
{{ partial "alphabet-nav.html" (dict "currentLetter" $currentLetter "letterCounts" $letterCounts "showCounts" false) }}

<div class="flex items-center justify-between mb-6">
  <h1 class="text-3xl font-black">Speakers — {{ $currentLetter }}</h1>
  <span class="text-warm-brown/60">
    {{ len $filtered }} speaker{{ if ne (len $filtered) 1 }}s{{ end }}
  </span>
</div>

{{ if $filtered }}
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    {{ range $filtered }}
      {{ partial "speaker-card.html" . }}
    {{ end }}
  </div>
{{ else }}
  <p class="text-warm-brown/60 text-center py-12">Aucun speaker pour cette lettre.</p>
{{ end }}
{{ end }}
```

- [ ] **Step 2: Build and verify `/speakers/a/` is generated**

```bash
hugo --quiet && ls public/speakers/a/
```
Expected: `index.html` present in `public/speakers/a/`.

- [ ] **Step 3: Spot-check speaker names on letter D page**

```bash
grep -i "david\|dimitri\|dridi\|duyhai" public/speakers/d/index.html | head -5
```
Expected: at least one name starting with "D" appears in the HTML.

- [ ] **Step 4: Verify a letter without speakers renders correctly**

Find a letter with no speakers (likely Q, W, X, Y…):
```bash
hugo --quiet && grep -l "Aucun speaker" public/speakers/*/index.html | head -3
```
Expected: at least one letter page shows the empty state message.

- [ ] **Step 5: Commit**

```bash
git add themes/brownbaglunch/layouts/speakers/letter.html
git commit -m "✨ feat: add letter.html template for alphabet speaker sub-pages"
```

---

## Task 5 — Rewrite speakers stats page (`list.html`)

**Files:**
- Rewrite: `themes/brownbaglunch/layouts/speakers/list.html`

- [ ] **Step 1: Rewrite the template**

```html
{{ define "main" }}
{{ $allSpeakers := where site.RegularPages "Section" "speakers" }}

{{/* ── Letter counts ── */}}
{{ $letterCounts := dict }}
{{ range $allSpeakers }}
  {{ if .Params.name }}
    {{ $first := partial "first-letter.html" .Params.name }}
    {{ $count := add (default 0 (index $letterCounts $first)) 1 }}
    {{ $letterCounts = merge $letterCounts (dict $first $count) }}
  {{ end }}
{{ end }}

{{/* ── Country counts — 1 per speaker per unique country ── */}}
{{ $countryCounts := dict }}
{{ range $allSpeakers }}
  {{ $seenCountries := slice }}
  {{ range .Params.cities }}
    {{ $parts   := split . "/" }}
    {{ $country := index $parts 0 }}
    {{ $city    := index $parts 1 }}
    {{ if and (ne $country "") (ne $country "*") (ne $city "*") (not (in $seenCountries $country)) }}
      {{ $seenCountries = $seenCountries | append $country }}
      {{ $n := add (default 0 (index $countryCounts $country)) 1 }}
      {{ $countryCounts = merge $countryCounts (dict $country $n) }}
    {{ end }}
  {{ end }}
{{ end }}
{{ $countryList := slice }}
{{ range $k, $v := $countryCounts }}
  {{ $countryList = $countryList | append (dict "name" $k "count" $v) }}
{{ end }}
{{ $countryList = sort $countryList "count" "desc" }}

{{/* ── City counts (exclude wildcards) ── */}}
{{ $cityCounts := dict }}
{{ range $allSpeakers }}
  {{ range .Params.cities }}
    {{ $parts := split . "/" }}
    {{ $city := index $parts 1 }}
    {{ if and (ne $city "") (ne $city "*") }}
      {{ $n := add (default 0 (index $cityCounts .)) 1 }}
      {{ $cityCounts = merge $cityCounts (dict . $n) }}
    {{ end }}
  {{ end }}
{{ end }}
{{ $cityList := slice }}
{{ range $k, $v := $cityCounts }}
  {{ $cityList = $cityList | append (dict "name" $k "count" $v) }}
{{ end }}
{{ $cityList = sort $cityList "count" "desc" }}

{{/* ── Tag counts ── */}}
{{ $tagCounts := dict }}
{{ range $allSpeakers }}
  {{ range .Params.sessions }}
    {{ range .tags }}
      {{ $n := add (default 0 (index $tagCounts .)) 1 }}
      {{ $tagCounts = merge $tagCounts (dict . $n) }}
    {{ end }}
  {{ end }}
{{ end }}
{{ $tagList := slice }}
{{ range $k, $v := $tagCounts }}
  {{ $tagList = $tagList | append (dict "name" $k "count" $v) }}
{{ end }}
{{ $tagList = sort $tagList "count" "desc" }}

{{/* ── Speakers available everywhere (wildcard city) ── */}}
{{ $worldwide := slice }}
{{ range $allSpeakers }}
  {{ $speaker := . }}
  {{ range .Params.cities }}
    {{ $parts := split . "/" }}
    {{ if eq (index $parts 1) "*" }}
      {{ $worldwide = $worldwide | append $speaker }}
      {{ break }}
    {{ end }}
  {{ end }}
{{ end }}
{{ $worldwide = sort $worldwide "Params.name" }}

{{/* ── Latest arrivals (top 5 by since date) ── */}}
{{ $withDate := where $allSpeakers "Params.since" "ne" nil }}
{{ $latest   := first 5 (sort $withDate "Params.since" "desc") }}

{{/* ══════════════════════ RENDER ══════════════════════ */}}

{{/* Header */}}
<div class="flex items-center justify-between mb-8">
  <h1 class="text-3xl font-black">Speakers</h1>
  <span class="text-5xl font-black text-terracotta">{{ len $allSpeakers }}</span>
</div>

{{/* Alphabet distribution + navigation */}}
<section class="mb-10 card">
  <h2 class="text-xl font-bold mb-4">Parcourir par lettre</h2>
  {{ partial "alphabet-nav.html" (dict "currentLetter" "" "letterCounts" $letterCounts "showCounts" true) }}
</section>

{{/* Top countries + Top cities side by side */}}
<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">

  {{/* Top 10 countries */}}
  <section class="card">
    <h2 class="text-xl font-bold mb-4">Top pays</h2>
    <ol class="space-y-2">
      {{ range first 10 $countryList }}
        <li class="flex items-center justify-between">
          <span class="font-mono text-sm uppercase">{{ .name }}</span>
          <span class="badge">{{ .count }}</span>
        </li>
      {{ end }}
    </ol>
  </section>

  {{/* Top 10 cities overall */}}
  <section class="card">
    <h2 class="text-xl font-bold mb-4">Top villes</h2>
    <ol class="space-y-2">
      {{ range first 10 $cityList }}
        {{ $parts := split .name "/" }}
        <li class="flex items-center justify-between">
          <span class="text-sm">
            {{ index $parts 1 | title }}
            <span class="text-warm-brown/50 text-xs">({{ index $parts 0 | upper }})</span>
          </span>
          <span class="badge">{{ .count }}</span>
        </li>
      {{ end }}
    </ol>
  </section>

</div>

{{/* Top 10 cities excluding #1 */}}
{{ if gt (len $cityList) 1 }}
<section class="card mb-10">
  <h2 class="text-xl font-bold mb-1">Top villes hors #1</h2>
  {{ with index $cityList 0 }}
    {{ $parts := split .name "/" }}
    <p class="text-sm text-warm-brown/50 mb-4">
      ({{ index $parts 1 | title }} mis de côté pour laisser la place aux autres)
    </p>
  {{ end }}
  <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
    {{ range first 10 (after 1 $cityList) }}
      {{ $parts := split .name "/" }}
      <div class="flex items-center justify-between px-2 py-1 rounded hover:bg-warm-light transition-colors">
        <span class="text-sm">
          {{ index $parts 1 | title }}
          <span class="text-warm-brown/50 text-xs">({{ index $parts 0 | upper }})</span>
        </span>
        <span class="badge">{{ .count }}</span>
      </div>
    {{ end }}
  </div>
</section>
{{ end }}

{{/* Top 10 tags */}}
<section class="card mb-10">
  <h2 class="text-xl font-bold mb-4">Top sujets</h2>
  <div class="flex flex-wrap gap-2">
    {{ range first 10 $tagList }}
      <a href="{{ printf "/talks/%s/" .name | relURL }}"
         class="badge hover:bg-terracotta hover:text-white transition-colors">
        #{{ .name }}
        <span class="ml-1 opacity-60">{{ .count }}</span>
      </a>
    {{ end }}
  </div>
</section>

{{/* Speakers available everywhere */}}
{{ if $worldwide }}
<section class="card mb-10">
  <h2 class="text-xl font-bold mb-4">
    🌍 Disponibles partout
    <span class="text-warm-brown/50 text-base font-normal">({{ len $worldwide }})</span>
  </h2>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    {{ range $worldwide }}
      {{ partial "speaker-card.html" . }}
    {{ end }}
  </div>
</section>
{{ end }}

{{/* Latest arrivals */}}
{{ if $latest }}
<section class="card mb-10">
  <h2 class="text-xl font-bold mb-4">Derniers arrivés</h2>
  <div class="space-y-3">
    {{ range $latest }}
      <div class="flex items-center gap-3">
        {{ if .Params.picture }}
          <img src="{{ .Params.picture }}" alt="{{ .Params.name }}"
               class="w-10 h-10 rounded-full object-cover border-2 border-warm-border shrink-0">
        {{ end }}
        <div class="flex-1">
          <a href="{{ .RelPermalink }}" class="font-semibold hover:text-terracotta transition-colors">
            {{ .Params.name }}
          </a>
        </div>
        <span class="text-sm text-warm-brown/50 shrink-0">{{ .Params.since }}</span>
      </div>
    {{ end }}
  </div>
</section>
{{ end }}

{{ end }}
```

- [ ] **Step 2: Verify the stats page builds correctly**

```bash
hugo --quiet && ls public/speakers/index.html
```
Expected: file exists, exit 0.

- [ ] **Step 3: Check the total speaker count appears in the HTML**

```bash
grep -c "speaker-card\|card flex gap" public/speakers/index.html || true
grep "text-5xl" public/speakers/index.html | head -3
```
Expected: the large number (total speakers) appears somewhere in the stats page HTML.

- [ ] **Step 4: Verify letter sub-pages are still intact**

```bash
ls public/speakers/a/index.html public/speakers/z/index.html
```
Expected: both files exist.

- [ ] **Step 5: Commit**

```bash
git add themes/brownbaglunch/layouts/speakers/list.html
git commit -m "✨ feat: rewrite speakers list as stats dashboard with alphabet navigation"
```

---

## Task 6 — Final build verification

- [ ] **Step 1: Full production build**

```bash
npm run build 2>&1 | tail -20
```
Expected: exits 0. Hugo build + Pagefind index both complete without errors.

- [ ] **Step 2: Verify URL coverage**

```bash
for l in a b c d e f g h i j k l m n o p q r s t u v w x y z; do
  [ -f "public/speakers/$l/index.html" ] && echo "OK $l" || echo "MISSING $l"
done
```
Expected: all 26 print `OK`.

- [ ] **Step 3: Spot-check accent handling — find a speaker with an accented first name**

```bash
grep -r "Éric\|Émilien\|Ágnes\|Cédric" content/speakers/ | head -5
```
Then verify the speaker appears on the correct letter page (É → E):
```bash
grep -i "emilien\|cedric\|eric" public/speakers/e/index.html | head -3
grep -i "emilien\|cedric\|eric" public/speakers/c/index.html | head -3
```
Expected: accented-initial speakers appear under the ASCII equivalent letter.

- [ ] **Step 4: Verify navigation links are present on a letter page**

```bash
grep 'href="/speakers/b/"' public/speakers/a/index.html | head -2
```
Expected: link to `/speakers/b/` present in the A page nav bar.

- [ ] **Step 5: Final commit if any fixes were applied**

If any corrections were made during verification:
```bash
git add -p
git commit -m "🐛 fix: correct accent normalization / nav link issues in speaker alphabet pages"
```
