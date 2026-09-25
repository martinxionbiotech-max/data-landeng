#!/usr/bin/env python3
"""Export LanDeng datasets/*.json to flat CSV distribution packages.

Each dataset's `mainEntity` array is flattened into rows. Chinese and English
names are carried side by side (`name_zh` / `name_en`); dataset-specific
`additionalProperty` values become their own columns. Output is UTF-8 with a
BOM so Excel opens the files directly.

Idempotent: re-running overwrites the same files. Run standalone (writes to
`datasets/csv/`) or via the MkDocs hook (writes to `site/downloads/`).

Usage:
    python3 scripts/export_csv.py [--out DIR]
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASETS_DIR = REPO_ROOT / "datasets"
DEFAULT_OUT = DATASETS_DIR / "csv"

# Datasets whose mainEntity holds an edge list (entity -> relatedEntity[]).
EDGE_LIST_DATASETS = {"relationships"}

# Fixed leading columns shared by every entity-row CSV.
FIXED_COLUMNS = ["termCode", "name", "name_zh", "name_en", "type"]

# List-valued raw fields appended after additionalProperty columns (only when
# at least one entity carries the field).
LIST_FIELDS = ["alternateName", "sameAs", "memberIngredients"]


def is_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def join_list(value, sep="; "):
    if isinstance(value, list):
        return sep.join(str(v) for v in value if v not in (None, ""))
    return "" if value in (None, "") else str(value)


def additional_property_map(entity):
    out = {}
    for ap in entity.get("additionalProperty", []):
        if isinstance(ap, dict) and "name" in ap:
            out[ap["name"]] = ap.get("value", "")
    return out


def chinese_name(entity):
    """Chinese display name: name if CJK, else first CJK alternateName / Chinese property."""
    name = entity.get("name", "")
    if is_cjk(name):
        return name
    for alt in entity.get("alternateName", []) or []:
        if is_cjk(str(alt)):
            return str(alt)
    apm = additional_property_map(entity)
    for key in ("Chinese", "Chinese name"):
        val = str(apm.get(key, ""))
        if is_cjk(val):
            return val
    return ""


def english_name(entity):
    """English display name: name if Latin, else Preferred English / Literal meaning."""
    name = entity.get("name", "")
    if name and not is_cjk(name):
        return name
    apm = additional_property_map(entity)
    for key in ("Preferred English", "Literal meaning", "English"):
        val = str(apm.get(key, "")).strip()
        if val:
            return val
    return ""


def sources_summary(entity):
    sources = entity.get("sources", []) or []
    urls = [s.get("url", "") for s in sources if isinstance(s, dict) and s.get("url")]
    levels = sorted({s.get("evidenceLevel", "") for s in sources
                     if isinstance(s, dict) and s.get("evidenceLevel")})
    return {
        "sources": "; ".join(urls),
        "sources_count": len(urls),
        "evidenceLevel": "; ".join(levels),
    }


def export_entity_rows(entities):
    """Return (columns, rows) for entity-list datasets."""
    ap_keys = []
    for e in entities:
        for ap in e.get("additionalProperty", []):
            name = ap.get("name") if isinstance(ap, dict) else None
            if name and name not in ap_keys:
                ap_keys.append(name)

    has_field = {f: any(e.get(f) for e in entities) for f in LIST_FIELDS}
    has_sources = any(e.get("sources") for e in entities)
    has_description = any(e.get("description") for e in entities)

    columns = list(FIXED_COLUMNS) + ap_keys
    for f in LIST_FIELDS:
        if has_field[f]:
            columns.append(f)
    if has_sources:
        columns += ["sources", "sources_count", "evidenceLevel"]
    if has_description:
        columns.append("description")

    rows = []
    for e in entities:
        apm = additional_property_map(e)
        row = {
            "termCode": e.get("termCode", ""),
            "name": e.get("name", ""),
            "name_zh": chinese_name(e),
            "name_en": english_name(e),
            "type": e.get("@type", ""),
        }
        for k in ap_keys:
            row[k] = apm.get(k, "")
        for f in LIST_FIELDS:
            if has_field[f]:
                row[f] = join_list(e.get(f))
        if has_sources:
            row.update(sources_summary(e))
        if has_description:
            row["description"] = e.get("description", "")
        rows.append(row)
    return columns, rows


def export_edge_rows(entities):
    """Return (columns, rows) for relationships — one row per edge."""
    columns = ["source_termCode", "source_name", "relation_type",
               "target_termCode", "target_name", "target_dataset"]
    rows = []
    for e in entities:
        src_code = e.get("termCode", "")
        src_name = e.get("name", "")
        for rel in e.get("relatedEntity", []) or []:
            if not isinstance(rel, dict):
                continue
            rows.append({
                "source_termCode": src_code,
                "source_name": src_name,
                "relation_type": rel.get("type", ""),
                "target_termCode": rel.get("termCode", ""),
                "target_name": rel.get("name", ""),
                "target_dataset": rel.get("inDataset", ""),
            })
    return columns, rows


def export_dataset(json_path, out_dir):
    with open(json_path, encoding="utf-8") as fh:
        data = json.load(fh)
    entities = data.get("mainEntity", [])
    name = json_path.stem
    if name in EDGE_LIST_DATASETS:
        columns, rows = export_edge_rows(entities)
    else:
        columns, rows = export_entity_rows(entities)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{name}.csv"
    with open(out_path, "w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    return out_path, len(rows)


def export_all(datasets_dir, out_dir):
    results = []
    for json_path in sorted(datasets_dir.glob("*.json")):
        out_path, n = export_dataset(json_path, out_dir)
        results.append((out_path, n))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="output directory (default: datasets/csv)")
    args = parser.parse_args()
    results = export_all(DATASETS_DIR, args.out)
    total = 0
    for p, n in results:
        total += n
        print(f"{p.name}: {n} rows")
    print(f"Exported {len(results)} CSV files ({total} data rows) to {args.out}")


if __name__ == "__main__":
    main()
