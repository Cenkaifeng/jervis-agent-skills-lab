# Community Template Gap Analysis (v0.8)

Compared against previously discovered community patterns:
- wshobson/agents@workflow-orchestration-patterns
- qodex-ai/ai-agent-skills@multi-agent-orchestration
- sickn33/antigravity-awesome-skills@multi-agent-brainstorming
- ruvnet/claude-flow@swarm-orchestration

## What we now do better
1. **OpenClaw-native execution path**
   - Our flow maps directly to sessions/subagents without external runtime dependencies.
2. **Deterministic governance**
   - Unified termination protocol + loop ceiling + human gates.
3. **Machine-checkable contracts**
   - Schema-like contracts + runtime lint script for taishi/final outputs.
4. **Token-aware operations**
   - Compact/detail dual channel, pointer evidence, delta retries.
5. **Interrupt/backpressure handling**
   - Safe stage-boundary preemption and checkpoint resume.

## Remaining improvement opportunities (vs community broad patterns)
1. **Dynamic capability-based agent selection**
   - Current routing is role-fixed (jarvis/livemore/enkidu/taishi).
   - Improvement: dynamic role fallback matrix by model/tool availability.
2. **Portfolio-level scheduler**
   - Current queue policy is single-pipeline + priority.
   - Improvement: weighted fair scheduling across ongoing projects.
3. **Observability dashboard**
   - We have policy and logs, but no aggregated metrics board.
   - Improvement: daily KPI report (pass rate, retry rate, timeout rate, token/run).
4. **Automated regression taskpack**
   - Need fixed benchmark tasks to validate every version bump.
5. **Model-role optimization loop**
   - Reserved but not executed yet (`docs/agent-model-fit-research.md`).

## v0.9+ Candidate Upgrades
- Add dynamic role/model fallback matrix.
- Add queue fairness metrics and adaptive preemption.
- Add nightly regression runner for 3 canonical tasks.
- Add orchestration KPI summary artifact.
