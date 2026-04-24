# Jiuzhang 4.0 关键参数（实测拉取自原文 PDF）

> **来源**：arXiv:2508.09092v3，"Robust quantum computational advantage with programmable 3050-photon Gaussian boson sampling"
> **拉取人**：claude5（2026-04-25 06:55 via WebFetch + pypdf 提取）
> **拉取动机**：T7 主攻；同时为 claude2 T8 提供 JZ 3.0 vs JZ 4.0 对比。
> **共享对象**：claude2（T8 主攻）/ claude8（T7 协作 Bulmer baseline）/ claude4 / claude7

---

## 实验参数（页 1–3 直接摘录）

| 参数 | 值 | 来源 |
|---|---|---|
| Squeezed light sources | **1024 SMSS** (single-mode) | p2 §experimental setup |
| OPO 数量 | 4 个 OPOs 复用产生 | p2 |
| 输出模式数 | **8176 qumodes** (L1024 group) | p2-3 |
| 三组数据 | S64 (64/4336)、M256 (256/5104)、L1024 (1024/8176) | p3 line 26-29 |
| 干涉结构 | 3 个 cascade 16-mode 干涉仪 + 2 fiber-delay-loop arrays | p2 |
| 时空编码 | 16×16×16 spatial-temporal modes，连接性 cubic 16³=4096 | p2 |
| **Squeezing parameter r** | **r ≤ 1.8** (典型工作点；97% indistinguishability 在 r=1.8 校准) | p2 line 30-31 |
| **r=1.8 等价 dB** | **15.6 dB**；⟨n⟩ = sinh²(1.8) ≈ 9.5 photons/source | claude5 推导 |
| Source efficiency | **92%** (squeezed light source coupling，明显高于 JZ 3.0 的 88.4%) | p2 line 27 |
| Filter transmission | 99.8%（>40 dB extinction） | p2 line 26 |
| Detection efficiency | 93% per SNSPD，43 ns recovery | p3 line 18-19 |
| **Overall system efficiency** | **51%**（包括 detection；JZ 3.0 是 43%）| p3 line 19-21 |
| Phase locking | λ/200 at 1550 nm | p3 line 22 |
| Max photon clicks | **3050** (L1024) | p3 line 32 |
| **N_eff** (effective squeezed photon number) | **up to 113.5** (L1024) | p4 line 198 |
| Bond dim scan | up to **χ = 2×10⁵** | p5 |

---

## JZ 3.0 vs JZ 4.0 对比表

| 维度 | **JZ 3.0**（PRL 134, 090604, 2025） | **JZ 4.0**（arXiv:2508.09092, 2025） | 攻击方向变化 |
|---|---|---|---|
| Sources | 25 stimulated TMSS | **1024 SMSS** | 40× scale-up |
| Modes | 144 | **8176** | 57× scale-up |
| Squeezing r (nepers) | 1.2–1.6 (≈10.4–13.9 dB) | **≤ 1.8** (≈ 15.6 dB) | 略提升 |
| ⟨n⟩ per source | 2.27–5.94 | **≈ 9.5** | ≈2× 更高 |
| Source η | 88.4% | **92%** | +3.6 pp |
| Overall η | **43%** | **51%** | +8 pp（损耗 LESS）|
| Max photon clicks | 255 | **3050** | 12× 更多 |
| Bond dim feasibility | naive MPS D = 2³¹–2³⁸（不可行）| MPS efficient regime 受 N_eff=113.5 + η=51% 双重压制 | **MPS 路径更难** |

---

## 关键意义：JZ 4.0 是**针对 Oh-2024 设计的反 attack**

论文页 5（line 248-253）明文论证：

> "the MPS algorithm would keep being efficient as long as the transmission η decays as η = o(1/[M^?])... in our experimental architecture the scale-up is achieved at a fixed transmission rate, in which case the **MPS is driven outside its efficient regime** as [N grows]"

⚠️ **这直接关闭 Oh-2024 路径在 T7 上的应用**：

- Oh-2024 在 NP 2024 §3 给出 lossy GBS efficient classical simulation 区域 = high loss & low N。
- JZ 4.0 故意维持 **fixed 高 η（51%）**且 scale-up N（1024 sources）→ N_eff=113.5 推到 Oh-2024 efficient 区外。
- "no χ and N_eff compatible with present-day resources can [break the experiment]"（p4 line 144）

> 攻击复杂度 T_MPS = O(M · d · χ(ε)² · 2^(N_eff/2))
> 在 N_eff=113.5 下，2^(N_eff/2) = 2^56.75 ≈ 1.3×10¹⁷，单 sample MPS 评估即天文量级。

## 对 T7 攻击策略的硬性影响

**结论：Oh-2024 直接 attack T7 路径在论文工作点处理论上不通。** 必须切换：

### Option A — Bulmer-2022 phase-space sampler（claude8 baseline，升级为主攻）

- 不依赖 MPS bond dim
- 操作 Gaussian phase-space (P-rep)，复杂度由 P-rep 是否非负决定（"squashed" classical regime 内可解）
- JZ 4.0 没有针对 Bulmer-2022 设计防御 → **可能可行**
- 需要 claude8 的 baseline 落地后做实际尺寸 estimation

### Option B — 找 JZ 4.0 自身论证的漏洞

候选：
1. **N_eff=113.5 的"effective" 定义可疑**：他们用 covariance matrix 的某种估计；如果 covariance matrix 在 photon-loss + indistinguishability 下被 over-estimate，真实 N_eff 可能小很多 → MPS 变可行
2. **Bayesian test 的"经典 mockup"列表不全**：他们对照的是 thermal / squashed / distinguishable 三类，**没对照 Bulmer phase-space sampler**——这是空白
3. **他们 χ=2×10⁵ 的 truncation error 是 0.9999**——基本是 garbage，但他们的"adapted MPS sampler"通过降低 N_eff（以损失 ground-truth fidelity 为代价）来变高效；这种 hack 是否真的 fair classical sampler？ K-S test G> 2 在 Fig. 3f 上显示 deviation —— 攻击点

### Option C — 实验 robustness 自报告 vs 复测

- "Robust" 是新声明，没经独立重复验证
- 论文 Fig S6-S8 等 SI 校准是否完整披露，也是审查切入点
- **仅 arXiv 预印本，未 accept**——按 README §T7 注：审查门槛低于已中

---

## 立即行动（T7 工作流调整）

1. **claude8 Bulmer baseline 路径升级为 T7 主攻**（不再是"D5 cross-validation"）。我同步通知 claude8。
2. 我自己暂缓"Oh-2024 toy GBS scale-up"路线，转向"在 JZ 4.0 工作点（r=1.8, η=0.51, N=1024）做 Bulmer phase-space simulability 估算"
3. 同时开 Option B 文献审查线（找 JZ 4.0 自身论证的漏洞）—— 这是 AGENTS.md 目标 2 直接产出
4. T7 toy_baseline_spec v0.1 的 grid 仍合理（小规模可比 Oh vs Bulmer），但 Phase 2 scale-up 路径改为 Bulmer-only

---

*v0.1 — 2026-04-25 06:55 by claude5；待 claude2 / claude8 共审。*
