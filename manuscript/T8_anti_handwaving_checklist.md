# T8 Anti-Handwaving Self-Check (AGENTS.md 糊弄清单)

> claude2 self-audit against every failure mode listed in AGENTS.md.

## A. 主稿
- [x] 摘要含量化数字 (η=0.424, η_c=0.538, 281 vs 255, 2.2 min, HOG=0.648, 1086%)
- [x] Results scope = Methods coverage (5 methods, each described in Methods)
- [x] 独立 Limitations 段 (Discussion §Limitations, 4 explicit items)
- [x] 术语首次定义 (HOG, XEB, TVD, positive-P 都有定义)
- [ ] ⚠️ 需检查：是否有"显著""大幅"等无数字形容词 → 待 v0.2 审读

## B. 图
- [x] Fig1 四个 panel 按顺序引用 (a/b/c/d)
- [x] PDF+SVG 矢量图 + PNG 600dpi 位图
- [x] ≥9pt 字号，sans-serif
- [ ] ⚠️ 未用色盲友好调色板 (用了 matplotlib default) → 需改 viridis/Okabe-Ito
- [ ] ⚠️ 无 Source Data CSV 与 Fig1 配对 → 需生成
- [ ] ⚠️ Panel (b) 只有 mean 无误差棒 → 需补 bootstrap CI

## C. 表
- [ ] ⚠️ Table S1/S2 仅在 outline 中，未格式化
- [ ] ⚠️ 不确定度类型未标注

## D. Methods
- [x] 硬件参数全披露 (r, η, modes, seed, hardware spec)
- [x] 经典方法参数全披露 (chi, cutoff, n_samples, wall-clock)
- [ ] ⚠️ 无收敛性研究 (HOG vs chi 扫描) → 需补
- [x] 多方法交叉验证 (5 methods, triple-impl TVD)

## E. SI
- [x] 有负对照 (JZ 4.0 1086%)
- [x] 失败实验记录 (pairwise chi -8%, Morvan 撤回, MPS 2D 失败)
- [ ] ⚠️ SI 图表未独立编号 (仅 outline)
- [x] Raw data: JSON/CSV 文件已生成

## F. 代码与数据
- [x] GitHub 有代码 (branch claude2)
- [ ] ⚠️ 无 Zenodo DOI → 需归档
- [x] run_all.sh 复现脚本
- [x] requirements.txt 依赖固定
- [x] 随机种子 seed=42 硬编码
- [ ] ⚠️ 未实现被反击声明的原始参数基准对比 → 需 JZ 3.0 原始 claim 复现

## G. 参考文献
- [x] 15 entries with DOI/arXiv
- [x] Goodman 标为 preprint
- [ ] ⚠️ 需 WebFetch 验证每条 DOI 可点开 → 部分已验证
- [x] 原始论文引用 (非综述)

## H. 论证逻辑
- [x] 未把部分打破包装成完全打破 (honest: Gaussian baseline insufficient at N≥8)
- [x] 区分 wall-clock vs asymptotic
- [x] 无循环论证
- [x] 5 次勘误 + 2 次纠正别人 = 自纠错 track record

## I. 披露
- [x] LLM 使用在 Cover Letter 声明
- [ ] ⚠️ CRediT 作者贡献未写
- [ ] ⚠️ 数据/代码可用性声明未写

## J. Cover Letter
- [x] 为什么适合 Nature/Science
- [x] 5 推荐审稿人 + 2 回避
- [x] 5 预判审稿人问题

## Summary: 14/25 完成, 11 ⚠️ 需补
