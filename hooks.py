"""MkDocs hooks.

1) Inject dataset counts / version / dateModified from datasets/*.json into the
   docs Markdown (index.md, datasets.md, README.md, docs/*.md) before the pages
   are read — via scripts/inject-counts.py. Idempotent, re-runs on every build.
2) Copy datasets/*.json (single source) into the built site.
3) Generate flat CSV distribution packages (UTF-8 BOM) into site/downloads/
   via scripts/export_csv.py — idempotent, re-runs on every build.
"""
import importlib.util
import re
import shutil
import sys
from pathlib import Path


def _load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def on_pre_build(config, **kwargs):
    """Inject counts/version/date into docs before MkDocs reads the pages.

    Runs on_pre_build (not on_post_build) because inject-counts.py rewrites the
    docs source files that feed this same build — so the rendered site must
    always carry the same numbers as the JSON.
    """
    root = Path(config.config_file_path).parent
    inject_counts = _load_module(
        "inject_counts", str(root / "scripts" / "inject-counts.py")
    )
    inject_counts.main()


def on_post_build(config, **kwargs):
    root = Path(config.config_file_path).parent

    # 1) Copy JSON datasets into site/datasets/.
    src = root / "datasets"
    dst = Path(config.site_dir) / "datasets"
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.glob("*.json"):
        shutil.copy2(f, dst / f.name)

    # 2) Generate CSV distributions into site/downloads/.
    sys.path.insert(0, str(root / "scripts"))
    import export_csv  # noqa: E402  (repo-local module)

    downloads = Path(config.site_dir) / "downloads"
    export_csv.export_all(src, downloads)

    # 3) Strip AUTO:counts marker comments from the rendered HTML. They only
    #    delimit injection regions in the Markdown source and must not leak
    #    into the served pages.
    marker_re = re.compile(r"<!--\s*/?AUTO:counts:[^>]*-->")
    for html in Path(config.site_dir).rglob("*.html"):
        text = html.read_text(encoding="utf-8")
        cleaned = marker_re.sub("", text)
        if cleaned != text:
            html.write_text(cleaned, encoding="utf-8")

    # 4) Inject Dataset JSON-LD into each dataset page (auto from JSON truth).
    import json  # noqa: E402

    site_url = (config.get("site_url") or "https://data.incenseherbs.com").rstrip("/")
    title_re = re.compile(r"(<title>.*?</title>)", re.S)
    for slug in [
        "ingredients", "terminology", "aroma", "materials", "comparisons",
        "techniques", "forms", "relationships",
    ]:
        page = Path(config.site_dir) / slug / "index.html"
        jpath = src / f"{slug}.json"
        if not page.exists() or not jpath.exists():
            continue
        try:
            data = json.loads(jpath.read_text(encoding="utf-8"))
        except Exception:
            continue
        org = {"@type": "Organization", "name": "Zhangjiakou Landeng Technology Co., Ltd."}
        ds = {
            "@context": "https://schema.org",
            "@type": "Dataset",
            "@id": f"{site_url}/{slug}/#dataset",
            "name": data.get("name", slug),
            "description": data.get("description", ""),
            "url": f"{site_url}/{slug}/",
            "version": data.get("version"),
            "dateModified": data.get("dateModified"),
            "license": data.get("license"),
            "creator": org,
            "publisher": org,
        }
        ds = {k: v for k, v in ds.items() if v is not None}
        script = (
            '<script type="application/ld+json">'
            + json.dumps(ds, ensure_ascii=False)
            + "</script>"
        )
        html = page.read_text(encoding="utf-8")
        if "application/ld+json" not in html:
            html = title_re.sub(lambda m: m.group(1) + "\n" + script, html, count=1)
            page.write_text(html, encoding="utf-8")

    # 5) Generate llms.txt from the JSON truth (no manual counts).
    def _counts(path):
        try:
            d = json.loads(path.read_text(encoding="utf-8"))
            if path.name == "relationships.json":
                return len(d.get("edges", d.get("mainEntity", [])))
            return len(d.get("mainEntity", []))
        except Exception:
            return 0

    lines = [
        "# LanDeng Open Datasets",
        "",
        "> Machine-readable knowledge datasets for Chinese botanical incense.",
        "",
        "## Datasets (JSON)",
    ]
    for slug in ["ingredients", "terminology", "aroma", "materials", "comparisons", "techniques", "forms", "relationships"]:
        jp = src / f"{slug}.json"
        n = _counts(jp)
        lines.append(f"- [{slug}]({site_url}/datasets/{slug}.json): {n} records")
    lines += [
        "",
        "## CSV downloads",
    ]
    for slug in ["ingredients", "terminology", "aroma", "materials", "comparisons", "techniques", "forms", "relationships"]:
        lines.append(f"- [{slug}.csv]({site_url}/downloads/{slug}.csv)")
    lines += [
        "",
        "## Human-readable pages",
    ]
    for slug in ["ingredients", "terminology", "aroma", "materials", "comparisons", "techniques", "forms", "relationships", "datasets"]:
        lines.append(f"- [{slug}]({site_url}/{slug}/)")
    (Path(config.site_dir) / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
