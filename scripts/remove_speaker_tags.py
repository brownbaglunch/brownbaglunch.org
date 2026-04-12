#!/usr/bin/env python3
"""Remove the top-level 'tags' field from speaker _index.md files only.
Talk pages (content/speakers/.../talks/...index.md) are not touched.

Run from the repo root:
    python3 scripts/remove_speaker_tags.py
"""

from pathlib import Path
import yaml

SPEAKERS_DIR = Path("content/speakers")


def parse_md(path: Path):
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return {}, raw
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return {}, raw
    fm = yaml.safe_load(parts[1]) or {}
    return fm, parts[2]


def write_md(path: Path, frontmatter: dict, body: str = "") -> None:
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


def main() -> None:
    count = 0
    for path in sorted(SPEAKERS_DIR.rglob("_index.md")):
        rel = path.relative_to(SPEAKERS_DIR)
        # Only speaker branch bundles: {letter}/{speaker}/_index.md (depth 3)
        if len(rel.parts) != 3:
            continue
        fm, body = parse_md(path)
        if "tags" not in fm:
            continue
        fm.pop("tags")
        write_md(path, fm, body)
        print(f"  removed tags from {rel.parent}")
        count += 1

    print(f"\nDone — {count} speaker(s) updated.")


if __name__ == "__main__":
    main()
