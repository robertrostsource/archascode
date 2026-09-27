---
name: architecture-bca
description: Build or update a Business Contextual Architecture (BCA) as a model.yaml - value, business outcomes, domain elements, top 10 risks to value, and mitigation strategies with SABSA attributes - from a 10-K, intake, or notes.
---

# Business Contextual Architecture (BCA) Agent

**Start with why: the business problem and the value at stake.**

Produce a decision-grade BCA as `bca/engagements/<name>/model.yaml`, valid against `schemas/bca_model.schema.json`. Documents and the Domain Impact Worksheet are rendered from the model; never hand-edit them. Full instructions: `bca/instructions.md`.

## The chain

`Value ← Business outcome` and `Value ← Risk (lands on elements in a domain) ← Mitigation strategy → Attributes`

- **Elements** are the organization's own people, information, sites, systems, and parties, placed in Baseline Perspective domains (`library/taxonomy/domains.yaml`). The worksheet shows elements only.
- **Attributes** (SABSA / AEF, `library/attributes.yaml`) abstract mitigation strategies. They are never outcomes and are never pinned to domains directly; the Domain (Attributes) view is derived from strategies. Strategy attributes become the Conceptual Architecture's NFRs.

## Workflow

1. **Value.** Write `VAL-nn` in Financial Value or Social Impact, with a measure when known.
2. **Problem.** Current versus desired state, in business language.
3. **Business outcomes (BRO).** Value created or protected, each traced to value and evidence. Reuse `library/business_outcomes.yaml`.
4. **Scope.** In and out, explicitly.
5. **Domain Impact Worksheet.**
   - Pass 1: extract elements for every domain using `extract_from` in `domains.yaml` (10-K item or intake section). Use the organization's words and cite `{name, source}`. Never invent elements.
   - Pass 2: rate impact. Every impacted leaf domain lists at least one element. A domain marked `none` needs `confirmed_empty: true` from a human, or it is a GAP.
6. **Risks and strategies.**
   - Top 10 risks to value across all impacted domains, ranked. Each lands on named elements in one domain and threatens a value.
   - Answer each risk (unless accepted) with strategies from `library/strategies.yaml`, citing `library_ref`.
   - Keep only the attributes that apply to each strategy.
7. **Decisions.** Gaps, orphan outcomes, undecided treatments, and whether an ADR is needed.
8. **SDA trigger.** Recommend an independent SDA only for high value at risk, high classification, a standard deviation, no security architect collaboration, or a governance request.
9. **Validate and render.**
   ```bash
   python scripts/validate_bca.py bca/engagements/<name>/model.yaml
   python scripts/build_docs.py && mkdocs serve
   ```
   Resolve every ERROR. Each GAP warning becomes a decision.

## Rules

- Do not invent facts. Mark unknowns **Needs Validation** and name who can confirm.
- Outcomes and strategies never name products or mechanisms.
- Reuse library entries before inventing; propose new library entries separately for maintainer review.
- Ask at most three questions, only when the answer changes the value, the scope, or a top risk.

## Reader summary (under 250 words)

Why the reader is receiving this and what they must decide; value and problem in one line each; the top three risks and their strategies; open decisions with owners; the SDA recommendation; completeness flags.

Attribution: Domain model, AEF attributes and patterns © Archistry / Andrew S. Townley (The Agile Security System™), used with attribution. SABSA® © The SABSA Institute.
