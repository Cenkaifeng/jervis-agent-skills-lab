# Dual Review Executor (v1.1.5)

## Goal
Turn dual-review policy from guidance into executable merge logic for L3/high-risk tasks.

## Inputs
- `primary_review.json` (taishi output)
- `secondary_review.json` (independent reviewer output)

## Execution Rules
1. If either review contains hard-gate failure (`release_blockers` non-empty, security fail, or critical acceptance fail) -> merged verdict = `fail`.
2. If verdict mismatch (`pass` vs `fail`) -> mark conflict and require focused re-check.
3. If score delta (`|primary.total - secondary.total|`) > 3 -> mark conflict and require arbiter note.
4. If no hard-gate and no conflict:
   - both pass -> merged `pass`
   - any pass_with_risk -> merged `pass_with_risk`

## Output
Generate `dual_review_merge.json`:
```json
{
  "task_id": "T-...",
  "schema_version": "dual_review.v1",
  "dual_review": {
    "primary": {...},
    "secondary": {...},
    "merged_verdict": "pass|fail|pass_with_risk",
    "conflicts": ["..."],
    "arbiter_note": "..."
  }
}
```

## Script
Use:
- `scripts/merge_dual_review_v1_1_5.py`
