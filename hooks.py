"""MkDocs hook: copy datasets/*.json (single source) into the built site."""
import shutil
from pathlib import Path


def on_post_build(config, **kwargs):
    src = Path(config.config_file_path).parent / "datasets"
    dst = Path(config.site_dir) / "datasets"
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.glob("*.json"):
        shutil.copy2(f, dst / f.name)
