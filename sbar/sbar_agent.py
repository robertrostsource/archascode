#!/usr/bin/env python3
"""
Architecture SBAR Agent - Claude edition
"Structured Thinking. Clear Communication."

Single-pass agent: reads architecture evidence (notes, transcripts, emails),
applies the Architecture SBAR Agent core instructions as the system prompt,
streams a one-page SBAR from Claude, then runs deterministic quality checks
from Section 7 of the instructions.

Usage:
    export ANTHROPIC_API_KEY=...
    python sbar_agent.py examples/inputs/novacorp_vpn_ztna_meeting_notes.md

    # Rehearsal / safety modes
    python sbar_agent.py examples/inputs/... --dry-run          # show what would be sent, no API call
    python sbar_agent.py --check outputs/some_sbar.md  # run quality checks only
    python sbar_agent.py examples/inputs/... --fallback examples/outputs/<file>.md
        # if the API call fails, show the pre-rendered SBAR (clearly labeled)
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTRUCTIONS = HERE / "instructions.md"
DEFAULT_MODEL = os.environ.get("SBAR_MODEL", "claude-sonnet-4-5")

REQUIRED_SECTIONS = [
    "BLUF",
    "Situation",
    "Background",
    "Assessment",
    "Recommendation",
    "Decision Requested",
    "Sources",
]
CORE_SECTIONS = REQUIRED_SECTIONS + ["Open Questions"]  # counted toward word limit
ACTION_VERBS = ["approve", "endorse", "select", "defer", "reject", "confirm", "assign", "authorize"]

# Runtime addendum: tells Claude how to shape output for this runner.
# The core instructions file stays untouched so it remains portable
# between Claude and M365 Copilot.
RUNTIME_ADDENDUM = """
---

## Runtime Context (Claude runner)

- Today's date is {today}. Use it in the title unless the input supplies a different decision date for the SBAR itself.
- Output ONLY the ready-to-paste repository content from Section 10, in Markdown, starting with the `# [SBAR] ...` title line.
- Include the Repository Location, Labels, and ADR Need lines under the title.
- Use `##` headings exactly as named: BLUF, Situation, Background, Assessment, Recommendation, Decision Requested, Open Questions (if needed), Sources, ADR Follow-up, Sharing Guidance.
- The words from BLUF through Sources must total 350 to 500 (10% tolerance). No more than three bullets per section.
- Do not add preamble, commentary, or a closing note outside the SBAR.
"""


# --------------------------------------------------------------------------- #
# Prompt assembly
# --------------------------------------------------------------------------- #
def build_system_prompt(today: str) -> str:
    core = INSTRUCTIONS.read_text(encoding="utf-8")
    return core + RUNTIME_ADDENDUM.format(today=today)


def build_user_message(evidence: str, source_name: str) -> str:
    return (
        "Convert the following evidence into an SBAR per your instructions.\n\n"
        f"<evidence source=\"{source_name}\" type=\"user-provided\">\n"
        f"{evidence}\n"
        "</evidence>"
    )


# --------------------------------------------------------------------------- #
# Quality checks (Section 7) - deterministic, no model involved
# --------------------------------------------------------------------------- #
def split_sections(md: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current = None
    buf: list[str] = []
    for line in md.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if current:
                sections[current] = "\n".join(buf).strip()
            current, buf = m.group(1).strip(), []
        elif current:
            buf.append(line)
    if current:
        sections[current] = "\n".join(buf).strip()
    return sections


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9$%][\w$%./,'-]*", text))


def run_checks(md: str) -> list[tuple[bool, str]]:
    results: list[tuple[bool, str]] = []
    sections = split_sections(md)
    headings = list(sections.keys())

    title = next((l for l in md.splitlines() if l.startswith("# ")), "")
    results.append((bool(re.match(r"^# \[SBAR\] .+ - (\d{4}-\d{2}-\d{2}|Needs Validation)$", title)),
                    f"Title format: {title or '(missing)'}"))

    missing = [s for s in REQUIRED_SECTIONS if s not in sections]
    results.append((not missing, "All required sections present" if not missing
                    else f"Missing sections: {', '.join(missing)}"))

    results.append((bool(headings) and headings[0] == "BLUF", "BLUF is the first section"))

    words = sum(word_count(sections.get(s, "")) for s in CORE_SECTIONS)
    results.append((315 <= words <= 550, f"Word count {words} (target 350-500, +/-10%)"))

    over = [s for s in CORE_SECTIONS
            if len(re.findall(r"^\s*[-*]\s+", sections.get(s, ""), re.M)) > 3]
    results.append((not over, "Max three bullets per section" if not over
                    else f"Too many bullets: {', '.join(over)}"))

    decision = sections.get("Decision Requested", "").lower()
    ok_decision = decision.startswith("none - informational") or any(v in decision for v in ACTION_VERBS)
    results.append((ok_decision, "Decision Requested uses an action verb"))

    placeholder = re.search(r"<[A-Z][^>]{2,}>|\bTBD\b|lorem ipsum", md, re.I)
    results.append((not placeholder, "No placeholder text" if not placeholder
                    else f"Placeholder found: {placeholder.group(0)}"))

    adr = re.search(r"\*\*ADR Need:\*\*\s*(Yes|No|Unknown)", md)
    results.append((bool(adr), f"ADR need stated: {adr.group(1) if adr else '(missing)'}"))

    approved = None
    for m in re.finditer(r"\b(was|has been|is|were|have been) approved\b", md, re.I):
        before = md[max(0, m.start() - 30):m.start()].lower()
        if not re.search(r"\b(no|not|nothing|none|neither)\b", before):
            approved = m
            break
    results.append((not approved, "No implied approval" if not approved
                    else f"Possible implied approval: '{approved.group(0)}'"))

    return results


def print_checks(results: list[tuple[bool, str]]) -> bool:
    print("\n" + "=" * 64)
    print(" QUALITY CHECKS (Section 7)")
    print("=" * 64)
    for ok, msg in results:
        print(f" [{'PASS' if ok else 'FAIL'}] {msg}")
    passed = sum(ok for ok, _ in results)
    print("-" * 64)
    print(f" {passed}/{len(results)} checks passed")
    print("=" * 64)
    return passed == len(results)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def slugify(title_line: str) -> str:
    t = re.sub(r"^# \[SBAR\]\s*", "", title_line)
    return re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-")[:80] or "SBAR"


def generate(system: str, user: str, model: str) -> str:
    import anthropic  # imported here so --dry-run and --check work without the SDK

    client = anthropic.Anthropic()
    chunks: list[str] = []
    with client.messages.stream(
        model=model,
        max_tokens=2000,
        system=system,
        messages=[{"role": "user", "content": user}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            chunks.append(text)
    print()
    return "".join(chunks).strip()


def main() -> int:
    p = argparse.ArgumentParser(description="Architecture SBAR Agent (Claude)")
    p.add_argument("input", nargs="?", help="Evidence file: notes, transcript, email, doc (.md/.txt)")
    p.add_argument("--out", default=str(HERE / "outputs"), help="Output directory")
    p.add_argument("--model", default=DEFAULT_MODEL, help=f"Claude model (default {DEFAULT_MODEL}, or SBAR_MODEL env)")
    p.add_argument("--date", default=dt.date.today().isoformat(), help="Date for the SBAR title (YYYY-MM-DD)")
    p.add_argument("--dry-run", action="store_true", help="Show prompt sizes and exit without calling the API")
    p.add_argument("--check", metavar="SBAR_MD", help="Run quality checks on an existing SBAR and exit")
    p.add_argument("--fallback", metavar="SBAR_MD", help="Pre-rendered SBAR to show if the API call fails")
    args = p.parse_args()

    if args.check:
        return 0 if print_checks(run_checks(Path(args.check).read_text(encoding="utf-8"))) else 1

    if not args.input:
        p.error("an input file is required (or use --check)")

    src = Path(args.input)
    evidence = src.read_text(encoding="utf-8")
    system = build_system_prompt(args.date)
    user = build_user_message(evidence, src.name)

    print("=" * 64)
    print(" ARCHITECTURE SBAR AGENT  |  Structured Thinking. Clear Communication.")
    print("=" * 64)
    print(f" Evidence : {src.name} ({word_count(evidence)} words)")
    print(f" Model    : {args.model}")
    print(f" Date     : {args.date}")
    print("=" * 64 + "\n")

    if args.dry_run:
        print(f"[dry-run] System prompt: {len(system):,} chars | User message: {len(user):,} chars")
        print("[dry-run] No API call made.")
        return 0

    try:
        sbar = generate(system, user, args.model)
        label = ""
    except Exception as exc:  # demo safety net
        if not args.fallback:
            print(f"\n[ERROR] API call failed: {exc}", file=sys.stderr)
            return 2
        print(f"\n[FALLBACK] API call failed ({type(exc).__name__}). Showing PRE-RENDERED output.\n")
        sbar = Path(args.fallback).read_text(encoding="utf-8").strip()
        print(sbar)
        label = "-FALLBACK"

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    title = next((l for l in sbar.splitlines() if l.startswith("# ")), "# [SBAR] Output")
    out_file = out_dir / f"{slugify(title)}{label}.md"
    out_file.write_text(sbar + "\n", encoding="utf-8")

    all_ok = print_checks(run_checks(sbar))
    print(f"\n Saved: {out_file.relative_to(HERE) if out_file.is_relative_to(HERE) else out_file}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
