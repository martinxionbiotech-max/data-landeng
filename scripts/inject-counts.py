#!/usr/bin/env python3
"""Inject dataset counts / version / dateModified from JSON into docs Markdown.

Reads the eight `datasets/*.json` (the single source of truth) and rewrites
only the marked dynamic regions (<!-- AUTO:counts:KEY --> ... <!-- /... -->)
inside the human-readable docs, so the numbers in the docs never drift from
the JSON. Never rewrites a whole file.

Surfaces covered:
  - docs/index.md      — dataset status table (7 entity datasets)
  - docs/datasets.md   — dataset overview table (8 rows) + per-dataset H2 headings
  - README.md          — dataset status table (8 rows, incl. relationships edges)
  - docs/<stem>.md     — "Data governance" Last updated / Version lines
                         (7 entity datasets; relationships.md has no such block)

Idempotent: re-running regenerates the same output. Run standalone
(`python3 scripts/inject-counts.py`) or from the MkDocs `on_pre_build` hook.

Usage:
    python3 scripts/inject-counts.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASETS_DIR = REPO_ROOT / "datasets"

# (stem, label, noun_in_table, noun_in_h2) — order matches every doc table.
DATASETS = [
    ("ingredients",   "Ingredient database",   "entities",       "entities"),
    ("terminology",   "Terminology database",  "terms",          "terms"),
    ("aroma",         "Aroma database",        "aroma families", "families"),
    ("materials",     "Material database",     "entities",       "entities"),
    ("comparisons",   "Comparison database",   "profiles",       "profiles"),
    ("techniques",    "Technique database",    "techniques",     "techniques"),
    ("forms",         "Form database",         "forms",          "forms"),
    ("relationships", "Relationships database", "entities",      "entities"),
]
STEMS = [d[0] for d in DATASETS]


def json_url(stem: str) -> str:
    return f"https://data.incenseherbs.com/datasets/{stem}.json"


def csv_url(stem: str) -> str:
    return f"https://data.incenseherbs.com/downloads/{stem}.csv"


def read_counts() -> dict:
    """Return {stem: {n, edges, version, date}} read from datasets/*.json."""
    counts = {}
    for stem, *_ in DATASETS:
        path = DATASETS_DIR / f"{stem}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        entities = data.get("mainEntity", []) or []
        n = len(entities)
        edges = 0
        if stem == "relationships":
            edges = sum(len(r.get("relatedEntity", []) or []) for r in entities)
        counts[stem] = {
            "n": n,
            "edges": edges,
            "version": data.get("version", ""),
            "date": data.get("dateModified", ""),
        }
    return counts


# --- renderers (marker key -> injected content, WITHOUT the markers) ---

def _index_table(counts: dict) -> str:
    lines = ["| Dataset | File | Status |", "|---|---|---|"]
    for stem, label, noun, _ in DATASETS:
        if stem == "relationships":
            continue
        n = counts[stem]["n"]
        suffix = ", CC BY-SA 4.0" if stem == "terminology" else ""
        lines.append(f"| {label} | [datasets/{stem}.json]({json_url(stem)}) | live ({n} {noun}{suffix}) |")
    return "\n".join(lines)


def _readme_table(counts: dict) -> str:
    lines = ["| Dataset | File | CSV | Status |", "|---|---|---|---|"]
    for stem, label, noun, _ in DATASETS:
        n = counts[stem]["n"]
        if stem == "relationships":
            status = f"live ({n} entities, {counts[stem]['edges']} edges)"
        elif stem == "terminology":
            status = f"live ({n} terms, CC BY-SA 4.0)"
        else:
            status = f"live ({n} {noun})"
        lines.append(f"| {label} | datasets/{stem}.json | [{stem}.csv]({csv_url(stem)}) | {status} |")
    return "\n".join(lines)


def _datasets_table(counts: dict) -> str:
    lines = ["| Dataset | File | CSV | Entities | Last updated | Version |",
             "|---|---|---|---|---|---|"]
    for stem, label, _, _ in DATASETS:
        c = counts[stem]
        lines.append(
            f"| {label} | [{stem}.json]({json_url(stem)}) | [{stem}.csv]({csv_url(stem)}) "
            f"| {c['n']} | {c['date']} | {c['version']} |"
        )
    return "\n".join(lines)


def _h2(stem: str, counts: dict) -> str:
    c = counts[stem]
    noun_h2 = dict((d[0], d[3]) for d in DATASETS)[stem]
    return f"## {dict((d[0], d[1]) for d in DATASETS)[stem]} — {c['n']} {noun_h2}"


def render(key: str, counts: dict) -> str:
    if key == "index-table":
        return _index_table(counts)
    if key == "datasets-table":
        return _datasets_table(counts)
    if key == "readme-table":
        return _readme_table(counts)
    if key.startswith("h2-"):
        return _h2(key[3:], counts)
    if key.startswith("date-"):
        return counts[key[5:]]["date"]
    if key.startswith("version-"):
        return counts[key[8:]]["version"]
    raise ValueError(f"unknown marker key: {key}")


# marker key -> (relative file, inline?)
TARGETS: list[tuple[str, str, bool]] = []
TARGETS.append(("docs/index.md", "index-table", False))
TARGETS.append(("docs/datasets.md", "datasets-table", False))
for stem, *_ in DATASETS:
    TARGETS.append(("docs/datasets.md", f"h2-{stem}", False))
TARGETS.append(("README.md", "readme-table", False))
for stem, *_ in DATASETS:
    if stem == "relationships":
        continue
    TARGETS.append((f"docs/{stem}.md", f"date-{stem}", True))
    TARGETS.append((f"docs/{stem}.md", f"version-{stem}", True))


def start_marker(key: str) -> str:
    return f"<!-- AUTO:counts:{key} -->"


def end_marker(key: str) -> str:
    return f"<!-- /AUTO:counts:{key} -->"


def inject_text(text: str, key: str, content: str, inline: bool) -> str:
    start, end = start_marker(key), end_marker(key)
    if inline:
        pattern = re.compile(re.escape(start) + r"[^\n]*" + re.escape(end))
        new = start + content + end
    else:
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
        new = start + "\n" + content + "\n" + end
    if not pattern.search(text):
        raise SystemExit(f"ERROR: marker '{key}' not found in target")
    return pattern.sub(new, text, count=1)


def extract_text(text: str, key: str, inline: bool) -> str | None:
    start, end = start_marker(key), end_marker(key)
    if inline:
        m = re.search(re.escape(start) + r"(.*?)" + re.escape(end), text)
        return m.group(1) if m else None
    m = re.search(re.escape(start) + r"(.*?)" + re.escape(end), text, re.DOTALL)
    return m.group(1).strip() if m else None


def inject_all(counts: dict) -> None:
    for rel, key, inline in TARGETS:
        path = REPO_ROOT / rel
        text = path.read_text(encoding="utf-8")
        updated = inject_text(text, key, render(key, counts), inline)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(f"injected {rel} [{key}]")
        else:
            print(f"unchanged {rel} [{key}]")


def main() -> None:
    counts = read_counts()
    inject_all(counts)
    print("inject-counts.py: done")


if __name__ == "__main__":
    sys.exit(main())
