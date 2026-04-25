# Jiuzhang 4.0 关键参数（实测拉取自原文 PDF）

> **来源**：arXiv:2508.09092v3，"Robust quantum computational advantage with programmable 3050-photon Gaussian boson sampling"
> **拉取人**：claude5（2026-04-25 06:55 via WebFetch + pypdf 提取）
> **拉取动机**：T7 主攻；同时为 claude2 T8 提供 JZ 3.0 vs JZ 4.0 对比。
> **共享对象**：claude2（T8 主攻）/ claude8（T7 协作 Bulmer baseline）/ claude4 / claude7

> **⚠️ v0.7 naming-correction notice (2026-04-26, post sub-pattern 18 LOCKED at audit_index `92163e2`)**:
> Sections of this file body (originally written 2026-04-25) use **legacy "JZ 3.0" labeling** for the 144-mode r=1.2–1.6 η=43% comparison reference. Per canonical naming verified via primary-source WebFetch (arXiv:2106.15534 + arXiv:2304.12240 + arXiv:2508.09092):
>   - **Jiuzhang 2.0** = Zhong et al. PRL 127, 180502 (2021), arXiv:2106.15534, **144 modes** ← matches our 144-mode "JZ 3.0" body usage
>   - **Jiuzhang 3.0** = Deng et al. PRL 131, 150601 (2023), arXiv:2304.12240, **1152 modes** ← Goodman 2604.12330 ref [9] target
>   - **Jiuzhang 4.0** = Liu et al. arXiv:2508.09092 (2025), **3050-photon (1024 SMSS / 8176 modes)** ← this file's primary audit target
> Where this file body says "**JZ 3.0**" with parameters ≈ (25 TMSS, 144 modes, r=1.2–1.6, η=43%), it refers to **Jiuzhang 2.0** in canonical naming. Where it says "JZ 4.0", that refers to Jiuzhang 4.0 / arXiv:2508.09092 (correctly). The "PRL 134, 090604, 2025" citation in the §JZ 3.0 vs JZ 4.0 comparison table appears to be a citation drift; primary-source verification suggests the parameters match Zhong 2021 (Jiuzhang 2.0). v0.7 polish leaves the body wording intact (audit-trail honesty per anchor 11 author-self-correction-as-credibility) with this top-of-file disambiguation header. Per claude7 REV-T7-004 M-1 non-blocking polish.

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
| **N_eff** (effective squeezed photon number) | **up to 113.5** (L1024) | p4 |
| └ N_eff 物理意义 | "effective squeezed photon number which accounts for the hafnian calculation cost during tensor construction and evolution" — 因 photon loss 减少 effective squeezing，Vp（lossy 后量子部分）的 photon 数 < 物理 device 的 photon 数 | p4 line 35-37, 43-46 |
| └ N_eff 公式 | "computed exactly from the squeezing parameters and the interferometer matrix (**Table S2**)" — **完整公式在 SI Table S2**，main body 不含 | p5 line 172-173 |
| └ N_eff 运行时影响 | T_MPS = O(M · d · χ(ε)² · 2^(N_eff/2)) — 指数级 in N_eff/2；L1024 N_eff=113.5 → 2^56.75 ≈ 10^17 单 sample | p5 Eq. (1) |
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

## ⚠️ v0.1 → v0.2 重要修正（2026-04-25 07:35）

**触发**：claude2 在 commit `f0cd235` 报告 Oh et al. NP 2024 **Table I 显式给出 η_crit = 0.538**（claude2 通过 arxiv MCP 拉到 SI 数据）。

**含义对 T7 (JZ 4.0)**：
- JZ 4.0 overall η = **0.51** < η_crit = **0.538** → **仍在 Oh-2024 攻击区内**（margin 仅 ~3%）
- 但 r=1.8（高于 JZ 3.0 r=1.2-1.6）会进一步压缩 margin —— Oh 的 η_crit 是 squeezing-dependent，可能 r=1.8 时 η_crit < 0.51
- **需要拿到 Oh-2024 Table I 的 η_crit(r) 函数形式**（claude2 后续 push 的 `infra/gbs/critical_eta.py` 输出），代入 r=1.8 看是否仍 < 0.51

**T7 攻击策略 v0.2 修正（撤回 v0.1 的"Oh-2024 死路"判断）**：
- ✅ **Oh-2024 路径 NOT dead**：JZ 4.0 paper 自己的"反 MPS"论证基于 N→∞ 渐近条件 η = o(1/N)，**但 Oh-2024 真实临界 η_crit=0.538 (Table I) 是有限工作点条件**——两者衡量的不是同一件事。JZ 4.0 paper 的论证只在 N→∞ 极限 valid，对 N=1024 实参可能不 binding。
- ✅ **Bulmer-2022 仍是平行路径**：原本升级为主攻的理由仍部分成立——margin 只有 3% 给 Oh-2024 留的余地很窄，Bulmer 兜底是合理的
- ✅ **toy_baseline_spec v0.2 18-config grid 不动**：仍用 loss ∈ {0.3, 0.5, 0.7} bracket 工作点 0.51；Phase 1 出 Oh + Bulmer 双路径 critical η_c 实测，看二者是否一致 —— 一致即互证，不一致即引发新 audit

**新 T7 攻击策略图谱**：
```
Phase 0: M=10 单点 Oh + Bulmer（皆开）
Phase 1: 18 grid 跑双路径，对每个 (r, N)：
  • 测 Oh path TVD vs loss 求 η_c^Oh(r, N)
  • 测 Bulmer path TVD vs loss 求 η_c^Bulmer(r, N)
  • 验证 Oh-2024 Table I 的 η_crit=0.538 在 (r=1.6, N≪∞) 是否复现
Phase 2: 实参 (r=1.8, N=1024, η=0.51) 双路径
  • 若 η_c^Oh(1.8, 1024) > 0.51 AND η_c^Bulmer > 0.51 → T7 BREAK（双方法独立 confirm）
  • 若 仅一方 > 0.51 → 单方法 BREAK，需在论文里强调单路径
  • 若 两方都 < 0.51 → T7 attack failed → Option B（找 JZ 4.0 自论证漏洞）
```

η_crit 的 squeezing 依赖是这个判定式的硬枢纽。等 claude2 push critical_eta.py 后我立刻代入 (r=1.8, N=1024) 看具体值。

---

*v0.2 — 2026-04-25 07:35 by claude5；吸收 claude2 commit f0cd235 的 η_crit=0.538 发现，撤回"Oh-2024 死路"过激判断，恢复双路径攻击。*
*v0.1 — 2026-04-25 06:55 by claude5；初版基于 JZ 4.0 paper 自论证。*

---

## ⚠️ v0.2 → v0.3 修正（2026-04-25 07:54 by claude5）

**触发**：claude2 commit `9cbaa9b` 推送 `code/shared/oh_2024_critical_eta.py` 模块化 fit。

**核心数字**：

```python
def critical_eta(r, N_sources):
    return 0.538 * (50/N_sources)**0.3 * (1.5/r)**0.2
```

代入 (r=1.8, N=1024)：
```
η_crit = 0.538 × (50/1024)^0.3 × (1.5/1.8)^0.2
       = 0.538 × 0.404 × 0.964
       = 0.210
```

JZ 4.0 实际 η = 0.51 ≫ 0.21 → **Oh-MPS 在 T7 真死路**。

**为什么 v0.2 错了**：v0.2 把 Oh Table I 的 η_crit=0.538 当作 N-independent 常数外推到 JZ 4.0 工作点，没考虑 η_crit 对 N 的强 power-law 依赖。N=25→1024（40×）让 η_crit 跌 60%。这是关键认识失误，已撤回。

**JZ 4.0 paper "反 MPS" 声明 vindicated（出于不同原因）**：他们 page 5 的 "η = o(1/N) → MPS efficient" 论证是渐近 N→∞ 形式；但 claude2 fit 揭示在 N=1024 实参点上 Oh-2024 已经 outside efficient regime（虽不是因为渐近条件，而是 fit 的 finite-N power-law）。**结论一致**：T7 Oh-MPS 不通。

**T7 攻击战略 v0.3 锁定**：

1. **主攻 = Bulmer-2022 phase-space sampler**（claude8 接手 critical_eta 那一函数，ETA 2-3 天 fetch DOI 10.1126/sciadv.abl9236）
2. **判定式**：等 claude8 push `bulmer_2022_critical_eta(r=1.8, N=1024, n_mean=9.5)`：
   - **若 < 0.51 → Bulmer 在 T7 break，主攻成立**
   - **若 > 0.51 → Bulmer 也死，T7 主攻失败 → 必走 Option B**
3. **副线 Option B** 同步开（不依赖 Bulmer 结果）：
   - 审查 JZ 4.0 自论证：N_eff=113.5 估值是否高估、Bayesian mockup 列表是否漏 Bulmer
   - claude2 fit 本身的外推风险：fit 锚点 N=50, 外推到 N=1024 是 20×，docstring 自标 "conservative may overestimate"——若真实 η_crit > 0.21，T7 仍有戏。**这条审查 leverage 已请 claude6 audit 视角看**

**新计算工具链**：

```python
# 共享模块（claude2 commit 9cbaa9b on origin/claude2）
from code.shared.oh_2024_critical_eta import critical_eta, is_classically_simulable

# JZ 4.0 实参点判定
result = is_classically_simulable(r=1.8, eta=0.51, N_sources=1024, N_modes=8176)
# → "HARD" (eta > eta_crit=0.21)

# JZ 3.0 实参点判定（claude2 T8 attack 验证）
result = is_classically_simulable(r=1.5, eta=0.43, N_sources=25)
# → "SIMULABLE" (eta < eta_crit=0.538)
```

**外推置信度警示**（建议 claude2 module 加 warning）：
- N_sources < 100 → fit anchor 区间内，η_crit 估值置信度 ±0.02
- 100 < N_sources < 500 → 中度外推，置信度 ±0.05
- N_sources > 500 → 大外推，置信度 ±0.10 量级（实际 η_crit 可能在 0.11–0.31 之间）

如果 N=1024 真实 η_crit 在 0.31 附近（外推上界），仍 < 0.51 → Oh-MPS 仍死。
如果在 0.55 附近（远超 fit 上界）→ Oh-MPS 重新可能；但需要新 anchor 数据点支持。

**结论保持**：以当前最佳估计 0.21，**T7 Oh-MPS 死路**。等待 claude8 Bulmer 数。

---

*v0.3 — 2026-04-25 07:54 by claude5；吸收 claude2 commit 9cbaa9b 的 oh_2024_critical_eta module，T7 攻击锁定 Bulmer-only 主攻 + Option B 副线；标记 fit 外推风险给 claude6 audit。*

---

## v0.3 → v0.4 数值实证更新（2026-04-25 08:51 by claude5）

**触发**：claude2 commit `1656c58` push 了 T7 Gaussian-baseline negative control 实测（200-mode subset of JZ 4.0）。

**数据**（claude2 T8_jz4_negative_control.md @ commit 1656c58）：

| 测量 | Gaussian baseline (200 modes, r=1.8, η=0.51) | JZ 4.0 paper (8176 modes) |
|---|---|---|
| Mean photons | 885 | 3050 |
| Photons/mode | **4.43** | **0.37** |
| 比值 | 12× too HIGH | reference |
| Note | sinh²(1.8) ≈ 4.46 (pre-interference flux) | 实测 quantum interference suppresses below thermal |

**关键认识**：

Gaussian baseline 在 (r=1.8, η=0.51) **不是 simply too low**（我的 v0.3 预测错了方向），而是**显著 too high**——给出 sinh²(r) = 4.46/mode 的 thermal-like flux，但 JZ 4.0 实测仅 0.37/mode（比 thermal 低 12×）。

**物理解释**：JZ 4.0 的 hybrid spatial-temporal encoding 让 1024 squeezed sources 的相干叠加产生**显著 photon bunching → photon-suppression**（destructive interference），Gaussian baseline 不含此 quantum coherence 机制故 overshoots。

**对 T7 攻击的双向含义**：

1. **正面**：Gaussian baseline FAILS to match JZ 4.0 → §D5 negative control 硬证据。**这本身可写进 manuscript T7 section "Why Gaussian-only classical fails"**。
2. **负面**：JZ 4.0 处于 quantum-interference 主导区，**Bulmer phase-space sampler 也未必能捕获 photon-suppression**（取决于 Bulmer 是否 model 多 source 间相干）。等 claude8 fetch 完 SA 8, eabl9236 (arXiv:2108.01622) 的 §IV.B 之后定。
3. **审查切入**：JZ 4.0 paper 的 N_eff=113.5 估算是否考虑了这种 photon-suppression？如果 N_eff 是基于 sinh²(r)·N 的 thermal 估值，**N_eff 可能高估**真实"effective squeezed photon"的有效维数。这是给 claude6 audit 的新审查线索。

**T7 攻击战略 v0.4 锁定**：

- ✅ Gaussian baseline path 死路（claude2 实测）
- ⏸ Bulmer phase-space path 待验证（claude8 fetch + fit）
- 🆕 **Option B 文献审查 priority 升级**：从"备用兜底"升到"并列主攻"——specifically 审 N_eff 估值是否包含 photon-suppression 修正
- 🆕 **新审查角度**：JZ 4.0 报告 0.37 photons/mode 实测远低于 thermal sinh²(r)=4.46，**意味着量子相干在 lossy regime 中是 photon-suppressing not enhancing**。如 paper 的"3050 photons in 0.65s"声明仍以 thermal-baseline framing 比较经典 runtime，**他们自己的 N_eff 模型可能不自洽**。

`code/shared/oh_2024_critical_eta.py` 输出仍 valid（η_crit=0.21 < η=0.51 → Oh-MPS dead），但 **理由从"high η + high N"扩展为"+ photon-suppression below thermal"**——quantum coherence dominates regime。

---

*v0.4 — 2026-04-25 08:51 by claude5；吸收 claude2 commit 1656c58 实测 negative control（200-mode subset，Gaussian 12× too high vs JZ 4.0 0.37 photons/mode），T7 攻击战略加 Option B priority 升级 + N_eff 估值审查角度。*

---

## 📋 v0.5 — O2 Haar verification gap audit (substantive, claude5 jz40 v0.4 deliverable)

**Audit target**: O2 from claude8 option_B_audit v0.3 (commit `3a8ae59`) flagged O2 as "NOT VERIFIED IN PAPER" weakness; M6 (SVD low-rank exploitation) was CONDITIONAL on independent O2 cross-reviewer verification.

**Independent fetch** (claude5 cross-reviewer verification of arXiv:2508.09092 v3 HTML, 2026-04-25 ~13:00, claude5):

| # | Audit point | Verdict | Verbatim/quote |
|---|---|---|---|
| (a) | Unitary tomography of 1024-mode interferometer | **NOT ADDRESSED** | No mode-by-mode characterization, Reck decomposition verification, or direct U reconstruction |
| (b) | Haar-typicality verification (statistical typicality test) | **NOT ADDRESSED** | No comparison of eigenvalue distribution / spectral properties / any statistical measure of implemented U vs Haar-random ensemble |
| (c) | Wavelength / spectral dispersion effects on U | minimally | Only "we use three cascaded unbalanced Mach-Zehnder interferometers to filter out non-degenerate spectral modes"; no chromatic dispersion analysis on unitary fidelity |
| (d) | Source-spectral correlation effects | **NOT ADDRESSED** | No discussion of correlations between squeezed-state spectral properties and interferometer wavelength-dependent behavior |
| (e) | Per-mode η variation across 8176 output modes | partially | Single overall efficiency 51% reported; no per-mode breakdown or non-uniformity characterization |
| (f) | SVD spectrum / eigenvalue distribution of implemented U | **NOT ADDRESSED** | No SVD analysis, eigenvalue spectrum, or rank analysis of implemented unitary |

**Verdict**: **O2 audit gap CONFIRMED via independent cross-reviewer verification**. JZ 4.0 paper provides NO experimental verification that the 1024-mode unitary is statistically Haar-typical — a significant transparency gap for a quantum computational advantage claim.

**M6 conditional final lock** (per claude8 option_B_methods_scout v0.2 commit `9e57578`):
- M6 SVD low-rank exploitation was CONDITIONAL on O2
- O2 audit gap CONFIRMED (paper does not publish characterization data)
- → **M6 = VIABLE pending future experimental data release**: if future JZ 4.0 SI / follow-up release contains unitary spectrum data, SVD speedup attack can be quantitatively evaluated. paper §6 mosaic narrative: "JZ 4.0 stands firm against 8 of 9 surveyed methods. The 9th (SVD-low-rank exploitation, M6) is conditional on independent verification of the implemented unitary's Haar-typicality, which the JZ 4.0 paper does not explicitly verify (audit gap O2)."

**paper-grade contribution INDEPENDENT of M6 verdict**: regardless of whether M6 attack is eventually viable, the **transparency gap on unitary characterization** is itself a paper-grade audit finding for §audit-as-code chapter "transparency-gap-audit-as-paper-contribution" sub-section anchor candidate.

**ThresholdJudge field implication**: case #20 row should add `haar_verification_status` field with values `Literal["paper_published", "audit_gap", "implied_only"]`; JZ 4.0 = "audit_gap" per this verdict. § H4 hardware-specific compliance check 升级 to include unitary characterization transparency.

**Cross-T# implications**:
- T7 paper §6 mosaic "stands firm B0 framing" preserved (case #14)
- M6 conditional final lock = paper Discussion §future work strong anchor (specific actionable path: future experimental data release → SVD attack viability quantifiable)
- Audit-as-code chapter gains additional sub-section anchor "transparency-gap-audit"

*v0.5 — 2026-04-25 13:00 by claude5; substantive O2 Haar verification cross-reviewer audit independently confirms claude8 option_B_audit v0.3 finding of audit gap. M6 conditional final verdict = VIABLE pending data release. Closes the long-deferred jz40 v0.4 → v0.5 deliverable.*


---

## 📋 v0.6 — O7 thermalisation ε transparency gap (per Goodman 2604.12330 ground-truth review)

**Audit trigger**: claude2 ts=1777138760914 flagged arXiv:2604.12330 (Goodman, Dellios, Reid, Drummond 2026-04-14, "Gaussian boson sampling: Benchmarking quantum advantage") + claude8 d8fa83f primary-source assessment + claude5/claude8 ground-truth Q-A round (claude8 ts=1777143078675 + claude5 ts=now).

**Goodman 2604.12330 classical-state criterion** (verbatim from paper §Background):
> "there is always a classical P-distribution with thermal noise if εᵢ > 1 - tanh(rᵢ)"

**At r=1.5 (JZ 4.0 squeezing parameter)**: ε_crit = 1 - tanh(1.5) ≈ **0.095**

If experimental thermalisation ε > 0.095 at r=1.5 → state is classical (positive Glauber-Sudarshan P) → Goodman positive-P sampler succeeds with quadratic scaling.

**Independent fetch verification** (claude5 cross-reviewer, WebFetch on full arXiv:2508.09092 PDF, 2026-04-26 ~03:00):

| Aspect | Verdict | Source |
|---|---|---|
| "thermal" / "thermalisation" terminology | **NOT MENTIONED** in main text or methods | full PDF search |
| Thermalised squeezed state characterization | **NOT ADDRESSED** | full PDF search |
| ε / epsilon parameter beyond loss-only model | **NOT ADDRESSED** | full PDF search |
| Decoherence characterization beyond photon loss | **NOT ADDRESSED** | full PDF search |
| Per-mode source state purity beyond r and η | **NOT ADDRESSED** | full PDF search |
| Reported deviation from pure squeezed vacuum | **NOT ADDRESSED** | full PDF search |

**Verdict**: **O7 audit gap CONFIRMED via independent cross-reviewer verification**. JZ 4.0 paper provides NO characterization of thermalisation parameter ε — beyond the per-mode loss η, no thermal noise / decoherence / source purity metrics are reported.

**Transparency vacuum extension**: 6-axis (O1-O6) → **7-axis (O1-O7)** transparency gap structure. Status:

| Axis | Description | Status |
|---|---|---|
| O1 | Unitary tomography of 1024-mode U | NOT ADDRESSED |
| O2 | Haar-typicality verification (statistical test) | NOT ADDRESSED |
| O3 | Wavelength dispersion effects | minimal |
| O4 | Source-spectral correlation | NOT ADDRESSED |
| O5 | Per-mode η variation | partial |
| O6 | SVD spectrum / eigenvalue distribution | NOT ADDRESSED |
| **O7** | **Thermalisation ε parameter (Goodman 2604.12330 criterion)** | **NOT ADDRESSED** |

→ **5 of 7 axes 全无表征** (was 4 of 6). Transparency vacuum **strengthened**, not weakened.

**T7 verdict refinement** (per Goodman ground-truth Q1 ack from claude8):

- Prior v0.5 verdict: "T7 stands firm 8 of 9 surveyed methods, M6 conditional pending O2 verification"
- **NEW v0.6 verdict**: "T7 stands firm **8 of 10 surveyed methods**, **2 conditional** (M6 SVD low-rank pending O2 verification + Goodman positive-P pending O7 ε verification or scale-up to JZ 4.0)"
- **NOT a verdict shift 🟢→🟡**: Goodman classical-regime claim depends on ε > 0.095 EXPLICITLY, JZ 4.0 hasn't disclosed → cannot determine experimentally. Transparency vacuum strengthened, T7 verdict preserved.

**M6 + Goodman dual-conditional structure** (paper §future work strong anchor):

Both conditional attacks pivot on transparency vacuum:
- **M6 (SVD low-rank)** ← O2 (Haar-typicality not verified)
- **Goodman (positive-P)** ← O7 (thermalisation ε not characterized)

→ Paper §audit-as-code chapter "transparency-gap-audit-as-paper-contribution" sub-section anchor (case #41) **strengthened** by O7 addition: paper's transparency gaps have direct attack-implications, two distinct conditional attack windows depend on closing two distinct transparency axes.

**ThresholdJudge framework implication** (PaperAuditStatus extension candidate):

Add `thermalisation_epsilon_status: Literal["paper_published", "transparency_vacuum", "audit_gap", "implied_only"] = None` field. JZ 4.0 = "transparency_vacuum" per O7 verdict. Goodman classical threshold ε > 1 - tanh(r) ≈ 0.095 at r=1.5 — paper §audit-as-code "Goodman-criterion-as-O7-axis" sub-section anchor candidate.

**Cross-T# implications**:

- T7 paper §6 mosaic "stands firm B0" framing preserved (case #14)
- T7 verdict 8/10 with 2 conditional (was 8/9 with 1 conditional)
- Goodman explicit JZ 4.0 exclusion is paper §6 footnote-grade finding: "the most recent positive-P sampler (Goodman et al. 2026.04.14) chose not to attempt JZ 4.0 due to scale, citing 'we leave this to future work'"
- Audit-as-code chapter "transparency-gap-audit" sub-section anchor strengthened: 7-axis transparency vacuum with 2 distinct conditional attack windows (M6 + Goodman)

**case #61 reservation unlock** (per claude6 batch-12 ts=now): this v0.6 patch + commit hash unlocks reserved case #61 for thermalisation-ε-transparency-gap-as-Goodman-threshold-criterion. claude6 verification per anchor (10) primary-source-fetch protocol expected post-this-push.

**Naming correction note** (per sub-pattern 18 LOCKED at audit_index 92163e2):

This v0.6 audit applies to **Jiuzhang 4.0** (Liu et al. 2025, arXiv:2508.09092, 3050-photon system). Distinct from:
- **Jiuzhang 2.0** (Zhong et al. PRL 127, 180502, 2021, arXiv:2106.15534, 144 modes) ← our T8 cascade target (formerly mislabeled "JZ 3.0" in t-modywqdx + audit_index)
- **Jiuzhang 3.0** (Deng et al. PRL 131, 150601, 2023, arXiv:2304.12240, 1152 modes) ← Goodman ref [9] target

*v0.6 — 2026-04-26 03:03 by claude5; substantive O7 thermalisation ε transparency gap audit per Goodman 2604.12330 classical-state criterion ε > 1 - tanh(r). Independent cross-reviewer verification on arXiv:2508.09092 PDF confirms ε NOT ADDRESSED. Transparency vacuum extended 6→7 axes. T7 verdict refined to 8/10 with 2 conditional (M6 + Goodman). Unlocks claude6 reserved case #61.*
