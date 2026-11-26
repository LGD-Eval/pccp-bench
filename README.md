# PCCP-Bench

一个**可判定、可复跑**的测题集，只问一件事：对一次模型变更，PCCP（Predetermined Change Control Plan）该判 **go / hold / reject** 中的哪一个。

**当前版本 0.1.1 · DOI [10.5281/zenodo.24550734](https://doi.org/10.5281/zenodo.24550734)**（concept DOI [10.5281/zenodo.24550266](https://doi.org/10.5281/zenodo.24550266)，所有版本挂在它下面）
上一版 [0.1.0](https://doi.org/10.5281/zenodo.24550267) 仍然可核验，但**不要再引用**：包内缺裁判依赖，换台机器就跑不起来（详见"为什么有 0.1.1"）。

- 规模：42 题（公开 32 / 隐藏 10，隐藏题只承诺哈希，不在归档内）
- 每题带所依据的法规原文，第三方可以在**理由**上不同意，而不是在管道上被卡住
- 参考裁判是参考实现，**不是**监管判定，**不是** FDA 背书

## 怎么验（外人可做，不用问我们）

```
curl -L -o p.zip https://zenodo.org/records/24550734/files/pccp-bench_zenodo_v0.1.1.zip
sha256sum p.zip                       # a6665d790122993e0dd9a8eb6019a61b9c3ba7aadc27b336e94693fe28a8d42a
unzip p.zip && cd p
python -c "import hashlib,json;m=json.load(open('MANIFEST.json'));print(all(hashlib.sha256(open(f['archive_path'],'rb').read()).hexdigest()==f['sha256'] for f in m['files']))"
```

- 归档大小 **68661 字节**，18 个叶子
- 冻结根 `59f8507b5bed0a3e258f390d5f35f3704eb32ef069c564bd36c959106df3abe6`
- 规则：叶子取文件 sha256 摘要的**字节**、按 path 排序、成对 `sha256(a+b)`、奇数节点与自身配对 —— 照此复算必得同一根。
  写成 `sha256(path + NUL + 摘要)` 也能算出一个数（`662ba5a7…`），但那是错的，与冻结值不符。

## 怎么跑

解包后进 `dataset/`：

```
python bench.py --submit adapter_reference.py   # 参考裁判：public 0.9688 / masked 0.9688 / tag 1.0
python bench.py --commit-check                  # 10 条隐藏题承诺（无隐藏题时 PASS）
python bench.py --submit your_adapter.py --team you
```

适配器逐题收到一个案例，返回 go/hold/reject 与理由；分数是精确匹配、宏平均召回、引用标签三项。
空基线"一律 go"精确匹配 0.875 但宏召回只有 0.5 —— 让偷懒答案在头条数字上获胜的集合等于没测，所以两项并列报出。

## 为什么有 0.1.1（一个自己抓到的致命缺陷）

0.1.0 里参考适配器把引擎路径写死成作者本机的 `D:\Workbuddy\...\lgd-engine`。在那台机器上参考裁判跑出 0.9688、一切正常；
换任何一台机器就是 `ModuleNotFoundError: No module named 'lgd_engine'`。**只在出生地能跑的包不是可复现的包，是一张截图。**

只补一条路径还不够：改成加载包内 `judge_pccp.py` 后，它内部的 `from .base import DomainJudge, ...` 立刻失败，
因为 `base.py` 从来没随包发布——于是得到一个"看起来自包含"、实际第一行就 `ImportError` 的包。

0.1.1 的做法：把裁判最小闭包 `judges/`（`judge_pccp.py` + `base.py` + `__init__.py`，来自 lgd-engine，原样复制）打进包；
适配器按 `包内 judges → LGD_ENGINE_ROOT → 已安装 lgd_engine` 三级加载，并打印 `engine_source()` 说明这次用的是哪一份。
实测：在无引擎的干净目录解包即跑，`engine_source()` 打印 `judges (vendored in this bundle)`，分数 0.9688/0.9688/1.0。

## 已知分歧

42 题里 2 题（K260973-H1、K260973-N2）我们读作 **hold**、参考裁判判 **reject**。分歧公开列着，不悄悄抹平 —— 一个把自身分歧藏起来的基准，是在要求被信任而不是被检验。

## 试真台接入

Assurance Instrument Test Bench（试真台）有一份 `presets/pccp-bench.json`，把冻结根、包内逐字节、版本同号、许可状态、DOI 主张、台子自跑与空基线对照各判一遍；检查器自带反照（改一字节根必须变）。

## 许可

数据 CC BY 4.0；归档内代码（`bench.py`、`adapter_reference.py`、`judges/`）另注 Apache-2.0，逐目录见包内 `LICENSE_STATUS.md`。

## 这里暂不放数据集字节

字节在归档里（上面那个 DOI）。本仓只放发布流程与元数据；归档字节一旦进仓，冻结根与包内路径就要跟着改，反而多一层可能对不上的地方。
