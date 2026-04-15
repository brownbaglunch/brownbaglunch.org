# Firstname/Lastname Speaker Field Split — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace `name:` with `firstname:` + `lastname:` in all speaker content files, update all Hugo templates to display and sort by last name, in a single atomic commit.

**Architecture:** A Python migration script handles the content files using hardcoded overrides for the 6 ambiguous names and a default last-token rule for all others. Templates are then updated to filter/sort on `lastname`, group the alphabet nav by the first letter of `lastname`, and render `Firstname **L**astname`.

**Tech Stack:** Python 3 (stdlib only), Hugo templates

---

## File Map

**Created:**
- `scripts/migrate_names.py` — one-off migration script

**Modified (content):**
- `content/speakers/**/_index.md` (~250 files) — `name:` → `firstname:` + `lastname:`

**Modified (templates):**
- `themes/brownbaglunch/layouts/home.html` — filter
- `themes/brownbaglunch/layouts/index.html` — filter
- `themes/brownbaglunch/layouts/speakers/list.html` — filter, letter nav, display
- `themes/brownbaglunch/layouts/speakers/letter.html` — filter, sort, letter nav
- `themes/brownbaglunch/layouts/speakers/speaker.html` — display
- `themes/brownbaglunch/layouts/speakers/talk.html` — display
- `themes/brownbaglunch/layouts/_partials/speaker-card.html` — display
- `themes/brownbaglunch/layouts/_partials/speakers-for-city.html` — filter
- `themes/brownbaglunch/layouts/cities/list.html` — filter, sort, display
- `themes/brownbaglunch/layouts/talks/list.html` — display
- `themes/brownbaglunch/layouts/tags/term.html` — display

---

### Task 1: Write and run the migration script

**Files:**
- Create: `scripts/migrate_names.py`

- [ ] **Step 1: Create the script**

```python
#!/usr/bin/env python3
"""Migrate speaker name: field to firstname: + lastname:

Usage:
    python scripts/migrate_names.py --dry-run   # preview only
    python scripts/migrate_names.py             # apply changes
"""

import re
import sys
from pathlib import Path

OVERRIDES = {
    "Augustin De Laveaucoupet": ("Augustin", "De Laveaucoupet"),
    "David De Carvalho": ("David", "De Carvalho"),
    "Jean-François Le Foll": ("Jean-François", "Le Foll"),
    "Jean-françois Le Foll": ("Jean-François", "Le Foll"),
    "Marine Corbelin Laporte": ("Marine", "Corbelin Laporte"),
    "Nicolas De Loof": ("Nicolas", "De Loof"),
    "Xavier F. Gouchet": ("Xavier", "F. Gouchet"),
}


def split_name(name: str) -> tuple[str, str]:
    if name in OVERRIDES:
        return OVERRIDES[name]
    tokens = name.split()
    if len(tokens) == 1:
        return (name, name)
    return (" ".join(tokens[:-1]), tokens[-1])


def migrate_file(path: Path, dry_run: bool) -> bool:
    content = path.read_text(encoding="utf-8")
    match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    if not match:
        return False

    name = match.group(1).strip()
    firstname, lastname = split_name(name)
    replacement = f"firstname: {firstname}\nlastname: {lastname}"
    new_content = content[:match.start()] + replacement + content[match.end():]

    if dry_run:
        print(f"  {name!r:50s} → {firstname!r} / {lastname!r}")
        return True

    path.write_text(new_content, encoding="utf-8")
    return True


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    speakers_dir = Path("content/speakers")

    if not speakers_dir.exists():
        print("ERROR: Run from repo root (content/speakers/ not found)", file=sys.stderr)
        sys.exit(1)

    count = 0
    for index_file in sorted(speakers_dir.glob("*/*/_index.md")):
        if migrate_file(index_file, dry_run):
            count += 1

    mode = "DRY RUN" if dry_run else "MIGRATED"
    print(f"\n[{mode}] {count} speaker files processed")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run dry-run and verify all splits**

```bash
python scripts/migrate_names.py --dry-run
```

Expected: ~250 lines. Verify the 6 ambiguous cases appear correctly:
```
'Augustin De Laveaucoupet'    → 'Augustin' / 'De Laveaucoupet'
'David De Carvalho'           → 'David' / 'De Carvalho'
'Jean-François Le Foll'       → 'Jean-François' / 'Le Foll'
'Marine Corbelin Laporte'     → 'Marine' / 'Corbelin Laporte'
'Nicolas De Loof'             → 'Nicolas' / 'De Loof'
'Xavier F. Gouchet'           → 'Xavier' / 'F. Gouchet'
```

- [ ] **Step 3: Apply the migration**

```bash
python scripts/migrate_names.py
```

Expected:
```
[MIGRATED] 250 speaker files processed
```

- [ ] **Step 4: Spot-check a migrated file**

```bash
head -10 content/speakers/p/david-pilato/_index.md
```

Expected front matter to contain `firstname: David` and `lastname: Pilato` with no `name:` field.

---

### Task 2: Update template filters

All templates that detect speaker pages via `"Params.name" "ne" nil` or `{{ if .Params.name }}` must switch to `lastname`.

**Files:**
- Modify: `themes/brownbaglunch/layouts/home.html`
- Modify: `themes/brownbaglunch/layouts/index.html`
- Modify: `themes/brownbaglunch/layouts/speakers/list.html`
- Modify: `themes/brownbaglunch/layouts/speakers/letter.html`
- Modify: `themes/brownbaglunch/layouts/_partials/speakers-for-city.html`
- Modify: `themes/brownbaglunch/layouts/cities/list.html`

- [ ] **Step 1: Update `home.html` and `index.html`**

In both files, find and replace:
```
"Params.name" "ne" nil
```
with:
```
"Params.lastname" "ne" nil
```

- [ ] **Step 2: Update `speakers/list.html`**

Line 3 — filter:
```
"Params.name" "ne" nil
```
→
```
"Params.lastname" "ne" nil
```

Line 8 — existence check:
```
{{ if .Params.name }}
```
→
```
{{ if .Params.lastname }}
```

- [ ] **Step 3: Update `speakers/letter.html`**

Line 4 — filter:
```
"Params.name" "ne" nil
```
→
```
"Params.lastname" "ne" nil
```

Line 11 — existence check:
```
{{ if .Params.name }}
```
→
```
{{ if .Params.lastname }}
```

- [ ] **Step 4: Update `_partials/speakers-for-city.html`**

Line 12:
```
{{ if .Params.name }}
```
→
```
{{ if .Params.lastname }}
```

- [ ] **Step 5: Update `cities/list.html`**

Line 4:
```
"Params.name" "ne" nil
```
→
```
"Params.lastname" "ne" nil
```

---

### Task 3: Update sorts and alphabet nav

**Files:**
- Modify: `themes/brownbaglunch/layouts/speakers/list.html`
- Modify: `themes/brownbaglunch/layouts/speakers/letter.html`
- Modify: `themes/brownbaglunch/layouts/cities/list.html`

- [ ] **Step 1: Update alphabet nav in `speakers/list.html`**

Line 9:
```
partial "first-letter.html" .Params.name
```
→
```
partial "first-letter.html" .Params.lastname
```

- [ ] **Step 2: Update alphabet nav and sort in `speakers/letter.html`**

Line 12:
```
partial "first-letter.html" .Params.name
```
→
```
partial "first-letter.html" .Params.lastname
```

Line 20:
```
sort $filtered "Params.name"
```
→
```
sort $filtered "Params.lastname"
```

- [ ] **Step 3: Update sort in `cities/list.html`**

Line 31:
```
sort $speakers "Params.name"
```
→
```
sort $speakers "Params.lastname"
```

---

### Task 4: Update template displays

Two patterns apply depending on context:

**Text display** (links, headings, paragraphs):
```html
{{ $speaker.firstname }} <strong>{{ substr $speaker.lastname 0 1 }}</strong>{{ substr $speaker.lastname 1 }}
```

**`alt` attributes** (no HTML allowed):
```html
{{ $speaker.firstname }} {{ $speaker.lastname }}
```

**Files:**
- Modify: `themes/brownbaglunch/layouts/speakers/speaker.html`
- Modify: `themes/brownbaglunch/layouts/_partials/speaker-card.html`
- Modify: `themes/brownbaglunch/layouts/speakers/list.html`
- Modify: `themes/brownbaglunch/layouts/speakers/talk.html`
- Modify: `themes/brownbaglunch/layouts/talks/list.html`
- Modify: `themes/brownbaglunch/layouts/tags/term.html`

Note: in `speaker.html` and `speaker-card.html`, `.Params` is assigned to `$speaker`, so use `$speaker.firstname` / `$speaker.lastname`. In `list.html`'s latest-arrivals section and in `talk.html` / `talks/list.html` / `tags/term.html`, the page is accessed as `.Params.firstname` / `.Params.lastname` or `$speakerPage.Params.firstname` / `$speakerPage.Params.lastname`.

- [ ] **Step 1: Update `speakers/speaker.html`**

Line 9 — alt attribute:
```html
alt="{{ $speaker.name }}"
```
→
```html
alt="{{ $speaker.firstname }} {{ $speaker.lastname }}"
```

Line 15 — h1:
```html
{{ $speaker.name }}
```
→
```html
{{ $speaker.firstname }} <strong>{{ substr $speaker.lastname 0 1 }}</strong>{{ substr $speaker.lastname 1 }}
```

- [ ] **Step 2: Update `_partials/speaker-card.html`**

Line 6 — alt attribute:
```html
alt="{{ $speaker.name }}"
```
→
```html
alt="{{ $speaker.firstname }} {{ $speaker.lastname }}"
```

Line 11 — link text:
```html
{{ $speaker.name }}
```
→
```html
{{ $speaker.firstname }} <strong>{{ substr $speaker.lastname 0 1 }}</strong>{{ substr $speaker.lastname 1 }}
```

- [ ] **Step 3: Update `speakers/list.html` (latest-arrivals section)**

Line 171 — alt attribute:
```html
alt="{{ .Params.name }}"
```
→
```html
alt="{{ .Params.firstname }} {{ .Params.lastname }}"
```

Line 176 — link text:
```html
{{ .Params.name }}
```
→
```html
{{ .Params.firstname }} <strong>{{ substr .Params.lastname 0 1 }}</strong>{{ substr .Params.lastname 1 }}
```

- [ ] **Step 4: Update `speakers/talk.html`**

Line 20 — text:
```html
{{ $speakerPage.Params.name }}
```
→
```html
{{ $speakerPage.Params.firstname }} <strong>{{ substr $speakerPage.Params.lastname 0 1 }}</strong>{{ substr $speakerPage.Params.lastname 1 }}
```

Line 79 — alt attribute:
```html
alt="{{ $speakerPage.Params.name }}"
```
→
```html
alt="{{ $speakerPage.Params.firstname }} {{ $speakerPage.Params.lastname }}"
```

Line 86 — text:
```html
{{ $speakerPage.Params.name }}
```
→
```html
{{ $speakerPage.Params.firstname }} <strong>{{ substr $speakerPage.Params.lastname 0 1 }}</strong>{{ substr $speakerPage.Params.lastname 1 }}
```

- [ ] **Step 5: Update `talks/list.html`**

Line 112:
```html
{{ $speakerPage.Params.name }}
```
→
```html
{{ $speakerPage.Params.firstname }} <strong>{{ substr $speakerPage.Params.lastname 0 1 }}</strong>{{ substr $speakerPage.Params.lastname 1 }}
```

- [ ] **Step 6: Update `tags/term.html`**

Line 31 — alt attribute:
```html
alt="{{ $speakerPage.Params.name }}"
```
→
```html
alt="{{ $speakerPage.Params.firstname }} {{ $speakerPage.Params.lastname }}"
```

Line 34 — link text:
```html
{{ $speakerPage.Params.name }}
```
→
```html
{{ $speakerPage.Params.firstname }} <strong>{{ substr $speakerPage.Params.lastname 0 1 }}</strong>{{ substr $speakerPage.Params.lastname 1 }}
```

---

### Task 5: Build verification and single commit

- [ ] **Step 1: Verify no `name:` field remains in speaker content**

```bash
grep -r "^name:" content/speakers/
```

Expected: no output.

- [ ] **Step 2: Verify no `Params.name` remains in templates**

```bash
grep -r "Params\.name\b" themes/brownbaglunch/layouts/
```

Expected: no output.

- [ ] **Step 3: Run Hugo build**

```bash
hugo --gc --minify
```

Expected: build completes with 0 errors.

- [ ] **Step 4: Spot-check in browser**

```bash
hugo server
```

Navigate to:
- `/speakers/` — alphabet nav groups by last name initial; "latest arrivals" cards show `Firstname **L**astname`
- `/speakers/p/` — speakers sorted alphabetically by last name, all showing `Firstname **L**astname`
- A city page — speaker list sorted by last name
- A speaker profile page — `h1` shows `Firstname **L**astname`
- A talk page — speaker name in breadcrumb/header shows correct format

- [ ] **Step 5: Single commit**

```bash
git add content/speakers/ scripts/migrate_names.py themes/brownbaglunch/layouts/
git commit -m "✨ feat: split speaker name into firstname + lastname, sort by lastname"
```
