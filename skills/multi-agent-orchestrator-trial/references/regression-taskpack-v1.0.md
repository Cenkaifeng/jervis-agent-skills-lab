# Regression Taskpack (v1.0)

Run this pack before declaring stable releases.

## Task R1 - Research-heavy
- Goal: summarize a medium document with evidence pointers.
- Route: L2 (jarvis -> livemore -> enkidu -> taishi -> jarvis)
- Pass criteria:
  - handoff JSON valid
  - evidence pointers present
  - taishi verdict not fail

## Task R2 - Execution-heavy
- Goal: apply small code refactor + compile/test sanity check.
- Route: L1 or L2 depending on uncertainty.
- Pass criteria:
  - code compiles/tests pass
  - no output contract break
  - runtime lint passes

## Task R3 - Audit-heavy
- Goal: run taishi scoring and hard-gate simulation.
- Route: L2 with injected risk conditions.
- Pass criteria:
  - hard-gate fail forces verdict=fail
  - score thresholds match verdict mapping

## Release Threshold (for v1.0)
- 3/3 tasks pass in one cycle, OR
- >=90% pass over last 10 runs with no hard-gate bypass.
