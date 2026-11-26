# PCCP-Bench

![verify-archive](https://github.com/LGD-Eval/pccp-bench/actions/workflows/verify-archive.yml/badge.svg)   ![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24551199.svg)

一个**可判定、可复跑、分数可追到原始输出**的测题集，只问一件事：对一次模型变更，PCCP（Predetermined Change Control Plan）该判 **go / hold / reject** 中的哪一个。

**当前版本 0.1.3 · DOI [10.5281/zenodo.24551199](https://doi.org/10.5281/zenodo.24551199)**（concept DOI [10.5281/zenodo.24550266](https://doi.org/10.5281/zenodo.24550266)）
历史版本： · [0.1.2](https://doi.org/10.5281/zenodo.24551117)（补 evidence/、更正旧数字）
 · [0.1.1](https://doi.org/10.5281/zenodo.24550734)（可跑但分数无证据）
 · [0.1.0](https://doi.org/10.5281/zenodo.24550267)（包内缺裁判依赖，不可直接跑）

- 规模：42 题（公开 32 / 隐藏 10，隐藏题只承诺哈希，不在归档内）
- 每题附所依据的法规原文；第三方可以在**理由**上不同意，而不是在管道上被卡住
- 参考裁判是参考实现，**不是**监管判定，**不是** FDA 背书

## 怎么验（外人可做，不用问我们）

```
curl -L -o p.zip https://zenodo.org/records/24551199/files/pccp-bench_zenodo_v0.1.3.zip
sha256sum p.zip                       # 5151fe7ffa48be46ad55201bf334b536320535805363fa81c3f93a809d942b83
unzip p.zip && cd p
python -c "import hashlib,json;m=json.load(open('MANIFEST.json'));print(all(hashlib.sha256(open(f['archive_path'],'rb').read()).hexdigest()==f['sha256'] for f in m['files']))"
```

- 归档 **82283 字节**，27 个叶子
- 冻结根 `0f1e697b60ea39face648f86a3268006a410b3ec6e93c5adc8e3165e61a1c60f`
- 规则：叶子取文件 sha256 摘要的**字节**、按 path 排序、成对 `sha256(a+b)`、奇数节点与自身配对。
  写成 `sha256(path + NUL + 摘要)` 也能算出个数（`662ba5a7…`），但那是错的，与冻结值不符。

## 怎么跑

```
cd dataset
python bench.py --submit adapter_reference.py   # 参考裁判
python bench.py --commit-check                  # 10 条隐藏题承诺
python bench.py --submit your_adapter.py --team you
```

## 分数与证据

| 行 | public 结论 | masked 结论 | hidden 结论 | public 理由 | masked 理由 | 落差 |
|---|---|---|---|---|---|---|
| 参考实现 | 0.9688 | 0.9688 | 0.9 | 1.0 | 1.0 | 0.0 |
| 背题者（直接读公开答案表） | 1.0 | **0.125** | 0.1 | 1.0 | **0.0312** | **0.875** |

每个数都能在包内 `evidence/` 找到对应的原始输出（运行日志 + 逐题成绩文件 + 承诺核对日志）；
每次跑分自行打出类别分布（`go 28 / hold 4 / reject 0 of 32`）与空基线（一律 go：exact 0.875、宏召回 0.5）。

**旧数字已作废**：早先文档写的"参考 1.0、背题者 masked 0.094"来自旧掩码规则与旧题集状态，重跑为 0.9688 与 0.125。
本台以 `evidence/` 为准，不以任何转述为准。

### 一条如实说明：哪一处不能被外人验证

`evidence/scores/*.json` 的摘要含隐藏题，外人环境没有隐藏集，所以 `--verify` 在外人环境**必然 REFUSE**——预期，不是坏了。
外人可复算的是公开列：重跑 `--submit adapter_reference.py` 应得 `public=0.9688 masked=0.9688 tag=1.0/1.0`，与日志逐字一致。

## 为什么一路升到 0.1.3

- **0.1.1 修"跑不起来"**：0.1.0 把引擎路径写死成作者本机路径，换机即 `ModuleNotFoundError`；补路径后 `judge_pccp.py` 的
  `from .base import …` 又因 `base.py` 未随包发布而失败。0.1.1 把裁判闭包 `judges/` 打进包，
  适配器按 **包内 judges → `LGD_ENGINE_ROOT` → 已安装 `lgd_engine`** 三级加载，并打印 `engine_source()`。
- **0.1.2 修"凭什么信你的数"**：外部模型（DeepSeek-V3，只读公网材料）指出分数无包内证据、两处数字与实测不符；
  本版补 `evidence/`、就地打类别分布、更正旧数。
- **0.1.3 修"卡里写现行会变成假话"**：发布包字节在发布前冻死，卡里写"哪一版现行"必然过期；
  改为只写历史 + concept 关系，并给出"如何自行确认最新版/自身版"的办法。

## 已知分歧

42 题里 2 题（K260973-H1、K260973-N2）我方读作 **hold**、参考裁判判 **reject**；包内 `DECISION_reject_vs_hold.md` 有逐条对照与法规依据。

## 许可

数据 CC BY 4.0（含 `evidence/` 日志）；代码（`bench.py`、`adapter_reference.py`、`judges/`、`make_evidence.py`）Apache-2.0。逐目录见包内 `LICENSE_STATUS.md`。

## 试真台接入

Assurance Instrument Test Bench（试真台）的 `presets/pccp-bench.json` 把冻结根、包内逐字节、版本同号、许可状态、DOI 主张、台子自跑与空基线对照各判一遍；检查器自带反照（改一字节根必须变）。

## 字节在归档里，不在本仓

归档字节一旦进仓，冻结根与包内路径要跟着改，反而多一层可能对不上的地方。本仓只放发布流程、元数据与外部跑分工具包（`external_run_kit/`），归档字节仍在 Zenodo。

## 第三方基础设施上的复跑（不是我们自己说能跑）

仓库里有一个 CI 作业 [`.github/workflows/verify-archive.yml`](https://github.com/LGD-Eval/pccp-bench/blob/main/.github/workflows/verify-archive.yml)，
**跑在 GitHub 自己的机器上**，每次改动和每周一自动执行四件事：

1. 从 Zenodo 下载归档（`records/24551199`）
2. `sha256sum -c` 校验归档字节（`5151fe7f…`）
3. 解包后逐字节核 MANIFEST，并按冻结规则**重算 27 叶子 Merkle 根**，必须等于 `0f1e697b60ea39fa…`
4. 在 `dataset/` 跑参考适配器，`exact public` 与 `masked` 必须都是 0.9688

任何一项不符就红。当前状态见 [最新一次运行](https://github.com/LGD-Eval/pccp-bench/actions/workflows/verify-archive.yml)。

这条能说明的是：**归档、冻结根、参考分数在别人的机器上成立**，不需要信我们任何一句话。
它不能说明的是：题出得好、标签都对、有同行评议——那是另外三件事，别混着读。

## 想当"外部队"（跑分、或只是找茬）

工具包在 [`external_run_kit/`](https://github.com/LGD-Eval/pccp-bench/tree/main/external_run_kit)：
适配器骨架、外部实跑协议、提交前自检清单、只增不删的台账。公开列五条命令自助；隐藏列我们离线代跑、48 小时内交回逐题文件。
入口只有一个：[Issue #1 公开认领](https://github.com/LGD-Eval/pccp-bench/issues/1)——公开认领是为了可追溯，不搞私下排队。

## 裁判闭包 `judges/` 的来源（外人常问）

包内 `judges/` 三个文件来自 lgd-engine 的 `lgd_engine/judges/`（`__init__.py`、`base.py`、`judge_pccp.py`），
**原样复制、不做改写**，作为本评测台的参考裁判实现。上游仓库目前不是公开仓，所以"看源码"这件事
只能靠包里这三份——它们就是本台认定的权威副本，sha256 记载在 `MANIFEST.json` 里，改一字节即可查出。

不隐瞒的一点：裁判是我们自己写的。参考实现的分数高，一部分原因是题也是我们出的——这是循环论证的温床。
缓解手段只有两个，都已落地：一是公开 masked 列（抹掉编号后背题者从 1.0 掉到 0.125），
二是把 2/42 题的分歧（K260973-H1、N2）逐条列出来而不是抹平。

## 论文级缺口：把门槛预先写死，而不是许愿

现在有三条已知边界，其中"单人标注、无 κ"这条**可以靠别人补**，而且门槛不该在看到结果之后再定：

- 协议 `annotation/ANNOTATION_PROTOCOL_v1.md`：三个标签按"计划文本说了什么"定义，五步判定顺序，盲标（不给我们的答案、不给 `evidence/`），每道题必须引用决定它的那句话
- 工具 `annotation/kappa.py`：Cohen's κ + 逐类一致率 + 分歧逐条列出 + 空跑自测（`--selftest` 3/3）
- **阈值现在就定**：κ≥0.60 才写"两个独立标注人实质一致"；0.40–0.59 只能写"中等一致、属限制"；**<0.40 不发论文，改协议不改题**
- 招募入口：[Issue #2](https://github.com/LGD-Eval/pccp-bench/issues/2)

分歧一律公开列题号与双方所引原句，不私了、不"二比一定胜负"。这条比数字重要：改题凑 κ 正是这套协议要防的事。

## 已知边界（不打算假装解决的部分）

外部模型（DeepSeek-V3，只读公网材料）两次反审各提了 5 条必修。能修的都修了：打包闭包、证据日志、
更正旧数字、版本表不写过时措辞。剩下三条**我们没做到，但不等于做不到**——同领域已有两人独立标注、ICC 0.93 的先例（Radiology: AI 2026，Dayma 等）；写在这里而不是留到被人问起：

1. **隐藏题不能公开验字节**。公开到能验字节的程度，就等于公开了题。现在只能"承诺 + 事后交付"。
2. **标注是单人完成**。没有第三方标注、没有 κ 系数。**这不是“做不到”：同领域已有人用两名独立观察者、ICC 0.93 完成同类文档评分**；我们只是还没找到那个人，所以把标注协议与 κ 工具先公开（`annotation/`，Issue #2 招募）。
3. **类别不均衡（go 28 / hold 4 / reject 0）**。不给"平衡方案"，因为改分布就等于改题目意图；
   能做的是每次跑分都把分布和空基线打在输出里，让读者自己打折。

如果你要拿它做论文级结论，这三条就是必须先补的缺口；拿它做工程自检或对外解释，够用。
