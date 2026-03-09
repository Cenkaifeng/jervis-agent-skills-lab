# Skill 治理约定

## 单一事实源

- 统一以本仓 `skills/` 为开发源
- `manifests/skills-index.yaml` 为版本与状态权威清单
- `manifests/external-skills-excluded.yaml` 为外源技能排除清单

## 收录边界

- 仅纳管自研或共同开发、具备复用价值的 skills
- 外源下载 skills 不进入本仓，避免供应链污染与版权/维护边界不清

## 标准约束

- 强制遵循：
  - `docs/skill-implementation-standard.md`
  - `docs/skill-standard-anthropic-claude.md`

## 安全约束

- 新增 skill 默认零信任审计
- 外发/公开动作必须人工确认
- 高风险脚本建议隔离环境验证

