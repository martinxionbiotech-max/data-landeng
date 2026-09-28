#!/usr/bin/env python3
"""Cross-check dataset counts / docs / CSV / dateModified consistency.

Verifies that the single source of truth (datasets/*.json) agrees with every
downstream surface:
  1) docs injection regions (index.md / datasets.md / README.md / docs/*.md)
     match the JSON entity+edge counts, version and dateModified.
  2) the CSV distribution packages derive the right number of rows
     (entity datasets: N + 1 header; relationships: edges + 1 header).
  3) all eight datasets share one dateModified (no per-file date drift).

Any mismatch exits non-zero so CI fails before drifting data ships.

Usage:
    python3 scripts/check-consistency.py
"""
from __future__ import annotations

import csv
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# inject-counts.py uses a hyphenated filename (per spec), so load it by path.
ic = _load_module("inject_counts", str(REPO_ROOT / "scripts" / "inject-counts.py"))


def check_injection_regions(counts: dict) -> list[str]:
    errors = []
    for rel, key, inline in ic.TARGETS:
        path = ic.REPO_ROOT / rel
        if not path.exists():
            errors.append(f"{rel}: missing file")
            continue
        actual = ic.extract_text(path.read_text(encoding="utf-8"), key, inline)
        expected = ic.render(key, counts)
        if actual != expected:
            errors.append(
                f"{rel} [{key}]: docs != JSON\n"
                f"    expected: {expected!r}\n"
                f"    actual:   {actual!r}"
            )
    return errors


def check_csv_rows(counts: dict) -> list[str]:
    errors = []
    with tempfile.TemporaryDirectory() as tmp:
        spec = importlib.util.spec_from_file_location(
            "export_csv", str(REPO_ROOT / "scripts" / "export_csv.py")
        )
        export_csv = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(export_csv)

        out_dir = Path(tmp)
        for json_path in sorted(ic.DATASETS_DIR.glob("*.json")):
            out_path, _ = export_csv.export_dataset(json_path, out_dir)
            stem = json_path.stem
            with open(out_path, encoding="utf-8-sig", newline="") as fh:
                n_lines = sum(1 for _ in csv.reader(fh))
            expected = counts[stem]["edges"] + 1 if stem == "relationships" else counts[stem]["n"] + 1
            if n_lines != expected:
                errors.append(
                    f"{stem}.csv: {n_lines} rows != expected {expected} "
                    f"(JSON {'edges' if stem == 'relationships' else 'entities'} + 1 header)"
                )
    return errors


def check_date_modified(counts: dict) -> list[str]:
    errors = []
    dates = {stem: counts[stem]["date"] for stem in ic.STEMS}
    if len(set(dates.values())) != 1:
        errors.append(f"dateModified not uniform across datasets: {dates}")
    return errors


# Relationship edge types and the dataset / value space each one must resolve
# against. `category` resolves against the Category values declared in
# ingredients.json (category is a label, not a separate entity dataset);
# every other type resolves against entity termCodes.
EDGE_RULES = {
    "category": "ingredient-categories",
    "aroma": "aroma",
    "comparison": "comparisons",
    "technique": "techniques",
    "form": "forms",
    "related": "ingredients",
}


def check_relationship_edges(counts: dict) -> list[str]:
    """Validate every relationships.json edge: known type, resolvable target,
    subject is a real ingredient, and no duplicate (type, termCode) pair."""
    errors = []
    datasets = {}
    for stem in ic.STEMS:
        with open(ic.DATASETS_DIR / f"{stem}.json", encoding="utf-8") as fh:
            datasets[stem] = json.load(fh)

    ingredient_codes = {e.get("termCode") for e in datasets["ingredients"]["mainEntity"]}

    # Category labels live in ingredients.json additionalProperty, not as entities.
    category_values = set()
    for e in datasets["ingredients"]["mainEntity"]:
        for p in e.get("additionalProperty", []) or []:
            if p.get("name") == "Category" and p.get("value"):
                category_values.add(p["value"])

    resolvers = {
        "ingredient-categories": category_values,
    }
    for stem in ("aroma", "comparisons", "techniques", "forms", "ingredients"):
        resolvers[stem] = {e.get("termCode") for e in datasets[stem]["mainEntity"]}

    for rec in datasets["relationships"]["mainEntity"]:
        subj = rec.get("termCode")
        if not subj or subj not in ingredient_codes:
            errors.append(f"relationships.json: subject {subj!r} is not an ingredient termCode")
            continue
        seen = set()
        for edge in rec.get("relatedEntity", []) or []:
            etype = edge.get("type")
            code = edge.get("termCode")
            rule = EDGE_RULES.get(etype)
            if rule is None:
                errors.append(f"relationships.json [{subj}]: unknown edge type {etype!r}")
                continue
            if not code or code not in resolvers[rule]:
                errors.append(
                    f"relationships.json [{subj}]: {etype} edge {code!r} does not resolve "
                    f"in {rule}"
                )
            pair = (etype, code)
            if pair in seen:
                errors.append(f"relationships.json [{subj}]: duplicate edge {etype}->{code}")
            seen.add(pair)
    return errors


def check_entity_pages(counts: dict) -> list[str]:
    """Validate docs/entities/ against datasets/*.json truth.

    - one page per entity termCode across the six entity datasets (shared
      termCodes merge, so the page count may be lower than the raw sum)
    - no orphan pages (every page maps to a dataset entity)
    - retrieval index (entities/index.json) item count matches page count
    - no broken /entities/ links inside entity pages
    """
    import re

    ENTITY_DATASETS = ["ingredients", "aroma", "materials", "techniques", "forms", "comparisons"]
    errors = []
    codes = set()
    for stem in ENTITY_DATASETS:
        with open(REPO_ROOT / "datasets" / f"{stem}.json", encoding="utf-8") as fh:
            data = json.load(fh)
        codes.update(e.get("termCode") for e in data.get("mainEntity", []) if e.get("termCode"))

    ent_dir = REPO_ROOT / "docs" / "entities"
    if not ent_dir.exists():
        errors.append("docs/entities/: missing directory")
        return errors
    pages = {p.stem for p in ent_dir.glob("*.md") if p.stem != "index"}

    orphan_pages = sorted(pages - codes)
    if orphan_pages:
        errors.append(f"docs/entities/: orphan pages not in any dataset: {orphan_pages}")
    missing_pages = sorted(codes - pages)
    if missing_pages:
        errors.append(f"docs/entities/: entities without pages: {missing_pages[:5]}...")

    for p in sorted(ent_dir.glob("*.md")):
        if p.stem == "index":
            continue
        raw = p.read_text(encoding="utf-8")
        for m in re.finditer(r"\]\((/entities/[a-z0-9\-]+)/\)", raw):
            target = m.group(1).split("/")[-1]
            if target not in pages:
                errors.append(f"docs/entities/{p.name}: broken link to /entities/{target}/")

    idx_path = ent_dir / "index.json"
    if idx_path.exists():
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        if idx.get("numberOfItems") != len(pages):
            errors.append(
                f"entities/index.json: numberOfItems {idx.get('numberOfItems')} != pages {len(pages)}"
            )
    else:
        errors.append("entities/index.json: missing retrieval index")
    return errors


def main() -> int:
    counts = ic.read_counts()

    errors = []
    errors += check_injection_regions(counts)
    errors += check_csv_rows(counts)
    errors += check_date_modified(counts)
    errors += check_relationship_edges(counts)
    errors += check_entity_pages(counts)

    if errors:
        print("Consistency check FAILED:")
        for e in errors:
            print("  -", e)
        return 1

    total = sum(c["n"] for c in counts.values())
    edges = counts["relationships"]["edges"]
    date = counts["ingredients"]["date"]
    print("OK: datasets, docs, CSV and dateModified are consistent")
    print(f"    {len(counts)} datasets | {total} entities | {edges} relationship edges | dateModified {date}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
