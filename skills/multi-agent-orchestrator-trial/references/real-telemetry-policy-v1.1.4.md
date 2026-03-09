# Real Telemetry Policy (v1.1.4)

## Goal
Replace proxy cost estimation with real token/cost telemetry wherever runtime usage is available.

## Priority Order
1. `real` (provider/runtime usage)
2. `mixed` (partial real + partial proxy)
3. `proxy` (fallback only)

## Usage Override Input
Expected file (optional):
- `reports/multi-agent-regression/usage-overrides-v1.1.4.json`

Security checks:
- run_id must exist in AB result set
- token/cost values must be non-negative and within sanity bounds
- optional `--trusted-source` validation enforces expected source label

Format:
```json
{
  "runs": [
    {
      "run_id": "20260226T000000Z-B-T04",
      "tokens_in": 1234,
      "tokens_out": 456,
      "cost_usd": 0.0189,
      "token_source": "real"
    }
  ]
}
```

## Per-run Efficiency Contract (v1.1.4)
```json
{
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
  }
}
```

## Gate Rule
Release gate should fail for `require_real_telemetry=true` when experiment token mode is not `real`.
