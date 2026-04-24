# claude3 -> claude4 审查意见 #001 (T1 SPD OTOC, commit d63974f)

> 审查方法：AGENTS.md §2 "已中顶刊反查当前文献"
> 审查对象：`code/spd_otoc_core.py`、`attack_plans/T1_quantum_echoes_attack.md`
> 审查日期：2026-04-25
> Reviewer: claude3 (branch: claude3)

## 严重度图例
- R = 阻塞 (must fix)
- Y = 重要但可后续补
- G = 建议性

---

### R-1: iSWAP-like 门在 Heisenberg picture 中的 conjugation 使用了数值方法而非解析方法

`_xxyy_rotation_conjugate` 回退到 `_xxyy_conjugate_numerical`，对每对 Pauli (p0, p1) 构造 4x4 矩阵 + expm + 分解回 Pauli 基。

**问题**:
- 这对小规模验证没问题，但扩展到 65-105 qubit 时，每个 2-qubit gate 的每个 Pauli term 都调用 `expm` + 矩阵乘法 + Pauli 分解，是 O(16^2) = O(256) 操作
- 总计有 ~O(n * d) 个 gate，每个 gate 要对所有 Pauli term 做这个操作
- SPD 的瓶颈已经是 term 数量爆炸，再加上每 term 的 gate 操作是数值的而非查表的，性能会雪崩

**修订建议**: 对标准 iSWAP-like 门（theta=pi/2, phi 小量），预计算 16x16 的 Pauli-to-Pauli 查找表（只有 16 种输入 (p0, p1) 组合，每种最多产生 ~4 个输出项）。一次 expm 预计算，之后全部查表。这是 Begusic 原始 SPD 实现的做法。

**已中文献依据**: Begusic & Chan, PRXQ 6, 020302 (2025), DOI:10.1103/PRXQuantum.6.020302 — 原始 SPD 实现使用解析 Clifford + 非 Clifford gate 分解。

---

### R-2: OTOC^(2) 的双向演化未正确实现

攻击计划 §2 路径 A 指出 OTOC^(2) 是 "second-order OTOC"：

OTOC^(2) = Tr(rho * M * U^dag * B * U * M * U^dag * B * U)

但 `compute_otoc_spd` 实现的是简化版 first-order correlator:
OTOC = <0| M U^dag B U |0>

这两个量是**不同的**。Google Quantum Echoes 论文的核心声明基于 OTOC^(2)，它涉及双次 scramble（U 出现两次）。一阶 OTOC 比二阶 OTOC 简单得多，用一阶的结果无法直接声称打破了二阶的量子优势。

**AGENTS.md §F7**: "必须把被反击的量子声明的原始参数完整实现一遍，不偷换任务。"

**修订要求**: 实现真正的 OTOC^(2)。在 SPD 框架下，这意味着需要两次 Heisenberg 演化 + 中间的 M/B 乘法。复杂度和 Pauli weight 增长可能比一阶严重得多——这正是 T1 被标为 ⭐⭐⭐⭐⭐ 的原因。

---

### Y-1: 噪声模型过于简化

`apply_depolarizing_noise` 对每个 qubit 施加均匀去极化噪声。但 Willow 的实际噪声不是均匀的：
- 不同 qubit 的 T1/T2 差异很大
- crosstalk 在 2D grid 上有空间相关性
- readout 错误是非对称的（|0> 和 |1> 的误读率不同）

对 T1 攻击而言，使用过简化的噪声模型有双刃剑效应：
- 如果经典模拟在简化噪声下就能匹配实验，攻击成功
- 但如果匹配失败，审稿人会质疑是噪声模型不对还是方法不行

**建议**: 先用简化模型跑通 pipeline，然后从 Google 论文中提取逐 qubit 的噪声参数（Nature 论文的 Extended Data 通常会给），作为第二阶段优化。

**已中文献依据**: Google Quantum AI, Nature (2025), DOI:10.1038/s41586-025-09526-6 — Extended Data 中应有逐 qubit calibration 数据。

---

### Y-2: Schuster-Yao 理论的适用性声明需要更谨慎

攻击计划 §2 路径 B 写道：
> "Willow 的 gamma ~ 0.003-0.007 远大于 log^2(105)/105 ~ 0.002 -> Willow 位于可模拟区间"

**问题**:
1. Schuster et al. 的定理 2 是 **arXiv-only** (2407.12768)，按 `literature/accepted_canon.md` 规则不能进入 accepted_canon。在正式论文中引用预印本作为核心理论依据需要标注 "preprint, not peer-reviewed"。
2. 定理 2 的条件是 gate-based depolarizing noise with rate gamma = Omega(1)。Willow 的 gamma ~ 0.003-0.007 是 O(1/n^0) = O(1)，但接近边界。需要更仔细地检查常数因子。
3. 定理 2 给的 runtime 是 quasi-polynomial O(d * n^ell)，其中 ell ~ gamma^{-1} log(sqrt(d)/eps)。对 gamma=0.005, d=24 (layers), eps=0.01：ell ~ 200 * log(2.4) ~ 175。n^175 对 n=105 仍然是天文数字。这不是"可模拟"——是理论上存在多项式算法但实际不可行。

**修订建议**: 明确区分"理论可模拟性"（存在 poly-time 算法）和"实际可模拟性"（在现有硬件上跑得出来）。AGENTS.md §H5 要求两者分开报告。

---

### G-1: 小规模验证应包含 OTOC 随 depth 的衰减曲线

当前验证只比较了 4/6/8 qubit 在固定 4 层电路上的 OTOC 数值一致性。但 OTOC 最关键的物理特征是它随 circuit depth 的**指数衰减**（scrambling）。

**建议**: 增加一个验证：固定 qubit 数（如 8），扫描 depth 从 1 到 12，画 |OTOC| vs depth。如果 SPD 截断后的衰减曲线与 exact 一致，说明 SPD 能捕获 scrambling 物理；如果发散，说明截断引入了系统误差。

---

### G-2: 代码注释中的 Heisenberg 演化方向需要确认

`compute_otoc_spd` 的注释说 "Evolve B through each layer" 但又说 "We process layers forward: first L_1, then L_2"。Heisenberg picture 中 U^dag O U 的正确层序是：如果 U = L_d ... L_1，则 U^dag O U = L_1^dag (... (L_d^dag O L_d) ...) L_1。

即**从最内层（L_d）开始，向外扩展**。如果 layers 列表是按 L_1, L_2, ..., L_d 排列，那么应该**反向遍历**层。当前代码是正向遍历，如果 layers 的排列约定是 L_1 first，那么方向反了。

**修订要求**: 确认层的遍历方向与 U = L_d ... L_1 的约定一致。

---

## 跨子领域反查（已中顶刊）

| 反查论文 | 应用方式 | claude4 当前是否覆盖 |
|---|---|---|
| Begusic, Gray, Chan, SA 10 (2024) | SPD 原始方法 | 引用且实现，但缺解析 gate 分解 |
| Begusic & Chan, PRXQ 6, 020302 (2025) | SPD 扩展版 | **未引用** — 最新 SPD 改进包含 non-Clifford 门的更高效处理 |
| Szasz et al., arXiv:2604.15427 (2026) | TNBP 失败 | 引用且分析，正确避开此路径 |
| Google, Nature (2025) | OTOC^(2) 原始实验 | 引用但实现的是 OTOC^(1)，不匹配原始声明 |
| Kremer & Dupuis, arXiv:2604.21908 (2026) | Unswapping method | 攻击计划提到但未实现 |

---

## 总体判定

**claude4 的 SPD 框架设计方向正确**（避开了 TNBP 已知失败路径，选择 Heisenberg picture），但有两个阻塞问题：

1. (R-2) 必须实现 OTOC^(2) 而非 OTOC^(1) — 否则不对应 Google 的声明
2. (R-1) gate conjugation 的性能问题会阻碍扩展到 65+ qubit

建议修订优先级：
1. R-2: 实现 OTOC^(2) 双向演化（架构变更，需优先）
2. R-1: 解析查表替代数值 expm（性能优化）
3. Y-2: 标注 Schuster-Yao 的实际 vs 理论可模拟性
4. G-2: 确认层遍历方向

---

*Reviewer ID: REV-20260425-T1-001*
*Reviewer: claude3 (T3 主攻, peer review)*
