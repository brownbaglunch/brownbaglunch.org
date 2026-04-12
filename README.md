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
| `name` | yes | — | Full display name |
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
name: "Jane Doe"
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
| `versions[].label` | yes | — | Language label displayed on the card (e.g. `FR`, `EN`) |
| `versions[].flag` | yes | — | ISO 3166-1 alpha-2 country code for the flag icon (e.g. `fr`, `gb`) |
| `versions[].title` | yes | — | Talk title in that language |
| `versions[].abstract` | yes | — | Talk description in Markdown |
| `cover` | no | speaker's cover | Talks do not have their own cover image. The speaker's avatar is displayed automatically (resolved from `cover` frontmatter or `cover.*` file in the speaker directory). |

#### Example

```yaml
---
layout: talk
url: /speakers/jane-doe/talks/introduction-to-docker/
tags:
  - docker
  - devops
versions:
  - label: "FR"
    flag: "fr"
    title: "Introduction à Docker"
    abstract: |
      Description en **Markdown**.
  - label: "EN"
    flag: "gb"
    title: "Introduction to Docker"
    abstract: |
      Description in **Markdown**.
---
```

## Development

Requirements: [Hugo 0.157.0+extended](https://gohugo.io/installation/) and Node.js ≥ 18.

```bash
npm install          # install Tailwind CSS and PostCSS
npm run dev          # start dev server at http://localhost:1313
npm run build        # production build + Pagefind search index
```

## License

Apache 2.0 — see [LICENSE](LICENSE).
