# PCCP-Bench

一个**可判定、可复跑、分数可追到原始输出**的测题集，只问一件事：对一次模型变更，PCCP（Predetermined Change Control Plan）该判 **go / hold / reject** 中的哪一个。

**当前版本 0.1.2 · DOI [10.5281/zenodo.24551117](https://doi.org/10.5281/zenodo.24551117)**（concept DOI [10.5281/zenodo.24550266](https://doi.org/10.5281/zenodo.24550266))
历史版本：[0.1.1](https://doi.org/10.5281/zenodo.24550734)（可跑但分数无证据，已被取代） · [0.1.0](https://doi.org/10.5281/zenodo.24550267)（包内缺裁判依赖，不可直接跑）

- 规模：42 题（公开 32 / 隐藏 10，隐藏题只承诺哈希，不在归档内）
- 每题带所依据的法规原文，第三方可以在**理由**上不同意，而不是在管道上被卡住
- 参考裁判是参考实现，**不是**监管判定，**不是** FDA 背书

## 怎么验（外人可做，不用问我们）

```
curl -L -o p.zip https://zenodo.org/records/24551117/files/pccp-bench_zenodo_v0.1.2.zip
sha256sum p.zip                       # cb25b3279ee37b7711c2d930c2c8e960ddc312889cc9b8a5ed00df51304b015d
unzip p.zip && cd p
python -c "import hashlib,json;m=json.load(open('MANIFEST.json'));print(all(hashlib.sha256(open(f['archive_path'],'rb').read()).hexdigest()==f['sha256'] for f in m['files']))"
```

- 归档 **82572 字节**，27 个叶子
- 冻结根 `751eececc917a27f90803644a569675e3790393f83dba2105e104dcabef694c7`
- 规则：叶子取文件 sha256 摘要的**字节**、按 path 排序、成对 `sha256(a+b)`、奇数节点与自身配对。
  写成 `sha256(path + NUL + 摘要)` 也能算出个数（`662ba5a7…`），但那是错的，与冻结值不符。

## 怎么跑

```
cd dataset
python bench.py --submit adapter_reference.py   # 参考裁判
python bench.py --commit-check                  # 10 条隐藏题承诺
python bench.py --submit your_adapter.py --team you
```

## 分数与证据（这一版的重点）

| 行 | public 结论 | masked 结论 | hidden 结论 | public 理由 | masked 理由 | 落差 |
|---|---|---|---|---|---|---|
| 参考实现 | 0.9688 | 0.9688 | 0.9 | 1.0 | 1.0 | 0.0 |
| 背题者（直接读公开答案表） | 1.0 | **0.125** | 0.1 | 1.0 | **0.0312** | **0.875** |

每个数都能在包内 `evidence/` 找到对应的原始输出（运行日志 + 逐题成绩文件 + 承诺核对日志）；
每次跑分还会自己打出类别分布（`go 28 / hold 4 / reject 0 of 32`）与空基线（一律 go：exact 0.875、宏召回 0.5）。

**旧数字已作废**：早先文档写的"参考 1.0、背题者 masked 0.094"来自旧掩码规则与旧题集状态，本版重跑为 0.9688 与 0.125。
本台以 `evidence/` 为准，不以任何转述为准。

### 一条如实说明：哪一处不能被外人验证

`evidence/scores/*.json` 的摘要含隐藏题，外人环境没有隐藏集，所以 `--verify` 在外人环境**必然 REFUSE**——这是预期，不是坏了。
外人可复算的是公开列：重跑 `--submit adapter_reference.py` 应得 `public=0.9688 masked=0.9688 tag=1.0/1.0`，与日志逐字一致。
把这条限制写进包内，是刻意的：一份说自己"哪里不能被验证"的交付，比一份处处自称"已验证"的交付可信。

## 为什么有 0.1.1 / 0.1.2

- **0.1.1 修"跑不起来"**：0.1.0 把引擎路径写死成作者本机路径（`D:\Workbuddy\...`），换机器就 `ModuleNotFoundError`；
  只补路径还不够，`judge_pccp.py` 内部 `from .base import …` 又因 `base.py` 从未随包发布而失败。
  0.1.1 把裁判最小闭包 `judges/`（`judge_pccp.py` + `base.py` + `__init__.py`，原样复制）打进包，
  适配器按 **包内 judges → `LGD_ENGINE_ROOT` → 已安装 `lgd_engine`** 三级加载，并打印 `engine_source()` 说明用的是哪一份。
- **0.1.2 修"凭什么信你的数"**：外部模型（DeepSeek-V3，只读公网材料）指出分数没有包内证据，且两处数字与实测不符。
  本版补 `evidence/`、就地打类别分布、更正旧数。

## 已知分歧

42 题里 2 题（K260973-H1、K260973-N2）我方读作 **hold**、参考裁判判 **reject**；包内 `DECISION_reject_vs_hold.md` 有逐条对照与法规依据。
分歧公开列着，不悄悄抹平——把自家分歧藏起来的基准，是在要求被信任而不是被检验。

## 许可

数据 CC BY 4.0（含 `evidence/` 日志）；代码（`bench.py`、`adapter_reference.py`、`judges/`、`make_evidence.py`）Apache-2.0。逐目录见包内 `LICENSE_STATUS.md`。

## 试真台接入

Assurance Instrument Test Bench（试真台）的 `presets/pccp-bench.json` 把冻结根、包内逐字节、版本同号、许可状态、DOI 主张、台子自跑与空基线对照各判一遍；检查器自带反照（改一字节根必须变）。

## 字节在归档里，不在本仓

归档字节一旦进仓，冻结根与包内路径要跟着改，反而多一层可能对不上的地方。本仓只放发布流程与元数据。
