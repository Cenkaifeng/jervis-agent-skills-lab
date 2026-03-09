# Contribution Guide

## 提交流程

1. 新建分支：`feat/<skill-name>-<topic>`
2. 修改 `skills/<skill-name>/...`
3. 更新 `manifests/skills-index.yaml`
4. 运行：
   - `./scripts/validate-all.sh`
   - `./scripts/package-all.sh`
5. 提交 PR，说明：
   - 变更原因
   - 触发词变化
   - 风险与回滚方案

## 必需检查

- frontmatter 合规（`name` + `description`）
- `name` 与目录一致（kebab-case）
- `description` 包含 What + When
- 不包含多余文档（README/CHANGELOG 等）
- 脚本通过最小 smoke test

