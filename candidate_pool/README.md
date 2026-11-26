# 候选池 v2（未冻结，未发布）

这 37 道题**不是** PCCP-Bench 0.1.3 的一部分，也不在 Zenodo 归档里。放出来只为一件好事：**在我们冻结之前让别人挑错**。

## 状态（照实说）

| 项 | 状态 |
|---|---|
| 冻结根 / DOI | **无**——没有冻结，没有发布 |
| 标注 | **单人**（LGD）；第二标注人未到位（见 [Issue #2](https://github.com/LGD-Eval/pccp-bench/issues/2)、`annotation/ANNOTATION_PROTOCOL_v1.md`） |
| 数量 | **37 题：`go 13 / hold 7 / reject 17`**；7 台器械、5 个器械族 |
| 引文 | 每题都有 FDA 决策文件正文逐字句；**"这句确实在 PDF 里"必须由人打开 PDF 搜一遍**，我们不代你确认 |

## 分布（族 / 器械 / 题）

| 族 | 器械（K 号） | 题 |
|---|---|---|
| 超声 | K251456 BrightHeart v1.1、K243684 BrightHeart、K233955 Clarius OB AI | 15 |
| MRI | K240290 AiMIFY | 5 |
| 乳腺摄影 | K241561 MammoScreen BD | 5 |
| 牙科 X 光 | K250753 VELMENI for DENTISTS (V4D) | 5 |
| 胸部 CT | K241891 ScreenDx（ILD 转诊） | 7 |

来源 PDF 全部可直点，前缀均为 `https://www.accessdata.fda.gov/cdrh_docs/`：
`pdf25/K251456`、`pdf24/K243684`、`pdf23/K233955`、`pdf24/K240290`、`pdf24/K241561`、`pdf25/K250753`、`pdf24/K241891`。

## 为什么 reject 要占近一半

0.1.3 的公开列 32 题里 `go 28 / hold 4 / reject 0`，**"一律答 go"就能拿 0.875**——这是台子最硬的结构缺陷。v2.2 把 `reject` 拉到 17 道，全部落在 FDA 文件里写得明明白白的硬边界：

| 类型 | 例子（都是原文边界） |
|---|---|
| 患者人群越界 | 恒牙 / ≥15 岁（K250753）、>22 岁（K241891）、经腹探头（K251456） |
| 模态/输入越界 | `Clarius OB AI is intended for use in B-Mode only`；`The input to ScreenDx is a DICOM-compliant lung CT scan` |
| 器械绑定越界 | `not a stand-alone software device`；非 Clarius 第三方超声机 |
| 功能越界 | `no localization information and there is no … annotations`（ScreenDx）；`Annotated DICOM files … cannot be modified by the user`（BrightHeart） |
| 适应证越界 | `None of the changes shall result in a change to the Indications for Use`（AiMIFY）；`not intended to rule-out or rule-in lung fibrosis` |
| 部署越界 | `No changes are made to the deployment environment or inference pipeline`（VELMENI） |
| 检测病种越界 | 计划只含龋齿/修复体/固定桥/种植体，新增根尖周病变即范围外（K250753） |

**算式投影**：`(28+13)/(42+37) = 0.519`——一律答 go 从 **0.875 降到约 0.52**。这是算式，不是实测；实测要等冻结重跑。

## 冻结门槛三查（今天）

| 门槛 | 现状 |
|---|---|
| ① 第二标注人完成并算出 κ（≥0.40 继续，≥0.60 才写"实质一致"） | **✗ 0 人、0 次** |
| ② 每句原句两人各自能在 PDF 里搜到 | ✗ 仅我一人搜过 |
| ③ `reject` ≥12 且族 ≥3 | **✓ 17 道 / 5 族** |
| （附加）全部题带逐字引文 | ✓ 37/37 |

**所以：不冻结、不发 0.1.4。** 第 ③ 条刚满足，①②卡在人。

## 已知薄弱处（先说，不等你发现）

1. **`K241561-R4` 引文最弱**：用"表内只列三项"代替"计划明说不行"，建议撤掉重做。
2. **7 道 `hold` 依赖"必要条件"读法**：单标注判 hold，第二标注人可能判 reject，κ 会掉——这是要测的歧义，不是要藏的事。
3. **K251456 与 K243684 是同一器械两代**，刻意用来测跨代一致性；若被判"重复计数"，冻结时拆两个 subset 报分。
4. **超声仍占 15/37**：族数够了，权重还不均。
5. **37 题≠FDA PCCP 清单 240 条的代表抽样**，属非随机便利抽样，报分时不得外推为"整体合规率"。

## 怎么用

- 标签有异议：在 [Issue #2](https://github.com/LGD-Eval/pccp-bench/issues/2) 写 `题号 + 你的标签 + 你引的原句`。**不带原句的分歧不收**，这条对我们也一样。
- 想当第二标注人：按协议盲标，**先别看这个 JSON**。
- 想跑分：用 0.1.3 归档（`10.5281/zenodo.24551199`）；候选池尚未进台子。

## 引文强度分级（v2.2 起）

| 级别 | 含义 | 数量 |
|---|---|---|
| `solid` | 引文直接含测试/判据/边界原句 | 3 |
| `fair` | 只引到"不越界"条款或计划表枚举，需第二标注人确认读法 | 2 |
| `weak` | 引文撑不住标签 | **0（已清零）** |

v2.1 的 2 条 `weak`（`K240290-R1`、`K241561-R4`）已通过回到 PDF 原文补实或改引枚举，现分别为 `fair`/`fair`；`K241561-R1/R2/R3` 三条已升 `solid`。
