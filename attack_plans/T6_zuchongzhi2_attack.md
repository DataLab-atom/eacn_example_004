# T6 攻击方案：USTC Zuchongzhi 2.0 / 2.1 经典模拟反击

> 负责人: claude1 | 分支: claude1 | 难度: ⭐⭐ | 状态: 🟡→🔴 目标

## 1. 靶标概要

- **原始论文**:
  - Wu et al., PRL 127, 180501 (2021) — Zuchongzhi 2.0
  - Zhu et al., Sci. Bull. 67, 240 (2022) — Zuchongzhi 2.1
- **硬件**: 超导 60 qubit, 24 cycles
- **声明**: 比 Sycamore 难 6 个数量级，需经典 4.8x10^4 年
- **现状**: 🟡 Challenged — Morvan et al. Nature 634, 328 (2024) 间接削弱，但无完整反驳

## 2. 已有反击方法（可复用）

| 方法 | 论文 | 关键参数 | 适用性 |
|---|---|---|---|
| 张量收缩 | Pan & Zhang, PRL 129, 090502 (2022) | 打破 Sycamore 53q/20c → 6秒 | **直接适用**，规模更大但方法相同 |
| 多振幅张量收缩 | Liu et al., PRL 132, 030601 (2024) | 批量采样加速 | 高度适用 |
| Pauli path (噪声) | Schuster et al., arXiv:2407.12768 (2024) | 多项式时间理论保证 | 需验证 60q/24c 是否在可行域 |
| 相变框架 | Morvan et al., Nature 634, 328 (2024) | RCS 弱噪声相边界 | 分析 ZCZ 2.0 参数位置 |

## 3. 攻击策略

### 路线 A: 张量网络收缩 (主攻)
1. 用 quimb + cotengra 构建 60-qubit, 24-cycle RCS 张量网络
2. 使用 Pan-Zhang 优化的收缩路径 (slicing + contraction ordering)
3. 在 RTX 4060 上估算 wall-clock time
4. 与原始声明的 "4.8x10^4 年" 进行对比
5. 关键: 使用 XEB (cross-entropy benchmark) 作为 fidelity 验证指标

### 路线 B: Pauli Path 噪声利用 (辅攻)
1. 实现 Schuster-Yin-Gao-Yao 的多项式时间算法
2. 利用 ZCZ 2.0 的实际噪声参数 (1Q: ~99.86%, 2Q: ~99.41%)
3. 分析 60q x 24c 是否落入 "可高效模拟" 相

### 路线 C: 经典 runtime 重新估计
1. 用 2024-2026 最新 GPU (H100/B200) 基准重新估计
2. 算法改进 (contraction ordering, mixed precision) 的加速比
3. 产出: 新的 classical runtime 上界，对比原始声明

## 4. 预期产出

- [ ] 可复现的张量网络收缩代码 (quimb/cotengra)
- [ ] 60-qubit RCS 的 classical runtime 新上界
- [ ] XEB fidelity 匹配验证
- [ ] 与 Sycamore 打破案例的系统对比
- [ ] accepted_canon.md 更新

## 5. 时间节点

- Phase 1: 方法实现 + 小规模验证 (20-30 qubit)
- Phase 2: 60 qubit 全规模运行 + 性能分析
- Phase 3: 结果整理 + 论文素材输出

## 6. 风险与备选

- 风险: RTX 4060 (8GB) 可能不够跑 60-qubit 全规模收缩
- 备选: 降低采样数但保证 fidelity; 或使用 CPU 大内存路径
- 备选: 先从 ZCZ 2.0 的子集 (53 qubit) 开始，与 Sycamore 基准对齐

---
*创建时间: 2026-04-25 | claude1*
