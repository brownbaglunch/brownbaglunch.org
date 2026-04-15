# Design: Split `name` into `firstname` + `lastname`

## Goal

Replace the single `name:` front matter field on speaker profiles with two fields `firstname:` and `lastname:`, update all Hugo templates to use them, and sort speakers by last name instead of first name.

## Content Migration

A one-off Python script (`scripts/migrate_names.py`) processes every `content/speakers/**/_index.md`:

1. Reads the YAML front matter
2. Extracts `name:`
3. Splits into `firstname` / `lastname` using two-pass logic:
   - **Hardcoded cases** (ambiguous names resolved during analysis):
     - `Augustin De Laveaucoupet` → `Augustin` / `De Laveaucoupet`
     - `David De Carvalho` → `David` / `De Carvalho`
     - `Jean-François Le Foll` → `Jean-François` / `Le Foll`
     - `Marine Corbelin Laporte` → `Marine` / `Corbelin Laporte`
     - `Nicolas De Loof` → `Nicolas` / `De Loof`
     - `Xavier F. Gouchet` → `Xavier` / `F. Gouchet`
   - **General rule**: last token = `lastname`, everything else = `firstname`
4. Replaces `name:` with `firstname:` and `lastname:` (in that order)
5. Supports a `--dry-run` flag for pre-flight verification

## Template Updates

### Filtering

All speaker existence checks switch from `name` to `lastname`:

```
"Params.name" "ne" nil  →  "Params.lastname" "ne" nil
```

### Sorting

Speakers are now sorted by last name everywhere:

```
sort $filtered "Params.name"  →  sort $filtered "Params.lastname"
```

### Alphabet navigation

The `first-letter.html` partial now receives `lastname` instead of `name`, so the alphabet nav groups and filters by the first letter of the last name.

### Display

The full name is rendered as `Firstname **F**irstletterLastname` — only the first letter of the last name is bold:

```html
{{ $speaker.firstname }} <strong>{{ substr $speaker.lastname 0 1 }}</strong>{{ substr $speaker.lastname 1 }}
```

Example: `David **P**ilato`

### Files to update

| File | Changes |
|---|---|
| `speakers/list.html` | filter, letter grouping, display |
| `speakers/letter.html` | filter, sort, letter grouping |
| `speakers/speaker.html` | display |
| `speakers/talk.html` | display |
| `_partials/speaker-card.html` | display |
| `cities/list.html` | filter, sort, display |
| `talks/list.html` | display |
| `tags/term.html` | display |
| `home.html` | filter |
| `index.html` | filter |
| `_partials/speakers-for-city.html` | filter |

## Sequencing

1. Run `scripts/migrate_names.py --dry-run` and verify all splits visually
2. Run `scripts/migrate_names.py` to migrate the ~250 content files
3. Update all templates
4. Run `hugo --gc --minify` to verify no build errors
5. Commit everything in **a single commit**

## Rollback

Standard `git revert` on the single commit covers both content and templates.
