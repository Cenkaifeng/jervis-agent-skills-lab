# Token Efficiency Design (v0.5)

## Objectives
- Reduce orchestration overhead tokens by 25-40% in normal runs.
- Keep quality gates intact (do not skip taishi/security checks).

## Design Rules

0. **Compact/Detail Dual Channel (mandatory)**
   - Chat channel may return compact top-N summary.
   - Full audit payload (`acceptance_check`, `security_check`, full `fix_list`) must be persisted in artifact files.
   - Chat must include artifact pointers so details are always recoverable.

1. **Progressive Detail Output**
   - First response per stage: compact summary (<= 8 bullets).
   - Only expand details when jarvis explicitly requests `DETAIL_MODE`.

2. **Evidence by Pointer, not Full Dump**
   - Prefer `file:path#section` or `url` references.
   - Avoid pasting large command output; provide hash/line-range pointers.

3. **Fixed Compact JSON Keys in Runtime**
   - Internal runtime format may use short keys:
     - `tid, ag, sum, ev, rk, conf, nx`
   - Before user-facing output, jarvis maps compact keys back to canonical keys.

4. **Budget-Aware Stage Instructions**
   - L1: max 500 tokens per stage response
   - L2: max 800 tokens per stage response
   - L3: max 1200 tokens per stage response

5. **Delta-Only Retries**
   - On retry/fix loop, return only changed parts with `delta_from_prev`.
   - Never resend full prior payload unless requested.

6. **Single Source of Truth**
   - Artifacts persist in files; chat carries only index/summary.
   - Use consistent artifact index block:
```json
{
  "artifact_index": [
    "docs/x.md#sec-2",
    "logs/run-20260226.txt#L20-L55"
  ]
}
```

## Safety and Quality Caveat
- Token optimization must not bypass human confirmation gates.
- If compression hurts auditability, taishi can force `DETAIL_MODE`.
