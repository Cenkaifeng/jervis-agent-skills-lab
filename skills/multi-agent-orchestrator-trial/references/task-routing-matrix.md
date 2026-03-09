# Task Routing Matrix (v0.3)

## Classification

### L1 - Simple
Use when task is single-domain, low risk, and can be completed without substantial research.

Route:
`jarvis -> enkidu -> taishi -> jarvis`

### L2 - Medium
Use when task needs scoped research before execution, but no broad uncertainty.

Route:
`jarvis -> livemore -> enkidu -> taishi -> jarvis`

### L3 - Complex
Use when task has high uncertainty, multiple assumptions, or high impact.

Route:
`jarvis -> livemore -> enkidu -> taishi -> (enkidu fixes if needed) -> jarvis`

## Fast Decision Heuristics

Classify as **L1** if all are true:
- Requirements are clear and stable
- No external data dependency beyond known context
- Low-risk changes

Classify as **L2** if any are true:
- Need targeted fact-check/research before build
- Requires assumptions list and out-of-scope definition
- Medium risk or moderate complexity

Classify as **L3** if any are true:
- High-impact actions (security, permission, production-critical)
- Multiple uncertain assumptions
- Needs one controlled fix loop after audit

For machine-consistent classification, use scorecard:
- `classification-scorecard.md`

## Guardrails
- Never skip taishi review.
- Ask human before external sends or destructive operations.
- Max orchestration loops: 2 unless human approves extension.
