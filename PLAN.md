# Claude3 攻击计划

> 分支: `claude3` | Agent ID: `claude3` | Team: `team-modgdmq7`

## 靶标分配

| 优先级 | 靶标 | 难度 | 方法 | 状态 |
|--------|------|------|------|------|
| 主攻 | T6: Zuchongzhi 2.0/2.1 (60 qubit, 24 cycles) | ⭐⭐ | Pan-Zhang tensor contraction + runtime re-estimation | 进行中 |
| 主攻 | T4: Zuchongzhi 3.0 (83 qubit, 32 cycles) | ⭐⭐⭐ | Pauli path + tensor contraction upgrades | 待启动 |
| 辅攻 | T8: 九章 3.0 (255 photons GBS) | ⭐⭐⭐ | Oh et al. 2024 loss exploitation | 待启动 |
| 预研 | T1: Quantum Echoes (Willow 105 qubit OTOC) | ⭐⭐⭐⭐⭐ | SPD + 噪声近似 | 调研阶段 |

## 攻击路线

### T6: Zuchongzhi 2.0/2.1 (最易突破口)

**声明**: 60 qubit, 24 cycles RCS, 经典需 4.8x10^4 年 (Wu et al., PRL 127, 180501, 2021)

**反击思路**:
1. Pan & Zhang PRL 2022 的张量收缩方法已打破 Sycamore (53 qubit → 6秒)
2. Zuchongzhi 2.0 只有 60 qubit / 24 cycles，规模略大于 Sycamore 但远小于 ZCZ3.0
3. 4年来经典方法大幅进步：multi-amplitude contraction (Liu et al. PRL 2024)、GPU 集群提升
4. **核心工作**: 用最新方法重新估计 classical runtime，证明已可在合理时间完成

**具体步骤**:
- [ ] 文献调研：收集 2021-2026 所有 RCS 经典模拟改进
- [ ] 复现 Pan-Zhang 方法的 contraction order 优化
- [ ] 估算 60 qubit / 24 cycle 在当前最优方法下的 runtime
- [ ] 与原始声明对比，给出 speedup 的上下界
- [ ] 代码：实现小规模验证 (验证方法正确性)

### T4: Zuchongzhi 3.0

**声明**: 83 qubit, 32 cycles, Frontier 需 6.4x10^9 年 (Gao et al., PRL 134, 090601, 2025)

**反击思路**:
1. 继承 T6 的方法学基础设施
2. Pauli path (Schuster-Yin-Gao-Yao 2024) 理论上可处理此规模
3. Morvan phase transition 框架：分析 ZCZ3.0 是否真在"hard phase"内
4. 83x32 vs Sycamore 53x20：规模增加但方法也在增强

### T8: 九章 3.0

**声明**: 255 photons GBS, exact需 3.1x10^10 年 (Deng et al., PRL 134, 090604, 2025)

**反击思路**:
1. Oh et al. Nat. Phys. 2024 的 MPS 损耗利用方法 —— 九章系列每代都被损耗方法打破
2. Bulmer et al. 2022 的 phase-space sampler 作为辅助
3. 损耗率是关键参数：需从论文中提取实际损耗数据

### T1: Quantum Echoes (预研)

**声明**: OTOC on Willow 105 qubit, 比 Frontier TN 快 13000x (Google, Nature 2025)

**预研方向**:
1. SPD (Begusic-Gray-Chan) 尚未系统测试 OTOC
2. OTOC(2) 的双次 scramble 镜像结构 → Kremer-Dupuis unswapping?
3. 噪声下 OTOC 的经典近似路径 (Schuster-Yin-Gao-Yao 多项式时间思路)
4. Szasz et al. 2026.04 的失败案例要仔细读 —— 避免重蹈覆辙

## 目录结构

```
attacks/
  T6_zuchongzhi2/    # T6 攻击代码和结果
  T4_zuchongzhi3/    # T4 攻击代码和结果
  T8_jiuzhang3/      # T8 攻击代码和结果
  T1_quantum_echoes/ # T1 预研
results/               # 数值结果和图表
notes/                 # 决策记录和通信摘要
literature/            # 已中文献归档 (共享)
```

## 关键方法论文 (我的攻击依赖)

1. Pan & Zhang, PRL 129, 090502 (2022) — 打破 Sycamore 的张量收缩
2. Liu et al., PRL 132, 030601 (2024) — Multi-amplitude tensor contraction
3. Schuster, Yin, Gao, Yao, arXiv:2407.12768 (2024) — Pauli path 噪声稀疏性
4. Oh et al., Nat. Phys. 20, 1647 (2024) — GBS 经典欺骗 (MPS+损耗)
5. Begusic, Gray, Chan, SA 10, eadk4321 (2024) — SPD
6. Morvan et al., Nature 634, 328 (2024) — RCS phase transition
7. Szasz et al., arXiv:2604.15427 (2026) — Quantum Echoes 反击失败案例

---

*创建: 2026-04-25 | 最后更新: 2026-04-25*
