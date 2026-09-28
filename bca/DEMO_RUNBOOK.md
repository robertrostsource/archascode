# Demo Runbook — Architecture as Code: Add ITAR and PCI Risks

> **FICTITIOUS DEMO CONTENT.** NovaCorp, Project WAYFINDER, and all products are invented.
> **Time:** about 4 minutes. **Story:** type new elements and risks into the model and watch the page respond.
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

## Addition 1: two new information elements

Press **Cmd+F** and search for `Engineering data`. At the end of that line, press **Enter** and type:

```yaml
      - ITAR technical data
      - Cardholder payment data
```

(The dashes line up with the dash on the line above.) Save with **Cmd+S**.

**Say:** "The Information domain holds what the business must protect. We just added ITAR data and cardholder data."

---

## Addition 2: two risks to value

Search for `RSK-06`. At the end of that line, press **Enter** and type:

```yaml
  - id: RSK-07
    statement: Loss of US military contracts due to ITAR non-compliance
    threatens: [VAL-02]
    domain: AEF-LOC-0003
    treatment: Mitigate
  - id: RSK-08
    statement: Unable to accept credit cards due to PCI DSS non-compliance
    threatens: [VAL-02]
    domain: AEF-LOC-0003
    treatment: Mitigate
```

Save with **Cmd+S**.

**Say:** "Risks are framed as value at risk: losing defense revenue, and losing the ability to take payments."

---

## Show the page

Refresh the browser (**Cmd+Shift+R**) and scroll through:

- **4.0 Worksheet:** the Information box lists *ITAR technical data* and *Cardholder payment data*.
- **5.1 Top Risks:** RSK-07 and RSK-08, located in Information.
- **Top of the page:** an "Incomplete" note says a risk has no mitigation strategy.

**Say:** "I wrote the model; everything else was generated. And the model tells us what comes next: each new risk needs a mitigation strategy, whose attributes become the NFRs of the Conceptual Architecture."

**Say (instead of pushing live):** "In practice this change goes to a pull request, and on merge the published site updates." Point to the published site tab.

---

## Reset for the next run

In the second terminal:

```
git restore bca/engagements/novacorp/wayfinder/model.yaml
```

---

## Typing rules

- Indent with **spaces**, never Tab. Addition 1 lines start with 6 spaces. In Addition 2, each `- id:` line starts with 2 spaces, and the lines below it start with 4.
- A red squiggle in VS Code means the indentation is off. Line it up with the entries above it.

## If something goes wrong

| Symptom | Fix |
|---|---|
| Page shows "404" or is blank | Use the full address, including `/archascode/`. |
| Page does not change | Check the file is saved, then press **Cmd+Shift+R**. |
| `command not found` | Run `source .venv/bin/activate`. |
| Page stops updating after typing | Usually indentation. Line your text up with the entries above, save, and refresh. |
| Worksheet diagram shows as text | The diagram needs internet access. Switch to the fallback image. |
| Anything else on stage | Run the reset command, or switch to the published site and keep talking. |
