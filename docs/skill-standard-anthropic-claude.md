# Skill 最佳实现标准（Anthropic Guide 对齐版）

> 来源基线：
> - `docs/references/The-Complete-Guide-to-Building-Skill-for-Claude.pdf`
> - 提取文本：`docs/references/The-Complete-Guide-to-Building-Skill-for-Claude.extracted.md`

本文件把 Anthropic《The Complete Guide to Building Skill for Claude》的可执行规范，映射成我们工作区可落地标准。

## 1) 下载/安装前校验标准（Pre-Install Gate）

### 1.1 来源与用途
- 必须记录：来源、版本、用途、风险级别。
- `find-skills` 仅用于发现，不直接安装。
- 优先 `clawhub inspect` + `clawhub install`；其他来源也必须走同一审计。

### 1.2 结构与元数据快速体检
- 目录必须有且仅有核心结构：`SKILL.md`（必需）+ `scripts/references/assets`（可选）。
- skill 文件名必须是 **`SKILL.md`**（区分大小写）。
- `SKILL.md` frontmatter 至少包含：
  - `name`（kebab-case）
  - `description`（必须含“做什么 + 何时触发”）

### 1.3 Frontmatter 安全规则
- 禁止在 frontmatter 中放注入性内容（如恶意指令、XML 注入）。
- `description` 应具体、可触发，不得过于泛化。
- 禁止使用保留品牌命名（如将 skill 命名为 anthropic/claude 相关保留名）。

### 1.4 风险脚本扫描
至少扫描以下风险：
- 命令注入（`shell=True` / `eval` / 拼接执行命令）
- 越权写入（绝对路径、`..`、`.git/`）
- 外发动作（消息、公开发布、权限修改）
- 密钥读取/泄露

## 2) 新建 Skill 标准（Creation Standard）

### 2.1 Progressive Disclosure（分层加载）
遵循三层：
1. Frontmatter（始终可见，必须精炼）
2. `SKILL.md` 主体（核心流程）
3. `references/`（详细资料按需加载）

### 2.2 SKILL.md 编写规范
- `description` 必须包含：
  - 能力描述（What）
  - 触发语句/场景（When）
  - 关键边界（Scope）
- 优先使用“可执行指令 + 明确输出”的写法。
- 关键步骤前置，避免冗长叙述。

### 2.3 目录规范
- 仅保留必要资源：`scripts/`、`references/`、`assets/`。
- 不在 skill 包内放无关文档（README/CHANGELOG/安装说明等）。
- 大段详细材料放 `references/`，`SKILL.md` 保持核心流程。

## 3) 测试与迭代标准（Testing & Iteration）

### 3.1 三类测试（最低要求）
1. **触发测试**：该触发时触发，不该触发时不触发。
2. **功能测试**：主路径正确、错误处理有效。
3. **成本/上下文测试**：上下文负载与执行成本可接受。

### 3.2 质量门
- 至少 1 条 smoke test 可自动跑。
- 高风险动作必须有 dry-run + apply 双模式。
- 关键输出建议结构化（JSON/schema）并可 lint。

## 4) 安全执行标准（Runtime Safety）
- 默认最小权限。
- 危险动作 require explicit confirm token。
- 路径与文件操作必须在 allowlist/repo 边界内。
- 外发/公开动作必须人工确认。

## 5) 交付标准（Release Standard）
- 每次 skill 变更必须 commit。
- 重大变更推送备份仓库。
- 写入 `memory/YYYY-MM-DD.md` 记录变更与风险。
