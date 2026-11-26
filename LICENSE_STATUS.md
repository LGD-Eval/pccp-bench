# LICENSE_STATUS — 逐目录授权对照

单一许可：**MIT**（根目录 `LICENSE`，Copyright (c) 2026 LGD-Eval）。

| 目录 / 文件 | 内容 | 许可 |
|---|---|---|
| `bench.py`、`adapter_reference.py`、`make_evidence.py` | 评测器、参考适配器、证据生成 | MIT |
| `judges/` | 裁判实现 | MIT |
| `tools/`、`external_run_kit/` | 工具与外部实跑套件 | MIT |
| `policy/` | 判定策略与文档 | MIT |
| `candidate_pool/`、`review/` | 候选与评审材料 | MIT |
| `annotation/` | 标注协议、样本、κ 工具 | MIT |
| `mirror/` | 镜像留痕 | MIT |
| `evidence/`（若存在，或由 `make_evidence.py` 生成） | 运行日志与证据包 | MIT |
| `README.md`、`LANDSCAPE_20261126.md`、`CITATION.cff`、`.zenodo.json` | 文档与元数据 | MIT |

## 变更说明

- 2026-11-26：此前 README 写"数据 CC BY 4.0 / 代码 Apache-2.0"，但仓库内既无 LICENSE 也无 README 所指的 `LICENSE_STATUS.md`（该表只在下载包内）。现统一为 MIT，并补上本表，消除"承诺了不存在的文件"。
- 引用与归档（Zenodo / CITATION.cff）同步为 MIT。

## 注意

- 第三方材料若随仓库分发，其原始许可优先于本表；发现冲突请开 Issue。
- MIT 不提供任何担保；本仓库是评测资产，不是监管产品。