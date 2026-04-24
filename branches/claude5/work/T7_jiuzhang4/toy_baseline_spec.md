# T7 Toy GBS Baseline 实验参数 Spec v0.1

> **作者**：claude5（2026-04-25）
> **目的**：为 T7 (Jiuzhang 4.0, arXiv:2508.09092) 经典反击的 Phase 0 验证定义统一参数 grid，便于 claude5 的 Oh-2024 lossy MPS sampler 与 claude8 的 Bulmer-2022 phase-space sampler **独立 run、参数对齐、结果可比**。
> **D5 多方法交叉验证标准**：相同 (modes, loss, ⟨n⟩, seed) 配置，两套独立实现，输出在 TVD / cross-entropy / second-order cumulant 三个指标上偏差应落入 (combined statistical + systematic) uncertainty。
> **状态**：DRAFT v0.1，等 claude8 回 ✅/🔄 后冻结到 v1。

---

## 1. 参数 Grid

**模式数 M**：
- 10, 15, 20（三档）

**总传输 η（per-mode loss = 1−η）**：
- 0.30 (高损耗，远低于 JZ 3.0 实测 0.43；用作"经典极易"对照)
- 0.50 (中等)
- 0.70 (低损耗，远高于 JZ 3.0；用作"经典最难"对照)

**Per-mode 平均输入 photon number ⟨n⟩**：
- 5（squeezing r ≈ asinh(√5) ≈ 1.62 nepers ≈ 14.1 dB；与 JZ 3.0 上界 r=1.6 同档）
- 10（squeezing r ≈ asinh(√10) ≈ 1.85 nepers ≈ 16.1 dB；推到 JZ 3.0 之外的高 squeezing 区域）

**总配置数**：3 × 3 × 2 = **18 configurations**

> **说明**：选 ⟨n⟩=5 的理由是它对齐 JZ 3.0 高位（r=1.6 → ⟨n⟩=sinh²(1.6)≈5.94），便于 claude2 T8 复用我们的 toy 结果。⟨n⟩=10 是给 JZ 4.0 (3050 photons / 1024 squeezed states ≈ 2.98 photons/source 平均，但 claim 局部更高密度) 留 headroom。

---

## 2. 输入态约定

- **输入**：M 个独立 single-mode squeezed vacuum (SMSV)，每个 squeezing 参数 r_i = arsinh(√⟨n⟩) (uniform 全 mode 一致)
- **干涉**：Haar-random unitary U ∈ U(M)，固定 seed（见 §4），不与 JZ 3.0 / 4.0 真实 U 直接对应（toy 阶段不需要硬件对齐）
- **Loss model**：均匀 per-mode beam splitter loss，loss probability p = 1 − η
- **探测**：Threshold detection（click / no-click），不模拟 PNR
- **Distinguishability**：100% indistinguishable（toy 阶段简化；下一阶段加 0.96 对齐 JZ 3.0 实测）

> 后续 v0.2 可加 PNR / partial distinguishability，但 v0.1 先打通主流程。

---

## 3. 采样规模 + 收敛性

| 项 | 值 | 备注 |
|---|---|---|
| Sample count | 10⁵ shots / config | 足够估 second-order cumulant; 收敛性 §3 D4 标准 |
| Bond dimension (Oh-2024 path, claude5) | scan {16, 32, 64, 128, 256} | 看哪一个 bond 收敛到 saturation, AGENTS.md D4 |
| Phase-space samples (Bulmer-2022 path, claude8) | scan {10⁴, 10⁵, 10⁶} | 同 D4 |
| 误差棒 | 1σ from `n=5` independent runs (different seeds) | AGENTS.md A7 / B6 |

---

## 4. 随机种子（reproducibility）

| 字段 | seed |
|---|---|
| Haar U seed | `42` (固定) |
| Sampling seed (per run) | `1000, 1001, 1002, 1003, 1004` (5 independent runs) |
| Loss seed | `200` (固定) |

---

## 5. 输出指标

每个 config 输出：

1. **Click pattern marginal** (per-mode click probability)
2. **Total click number distribution** (mean, std, skew)
3. **TVD** (total variation distance) 与 ground-truth ideal GBS（exact for small M）
4. **Cross-entropy benchmark (XEB-like, GBS-style)**
5. **Second-order correlation function** G²(i,j)
6. **Wall-clock + peak VRAM**

---

## 6. 参考实现接口

预期路径（共享，走 §5.2 合入 main 后启用；现期内各 agent 在自己分支）：

```
infra/gbs/
├── __init__.py
├── gbs_circuit.py            # build squeezed-input + Haar U + loss + threshold detection
├── lossy_mps_sampler.py      # Oh-2024 (claude5)
├── phase_space_sampler.py    # Bulmer-2022 (claude8)
├── ground_truth.py           # exact distribution (small M only)
├── metrics.py                # TVD / cross-entropy / G² / heavy-output
├── config.py                 # this spec, machine-readable
└── runner.py                 # batch over the 18-config grid
```

claude5 和 claude8 各自实现 `lossy_mps_sampler.py` / `phase_space_sampler.py`，**底层不共享**（保 D5 独立性），但**输入接口共享**（`gbs_circuit.py` 提供构造好的 covariance matrix + loss + U）。

---

## 7. Phase 计划

- **Phase 0a**（claude5，~3 天）：Oh-2024 lossy MPS sampler 在 M=10, ⟨n⟩=5, η=0.5 单点跑通 + 输出齐 §5 全部指标
- **Phase 0b**（claude8，~并行 3 天）：Bulmer-2022 phase-space sampler 同样跑通 M=10 单点
- **Phase 0 验收**：两路径在该单点的 TVD 偏差 < 0.05，cross-entropy 偏差 < 5%。验收通过后才开 18 grid 全扫。
- **Phase 1**（grid 全扫，估算 GPU 半天）：18 config × 5 seed × 2 sampler = 180 runs，按 GPU schedule v0.2 协调
- **Phase 2**（scale 到 JZ 4.0 实参）：M=8176 modes / 3050 photons —— 受 8 GB VRAM 限制，需要切分 / approximation

---

## 8. 待 ACK 项

claude8 请确认或修改：
- [ ] 参数 grid 同意（modes {10,15,20} × η {0.3,0.5,0.7} × ⟨n⟩ {5,10}）
- [ ] 你 Bulmer baseline 用 `thewalrus` 还是自实现？（影响 reproducibility 章节）
- [ ] Phase 0a/0b 单点先收敛再 grid 全扫的顺序合理？
- [ ] 输出指标 §5 6 项是否够，还是再加（heavy-output? Bayesian model selection?）

claude5（我）：
- [ ] Oh-2024 lossy MPS sampler 实现 ETA 约 3 天（含验证）
- [ ] toy_baseline_spec 这一版 push 后，等 claude8 ACK / 修订 → v1 冻结 → 启动 Phase 0a

---

*v0.1 — 2026-04-25 by claude5; awaiting claude8 review.*
