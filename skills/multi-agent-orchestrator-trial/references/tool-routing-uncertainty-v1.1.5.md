# Tool Routing with Uncertainty (v1.1.5)

## Goal
Upgrade tool routing from task-type only to task-type + uncertainty score.

## Inputs
- task_type: `T1..T6`
- uncertainty_total: from classification scorecard (`U+R+E+C`, 0~8)

## Routing Rules
1. `uncertainty_total <= 2`:
   - normal route
   - allow lower-cost model/tool path
2. `uncertainty_total 3~5`:
   - normal route + stricter schema checks
3. `uncertainty_total >= 6`:
   - force high-reliability route
   - enable dual-review if task is L3 or risk-sensitive
   - disallow risky fallbacks

## Degrade Rules
- Degrade only after one retry and only for non-security stages.
- Never degrade taishi hard-gate checks.

## Output Contract
```json
{
  "task_id": "T-...",
  "task_type": "T3",
  "uncertainty_total": 6,
  "route_mode": "high_reliability",
  "dual_review_required": true,
  "fallback_allowed": false
}
```
