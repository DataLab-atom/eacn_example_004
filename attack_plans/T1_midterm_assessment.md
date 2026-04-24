# T1 中期评估：Google Quantum Echoes 经典反击可行性

> **日期**: 2026-04-25
> **作者**: claude4 (branch: claude4)
> **审查**: claude3 (REV-20260425-T1-001), claude6 (SPD code review)
> **状态**: Phase 2 完成, Phase 3 进行中

---

## 1. 已完成的工作

### 1.1 文献调研
- 深度阅读 Szasz et al. (2604.15427): TNBP 失败，排除了全部 Schrödinger 图景方法
- 深度阅读 Schuster et al. (2407.12768, preprint): 噪声下拟多项式算法理论
- 确认 SPD (Begušić-Chan) 作为 Heisenberg 图景主攻路径

### 1.2 代码实现
- SPD 核心框架: Pauli 代数、Heisenberg 门共轭、iSWAP-like 门
- OTOC^(1) 和 OTOC^(2) 均已实现和验证
- 查表优化: 20-77x 加速
- 去极化噪声模型

### 1.3 数值验证
- 4/6/8 qubit OTOC^(1): w=n 时机器精度 (1e-16)
- 4/6/8 qubit OTOC^(2): w=n 时机器精度 (1e-15)
- 10 qubit OTOC^(2) depth scan: 精确验证通过

### 1.4 Peer Review
- claude3 审查 (REV-20260425-T1-001): R-1/R-2 均已修复
- 我审查了 claude2 T4 (REV-20260425-T4-001)

---

## 2. 关键发现

### 2.1 正面发现 (支持攻击可行)
1. **SPD 在 OTOC 上首次验证成功** — 此前从未有人用 SPD 计算 OTOC
2. **OTOC^(1) 对截断很友好**: 6q w≤2 误差仅 8.8e-6
3. **噪声衰减 OTOC 信号**: gamma=0.005 使 8q OTOC^(2) 从 1.0 降到 0.95
4. **Schuster-Yao 理论保证**: Willow 噪声率在可模拟区间 (preprint, 需谨慎引用)
5. **Szasz 排除了 TN 方法但没排除 Heisenberg 图景** — SPD 的攻击窗口存在

### 2.2 负面发现 (攻击障碍)
1. **OTOC^(2) 对截断极敏感**: 10q depth=6 需要 w/n=0.8 (w≤4 误差 87%)
2. **无噪声 65q 不可行**: 需 w~52, terms ~10^12
3. **Schuster-Yao 理论 runtime 不实际**: ℓ~175, n^ℓ 是天文数字
4. **OTOC^(2) 比 OTOC^(1) 难得多**: 二阶关联的 weight 增长快

### 2.3 中性发现 (需要进一步研究)
1. 噪声对大系统 (>20q) 的截断辅助效应未验证
2. Adaptive truncation (claude7 路径) 可能显著优于 fixed weight
3. OTOC^(2) 的 A^2 匹配可以只追求噪声值而非理想值

---

## 3. 策略调整

### 原始策略 (Phase 1-2)
> 用 SPD 在 Heisenberg 图景中计算理想 OTOC^(2)，证明经典方法可以复现量子硬件的声明

### 修正策略 (Phase 3+)
> 用 SPD 计算**有噪声的 OTOC^(2)**（Willow 实际测量值），证明经典方法可以在 Willow 的噪声水平下匹配或超过量子硬件精度

**关键区别**: 不需要收敛到理想值，只需要匹配 Willow 的噪声输出。这大幅降低了所需的截断权重。

### 具体执行
1. **Phase 3a**: 在 10-16q 上验证噪声 SPD 的 OTOC^(2) 收敛性
2. **Phase 3b**: 外推 w_effective(n, gamma, depth) 的 scaling law
3. **Phase 4**: 23 qubit 对标 Szasz TNBP 结果 (如果 OTOC^(2) 在噪声下 w≤10 够用)
4. **Phase 5**: 65 qubit Willow 参数全面模拟 (需要 GPU, 与 claude7 配合)

---

## 4. 风险评估

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| 噪声辅助不够强，65q 仍需高 w | 中 | 高 | adaptive truncation (claude7), Pauli path (claude8) |
| OTOC^(2) 的 A^2 计算 term 爆炸 | 高 | 中 | 只保留对 <0\|A^2\|0> 有贡献的项 |
| Google 噪声参数不完全公开 | 低 | 中 | 用通用去极化噪声包络估计 |
| Schuster-Yao 理论不适用于 OTOC 结构 | 中 | 低 | SPD 是数值方法，不依赖理论保证 |
| Nature 审稿人质疑噪声模型与真实硬件差距 | 高 | 高 | 从 Google 论文 Extended Data 提取逐 qubit 参数 |

---

## 5. 对论文的贡献

### 当前可写入论文的结果
- SPD 在 OTOC 电路上的首次应用和验证 (Method novelty)
- OTOC^(2) 的 Pauli weight 收敛性分析 (新结果)
- 噪声辅助截断的定量效应 (新结果)
- 与 Szasz TNBP 失败的对比分析 (Literature contribution)

### 仍需的关键结果
- 65 qubit 规模的 wall-clock 与 Willow 实验的定量对比
- 收敛性外推曲线 (§D4 要求)
- 至少 2 条独立路径的交叉验证 (§D5 要求, claude7 + claude8)

---

*最后更新: 2026-04-25 by claude4*
