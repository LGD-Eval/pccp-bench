# 候选池 v0（未冻结，未发布）

这 14 道题**不是** PCCP-Bench 0.1.3 的一部分，也不在 Zenodo 归档里。它们放在仓里只为一件好事：**让别人在我们冻结之前就能挑错**。

## 状态（照实说）

| 项 | 状态 |
|---|---|
| 冻结根 / DOI | **无**——没有冻结，没有发布 |
| 标注 | **单人**（LGD）一份；第二标注人尚未到位（见 [Issue #2](https://github.com/LGD-Eval/pccp-bench/issues/2)、协议 `annotation/ANNOTATION_PROTOCOL_v1.md`） |
| 引文来源 | 全部取自 FDA 决策文件正文（510(k) Summary 的 PCCP 段），三条直达链接见下 |
| 引文校验 | 自动校验只做了长度与字段完整性；**"这句话确实在 PDF 里"需要人打开 PDF 搜一遍**——这是留给你的活，也是我们要求的活 |
| 分布 | 14 题：`go 7 / hold 3 / reject 4`；器械族：超声 5、MRI 5、乳腺摄影 4 |

## 来源（可直点，均为公开决策文件）

- K251456 BrightHeart View Classifier v1.1（胎儿心脏超声切面分类）：https://www.accessdata.fda.gov/cdrh_docs/pdf25/K251456.pdf
- K240290 AiMIFY（MRI 增强，Subtle Medical）：https://www.accessdata.fda.gov/cdrh_docs/pdf24/K240290.pdf
- K241561 MammoScreen BD（乳腺密度，Therapixel）：https://www.accessdata.fda.gov/cdrh_docs/pdf24/K241561.pdf

## 我们已知的薄弱处（先说，不等你发现）

1. **`K241561-R4` 的引文最弱**：我用的是表格前的说明句（"The table below explains, for each Predetermined change…"）加一句"表内仅列 GE、Siemens 与骨干预训练"。严格讲这不是"计划没写"的直接引证，而是"表里没有"。要么补一句更硬的原文，要么撤掉这题。**我倾向撤掉重做。**
2. **"缺步骤判 hold" 的三题（K251456-R4、K240290-R3、K241561-R3）依赖"必要条件"的读法**：PCCP 把这些测试/比较写成该类修改的必要条件，我们据此判 hold。若第二标注人认为"计划没写验收方式"应算 reject，κ 会掉——这正是要测的歧义点，不是要藏的事。
3. **全部 14 题来自 3 台器械、3 个族**，不代表 FDA PCCP 清单 240 条的整体。加题优先补 `reject` 与其它族（心血管、病理、内镜）。
4. 每道题都是"读计划文本 + 判断"，不含"看代码/看数据"的工序；这是题集定位，不是缺陷，但别拿它当"全面合规审计"。

## 怎么用

- 觉得某题标签错了：在 [Issue #2](https://github.com/LGD-Eval/pccp-bench/issues/2) 或 [Issue #1](https://github.com/LGD-Eval/pccp-bench/issues/1) 里写 `题号 + 你的标签 + 你引的原句`。**不带原句的分歧我们不收**，这条对我们也一样。
- 想当第二标注人：按协议盲标，不要先看这个 JSON（看了就不算独立）。
- 想跑分：用 0.1.3 归档（`10.5281/zenodo.24551199`），候选池尚未进台子。

## 什么时候冻结

满足三条才冻：①第二标注人完成并算出 κ（≥0.4 才继续，≥0.6 才敢写"实质一致"）；②每道题的原句由两人各自能在 PDF 里搜到；③`reject` 类补到 ≥6 道，避免"三类其实只有两类"的批评。
