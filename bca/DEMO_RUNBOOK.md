# Demo Runbook — Architecture as Code: Add a Partner

> **FICTITIOUS DEMO CONTENT.** NovaCorp, Project WAYFINDER, and all products are invented.
> **Time:** about 3 minutes. **Story:** one YAML edit flows through validation into the worksheet, the top risks, the strategies, and the attributes.

---

## Before the session (5 minutes)

1. In Terminal: `cd ~/Documents/archascode && git pull`
2. Open the folder in VS Code (**File → Open Folder → Documents → archascode**).
3. Open the terminal (**Ctrl+`**) and activate Python: `source .venv/bin/activate` (the prompt shows `(.venv)`).
4. Confirm the baseline:
   ```bash
   python scripts/validate_bca.py bca/engagements/novacorp/wayfinder/model.yaml
   ```
   Expected result: **0 errors, 3 warnings** (GAP Processes, GAP Data, GAP Suppliers).
5. Start the live preview and leave it running:
   ```bash
   mkdocs serve
   ```
6. In the browser, open **http://127.0.0.1:8000/archascode/bca/novacorp-wayfinder/**
   > The address must include **/archascode/**. Without it, the page is blank or shows "404".
7. Open a **second terminal** for the validator: click **+** in the terminal panel, then run `source .venv/bin/activate`.
8. In VS Code, open `bca/engagements/novacorp/wayfinder/model.yaml`.

**Backups:** Keep the fallback image on local disk, and keep the live site open in a separate tab:
robertrostsource.github.io/archascode/bca/novacorp-wayfinder/

---

## Live steps

### 1. Add the element (Partners)

Find this block, around line 102:

```yaml
  - domain: AEF-LOC-0037
    impact: low
    elements:
      - {name: Contractor firms, source: "Conceptual FR2, UC02"}
```

Change `low` to `medium`, and add the last line:

```yaml
  - domain: AEF-LOC-0037
    impact: medium
    elements:
      - {name: Contractor firms, source: "Conceptual FR2, UC02"}
      - {name: Managed SOC provider, source: "Live demo"}
```

**Say:** "The domains hold the organization's own elements: its people, systems, and parties. We just added a partner."

### 2. Add a risk to value

Under `risks:`, click at the end of the **RSK-06** line, press Enter, and paste (keep the two leading spaces):

```yaml
  - {id: RSK-07, rank: 7, statement: "A compromised managed SOC provider is used to reach NovaCorp sessions and logs", threatens: [VAL-02], domain: AEF-LOC-0037, elements: [Managed SOC provider], likelihood: Low, impact: High, treatment: Mitigate, strategies: [STR-06]}
```

Save with **Cmd+S**.

### 3. Show the guardrail

In the second terminal:

```bash
python scripts/validate_bca.py bca/engagements/novacorp/wayfinder/model.yaml
```

Expected result: **ERROR RSK-07: unknown strategy STR-06** (1 error, 3 warnings).

**Say:** "A risk without a mitigation strategy doesn't get in."

### 4. Add the strategy and its attributes

Under `strategies:`, click at the end of the **STR-05** line, press Enter, and paste:

```yaml
  - {id: STR-06, library_ref: STR-THIRD-PARTY-ASSURANCE, name: Assure the SOC partner, statement: "Vet, contract, and monitor the managed SOC provider in proportion to its access.", mitigates: [RSK-07], domains: [AEF-LOC-0037], attributes: [Vetted, Monitored, Assured, Risk-Managed]}
```

Save with **Cmd+S**.

### 5. Validate again

Run the same command. Expected result: **0 errors, 3 warnings**.

**Say:** "The three gaps stay. Hold on to them; the next two demos come back to them."

### 6. Show the result

Switch to the browser tab. The page refreshes by itself after each save; if it does not, press **Cmd+Shift+R**. Walk top to bottom:

- **4.0 Domain Impact Worksheet:** the Partners box now lists *Managed SOC provider*.
- **5.1 Top Risks to Value:** RSK-07 appears.
- **5.2 Mitigation Strategies and Attributes:** STR-06, with *Vetted, Monitored, Assured, Risk-Managed*.
- **5.3 Attributes by Domain (derived):** Partners now shows those attributes. Nobody typed them there.

**Say:** "These attributes abstract the strategy. They become the NFRs the Conceptual Architecture must meet. One edit, and the whole chain stays consistent."

### 7. Reset for the next run

- **Source Control** panel (branching icon) → right-click `model.yaml` → **Discard Changes**.
- Validate again and confirm **0 errors, 3 warnings**.

---

## If something goes wrong

| Symptom | Fix |
|---|---|
| Page shows "404" or is blank | Use the full address, including `/archascode/`: http://127.0.0.1:8000/archascode/bca/novacorp-wayfinder/ |
| Page does not show the change | Check the file is saved (no dot on the VS Code tab). Press **Cmd+Shift+R**. If it still has not changed, press **Ctrl+C** in the preview terminal and run `mkdocs serve` again. |
| `command not found: mkdocs` or `No module named yaml` | The virtual environment is not active. Run `source .venv/bin/activate`. |
| `No such file or directory` | The terminal is in the wrong folder. Run `cd ~/Documents/archascode`. |
| YAML or schema error after pasting | Check that the pasted line starts with exactly two spaces and a dash, aligned with the lines above it. |
| Anything else on stage | Switch to the fallback image or the live site tab and keep talking. |

---

## Chain to narrate

`Value ← Risk (lands on elements in a domain) ← Mitigation strategy → Attributes → Conceptual NFRs`
