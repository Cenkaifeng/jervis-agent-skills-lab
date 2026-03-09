# Model-Role Selection Policy (v1.2-draft)

## 目的
将 v1.0 的 tier 占位 fallback，升级为可实测、可审计、可自动升降档的 role->model 决策策略。

---

## 1) 角色评估权重

评分范围 0-100，按角色加权：

| Role | 质量 | 合规 | 可靠性 | 效率 | 成本 | 稳定性 |
|---|---:|---:|---:|---:|---:|---:|
| jarvis | 30% | 25% | 20% | 10% | 5% | 10% |
| livemore | 25% | 10% | 25% | 15% | 15% | 10% |
| enkidu | 30% | 20% | 20% | 15% | 5% | 10% |
| taishi | 35% | 25% | 25% | 5% | 0% | 10% |

硬门：
- taishi hard_gate_fail=true -> 直接 FAIL
- jarvis/taishi schema_violations>0 -> 直接 FAIL

---

## 2) 最小实验矩阵（强制）

至少跑 3 组：

| Group | jarvis | livemore | enkidu | taishi |
|---|---|---|---|---|
| G1 质量优先 | A | B | A | A |
| G2 平衡基线（默认候选） | A | B | B | A |
| G3 成本优先 | B | C | B | A |

样本要求（每组最少 12）：
- L1/L2/L3 = 4/4/4

组合放行门槛：
- L2/L3 hard-gate 通过率 >= 95%
- L3 PASS(+PASS_WITH_RISK可控) >= 90%

---

## 3) 组合决策

角色分：
`RoleFitScore(role) = Σ(weight_i × metric_i)`

组合分：
`TeamScore = 0.30*jarvis + 0.20*livemore + 0.25*enkidu + 0.25*taishi`

默认选择：
1. 首选 G2（A/B/B/A）
2. 高风险或回归失败时切 G1（A/B/A/A）
3. 预算模式可试 G3（B/C/B/A），仅限 L1/L2

约束：
- L3 禁止 jarvis=C、taishi=C

---

## 4) 升档/降档规则

### 升档（任一触发）
- 最近 10 次内 schema_violations>=2
- L2/L3 出现关键事实错误>=1
- taishi FAIL / PASS_WITH_RISK 重复>=2
- 角色重试率>20%

动作：角色升 1 档，并冻结 5 次不降档。

### 降档（全部满足）
- 最近 20 次 hard gate 100% 通过
- schema_violations=0
- 成本/成功 高于目标线 20%+
- 降档灰度 5 次无质量回退

动作：角色降 1 档；若回退则立即回升并锁 10 次。

质量回退定义：
- taishi_total 下降 > 8 分，或
- PASS 率下降 > 10%，或
- 超时率上升 > 8%

---

## 5) 运行记录（扩展 KPI）

在 `kpi-artifact-schema-v1.1` 基础上增加：

```json
{
  "model_fit": {
    "experiment_group": "G1|G2|G3",
    "role_fit_score": {"jarvis": 0, "livemore": 0, "enkidu": 0, "taishi": 0},
    "team_score": 0,
    "decision": "keep|upgrade_role|downgrade_role|switch_group",
    "decision_reason": ["..."]
  }
}
```

---

## 6) 与 v1.0 的兼容替换

- 保留 Tier-A/B/C 抽象层（不绑定具体供应商）
- 替换静态 fallback 顺序为“实验矩阵 + 阈值触发”
- 保留 L3 风险约束与 taishi 强审计地位

> 本策略为可直接纳入 skill 的草案版本；建议先以 2 周观测窗口验证阈值稳定性后固化为 v1.2 正式版。
