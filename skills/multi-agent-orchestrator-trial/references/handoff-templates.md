# Handoff Templates

## livemore -> enkidu

```json
{
  "schema_version": "handoff.v1",
  "task_id": "T-YYYYMMDD-XX",
  "agent": "livemore",
  "summary": "one-line conclusion",
  "execution_brief": ["step1", "step2"],
  "assumptions": ["A1", "A2"],
  "out_of_scope": ["not doing X"],
  "evidence": ["url/file/command-output"],
  "risk": ["R1"],
  "confidence": 0.0,
  "next_action": "handoff_to_enkidu"
}
```

## enkidu -> taishi

```json
{
  "schema_version": "handoff.v1",
  "task_id": "T-YYYYMMDD-XX",
  "agent": "enkidu",
  "summary": "implementation result",
  "execution_log": ["cmd1", "cmd2"],
  "artifacts": ["path/to/file", "diff summary"],
  "limitations": ["L1"],
  "risk": ["R1"],
  "confidence": 0.0,
  "next_action": "handoff_to_taishi"
}
```

## taishi -> jarvis

```json
{
  "schema_version": "handoff.v1",
  "task_id": "T-YYYYMMDD-XX",
  "agent": "taishi",
  "verdict": "pass|fail|pass_with_risk",
  "fix_list": ["fix1", "fix2"],
  "release_blockers": ["B1"],
  "acceptance_check": ["criterion A: pass", "criterion B: fail"],
  "security_check": ["boundary1: pass"],
  "next_action": "return_to_jarvis"
}
```
