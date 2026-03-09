#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ALLOWED_TOKEN_SOURCES = {"real", "mixed", "proxy"}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def avg(values):
    return sum(values) / len(values) if values else 0.0


def recompute(ab):
    runs = ab.get("runs", [])

    def agg(variant):
        subset = [r for r in runs if r.get("variant") == variant]
        n = len(subset)
        if n == 0:
            return {
                "sample_size": 0,
                "pass_rate": 0,
                "timeout_rate": 0,
                "retry_rate": 0,
                "avg_total_sec": 0,
                "avg_tokens_per_pass": 0,
                "avg_proxy_cost_per_pass": 0,
                "avg_cost_usd_per_pass": 0,
            }
        passes = [r for r in subset if r.get("success")]
        pass_n = len(passes)
        timeout_n = sum(1 for r in subset if r.get("efficiency", {}).get("timeouts", 0) > 0)
        retry_total = sum(r.get("efficiency", {}).get("retries", 0) for r in subset)
        total_sec = avg([r.get("timing", {}).get("total_sec", 0) for r in subset])
        tokens_per_pass = avg([r.get("efficiency", {}).get("tokens_in", 0) + r.get("efficiency", {}).get("tokens_out", 0) for r in passes]) if pass_n else 0
        proxy_per_pass = avg([r.get("efficiency", {}).get("proxy_cost", 0) for r in passes]) if pass_n else 0
        cost_per_pass = avg([r.get("efficiency", {}).get("cost_usd", 0) for r in passes]) if pass_n else 0
        return {
            "sample_size": n,
            "pass_rate": round(pass_n / n, 4),
            "timeout_rate": round(timeout_n / n, 4),
            "retry_rate": round(retry_total / n, 4),
            "avg_total_sec": round(total_sec, 4),
            "avg_tokens_per_pass": round(tokens_per_pass, 4),
            "avg_proxy_cost_per_pass": round(proxy_per_pass, 4),
            "avg_cost_usd_per_pass": round(cost_per_pass, 6),
        }

    a = agg("A")
    b = agg("B")
    ab["aggregates"] = {
        "A": a,
        "B": b,
        "delta_B_minus_A": {
            "pass_rate": round(b["pass_rate"] - a["pass_rate"], 4),
            "timeout_rate": round(b["timeout_rate"] - a["timeout_rate"], 4),
            "retry_rate": round(b["retry_rate"] - a["retry_rate"], 4),
            "avg_total_sec": round(b["avg_total_sec"] - a["avg_total_sec"], 4),
            "avg_tokens_per_pass": round(b["avg_tokens_per_pass"] - a["avg_tokens_per_pass"], 4),
            "avg_proxy_cost_per_pass": round(b["avg_proxy_cost_per_pass"] - a["avg_proxy_cost_per_pass"], 4),
            "avg_cost_usd_per_pass": round(b["avg_cost_usd_per_pass"] - a["avg_cost_usd_per_pass"], 6),
        },
    }


def validate_usage(usage: dict, valid_run_ids: set, trusted_source: str | None):
    if trusted_source is not None:
        source = usage.get("source")
        if source != trusted_source:
            raise ValueError(f"usage source mismatch: expected {trusted_source}, got {source}")

    for item in usage.get("runs", []):
        rid = item.get("run_id")
        if not rid or rid not in valid_run_ids:
            raise ValueError(f"invalid or unknown run_id in usage override: {rid}")

        tokens_in = int(item.get("tokens_in", 0))
        tokens_out = int(item.get("tokens_out", 0))
        cost_usd = float(item.get("cost_usd", 0.0))
        token_source = item.get("token_source", "real")

        if tokens_in < 0 or tokens_out < 0:
            raise ValueError(f"negative token values for run {rid}")
        if tokens_in > 10_000_000 or tokens_out > 10_000_000:
            raise ValueError(f"unreasonably large token values for run {rid}")
        if cost_usd < 0 or cost_usd > 1000:
            raise ValueError(f"invalid cost_usd for run {rid}")
        if token_source not in ALLOWED_TOKEN_SOURCES:
            raise ValueError(f"invalid token_source for run {rid}: {token_source}")


def main():
    ap = argparse.ArgumentParser(description="Apply real usage telemetry to AB quant result")
    ap.add_argument("--ab", required=True)
    ap.add_argument("--usage", required=True)
    ap.add_argument("--out", required=False)
    ap.add_argument("--trusted-source", required=False, help="if set, usage['source'] must match exactly")
    args = ap.parse_args()

    ab_path = Path(args.ab)
    usage_path = Path(args.usage)
    out_path = Path(args.out) if args.out else ab_path

    ab = load_json(ab_path)
    usage = load_json(usage_path)

    valid_run_ids = {r.get("run_id") for r in ab.get("runs", []) if r.get("run_id")}
    validate_usage(usage, valid_run_ids, args.trusted_source)

    usage_map = {x["run_id"]: x for x in usage.get("runs", []) if "run_id" in x}

    updated = 0
    for run in ab.get("runs", []):
        rid = run.get("run_id")
        if rid in usage_map:
            u = usage_map[rid]
            eff = run.setdefault("efficiency", {})
            eff["tokens_in"] = int(u.get("tokens_in", eff.get("tokens_in", 0)))
            eff["tokens_out"] = int(u.get("tokens_out", eff.get("tokens_out", 0)))
            eff["cost_usd"] = float(u.get("cost_usd", eff.get("cost_usd", 0)))
            eff["token_source"] = u.get("token_source", "real")
            updated += 1

    sources = {run.get("efficiency", {}).get("token_source", "proxy") for run in ab.get("runs", [])}
    if sources == {"real"}:
        mode = "real"
    elif "real" in sources:
        mode = "mixed"
    else:
        mode = "proxy"
    ab.setdefault("experiment", {})["token_mode"] = mode
    ab.setdefault("experiment", {})["token_source"] = mode

    recompute(ab)

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(ab, f, ensure_ascii=False, indent=2)

    print(f"updated_runs={updated}")
    print(str(out_path))


if __name__ == "__main__":
    main()
