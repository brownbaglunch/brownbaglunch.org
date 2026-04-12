#!/usr/bin/env python3
"""
Normalize tags across all talk pages.

Mapping rules (old → canonical):
  - typos
  - plural/singular variants
  - hyphen vs no-hyphen
  - same tool, different name
  - user-validated semantic merges

After replacement, duplicates in a single talk are removed.

Run from the repo root:
    python3 scripts/normalize_tags.py
"""

from pathlib import Path
from collections import defaultdict
import yaml

SPEAKERS_DIR = Path("content/speakers")

# ── Complete tag mapping (old → canonical) ────────────────────────────────────
TAG_MAP: dict[str, str] = {
    # Typos
    "assynchronisme":           "asynchronous",
    "asynchrone":               "asynchronous",
    "continous-delivery":       "continuous-delivery",
    "continous":                "continuous-delivery",
    "craftmanship":             "craftsmanship",
    "extreme-programmming":     "extreme-programming",
    "functional-programing":    "functional-programming",
    "guithub":                  "github",
    "gooogle":                  "google",
    "culuture":                 "culture",
    "tddflow":                  "tdd",
    "tddlego":                  "lego",

    # Plural / singular
    "12-factors":               "12-factor",
    "apis":                     "api",
    "architectures":            "architecture",
    "base-de-donnees":          "database",
    "bases-de-donnees":         "database",
    "containers":               "container",
    "databases":                "database",
    "equipes":                  "equipe",
    "innovation-game":          "innovation-games",
    "moteur-de-regles":         "moteurs-de-regles",
    "serious-games":            "serious-game",
    "seriousgame":              "serious-game",
    "tests":                    "test",

    # Hyphen / soudé
    "b-d-d":                    "bdd",
    "caching":                  "cache",
    "cicd":                     "ci-cd",
    "cleancode":                "clean-code",
    "codingdojo":               "coding-dojo",
    "deeplearning":             "deep-learning",
    "eventsourcing":            "event-sourcing",
    "eventstorming":            "event-storming",
    "examplemapping":           "example-mapping",
    "feature-toggling":         "feature-toggle",
    "infra-as-code":            "infrastructure-as-code",
    "leanstartup":              "lean-startup",
    "lego-serious-play":        "lego",
    "livecoding":               "live-coding",
    "raspberry":                "raspberry-pi",
    "serversentevent":          "server-sent-event",
    "serviceworker":            "service-worker",
    "sonarqube":                "sonar",
    "streamprocessing":         "streaming",
    "t-d-d":                    "tdd",
    "teambuilding":             "team-building",

    # Même outil, noms différents
    "angular2":                 "angular",
    "apache-kafka":             "kafka",
    "front":                    "frontend",
    "front-end":                "frontend",
    "go":                       "golang",
    "googlecloud":              "google-cloud",
    "js":                       "javascript",
    "micro-services":           "microservices",
    "microservice":             "microservices",
    "node":                     "nodejs",
    "node-js":                  "nodejs",
    "opensource":               "open-source",
    "postgres":                 "postgresql",
    "react-js":                 "react",
    "vue-js":                   "vue",
    "vuejs":                    "vue",
    "warp10":                   "warp-10",

    # FR → EN
    "atelier":                  "workshop",
    "automatisation":           "automation",
    "cryptomonnaies":           "cryptocurrency",
    "haute-disponibilite":      "highavailability",
    "ia":                       "ai",
    "supervision":              "monitoring",
    "observabilite":            "observability",
    "organisation":             "organization",
    "recrutement":              "recruiting",
    "tests-unitaires":          "unit-test",

    # Merges sémantiques — pass 1
    "cloud-computing":          "cloud",
    "ddd":                      "domain-driven-design",
    "es":                       "ecmascript",
    "es2015":                   "ecmascript",
    "es6":                      "ecmascript",
    "http-2":                   "http2",
    "j2ee":                     "javaee",
    "java-ee":                  "javaee",
    "jee":                      "javaee",
    "open-data":                "opendata",
    "rest-api":                 "rest",
    "securite":                 "security",
    "spark":                    "apache-spark",
    "xp":                       "extreme-programming",

    # Merges sémantiques — pass 2
    "agilite":                  "agile",
    "cd":                       "continuous-delivery",
    "ci":                       "continuous-integration",
    "code-legacy":              "legacy-code",
    "deploy":                   "deployment",
    "deploiement":              "deployment",
    "deploiement-continue":     "continuous-delivery",
    "dojo":                     "coding-dojo",
    "experience-utilisateur":   "ux",
    "fp":                       "functional-programming",
    "fp-style":                 "functional-programming",
    "integration-continue":     "continuous-integration",
    "legacy":                   "legacy-code",
    "programmation-fonctionnelle": "functional-programming",
    "qualite":                  "quality",
    "qualite-de-code":          "quality",
    "qualite-logicielle":       "quality",
    "scale":                    "scalability",
    "scalabilite":              "scalability",
    "scaling":                  "scalability",
    "user-experience":          "ux",
}


def parse_md(path: Path):
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return {}, raw
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return {}, raw
    return yaml.safe_load(parts[1]) or {}, parts[2]


def write_md(path: Path, frontmatter: dict, body: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("---\n")
        yaml.dump(frontmatter, fh, allow_unicode=True,
                  default_flow_style=False, sort_keys=False)
        fh.write("---\n")
        stripped = body.strip()
        if stripped:
            fh.write("\n" + stripped + "\n")


def main() -> None:
    changes: dict[str, list[str]] = defaultdict(list)  # old → [files changed]
    files_updated = 0

    for path in sorted(SPEAKERS_DIR.rglob("index.md")):
        if "talks" not in path.parts:
            continue

        fm, body = parse_md(path)
        original_tags: list = list(fm.get("tags") or [])
        if not original_tags:
            continue

        new_tags: list[str] = []
        seen: set[str] = set()
        modified = False

        for tag in original_tags:
            canonical = TAG_MAP.get(tag, tag)
            if canonical != tag:
                changes[tag].append(str(path))
                modified = True
            if canonical not in seen:
                new_tags.append(canonical)
                seen.add(canonical)
            # else: duplicate after mapping — silently dropped

        if modified or len(new_tags) != len(original_tags):
            fm["tags"] = new_tags
            write_md(path, fm, body)
            files_updated += 1

    print("Tags normalized:")
    for old, files in sorted(changes.items()):
        canonical = TAG_MAP[old]
        print(f"  {old!r:35s} → {canonical!r}  ({len(files)} talk(s))")

    print(f"\n{files_updated} file(s) updated.")


if __name__ == "__main__":
    main()
