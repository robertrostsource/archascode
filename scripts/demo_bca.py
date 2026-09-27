#!/usr/bin/env python3
"""COSAC demo: add a managed SOC partner to the WAYFINDER BCA in three steps.

Each step makes one addition to model.yaml, then runs the validator, so the
audience sees the model and the guardrails change one piece at a time.

Usage (from the repo folder, with .venv active):
  python scripts/demo_bca.py reset   # back to the starting point
  python scripts/demo_bca.py 1       # add the element (Partners domain)
  python scripts/demo_bca.py 2       # add the risk to value (validator flags it)
  python scripts/demo_bca.py 3       # add the strategy and its attributes (validator passes)

Every step is safe to repeat. Steps must be run in order after a reset.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODEL = ROOT / "bca/engagements/novacorp/wayfinder/model.yaml"

PARTNER_LOW = '''  - domain: AEF-LOC-0037
    impact: low
    elements:
      - {name: Contractor firms, source: "Conceptual FR2, UC02"}
'''
PARTNER_MEDIUM = PARTNER_LOW.replace("impact: low", "impact: medium")
ELEMENT = '      - {name: Managed SOC provider, source: "Live demo"}\n'
RISK = ('  - {id: RSK-07, rank: 7, statement: "A compromised managed SOC provider is used to reach '
        'NovaCorp sessions and logs", threatens: [VAL-02], domain: AEF-LOC-0037, elements: '
        '[Managed SOC provider], likelihood: Low, impact: High, treatment: Mitigate, strategies: [STR-06]}\n')
STRATEGY = ('  - {id: STR-06, library_ref: STR-THIRD-PARTY-ASSURANCE, name: Assure the SOC partner, '
            'statement: "Vet, contract, and monitor the managed SOC provider in proportion to its access.", '
            'mitigates: [RSK-07], domains: [AEF-LOC-0037], attributes: [Vetted, Monitored, Assured, Risk-Managed]}\n')

STEPS = {
    "reset": "Starting point restored: no SOC partner, no RSK-07, no STR-06.",
    "1": "Addition 1 of 3: 'Managed SOC provider' added to the Partners domain (impact raised to medium).",
    "2": "Addition 2 of 3: risk RSK-07 added. It names strategy STR-06, which does not exist yet.",
    "3": "Addition 3 of 3: strategy STR-06 added, with attributes Vetted, Monitored, Assured, Risk-Managed.",
}


def insert_after_line(text, marker, new_line):
    """Insert new_line after the first line that contains marker."""
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if marker in line:
            lines.insert(i + 1, new_line)
            return "".join(lines)
    sys.exit(f"Could not find '{marker}' in {MODEL.name}. Run: python scripts/demo_bca.py reset")


def reset(text):
    for line in (ELEMENT, RISK, STRATEGY):
        text = text.replace(line, "")
    return text.replace(PARTNER_MEDIUM, PARTNER_LOW)


def main():
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step not in STEPS:
        sys.exit(__doc__)
    text = MODEL.read_text(encoding="utf-8")

    if step == "reset":
        text = reset(text)
    elif step == "1":
        if ELEMENT not in text:
            text = text.replace(PARTNER_LOW, PARTNER_MEDIUM + ELEMENT)
            if ELEMENT not in text:
                sys.exit("Partners block not in its starting form. Run: python scripts/demo_bca.py reset")
    elif step == "2":
        if RISK not in text:
            text = insert_after_line(text, "id: RSK-06", RISK)
    elif step == "3":
        if STRATEGY not in text:
            text = insert_after_line(text, "id: STR-05", STRATEGY)

    MODEL.write_text(text, encoding="utf-8")
    print(f"\n{STEPS[step]}\n")
    print("Validating the model...\n")
    subprocess.run([sys.executable, str(ROOT / "scripts/validate_bca.py"), str(MODEL)])
    subprocess.run([sys.executable, str(ROOT / "scripts/build_docs.py")], stdout=subprocess.DEVNULL)
    print("\nPage regenerated. Refresh the browser (Cmd+Shift+R) if it has not updated.")


if __name__ == "__main__":
    main()
