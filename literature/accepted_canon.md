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

<!-- 模板，添加条目时复制一份并取消注释：
### <短标题：第一作者 + 年份>
- **引用**：Tindall et al., PRX Quantum 5, 010308 (2024)
- **DOI**：10.1103/PRXQuantum.5.010308
- **arXiv**：2306.17839
- **子领域**：张量网络经典模拟
- **关键方法**：Tensor Network + Belief Propagation
- **已用于反查的目标**：T3 (D-Wave), T9 (IBM Nighthawk)
- **关联审查意见 ID**：REV-20260424-T3-001
- **一句话要点**：在 heavy-hex 几何上，TN+BP 可以以多项式代价达到与 IBM Eagle utility 实验同量级精度——任何 heavy-hex / square lattice 的新量子声明都必须先排除这个基线。
-->

### Pan & Zhang 2022
- **引用**：Pan & Zhang, PRL 129, 090502 (2022)
- **DOI**：10.1103/PhysRevLett.129.090502
- **arXiv**：2103.03074
- **子领域**：RCS 经典模拟
- **关键方法**：Tensor Network RCS Contraction
- **已用于反查的目标**：T4 (ZCZ 3.0), T5 (Willow RCS), T6 (ZCZ 2.0/2.1)
- **关联审查意见 ID**：（待生成）
- **一句话要点**：张量收缩方法在 Sycamore 53q/20c 上实现 6 秒经典模拟，打破首个 RCS 量子优势声明——所有后续 RCS 声明必须证明超出此方法的可扩展极限。

### Liu et al. 2024
- **引用**：Liu et al., PRL 132, 030601 (2024)
- **DOI**：10.1103/PhysRevLett.132.030601
- **arXiv**：2304.11573
- **子领域**：RCS 经典模拟
- **关键方法**：Multi-amplitude Tensor Contraction
- **已用于反查的目标**：T4 (ZCZ 3.0), T5 (Willow RCS), T6 (ZCZ 2.0/2.1)
- **关联审查意见 ID**：（待生成）
- **一句话要点**：多振幅张量收缩在超算上实现 Sycamore 规模 300 万精确振幅计算，为更大规模 RCS 经典模拟提供可扩展框架。

### ~~Schuster, Yin, Gao & Yao 2025~~ — REMOVED (arXiv-only)
<!-- ERRATUM (2026-04-25): claude2 hallucinated DOI "10.1103/PRXQuantum.15.041018".
     Verified by claude6+claude8 via WebFetch: HTTP 404. Paper is arXiv-only (2407.12768).
     Removed per accepted_canon policy: "预印本（arXiv-only）不进入本清单".
     The paper IS cited in attack plans but does NOT qualify for accepted_canon. -->


### Morvan et al. 2024
- **引用**：Morvan et al., Nature 634, 328 (2024)
- **DOI**：10.1038/s41586-024-07998-6
- **arXiv**：2304.11119
- **子领域**：RCS 相变分析
- **关键方法**：Phase Transition Framework
- **已用于反查的目标**：T4 (ZCZ 3.0), T5 (Willow RCS), T6 (ZCZ 2.0/2.1)
- **关联审查意见 ID**：（待生成）
- **一句话要点**：RCS 存在噪声驱动的相变——强噪声相中量子输出退化为不关联子系统的乘积，可高效经典模拟。ZCZ 系列的低 XEB fidelity 可能处于此相。

### Oh et al. 2024
- **引用**：Oh, Lim, Fefferman, Jiang, Nature Physics 20, 1647 (2024)
- **DOI**：10.1038/s41567-024-02596-3
- **arXiv**：2306.03709
- **子领域**：GBS 经典模拟
- **关键方法**：Boson Sampling 损耗利用
- **已用于反查的目标**：T7 (九章 4.0), T8 (九章 3.0)
- **关联审查意见 ID**：（待生成）
- **一句话要点**：光子损耗使 GBS 可被 MPS 高效经典模拟——九章系列每一代都在此方法的攻击范围内。

### Gao et al. 2025 (ZCZ 3.0 原始论文)
- **引用**：Gao et al., PRL 134, 090601 (2025)
- **DOI**：10.1103/PhysRevLett.134.090601
- **arXiv**：2304.02199
- **子领域**：RCS 量子优势声明
- **关键方法**：Random Circuit Sampling
- **已用于反查的目标**：T4 (ZCZ 3.0)
- **关联审查意见 ID**：（待生成）
- **一句话要点**：T4 攻击靶标原始论文——声称 Frontier 需 6.4x10^9 年，83q/32c，fidelity 1Q:99.90% 2Q:99.62% readout:99.13%。

### Deng et al. 2025 (九章 3.0 原始论文)
- **引用**：Deng et al., PRL 134, 090604 (2025)
- **DOI**：10.1103/PhysRevLett.134.090604
- **子领域**：GBS 量子优势声明
- **关键方法**：Gaussian Boson Sampling
- **已用于反查的目标**：T8 (九章 3.0)
- **关联审查意见 ID**：（待生成）
- **一句话要点**：T8 攻击靶标原始论文——255 photons, Frontier exact 需 3.1x10^10 年。
