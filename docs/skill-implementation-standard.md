# Skill 最佳实现标准（统一执行版）

> 生效范围：本工作区后续所有新建/安装/升级 skill。  
> 规范基线：`docs/skill-standard-anthropic-claude.md`

## A. 安装前（下载前）校验
1. `find-skills` 仅用于发现，不直接安装。
2. 优先 `clawhub inspect` + `clawhub install`；其他来源统一审计。
3. 安装前记录：来源、版本、用途、风险等级。
4. 预检结构：必须有 `SKILL.md`（大小写严格）。

## B. Frontmatter 与触发质量校验
1. 必填：`name`、`description`。
2. `name`：kebab-case，且与目录名一致。
3. `description`：必须同时包含
   - 做什么（What）
   - 何时用（When/触发语句）
4. description 禁止过于泛化（如“helps with projects”）。

## C. 创建新 Skill 结构标准
1. 只保留：`SKILL.md` + 可选 `scripts/ references/ assets/`。
2. 不在 skill 包内放 README/CHANGELOG 等非必要文件。
3. 遵循 Progressive Disclosure：
   - `SKILL.md` 放核心流程
   - 详细资料放 `references/` 按需加载

## D. 代码与安全标准
1. 避免 `shell=True`，优先 argv 数组执行。
2. 危险动作默认 dry-run；apply 必须显式确认 token。
3. 路径安全：阻断绝对路径、`..`、`.git/` 越界。
4. 外发/公开动作必须人工确认。
5. 扫描并阻断密钥泄露与可疑 exfiltration。

## E. 测试与回归标准
1. 最少三类测试：触发测试、功能测试、成本/上下文测试。
2. 每个 skill 至少 1 条 smoke test。
3. 高风险流程需有回滚/补偿方案。
4. 关键输出优先 JSON/schema，并提供 lint。

## F. 交付与版本管理
1. 所有变更必须 commit（清晰 message）。
2. 重大变更后推送备份仓库。
3. 当日 memory 记录：变更、风险、后续计划。
