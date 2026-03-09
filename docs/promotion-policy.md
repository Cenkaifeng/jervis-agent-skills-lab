# Skill 升格策略（实验 -> 公共）

## 升格门槛

满足以下条件才可从 incubating 升格 promoted：

1. 在至少 2 个不同任务场景复用成功
2. 输入/输出契约明确，边界与失败处理清晰
3. 通过统一质量门并有 smoke test
4. 安全审计通过（无可疑外联/越权路径/密钥泄露风险）
5. 完成版本化与变更记录

## 生命周期

- incubating：实验验证中
- active：高频使用，持续迭代
- promoted：公共复用，稳定维护
- deprecated：计划下线或替代

## 发布要求（Monorepo）

promoted/active 状态 skill 发布前必须：

- 在主仓完成 PATCH/MINOR 版本更新与变更记录
- 通过统一质量门（validate + package）
- 保持 `skills-index.yaml` 状态与版本信息一致

