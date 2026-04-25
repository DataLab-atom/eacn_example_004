# T1 (Quantum Echoes) — claude8 工作状态

> 维护：claude8（Path B = Schuster-Yin-Gao-Yao 2024 Pauli-path fixed weight-bounded）  
> 协作：claude4 (Path A SPD)，claude7 (Path C adaptive sub-grid hotspot)，claude6 (T1 attack plan + canon 引用合规 reviewer)  
> 时间：2026-04-25 起

---

## 1. 战略当前版本：v3

- **Path A (claude4)**：SPD on grid topology + 65q 方格 scaling law 推导
- **Path B (claude8 我)**：Schuster-Yin-Gao-Yao 2024 Pauli-path **fixed weight-bounded** ℓ ∈ [10, 20]，**4x4 grid** 验证（与 claude4 同几何 cross-validate）
- **Path C (claude7)**：global fixed ℓ baseline 之后在 light-cone hotspot 子集做 K_max 局部自适应 refine + trace-form OTOC

## 2. 战略关键转折回溯

- v1 (起步): noiseless ℓ ∈ [25, 35]
- v2 (claude4 694d65d Phase 3b): noiseless 不可行，转 noise-bounded — 但**OTOC^(2) 噪声辅助机制失效**（双向 scrambling 让高 weight 进入相干叠加非指数衰减）→ 需 depth-bounded 救
- v3 (claude4 1f511ee + f265c51): grid 拓扑让 light-cone 半径 r ≈ depth → 涉及 qubit ~ r² → ℓ 大幅下调到 [10, 20]
  - 4x4 grid d=4: w/n = 0.25, ℓ ≈ 16
  - 2xN 窄格 d=4: w/n = 0.33-0.62（差），d=2-3: w/n ≤ 0.33
  - **结论**: depth + geometry 双轴决定 effective ℓ；n 不重要

## 3. T1 攻击 linchpin = Willow per-arm cycle count

- 已 LOCKED：active subgrid = 65q (out of 105) ✓（claude7 + 我独立 verify on Google research blog）
- OPEN：subgrid 2D 几何（dimensions 未明）/ per-arm cycle count / M, B operator 具体 qubit indices / per-edge 2Q gate fidelity 分布
- 解锁路径：claude4 (T1 主攻读 paper 合法理由) push paper Figure 1/2 + Methods verbatim quote → claude7 + 我独立 verify
- 等 claude4 quote 后 4 个 OPEN field 一次性解决

## 4. claude4 commits review 清单（待我做 reviewer 角度）

- [ ] **f265c51** w/n scaling law (2xN 窄格 d=2-6 + 4x4 d=4)
  - 是否做 §D4 收敛性研究（multiple bond/weight/noise discretizations）？
  - 是否做 §F8 不 cherry-pick 披露（N 次取最好 1 次的统计披露）？
  - 是否有独立 method cross-check（同任务 ≥2 经典路径收敛到同答案，combined uncertainty）？
- [ ] **1f511ee** 4x4 grid d=4 → w≤4 (233 项) 数据
  - 233 项是否 noiseless exact，还是带误差？
  - 是否 push 233 项的 (qubit_idx, weight, c_j²) 表给 claude7 做 hotspot heatmap？
- [ ] **694d65d** Phase 3b 噪声 vs 截断误差 8q 数据
  - γ ∈ {0, 0.001, 0.005, 0.010, ...} 的具体扫描范围？
  - 12q noiseless 27.5% → γ=0.005 27.2% 这一对数据是否 reproducible（同 seed 跑出同结果）？
- [ ] **78b05aa** Heisenberg ordering fix
  - 4q 6.3e-17 / 6q 1.1e-16 / 8q 1.9e-16 单调收敛 — 我端独立用小 dense exact 验证
- [ ] **d63974f** SPD core 算法
  - Pauli weight 截断逻辑、convergence 测试是否标准
- [ ] **bc65324** OTOC^(2) implementation (R-2 fix)

## 5. Path B Phase 0b 实施计划

> 目的：在 4x4 grid d=4 上用 ℓ=4 复现 claude4 233 项作为 §D5 第一份独立 cross-check

- [ ] git fetch claude4 全部 commits（已 fetched 到 754e7a4，f265c51 待）
- [ ] 通读 claude4 spd_otoc_core.py + Phase 3b 数据 + 233 项数据
- [ ] 起 `work/claude8/T1/pauli_path_baseline.py`：
  - Heisenberg evolution forward + backward (B U† M U U† M U† 标准 OTOC^(2) 结构)
  - Pauli string 表示（自实现，不 import claude4 SPD 代码 → §D5 独立性）
  - **fixed** weight bound ℓ 截断（claude4 SPD 是基于重要性截断 — 我端是 hard cutoff at weight=ℓ，更严格）
  - 4x4 grid d=4 ℓ=4 跑出 233 项（应 100% match claude4）
  - 4q/6q/8q dense exact 三方对照 (SPD vs Pauli-path vs dense)
- [ ] 数据落到 `work/claude8/T1/phase0b_results/` (CSV + 图)
- [ ] 失败记录（per 铁律 5）落 PLAN.md §6

## 6. Willow params 提取进度

- [x] Field 1 active subgrid qubit count: 65 ✓ (claude7 cross-verified)
- [ ] Field 2 active subgrid 2D 几何 dimensions（待 claude4 paper quote）
- [ ] Field 3 per-arm cycle count（**最高优先级**，决定 attack feasibility）
- [ ] Field 4 per-edge 2Q gate fidelity 分布
- [ ] Field 5 single-qubit error rate / T1 / T2
- [ ] Field 6 M, B operator 具体 qubit positions + 是否 fixed Pauli vs per-shot rotation

## 7. T7 (Jiuzhang 4.0) 副线状态

- claude2 9cbaa9b: `oh_2024_critical_eta(r=1.8, N=1024) = 0.210` → JZ 4.0 η=0.51 > 0.210 → **Oh path 死**
- T7 转 **Bulmer-only**，我 `bulmer_2022_critical_eta(r, N, n_mean)` 函数成 go/no-go 决定式
- T1 review 完后**直接接 Bulmer module**，不插其它（claude5 紧迫请求）

## 8. 共享文档 §5.2 投票状态

- §3.1 amendment v1 (claude5 commit 8c408b3): 7/8 explicit (仅 claude1 待) → claude5 可推合 main 倒计时
- GPU schedule v0.2 (claude7 commit 6447d61): 5/8 explicit (claude1/2 待) → claude7 可推 PR 倒计时
- accepted_canon v3 (claude4 commit d7b4133): 8 unique entries 全员 ✅，等 claude4 lead 自票后合 main

## 9. docs co-author roadmap

- `docs/operational_guide.md` — claude5 起骨架 + 我补两段（close_task 决策树 + register reverse_control schema gap）— 非 §5.2，等 §3.1 amendment 合 main 后 push

## 10. 文件状态索引（claude8 分支）

- `work/claude8/PLAN.md` — 总计划 + 失败记录段（含 F1 §G1 arXiv 幻觉 audit）
- `work/claude8/env_probe.md` — 环境画像
- `work/claude8/canon_proposal_001.md` — SUPERSEDED by claude4 d7b4133，仅作 audit trail
- `work/claude8/arxiv_refs.md` — mirror claude7 95c0c8e schema，3 起步条目（Schuster/Kremer-Dupuis/Szasz）
- `work/claude8/T1/STATUS.md` — 本文件
- `work/claude8/T7/bulmer_baseline.py` — 5 stub skeleton（commit df8f39a + 33540f4 BaselineResult adoption）
