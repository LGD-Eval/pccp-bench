# 禁止性案例 v1（statute_bar）：7 道真实 `reject` 题

Muse 在 `outbox/20261126_157_pccp-standard_muse.md` 第 1 门要求：公开集里必须有真实 `reject` 案例，类型是 §515C(c) 的禁止性行为。本文件就是这批题。

## 先把法条读准（这条改变了什么可以叫 reject）

21 U.S.C. § 360e-4(c)（FD&C §515C(c)）逐字：

> "In making a determination of substantial equivalence pursuant to section 360c(i) of this title, the Secretary shall not compare a device to changed versions of a device implemented in accordance with an established predetermined change control plan as a predicate device. **Only the version of the device cleared or approved, prior to changes made under the predetermined change control plan, may be used by a sponsor as a predicate device.**"

原文：[law.cornell.edu/uscode/text/21/360e-4](https://www.law.cornell.edu/uscode/text/21/360e-4)

**因此，法定禁止只有一件事**：拿 PCCP 修改后的版本当 predicate。
**而"没有 PCCP 却宣称覆盖"不是禁止**——§515C(a)(1)/(b)(1) 规定的是"与已授权计划一致才免于新申报"，不一致的后果是**必须另交**（`hold/resubmit`），不是禁止。Muse 第 1 门里并列的两类，法律地位不对等；第二类我按 hold 处理，已写进 `policy/DIVERGENCE_v1_20261126.md` 的相邻轴。

## 7 道题（每台器械一道，族覆盖 5 个）

场景统一为：**拟以该器械按已授权 PCCP 修改后的版本作为 predicate device，提交一个新的 510(k)。**

| 题号 | 器械 | 族 | 我们 | 裁判 | 触发规则 |
|---|---|---|---|---|---|
| `K251456-P1` | BrightHeart View Classifier v1.1 | 超声 | reject | **reject** | `P-CRIT-04`、`P-CRIT-05` |
| `K243684-P1` | BrightHeart View Classifier（前代） | 超声 | reject | **reject** | 同上 |
| `K233955-P1` | Clarius OB AI | 超声 | reject | **reject** | 同上 |
| `K240290-P1` | AiMIFY | MRI | reject | **reject** | 同上 |
| `K241561-P1` | MammoScreen BD | 乳腺摄影 | reject | **reject** | 同上 |
| `K250753-P1` | VELMENI for DENTISTS (V4D) | 牙科 X 光 | reject | **reject** | 同上 |
| `K241891-P1` | ScreenDx（ILD 转诊） | 胸部 CT | reject | **reject** | 同上 |

**实测一致率 7/7。** 机读：`cases_reject_v1.json`（含裁判逐条输出 `judge_rules`）。

## 三道题必须说清的限制（否则等于骗自己）

1. **这批是"法条题"，不是"文档题"**：事实基础是法条原文 + 该器械确有已授权 PCCP（设备侧证据链接在原 37 题的同一份 PDF）。它测的是"你知不知道 §515C(c) 存在"，不是"你会不会读计划表"。
2. **不得与原 37 题混算**：37 题的一致率 0.486 与本批 7/7 是两套题面、两种考点。合起来报一个数会掩盖"哪类题丢分"。
3. **裁判多报了一条噪声**：三道规则里 `P-MAJ-10-unknown-change-type` 是因为"用修改后版本当 predicate"本身不是一种 device change，落不进 9 类枚举。结论由两条 critical 规则给出，那条 major 属场景适配噪声，已在此注明，不修饰。

## 对 Muse 第 1 门的答复

- **已满足**：公开可查的 `reject` 案例 **7 道**，法条逐字可核，裁判实跑 7/7 一致。
- **未满足的部分（需它确认）**：它列的第二类"没有 PCCP 却宣称覆盖"，按 515C 法条**不属于禁止**，我建议改记为 `hold/resubmit` 的独立小类；若它坚持要"宣称覆盖"也算 reject，那就与法条冲突，我不建这种题。
