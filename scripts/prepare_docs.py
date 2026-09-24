#!/usr/bin/env python3
"""
Copy every SBAR dropped into the top-level sbar/ folder into docs/sbar/ for MkDocs.

- Adds tags from the SBAR's **Labels:** line (so the site can filter by tag).
- Keeps the Repository Location / Labels / ADR Need lines on separate rows.
- Files that already start with front matter are copied as they are.

Runs automatically in GitHub Actions before the site is built.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, DEST = ROOT / "sbar", ROOT / "docs" / "sbar"


def prepare(text: str) -> str:
    if text.lstrip().startswith("---"):
        return text
    labels = re.search(r"^\*\*Labels:\*\*\s*(.+)$", text, re.M)
    tags = [t.strip() for t in labels.group(1).split(",") if t.strip()] if labels else ["sbar"]
    text = re.sub(r"^(\*\*(Repository Location|Labels|ADR Need):\*\*.*?)\s*$", r"\1  ", text, flags=re.M)
    return "---\ntags:\n" + "".join(f"  - {t}\n" for t in tags) + "---\n\n" + text.strip() + "\n"


DEST.mkdir(parents=True, exist_ok=True)
count = 0
for f in sorted(SRC.glob("*.md")):
    if f.name.lower() in ("index.md", "readme.md"):
        continue
    (DEST / f.name).write_text(prepare(f.read_text(encoding="utf-8")), encoding="utf-8")
    count += 1
print(f"Prepared {count} SBAR(s) for the site")
