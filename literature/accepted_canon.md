# 已中顶刊文献归档（accepted_canon）

> 本文件由 `AGENTS.md` 目标 2 强制要求维护。  
> 所有用于"反查当前文献"的**已被顶刊正式接收**的论文在此归档（Nature / Science / PRL / PRX / NP / PRXQ / SA / SB / NPJ-QI / PRR 等）。预印本（arXiv-only）不进入本清单，除非同时已 accept。

---

## 使用约定

- **添加时机**：任何智能体在审查或反击过程中引用一篇已中文献作为依据时，必须把它按下方模板登记到本文件。
- **添加流程**：先在自己分支里登记 → commit + push（铁律 5）→ 发 PR 合入 main。
- **去重**：同一 DOI 仅一条记录；后续智能体若扩展其"已用于反查的目标"字段，就地 append 不新增条目。
- **删除**：仅在论文被撤稿（retracted）时标注 `⚠️ RETRACTED`，不物理删除条目。

---

## 字段 schema（每条记录必备）

| 字段 | 说明 |
|---|---|
| **引用** | `作者 et al., 期刊 卷, 起始页 (年份)` 格式 |
| **DOI** | 完整 DOI，可点开验证（不允许 arXiv-only） |
| **arXiv**（可选） | 对应预印本 ID，便于追溯版本 |
| **子领域** | RCS / GBS / annealing / OTOC / NISQ utility / QEC / … |
| **关键方法** | 与 `README.md` 第三部分"经典反击方法工具箱"对齐的方法名 |
| **已用于反查的目标** | `README.md` 的 T1–T9 编号，可多选 |
| **关联审查意见 ID** | 本项目产出的审查记录编号（形如 `REV-YYYYMMDD-T#-NNN`） |
| **一句话要点** | 本论文能用来"反查"什么（方法、结论、或标准） |

---

## 条目（按 DOI 字母/数字序排列）

### #1 Begušić, Gray & Chan 2024 (SPD 打破 IBM Eagle)
- **引用**: Begušić T, Gray J, Chan GK-L, Science Advances 10, eadk4321 (2024)
- **DOI**: 10.1126/sciadv.adk4321
- **arXiv**: 2308.05077
- **子领域**: NISQ utility / 经典模拟
- **关键方法**: Sparse Pauli Dynamics (SPD)
- **已用于反查的目标**: T1 (Quantum Echoes), T2 (Algorithmiq), T9 (IBM Nighthawk)
- **关联审查意见 ID**: —
- **一句话要点**: SPD 在单核笔记本上比 IBM Eagle 127-qubit 实验快数个数量级——任何基于 Heisenberg 图景 observable estimation 的新量子声明都必须先排除 SPD 基线。

### #2 Begušić & Chan 2025 (SPD 2D/3D 算符演化)
- **引用**: Begušić T, Chan GK-L, PRX Quantum 6, 020302 (2025)
- **DOI**: 10.1103/PRXQuantum.6.020302
- **arXiv**: 2409.03097
- **子领域**: 经典模拟 / 算符动力学
- **关键方法**: Sparse Pauli Dynamics (SPD)
- **已用于反查的目标**: T1 (Quantum Echoes), T2 (Algorithmiq)
- **关联审查意见 ID**: —
- **一句话要点**: SPD 在 2D/3D 横场 Ising quench 动力学上与最先进 TN 方法竞争——证明 SPD 不限于 1D，可用于 2D 格子上的算符演化（与 Willow 2D 架构直接相关）。

### #3 Bulmer et al. 2022 (GBS 经典模拟)
- **引用**: Bulmer JFF et al., Science Advances 8, eabl9236 (2022)
- **DOI**: 10.1126/sciadv.abl9236
- **arXiv**: 2109.06957
- **子领域**: GBS / 经典模拟
- **关键方法**: Phase-space classical sampler
- **已用于反查的目标**: T7 (九章 4.0), T8 (九章 3.0)
- **关联审查意见 ID**: —
- **一句话要点**: 相空间经典采样器打破九章 1.0 的 GBS 量子优势声明——九章系列每一代都有被经典方法打破的先例，4.0 专门防御的是 Oh 方法而非 Bulmer 方法。

### #4 Liu et al. 2024 (Multi-amplitude TN)
- **引用**: Liu et al., PRL 132, 030601 (2024)
- **DOI**: 10.1103/PhysRevLett.132.030601
- **arXiv**: 2304.11573
- **子领域**: RCS 经典模拟
- **关键方法**: Multi-amplitude Tensor Contraction
- **已用于反查的目标**: T4 (ZCZ 3.0), T5 (Willow RCS), T6 (ZCZ 2.0/2.1)
- **关联审查意见 ID**: —
- **一句话要点**: 多振幅张量收缩在超算上实现 Sycamore 规模精确振幅计算，为更大规模 RCS 经典模拟提供可扩展框架。

### #5 Morvan et al. 2024 (RCS 相变)
- **引用**: Morvan et al., Nature 634, 328 (2024)
- **DOI**: 10.1038/s41586-024-07998-6
- **arXiv**: 2304.11119
- **子领域**: RCS 相变分析
- **关键方法**: Phase Transition Framework
- **已用于反查的目标**: T4 (ZCZ 3.0), T5 (Willow RCS), T6 (ZCZ 2.0/2.1)
- **关联审查意见 ID**: —
- **一句话要点**: RCS 存在噪声驱动的相变——强噪声相中量子输出退化为不关联子系统的乘积，可高效经典模拟。

### #6 Oh et al. 2024 (GBS 经典欺骗)
- **引用**: Oh C, Lim Y, Fefferman B, Jiang L, Nature Physics 20, 1647 (2024)
- **DOI**: 10.1038/s41567-024-02535-8
- **arXiv**: —
- **子领域**: GBS / 经典模拟
- **关键方法**: Boson Sampling 损耗利用
- **已用于反查的目标**: T7 (九章 4.0), T8 (九章 3.0)
- **关联审查意见 ID**: —
- **一句话要点**: 利用光子损耗构造 MPS 经典采样器，打破了此前的 GBS 量子优势声明——九章系列每一版都有被打破的先例。

### #7 Pan & Zhang 2022 (TN 收缩打破 Sycamore)
- **引用**: Pan F, Zhang P, PRL 129, 090502 (2022)
- **DOI**: 10.1103/PhysRevLett.129.090502
- **arXiv**: 2111.03011
- **子领域**: RCS / 经典模拟
- **关键方法**: Tensor Network RCS Contraction
- **已用于反查的目标**: T4 (ZCZ 3.0), T5 (Willow RCS), T6 (ZCZ 2.0/2.1)
- **关联审查意见 ID**: —
- **一句话要点**: 经典 TN 收缩将 Sycamore 53-qubit RCS 从"10000年"降至可行范围——RCS 声明被打破是历史常态，此方法可直接升级。

### #8 Schuster, Yin, Gao & Yao 2025 (噪声多项式算法)
- **引用**: Schuster T, Yin C, Gao X, Yao NY, PRX 15, 041018 (2025)
- **DOI**: 10.1103/PhysRevX.15.041018
- **arXiv**: 2407.12768
- **子领域**: RCS / OTOC 经典模拟（理论）
- **关键方法**: Pauli Path + 噪声稀疏性
- **已用于反查的目标**: T1 (Quantum Echoes), T4 (ZCZ 3.0), T6 (ZCZ 2.0/2.1)
- **关联审查意见 ID**: —
- **一句话要点**: 证明在常数去极化噪声下任何量子电路的期望值可在拟多项式时间内经典计算——Willow 噪声率 γ~0.005 远超理论阈值 log²(n)/n。

### #9 Tindall et al. 2024 (TN+BP 打破 IBM Eagle)
- **引用**: Tindall J et al., PRX Quantum 5, 010308 (2024)
- **DOI**: 10.1103/PRXQuantum.5.010308
- **arXiv**: 2306.17839
- **子领域**: NISQ utility / 张量网络
- **关键方法**: Tensor Network + Belief Propagation
- **已用于反查的目标**: T3 (D-Wave), T9 (IBM Nighthawk)
- **关联审查意见 ID**: —
- **一句话要点**: 在 heavy-hex 几何上，TN+BP 可以以多项式代价达到与 IBM Eagle utility 实验同量级精度——任何 heavy-hex / square lattice 的新量子声明都必须先排除这个基线。

---

*合并版 v2：claude4 (5条) + claude2 (Liu/Morvan/Schuster-Yin) + claude8 (Bulmer) = 9 unique entries*
*§5.2 投票: claude1 ✅, claude2 ✅, claude3 ✅, claude5 ✅, claude6 ✅, claude7 ✅*
*最后更新: 2026-04-25 by claude4 (merge lead)*
