#!/usr/bin/env node
/**
 * Migrate speaker _index.md files:
 * - websites[] entries for GitHub, LinkedIn, SlideShare → structured contacts.*
 * - websites[] entries with name "Blog" → contacts.blog
 * - Generic/unknown websites stay in websites[]
 *
 * Already-migrated speakers (Alexander Dejanovski) are skipped safely
 * because we never overwrite an existing contacts.* key.
 */

const fs   = require('fs');
const path = require('path');
const yaml = require('./node_modules/yaml');

// ── URL extractors ──────────────────────────────────────────────────────────

function extractGitHub(url) {
  // github.com/<username>  — NOT *.github.io or *.github.com personal pages
  const m = url.match(/^https?:\/\/(?:www\.)?github\.com\/([^/]+)\/?$/i);
  return m ? m[1] : null;
}

function extractLinkedIn(url) {
  // (www|fr|en|...).linkedin.com/in/<slug>[/lang]
  const m = url.match(/^https?:\/\/(?:[a-z]+\.)?linkedin\.com\/in\/([^/?#]+)/i);
  if (m) return m[1].replace(/\/$/, '');
  return null;
}

function extractSlideShare(url) {
  // (www|fr|...).slideshare.net/<username>[/...]
  const m = url.match(/^https?:\/\/(?:[a-z]+\.)?slideshare\.net\/([^/]+)/i);
  return m ? m[1] : null;
}

function isBlog(name) {
  return /^blog$/i.test((name || '').trim());
}

// ── File helpers ────────────────────────────────────────────────────────────

function parseFrontMatter(src) {
  const match = src.match(/^---\n([\s\S]*?)\n---(\n?)([\s\S]*)$/);
  if (!match) return null;
  return { fm: match[1], sep: match[2], body: match[3] };
}

function serializeFrontMatter(data, sep, body) {
  const fm = yaml.stringify(data, { lineWidth: 0, defaultStringType: 'PLAIN', defaultKeyType: 'PLAIN' }).trimEnd();
  return `---\n${fm}\n---${sep}${body}`;
}

// ── Migration logic ─────────────────────────────────────────────────────────

function migrateSpeaker(filePath) {
  const src    = fs.readFileSync(filePath, 'utf8');
  const parsed = parseFrontMatter(src);
  if (!parsed) return { skipped: true, reason: 'no front matter' };

  const data     = yaml.parse(parsed.fm);
  const contacts = data.contacts || {};
  const websites = Array.isArray(data.websites) ? data.websites : [];

  if (!websites.length) return { skipped: true, reason: 'no websites' };

  const remaining = [];
  const moved     = [];

  for (const site of websites) {
    const url  = (site.url  || '').trim();
    const name = (site.name || '').trim();
    let   handled = false;

    // GitHub profile
    if (!contacts.github) {
      const gh = extractGitHub(url);
      if (gh) { contacts.github = gh; moved.push(`github: ${gh}`); handled = true; }
    }

    // LinkedIn
    if (!handled && !contacts.linkedin) {
      const li = extractLinkedIn(url);
      if (li) { contacts.linkedin = li; moved.push(`linkedin: ${li}`); handled = true; }
    }

    // SlideShare
    if (!handled && !contacts.slideshare) {
      const ss = extractSlideShare(url);
      if (ss) { contacts.slideshare = ss; moved.push(`slideshare: ${ss}`); handled = true; }
    }

    // Blog (by name)
    if (!handled && !contacts.blog && isBlog(name)) {
      contacts.blog = url; moved.push(`blog: ${url}`); handled = true;
    }

    if (!handled) remaining.push(site);
  }

  if (!moved.length) return { skipped: true, reason: 'nothing to migrate' };

  data.contacts = contacts;
  if (remaining.length) {
    data.websites = remaining;
  } else {
    delete data.websites;
  }

  const out = serializeFrontMatter(data, parsed.sep, parsed.body);
  fs.writeFileSync(filePath, out, 'utf8');
  return { skipped: false, moved };
}

// ── Walk content/speakers ───────────────────────────────────────────────────

function walk(dir, results = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, results);
    else if (entry.name === '_index.md') results.push(full);
  }
  return results;
}

const speakersDir = path.join(__dirname, 'content', 'speakers');
const files       = walk(speakersDir);

let migrated = 0, skipped = 0;

for (const f of files) {
  const rel    = path.relative(__dirname, f);
  const result = migrateSpeaker(f);
  if (result.skipped) {
    skipped++;
  } else {
    migrated++;
    console.log(`✓ ${rel}`);
    for (const m of result.moved) console.log(`    → ${m}`);
  }
}

console.log(`\nDone: ${migrated} migrated, ${skipped} skipped.`);
