#!/usr/bin/env python3
import json
import sys
from typing import Dict, Any


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def load(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_taishi(payload: Dict[str, Any]) -> None:
    required = ["schema_version", "task_id", "agent", "verdict", "scores", "fix_list", "release_blockers", "acceptance_check", "security_check", "next_action"]
    for k in required:
        if k not in payload:
            fail(f"missing taishi field: {k}")
    if payload["schema_version"] != "handoff.v1":
        fail("schema_version must be handoff.v1 for taishi handoff")
    if payload["agent"] != "taishi":
        fail("agent must be taishi")
    scores = payload["scores"]
    for k in ["quality", "security", "completeness", "total"]:
        if k not in scores:
            fail(f"missing scores field: {k}")
    total = scores["quality"] + scores["security"] + scores["completeness"]
    if total != scores["total"]:
        fail("scores.total mismatch")

    verdict = payload["verdict"]
    blockers = payload.get("release_blockers", [])
    acceptance = payload.get("acceptance_check", [])
    security_gate_fail = any("fail" in str(x).lower() for x in payload.get("security_check", []))
    critical_accept_fail = any(": fail" in str(x).lower() for x in acceptance)

    hard_gate = bool(blockers) or security_gate_fail or critical_accept_fail

    if hard_gate and verdict != "fail":
        fail("hard gate failed but verdict is not fail")

    if not hard_gate:
        if total >= 12 and min(scores["quality"], scores["security"], scores["completeness"]) >= 3 and verdict != "pass":
            fail("score threshold expects pass")
        if 9 <= total <= 11 and verdict not in ("pass_with_risk", "pass"):
            fail("score threshold expects pass_with_risk/pass")
        if total <= 8 and verdict != "fail":
            fail("score threshold expects fail")


def check_final(payload: Dict[str, Any]) -> None:
    required = ["schema_version", "goal", "outcome", "evidence", "risks_boundaries", "completed", "needs_human_confirmation", "next_steps"]
    for k in required:
        if k not in payload:
            fail(f"missing final_decision field: {k}")
    if payload["schema_version"] != "final.v1":
        fail("schema_version must be final.v1 for final decision")


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: runtime_lint_v0_8.py <taishi.json> <final_decision.json>")
        sys.exit(2)
    taishi = load(sys.argv[1])
    final = load(sys.argv[2])
    check_taishi(taishi)
    check_final(final)
    print("PASS: runtime lint checks succeeded")


if __name__ == "__main__":
    main()
