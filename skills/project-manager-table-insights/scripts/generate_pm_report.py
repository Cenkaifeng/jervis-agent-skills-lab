#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def health_cn(v: str) -> str:
    return {
        "on_track": "正常推进",
        "at_risk": "存在风险",
        "delayed": "已延期",
        "unknown": "未知",
    }.get(v, v)


def main():
    p = argparse.ArgumentParser(description="Generate PM markdown report from analyzer JSON")
    p.add_argument("--input", required=True, help="Analyzer JSON path")
    p.add_argument("--output", required=True, help="Markdown output path")
    p.add_argument("--title", default="项目周报", help="Report title")
    args = p.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    s = data.get("summary", {})
    actions = data.get("next_actions", [])

    lines = []
    lines.append(f"# {args.title}")
    lines.append("")
    lines.append("## 一、项目总览")
    lines.append(f"- 项目健康度：**{health_cn(s.get('health', 'unknown'))}**")
    lines.append(f"- 任务总数：{s.get('total_tasks', 0)}")
    lines.append(f"- 延期任务：{s.get('delayed_tasks', 0)}")
    lines.append(f"- 风险任务：{s.get('at_risk_tasks', 0)}")
    lines.append(f"- 高优任务：{s.get('high_priority_tasks', 0)}")
    lines.append("")

    lines.append("## 二、重点风险与阻塞")
    if not actions:
        lines.append("- 暂未识别到高风险/延期任务。")
    else:
        for i, a in enumerate(actions[:10], 1):
            task = a.get("task") or "未命名任务"
            owner = a.get("owner") or "待定"
            due = a.get("due_date") or "未设置"
            risk = a.get("risk") or "-"
            blocker = a.get("blocker") or "-"
            flag = "延期" if a.get("is_delayed") else "风险"
            lines.append(f"{i}. [{flag}] {task}（Owner: {owner}, Due: {due}）")
            if risk != "-":
                lines.append(f"   - 风险：{risk}")
            if blocker != "-":
                lines.append(f"   - 阻塞：{blocker}")
    lines.append("")

    lines.append("## 三、下周优先动作")
    if not actions:
        lines.append("- 继续按计划推进，建议复盘关键里程碑和依赖项。")
    else:
        for a in actions[:5]:
            task = a.get("task") or "未命名任务"
            owner = a.get("owner") or "待定"
            due = a.get("due_date") or "本周内"
            lines.append(f"- 推进「{task}」，负责人：{owner}，目标截止：{due}")
    lines.append("")

    lines.append("## 四、给管理层的5行摘要")
    lines.append(f"1. 当前项目状态：{health_cn(s.get('health', 'unknown'))}。")
    lines.append("2. 本周关键进展：核心任务持续推进，已识别关键风险并进入跟踪。")
    lines.append(f"3. 主要风险点：延期 {s.get('delayed_tasks', 0)} 项，风险 {s.get('at_risk_tasks', 0)} 项。")
    lines.append("4. 需要支持事项：跨团队依赖协调与资源优先级确认。")
    lines.append("5. 下个检查点：下次周会前完成高风险任务清零或给出替代方案。")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
