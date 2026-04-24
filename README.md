# 未被打破的量子优势声明与可能的反击切入点

> **工作规范见 [`AGENTS.md`](./AGENTS.md)：怎么打 + 打到什么程度。本文档是"打什么"。**

> **本表聚焦：仍"活着"的顶刊声明 + 其弱点分析 + 潜在反击方法**  
> 已被完全打破（🔴）的声明不在本表讨论范围——它们是历史，不是机会。

> **状态说明**  
> - 🟢 **未被打破**：尚无成功反击  
> - 🟡 **Challenged（部分挑战）**：已有反击但未完全追平，仍有空间可扩展反击  

> **期刊标识**：NAT = Nature；SCI = Science；NP = Nature Physics；NPJ-QI = npj Quantum Information；PRL = Physical Review Letters；PRX = Physical Review X；PRXQ = PRX Quantum；PRR = Physical Review Research；SA = Science Advances；SB = Science Bulletin

---

## 🎯 第一梯队：最热、最稳、尚无成功反击（最高难度靶标）

### T1. Google Quantum Echoes (OTOC on Willow) 🟢

| 字段 | 内容 |
|---|---|
| **论文** | Google Quantum AI, **Nature** (2025), DOI: 10.1038/s41586-025-09526-6 |
| **时间 / 硬件** | 2025.10 发表 / Willow 105 qubit |
| **声明核心** | 首个"可验证"量子优势；second-order OTOC ≡ Quantum Echoes；65 qubit 测量比 Frontier 经典 TN 快 13,000 倍（2.1 小时 vs 3.2 年）；应用于 NMR 分子几何（15 原子 & 28 原子分子） |
| **已有反击尝试** | Szasz et al., **arXiv:2604.15427 (2026.04)**："Tensor Networks with Belief Propagation Cannot Feasibly Simulate Google's Quantum Echoes Experiment" — **尝试反击失败**；TNBP 证明不可行，反而**加强**了 Google 声明 |
| **弱点 / 反击切入点** | ① Willow 硬件噪声：实验 fidelity 并非 1，**噪声下的 OTOC 可能有经典近似路径**（类似 Schuster-Yin-Gao-Yao 的多项式时间思路）<br>② OTOC(2) 使用了"双次 scramble"，镜像/时间反演结构——是否可用 Kremer-Dupuis 的 unswapping 思路？<br>③ 分子几何应用（15/28 原子）有限规模——针对这类小分子能否用量子化学方法（DMRG/CCSD(T)）直接匹敌？<br>④ OTOC 作为 observable 本质是 Heisenberg 图景算符期望值——**Sparse Pauli Dynamics (SPD)** 尚未系统测试过此问题 |
| **攻击难度** | ⭐⭐⭐⭐⭐（极难）|
| **论文潜在影响** | Nature 级 |

---

### T2. Algorithmiq Heterogeneous Materials 🟢

| 字段 | 内容 |
|---|---|
| **论文** | arXiv + Quantum Advantage Tracker submission (2025.11)；IBM Quantum Developer Conference 宣布 |
| **时间 / 硬件** | 2025.11 / IBM Heron 133 qubit |
| **声明核心** | 异质量子材料的算子动力学模拟；**Flatiron Institute 独立验证经典困难性**；模型具有不同区域的局部性质，无序+不规则连接性支配信息流动 |
| **已有反击尝试** | 目前追踪器上尚无成功反击；Flatiron 自己就是经典模拟权威，已验证过经典方法难以处理 |
| **弱点 / 反击切入点** | ① 模型由 Algorithmiq 设计——**设计是否存在隐藏的可利用结构**？（类似 BlueQubit peaked circuits 被 unswapping 打破）<br>② 异质性 + 无序 = 可能存在局域化区域，**Neural Quantum States (NQS) 可能在某些参数区间表现良好**<br>③ 算子动力学 → observable estimation → SPD 类方法可能适用<br>④ 由于是新设计的模型，**PEPS + belief propagation 的效果**尚未被完整测试 |
| **攻击难度** | ⭐⭐⭐⭐（困难）|
| **论文潜在影响** | PRX Quantum / Science Advances 级 |

---

### T3. D-Wave "Beyond-Classical" 🟡（已有部分挑战，可扩展）

| 字段 | 内容 |
|---|---|
| **论文** | King et al., **Science 388, 199** (2025), "Beyond-classical computation in quantum simulation"；arXiv:2403.00910 |
| **时间 / 硬件** | 2025.03 / D-Wave Advantage2 prototype (up to ~3200 qubits) |
| **声明核心** | 二维、三维、无限维自旋玻璃的淬火动力学；声称 MPS、PEPS、NQS 均无法在合理时间内达到相同精度 |
| **已有反击尝试** | ① **Sels et al., NYU 2025**：笔记本 2 小时完成类似问题（54 qubit），**部分挑战**<br>② **Mauron & Carleo, EPFL 2025**（arXiv:2503.08247）：t-VMC + Jastrow-Feenberg 波函数，4 GPU 3 天，128 qubit 3D diamond lattice，误差 <7%<br>③ Flatiron 另有张量网络论文挑战<br>④ D-Wave 已正式回应，**维护声明**，并扩展到 3200 qubit |
| **弱点 / 反击切入点** | ① **退火机动力学本质上是 annealing path 依赖的**——经典 Monte Carlo + variational 方法可能比 TN 更合适<br>② Mauron-Carleo 的方法**可推广**：从 128 qubit 拓展到更大系统是明确的未完成工作<br>③ 三维拓扑是难点，但 **PEPS with auxiliary bonds** 尚未完全优化<br>④ D-Wave 声明的"3D 尤其难"——是否所有 3D 拓扑都难？找到特定拓扑可被经典模拟<br>⑤ 声明的"长退火时间"区间可能**反而更接近热平衡态**，经典可模拟 |
| **攻击难度** | ⭐⭐⭐（中等，**已有明确突破口**）|
| **论文潜在影响** | PRL / Nature Physics 级 |

---

## 🎯 第二梯队：中等难度、未被完全反驳

### T4. USTC Zuchongzhi 3.0 🟢

| 字段 | 内容 |
|---|---|
| **论文** | Gao et al., **PRL 134, 090601** (2025), "Establishing a New Benchmark in Quantum Computational Advantage with 105-qubit Zuchongzhi 3.0" |
| **时间 / 硬件** | 2025.03 / 超导 105 qubit（实验 83 qubit, 32 cycles）|
| **声明核心** | Frontier 需 6.4×10⁹ 年；比 Google SYC-67/70 高 6 个数量级；fidelity：1Q 99.90%、2Q 99.62%、readout 99.13% |
| **已有反击尝试** | 无（刚发表一年）|
| **弱点 / 反击切入点** | ① RCS 历来是经典方法的"主场"——**张量收缩 + XEB 验证**（Pan-Zhang 2022 方法）可以**直接升级**<br>② 83 qubit × 32 cycle 仍在 Pauli path 算法的理论可处理区间（Schuster-Yin-Gao-Yao 2024）<br>③ **Sycamore 的 6 秒下场**是最强提示：RCS 声明被打破是**历史常态**，不是例外<br>④ Nvidia / Cerebras 大规模 GPU 集群 + tensor contraction 算法的改进持续在发生<br>⑤ Morvan 的 phase transition 框架指出 RCS 有"弱噪声相"边界——可分析 Zuchongzhi 3.0 是否真的在该相内 |
| **攻击难度** | ⭐⭐⭐（中等）|
| **论文潜在影响** | PRL 级 |

---

### T5. Google Willow RCS 🟡

| 字段 | 内容 |
|---|---|
| **论文** | Google Quantum AI, **Nature 638, 920** (2025) — Willow 论文中 RCS 部分 |
| **时间 / 硬件** | 2024.12 / Willow 105 qubit |
| **声明核心** | 5 分钟完成经典 10²⁵ 年的 RCS 任务 |
| **已有反击尝试** | Multiverse / DIPC 2024-2025 用 gPEPS 部分挑战 |
| **弱点 / 反击切入点** | ① 同 T4（RCS 通用弱点）<br>② RCS 任务子规模相比 Zuchongzhi 3.0 略小（Willow RCS 部分所用 qubit × cycle 低于 ZCZ3.0 的 83 qubit × 32 cycle 配置），经典攻击窗口更宽<br>③ Willow 主要卖点是 QEC，其 RCS 部分并非论文核心——**可能 Google 自己没有优化到极致** |
| **攻击难度** | ⭐⭐⭐（中等）|
| **论文潜在影响** | PRL / Nature 级 |

---

### T6. USTC Zuchongzhi 2.0 / 2.1 🟡

| 字段 | 内容 |
|---|---|
| **论文** | Wu et al., **PRL 127, 180501**（2.0）；Zhu et al., **Sci. Bull. 67, 240**（2.1）|
| **时间 / 硬件** | 2021 / 超导 60 qubit, 24 cycles |
| **声明核心** | 比 Sycamore 难 6 个数量级，需经典 4.8×10⁴ 年 |
| **已有反击尝试** | Morvan et al., **Nature 634, 328 (2024)** 间接削弱；但至今无完整反驳 |
| **弱点 / 反击切入点** | ① 已过去 4 年，**经典方法大幅进步**（2022 Pan-Zhang 等）——用当前最好方法重新估计 classical runtime<br>② Sycamore 的经验：从 "10,000 年" 到 "6 秒" 只用了 5 年——类似命运极有可能<br>③ 比 Zuchongzhi 3.0 规模更小，**先从小目标下手** |
| **攻击难度** | ⭐⭐（容易）|
| **论文潜在影响** | PRL 级 |

---

### T7. USTC 九章 4.0 🟢

| 字段 | 内容 |
|---|---|
| **论文** | arXiv:2508.09092 (预印本) "Robust quantum computational advantage with programmable 3050-photon Gaussian boson sampling" |
| **时间 / 硬件** | 2025 / 光量子，1024 squeezed states, 8176 modes, 3050 photons |
| **声明核心** | 专门设计用于**对抗 MPS 经典欺骗方法**（Oh et al. Nat. Phys. 2024 是其主要防御目标）；利用混合时空编码 |
| **已有反击尝试** | 无（刚出现）|
| **弱点 / 反击切入点** | ① 声明明确说**用来对抗 MPS 方法**——但经典模拟不止 MPS，**其他方法（如 Bulmer's phase-space samplers、neural classical samplers）可能绕过此防御**<br>② 3050 photons 规模极大，但**光子损耗依然是攻击点**——Oh et al. 方法的核心是利用损耗<br>③ 是否真正实现了"robust"？需要独立验证<br>④ 预印本，非顶刊正式发表，**如有严重问题可快速质疑** |
| **攻击难度** | ⭐⭐⭐（中等）|
| **论文潜在影响** | Nature Physics / Science Advances 级 |

---

### T8. USTC 九章 3.0 🟡

| 字段 | 内容 |
|---|---|
| **论文** | Deng et al., **PRL 134, 090604** (2025) "GBS with Pseudo-Photon-Number Resolving Detectors and Quantum Computational Advantage" |
| **时间 / 硬件** | 2023 arXiv → 2025 正式 / 光量子 255 photons |
| **声明核心** | Frontier exact 需 3.1×10¹⁰ 年；样本 1.27 μs |
| **已有反击尝试** | 经典损耗模拟（Oh et al. 方法）在推进中但未完整反驳 |
| **弱点 / 反击切入点** | ① 同所有 GBS 声明的通用弱点：**损耗→经典易模拟**<br>② Oh et al. **Nat. Phys. 20, 1647 (2024)** 方法可直接适配<br>③ 九章系列历来**每一版都被后续打破**（1.0 被 Bulmer，2.0 被 Oh）——3.0 时间上已到"被打破的窗口期"|
| **攻击难度** | ⭐⭐⭐（中等）|
| **论文潜在影响** | PRL / Nature Physics 级 |

---

### T9. IBM Nighthawk 实验 🟢

| 字段 | 内容 |
|---|---|
| **论文** | IBM announcement (2025.11)，论文待发表 |
| **时间 / 硬件** | 2025.11 / IBM Nighthawk 120 qubit，218 耦合器，square lattice |
| **声明核心** | 支持 5000 个 2-qubit gates，路线图目标 2026 年底前 verified quantum advantage |
| **已有反击尝试** | 无（硬件刚发布）|
| **弱点 / 反击切入点** | ① 未来可能的声明问题最可能是**某种 utility 或 observable estimation**，类似 IBM Eagle 套路<br>② IBM Eagle 的经验：**发布当月就有打破论文**（Tindall/Begušić 等）——可以**预设**打破框架，等实验发布后立即响应<br>③ Square lattice + heavy-hex 的几何特征**完全契合 gPEPS/belief propagation** 方法 |
| **攻击难度** | ⭐⭐⭐（中等，待实验公布）|
| **论文潜在影响** | 取决于具体声明 |

---

## 📚 第三部分：经典反击方法工具箱（按攻击目标匹配）

| 方法 | 代表工作 | 最适合攻击的目标（本表编号）|
|---|---|---|
| **Tensor Network + Belief Propagation** | Tindall et al., **PRXQ 5, 010308 (2024)** | T3 (D-Wave)、T9 (IBM Nighthawk) |
| **gPEPS (Graph-based PEPS)** | Patra et al., **PRR 6, 013326 (2024)**；Jahromi & Orús, **PRB 99, 195105 (2019)** | T3、T4、T5、T9 |
| **Sparse Pauli Dynamics (SPD)** | Begušić, Gray, Chan, **SA 10, eadk4321 (2024)**；Begušić & Chan, **PRXQ 6, 020302 (2025)** | T1 (Quantum Echoes)、T2 (Algorithmiq)、T9 |
| **Pauli Path + 噪声稀疏性（理论）** | Schuster, Yin, Gao, Yao, arXiv:2407.12768 (2024) | T1、T2 |
| **Tensor Network RCS Contraction** | Pan & Zhang, **PRL 129, 090502 (2022)**；Liu et al., **NCS 1, 578 (2021)** | T4、T5、T6 |
| **Multi-amplitude Tensor Contraction** | Liu et al., **PRL 132, 030601 (2024)** | T4、T5、T6 |
| **t-VMC + Jastrow-Feenberg NQS** | Mauron & Carleo (EPFL) 2025 | T3 (已打破部分) |
| **MPO Heisenberg Evolution** | Anand, Temme, Kandala, Zaletel, arXiv:2306.17839 (2023) | T2、T9 |
| **Boson Sampling 损耗利用** | Oh, Lim, Fefferman, Jiang, **Nat. Phys. 20, 1647 (2024)**；Bulmer et al., **SA 8, eabl9236 (2022)** | T7、T8 |
| **Unswapping / Mirror Symmetry** | Kremer & Dupuis (IBM) 2026 | T1（OTOC 有时间反演结构，可尝试）|
| **Neural Quantum States** | Carleo & Troyer, **Science 355, 602 (2017)** | T3、T2 |

---

## 📖 第四部分：必读文献

### 反击方法核心论文
- Tindall et al., **PRX Quantum 5, 010308** (2024) — 打破 IBM Eagle 模板
- Begušić, Gray, Chan, **Science Advances 10, eadk4321** (2024) — SPD 打破 IBM Eagle
- Patra et al., **Phys. Rev. Research 6, 013326** (2024) — gPEPS 扩展
- Pan, Chen, Zhang, **PRL 129, 090502** (2022) — 打破 Sycamore 模板
- Bulmer et al., **Science Advances 8, eabl9236** (2022) — 打破 Jiuzhang 模板
- Oh et al., **Nature Physics 20, 1647** (2024) — GBS 经典欺骗
- Kremer & Dupuis, arXiv:2604.21908 (2026) — 最新打破模板（peaked circuits）
- Szasz et al., arXiv:2604.15427 (2026.04) — **反击失败的重要案例**（Quantum Echoes）
- Schuster, Yin, Gao, Yao, arXiv:2407.12768 (2024) — 噪声量子线路多项式算法理论

### 综述与元分析
- Hariprakash et al., arXiv:2412.14703 (2024) — 量子 vs 经典优势完整年表
- Xu et al., **Sci. Bull.** / arXiv:2302.08880 — 经典模拟方法综述
- Google Quantum AI, arXiv:2511.09124 (2025) — "Grand Challenge" perspective

### 当前仍活的量子声明原始论文
- Google Quantum AI, **Nature** (2025), DOI:10.1038/s41586-025-09526-6 — Quantum Echoes
- King et al., **Science 388, 199** (2025) — D-Wave beyond-classical
- Google Quantum AI, **Nature 638, 920** (2025) — Willow
- Gao et al., **PRL 134, 090601** (2025) — Zuchongzhi 3.0
- Deng et al., **PRL 134, 090604** (2025) — Jiuzhang 3.0
- arXiv:2508.09092 (2025) — Jiuzhang 4.0
- Algorithmiq 异质材料论文（Tracker 上可查）

### Quantum Advantage Tracker
- https://quantum-advantage-tracker.github.io/（实时追踪所有提交与反击）

---

*最后更新：2026 年 4 月 24 日*
