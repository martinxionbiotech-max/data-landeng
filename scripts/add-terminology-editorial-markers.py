#!/usr/bin/env python3
"""Phase 2 (P4): explicit Tier 6 editorial markers for terminology entries
without a sources array, so every entity answers "where does this come from".

No external citation is invented: these entries are this site's own editorial
definitions, and the marker says so explicitly, mirroring the pattern already
applied to aroma / comparisons / forms / materials.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASET = REPO_ROOT / "datasets" / "terminology.json"

MARKER = {
    "type": "editorial_interpretation",
    "title": "Editorial definition from this site's terminology work (no external source claimed).",
    "url": "https://data.incenseherbs.com/terminology/",
    "accessed": "2026-09-28",
    "evidenceLevel": "Tier 6 — Editorial synthesis",
}


def main() -> int:
    doc = json.loads(DATASET.read_text(encoding="utf-8"))
    entities = doc["mainEntity"]
    added = 0
    for e in entities:
        if not e.get("sources"):
            e["sources"] = [dict(MARKER)]
            added += 1

    doc["version"] = "1.5"
    doc["dateModified"] = "2026-09-28"
    doc["changelog"] = (
        "P4 evidence model completion: 169 terminology entries without an external "
        "source now carry an explicit Tier 6 editorial_interpretation marker. Every "
        "entity can now answer 'where does this come from' — external citation where "
        "one exists, explicit editorial label where it does not. No citation invented."
    )

    DATASET.write_text(
        json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    print(f"OK: {len(entities)} terminology entities | Tier 6 markers added={added}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
