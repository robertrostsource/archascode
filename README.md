Demo files for COSAC 2026. Use to create your own agents. All info is fake.
SBAR - Info to create agent to make an SBAR document.

BCA - Business Contextual Architecture agent: the business problem and value each solution serves, with a Domain Impact Worksheet rendered from code.

## Layout

| Path | Purpose |
|---|---|
| `bca/` | BCA agent instructions and engagement models (`bca/engagements/<name>/model.yaml`) |
| `sbar/` | SBAR agent, skill, examples, and published SBARs |
| `library/` | Reusable domains, business attributes, and business outcomes shared by all agents |
| `schemas/` | Contracts that every model must pass |
| `scripts/` | Validate models, render diagrams, generate site pages |
| `docs/` | MkDocs site; pages for SBARs, BCAs, and the library are generated at build time |

## Build the site locally

```bash
pip install -r requirements-docs.txt
python scripts/validate_bca.py bca/engagements/rogers/enterprise/model.yaml
python scripts/prepare_docs.py && python scripts/build_docs.py
mkdocs serve
```

Domain model, AEF attributes, and attribute patterns © Archistry / Andrew S. Townley (The Agile Security System™), used with attribution. SABSA® © The SABSA Institute.
