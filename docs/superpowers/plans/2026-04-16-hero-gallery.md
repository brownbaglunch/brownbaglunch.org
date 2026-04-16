# Hero Gallery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an auto-rotating, CSS-only photo background to the homepage hero section, with images auto-discovered from `assets/gallery/` and styled with a warm sepia/brown filter.

**Architecture:** Images live in `assets/gallery/` and are discovered at build time via Hugo's `resources.Match`. Hugo generates an inline `<style>` block with a `@keyframes bbl-crossfade` animation whose percentages are computed from the image count. Each `<img>` receives a CSS `animation-delay` to offset its entry in the cycle. No JavaScript.

**Tech Stack:** Hugo templates (Go template syntax), Tailwind CSS utility classes, CSS `@keyframes` animation, Hugo `resources.Match`

---

### Task 1: Copy photos to assets/gallery/

**Files:**
- Create: `assets/gallery/2013-03-15-sg-mathilde.jpg`
- Create: `assets/gallery/2013-03-24-sg-tugdual.jpg`
- Create: `assets/gallery/2013-03-24-x-david.jpg`

- [ ] **Step 1: Create the directory and copy the images**

```bash
mkdir -p assets/gallery
cp IGNORE_ME/2013-03-15-sg-mathilde.jpg assets/gallery/
cp IGNORE_ME/2013-03-24-sg-tugdual.jpg assets/gallery/
cp IGNORE_ME/2013-03-24-x-david.jpg assets/gallery/
```

- [ ] **Step 2: Verify Hugo discovers them**

```bash
hugo --gc --minify 2>&1 | grep -i error || echo "Build OK"
ls public/gallery/
```

Expected: no errors, 3 `.jpg` files listed in `public/gallery/`.

- [ ] **Step 3: Commit**

```bash
git add assets/gallery/
git commit -m "✨ feat: add BBL community photos to gallery"
```

---

### Task 2: Rewrite the hero section in home.html

**Files:**
- Modify: `themes/brownbaglunch/layouts/home.html`

The entire `home.html` is replaced. The key changes:
- Add `resources.Match` at top to load gallery images
- Inject a `<style>` block with a dynamically computed `@keyframes bbl-crossfade`
- Make the hero `<section>` `relative overflow-hidden min-h-[380px]`
- Add an `absolute inset-0` background layer with stacked `<img>` tags + dark overlay
- Wrap all existing hero content in `relative z-10`
- Change heading/paragraph text from `text-warm-brown` to `text-white` (only when images exist — graceful fallback if `assets/gallery/` is empty)

- [ ] **Step 1: Replace home.html with the new version**

Replace the entire contents of `themes/brownbaglunch/layouts/home.html` with:

```html
{{ define "main" }}
{{ $srcPages := site.Pages }}
{{ $images := resources.Match "gallery/*" }}
{{ $n := len $images }}
{{ $dur := 5 }}
{{ $total := mul $n $dur }}
<div data-pagefind-ignore>
{{ if $images }}
{{ $fadeP := div 100.0 $total }}
{{ $slotP := div 100.0 $n }}
<style>
.bbl-photo {
  filter: sepia(1) brightness(0.8) contrast(1.1);
  opacity: 0;
  animation-name: bbl-crossfade;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
  animation-duration: {{ $total }}s;
}
@keyframes bbl-crossfade {
  0%                                        { opacity: 0; }
  {{ printf "%.2f" $fadeP }}%               { opacity: 1; }
  {{ printf "%.2f" (sub $slotP $fadeP) }}%  { opacity: 1; }
  {{ printf "%.2f" $slotP }}%               { opacity: 0; }
  100%                                      { opacity: 0; }
}
</style>
{{ end }}
<section class="py-16 text-center{{ if $images }} relative overflow-hidden min-h-[380px]{{ end }}">
  {{ if $images }}
  <div class="absolute inset-0">
    {{ range $i, $img := $images }}
    <img src="{{ $img.RelPermalink }}"
         alt="Session Brown Bag Lunch"
         class="bbl-photo absolute inset-0 w-full h-full object-cover"
         style="animation-delay:{{ mul $i $dur }}s"
         loading="{{ if eq $i 0 }}eager{{ else }}lazy{{ end }}">
    {{ end }}
    <div class="absolute inset-0 bg-warm-brown/50"></div>
  </div>
  {{ end }}
  <div class="{{ if $images }}relative z-10{{ end }}">
    <h1 class="text-5xl font-black {{ if $images }}text-white{{ else }}text-warm-brown{{ end }} mb-4 leading-tight">
      {{ i18n "home_tagline" | safeHTML }}
    </h1>
    <p class="text-xl {{ if $images }}text-white/80{{ else }}text-warm-brown/70{{ end }} mb-4 max-w-xl mx-auto">
      {{ i18n "home_description" | safeHTML }}
    </p>
    <div class="flex justify-center mb-8">
      {{ partial "github-edit-link.html" "https://github.com/brownbaglunch/brownbaglunch.org" }}
    </div>
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
  </div>
</section>

<section class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
  {{ $speakerCount := len (where (where (where $srcPages "Kind" "section") "Section" "speakers") "Params.lastname" "ne" nil) }}
  {{ $cityCount := len (where (where $srcPages "Section" "cities") "Params.city" "ne" nil) }}
  {{ $talkCount := len (where site.RegularPages "Section" "speakers") }}
  <a href="{{ "/speakers/" | relLangURL }}" class="card hover:border-terracotta transition-colors group">
    <div class="text-4xl font-black text-terracotta group-hover:text-orange-600">{{ $speakerCount }}</div>
    <div class="text-warm-brown/70 mt-1">{{ i18n "home_stat_speakers" }}</div>
  </a>
  <a href="{{ "/talks/" | relLangURL }}" class="card hover:border-terracotta transition-colors group">
    <div class="text-4xl font-black text-terracotta group-hover:text-orange-600">{{ $talkCount }}</div>
    <div class="text-warm-brown/70 mt-1">{{ i18n "home_stat_topics" }}</div>
  </a>
  <a href="{{ "/cities/" | relLangURL }}" class="card hover:border-terracotta transition-colors group">
    <div class="text-4xl font-black text-terracotta group-hover:text-orange-600">{{ $cityCount }}</div>
    <div class="text-warm-brown/70 mt-1">{{ i18n "home_stat_cities" }}</div>
  </a>
</section>

<section class="mt-16">
  <h2 class="text-2xl font-bold mb-6">{{ i18n "home_how_title" }}</h2>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <div class="card">
      <div class="text-3xl mb-3">🔍</div>
      <h3 class="font-bold text-lg mb-2">{{ i18n "home_step1_title" }}</h3>
      <p class="text-warm-brown/70">{{ i18n "home_step1_desc" }}</p>
    </div>
    <div class="card">
      <div class="text-3xl mb-3">📧</div>
      <h3 class="font-bold text-lg mb-2">{{ i18n "home_step2_title" }}</h3>
      <p class="text-warm-brown/70">{{ i18n "home_step2_desc" }}</p>
    </div>
    <div class="card">
      <div class="text-3xl mb-3">🍕</div>
      <h3 class="font-bold text-lg mb-2">{{ i18n "home_step3_title" }}</h3>
      <p class="text-warm-brown/70">{{ i18n "home_step3_desc" }}</p>
    </div>
  </div>
</section>

<section class="mt-16">
  <h2 class="text-2xl font-bold mb-6">💬 {{ i18n "home_press_title" }}</h2>
  <ul class="space-y-1 text-sm">
    {{ range sort site.Data.press "date" "desc" }}<li><span class="text-warm-brown/40 tabular-nums">{{ .date }}</span> · <a href="{{ .url }}" target="_blank" rel="noopener noreferrer" class="text-terracotta hover:underline">{{ .title }}</a> · <span class="text-warm-brown/60">{{ .author }}</span></li>
    {{ end }}
  </ul>
</section>
</div>{{/* end data-pagefind-ignore */}}
{{ end }}
```

- [ ] **Step 2: Verify the build succeeds**

```bash
hugo --gc --minify 2>&1 | grep -i error || echo "Build OK"
```

Expected: `Build OK` — no template errors, no missing resource warnings.

- [ ] **Step 3: Start dev server and visually inspect**

```bash
hugo server
```

Open http://localhost:1313 and verify:
- The hero shows one of the 3 BBL photos as a full-width background
- The photo has a warm sepia/brown tint
- Title and subtitle are white and legible
- The search bar has its white background, fully readable
- After 5 seconds, the photo cross-fades to the next one
- After 15 seconds total, the cycle restarts from the first photo
- Removing the `assets/gallery/` images and restarting the server shows the hero falling back gracefully to a plain `text-warm-brown` layout (no broken CSS)

- [ ] **Step 4: Commit**

```bash
git add themes/brownbaglunch/layouts/home.html
git commit -m "✨ feat: add auto-rotating hero photo background with sepia filter"
```
