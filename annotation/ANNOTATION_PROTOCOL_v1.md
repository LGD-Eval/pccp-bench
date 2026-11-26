# Annotation protocol v1 — PCCP-Bench (for a second, independent annotator)

中文摘要：这份是给"第二标注人"看的协议。目标只有一个——把我们自己那套 `go / hold / reject` 的判断，
在**不看你我答案**的条件下重做一遍，然后用 Cohen's κ 算一致度。κ 低于 0.4 就改协议、不改题；达到 0.6 才够论文级。

---

## 1. What you get, and what you do not get

You get, per case:

- `device` — device name, 510(k)/PMA number, decision date, product code
- `change` — the proposed change, in the wording used in the decision document
- `sources` — the exact passages the case rests on, with the document id and page/section
- `question` — restated as a yes/no-shaped question, no answer

You do **not** get: our verdict, our reasoning, our `expected_verdict`, our `expected_tag`, any file from `evidence/`.
If you are handed any of those by accident, say so before you start — a contaminated second annotation is worse than none.

## 2. The three labels, defined by what the plan says (not by what feels right)

| Label | Condition (all must hold) | Typical failure mode |
|---|---|---|
| `go` | The change is covered by an affirmative statement in the device's PCCP **and** every acceptance criterion the plan states for that class of change is met by the description given | Calling it `go` because "it's a small change" — size is not the test; plan text is |
| `hold` | The change *may* be covered, but a stated precondition, validation activity, or acceptance criterion is not evidenced in the material | Calling it `hold` when the plan simply doesn't mention this change class — that is `reject` |
| `reject` | The change is outside the plan's stated scope, or would alter the device's intended use / patient population / core algorithm in a way the plan does not authorise | Calling it `reject` because you personally think it should need a new submission — the plan governs, not your policy view |

Decision order — apply strictly, stop at first hit:

1. Is the change described in the plan's scope section at all? **No → `reject`.**
2. Does the plan name an acceptance criterion (metric, threshold, validation) for this class of change? **No → `reject`.**
3. Is that criterion met by the material given? **No → `hold`.**
4. Does the plan require a specific validation activity (e.g. re-testing on a held-out set) that is claimed but not evidenced? **→ `hold`.**
5. Otherwise **→ `go`.**

## 3. Blind procedure

1. Work case by case, in the order given. Do not look ahead to later cases in the same device family.
2. Write one paragraph per case: which sentence in `sources` decided it, and which rule (1–5) you stopped at.
   A label without a cited sentence is not a label — we will send it back.
3. Do not discuss cases with us until your file is submitted. Questions about the *protocol* are fine at any time.
4. Do not edit the case text. If the case looks broken (missing source, contradictory text), mark it `defect` and say why — a
   defect is a finding, not a failure on your side.
5. Time budget: ~3–4 minutes per case, 42 cases ≈ 2.5 hours. Do it in two sittings if you like; just don't re-read our
   published card between sittings.

## 4. Output format

```json
[
  {"id": "K260973-H1", "verdict": "hold", "rule": 4,
   "cite": "PCCP §3.2: '...'", "note": "validation activity claimed, no dataset described"},
  ...
]
```

Then we run:

```bash
python annotation/kappa.py --ours ours.json --theirs yours.json --json-out kappa.json
```

Output includes `kappa`, `observed_agreement`, `expected_agreement`, per-label agreement, the full disagreement list, and
both distributions. **Nothing is smoothed**: every disagreement appears by case id in the report we publish.

## 5. Thresholds, decided before we see your file

| κ | What we may then say |
|---|---|
| ≥ 0.60 | "substantial agreement between two independent annotators" — enough to report in a paper |
| 0.40–0.59 | "moderate agreement"; must be reported as a limitation, not as validation |
| < 0.40 | **We do not publish a paper.** We rewrite the protocol (§2), not the cases |

This ordering matters: if κ comes back low because our definitions are ambiguous, the fix is the definition. Adjusting
cases until κ looks good would be exactly the thing this protocol exists to prevent.

## 6. Disagreement handling (no private settlement)

For each disagreement we publish: case id, our label, your label, the sentence each of us cited. If the disagreement is
about the *plan's text*, it stays open until a third reader breaks the tie — and if no third reader is available, it stays
open and is reported as an open disagreement. We do not "resolve" disagreements by majority of two.

## 7. What this does and does not fix

Fixes: the "single-annotator, no κ" gap — the second of the three known limits in our data card.
Does not fix: sample size (still 42), class skew (28 go / 4 hold / 0 reject), or the circularity of our own reference score.
Those need different work (cases, and a third-party implementation), not more annotators.

## 8. Credit and what you may say

You are named as second annotator in the data card and in any paper that uses this κ, or you may stay anonymous —
your choice, stated before you start. You may publish your own labels and your own reading of any case; we will link to it.
You may not be quoted as endorsing the benchmark's *quality* — agreement is not endorsement.
