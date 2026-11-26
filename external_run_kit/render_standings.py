"""把外部跑分台账渲染成 Markdown（可直接贴进 Issue / CI summary / README）。

用法：
    python render_standings.py                 # 读同目录 standings.json
    python render_standings.py path/to.json
"""
import json, sys, datetime, pathlib

HERE = pathlib.Path(__file__).parent
DEFAULT = HERE / "standings.json"


def fmt(x):
    if x is None:
        return "—"
    if isinstance(x, float):
        return f"{x:.4f}".rstrip("0").rstrip(".")
    return str(x)


def main():
    p = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    data = json.loads(p.read_text(encoding="utf-8"))
    entries = data.get("entries", [])

    print("## 外部实跑台账（PCCP-Bench）")
    print()
    b = data.get("baseline_reference", {})
    m = data.get("baseline_memoriser", {})
    g = data.get("baseline_always_go", {})
    print(f"基线：参考 `{fmt(b.get('public'))}/{fmt(b.get('masked'))}` · "
          f"背题者 masked `{fmt(m.get('masked'))}` · 空基线 exact `{fmt(g.get('exact_public'))}`")
    print()
    if not entries:
        print(f"**尚无外部队伍提交**（截至 {datetime.date.today().isoformat()}）。公开列可自助跑，隐藏列请走 Issue 认领。")
        return
    print("| 日期 | 队伍 | 公开列 exact | masked | hidden | 对照通过 | 复跑一致 | 状态 |")
    print("|---|---|---|---|---|---|---|---|")
    for e in entries:
        pub = (e.get("public") or {})
        hid = (e.get("hidden") or {})
        print(f"| {e.get('date','')} | {e.get('team','')} | {fmt(pub.get('exact'))} | "
              f"{fmt(pub.get('masked'))} | {fmt(hid.get('exact'))} | "
              f"{'✅' if e.get('controls_pass') else '❌'} | "
              f"{'✅' if e.get('rerun_consistent') else '❌'} | {e.get('status','')} |")
    voids = [e for e in entries if e.get("status") == "void"]
    if voids:
        print()
        print(f"作废 {len(voids)} 条（保留不删，原因写在 `why_void`）：")
        for e in voids:
            print(f"- {e.get('date','')} {e.get('team','')}：{e.get('why_void') or '未填'}")


if __name__ == "__main__":
    main()
