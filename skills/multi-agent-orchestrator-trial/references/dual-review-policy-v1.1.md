# Dual-Review Policy (v1.1)

## Trigger
Enable dual-review when any of these holds:
- Task class is L3
- Contains security/permission/public-send risk
- taishi emits `pass_with_risk` with `security <= 3`

## Roles
- Reviewer-1: taishi (primary)
- Reviewer-2: secondary reviewer (fresh context, same rubric)
- Arbiter: jarvis

## Review Flow
1. taishi completes primary scoring.
2. secondary reviewer runs independent scoring.
3. jarvis merges results and resolves conflicts.

## Conflict Resolution
- If either reviewer emits hard-gate fail -> final verdict = fail.
- If score delta > 3 total points -> require reconciliation note.
- If verdict mismatch (`pass` vs `fail`) -> jarvis requests focused re-check on disputed items only.

## Merge Contract
```json
{
  "task_id": "T-YYYYMMDD-XX",
  "dual_review": {
    "primary": {"verdict": "pass|fail|pass_with_risk", "scores": {"quality": 0, "security": 0, "completeness": 0, "total": 0}},
    "secondary": {"verdict": "pass|fail|pass_with_risk", "scores": {"quality": 0, "security": 0, "completeness": 0, "total": 0}},
    "merged_verdict": "pass|fail|pass_with_risk",
    "conflicts": ["item1"],
    "arbiter_note": "..."
  }
}
```

## Token Control
- Secondary reviewer defaults to COMPACT_MODE.
- DETAIL_MODE only for conflict items.
