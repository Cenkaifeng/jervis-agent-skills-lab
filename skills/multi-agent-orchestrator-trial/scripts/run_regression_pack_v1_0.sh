#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LINT="$ROOT/skills/multi-agent-orchestrator-trial/scripts/runtime_lint_v0_8.py"
OUTDIR="$ROOT/reports/multi-agent-regression"
mkdir -p "$OUTDIR"

echo "[R3] taishi hard-gate + scoring lint"
cat > "$OUTDIR/taishi_r3.json" <<'EOF'
{
  "schema_version": "handoff.v1",
  "task_id": "R3-TEST",
  "agent": "taishi",
  "verdict": "fail",
  "scores": {"quality": 3, "security": 2, "completeness": 4, "total": 9},
  "fix_list": ["[P0] security_blocker"],
  "release_blockers": ["security_blocker"],
  "acceptance_check": ["criterion A: pass"],
  "security_check": ["boundary1: fail"],
  "next_action": "return_to_jarvis"
}
EOF

cat > "$OUTDIR/final_r3.json" <<'EOF'
{
  "schema_version": "final.v1",
  "goal": "regression R3",
  "outcome": "hard gate simulation",
  "evidence": ["simulated"],
  "risks_boundaries": ["simulated"],
  "completed": ["schema check"],
  "needs_human_confirmation": [],
  "next_steps": ["none"]
}
EOF

python3 "$LINT" "$OUTDIR/taishi_r3.json" "$OUTDIR/final_r3.json"
echo "PASS: regression pack minimal checks done"
