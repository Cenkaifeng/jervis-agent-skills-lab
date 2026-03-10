#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, List


def extract_json_payload(text: str) -> str:
    start = text.find("{")
    if start == -1:
        start = text.find("[")
    if start == -1:
        raise json.JSONDecodeError("No JSON object/array start found", text, 0)
    return text[start:]


def run_json(cmd: List[str]) -> Any:
    out = subprocess.check_output(cmd, text=True)
    return json.loads(extract_json_payload(out))


def human_age(ms: int | None) -> str:
    if not isinstance(ms, int):
        return "unknown"
    seconds = max(0, ms // 1000)
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m"
    if seconds < 86400:
        return f"{seconds // 3600}h"
    return f"{seconds // 86400}d"


def pct_used(sess: Dict[str, Any]) -> float:
    total = sess.get("totalTokens") or 0
    ctx = sess.get("contextTokens") or 0
    if not ctx:
        return 0.0
    return total / ctx * 100.0


def warning_level(percent: float, warn_pct: float, crit_pct: float) -> str:
    if percent >= crit_pct:
        return "CRIT"
    if percent >= warn_pct:
        return "WARN"
    return "OK"


def filter_sessions(sessions: List[Dict[str, Any]], agent: str | None, min_pct: float | None) -> List[Dict[str, Any]]:
    out = sessions
    if agent:
        out = [s for s in out if (s.get("agentId") or "") == agent]
    if min_pct is not None:
        out = [s for s in out if pct_used(s) >= min_pct]
    return out


def top_sessions(sessions: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    return sorted(sessions, key=lambda s: (pct_used(s), s.get("totalTokens") or 0), reverse=True)[:limit]


def summarize_agents(sessions: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    by_agent: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            "count": 0,
            "models": Counter(),
            "totalTokens": 0,
            "maxPct": 0.0,
        }
    )
    for s in sessions:
        agent = s.get("agentId") or "unknown"
        item = by_agent[agent]
        item["count"] += 1
        item["models"][s.get("model") or "unknown"] += 1
        item["totalTokens"] += s.get("totalTokens") or 0
        item["maxPct"] = max(item["maxPct"], pct_used(s))
    return by_agent


def render_text(
    status: Dict[str, Any],
    sessions_payload: Dict[str, Any],
    top_n: int,
    warn_pct: float,
    crit_pct: float,
    agent: str | None,
    min_pct: float | None,
) -> str:
    sessions = filter_sessions(sessions_payload.get("sessions", []), agent=agent, min_pct=min_pct)
    defaults = (status.get("sessions") or {}).get("defaults") or {}
    model_counts = Counter((s.get("model") or "unknown") for s in sessions)
    tops = top_sessions(sessions, top_n)
    agents = summarize_agents(sessions)

    lines: List[str] = []
    gateway = status.get("gateway") or {}
    version = (gateway.get("self") or {}).get("version") or gateway.get("appVersion") or "unknown"
    lines.append(f"OpenClaw version: {version}")
    lines.append(f"Default model: {defaults.get('model', 'unknown')} ({defaults.get('contextTokens', 'unknown')} ctx)")
    lines.append(f"Active sessions inspected: {len(sessions)}")
    if agent:
        lines.append(f"Agent filter: {agent}")
    lines.append(f"Warning thresholds: WARN>={warn_pct:.1f}% · CRIT>={crit_pct:.1f}%")
    lines.append("")
    lines.append("Model distribution:")
    for model, count in model_counts.most_common():
        lines.append(f"- {model}: {count}")
    if not model_counts:
        lines.append("- none")
    lines.append("")
    lines.append(f"Top {len(tops)} sessions by context occupancy:")
    for s in tops:
        percent = pct_used(s)
        level = warning_level(percent, warn_pct, crit_pct)
        lines.append(
            f"- [{level}] {s.get('key')}: {s.get('totalTokens', 0)}/{s.get('contextTokens', 0)} "
            f"({percent:.1f}%) · model={s.get('model')} · age={human_age(s.get('ageMs'))}"
        )
    if not tops:
        lines.append("- none")
    lines.append("")
    lines.append("Agent summary:")
    for agent_id, item in sorted(agents.items()):
        model_summary = ", ".join(f"{m}×{c}" for m, c in item["models"].most_common())
        lines.append(
            f"- {agent_id}: sessions={item['count']} · totalTokens={item['totalTokens']} "
            f"· peakOccupancy={item['maxPct']:.1f}% · models={model_summary}"
        )
    if not agents:
        lines.append("- none")
    return "\n".join(lines)


def render_json(
    status: Dict[str, Any],
    sessions_payload: Dict[str, Any],
    top_n: int,
    warn_pct: float,
    crit_pct: float,
    agent: str | None,
    min_pct: float | None,
) -> str:
    sessions = filter_sessions(sessions_payload.get("sessions", []), agent=agent, min_pct=min_pct)
    defaults = (status.get("sessions") or {}).get("defaults") or {}
    model_counts = Counter((s.get("model") or "unknown") for s in sessions)
    tops = top_sessions(sessions, top_n)
    agents = summarize_agents(sessions)
    gateway = status.get("gateway") or {}
    payload = {
        "openclawVersion": ((gateway.get("self") or {}).get("version")) or gateway.get("appVersion"),
        "defaultModel": defaults.get("model"),
        "defaultContextTokens": defaults.get("contextTokens"),
        "sessionCount": len(sessions),
        "agentFilter": agent,
        "warnThresholdPercent": warn_pct,
        "critThresholdPercent": crit_pct,
        "modelDistribution": [{"model": m, "count": c} for m, c in model_counts.most_common()],
        "topSessions": [
            {
                "key": s.get("key"),
                "agentId": s.get("agentId"),
                "model": s.get("model"),
                "totalTokens": s.get("totalTokens"),
                "contextTokens": s.get("contextTokens"),
                "percentUsed": round(pct_used(s), 2),
                "warningLevel": warning_level(pct_used(s), warn_pct, crit_pct),
                "ageMs": s.get("ageMs"),
            }
            for s in tops
        ],
        "agents": [
            {
                "agentId": agent_id,
                "sessionCount": item["count"],
                "totalTokens": item["totalTokens"],
                "peakOccupancy": round(item["maxPct"], 2),
                "models": [{"model": m, "count": c} for m, c in item["models"].most_common()],
            }
            for agent_id, item in sorted(agents.items())
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize OpenClaw model usage from active sessions.")
    parser.add_argument("--active-minutes", type=int, default=10080, help="Inspect sessions active within the past N minutes.")
    parser.add_argument("--active-hours", type=int, help="Shortcut for --active-minutes <hours*60>.")
    parser.add_argument("--agent", help="Only inspect one agent id (for example: main, jarvis, enkidu).")
    parser.add_argument("--top", type=int, default=5, help="Number of top occupancy sessions to show.")
    parser.add_argument("--warn-pct", type=float, default=40.0, help="Warn threshold for context occupancy percent.")
    parser.add_argument("--crit-pct", type=float, default=70.0, help="Critical threshold for context occupancy percent.")
    parser.add_argument("--min-pct", type=float, help="Only include sessions at or above this occupancy percent.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    active_minutes = args.active_minutes
    if args.active_hours is not None:
        active_minutes = args.active_hours * 60

    try:
        status = run_json(["openclaw", "status", "--json"])
        sessions_payload = run_json(["openclaw", "sessions", "--all-agents", "--active", str(active_minutes), "--json"])
    except subprocess.CalledProcessError as exc:
        print(f"command failed: {exc}", file=sys.stderr)
        return exc.returncode or 1
    except json.JSONDecodeError as exc:
        print(f"failed to parse OpenClaw JSON output: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(render_json(status, sessions_payload, args.top, args.warn_pct, args.crit_pct, args.agent, args.min_pct))
    else:
        print(render_text(status, sessions_payload, args.top, args.warn_pct, args.crit_pct, args.agent, args.min_pct))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
