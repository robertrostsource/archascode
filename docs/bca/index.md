# Business Contextual Architecture

The Business Contextual Architecture (BCA) sets the context for a solution: **the business problem and the value it creates or protects**. Conceptual and component designs, ADRs, SBARs, and security assessments all trace back to it.

Each engagement page in this section is generated from a `model.yaml` file and appears in the menu automatically.

## What every BCA contains

- **Value** created or protected (financial value or social impact)
- **Problem** stated as a value gap: current versus desired state
- **Business outcomes** that trace to value and cite evidence, such as 10-K filings
- **Domain Impact Worksheet**: the organization's own elements placed in each domain, rendered from the model; unassessed domains show as gaps
- **Top 10 risks to value** across all domains, each landing on named elements
- **Mitigation strategies** answering each risk, abstracted by SABSA / AEF **business attributes**, which become the Conceptual Architecture's NFRs
- **Decisions required**, and whether an independent SDA is warranted

## How to add a BCA

1. Create `bca/engagements/<name>/model.yaml`, by hand or with the BCA agent (`bca/instructions.md`).
2. Check it: `python scripts/validate_bca.py bca/engagements/<name>/model.yaml`
3. Commit to a branch and open a pull request. The pipeline validates it and, once merged, publishes the page.

!!! note "Collaboration first"
    Security is designed in by architects working together. An independent Security Design Assessment is recommended only when risk-based triggers apply, and each page states whether it is.
