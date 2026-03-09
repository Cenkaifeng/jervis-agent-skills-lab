# Skill 专仓同步计划

> 说明：本仓只纳管自研 skills；每个可复用 skill 可映射到独立专仓做对外发布与独立迭代。

## 目标映射（建议）

- `readx` -> `github.com/cenkaifeng/skill-readx`
- `project-manager-table-insights` -> `github.com/cenkaifeng/skill-project-manager-table-insights`
- `finance-data-fetch` -> `github.com/cenkaifeng/skill-finance-data-fetch`
- `finance-report-render` -> `github.com/cenkaifeng/skill-finance-report-render`
- `finance-daily-orchestrator` -> `github.com/cenkaifeng/skill-finance-daily-orchestrator`
- `crawl-supabase-base` -> `github.com/cenkaifeng/skill-crawl-supabase-base`
- `multi-agent-orchestrator-trial` -> `github.com/cenkaifeng/skill-multi-agent-orchestrator-trial`

## 同步流程

1. 在 `manifests/skills-index.yaml` 里为目标 skill 设置：
   - `subrepo.enabled: true`
   - `subrepo.repo: github.com/<org>/<repo>`
2. 运行：`./scripts/sync-to-subrepos.sh [skill-name]`
3. 观察输出并验证专仓提交

## 注意

- 专仓不存在时先用 `gh repo create` 创建空仓（默认 main 分支）
- 同步只处理已启用映射的 skill，避免误推送
