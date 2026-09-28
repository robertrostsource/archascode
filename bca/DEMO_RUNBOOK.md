# Demo Runbook — Architecture as Code: Type Three Additions

> **FICTITIOUS DEMO CONTENT.** NovaCorp, Project WAYFINDER, and all products are invented.
> **Time:** about 4 minutes. **Story:** type three additions into the model (element, risk, strategy) and watch the guardrails and the page respond.
> **Local only.** Nothing is pushed to GitHub during the demo.

---

## The night before (once)

In VS Code, choose **Terminal → New Terminal**, then type:

```
git pull
```

## Before the session

In VS Code, choose **Terminal → New Terminal**, then type:

```
source .venv/bin/activate
mkdocs serve
```

Open in the browser: **http://127.0.0.1:8000/archascode/bca/novacorp-wayfinder/**

Open a **second terminal** (click **+** in the terminal panel) and type:

```
source .venv/bin/activate
```

Open the file `bca/engagements/novacorp/wayfinder/model.yaml`.

---

## Addition 1: the element

Press **Cmd+F** and search for `Contractor firms`. At the end of that line, press **Enter** and type:

```yaml
      - Managed SOC provider
```

(The dash lines up with the dash on the line above.) Save with **Cmd+S**.

**Say:** "Domains hold the organization's own elements. We just added a partner."

---

## Addition 2: the risk

Search for `RSK-06`. At the end of that line, press **Enter** and type:

```yaml
  - id: RSK-07
    statement: Compromised SOC partner reaches NovaCorp data
    threatens: [VAL-02]
    domain: AEF-LOC-0037
    treatment: Mitigate
    strategies: [STR-06]
```

Save with **Cmd+S**. In the second terminal, type:

```
python scripts/validate_bca.py bca/engagements/novacorp/wayfinder/model.yaml
```

Result: **ERROR RSK-07: unknown strategy STR-06**

**Say:** "A risk without a mitigation strategy doesn't get in."

---

## Addition 3: the strategy

Search for `STR-05`. At the end of that line, press **Enter** and type:

```yaml
  - id: STR-06
    statement: Vet and monitor the SOC partner
    mitigates: [RSK-07]
    domains: [AEF-LOC-0037]
    attributes: [Vetted, Monitored, Assured]
```

Save with **Cmd+S**. Run the validator again (press the **Up arrow**, then **Enter**).

Result: **0 errors, 3 warnings**

**Say:** "The three gaps stay. Hold on to them; the next two demos come back to them."

---

## Show the page

Refresh the browser (**Cmd+Shift+R**) and scroll through:

- **4.0 Worksheet:** the Partners box lists *Managed SOC provider*.
- **5.1 Top Risks:** RSK-07.
- **5.2 Strategies:** STR-06 with *Vetted, Monitored, Assured*.
- **5.3 Attributes by Domain:** Partners now shows those attributes. Nobody typed them there.

**Say:** "I wrote the model; everything else was generated. The attributes become the NFRs of the Conceptual Architecture."

**Say (instead of pushing live):** "In practice this change goes to a pull request. The pipeline runs this same validator, and on merge the published site updates." Point to the published site tab.

---

## Reset for the next run

In the second terminal:

```
git restore bca/engagements/novacorp/wayfinder/model.yaml
```

---

## Typing rules

- Indent with **spaces**, never Tab. Addition 1 starts with 6 spaces; Additions 2 and 3 start with 2 spaces before the dash and 4 spaces on the lines below it.
- A red squiggle in VS Code means the indentation is off. Line it up with the entries above it.

## If something goes wrong

| Symptom | Fix |
|---|---|
| Page shows "404" or is blank | Use the full address, including `/archascode/`. |
| Page does not change | Check the file is saved, then press **Cmd+Shift+R**. |
| `command not found` | Run `source .venv/bin/activate`. |
| Schema or YAML error after typing | Check the indentation against the entries above. |
| Worksheet diagram shows as text | The diagram needs internet access. Switch to the fallback image. |
| Anything else on stage | Run the reset command, or switch to the published site and keep talking. |
