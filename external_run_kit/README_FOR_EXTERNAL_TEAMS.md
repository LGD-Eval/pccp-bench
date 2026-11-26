# 给外来队的跑分快包（v1，2026-11-26）

你不需要联系我们就能跑公开列；隐藏列由我们代跑并把逐题成绩交回。包内四件：

| 文件 | 用途 |
|---|---|
| `adapter_template.py` | 你要填的适配器骨架；不填也能跑（保守占位：越界即 hold），用来验证环境 |
| `外部实跑协议_v1.md` | 规则、反照、时间线、边界 |
| `提交清单.md` | 提交前自检表，照着打勾 |
| `standings.json` | 台账结构（只增不删），告诉你我们会记录什么 |

## 三分钟跑通

```bash
curl -L -o p.zip https://zenodo.org/records/24551199/files/pccp-bench_zenodo_v0.1.3.zip
sha256sum p.zip    # 应为 5151fe7ffa48be46ad55201bf334b536320535805363fa81c3f93a809d942b83
unzip p.zip && cd p/dataset

python bench.py --submit adapter_reference.py     # 参考裁判：public 0.9688 / masked 0.9688 / tag 1.0
python bench.py --submit ../../adapter_template.py --team 你的队名
```

## 你要实现的只有一件事

```python
def evaluate(ctx: dict) -> dict:
    return {"verdict": "go" | "reject" | "hold", "tag": "六词之一", ...}
```

- 六个理由词：`ok_covered`、`outside_scope`、`acceptance_not_met`、`evidence_missing`、`intended_use_change`、`unclassifiable`
- 不许读 `expected_verdict` / `expected_tag`，不许改题，不许联网查 K 号答案
- 同一输入两次运行必须一致

## 你会看到什么

```
你的队名: exact public=… masked=… hidden=n/a (public bundle) tag=… gap=… sha=…
  macro_recall(verdict) public=… masked=… tag=…
  baseline: always-'go' scores exact=0.875 but macro_recall=0.5 -- exact alone is not a result.
  mix(public): go=28, reject=0, hold=4 of 32 -- skewed by design; read exact rate as base rate + skill.
```

`hidden=n/a` 是设计：公开包不带隐藏题。想要第三列，把 `adapter.py` 交给我们离线代跑。

## 提交什么（代跑）

1. `adapter.py`（或整个目录，若有依赖）
2. 队名（或要求匿名 → 我们只公开 sha256 前 8 位）
3. 一句许可声明：允许公开你的分数与「仅供参考、非监管结论」的免责说明

## 我们承诺 / 不承诺

- 承诺：48 小时内回结果；分数好坏不删不改；不因成绩改题（改题只能靠新版本承载）。
- 不承诺：不给隐藏题、不给逐题对错反馈（等于泄题）。

## 跑完自己就能对比

```bash
python compare.py 你的结果.json
```

它会把你的分与三条基线（参考裁判 / 背题者 / 一律答 go）排在一张表里，并直接标出可疑模式：public 高而 masked 塌陷、与空基线完全相同、复跑不一致、以及超过参考裁判本身。**退出码 1 表示触发了可疑项**，不阻断你提交，但我们会按 `standings.json` 的规则记 `void` 或要求补充材料。

我们自己也用同一个脚本，没有内部版本。
