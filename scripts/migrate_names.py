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
