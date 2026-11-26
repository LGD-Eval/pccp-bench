"""把一次外部跑分和三条基线放在一起比较，并把可疑模式直接标出来。

用法：
    python compare.py submission.json                 # 对比同目录 standings.json 的基线
    python compare.py submission.json standings.json

submission.json 至少含：
    {"team": "...", "adapter_sha256": "...",
     "public": {"exact": .., "masked": .., "tag": .., "macro_recall": ..},
     "controls_pass": true, "rerun_consistent": true}

退出码：0 正常；1 有可疑项（不阻断，只是让调用方知道）。
"""
import json, sys, pathlib

HERE = pathlib.Path(__file__).parent


def f(x):
    return "—" if x is None else f"{x:.4f}".rstrip("0").rstrip(".")


def find_ledger():
    if len(sys.argv) > 2:
        return pathlib.Path(sys.argv[2])
    for cand in (HERE / "standings.json", HERE / "external_run_kit" / "standings.json", HERE.parent / "external_run_kit" / "standings.json"):
        if cand.exists():
            return cand
    sys.exit("找不到 standings.json：把它放在脚本同目录，或显式传第二个参数")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sub = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    led = json.loads(find_ledger().read_text(encoding="utf-8"))

    ref = led["baseline_reference"]
    mem = led["baseline_memoriser"]
    go = led["baseline_always_go"]
    pub = sub.get("public") or {}
    hid = sub.get("hidden") or {}

    flags = []

    print(f"队伍：{sub.get('team')}  adapter_sha256={str(sub.get('adapter_sha256'))[:8]}")
    print()
    print("| 指标 | 你的队 | 参考裁判 | 背题者 | 空基线 | 差（你 − 参考） |")
    print("|---|---|---|---|---|---|")
    rows = [
        ("public exact", pub.get("exact"), ref.get("public"), mem.get("public"), go.get("exact_public")),
        ("public masked", pub.get("masked"), ref.get("masked"), mem.get("masked"), None),
        ("public tag", pub.get("tag"), ref.get("tag"), mem.get("tag_public"), None),
        ("public macro_recall", pub.get("macro_recall"), None, None, go.get("macro_recall_public")),
        ("hidden exact", hid.get("exact"), None, None, None),
    ]
    for name, mine, r, m, g in rows:
        delta = "—" if (mine is None or r is None) else f"{mine - r:+.4f}"
        print(f"| {name} | {f(mine)} | {f(r)} | {f(m)} | {f(g)} | {delta} |")
    print()

    # 可疑模式（只报事实，不裁决）
    e, k = pub.get("exact"), pub.get("masked")
    if e is not None and k is not None and e > 0.9 and (e - k) >= 0.6:
        flags.append("public 高而 masked 低 ≥0.6：接近背题者形态（背题者 1.0 → 0.125），需附逐题输出证明不是碰运气")
    if e is not None and go.get("exact_public") is not None and abs(e - go["exact_public"]) < 1e-9:
        flags.append("public exact 与『一律答 go』完全一致：说明没读文件，先证明适配器确实读了 ctx")
    if sub.get("controls_pass") is not True:
        flags.append("三对照（参考/背题者/空基线）未通过或未声明：本次按协议应作废（standings 记 void）")
    if sub.get("rerun_consistent") is not True:
        flags.append("同一输入两次运行不一致：协议要求一致，本次作废")
    if not sub.get("adapter_sha256"):
        flags.append("缺 adapter_sha256：无法核对提交物，台账只能记 anon")
    if pub.get("exact") is not None and ref.get("public") is not None and pub["exact"] > ref["public"] + 1e-9:
        flags.append("public exact 超过参考裁判本身：参考裁判就是这套题的一个『照抄原判』上界，超过它通常意味着读到了本不该读的字段")

    if flags:
        print("**可疑项（不裁决，只标出，交由台账 `why_void` 或补充材料处理）：**")
        for x in flags:
            print(f"- {x}")
        print()
        return 1

    print("**未触发任何可疑模式。** 仍不等于独立第三方认证：需另有人按同一流程独立复跑一次，两条日志一致才记 valid。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
