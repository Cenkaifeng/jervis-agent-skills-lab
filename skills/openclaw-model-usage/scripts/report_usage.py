#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, List


OLD_MODEL_AGE_DAYS = 3
STALE_LARGE_AGE_DAYS = 3
STALE_LARGE_PCT = 20.0
PREPARE_FRESH_THREAD_PCT = 60.0


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


def age_days(ms: int | None) -> float:
    if not isinstance(ms, int):
        return 0.0
    return ms / 1000 / 86400


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


def default_model(status: Dict[str, Any]) -> str | None:
    return ((status.get("sessions") or {}).get("defaults") or {}).get("model")


def build_recommendations(status: Dict[str, Any], sessions: List[Dict[str, Any]], warn_pct: float, crit_pct: float) -> List[str]:
    recs: List[str] = []
    default = default_model(status)
    sorted_sessions = top_sessions(sessions, len(sessions))

    hottest = sorted_sessions[0] if sorted_sessions else None
    if hottest:
        hottest_pct = pct_used(hottest)
        if hottest_pct >= PREPARE_FRESH_THREAD_PCT:
            recs.append(
                f"{hottest.get('key')} 已到 {hottest_pct:.1f}% 上下文占用，建议准备新线程/新会话，避免后续压缩影响质量。"
            )
        elif hottest_pct >= warn_pct:
            recs.append(
                f"{hottest.get('key')} 已进入高占用区 ({hottest_pct:.1f}%)，继续长聊前值得留意上下文膨胀。"
            )

    legacy = [
        s for s in sessions
        if default and s.get("model") and s.get("model") != default and age_days(s.get("ageMs")) >= OLD_MODEL_AGE_DAYS
    ]
    if legacy:
        sample = legacy[0]
        recs.append(
            f"检测到旧模型遗留会话 {sample.get('key')}（model={sample.get('model')}，age={human_age(sample.get('ageMs'))}）。这通常是历史会话，不代表当前路由异常。"
        )

    stale_large = [
        s for s in sessions
        if age_days(s.get("ageMs")) >= STALE_LARGE_AGE_DAYS and pct_used(s) >= STALE_LARGE_PCT
    ]
    if stale_large:
        sample = stale_large[0]
        recs.append(
            f"存在较旧且仍偏大的会话 {sample.get('key')}（{pct_used(sample):.1f}% / age={human_age(sample.get('ageMs'))}），若短期不用可考虑让后续工作转到新会话。"
        )

    crits = [s for s in sessions if pct_used(s) >= crit_pct]
    if crits:
        recs.append(f"当前有 {len(crits)} 个会话达到 CRIT 阈值（>={crit_pct:.1f}%），优先处理这些会话的续聊策略。")

    if not recs:
        recs.append("当前未发现明显异常；模型分布和会话占用都在可接受范围内。")
    return recs


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
    recs = build_recommendations(status, sessions, warn_pct, crit_pct)

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
    lines.append("")
    lines.append("Recommendations:")
    for rec in recs:
        lines.append(f"- {rec}")
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
        "recommendations": build_recommendations(status, sessions, warn_pct, crit_pct),
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
