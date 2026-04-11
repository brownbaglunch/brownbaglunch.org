# Brown Bag Lunch — bblfr

A static site built with [Hugo](https://gohugo.io) listing speakers, talks, and cities
for the Brown Bag Lunch community. Anyone can invite a speaker to give a free talk during
their team's lunch break — the host provides the food, the speaker provides the knowledge.

## How it works

- **Hosts** browse speakers and talks, then contact a speaker directly via email.
- **Speakers** register by opening a pull request adding their own Markdown file.
- The site is rebuilt and deployed automatically on every merge to `main`.

## Adding or updating your speaker profile

1. Fork this repository.
2. Create a file at `content/speakers/{country}/{city}/{your-slug}.md`
   following the naming rules below.
3. Fill in the front matter (see template below).
4. Open a pull request — once merged, the site rebuilds automatically.

### Naming rules

| Field | Rule | Example |
|-------|------|---------|
| `{country}` | ISO 3166-1 alpha-2 country code, lowercase | `fr`, `gb`, `de` |
| `{city}` | City name slugified (lowercase, diacritics removed, spaces → `-`) | `paris`, `sophia-antipolis` |
| `{your-slug}` | Your full name slugified | `jane-doe.md` |

### Speaker file template

```yaml
---
name: "Jane Doe"
since: "2024-01-15"          # date you joined BBL
city: "fr/paris"             # your home city (ISO country / city slug)
cities:                      # cities where you are available to speak
  - "fr/paris"               # specific city
  - "fr/*"                   # anywhere in France
  - "*/*"                    # anywhere in the world
picture: "https://..."       # URL to your avatar (Gravatar or GitHub avatar recommended)
contacts:
  x: "yourhandle"            # X (formerly Twitter) handle — optional
  mail: "you@example.com"    # email address (required)
websites:
  - name: "GitHub"
    url: "https://github.com/you"
sessions:
  - tags: ["tag1", "tag2"]
    versions:
      - label: "FR"
        flag: "fr"
        title: "Titre de votre talk"
        abstract: |
          Description en **Markdown**.
      - label: "EN"          # optional — add more languages as needed
        flag: "gb"
        title: "Your talk title"
        abstract: |
          Description in **Markdown**.
---

Your bio in Markdown here.
```

### `city` vs `cities`

- `city` — where you **live** (used to place your file in the directory tree).
- `cities` — where you are **willing to speak**. Use `"cc/*"` for "anywhere in country `cc`",
  or `"*/*"` for worldwide availability.

## Development

Requirements: [Hugo 0.157.0](https://gohugo.io/installation/) and Node.js ≥ 18.

```bash
npm install          # install Tailwind CSS and PostCSS
hugo server          # start dev server at http://localhost:1313
npm run build        # production build + Pagefind index
```

## License

Apache 2.0 — see [LICENSE](LICENSE).
