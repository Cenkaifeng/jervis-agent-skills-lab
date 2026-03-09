# Taishi Scoring Standard (v0.6)

## Purpose
Turn taishi review from descriptive output into deterministic release decisions.

## Dimensions (0-5 each)
- **quality**: implementation correctness, robustness, reproducibility
- **security**: boundary compliance, least-privilege, data handling safety
- **completeness**: acceptance criteria coverage and delivery integrity

Total score = quality + security + completeness (0-15)

## Hard Gates (must pass)
Regardless of total score, fail immediately if any:
1. Security blocker exists in `release_blockers`
2. Human confirmation gate violated
3. Critical acceptance criterion is `fail`

## Release Thresholds
- **Pass**: total >= 12 and each dimension >= 3 and no hard-gate failure
- **Pass with risk**: total 9-11 and no hard-gate failure
- **Fail**: total <= 8 OR any hard-gate failure

## Required Taishi Output Contract
```json
{
  "task_id": "T-YYYYMMDD-XX",
  "agent": "taishi",
  "verdict": "pass|fail|pass_with_risk",
  "scores": {
    "quality": 0,
    "security": 0,
    "completeness": 0,
    "total": 0
  },
  "release_blockers": ["B1"],
  "acceptance_check": ["criterion A: pass", "criterion B: fail"],
  "security_check": ["boundary1: pass"],
  "fix_list": ["fix1", "fix2"],
  "next_action": "return_to_jarvis"
}
```

## Consistency Assertion (mandatory)
- `scores.total` must equal `scores.quality + scores.security + scores.completeness`.
- If mismatch is detected, force verdict=`fail` and return `[P0] scoring_contract_mismatch` in `fix_list`.

## Remediation Priority
Taishi should tag fixes by priority in `fix_list`:
- `[P0]` blocker (must fix before release)
- `[P1]` high risk
- `[P2]` normal improvement

## Token-Efficient Review Mode
Default mode returns:
- 1-line verdict rationale
- compact `scores`
- top 3 blockers/fixes only
If jarvis requests `DETAIL_MODE`, expand to full checks.
