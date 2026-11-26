"""适配器骨架：把你要评的判定器接到 PCCP-Bench 上。

现在这份是保守占位（越界即 hold、判据未达即 hold），它存在的意义是让你先确认环境能跑通，
再把它换成你自己的逻辑。换成"一律 go"跑分时你会看到：
    exact public=0.875 but macro_recall=0.5
—— 这就是这张台子最难糊弄的地方：基率能给你 0.875 的精确率，但宏召回立刻露底。

填法：只改 evaluate()。其余不用动。
"""
from __future__ import annotations

TAGS = ("ok_covered", "outside_scope", "acceptance_not_met",
        "evidence_missing", "intended_use_change", "unclassifiable")


def evaluate(ctx: dict) -> dict:
    """ctx 是一条变更事实（bool 字段 + 描述 + 来源引用）。返回判定与理由。

    ctx 里你会看到（示例）：
      pccp_authorized / change_within_pccp_scope / affects_intended_use /
      change_class_described / acceptance_criteria_met / remains_se_to_predicate /
      validation_documented / labeling_version_history / udi_updated /
      change_type / evidence_sufficiency / jurisdiction / source_refs …

    规则（违反即作废）：
      - 不许读 expected_verdict / expected_tag（那是答案）
      - 不许改 ctx、不许联网去查 K 号对应的公开结论
      - 同一输入两次运行必须给出同一结果
    """
    # TODO: 换成你的逻辑。下面是最保守的占位：
    if not ctx.get("pccp_authorized", False):
        return {"verdict": "hold", "tag": "outside_scope",
                "why": "no authorized PCCP to compare against"}
    if ctx.get("affects_intended_use", False):
        return {"verdict": "hold", "tag": "intended_use_change",
                "why": "change touches intended use"}
    if not ctx.get("acceptance_criteria_met", True):
        return {"verdict": "hold", "tag": "acceptance_not_met",
                "why": "pre-specified acceptance criteria not met"}
    return {"verdict": "go", "tag": "ok_covered", "why": "within authorized scope and criteria met"}
