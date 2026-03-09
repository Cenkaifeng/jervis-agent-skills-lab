# KPI Artifact Schema (v1.1)

> Note: superseded by `kpi-artifact-schema-v1.1.4.md` for real telemetry and trace linkage.

## Purpose
Standardize orchestration observability output for run-to-run comparison.

## KPI JSON Schema (operational)
```json
{
  "run_id": "string",
  "task_id": "string",
  "task_class": "L1|L2|L3",
  "status": "PASS|PASS_WITH_RISK|FAIL|ABORT",
  "timing": {
    "total_sec": 0,
    "jarvis_sec": 0,
    "livemore_sec": 0,
    "enkidu_sec": 0,
    "taishi_sec": 0
  },
  "quality": {
    "taishi_total": 0,
    "schema_violations": 0,
    "hard_gate_fail": false
  },
  "efficiency": {
    "tokens_in": 0,
    "tokens_out": 0,
    "tool_calls": 0,
    "retries": 0,
    "timeouts": 0
  },
  "routing": {
    "model_tiers": {"jarvis": "tier-A", "livemore": "tier-B", "enkidu": "tier-A", "taishi": "tier-A"},
    "tools_primary": ["..."],
    "fallback_used": false
  },
  "notes": ["..."]
}
```

## Required Output Path
- `reports/multi-agent-regression/kpi-<run_id>.json`

## Minimum Dash Metrics
- pass_rate
- retry_rate
- timeout_rate
- avg_total_sec
- avg_tokens_per_pass
