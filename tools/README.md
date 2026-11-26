# tools/ — 发行闸门（pccp_gate.py）

一件给你直接用的小工具：拿一份已获授权的 PCCP 和一次即将发布的变更，判断这次发布是否还在计划范围内。

```bash
python tools/pccp_gate.py --selftest                       # 自测，6/6
python tools/pccp_gate.py --plan plan.json --release release.json
```

只依赖 Python 标准库，不联网，不读你的任何数据。

## 输入

`plan.json`（已授权计划，最小字段）
```json
{
  "plan_id": "P-001",
  "device": "示例器械",
  "version_authorized": "1.0",
  "allowed_changes": ["threshold_change", "retrain_same_distribution"],
  "acceptance_criteria": {"auc": {"min": 0.90, "required": true}}
}
```

`release.json`（本次发布记录，最小字段）
```json
{
  "change_id": "C-20261126",
  "change_type": "threshold_change",
  "intended_use_unchanged": true,
  "validation": "bench 2000 例 + 回归 45 项",
  "metrics": {"auc": 0.93},
  "predicate_uses_pccp_modified_version": false,
  "labeling_update": true
}
```

## 输出与退出码

| 结论 | 含义 | 退出码 |
|---|---|---|
| `go` | 全部规则通过，可直接发 | 0 |
| `hold_resubmit` | 越界或判据未达，须改后再发 / 另交 | 3 |
| `hold_insufficient` | 记录不全，先补证据 | 3 |
| `reject` | 触发法定禁止（§515C(c)） | 4 |

## 规则

- **R-1**（critical）§515C(c)：不得以 PCCP 修改后的版本作为 predicate
- **R-2**（critical）变更类型不在授权清单内 → 越界
- **R-3**（critical）预期用途改变 → 不属 PCCP 覆盖
- **R-4**（critical）验收判据未达成（含"应报未报"）
- **R-5**（major）无验证与确认记录
- **R-6**（major）未更新标签/版本历史

## 边界（请认真读）

1. **这是辅助判定，不是监管认定。** 不替代 FDA 审评，也不构成法律意见。
2. 规则集与 PCCP-Bench 的裁判共享口径，但**不宣称等价**；裁判版本以 `annotation/` 与 `candidate_pool/` 为准。
3. 缺字段不会被静默放过：空输入会返回 `hold_insufficient` 并列出缺哪些字段。
4. 不做文档层面的一致性检查（计划里的措辞是否自相矛盾），那需要读全文，超出本工具范围。
