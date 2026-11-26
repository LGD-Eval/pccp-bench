#!/usr/bin/env python3
"""pccp_gate.py — 离线发行闸门（stdlib only，无网络、无第三方依赖）

给厂商用的一件小工具：拿一份已授权的 PCCP（plan.json）和一次即将发布的变更（release.json），
判断这次发布是否落在计划范围内，并给出我们四类口径的结论。

用法：
    python pccp_gate.py --plan plan.json --release release.json
    python pccp_gate.py --selftest

输出：JSON（verdict / reasons / 缺失字段），退出码 0=go，3=需要另交（hold*），4=禁止（reject）。

重要边界：
 - 这是**辅助判定**，不是监管认定。§515C(c) 的禁止性判断由法条给出，我们只是把它落成可执行检查。
 - 规则集与 PCCP-Bench 的裁判共享口径，但**不宣称与之等价**；裁判版本以仓库 annotation/ 为准。
"""
import argparse, json, sys

VERDICT_GO = "go"
VERDICT_HOLD = "hold_resubmit"
VERDICT_INSUFF = "hold_insufficient"
VERDICT_REJECT = "reject"

PLAN_REQUIRED = ("plan_id", "device", "allowed_changes", "acceptance_criteria", "version_authorized")
RELEASE_REQUIRED = ("change_id", "change_type", "intended_use_unchanged", "validation", "metrics",
                    "predicate_uses_pccp_modified_version", "labeling_update")


def _missing(obj, keys):
    return [k for k in keys if obj.get(k) in (None, "", [], {})]


def evaluate(plan, rel):
    reasons = []
    missing = {"plan": _missing(plan, PLAN_REQUIRED), "release": _missing(rel, RELEASE_REQUIRED)}

    # R-1 §515C(c)：拿 PCCP 修改后版本当 predicate —— 法定禁止
    if rel.get("predicate_uses_pccp_modified_version") is True:
        reasons.append({"rule": "R-1-statute-predicate", "level": "critical",
                        "detail": "§515C(c)：不得以 PCCP 修改后的版本作为 predicate；只能用修改前已获准版本"})

    # R-2 变更类型不在授权清单内
    allowed = set((plan.get("allowed_changes") or []))
    ct = rel.get("change_type")
    if ct and allowed and ct not in allowed:
        reasons.append({"rule": "R-2-outside-authorized-scope", "level": "critical",
                        "detail": f"变更类型 {ct} 不在授权清单 {sorted(allowed)} 内；应按越界处理，另交申报"})

    # R-3 预期用途改变
    if rel.get("intended_use_unchanged") is False:
        reasons.append({"rule": "R-3-intended-use-change", "level": "critical",
                        "detail": "预期用途发生变化；此类变更不属 PCCP 覆盖范围，须另交"})

    # R-4 验收判据未达成
    crit = plan.get("acceptance_criteria") or {}
    met = rel.get("metrics") or {}
    fails = []
    for name, spec in crit.items():
        if not isinstance(spec, dict):
            continue
        floor = spec.get("min")
        observed = met.get(name)
        if floor is not None and observed is not None and observed < floor:
            fails.append(f"{name}: {observed} < {floor}")
        if spec.get("required") and observed is None:
            fails.append(f"{name}: 未报")
    if fails:
        reasons.append({"rule": "R-4-acceptance-criteria-not-met", "level": "critical",
                        "detail": "判据未达成：" + "；".join(fails)})

    # R-5 记录缺失（验证/确认、标签更新）
    if not rel.get("validation"):
        reasons.append({"rule": "R-5-validation-missing", "level": "major",
                        "detail": "无验证与确认记录"})
    if rel.get("labeling_update") is False:
        reasons.append({"rule": "R-6-labeling-not-updated", "level": "major",
                        "detail": "变更未反映到标签/版本历史"})

    crit_hit = [r for r in reasons if r["level"] == "critical" and r["rule"] != "R-5-validation-missing"]
    if any(r["rule"] == "R-1-statute-predicate" for r in crit_hit):
        verdict = VERDICT_REJECT
    elif crit_hit:
        verdict = VERDICT_HOLD
    elif reasons:
        verdict = VERDICT_INSUFF
    else:
        verdict = VERDICT_GO

    return {"verdict": verdict, "reasons": reasons, "missing_fields": missing,
            "disclaimer": "辅助判定，非监管认定；不得替代 FDA 审评。"}


def selftest():
    plan = {"plan_id": "P1", "device": "D", "version_authorized": "1.0",
            "allowed_changes": ["threshold_change", "retrain_same_distribution"],
            "acceptance_criteria": {"auc": {"min": 0.90, "required": True}}}
    base = {"change_id": "C1", "change_type": "threshold_change", "intended_use_unchanged": True,
            "validation": "bench + regression", "metrics": {"auc": 0.93},
            "predicate_uses_pccp_modified_version": False, "labeling_update": True}

    # 1 全部合规 -> go
    assert evaluate(plan, dict(base))["verdict"] == "go"
    # 2 判据未达 -> hold_resubmit，且理由点名 auc
    r = evaluate(plan, {**base, "metrics": {"auc": 0.88}})
    assert r["verdict"] == "hold_resubmit" and any("auc" in x["detail"] for x in r["reasons"]), r
    # 3 越界变更类型 -> hold_resubmit
    r = evaluate(plan, {**base, "change_type": "architecture_change"})
    assert r["verdict"] == "hold_resubmit" and r["reasons"][0]["rule"] == "R-2-outside-authorized-scope", r
    # 4 §515C(c) -> reject
    r = evaluate(plan, {**base, "predicate_uses_pccp_modified_version": True})
    assert r["verdict"] == "reject" and r["reasons"][0]["rule"] == "R-1-statute-predicate", r
    # 5 记录缺失 -> hold_insufficient
    r = evaluate(plan, {**base, "validation": "", "labeling_update": False})
    assert r["verdict"] == "hold_insufficient" and len(r["reasons"]) == 2, r
    # 6 缺字段不静默通过
    r = evaluate({}, {})
    assert r["verdict"] == "hold_insufficient" and r["missing_fields"]["plan"], r
    print("selftest OK: 6/6")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan"); ap.add_argument("--release"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.plan and a.release):
        raise SystemExit("need --plan and --release (or --selftest)")
    plan = json.load(open(a.plan, encoding="utf-8"))
    rel = json.load(open(a.release, encoding="utf-8"))
    out = evaluate(plan, rel)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return {"go": 0, "hold_resubmit": 3, "hold_insufficient": 3, "reject": 4}[out["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
