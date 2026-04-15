# Home Page Search Bar — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the two CTA buttons on the home page with a large search bar, and hide the nav search bar on the home page only.

**Architecture:** The existing Pagefind JS (`search.html`) binds to `#search-container`, `#search-input`, and `#search-panel` by ID. Since these IDs are never present together in the DOM (nav renders them on all pages except home; home renders them only on the home page), the JS requires zero modification. Two template files change: `nav.html` gets a conditional guard, `home.html` replaces its CTA buttons with a styled search bar using the same IDs.

**Tech Stack:** Hugo templates, Tailwind CSS

---

## File Map

**Modified:**
- `themes/brownbaglunch/layouts/_partials/nav.html` — conditionally hide search on home page
- `themes/brownbaglunch/layouts/home.html` — replace CTA buttons with large search bar

---

### Task 1: Hide nav search on the home page

**Files:**
- Modify: `themes/brownbaglunch/layouts/_partials/nav.html:37-48`

- [ ] **Step 1: Read the current nav search block**

Open `themes/brownbaglunch/layouts/_partials/nav.html`. The search block starts at the comment `{{/* Search — section drives default filter preset */}}` and ends at the closing `</div>` of `#search-container` (line ~48).

- [ ] **Step 2: Wrap the search block with an IsHome guard**

Replace this block (lines 31–48):
```html
    {{/* Search — section drives default filter preset */}}
    {{ $searchSection := "all" }}
    {{ if eq .Section "speakers" }}{{ $searchSection = "speakers" }}
    {{ else if or (eq .Type "tags") (eq .Section "talks") }}{{ $searchSection = "talks" }}
    {{ else if eq .Section "cities" }}{{ $searchSection = "cities" }}
    {{ end }}
    <div class="ml-auto w-64 relative" id="search-container" data-section="{{ $searchSection }}">
      <div class="relative">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-cream/50 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <input type="search" id="search-input"
               autocomplete="off" spellcheck="false"
               placeholder="{{ i18n "search_placeholder" }}"
               class="w-full bg-cream/20 text-cream placeholder:text-cream/50 border border-cream/30 rounded-full pl-9 pr-3 py-1.5 text-sm outline-none focus:bg-cream/30 focus:border-cream/50 transition-colors">
      </div>
      <div id="search-panel" class="hidden absolute right-0 top-full mt-2 w-[32rem] max-w-[calc(100vw-1rem)] max-h-[80vh] overflow-y-auto bg-cream text-warm-brown border border-warm-border rounded-xl shadow-xl z-[100] p-4"></div>
    </div>
```

With:
```html
    {{/* Search — section drives default filter preset. Hidden on home page (home has its own search bar). */}}
    {{ if not .IsHome }}
    {{ $searchSection := "all" }}
    {{ if eq .Section "speakers" }}{{ $searchSection = "speakers" }}
    {{ else if or (eq .Type "tags") (eq .Section "talks") }}{{ $searchSection = "talks" }}
    {{ else if eq .Section "cities" }}{{ $searchSection = "cities" }}
    {{ end }}
    <div class="ml-auto w-64 relative" id="search-container" data-section="{{ $searchSection }}">
      <div class="relative">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-cream/50 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <input type="search" id="search-input"
               autocomplete="off" spellcheck="false"
               placeholder="{{ i18n "search_placeholder" }}"
               class="w-full bg-cream/20 text-cream placeholder:text-cream/50 border border-cream/30 rounded-full pl-9 pr-3 py-1.5 text-sm outline-none focus:bg-cream/30 focus:border-cream/50 transition-colors">
      </div>
      <div id="search-panel" class="hidden absolute right-0 top-full mt-2 w-[32rem] max-w-[calc(100vw-1rem)] max-h-[80vh] overflow-y-auto bg-cream text-warm-brown border border-warm-border rounded-xl shadow-xl z-[100] p-4"></div>
    </div>
    {{ end }}
```

- [ ] **Step 3: Build and verify**

```bash
hugo --gc --minify 2>&1 | tail -3
```

Expected: 0 errors.

- [ ] **Step 4: Commit**

```bash
git add themes/brownbaglunch/layouts/_partials/nav.html
git commit -m "🔧 fix: hide nav search bar on home page"
```

---

### Task 2: Add large search bar to home page

**Files:**
- Modify: `themes/brownbaglunch/layouts/home.html:10-17`

- [ ] **Step 1: Read the current CTA block**

Open `themes/brownbaglunch/layouts/home.html`. The block to replace is:
```html
  <div class="flex gap-4 justify-center flex-wrap">
    <a href="{{ "/speakers/" | relLangURL }}" class="btn-primary text-lg px-6 py-3">
      {{ i18n "home_cta_speakers" }}
    </a>
    <a href="{{ "/talks/" | relLangURL }}" class="border-2 border-terracotta text-terracotta px-6 py-3 rounded-full font-semibold hover:bg-terracotta hover:text-white transition-colors">
      {{ i18n "home_cta_talks" }}
    </a>
  </div>
```

- [ ] **Step 2: Replace CTA buttons with large search bar**

Replace the block above with:
```html
  <div class="mt-8 max-w-xl mx-auto relative" id="search-container" data-section="all">
    <div class="relative">
      <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-warm-brown/40 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
      </svg>
      <input type="search" id="search-input"
             autocomplete="off" spellcheck="false"
             placeholder="{{ i18n "search_placeholder" }}"
             class="w-full bg-white text-warm-brown placeholder:text-warm-brown/40 border-2 border-warm-border rounded-full pl-12 pr-4 py-3 text-base outline-none focus:border-terracotta transition-colors shadow-sm">
    </div>
    <div id="search-panel" class="hidden absolute left-0 right-0 top-full mt-2 max-h-[80vh] overflow-y-auto bg-cream text-warm-brown border border-warm-border rounded-xl shadow-xl z-[100] p-4"></div>
  </div>
```

- [ ] **Step 3: Build and verify**

```bash
hugo --gc --minify 2>&1 | tail -3
```

Expected: 0 errors.

- [ ] **Step 4: Start dev server and verify visually**

```bash
hugo server
```

Navigate to `http://localhost:1313`:
- Home page: large search bar visible, no CTA buttons, no search in nav
- Any other page (e.g. `/speakers/`): nav search visible as before
- Type in home search bar: dropdown results appear below the bar
- Navigate to `/speakers/` and type in nav search: works as before

- [ ] **Step 5: Commit**

```bash
git add themes/brownbaglunch/layouts/home.html
git commit -m "✨ feat: replace home page CTA buttons with large search bar"
```
