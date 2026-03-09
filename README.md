# jervis-agent-skills-lab

统一管理 cenkaifeng 体系下可复用、高频 Agent Skills 的工程化仓库。

## 目标

- 把分散在个人工作区的**自研可复用** skill 统一纳管
- 建立“设计 -> 审计 -> 测试 -> 发布 -> 同步”的标准流程
- 对具备复用价值的 skill 进行公共仓治理与持续迭代

## 收录范围（重要）

- ✅ 收录：自研/共同设计开发的 skills
- ❌ 不收录：外部下载来源 skill（例如来自第三方仓库或市场）

## 强制标准

本仓库所有 skill 新建/安装/升级，必须遵循：

- `docs/skill-implementation-standard.md`（主标准）
- `docs/skill-standard-anthropic-claude.md`（基线）

## 目录

- `skills/`：托管中的 skill（每个子目录一个 skill）
- `manifests/skills-index.yaml`：技能索引（版本、状态、来源、同步映射）
- `manifests/migration-candidates.yaml`：现有技能迁移候选清单
- `scripts/validate-all.sh`：统一质量门校验入口
- `scripts/package-all.sh`：统一打包入口
- `scripts/sync-to-subrepos.sh`：同步 skill 到专有仓库入口
- `docs/`：贡献、升格策略与治理规范

## 快速开始

```bash
./scripts/validate-all.sh
./scripts/package-all.sh
```

## 同步策略

- 单个 skill 小版本升级（PATCH/MINOR）后：
  1) 更新 `skills/` 内容
  2) 更新 `manifests/skills-index.yaml`
  3) 若该 skill 已拆分专仓，执行 `scripts/sync-to-subrepos.sh`

