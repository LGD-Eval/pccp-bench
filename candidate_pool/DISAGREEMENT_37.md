# 37 道候选题：标签与参考裁判的分歧全记录

这份文件存在的理由只有一个：**我们自己的两个部件在 19 道题上意见不一致，而我把这 19 道连原句一起放出来，让任何人能手工复核，而不是让读者只看到一个 0.486。**

## 一句话结论

一致 **18/37 = 0.486**；一律答 `go` 的空基线 **0.351**。分歧 19 条，**全部落在同一个判据轴**，不是散乱错误。

机读版：[`disagreement_37.json`](disagreement_37.json)（含每题原句与 PDF 直链，字段 `our_label` 与 `judge` 可直接对比）。

## 分歧只有两个原因（合并同类）

| 引擎规则 | 引擎做法 | 我们的做法 | 条数 |
|---|---|---|---|
| `P-CRIT-03-acceptance-criteria-not-met` | 计划里的判据未达成 → 直接判 **reject** | 判 `hold/insufficient`：缺必要步骤是「材料没做」，不是「不许做」 | 7 |
| `P-CRIT-02-intended-use-change` | 动了适应证 / 人群 / 模态 → 直接判 **Veto = reject** | 判 `hold/resubmit`：§515C(b) 没覆盖不等于禁止，只是必须另交 | 12 |

**两条规则合起来覆盖全部 19 条分歧**：引擎看「条件是否成立」，我们看「这次变更属于哪种处置」。同一份文件，两种读法都能自圆其说 —— 这就是为什么它需要第二标注人，而不是我一个人改数字。

## 逐题（19 条）

| 题号 | 器械 | 被改的东西 | 我们的标签 | 引擎 | 触发规则 | 源文件 |
|---|---|---|---|---|---|---|
| `K251456-R4` | BrightHeart View Classifier v1.1 | 重训后直接发布新版本：没有与原模型做性能指标比较，也没有验证与确认记录 | **hold/insufficient** | reject | `P-CRIT-03-acceptance-criteria-not-met` | [K251456](https://www.accessdata.fda.gov/cdrh_docs/pdf51/K251456.pdf) |
| `K251456-R5` | BrightHeart View Classifier v1.1 | 把适用范围扩到经阴道探头（原器械仅验证并仅限经腹探头） | **hold/resubmit** | reject | `P-CRIT-02-intended-use-change` | [K251456](https://www.accessdata.fda.gov/cdrh_docs/pdf51/K251456.pdf) |
| `K240290-R3` | AiMIFY | 为缩短处理时间改用增加输出通道的重训模型，但未按原端点与验收判据重做性能测试 | **hold/insufficient** | reject | `P-CRIT-03-acceptance-criteria-not-met` | [K240290](https://www.accessdata.fda.gov/cdrh_docs/pdf40/K240290.pdf) |
| `K240290-R4` | AiMIFY | 把适应证从脑部 MRI 扩到脊柱 MRI | **hold/resubmit** | reject | `P-CRIT-02-intended-use-change` | [K240290](https://www.accessdata.fda.gov/cdrh_docs/pdf40/K240290.pdf) |
| `K241561-R3` | MammoScreen BD | 把骨干网络改为无监督预训练（计划内），但跳过与 5 位放射科医师的一致性测试 | **hold/insufficient** | reject | `P-CRIT-03-acceptance-criteria-not-met` | [K241561](https://www.accessdata.fda.gov/cdrh_docs/pdf41/K241561.pdf) |
| `K241561-R4` | MammoScreen BD | 新增一个计划里没写的厂商（如 Fujifilm）的乳腺机支持 | **hold/resubmit** | reject | `P-CRIT-02-intended-use-change` | [K241561](https://www.accessdata.fda.gov/cdrh_docs/pdf41/K241561.pdf) |
| `K243684-R2` | BrightHeart View Classifier（K243684） | 扩妊娠年龄段只加数据、不重训也不与原模型比较就发布 | **hold/insufficient** | reject | `P-CRIT-03-acceptance-criteria-not-met` | [K243684](https://www.accessdata.fda.gov/cdrh_docs/pdf43/K243684.pdf) |
| `K243684-R3` | BrightHeart View Classifier（K243684） | 允许用户在设备内修改 AI 生成的标注 DICOM | **hold/resubmit** | reject | `P-CRIT-02-intended-use-change` | [K243684](https://www.accessdata.fda.gov/cdrh_docs/pdf43/K243684.pdf) |
| `K243684-R4` | BrightHeart View Classifier（K243684） | 把用户人群扩到非专业人员/非产前超声环境（如助产士自助使用） | **hold/resubmit** | reject | `P-CRIT-02-intended-use-change` | [K243684](https://www.accessdata.fda.gov/cdrh_docs/pdf43/K243684.pdf) |
| `K233955-R3` | Clarius OB AI | 只改后处理算法把图像看着更顺眼，不做与原模型的性能比较、也不做临床验证 | **hold/insufficient** | reject | `P-CRIT-03-acceptance-criteria-not-met` | [K233955](https://www.accessdata.fda.gov/cdrh_docs/pdf33/K233955.pdf) |
| `K233955-R5` | Clarius OB AI | 从 B 模式扩到彩色多普勒/弹性成像模式下的自动测量 | **hold/resubmit** | reject | `P-CRIT-02-intended-use-change` | [K233955](https://www.accessdata.fda.gov/cdrh_docs/pdf33/K233955.pdf) |
| `K233955-R6` | Clarius OB AI | 从凸阵探头扩到线阵/相控阵探头采集的数据 | **hold/resubmit** | reject | `P-CRIT-02-intended-use-change` | [K233955](https://www.accessdata.fda.gov/cdrh_docs/pdf33/K233955.pdf) |
| `K250753-R2` | VELMENI for DENTISTS (V4D) | 重训后指标只对上一版报了数，没和原清关模型比，也没走预定义判据闸门就上线 | **hold/insufficient** | reject | `P-CRIT-03-acceptance-criteria-not-met` | [K250753](https://www.accessdata.fda.gov/cdrh_docs/pdf50/K250753.pdf) |
| `K250753-R4` | VELMENI for DENTISTS (V4D) | 新增计划外的检测病种（如根尖周病变、牙周骨丧失） | **hold/resubmit** | reject | `P-CRIT-02-intended-use-change` | [K250753](https://www.accessdata.fda.gov/cdrh_docs/pdf50/K250753.pdf) |
| `K250753-R5` | VELMENI for DENTISTS (V4D) | 把推理管线搬到本地边缘部署（脱离现有部署环境） | **hold/resubmit** | reject | `P-CRIT-02-intended-use-change` | [K250753](https://www.accessdata.fda.gov/cdrh_docs/pdf50/K250753.pdf) |
| `K241891-R3` | ScreenDx | 调阈值把阳性率降下来减少报警，但不做统计评估、不出非劣证据 | **hold/insufficient** | reject | `P-CRIT-03-acceptance-criteria-not-met` | [K241891](https://www.accessdata.fda.gov/cdrh_docs/pdf41/K241891.pdf) |
| `K241891-R5` | ScreenDx | 把适用人群扩到 ≤22 岁 | **hold/resubmit** | reject | `P-CRIT-02-intended-use-change` | [K241891](https://www.accessdata.fda.gov/cdrh_docs/pdf41/K241891.pdf) |
| `K241891-R7` | ScreenDx | 把输入模态从 CT 扩到胸部 X 光片 | **hold/resubmit** | reject | `P-CRIT-02-intended-use-change` | [K241891](https://www.accessdata.fda.gov/cdrh_docs/pdf41/K241891.pdf) |
| `K241561-R5` | MammoScreen BD | 把适用人群从“≥40 岁无症状筛查女性”扩到 40 岁以下或有症状的诊断性乳腺检查 | **hold/resubmit** | reject | `P-CRIT-02-intended-use-change` | [K241561](https://www.accessdata.fda.gov/cdrh_docs/pdf41/K241561.pdf) |

## 手工复核怎么做（三步，不用我们的代码）

1. 点开上表的源文件链接，打开 FDA 决策文件 PDF。
2. 在 PDF 里搜每题 `disagreement_37.json` 中 `cite` 字段那一段原句（搜前 6 个词即可）。
3. 自己判一句：这次变更**被 PCCP 覆盖了吗**。若你认为「没覆盖、但可以另交新申报」→ 你应该判 hold，我们一致；若你认为「没覆盖即不许做」→ 你判 reject，与引擎一致。**这两种读法都有道理，这正是要测的歧义。**

## 为什么我们不直接改引擎把数字做好看

引擎 `P-CRIT-02` 判 Veto 有它的道理：适应证变了，风险面就变了，一刀切拦下来更安全。我们判 `hold/resubmit` 也有道理：§515C(b) 的字面是「不在覆盖范围内」，不是「禁止」。**改内核实是政策选择，不是 bug 修复，必须由 Steven 单独批准，我不擅动。**

在那之前，这个 0.486 就是这个台子的真实成绩，写在这里，而不是藏起来。