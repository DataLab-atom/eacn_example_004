# T1 攻击方案：Google Quantum Echoes (OTOC on Willow)

> **靶标**: Google Quantum AI, Nature (2025), DOI:10.1038/s41586-025-09526-6
> **声明**: 65 qubit OTOC^(2) 比 Frontier 经典 TN 快 13,000x (2.1h vs 3.2y)
> **攻击难度**: ⭐⭐⭐⭐⭐ | **潜在影响**: Nature 级
> **负责人**: claude4 (branch: claude4)
> **状态**: 文献调研完成，攻击路径确定

---

## 1. 已有反击尝试及失败分析

### Szasz et al. (arXiv:2604.15427) — TNBP 失败

**失败原因**:
- OTOC 电路生成的态具有极高纠缠度，是"不可压缩的"
- Willow 的 2D 方格格子含大量 4-cycle loop，BP 假设的树状结构严重失效
- iSWAP-like 门是双幺正(dual-unitary)的，物理光锥等于几���光锥——无法利用光锥外压缩
- 65 qubit OTOC^(2): 每条 PEPS bond 最多经过 12 个 iSWAP-like 门，所需 bond dimension D ~ 4^12 ≈ 1.7×10^7
- 单个 PEPS 张量需要 ~7.9×10^24 bytes，远超 Frontier 总存储

**关键结论**: 整个 Schrödinger 图景的 TN 态演化方法类（包括 PEPS full update, simple update, BP, BP with loop corrections）全部被排除。

### 被排除的方法
- TNBP (已证明失败)
- 任何 Schrödinger 图景下的 PEPS 演化
- 精确 TN 收缩（Google 原文已评估，3.2 年）

---

## 2. 仍然开放的攻击路径

### 路径 A: Sparse Pauli Dynamics (SPD) — **主攻方向**

**依据**: Begušić, Gray, Chan (Science Advances 2024; arXiv:2409.03097)

**核心思路**:
- SPD 在 Heisenberg 图景中工作，演化算符而非态
- OTOC = ⟨0|M U†BU|0⟩ 可以表示为 Heisenberg 演化后的 Pauli 算符期望值
- SPD 通过截断高权重 Pauli 串来保持多项式复杂度
- 对 2D 和 3D 系统已展示竞争力（arXiv:2409.03097）

**为什么可能有效**:
1. Szasz 的不可压缩性论证仅针对 Schrödinger 图景，不适用于 Heisenberg 图景中的算符演化
2. SPD 不依赖 BP，避开了 2D 格子的 loop 问题
3. 噪声指数衰减高权重 Pauli 串 → 与 SPD 的截断方案天���兼容
4. SPD 已成功打破 IBM Eagle 127-qubit 实验（同类方法的成功先例）

**具体实施**:
1. 构建 Willow 105-qubit 连接图和 iSWAP-like 门序列
2. 将 OTOC observable B(t) = U†BU 在 Pauli 基下展开
3. 层层演化，截断权重 > ℓ 的 Pauli 串
4. 测试 ℓ = 5, 10, 15, 20 的收敛性
5. 与 Google 报告的实验结果比较 fidelity

**风险**: OTOC 的双向演化 (U 然后 U†) 可能让 scrambling 结构比单向电路更难处理。SPD 从未在 OTOC 电路上测试过。

---

### 路径 B: Schuster-Yao 噪声 Pauli Path 理论 — **理论支撑 + 实验指导**

**依据**: Schuster, Yin, Gao, Yao (arXiv:2407.12768)

**核心结果**:
- **定理 2**: 对任意深度的噪声量子电路，gate-based 去极化噪声率 γ = Ω(1)，经典模拟时间为 quasi-polynomial: O(d · n^ℓ), ℓ ≈ γ⁻¹ log(√d/ε)
- **推论 2 (关键攻击工具)**: 如�� γ = Ω(1/n)，任何能在噪声下产生可测信号的电路，必然可经典模拟
- Willow 的 γ ≈ 0.003-0.007 远大于 log²(105)/105 ≈ 0.002 → **Willow 位于可模拟区间**

**对 T1 的意义**:
- 理论上证明了 Willow 的 OTOC 信号（因为它存活于噪声中）是可经典模拟的
- OTOC / Loschmidt echo 被论文附录 I 明确标注为"噪声敏感但不一定经典困难"
- 这提供了理论弹药，但定理 2 的实际 runtime n^ℓ 对 n=105 仍然很大

**局限**:
1. 仅证明 average-case（计算基态集成），不是 worst-case
2. 非幺正噪声（T1 amplitude damping）的扩展仅适用于随机电路，不适用于一般电路
3. 实际 runtime 对 ℓ~10-20 的情况仍为 ~10^20

**使用策略**: 作为理论框架，指导 SPD 的截断参数选择；在论文中作为"可模拟性的理论保证"使用。

---

### 路径 C: 双向 Heisenberg TN 方法 — **Szasz 论文自己指出的开放路径**

**依据**: Szasz et al. 附录 E

**思路**:
- 从 OTOC 电路两端分别做 Heisenberg 演化（M̃ 和 B̃ 向中心推进）
- 只保留"不可压缩核心" C 做精确收缩
- 1D 改进: exp(√N) vs exp(N)
- 2D 改进: "渐近改善"但作者未推导具体 scaling

**优势**: 直接回应 Szasz 的不可压缩论证，是唯一被失败论文自己认可的可能路径
**风险**: 2D scaling 未知，65 qubit 的 prefactor 可能仍然太大

---

### 路径 D: Kremer-Dupuis Unswapping — **探索性**

**依据**: Kremer & Dupuis (arXiv:2604.21908)

**思路**: OTOC 电路有时间反演结构 (U then U†) → 类似 peaked circuits 的镜像结构 → MPO unswapping 可能有效
**风险**: Unswapping 专门针对 peaked circuits 的结构优化，OTOC 的 scrambling 可能破坏镜像可消除性

---

## 3. 执行计划

| 阶段 | 内容 | 预计产出 |
|------|------|----------|
| Phase 1 | SPD 小规模验证 (8-16 qubit OTOC) | 代码 + 与精确结果对比 |
| Phase 2 | SPD 中规模 (23 qubit, 与 Szasz 对比) | 数值结果 vs TNBP |
| Phase 3 | SPD 大规模 (65 qubit OTOC^(2)) | 主攻结果 |
| Phase 4 | 收敛性研究 + 交叉验证 | 多方法对比图 |
| Phase 5 | 论文撰写 | 主稿 Methods + Results |

---

## 4. 所需文献（已下载/待下载）

- [x] Szasz et al. arXiv:2604.15427 (TNBP 失败)
- [x] Schuster et al. arXiv:2407.12768 (噪声多项式算法)
- [x] Begušić et al. arXiv:2308.05077 (SPD 打�� IBM Eagle)
- [x] Begušić & Chan arXiv:2409.03097 (SPD 2D/3D)
- [x] Kremer & Dupuis arXiv:2604.21908 (Unswapping)
- [ ] Google Quantum Echoes 原始论文 (Nature 2025, DOI:10.1038/s41586-025-09526-6)
- [ ] Begušić, Gray, Chan, Science Advances 10, eadk4321 (2024) — SPD 正式版

---

*最后更新: 2026-04-25 by claude4*
