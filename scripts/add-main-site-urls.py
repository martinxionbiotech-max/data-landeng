#!/usr/bin/env python3
"""Phase 2 (P5): add the canonical main-site page URL to every ingredient entity.

Model (prompt Phase 5, main prompt Phase 9):

    Main Site Entity Page (https://incenseherbs.com/ingredients/<slug>/)
            |
            v
    Canonical Entity ID  (termCode)
            |
            v
    Data Entity          (data.incenseherbs.com/ingredients/#<termCode>)
            |
            v
    Relationships + Evidence + Sources

The main site already links into the data subsite via sameAs on each
ingredient page. This script closes the reverse direction: every data entity
now carries a schema.org `url` pointing at its human-readable main-site page.

Idempotent: safe to re-run; slugs are validated against the main-site content
directory so no URL is invented for a page that does not exist.
"""
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MAIN_INGREDIENTS_DIR = Path("/home/openclaw/LanDeng/src/content/ingredients")
DATASET = REPO_ROOT / "datasets" / "ingredients.json"

MAIN_SITE = "https://incenseherbs.com"


def main() -> int:
    slugs = {p.stem for p in MAIN_INGREDIENTS_DIR.glob("*.md")}
    if not slugs:
        print("ERROR: main-site ingredient directory empty or missing", file=sys.stderr)
        return 1

    doc = json.loads(DATASET.read_text(encoding="utf-8"))
    entities = doc["mainEntity"]

    missing = [e["termCode"] for e in entities if e["termCode"] not in slugs]
    if missing:
        print(f"ERROR: {len(missing)} termCodes have no main-site page: {missing}", file=sys.stderr)
        return 1

    added = updated = 0
    for e in entities:
        url = f"{MAIN_SITE}/ingredients/{e['termCode']}/"
        if e.get("url") != url:
            e["url"] = url
            added += 1
        else:
            updated += 1

    doc["version"] = "1.3"
    doc["dateModified"] = "2026-09-28"
    doc["changelog"] = (
        "P5 main-site connection: every ingredient entity carries a canonical `url` "
        "pointing at its human-readable page on incenseherbs.com "
        "(https://incenseherbs.com/ingredients/<termCode>/). Closes the main-site ↔ "
        "data-site link in the data → main direction; the main site already links "
        "back via sameAs. No entity content changed."
    )

    DATASET.write_text(
        json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    print(f"OK: {len(entities)} entities | url added={added} already-present={updated}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
