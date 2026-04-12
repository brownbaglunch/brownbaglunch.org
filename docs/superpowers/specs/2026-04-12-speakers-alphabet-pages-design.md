# Design: Speakers Alphabet Sub-Pages + Stats Overview

**Date:** 2026-04-12  
**Status:** Approved

---

## Overview

Replace the current `/speakers/` list page (all speakers in one big page) with:

1. A **stats overview page** at `/speakers/` — surfacing key metrics about the speaker community.
2. **26 sub-pages** at `/speakers/a/` through `/speakers/z/` — each listing speakers whose `name` starts with that letter.

---

## Architecture

### 1. Stats Overview Page — `/speakers/`

**Template:** `themes/brownbaglunch/layouts/speakers/list.html` (rewritten)

**Stats displayed:**

| Stat | Source field | Notes |
|---|---|---|
| Total speakers | `site.RegularPages` filtered by section `speakers` | |
| Top 10 countries | First segment of `cities` (`fr/paris` → `fr`) | Sorted by count desc |
| Top 10 cities overall | Full `cities` value, excluding `*/` wildcards | Sorted by count desc |
| Top 10 cities excluding #1 | Same, drop the top city | Avoids Paris dominating |
| Top 10 tags | All `sessions[].tags` across all speakers | Sorted by count desc |
| Alphabetical distribution | First letter of `name`, A–Z | Each letter links to `/speakers/{letter}/`; letters with 0 speakers are grayed |
| Speakers available everywhere | Speakers with at least one city matching `*/*` or `{country}/*` | |
| Latest arrivals | Top 5 speakers sorted by `since` desc | Shows photo + name + date |

The alphabetical distribution row serves as the primary navigation entry point to the letter sub-pages.

**All computations are done in Hugo templates — no JavaScript required.**

### 2. Letter Sub-Pages — `/speakers/{letter}/`

**Content files:** `content/speakers/{a..z}/_index.md` (26 files)

Each file contains:
```yaml
---
title: "Speakers — A"
letter: "a"
layout: "letter"
---
```

**Template:** `themes/brownbaglunch/layouts/speakers/letter.html`

Logic:
1. Retrieve all speakers: `where site.RegularPages "Section" "speakers"`
2. Get current letter from `$.Params.letter | upper`
3. For each speaker, normalize first char of `name`: map accented chars (`É→E`, `À→A`, `Ç→C`, etc.) then compare to current letter
4. Display matching speakers using existing `speaker-card.html` partial, sorted by `name`
5. Show speaker count for the letter

**Accented character normalization map** (applied in template):
```
É È Ê Ë → E
À Â Ä → A
Ç → C
Î Ï → I
Ô Ö → O
Ù Û Ü → U
```

### 3. Alphabet Navigation Bar (partial)

A new partial `themes/brownbaglunch/layouts/_partials/alphabet-nav.html`:
- Renders A–Z as badges
- Each letter: link to `/speakers/{letter}/` if at least one speaker exists, grayed span otherwise
- Active letter (current page) gets a highlighted style (e.g., `bg-terracotta text-white`)
- Accepts `currentLetter` and `speakersByLetter` (a map of letter → count) as context

This partial is used on:
- Each letter page (`letter.html`) — with the current letter highlighted
- The stats overview page (`list.html`) — without any active letter, counts shown below each letter

---

## Data Flow

```
site.RegularPages (section: speakers)
  │
  ├─► list.html (stats page)
  │     ├── total count
  │     ├── group by country → top 10
  │     ├── group by city → top 10 / top 10 excl. #1
  │     ├── flatten all session tags → top 10
  │     ├── filter cities with wildcard → available everywhere
  │     ├── sort by .Params.since desc → latest 5
  │     └── group by first letter → alphabet bar (links)
  │
  └─► letter.html (one per letter)
        ├── filter by normalized first letter
        └── render speaker-card.html for each match
```

---

## File Changes Summary

| Action | Path |
|---|---|
| Rewrite | `themes/brownbaglunch/layouts/speakers/list.html` |
| Create | `themes/brownbaglunch/layouts/speakers/letter.html` |
| Create | `themes/brownbaglunch/layouts/_partials/alphabet-nav.html` |
| Create (×26) | `content/speakers/{a..z}/_index.md` |

No existing speaker content files are modified.

---

## Edge Cases

- **Letter with no speakers:** page still exists, shows "Aucun speaker pour cette lettre", letter is grayed in nav.
- **Speaker with no `name`:** skipped silently (defensive check in template).
- **Cities with wildcard `*`:** excluded from city ranking; counted separately in "available everywhere" stat.
- **`since` field absent:** speaker excluded from "latest arrivals" only.
