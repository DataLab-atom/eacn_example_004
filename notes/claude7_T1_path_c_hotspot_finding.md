## T1 Path C — hotspot analysis 实证发现 (4x4 d=4, M=q0/Z, B=q15/X)

> Source data: claude4 commit 0775fa7 `results/16q_4x4_d4_pauli_terms.json` (233 项 Pauli terms)
> Analysis: claude7 commit (即将 push) `code/T1_hotspot_analysis.py`
> Output: `results/T1/path_c_hotspot_analysis_N16.json`

---

## 关键数字

**4x4 grid 上 16 sites 的 occupancy**（按 coeff² 加权）：

| Rank | Site | Occupancy | % of total |
|---|---|---|---|
| 1 | q0 (M) | 1.0000 | 100.0% |
| 2 | q7 | 0.9984 | 99.8% |
| 3 | q11 | 0.7660 | 76.6% |
| 4 | q14 | 0.7477 | 74.8% |
| 5 | q15 (B) | 0.3279 | 32.8% |
| 6-16 | q1-q6, q8-q10, q12, q13 | **0.0000** | **0.0%** |

```
4x4 grid view (% of total occupancy)
  q 0 M: 100.0% |  q 1: 0.0% |  q 2: 0.0% |  q 3: 0.0%
  q 4  :   0.0% |  q 5: 0.0% |  q 6: 0.0% |  q 7: 99.8%
  q 8  :   0.0% |  q 9: 0.0% |  q10: 0.0% |  q11: 76.6%
  q12  :   0.0% |  q13: 0.0% |  q14: 74.8% |  q15B: 32.8%
```

**Light-cone path q0 → q7 → q11 → q14 → q15** carries 100% of Pauli weight.
- Top-4 sites (q0, q7, q11, q14): 91.5% of occupancy
- Top-8 sites: 100% (any K_max ≥ 8 captures full distribution)
- 5 of 16 sites cover all 233 terms.

---

## Path C 含义

**实证支撑 hot-cluster framework**:
1. **adaptive refine 实际 sub-grid 大小 ≈ 5 sites (4x4 d=4)**，不是 16
2. **constant-factor speedup**: 16 / 5 = 3.2× 至少（exact ratio 取决于具体 Pauli weight 分配）
3. **Cold sites (零 occupancy) 完全可丢**: 任何 K_max budget 在它们上是浪费
4. **Hot path 几何**: q0 → q7 → q11 → q14 → q15 — 沿 4x4 对角，**不是** Manhattan 直线 q0→q1→q2→...→q15。OTOC 信息沿对角传播是 brick-wall 2Q gate pattern 的特征。

**Willow 65q (~10x10) 投射**:
- 如果同样比例: ~5/16 × 65 ≈ 20 hot sites
- Path C effective sub-grid: ~20q (vs Willow 全 65q)
- **重要 caveat**: 4 → 10 grid linear extrapolation 未必成立。需要 claude4 在 6x6 / 8x8 grid 重复 export Pauli term 表 verify。

---

## 与 claude4 866eccc decision matrix 接合

claude4 decision matrix 4 cell:
| Per-arm depth | M-B distance | Verdict | Required method |
|---|---|---|---|
| ≤12 cycles | nearby (≤4 edges) | ✅ Feasible | SPD w≤15 |
| ≤16 cycles | nearby | ✅ Likely feasible | SPD w≤20 |
| **≤16 cycles** | **distant (>6 edges)** | **⚠️ Uncertain** | **Adaptive SPD** |
| ≥24 cycles | any | ❌ Likely infeasible | New method needed |

本次数据点 (4x4 d=4, M=q0, B=q15) 是 **distant cell** (M-B Manhattan distance = 6 edges = 4x4 对角全长)。
- claude4 fixed-bound w≤4 给 233 terms 在 noiseless 0% err
- 我 Path C hotspot analysis: 5 sites carry all weight → 实际 active 维度 5/16 = 0.31
- **adaptive top-K refine focused on q0/7/11/14/15 cluster** 应能在 noisy γ=0.005 regime + larger depth 5-6 (where w/n→0.8) 持续奏效

---

## 后续 Path C deliverable 计划

- [ ] **claude4 export 6x6 grid d=4-6 Pauli term 表** — request via direct_message
- [ ] 同样 occupancy 分析: 验证 hot/cold 比例随 grid 大小是否成立
- [ ] **8q-12q 上对比 fixed-bound w≤4 vs hotspot-aware adaptive K_max**
  - fixed: 全 16 sites 上 K_max=8000 (假设)
  - adaptive: hot 5 sites K_max=8000 + cold 11 sites K_max=100 → 总 budget 减 65%, accuracy 应不变
- [ ] 实现 `code/spd_adaptive_hotspot.py`: 接 claude4 SPD core (commit d63974f) 加 hotspot detection layer
- [ ] noisy OTOC^(2) γ=0.005 测试: 验证 hot/cold 划分在噪声下稳定

---

## §H1 / §D5 合规

- 数据 source: claude4 commit 0775fa7 verbatim (file copy via git checkout)
- 分析方法 deterministic (Σ coeff² over sites): 任何 reviewer 可独立复现
- 不修改 claude4 baseline，仅在 claude7 分支生成派生 analysis
- Path C 与 claude4 Path A (fixed-bound)、claude8 Path B (Schuster Pauli-path) 差异化保持: hot-cluster adaptive refine 是 Path C 独有

— claude7 (T1 Path C, RCS reviewer)
*版本：v0.1，2026-04-25*
