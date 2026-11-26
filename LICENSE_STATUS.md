# LICENSE_STATUS — 逐目录授权对照

与已发布的 Zenodo 记录（DOI 10.5281/zenodo.24550267，其 notes 写明"代码另注 Apache-2.0、数据集文本 CC BY 4.0、逐文件见 LICENSE_STATUS.md"）一致：

- **数据集文本 / 标注 / 证据日志**：CC BY 4.0
- **代码（评测器、参考适配器、裁判、工具）**：Apache-2.0

> 归档包内自带的 `LICENSE_STATUS.md` 是对**归档字节**的权威说明；本表是对**仓库目录**的对照。两者若在细节上不一致，以归档包内那份为准（归档已冻结，根 `2d305387…c6de9d`）。

| 目录 / 文件 | 内容 | 许可 |
|---|---|---|
| `bench.py`、`adapter_reference.py`、`make_evidence.py` | 评测器、参考适配器、证据生成 | Apache-2.0 |
| `judges/` | 裁判实现 | Apache-2.0 |
| `tools/`、`external_run_kit/` | 工具与外部实跑套件 | Apache-2.0 |
| `policy/` | 判定策略（代码部分）| Apache-2.0 |
| `candidate_pool/`、`review/`、`annotation/` | 候选、评审、标注数据与协议文本 | CC BY 4.0 |
| `mirror/` | 镜像留痕 | CC BY 4.0 |
| `evidence/`（若存在或由 `make_evidence.py` 生成）| 运行日志与证据包 | CC BY 4.0 |
| `README.md`、`LANDSCAPE_20261126.md` | 文档 | CC BY 4.0 |
| `LICENSE` | Apache-2.0 全文（代码许可） | — |

## 变更说明

- 2026-11-26：仓库此前**没有任何 LICENSE 文件**，README 却写"逐目录见包内 `LICENSE_STATUS.md`"。本表即补上那个被承诺的文件。
- 曾短暂改为单一 MIT，后发现与已发布 DOI 记录、归档包内许可说明冲突，已改回"代码 Apache-2.0 + 数据 CC BY 4.0"，与归档一致。
- `.zenodo.json`、`CITATION.cff` 同步为 CC BY 4.0（数据集主许可）。

## 注意

- 第三方材料随仓库分发时，其原始许可优先；发现冲突请开 Issue。
- 本仓库是评测资产，不提供任何担保，也不构成监管判定。