---
name: multi-agent-orchestrator-trial
description: OpenClaw-native orchestration for fixed multi-agent teams using serial handoff (jarvis -> livemore -> enkidu -> taishi -> jarvis). Use when user asks to run or design multi-agent collaboration, role partitioning, staged execution, audit gates, regression/review workflows, or iterative workflow validation. Do NOT use for one-step/simple tasks that can be completed by a single agent.
---

# Multi-Agent Orchestrator Trial

Use this skill to run a **serial, partitioned** multi-agent workflow for complex tasks.

## Workflow

Run stages in order:
1. jarvis: define goal, constraints, acceptance criteria.
2. livemore: produce evidence-backed execution brief.
3. enkidu: execute implementation strictly within brief scope.
4. taishi: audit against acceptance/security boundaries.
5. jarvis: consolidate final decision and user-facing output.

Never run livemore and enkidu in parallel in this trial version.

## Stage Routing

- Send research/scoping/fact-check tasks to livemore.
- Send implementation/execution tasks to enkidu.
- Send audit/quality/security checks to taishi.
- Keep arbitration and final synthesis in jarvis.

Use classification-based routing from:
- `references/task-routing-matrix.md`

Default class: **L2 (medium)**.

## Required Handoff Contract

Each stage returns JSON. Keep keys stable.

Read and use templates from:
- `references/handoff-templates.md`

For handoff schema version control, use:
- `references/handoff-versioning-v1.1.4.md`

For strict runtime validation and failure protocol, use:
- `references/protocol-and-schema-v0.5.md`

For deterministic class routing rationale, use:
- `references/classification-scorecard.md`

For token-saving execution mode, use:
- `references/token-efficiency-design.md`

For deterministic taishi release scoring, use:
- `references/taishi-scoring-v0.6.md`

For long-task interruption, urgent insertion, and anti-padding updates, use:
- `references/interrupt-and-backpressure-v0.7.md`

For reusable role prompts, use:
- `references/prompt-pack-v0.7.md`

For runtime contract linting, use:
- `scripts/runtime_lint_v0_8.py`

For comparison with community orchestration patterns, use:
- `references/community-gap-analysis-v0.8.md`

For stable role-to-model fallback policy, use:
- `references/model-role-fallback-matrix-v1.0.md`

For release regression checks, use:
- `references/regression-taskpack-v1.0.md`
- `scripts/run_regression_pack_v1_0.sh`

For v1.1 execution upgrades, use:
- `references/compensation-policy-v1.1.md`
- `references/dual-review-policy-v1.1.md`
- `references/tool-routing-matrix-v1.1.md`
- `references/research-parallel-mode-v1.1.md`
- `references/kpi-artifact-schema-v1.1.4.md`
- `scripts/export_kpi_v1_1.py`

For v1.1.4 hardening (P0), use:
- `references/real-telemetry-policy-v1.1.4.md`
- `references/handoff-versioning-v1.1.4.md`
- `references/trace-event-spec-v1.1.4.md`
- `scripts/apply_real_usage_v1_1_4.py`
- `scripts/release_gate_v1_1_4.py`

For v1.1.5 P1 execution upgrades, use:
- `references/dual-review-executor-v1.1.5.md`
- `references/saga-compensation-executor-v1.1.5.md`
- `references/tool-routing-uncertainty-v1.1.5.md`
- `references/mcp-trust-tier-policy-v1.1.5.md`
- `scripts/merge_dual_review_v1_1_5.py`
- `scripts/run_saga_compensation_v1_1_5.py`

For v1.1.3 quantified A/B execution, use:
- `scripts/run_ab_quant_v1_1_3.py`
- `reports/multi-agent-regression/ab-quant-metrics-template-v1.1.3.json` (workspace-root relative)

For v1.2 model-role selection draft, use:
- `references/model-role-selection-policy-v1.2-draft.md`
- `docs/agent-model-fit-experiment-v1.2.md` (workspace-root relative)

## Retry Policy

- livemore incomplete -> rerun livemore once.
- enkidu execution failure -> rerun enkidu once within frozen scope.
- taishi fail -> send fix list back to enkidu.
- Return to livemore only if taishi proves assumptions are wrong.
- Max 2 orchestration loops per task unless user approves extension.

Use SLA/timeout handling from:
- `references/sla-and-timeout-policy.md`

## Human Confirmation Gates

Always ask user before:
- External/public sends
- Destructive file/permission operations
- Credential/access boundary changes

## Final Output Contract (jarvis)

Produce:
1. Goal
2. Outcome
3. Evidence
4. Risks/Boundaries
5. Completed items
6. Items requiring user confirmation
7. Next steps

See template in:
- `references/final-output-template.md`

## Smoke Tests (required before release)

Run at least:
1. `bash scripts/run_regression_pack_v1_0.sh`
2. `python3 scripts/release_gate_v1_1_4.py --taishi reports/multi-agent-regression/taishi_r3.json --final reports/multi-agent-regression/final_r3.json --ab reports/multi-agent-regression/ab-quant-results-v1.1.3.json`

## Iteration Log

For each run, append short notes to:
- `docs/multi-agent-orchestration-playbook.md` (workspace-root relative path)

Include: what failed, what changed, and next validation step.
