# 同类工作对照（2026-11-26）：我们比谁强，谁比我们强

这份文件的用途：让「我们查过同类工作」这句话**可核**。每条都带原文链接，并且**明确写出竞品强于我们的地方**——只列自己赢的对比表没有核验价值。

## 检索面（必须一起读）

- 时间：2026-11-26 当日检索。
- 范围：PubMed / npj Digital Medicine / Radiology: AI / FDA CDRH 公开决策文件 / GitHub 公开仓库。
- 关键词：`predetermined change control plan`、`PCCP`、`AI/ML-enabled medical device modification`、`change control benchmark`、`benchmark dataset PCCP evaluation`。
- 结论措辞只能是：**「在这个检索面内，我们没有找到比 PCCP-Bench 更贴近‘可复跑判定台’的公开物」**。不是「世界上没有」，也不是「我们最好」。

## 两张表能查到的东西

### AEGIS（npj Digital Medicine 9:789，2026）

链接：[nature.com/articles/s41746-026-03290-1](https://www.nature.com/articles/s41746-026-03290-1)

它做的是**治理基础设施**：DARM（数据获取与准备）/ MMM（模型监测）/ CDM（变更决策），决策用**四类** APPROVE / CONDITIONAL APPROVAL / CLINICAL REVIEW / REJECT，另有**独立的 PMS ALARM**，允许「REJECT + ALARM」复合态。规模：PhysioNet 20,336 名患者、11 轮迭代；BraTS 2,601 例。

**它比我们强在哪（照实写）**：

| 维度 | AEGIS | 我们 |
|---|---|---|
| 真实临床数据 | 20,336 名患者、11 轮 | **0**（全部是 FDA 决策文件文本） |
| 判定类别 | 四类 + 独立告警通道 | 四类（`go` / `hold-insufficient` / `hold-resubmit` / `reject`），无独立告警 |
| 漂移场景 | 有专门构造 | **无** |

**它的收尾句（逐字，这是它自己承认的缺口）**：

> "Development of standardized benchmark datasets and drift scenarios specifically designed for PCCP framework evaluation would facilitate reproducible comparison of governance approaches across the research community."

换句话说：**它呼吁有人来建我们这种东西**。这既是我们存在的理由，也是我们必须承认它比我们更接近真实部署的地方。

### RSNA《Radiology: Artificial Intelligence》`10.1148/ryai.260385`（Dayma 等，SUNY Upstate）

链接：[pubs.rsna.org/doi/10.1148/ryai.260385](https://pubs.rsna.org/doi/10.1148/ryai.260385)

它做的是**真实器械面的实证统计**：1,080 / 1,394 = 77.5% 为放射类；全 panel 170 台器械带有 PCCP；放射类 34/37 = 91.9%；34 台里 22 台（65%）在 2025 一年内放行；文档 8 分制均值 5/8；两名独立观察者 ICC 0.93；9/34（27%）官方库与摘要不一致需人工裁决；公开摘要普遍缺持续监控与漂移触发。

**它比我们强在哪（照实写）**：

| 维度 | RSNA | 我们 |
|---|---|---|
| 器械样本 | 170 台（全 panel，截至 2026-04） | 7 台 / 5 族 |
| 独立双人标注 | **两名独立观察者，ICC 0.93** | **0 名第二标注人，κ 未计算** |
| 决策体量 | 1,080 条 | 42 + 37 道题 |

**它没有的东西**：一个别人能下载、能复算字节、能在自己机器上跑出同一个分数的判定台。它的 ICC 0.93 是**它自己的**标注一致性，外部无法复现那 1,080 条标签，因为没有发布逐条数据与判据。

## 我们真正独有的三件（都可当场核）

1. **字节可复算**：归档 zip sha256 `5151fe7f…`，27 个文件逐字节对 MANIFEST，Merkle 根在 **GitHub 自己的机器上**复算通过（[CI](https://github.com/LGD-Eval/pccp-bench/actions)），不是我们本机自述。
2. **分数可复跑**：任何人 `python bench.py --submit adapter_reference.py` 得到 `exact public=0.9688 masked=0.9688`（0.1.3 自身 32 题）——CI 每次改动都断言这个数，漂了就红。
3. **分歧全公开**：19 条标签与裁判不一致的题，逐题带原句与 PDF 直链（[DISAGREEMENT_37.md](DISAGREEMENT_37.md)）。同类工作没有一家公开自己内部两个部件打架的明细。

## 结论（不许升级成更强的说法）

- 可以说：**在这个检索面内，没有找到可复跑、字节可验、并公开内部分歧的 PCCP 判定台；PCCP-Bench 是其中之一（目前唯一一个被我们找到的）。**
- 不可以说：「最先进」「业界第一」「已获认可」。
- 必须同时说：**规模上我们远小于 AEGIS（20,336 患者）与 RSNA（170 台器械 / 1,080 条决策）；标注独立性我们为 0，RSNA 有 ICC 0.93。**

这三条一起写，才是能过审的说法。

## 补充检索（2026-11-26 16:39，当日第二次）

第一轮检索漏了两个对象，补在这里，并按同样规则写它们强于我们的地方。

### ① IntuitionLabs《MedTech AI Quality Benchmark: Validation and PCCPs》（2026-09）

链接：[intuitionlabs.ai/articles/medtech-ai-quality-benchmark](https://intuitionlabs.ai/articles/medtech-ai-quality-benchmark)

做的是**跨产品 PCCP 成熟度记分**：把「未计划 / 起草 / 已递交 / 已授权未使用 / 已授权并已执行」五态分开统计，禁止把「讨论过」算成「已授权」，并要求先报原始 n 与题目分母、低于阈值的小格不报。

**它比我们强在哪**：覆盖**产品面**（跨厂商横向记分），我们只覆盖 37 道文本题；它的口径直接对齐 FDA/Health Canada/MHRA 的联合五原则，我们的判定类别仍是我们自己定的。

**它没有的**：逐条可下载数据与可复算判定；它的分数依赖问卷回收，不可外部复现。

### ② arXiv 2607.19020《Audit Before You Update》（MIMIC-IV 变更有界评测）

链接：[arxiv.org/html/2607.19020v5](https://arxiv.org/html/2607.19020v5)

做的是**变更策略的实证评测**：先审计 MIMIC-IV 的录入伪影，再用无标签双样本检验做变更门控，在预设非劣界 0.015 AUROC 下比较「有界更新」与全量微调。

**它比我们强在哪**：有真实 ICU 队列、有统计检验与预设非劣界、有归因稳定性度量；我们的判据来自文本，没有任何统计学意义上的效果测量。

**它没有的**：没有 PCCP 判定标签体系，也没有可复跑的判定台——它的贡献是方法，不是基准。

## 计数（据以上两轮检索）

| 层级 | 对象 | 与我们同型？ |
|---|---|---|
| 直接同类（可复跑+字节可验+公开内部分歧的 PCCP 判定台） | **0 个**（除我们） | — |
| 强相邻｜治理基础设施 + 四类决策 | AEGIS | 否（无开放基准） |
| 强相邻｜真实器械面实证统计 | RSNA | 否（不发布逐条数据） |
| 强相邻｜跨产品成熟度记分 | IntuitionLabs | 否（问卷制，不可复跑） |
| 强相邻｜变更策略方法评测 | arXiv 2607.19020 | 否（方法非基准） |

合计 **5 个可比对象，0 个同型**。这个 0 只在本检索面成立。
