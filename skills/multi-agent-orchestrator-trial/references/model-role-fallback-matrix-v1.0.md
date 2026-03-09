# Model-Role Fallback Matrix (v1.0)

## Purpose
Provide stable model fallback rules per agent role when preferred models are unavailable, overloaded, or too costly.

## Role Priorities

### jarvis (orchestrator)
- Priority: planning stability, policy adherence, JSON contract discipline
- Tier order:
  1. Tier-A reasoning model (primary)
  2. Tier-B balanced model (fallback)
  3. Tier-C fast model (degraded mode, human decision for high-risk)

### livemore (research/scoping)
- Priority: evidence extraction, concise synthesis, low token cost
- Tier order:
  1. Tier-B balanced model (primary)
  2. Tier-C fast model (fallback)
  3. Tier-A reasoning model (when uncertainty score high)

### enkidu (builder/executor)
- Priority: coding reliability, deterministic edits, low hallucination
- Tier order:
  1. Tier-A coding-strong model (primary)
  2. Tier-B balanced model (fallback)
  3. Tier-C fast model (only L1 tasks)

### taishi (review/audit)
- Priority: strict scoring, safety hard-gate enforcement, schema discipline
- Tier order:
  1. Tier-A reasoning/safety model (primary)
  2. Tier-B balanced model (fallback)
  3. Tier-C fast model (requires DETAIL_MODE + human confirmation on pass_with_risk)

## Selection Rules
1. If task class is L3, avoid Tier-C for jarvis/taishi.
2. If token budget tight, downgrade livemore first, never taishi hard-gate checks.
3. If schema violations >=2 in recent run, promote model tier by one level for next retry.
4. If runtime timeout occurs twice on same stage, allow one-tier downgrade with narrowed scope.

## Runtime Record
Jarvis should append to final artifact:
```json
{
  "model_role_decision": {
    "jarvis": "tier-A",
    "livemore": "tier-B",
    "enkidu": "tier-A",
    "taishi": "tier-A",
    "reason": "L2 normal run"
  }
}
```
