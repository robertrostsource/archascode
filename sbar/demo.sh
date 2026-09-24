#!/usr/bin/env bash
# COSAC 2026 live demo - Architecture SBAR Agent
# Usage:  ./demo.sh            live run (falls back to pre-rendered SBAR if the API fails)
#         ./demo.sh --preflight  checks setup without calling the API
set -u
cd "$(dirname "$0")"

INPUT="examples/inputs/novacorp_vpn_ztna_meeting_notes.md"
FALLBACK="examples/outputs/SBAR-Remote-Access-Future-State-VPN-to-ZTNA-2026-09-22.md"
PY="$(command -v python3 || command -v python)"

if [[ "${1:-}" == "--preflight" ]]; then
  echo "Preflight checks"
  [[ -n "$PY" ]] && echo "  [OK]   Python: $($PY --version 2>&1)" || echo "  [FAIL] Python not found"
  $PY -c "import anthropic" 2>/dev/null && echo "  [OK]   anthropic package installed" || echo "  [FAIL] run: pip3 install anthropic"
  [[ -n "${ANTHROPIC_API_KEY:-}" ]] && echo "  [OK]   ANTHROPIC_API_KEY is set" || echo "  [FAIL] ANTHROPIC_API_KEY not set"
  [[ -f "$INPUT" ]] && echo "  [OK]   Demo input found" || echo "  [FAIL] Missing $INPUT"
  [[ -f "$FALLBACK" ]] && echo "  [OK]   Fallback SBAR found" || echo "  [FAIL] Missing $FALLBACK"
  $PY sbar_agent.py "$INPUT" --dry-run >/dev/null && echo "  [OK]   Agent dry run" || echo "  [FAIL] Agent dry run"
  exit 0
fi

clear
$PY sbar_agent.py "$INPUT" --fallback "$FALLBACK"
