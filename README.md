# Brown Bag Lunch — bblfr

A static site built with [Hugo](https://gohugo.io) listing speakers, talks, and cities
for the Brown Bag Lunch community. Anyone can invite a speaker to give a free talk during
their team's lunch break — the host provides the food, the speaker provides the knowledge.

## How it works

- **Hosts** browse speakers and talks, then contact a speaker directly via email.
- **Speakers** register by opening a pull request adding their own Markdown files.
- The site is rebuilt and deployed automatically on every merge to `main`.

## Adding or updating your speaker profile

1. Fork this repository.
2. Create a directory at `content/speakers/{initial}/{your-slug}/` where `{initial}` is the
   first letter of your slug and `{your-slug}` is your full name slugified.
3. Inside that directory, create `_index.md` with the speaker front matter (see template below).
4. Add your talks as separate files under `content/speakers/{initial}/{your-slug}/talks/{talk-slug}/index.md`.
5. Open a pull request — once merged, the site rebuilds automatically.

### Naming rules

| Field | Rule | Example |
|-------|------|---------|
| `{initial}` | First letter of your slug, lowercase | `j` for `jane-doe` |
| `{your-slug}` | Your full name slugified (lowercase, diacritics removed, spaces → `-`) | `jane-doe` |
| `{talk-slug}` | Your talk title slugified | `introduction-to-docker` |

### Speaker file — `content/speakers/{initial}/{your-slug}/_index.md`

#### Front matter fields

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `firstname` | yes | — | First name |
| `lastname` | yes | — | Last name |
| `since` | yes | — | Date you joined BBL (`YYYY-MM-DD`) |
| `city` | yes | — | Your home city (`cc/city-slug`, e.g. `fr/paris`) |
| `cities` | yes | — | List of cities where you are willing to speak (see patterns below) |
| `cover` | no | none | URL to your avatar (Gravatar or GitHub avatar recommended). Alternatively, place a `cover.*` file (jpg, png…) in the speaker directory — it is loaded automatically when this field is absent. |
| `contacts.mail` | yes | — | Contact email address |
| `contacts.x` | no | none | X (formerly Twitter) handle, without `@` |
| `websites` | no | none | List of `{name, url}` objects linking to your personal pages |
| `layout` | yes | — | Must be `speaker` |
| *(body)* | no | none | Your bio in Markdown |

#### `cities` patterns

| Pattern | Meaning |
|---------|---------|
| `"cc/city-slug"` | A specific city (e.g. `fr/paris`) |
| `"cc/*"` | Anywhere in country `cc` (e.g. `fr/*`) |
| `"*/*"` | Worldwide |

#### `city` vs `cities`

- `city` — where you **live** (used to place your profile in the city listing).
- `cities` — where you are **willing to speak**.

#### Example

```yaml
---
firstname: "Jane"
lastname: "Doe"
since: "2024-01-15"
city: "fr/paris"
cities:
  - "gb/london"
  - "fr/*"
cover: "https://www.gravatar.com/avatar/abc123?s=200"
contacts:
  mail: "jane@example.com"
  x: "janedoe"
websites:
  - name: "GitHub"
    url: "https://github.com/janedoe"
layout: speaker
---

Your bio in Markdown here.
```

### Talk file — `content/speakers/{initial}/{your-slug}/talks/{talk-slug}/index.md`

#### Front matter fields

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `layout` | yes | — | Must be `talk` |
| `url` | yes | — | Canonical path: `/speakers/{your-slug}/talks/{talk-slug}/` |
| `tags` | no | none | List of topic tags |
| `versions` | yes | — | List of language versions (at least one required) |
| `versions[].lang` | yes | — | Language label displayed on the card (e.g. `FR`, `EN`). The flag emoji is resolved automatically from this label. |
| `versions[].title` | yes | — | Talk title in that language |
| `versions[].abstract` | yes | — | Talk description in Markdown |
| `cover` | no | speaker's cover | Talks do not have their own cover image. The speaker's avatar is displayed automatically (resolved from `cover` frontmatter or `cover.*` file in the speaker directory). |

#### Example

```yaml
---
layout: talk
url: speakers/jane-doe/talks/introduction-to-docker/
tags:
  - docker
  - devops
versions:
  - lang: "FR"
    title: "Introduction à Docker"
    abstract: |
      Description en **Markdown**.
  - lang: "EN"
    title: "Introduction to Docker"
    abstract: |
      Description in **Markdown**.
---
```

## Adding a new language

The site is multilingual (FR default, EN and DE currently supported). Speakers and city
content is shared across all languages — only the UI strings need translating.

### 1. `hugo.toml` — declare the language and extend the content mounts

Add a `[languages.xx]` block (replace `xx` with the ISO 639-1 code):

```toml
[languages.xx]
  languageName = 'Your Language'
  weight = 4               # display order in the language switcher
  title = 'Brown Bag Lunch'
```

Extend the two content mounts so the new language shares speakers and cities:

```toml
  [[module.mounts]]
    source = "content/speakers"
    target = "content/speakers"
  [module.mounts.sites.matrix]
    languages = ["en", "de", "xx"]   # ← add "xx" here

  [[module.mounts]]
    source = "content/cities"
    target = "content/cities"
  [module.mounts.sites.matrix]
    languages = ["en", "de", "xx"]   # ← and here
```

### 2. `i18n/xx.yaml` — translate all UI strings

Copy `i18n/en.yaml` to `i18n/xx.yaml` and translate every value.
The keys that matter most:

| Key | Description |
|-----|-------------|
| `nav_speakers`, `nav_talks`, `nav_villes` | Navigation labels |
| `invite` | Button on speaker / talk pages |
| `city_speakers_available` | Speaker count in city cards |
| `country_name_*` | Country names in the city list |
| `home_*` | Home page copy |

### 3. Section index files — titles for the list pages

Create these three files so Hugo generates the section list pages:

```
content/speakers/_index.xx.md   → title: "Speakers in your language"
content/cities/_index.xx.md     → title: "Cities in your language"
content/talks/_index.xx.md      → title: "Talks in your language"
```

Minimal content for each:

```yaml
---
title: "Sprecher"   # translated title
---
```

For `content/speakers/_index.xx.md` only, also add the canonical URL so
Hugo generates the list page at the right path:

```yaml
---
title: "Sprecher"
url: /xx/speakers/
---
```

> **Note on the leading `/`:** Unlike talk files (which are shared across all languages
> and must use a relative URL like `speakers/foo/talks/bar/`), `_index.xx.md` carries a
> language suffix so it only generates one page. An absolute URL like `/xx/speakers/` is
> therefore safe here — there is no other language mount that could overwrite it.

### 4. `themes/brownbaglunch/layouts/_partials/nav.html` — language switcher

Add a flag and label for the new language in the two `{{ if eq ... }}` chains:

```html
{{ else if eq $currentLang "xx" }}🏳️ XX
```

```html
{{ else if eq .Language.Lang "xx" }}🏳️ Your Language
```

### What you get for free

Once the four steps above are done:
- All speaker profiles are available at `/xx/speakers/…`
- All city pages are available at `/xx/cities/…`
- Talk pages are available at `/xx/speakers/…/talks/…`
- The full-text search (Pagefind) indexes the new language automatically
- Talk abstracts fall back to the first `versions` entry if no `xx` version exists

## Adding a press mention

The "On en parle" section on the home page is driven by [`data/press.yaml`](data/press.yaml).
To add a new entry, append a block at the end of the file:

```yaml
- date: "YYYY-MM-DD"
  title: "Article title"
  author: "Author Name"
  url: "https://..."
```

The list is sorted automatically by date (most recent first) — no need to insert entries in order.

## Development

Requirements: [Hugo 0.157.0+extended](https://gohugo.io/installation/) and Node.js ≥ 18.

```bash
npm install          # install Tailwind CSS and PostCSS
npm run dev          # start dev server at http://localhost:1313
npm run build        # production build + Pagefind search index
```

## License

Apache 2.0 — see [LICENSE](LICENSE).
