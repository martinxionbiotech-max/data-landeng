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


def main() -> int:
    counts = ic.read_counts()

    errors = []
    errors += check_injection_regions(counts)
    errors += check_csv_rows(counts)
    errors += check_date_modified(counts)

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
