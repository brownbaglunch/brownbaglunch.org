#!/usr/bin/env python3
"""
Migrate speaker leaf bundles (index.md) to branch bundles (_index.md)
and split sessions into individual talk pages under talks/{slug}/index.md.

Run from the repo root:
    python3 scripts/migrate_talks.py
"""

import os
import re
import unicodedata
from pathlib import Path

import yaml

SPEAKERS_DIR = Path("content/speakers")


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug (ASCII, lowercase, hyphens)."""
    # Decompose unicode (é → e + combining accent) then strip combining chars
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower()
    # Replace anything that is not alphanumeric or space/hyphen with nothing
    text = re.sub(r"[^\w\s-]", "", text)
    # Collapse whitespace/underscores to a single hyphen
    text = re.sub(r"[\s_]+", "-", text)
    # Collapse consecutive hyphens
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "talk"


def parse_md(path: Path):
    """Return (frontmatter_dict, body_str) for a YAML-fenced markdown file."""
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return {}, raw
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return {}, raw
    fm = yaml.safe_load(parts[1]) or {}
    return fm, parts[2]


def write_md(path: Path, frontmatter: dict, body: str = "") -> None:
    """Write a YAML-fenced markdown file, creating parent dirs as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("---\n")
        yaml.dump(
            frontmatter,
            fh,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )
        fh.write("---\n")
        stripped = body.strip()
        if stripped:
            fh.write("\n" + stripped + "\n")


def migrate_speaker(index_path: Path) -> None:
    """Convert one speaker leaf bundle → branch bundle + talk pages."""
    speaker_dir = index_path.parent
    speaker_slug = speaker_dir.name

    fm, body = parse_md(index_path)

    # Extract sessions before modifying frontmatter
    sessions = fm.pop("sessions", []) or []

    # Mark page type for Hugo template lookup
    fm["layout"] = "speaker"

    # Write branch bundle (replaces leaf bundle)
    branch_path = speaker_dir / "_index.md"
    write_md(branch_path, fm, body)
    index_path.unlink()

    if not sessions:
        return

    talks_dir = speaker_dir / "talks"
    talks_dir.mkdir(exist_ok=True)

    used_slugs: dict[str, int] = {}
    for session in sessions:
        # Derive talk slug from first version title, falling back to first tag
        title = ""
        if session.get("versions"):
            title = session["versions"][0].get("title", "") or ""
        if not title and session.get("tags"):
            title = session["tags"][0]

        base_slug = slugify(title)

        # Guarantee uniqueness within this speaker's talks
        if base_slug in used_slugs:
            used_slugs[base_slug] += 1
            slug = f"{base_slug}-{used_slugs[base_slug]}"
        else:
            used_slugs[base_slug] = 0
            slug = base_slug

        talk_fm: dict = {
            "layout": "talk",
            "url": f"/speakers/{speaker_slug}/talks/{slug}/",
            "tags": session.get("tags") or [],
            "versions": session.get("versions") or [],
        }

        write_md(talks_dir / slug / "index.md", talk_fm)
        print(f"  talk: {speaker_slug}/talks/{slug}/")


def main() -> None:
    count = 0
    for index_path in sorted(SPEAKERS_DIR.rglob("index.md")):
        # Skip any talk pages already migrated
        if "talks" in index_path.parts:
            continue
        # Only process exactly: speakers/{letter}/{speaker}/index.md
        rel = index_path.relative_to(SPEAKERS_DIR)
        if len(rel.parts) != 3:
            continue
        print(f"Migrating speaker: {rel.parent}")
        migrate_speaker(index_path)
        count += 1

    print(f"\nDone — {count} speaker(s) migrated.")


if __name__ == "__main__":
    main()
