---
title: Failure ledger (pre-release, not citable)
version: 2026-11-26
status: PRE-RELEASE — 未过门仍发布，门状态原样列出
---

# Failure ledger — PCCP-Bench

**这不是成功案例集，是我们自己翻车的记录。** 公开它只为一件用处：让读者能自己核验"错→修→可复核"这条链。

## 发布状态（不藏）

| 门 | 状态 |
|---|---|
| S4 外人实测 | **WAIVED** —— 0 名外人通读签字 |
| S6 外部 AI 复核 | **FAIL** —— 两轮实跑（DeepSeek-V3）均判"不可公开" |
| κ（第二标注人） | **未报出** —— 现有 κ 均为"我方 vs 引擎"，引擎不是人类标注者 |

因此：**本文件为预发布，不得作为引用来源，不得用于评价我们已达成某项一致性。** 我们选择先公开、再补签字，理由写在第 11 节，不做美化。

## 收录范围

- 收录：9 条，每条带可点开的修复物（提交或归档版本）。
- 暂缓：4 条（`F-009, F-010, F-011, F-012`），原因见第 10 节。**没有为了凑齐而硬写。**

## F-001 · 2026-11-26 · 死链 · 已修

**资产**：PCCP-Bench 候选池 37 题

**现象**：37 条 FDA PDF 外链全部 404，读者点任何一个都打不开

**根因**：链接规则错位一位：写成 cdrh_docs/pdf51/<K>.pdf，正解是 pdf + K 号前两位（pdf25）

**处置**：7 台器械逐一确认目录（K251456→pdf25、K243684→pdf24、K233955→pdf23、K240290→pdf24、K241561→pdf24、K250753→pdf25、K241891→pdf24），37 条全改，CI 加断言强制 /pdf<K前两位>/<K>.pdf

**修复物**：https://github.com/LGD-Eval/pccp-bench/commit/1e1df35 ｜ https://github.com/LGD-Eval/pccp-bench/commit/c046109 ｜ https://github.com/LGD-Eval/pccp-bench/commit/0bfc74a　—　37 条链接全改 + CI 断言防回归

**教训**：绿灯必须建在“读者点的那个链接”上，不能建在“我这边能读到正文”上

## F-002 · 2026-11-25 · 打包 · 已修

**资产**：PCCP-Bench 0.1.0 归档

**现象**：外人解包后跑不起来：适配器里硬编码作者本机路径

**根因**：开发机路径进入交付物，未做路径归一

**处置**：0.1.1 起适配器以相对路径解析 bundle；0.1.2 补 evidence/；0.1.3 修数据卡措辞。旧版字节一律不动

**修复物**：https://doi.org/10.5281/zenodo.24550266　—　归档侧修复（0.1.1 起相对路径），不在本仓库历史

**教训**：“我这儿能跑”不是“别人能跑”；交付物里出现绝对路径即视为缺陷

## F-003 · 2026-11-25 · 打包 · 已修

**资产**：PCCP-Bench judges 依赖

**现象**：解包后 import 失败，裁判模块依赖未随包发布

**根因**：把运行环境当成交付物的一部分

**处置**：0.1.1 vendored 依赖进包，零外部安装即可跑

**修复物**：https://doi.org/10.5281/zenodo.24550266　—　归档侧 vendored 依赖（0.1.1），不在本仓库历史

**教训**：可复跑的最低条件是“无网、无 pip、无本机依赖”

## F-004 · 2026-11-25 · 主张 · 已修

**资产**：PCCP-Bench 分数

**现象**：报了 0.9688，但拿不出对应的原始输出日志

**根因**：分数与执行证据分离存放

**处置**：0.1.2 起 evidence/ 随包发布原始日志；每个分数必须可追到 sha

**修复物**：https://doi.org/10.5281/zenodo.24550266　—　归档侧 evidence/ 随包（0.1.2），不在本仓库历史

**教训**：没有原始输出的分数＝不可核主张，等于没报

## F-005 · 2026-11-26 · 工具 · 已修

**资产**：annotation/kappa.py

**现象**：四类标签（含 hold_insufficient / hold_resubmit）进 κ 后一致率与 κ 同时失真；且 v1.1 改写版存在语法错误，文件从未成功运行过

**根因**：脚本硬编码 LABELS=('go','hold','reject')，沿用三类时代的假设；v1.1 改写时 dict( 未闭合，且没有任何自测拦住它

**处置**：v1.2 落地：四类 + 别名归一（含中文『另交』『材料不足』）+ 二分类主指标 + 9 项自测（含空交集报错、单一类别 κ 记 null、未知标签必列）+ CI 增设 kappa selftest 步骤，已推送并转绿

**修复物**：https://github.com/LGD-Eval/pccp-bench/commit/1729cb5 ｜ https://github.com/LGD-Eval/pccp-bench/commit/d3f57b7 ｜ https://github.com/LGD-Eval/pccp-bench/commit/fc3f7dc　—　四类 κ 落地 + 结果说明 + CI 自测转绿

**教训**：『未测试』往往等于『是坏的』；改写脚本必须自带自测，且自测要进 CI 才算数

## F-013 · 2026-11-26 · 工具 · 已修

**资产**：CI verify-archive 工作流

**现象**：新增 kappa 自测步骤后 CI 变红（38192d3），后续全部步骤被 skipped

**根因**：步骤插到了 steps: 之后、checkout/setup-python 之前，既无仓库文件也无 python 环境

**处置**：把该步骤移到 setup-python 之后（Download archive 之前），重跑转绿（fc3f7dc）

**修复物**：https://github.com/LGD-Eval/pccp-bench/commit/fc3f7dc　—　步骤移回 setup-python 之后，CI 转绿

**教训**：工作流步骤的失败是『位置错误』而不是『断言失败』时，读步骤序列比读报错更快

## F-006 · 2026-11-26 · 通道 · 已修

**资产**：CI verify-archive

**现象**：两次变红（b8d6915、5aabbb8），原因是 Zenodo 上游 503/反爬

**根因**：工作流只有一条 curl，单点依赖上游

**处置**：Zenodo 为主（6 次重试 + 递增退避 + 每次校 sha256），不可达退到仓库内字节相同镜像，标 SOURCE=mirror 并 warning，不宣称 Zenodo 在线

**修复物**：https://github.com/LGD-Eval/pccp-bench/commit/189aaf7 ｜ https://github.com/LGD-Eval/pccp-bench/commit/c230b16　—　仓库内字节相同镜像 + CI 重试退避与降级标注

**教训**：对外可用性不能依赖单一第三方；降级路径必须同字节

## F-007 · 2026-11-26 · 主张 · 已修

**资产**：公开集类别覆盖

**现象**：reject=0 却对外呈现“四类体系”，等于暗示类别完整

**根因**：标签体系升级后未回头补禁止性案例

**处置**：依 21 U.S.C. §360e-4(c) 补 7 道 statute_bar 题，裁判 7/7 一致；并明确不得与 37 题合并报一致率

**修复物**：https://github.com/LGD-Eval/pccp-bench/commit/bb18044 ｜ https://github.com/LGD-Eval/pccp-bench/commit/a36df4b ｜ https://github.com/LGD-Eval/pccp-bench/commit/33eb18f　—　7 道 statute_bar reject 题 + 题册 + README 另册说明

**教训**：体系的完整性必须由案例支撑，不能由枚举支撑

## F-008 · 2026-11-26 · 措辞 · 已修

**资产**：对外分数措辞

**现象**：0.9688 裸报，读者会外推到全部题面

**根因**：分数限域写在报告里，没写进每个对外文件

**处置**：10 个对外文件加限域：仅“0.1.3 自身 32 道公开题、我方参考实现”；任何精确率主张附空基线 0.351

**修复物**：https://github.com/LGD-Eval/pccp-bench/commit/e1e2b7f ｜ https://github.com/LGD-Eval/pccp-bench/commit/1dc87d4 ｜ https://github.com/LGD-Eval/pccp-bench/commit/54f0c8c ｜ https://github.com/LGD-Eval/pccp-bench/commit/ae232b1　—　四处对外文件加分数限域

**教训**：限域必须贴在数字旁边，不能放在报告第 8 节

## 10. 暂缓公开的 4 条，以及各自的原因

不公开不是因为有秘密，而是因为无可点开的修复物，放出来只会削弱可核验性。

- **F-009**（协作）：协作通道问题，修复物是重发消息，不在公开仓库

- **F-010**（工具）：冻结脚本属站位工具链，未随本仓库发布

- **F-011**（通道）：通道受限，无可公开修复物

- **F-012**（通道）：通道受限，无可公开修复物

## 11. 为什么在没过门的时候先公开

两个理由，都写出来，便于反驳：

1. S6 的否决理由在第二轮已经从『泄露』变成『你们把没修的东西也写出来了』——那是立场意见，不是安全结论；
2. S4 需要的是一名外人，而不是更多内部文档。把材料摆出来比继续包装更有用。

**但这也意味着我们接受一条代价：在有人签字之前，这份文件随时可能被判为不合格。**

## 12. 维护口径

- 只追加，不覆盖历史条目；已修只改状态，不改描述强度。
- **不承诺回复外部提问**：无专职工位，承诺了就是欠债。
- 任何条目若被外部指出『不应公开』，立即下架，并把下架本身记为新条目。
