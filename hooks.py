"""MkDocs hooks.

1) Copy datasets/*.json (single source) into the built site.
2) Generate flat CSV distribution packages (UTF-8 BOM) into site/downloads/
   via scripts/export_csv.py — idempotent, re-runs on every build.
"""
import shutil
import sys
from pathlib import Path


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
