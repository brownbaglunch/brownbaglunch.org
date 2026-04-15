# Utterances Comments Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add GitHub-backed comments (via utterances) to speaker profile pages and individual talk pages, sharing the same thread across all language variants.

**Architecture:** A new Hugo partial `comments.html` computes a canonical path by stripping the `/en/` or `/de/` language prefix from the page URL, then renders the utterances widget script. The partial is embedded at the bottom of `speaker.html` and `talk.html`.

**Tech Stack:** Hugo templates, utterances (external JS widget), GitHub Issues as comment storage, Tailwind CSS for layout.

> **Prerequisites (manual, one-time):**
> 1. Create public GitHub repo `brownbaglunch.org/public-comments`.
> 2. Install the utterances GitHub App on that repo at https://utteranc.es.

---

## File Map

| File | Action |
|------|--------|
| `themes/brownbaglunch/layouts/_partials/comments.html` | Create |
| `themes/brownbaglunch/layouts/speakers/speaker.html` | Modify — append partial call |
| `themes/brownbaglunch/layouts/speakers/talk.html` | Modify — append partial call |
| `i18n/fr.yaml` | Modify — add `comments` key |
| `i18n/en.yaml` | Modify — add `comments` key |
| `i18n/de.yaml` | Modify — add `comments` key |

---

## Task 1: Add i18n translation keys

**Files:**
- Modify: `i18n/fr.yaml`
- Modify: `i18n/en.yaml`
- Modify: `i18n/de.yaml`

- [ ] **Step 1: Add `comments` key to `i18n/fr.yaml`**

Append at the end of the `# Talks` section (after line 135):

```yaml
comments:
  other: Commentaires
```

- [ ] **Step 2: Add `comments` key to `i18n/en.yaml`**

Append at the end of the `# Talks` section (after line 135):

```yaml
comments:
  other: Comments
```

- [ ] **Step 3: Add `comments` key to `i18n/de.yaml`**

Append at the end of the `# Talks` section (after line 135):

```yaml
comments:
  other: Kommentare
```

- [ ] **Step 4: Verify the build still passes**

```bash
hugo --gc --minify
```

Expected: build completes with no errors.

- [ ] **Step 5: Commit**

```bash
git add i18n/fr.yaml i18n/en.yaml i18n/de.yaml
git commit -m "$(cat <<'EOF'
🌐 i18n: add comments translation key (FR/EN/DE)

Closes #1.
EOF
)"
```

---

## Task 2: Create the `comments.html` partial

**Files:**
- Create: `themes/brownbaglunch/layouts/_partials/comments.html`

- [ ] **Step 1: Create the partial**

```html
{{ $term := .RelPermalink | replaceRE "^/(en|de)/" "/" }}
<div class="max-w-3xl mx-auto mt-12 pt-8 border-t border-warm-border">
  <h2 class="text-2xl font-bold mb-6">{{ i18n "comments" }}</h2>
  <script src="https://utteranc.es/client.js"
    repo="brownbaglunch.org/public-comments"
    issue-term="{{ $term }}"
    label="comment"
    theme="github-light"
    crossorigin="anonymous"
    async>
  </script>
</div>
```

- [ ] **Step 2: Verify Hugo can parse the partial**

```bash
hugo --gc --minify
```

Expected: build completes with no errors (the partial is not yet used, so no output change yet).

- [ ] **Step 3: Commit**

```bash
git add themes/brownbaglunch/layouts/_partials/comments.html
git commit -m "$(cat <<'EOF'
✨ feat: add utterances comments partial

Closes #1.
EOF
)"
```

---

## Task 3: Embed comments on speaker pages

**Files:**
- Modify: `themes/brownbaglunch/layouts/speakers/speaker.html`

The current end of `speaker.html` (line 66) is:

```html
  {{ end }}
</div>
{{ end }}
```

- [ ] **Step 1: Add the partial call before the closing `</div>`**

Replace the closing block with:

```html
  {{ end }}

  {{ partial "comments.html" . }}
</div>
{{ end }}
```

- [ ] **Step 2: Build and spot-check the HTML output**

```bash
hugo --gc --minify
grep -A5 "utteranc.es" public/speakers/david-pilato/index.html
```

Expected: the `<script src="https://utteranc.es/client.js"` tag is present, and `issue-term="/speakers/david-pilato/"` (canonical path, no language prefix).

- [ ] **Step 3: Verify the EN language variant has the same `issue-term`**

```bash
grep "issue-term" public/en/speakers/david-pilato/index.html
```

Expected: `issue-term="/speakers/david-pilato/"` — identical to FR.

- [ ] **Step 4: Commit**

```bash
git add themes/brownbaglunch/layouts/speakers/speaker.html
git commit -m "$(cat <<'EOF'
✨ feat: add utterances comments widget to speaker pages

Closes #1.
EOF
)"
```

---

## Task 4: Embed comments on talk pages

**Files:**
- Modify: `themes/brownbaglunch/layouts/speakers/talk.html`

The current end of `talk.html` (line 97) is:

```html

</div>
{{ end }}
```

- [ ] **Step 1: Add the partial call before the closing `</div>`**

Replace the closing block with:

```html

  {{ partial "comments.html" . }}
</div>
{{ end }}
```

- [ ] **Step 2: Build and spot-check a talk page in the HTML output**

Find a talk slug first:

```bash
ls content/speakers/d/david-pilato/talks/ | head -1
```

Then check the output (replace `<talk-slug>` with what was returned):

```bash
hugo --gc --minify
grep -A5 "utteranc.es" public/speakers/david-pilato/talks/<talk-slug>/index.html
```

Expected: `issue-term="/speakers/david-pilato/talks/<talk-slug>/"`.

- [ ] **Step 3: Verify the EN language variant has the same `issue-term`**

```bash
grep "issue-term" public/en/speakers/david-pilato/talks/<talk-slug>/index.html
```

Expected: `issue-term="/speakers/david-pilato/talks/<talk-slug>/"` — identical to FR.

- [ ] **Step 4: Commit**

```bash
git add themes/brownbaglunch/layouts/speakers/talk.html
git commit -m "$(cat <<'EOF'
✨ feat: add utterances comments widget to talk pages

Closes #1.
EOF
)"
```

---

## Task 5: Visual verification with dev server

- [ ] **Step 1: Start the Hugo dev server**

```bash
hugo server
```

Open http://localhost:1313 in a browser.

- [ ] **Step 2: Check a speaker page**

Navigate to any speaker page (e.g. http://localhost:1313/speakers/david-pilato/).

Expected: a "Commentaires" heading and the utterances widget appear at the bottom, after the talks list. The widget shows a GitHub login prompt.

- [ ] **Step 3: Check a talk page**

Navigate to any talk page under a speaker.

Expected: a "Commentaires" heading and the utterances widget appear at the bottom, after the speaker attribution block.

- [ ] **Step 4: Check the English variant**

Navigate to http://localhost:1313/en/speakers/david-pilato/.

Expected: the heading reads "Comments" (EN translation). The widget is present.
