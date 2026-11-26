# 提交清单（照着打勾，别跳）

## A. 你自己跑公开列

- [ ] 归档 sha256 与记录页一致：`5151fe7ffa48be46ad55201bf334b536320535805363fa81c3f93a809d942b83`（0.1.3）
- [ ] `MANIFEST.json` 逐字节校验返回 `True`
- [ ] `python bench.py --submit adapter_reference.py` 得到 `public=0.9688 masked=0.9688 tag=1.0/1.0`
- [ ] `python bench.py --commit-check` 得到 `COMMIT: … PASS`
- [ ] 你的适配器跑出 `exact public` 与 `macro_recall` 两行，且你能解释两者差异
- [ ] 与空基线对照：你的 `exact` 若低于 0.875，说明适配器有问题，不是"题很难"

## B. 代码卫生（我们会抽查）

- [ ] 进程内没有对你的 `cases_public.json` 写操作（只读）
- [ ] 代码里不出现 `expected_verdict` / `expected_tag` / `hidden` 字样
- [ ] 无网络调用（离线可跑）
- [ ] 无绝对路径（换台机器能跑）
- [ ] 两次运行输出一致（随机因素已固定种子）
- [ ] 返回的 `verdict` 与 `tag` 都在允许集合内

## C. 提交（隐藏列代跑）

- [ ] 提交物：`adapter.py` 及依赖（或说明只需标准库）
- [ ] 队名 / 匿名选择（匿名则只公开 `sha256[:8]`）
- [ ] 许可声明一句话：允许公开分数 + 附「仅供参考、非监管结论」免责
- [ ] 声明你未使用任何 PCCP 官方清单以外的"答案表"反推

## D. 收到结果后

- [ ] 用我们交回的 `score_*.json` 自查公开列，`--verify` 应 VERIFIED（隐藏列摘要含隐藏题，外人环境会 REFUSE——预期）
- [ ] 若你不同意某题的标签，走「分歧登记」：给出题号 + 你的读法 + 依据原文；分歧会公开列着，不私了
