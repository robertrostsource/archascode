"""MkDocs hook: regenerate BCA and library pages before every build.

With this hook, `mkdocs serve` refreshes the site whenever a model.yaml or a
library file is saved (see `watch:` in mkdocs.yml). No manual rebuild needed.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_docs  # noqa: E402


def on_pre_build(config, **kwargs):
    try:
        build_docs.main(quiet=True)
    except Exception as exc:  # keep serving; show the problem in the terminal
        print(f"WARNING build_docs failed: {exc}. Run scripts/validate_bca.py for details.")
