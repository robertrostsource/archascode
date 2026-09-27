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
    bros = {b["id"] for b in model["business_outcomes"]}
    domas = {d["id"]: d for d in model["domas"]}

    def dom(ref, where):
        if ref not in domains:
            errors.append(f"{where}: unknown domain {ref}")

    for b in model["business_outcomes"]:
        for v in b["creates_value"]:
            if v not in vals: errors.append(f"{b['id']}: unknown value {v}")
        for d in b["domains"]: dom(d, b["id"])
        for d in b.get("domas", []):
            if d not in domas: errors.append(f"{b['id']}: unknown DOMA {d}")
        if b.get("library_ref") and b["library_ref"] not in outcomes_lib:
            warnings.append(f"{b['id']}: library_ref {b['library_ref']} not in library")
        if b["name"] in attributes:
            errors.append(f"{b['id']}: '{b['name']}' is an attribute, not an outcome; move it to a DOMA")

    for d in domas.values():
        dom(d["domain"], d["id"])
        for a in d["attributes"]:
            if a not in attributes: errors.append(f"{d['id']}: unknown attribute {a}")
        for b in d["supports"]:
            if b not in bros: errors.append(f"{d['id']}: supports unknown outcome {b}")

    for r in model["risks"]:
        dom(r["domain"], r["id"])
        for v in r["threatens"]:
            if v not in vals: errors.append(f"{r['id']}: threatens unknown value {v}")
        for d in r.get("domas_at_risk", []):
            if d not in domas: errors.append(f"{r['id']}: unknown DOMA {d}")

    covered = {i["domain"] for i in model["domain_impact"]}
    for i in model["domain_impact"]: dom(i["domain"], "domain_impact")
    for missing in sorted(domains - covered):
        warnings.append(f"GAP {dom_names[missing]} ({missing}): not assessed. Absence is a decision.")
    for i in model["domain_impact"]:
        if i["impact"] == "none" and not i.get("confirmed_empty"):
            warnings.append(f"GAP {dom_names[i['domain']]} ({i['domain']}): marked not impacted, but no human confirmed it.")

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
