#!/usr/bin/env python3
"""Validate a BCA model: JSON Schema, then library cross-references and completeness.

Usage: python scripts/validate_bca.py engagements/<name>/model.yaml
Exit code 0 = valid and complete, 1 = errors, 2 = complete-with-warnings is not used (warnings print only).
"""
import json, sys, pathlib
import yaml
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load(p):
    return yaml.safe_load(open(p, encoding="utf-8"))


def main(model_path):
    model = load(model_path)
    schema = json.load(open(ROOT / "schemas/bca_model.schema.json", encoding="utf-8"))
    dom_names = {d["id"]: d["name"] for d in load(ROOT / "library/taxonomy/domains.yaml")["domains"]}
    domains = set(dom_names)
    attributes = {a["id"] for a in load(ROOT / "library/attributes.yaml")["attributes"]}
    outcomes_lib = {o["id"] for o in load(ROOT / "library/business_outcomes.yaml")["outcomes"]}

    errors, warnings = [], []
    for e in Draft202012Validator(schema).iter_errors(model):
        errors.append(f"schema: {'/'.join(map(str, e.path))}: {e.message}")
    if errors:
        report(errors, warnings); return 1

    vals = {v["id"] for v in model["value"]}
    strategies_lib = {s["id"] for s in load(ROOT / "library/strategies.yaml")["strategies"]}
    risks = {r["id"]: r for r in model["risks"]}
    strategies = {s["id"]: s for s in model["strategies"]}

    def dom(ref, where):
        if ref not in domains:
            errors.append(f"{where}: unknown domain {ref}")

    # Business outcomes: value created, never a quality attribute.
    for b in model["business_outcomes"]:
        for v in b["creates_value"]:
            if v not in vals: errors.append(f"{b['id']}: unknown value {v}")
        for d in b["domains"]: dom(d, b["id"])
        if b.get("library_ref") and b["library_ref"] not in outcomes_lib:
            warnings.append(f"{b['id']}: library_ref {b['library_ref']} not in library")
        if b["name"] in attributes:
            errors.append(f"{b['id']}: '{b['name']}' is an attribute, not an outcome. "
                          "Attributes abstract mitigation strategies; record it on a strategy.")

    # Risks to value: located in a domain, answered by strategies.
    for r in model["risks"]:
        dom(r["domain"], r["id"])
        for v in r["threatens"]:
            if v not in vals: errors.append(f"{r['id']}: threatens unknown value {v}")
        for s in r.get("strategies", []):
            if s not in strategies: errors.append(f"{r['id']}: unknown strategy {s}")
        answered = set(r.get("strategies", [])) | {s["id"] for s in model["strategies"] if r["id"] in s["mitigates"]}
        if r["treatment"] != "Accept" and not answered:
            errors.append(f"{r['id']}: no mitigation strategy. Every risk not accepted needs at least one.")
    risk_domains = {r["domain"] for r in model["risks"]}
    if len(model["risks"]) >= 5 and len(risk_domains) < 3:
        warnings.append(f"Top risks sit in only {len(risk_domains)} domain(s). Look across all impacted domains.")

    # Strategies: mitigate risks, apply to domains, abstracted by attributes.
    for s in model["strategies"]:
        for rid in s["mitigates"]:
            if rid not in risks: errors.append(f"{s['id']}: mitigates unknown risk {rid}")
        for d in s["domains"]: dom(d, s["id"])
        for a in s["attributes"]:
            if a not in attributes: errors.append(f"{s['id']}: unknown attribute {a}")
        if s.get("library_ref") and s["library_ref"] not in strategies_lib:
            warnings.append(f"{s['id']}: library_ref {s['library_ref']} not in library/strategies.yaml")

    covered = {i["domain"] for i in model["domain_impact"]}
    for i in model["domain_impact"]: dom(i["domain"], "domain_impact")
    for missing in sorted(domains - covered):
        warnings.append(f"GAP {dom_names[missing]} ({missing}): not assessed. Absence is a decision.")
    for i in model["domain_impact"]:
        if i["impact"] == "none" and not i.get("confirmed_empty"):
            warnings.append(f"GAP {dom_names[i['domain']]} ({i['domain']}): marked not impacted, but no human confirmed it.")

    # Every impacted leaf domain must show the organization's own elements.
    tax = load(ROOT / "library/taxonomy/domains.yaml")["domains"]
    containers = {d["parent"] for d in tax if d["parent"]}
    for i in model["domain_impact"]:
        if i["impact"] != "none" and i["domain"] not in containers and not i.get("elements"):
            errors.append(f"{dom_names[i['domain']]} ({i['domain']}): impacted but lists no elements. "
                          "Extract them from the inputs; see extract_from in library/taxonomy/domains.yaml.")

    if not model["scope"]["out"]:
        errors.append("scope: no out-of-scope statements")

    report(errors, warnings)
    return 1 if errors else 0


def report(errors, warnings):
    for e in errors: print(f"ERROR   {e}")
    for w in warnings: print(f"WARNING {w}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
