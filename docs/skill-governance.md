# Skill 治理约定

## 单一事实源

- 统一以本仓 `skills/` 为开发源
- `manifests/skills-index.yaml` 为版本与状态权威清单

## 标准约束

- 强制遵循：
  - `docs/skill-implementation-standard.md`
  - `docs/skill-standard-anthropic-claude.md`

## 安全约束

- 新增 skill 默认零信任审计
- 外发/公开动作必须人工确认
- 高风险脚本建议隔离环境验证

