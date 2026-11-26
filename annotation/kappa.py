"""Cohen's kappa + agreement report for PCCP-Bench labels.

v1.2（2026-11-26）：修 v1.1 的致命语法错误（dict( 未闭合），并把四类口径写死。
v1 只认三类（go/hold/reject），会把"材料没做"和"另交"糊进同一个 hold。

用法：
    python kappa.py --ours a.json --theirs b.json
    python kappa.py --ours a.csv  --theirs b.csv        # 也吃盲标包的 CSV
    python kappa.py --selftest

主指标（协议 v1.1 预定）：二分类 kappa = 覆盖(go) vs 不覆盖(其余三类)；四分类 kappa 只作补充。
门槛（预先写死，不许事后改）：<0.40 改协议不改题；0.40–0.60 只能报为限制；>=0.60 才可写实质一致。
"""
import argparse, json, sys, csv
from collections import Counter

LABELS4 = ("go", "hold_insufficient", "hold_resubmit", "reject")

_ALIASES = {
    "go": "go", "覆盖": "go", "approved": "go", "approve": "go",
    "reject": "reject", "拒绝": "reject",
    "hold": "hold_insufficient", "hold/insufficient": "hold_insufficient",
    "hold_insufficient": "hold_insufficient", "insufficient": "hold_insufficient",
    "材料不足": "hold_insufficient", "不覆盖": "hold_insufficient",
    "hold/resubmit": "hold_resubmit", "hold_resubmit": "hold_resubmit",
    "resubmit": "hold_resubmit", "另交": "hold_resubmit",
}


def normalize(v):
    if v is None:
        return None
    s = str(v).strip().lower().replace(" ", "").replace("／", "/").replace("·", "/").replace("_", "/")
    s = s.replace("hold/hold", "hold")
    s = s.replace("/hold", "hold")
    if s in _ALIASES:
        return _ALIASES[s]
    s2 = s.replace("/", "_")
    if s2 in ("hold_insufficient", "hold_resubmit"):
        return s2
    if s in ("go", "reject"):
        return s
    return s  # 原样保留，让它出现在分歧清单里，而不是被悄悄丢掉


def load(path):
    if path.lower().endswith(".csv"):
        out = {}
        with open(path, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                cid = (row.get("case_id") or row.get("id") or "").strip()
                lab = row.get("label") or row.get("verdict") or row.get("answer")
                if cid and lab and str(lab).strip():
                    out[cid] = normalize(lab)
        return out
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    if isinstance(raw, dict):
        return {k: normalize(v) for k, v in raw.items()}
    field = "verdict" if "verdict" in raw[0] else "label"
    return {r["id"]: normalize(r.get(field)) for r in raw if r.get("id")}


def _kappa_core(a, b, ids):
    n = len(ids)
    if not n:
        raise ValueError("no overlapping case ids (两人没有任何共同题号)")
    obs = sum(1 for i in ids if a[i] == b[i]) / n
    ca, cb = Counter(a[i] for i in ids), Counter(b[i] for i in ids)
    universe = set(a[i] for i in ids) | set(b[i] for i in ids)
    exp = sum((ca[l] / n) * (cb[l] / n) for l in universe)
    k = float("nan") if exp >= 1 else (obs - exp) / (1 - exp)
    return n, obs, exp, k


def kappa(a, b, as_binary=False):
    ids = sorted(set(a) & set(b))
    unknown = sorted({a[i] for i in ids} - set(LABELS4)) + sorted({b[i] for i in ids} - set(LABELS4))
    if as_binary:
        a = {i: ("covered" if a[i] == "go" else "not_covered") for i in ids}
        b = {i: ("covered" if b[i] == "go" else "not_covered") for i in ids}
    n, obs, exp, k = _kappa_core(a, b, ids)
    per = {}
    for l in sorted(set(LABELS4) | {a[i] for i in ids} | {b[i] for i in ids}):
        m = [i for i in ids if a[i] == l or b[i] == l]
        per[l] = round(sum(1 for i in m if a[i] == b[i]) / len(m), 4) if m else None
    return {
        "n": n,
        "observed_agreement": round(obs, 4),
        "expected_agreement": round(exp, 4),
        "kappa": (round(k, 4) if k == k else None),
        "binary_mode": as_binary,
        "per_label_agreement": per,
        "unknown_labels": sorted(set(unknown)),
        "disagreements": [{"id": i, "ours": a[i], "theirs": b[i]} for i in ids if a[i] != b[i]],
        "distribution_ours": dict(Counter(a[i] for i in ids)),
        "distribution_theirs": dict(Counter(b[i] for i in ids)),
    }


def selftest():
    # 1) 完全一致
    a = {f"c{i}": ("go" if i % 3 == 0 else "hold_insufficient") for i in range(30)}
    r = kappa(a, dict(a))
    assert r["kappa"] == 1.0 and r["n"] == 30, r
    # 2) 教科书 kappa=0
    r = kappa({"x": "go", "y": "go", "z": "hold_insufficient", "w": "hold_insufficient"},
              {"x": "go", "y": "hold_insufficient", "z": "go", "w": "hold_insufficient"})
    assert r["observed_agreement"] == 0.5 and abs(r["expected_agreement"] - 0.5) < 1e-9, r
    assert r["kappa"] == 0.0 and len(r["disagreements"]) == 2, r
    # 3) 四类必须进期望一致率（v1 的 bug：三类之外被忽略）
    r = kappa({"p": "hold_resubmit", "q": "hold_resubmit", "r": "go", "s": "go"},
              {"p": "hold_resubmit", "q": "hold_insufficient", "r": "go", "s": "hold_resubmit"})
    assert abs(r["expected_agreement"] - 0.375) < 1e-9, r
    assert r["kappa"] == 0.2, r
    # 4) 别名归一
    assert normalize("hold/insufficient") == normalize("HOLD_INSUFFICIENT") == "hold_insufficient"
    assert normalize("另交") == "hold_resubmit" and normalize("hold_resubmit") == "hold_resubmit"
    # 5) 二分类：另交与材料不足都算"不覆盖"（需两类共存才能算 κ，单一类别见 #8）
    r = kappa({"a": "hold_resubmit", "b": "go"}, {"a": "hold_insufficient", "b": "go"}, as_binary=True)
    assert r["kappa"] == 1.0 and r["disagreements"] == [], r
    # 6) 交集比较
    assert kappa({"a": "go"}, {"a": "go", "b": "reject"})["n"] == 1
    # 7) 空交集必须报错而不是静默给 0
    try:
        kappa({}, {"a": "go"}); raise AssertionError("应该报错")
    except ValueError:
        pass
    # 8) 单一类别 -> 期望一致率 1 -> kappa 记为 None（不可解释，不写成 1.0）
    r = kappa({"a": "go", "b": "go"}, {"a": "go", "b": "go"}, as_binary=True)
    assert r["kappa"] is None, r
    # 9) 未知标签必须被列出，不许悄悄归并
    r = kappa({"a": "go"}, {"a": "weird_label"})
    assert r["unknown_labels"] == ["weird_label"], r
    print("selftest OK: 9/9")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ours"); ap.add_argument("--theirs")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json-out")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not (args.ours and args.theirs):
        raise SystemExit("need --ours and --theirs (or --selftest)")
    a, b = load(args.ours), load(args.theirs)
    primary = kappa(a, b, as_binary=True)
    full = kappa(a, b, as_binary=False)
    out = {
        "primary_binary_kappa": primary,
        "secondary_4class_kappa": full,
        "thresholds_predeclared": {
            "blocked": "<0.40 改协议不改题",
            "moderate": "0.40-0.60 只能报为限制",
            "substantial": ">=0.60 才可写实质一致",
        },
        "caveats": [
            f"n={primary['n']}；n<10 时 κ 不稳定，只能作描述" if primary["n"] < 10 else f"n={primary['n']}",
            "单一类别时 κ 不可解释，此处记为 null，不得写成 1.0",
        ],
    }
    txt = json.dumps(out, ensure_ascii=False, indent=2)
    print(txt)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            f.write(txt)
    k = primary["kappa"]
    if k is None:
        print("VERDICT: BLOCKED -- 主指标无法计算（重叠题不足或标签单一）", file=sys.stderr)
        sys.exit(3)
    if k < 0.4:
        print(f"VERDICT: BLOCKED -- 二分类 kappa={k} < 0.40，先修协议，不改题", file=sys.stderr)
        sys.exit(3)
    print(f"VERDICT: OK -- 二分类 kappa={k}" + ("（达到 substantial 0.60）" if k >= 0.6 else "（<0.60，只能报为限制，不得写实质一致）"))


if __name__ == "__main__":
    main()
