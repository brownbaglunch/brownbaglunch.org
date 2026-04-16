# Hero Gallery — Design Spec

**Date:** 2026-04-16
**Status:** Approved

## Goal

Display authentic BBL community photos as an auto-rotating background in the homepage hero section, styled with a warm sepia/brown CSS filter to match the site's color palette. Adding a new photo to the gallery directory must automatically include it in the rotation at the next build — no template changes required.

## Decisions

| Topic | Decision |
|---|---|
| Placement | Full-width hero background |
| Rotation | CSS-only, no JavaScript |
| Filter | `sepia(1) brightness(0.8) contrast(1.1)` + dark overlay `rgba(61,43,31,0.50)` |
| Overlay | `bg-warm-brown/50` div layered above the images |
| Timing | 5 seconds per photo |
| Transition | Cross-fade via `@keyframes bbl-crossfade` |
| Auto-discovery | `resources.Match "gallery/*"` in Hugo template |
| Image directory | `assets/gallery/` |
| Fallback | First image visible statically if CSS is disabled |

## Directory Structure

```
assets/
  gallery/
    2013-03-15-sg-mathilde.jpg
    2013-03-24-sg-tugdual.jpg
    2013-03-24-x-david.jpg
    (any future .jpg/.png added here will appear automatically)
```

Note: The `IGNORE_ME/` directory at repo root is kept as-is. The 3 photos are copied (not moved) to `assets/gallery/`.

## Hero Layout

The existing hero `<section>` gains:
- `relative overflow-hidden` and a minimum height (e.g. `min-h-[380px]`)
- A background layer (`absolute inset-0`) containing all `<img>` tags stacked on top of each other
- A dark overlay div (`absolute inset-0 bg-warm-brown/50`) above the photos
- The existing content (title, subtitle, search bar) wrapped in `relative z-10`

Simplified markup structure:

```html
<section class="relative overflow-hidden min-h-[380px] py-16 text-center">
  <!-- Background photos -->
  <div class="absolute inset-0">
    {{ range $i, $img := $images }}
    <img src="{{ $img.RelPermalink }}"
         alt="Session Brown Bag Lunch"
         class="bbl-photo absolute inset-0 w-full h-full object-cover"
         style="animation-delay:{{ mul $i 5 }}s"
         loading="{{ if eq $i 0 }}eager{{ else }}lazy{{ end }}">
    {{ end }}
    <div class="absolute inset-0 bg-warm-brown/50"></div>
  </div>
  <!-- Content -->
  <div class="relative z-10">
    ... existing title, subtitle, search bar ...
  </div>
</section>
```

## CSS Animation

The keyframe percentages depend on N (number of images), so Hugo generates a `<style>` block inline in `home.html` using the computed values. This ensures the animation is always correct regardless of how many images are in `assets/gallery/`.

Hugo template logic (in `home.html`, before the section):

```go-template
{{ $n     := len $images }}
{{ $dur   := 5 }}
{{ $total := mul $n $dur }}
{{/* 1s fade expressed as % of total cycle */}}
{{ $fadeP := div 100.0 (float $total) }}
{{/* each image's slot as % of total cycle */}}
{{ $slotP := div 100.0 (float $n) }}
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
```

For 3 images × 5s = 15s total, this produces:
- `fadeP` = 6.67% (~1s), `slotP` = 33.33%
- Keyframe: 0% → 6.67% → 26.67% → 33.33% → 100%

The `animation-delay` for image `i` is `i × 5s` (set via inline `style`):
- Image 0: starts immediately
- Image 1: starts at 5s
- Image 2: starts at 10s

## Text legibility

With the CSS filter + the `bg-warm-brown/50` overlay, all text uses `color: white` with `text-shadow` for additional contrast. The search bar keeps its white background and dark text — no change needed.

## Out of Scope

- Pause on hover (requires JS — not included)
- Manual navigation (arrows/dots — not included)
- Image processing/resizing via Hugo Pipes (originals are served as-is)
- Changes to other pages
