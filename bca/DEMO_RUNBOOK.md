# Demo Runbook — Architecture as Code: Three Additions

> **FICTITIOUS DEMO CONTENT.** NovaCorp, Project WAYFINDER, and all products are invented.
> **Time:** about 3 minutes. **Story:** add a managed SOC partner in three additions (element, risk, strategy), and watch the guardrails and the page respond to each one.

---

## Before the session (5 minutes)

1. In the VS Code terminal (**Terminal → New Terminal**):
   ```bash
   cd ~/Documents/archascode
   git pull
   source .venv/bin/activate
   python scripts/demo_bca.py reset
   ```
   The last line ends with **0 error(s), 3 warning(s)**.
2. Start the live preview and leave it running:
   ```bash
   mkdocs serve
   ```
3. In the browser, open **http://127.0.0.1:8000/archascode/bca/novacorp-wayfinder/**
   The address must include **/archascode/**.
4. Open a **second terminal** (click **+** in the terminal panel), then run `source .venv/bin/activate`.
5. In VS Code, open `bca/engagements/novacorp/wayfinder/model.yaml`, so the audience sees each addition appear.

**Backups:** the fallback image on local disk, and the published site in another tab:
robertrostsource.github.io/archascode/bca/novacorp-wayfinder/

---

## Live: three additions (all commands in the second terminal)

### Addition 1: the element

```bash
python scripts/demo_bca.py 1
```

- **You see:** "Managed SOC provider" appears in the Partners block of `model.yaml`. The result is **0 errors, 3 warnings**.
- **Say:** "Domains hold the organization's own elements. We just added a partner."

### Addition 2: the risk to value

```bash
python scripts/demo_bca.py 2
```

- **You see:** RSK-07 appears under `risks:`. The validator reports **ERROR RSK-07: unknown strategy STR-06**.
- **Say:** "A risk without a mitigation strategy doesn't get in."

### Addition 3: the strategy and its attributes

```bash
python scripts/demo_bca.py 3
```

- **You see:** STR-06 appears under `strategies:`. The result is **0 errors, 3 warnings**.
- **Say:** "The three gaps stay. Hold on to them; the next two demos come back to them."

### Show the page

Switch to the browser and refresh (**Cmd+Shift+R**):

- **4.0 Worksheet:** the Partners box lists *Managed SOC provider*.
- **5.1 Top Risks:** RSK-07.
- **5.2 Strategies:** STR-06, with *Vetted, Monitored, Assured, Risk-Managed*.
- **5.3 Attributes by Domain:** Partners now shows those attributes. Nobody typed them there.

**Say:** "The attributes abstract the strategy, and they become the NFRs of the Conceptual Architecture. Three additions, and the whole chain stays consistent."

### Reset for the next run

```bash
python scripts/demo_bca.py reset
```

---

## If something goes wrong

| Symptom | Fix |
|---|---|
| Page shows "404" or is blank | Use the full address, including `/archascode/`. |
| Page does not change | Press **Cmd+Shift+R**. If it still has not changed, press **Ctrl+C** in the preview terminal and run `mkdocs serve` again. |
| `command not found` or `No module named yaml` | Run `source .venv/bin/activate`. |
| `No such file or directory` | Run `cd ~/Documents/archascode`. |
| "Partners block not in its starting form" | Run `python scripts/demo_bca.py reset`, then start again at Addition 1. |
| Anything else on stage | Switch to the fallback image or the published site and keep talking. |

---

## Chain to narrate

`Value ← Risk (lands on elements in a domain) ← Mitigation strategy → Attributes → Conceptual NFRs`
