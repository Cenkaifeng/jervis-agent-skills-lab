#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


def fail(msg: str):
    print(f"FAIL: {msg}")
    sys.exit(1)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def run_runtime_lint(repo_root: Path, taishi: Path, final: Path):
    lint = repo_root / "skills/multi-agent-orchestrator-trial/scripts/runtime_lint_v0_8.py"
    cmd = ["python3", str(lint), str(taishi), str(final)]
    proc = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)
    if proc.returncode != 0:
        fail(f"runtime lint failed: {proc.stdout}\n{proc.stderr}")


def check_ab_metrics(ab, min_pass_rate, max_timeout_rate, max_retry_rate):
    b = ab.get("aggregates", {}).get("B")
    if not b:
        fail("missing aggregates.B")
    if b.get("sample_size", 0) < 10:
        fail("sample_size for B < 10")
    if b.get("pass_rate", 0) < min_pass_rate:
        fail(f"pass_rate below threshold: {b.get('pass_rate')} < {min_pass_rate}")
    if b.get("timeout_rate", 1) > max_timeout_rate:
        fail(f"timeout_rate above threshold: {b.get('timeout_rate')} > {max_timeout_rate}")
    if b.get("retry_rate", 1) > max_retry_rate:
        fail(f"retry_rate above threshold: {b.get('retry_rate')} > {max_retry_rate}")


def check_hard_gate(ab):
    for run in ab.get("runs", []):
        q = run.get("quality", {})
        if q.get("hard_gate_fail", False) and run.get("success", False):
            fail(f"hard gate bypass detected in run {run.get('run_id')}")


def check_telemetry_mode(ab, require_real):
    mode = ab.get("experiment", {}).get("token_mode", "proxy")
    if require_real and mode != "real":
        fail(f"real telemetry required, got token_mode={mode}")


def main():
    ap = argparse.ArgumentParser(description="Release gate for multi-agent skill v1.1.4")
    ap.add_argument("--repo-root", default="/root/.openclaw/workspace")
    ap.add_argument("--taishi", required=True)
    ap.add_argument("--final", required=True)
    ap.add_argument("--ab", required=True, help="ab-quant-results json")
    ap.add_argument("--min-pass-rate", type=float, default=0.9)
    ap.add_argument("--max-timeout-rate", type=float, default=0.1)
    ap.add_argument("--max-retry-rate", type=float, default=0.2)
    ap.add_argument("--require-real-telemetry", action="store_true")
    args = ap.parse_args()

    repo_root = Path(args.repo_root)
    taishi = Path(args.taishi)
    final = Path(args.final)
    ab_path = Path(args.ab)

    run_runtime_lint(repo_root, taishi, final)
    ab = load_json(ab_path)
    check_hard_gate(ab)
    check_ab_metrics(ab, args.min_pass_rate, args.max_timeout_rate, args.max_retry_rate)
    check_telemetry_mode(ab, args.require_real_telemetry)

    print("PASS: release gate v1.1.4 passed")


if __name__ == "__main__":
    main()
