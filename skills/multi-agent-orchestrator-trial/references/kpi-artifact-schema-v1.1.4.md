# KPI Artifact Schema (v1.1.4)

## Purpose
Add real token/cost telemetry and trace linkage to KPI artifacts.

## KPI JSON Schema (operational)
```json
{
  "run_id": "string",
  "trace_id": "string",
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
    "cost_usd": 0.0,
    "token_source": "real|mixed|proxy",
    "tool_calls": 0,
    "retries": 0,
    "timeouts": 0,
    "prompt_chars_in": 0,
    "output_chars_out": 0,
    "proxy_cost": 0
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

## Release-Critical Metrics
- pass_rate
- timeout_rate
- retry_rate
- avg_total_sec
- avg_tokens_per_pass
- avg_cost_usd_per_pass
