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
