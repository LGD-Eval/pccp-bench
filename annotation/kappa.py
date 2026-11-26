"""Cohen's kappa + agreement report for PCCP-Bench labels.

用法：
    python kappa.py --ours a.json --theirs b.json            # 两份标注
    python kappa.py --selftest                               # 自测（合成数据）

输入格式（JSON）：{"case_id": "go|hold|reject", ...} 或
                  [{"id": "...", "verdict": "go"}, ...]
"""
import argparse, json, sys
from collections import Counter

LABELS = ("go", "hold", "reject")


def load(path):
    raw = json.load(open(path, encoding="utf-8"))
    if isinstance(raw, dict):
        return {k: v for k, v in raw.items()}
    out = {}
    for row in raw:
        out[row.get("id") or row.get("case_id")] = row.get("verdict") or row.get("label")
    return out


def kappa(a, b):
    ids = sorted(set(a) & set(b))
    n = len(ids)
    if not n:
        raise SystemExit("no overlapping case ids")
    obs = sum(1 for i in ids if a[i] == b[i]) / n
    ca, cb = Counter(a[i] for i in ids), Counter(b[i] for i in ids)
    exp = sum((ca[l] / n) * (cb[l] / n) for l in LABELS)
    k = (obs - exp) / (1 - exp) if exp != 1 else float("nan")
    # 逐类一致率 + 分歧清单
    per = {}
    for l in LABELS:
        m = [i for i in ids if a[i] == l or b[i] == l]
        per[l] = (sum(1 for i in m if a[i] == b[i]) / len(m)) if m else None
    dis = [(i, a[i], b[i]) for i in ids if a[i] != b[i]]
    return dict(n=n, observed_agreement=round(obs, 4), expected_agreement=round(exp, 4),
                kappa=round(k, 4) if k == k else None, per_label={k2: (round(v, 4) if v is not None else None) for k2, v in per.items()},
                disagreements=[{"id": i, "ours": x, "theirs": y} for i, x, y in dis],
                distribution_ours=dict(Counter(a[i] for i in ids)),
                distribution_theirs=dict(Counter(b[i] for i in ids)))


def selftest():
    # 1) 完全一致 -> kappa 1.0
    a = {f"c{i}": ("go" if i % 3 == 0 else "hold") for i in range(30)}
    r = kappa(a, dict(a))
    assert r["kappa"] == 1.0 and r["n"] == 30, r
    # 2) 已知教科书例子：kappa = 0（观测=期望）
    a = {"x": "go", "y": "go", "z": "hold", "w": "hold"}
    b = {"x": "go", "y": "hold", "z": "go", "w": "hold"}
    r = kappa(a, b)
    assert r["observed_agreement"] == 0.5 and abs(r["expected_agreement"] - 0.5) < 1e-9, r
    assert r["kappa"] == 0.0, r
    # 3) 分歧必须逐条列出，不吞
    assert len(r["disagreements"]) == 2, r
    # 4) 缺 id 的只比较交集，且要能看出来
    r = kappa({"a": "go"}, {"a": "go", "b": "hold"})
    assert r["n"] == 1, r
    print("selftest OK: 3/3")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ours"); ap.add_argument("--theirs"); ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json-out")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not (args.ours and args.theirs):
        raise SystemExit("need --ours and --theirs (or --selftest)")
    r = kappa(load(args.ours), load(args.theirs))
    txt = json.dumps(r, ensure_ascii=False, indent=2)
    print(txt)
    if args.json_out:
        open(args.json_out, "w", encoding="utf-8").write(txt)
    # 门槛：论文级要 kappa>=0.6（substantial）；低于 0.4 说明标签定义有歧义，先改协议不改题
    k = r["kappa"]
    if k is None or k < 0.4:
        print("VERDICT: BLOCKED -- kappa<0.4, 先修标签定义，不要发论文", file=sys.stderr)
        sys.exit(3)
    print("VERDICT: OK -- kappa>=0.4" + ("（达到 substantial 门槛 0.6）" if k >= 0.6 else "（弱于 0.6，只能报为限制）"))


if __name__ == "__main__":
    main()
