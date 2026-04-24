# 已中顶刊文献归档（accepted_canon）

> 本文件由 `AGENTS.md` 目标 2 强制要求维护。  
> 所有用于"反查当前文献"的**已被顶刊正式接收**的论文在此归档（Nature / Science / PRL / PRX / NP / PRXQ / SA / SB / NPJ-QI / PRR 等）。预印本（arXiv-only）不进入本清单，除非同时已 accept。

---

## 使用约定

- **添加时机**：任何智能体在审查或反击过程中引用一篇已中文献作为依据时，必须把它按下方模板登记到本文件。
- **添加流程**：先在自己分支里登记 -> commit + push（铁律 5）-> 发 PR 合入 main。
- **去重**：同一 DOI 仅一条记录；后续智能体若扩展其"已用于反查的目标"字段，就地 append 不新增条目。
- **删除**：仅在论文被撤稿（retracted）时标注 `RETRACTED`，不物理删除条目。

---

## 字段 schema（每条记录必备）

| 字段 | 说明 |
|---|---|
| **引用** | `作者 et al., 期刊 卷, 起始页 (年份)` 格式 |
| **DOI** | 完整 DOI，可点开验证（不允许 arXiv-only） |
| **arXiv**（可选） | 对应预印本 ID，便于追溯版本 |
| **子领域** | RCS / GBS / annealing / OTOC / NISQ utility / QEC / ... |
| **关键方法** | 与 `README.md` 第三部分"经典反击方法工具箱"对齐的方法名 |
| **已用于反查的目标** | `README.md` 的 T1-T9 编号，可多选 |
| **关联审查意见 ID** | 本项目产出的审查记录编号（形如 `REV-YYYYMMDD-T#-NNN`） |
| **一句话要点** | 本论文能用来"反查"什么（方法、结论、或标准） |

---

## 条目（按 DOI 字母/数字序排列）

### Pan & Zhang 2022
- **引用**: Pan & Zhang, PRL 129, 090502 (2022)
- **DOI**: 10.1103/PhysRevLett.129.090502
- **arXiv**: 2111.03011
- **子领域**: RCS 张量网络经典模拟
- **关键方法**: Tensor Network RCS Contraction
- **已用于反查的目标**: T4, T5, T6
- **关联审查意见 ID**: --
- **一句话要点**: 用张量收缩在 Frontier 级集群上 304 秒完成 Sycamore 53-qubit RCS 采样——任何后续 RCS 声明必须与此方法的最新升级版对比，而非与 2019 年基线对比。

### Liu et al. 2024 (Multi-amplitude)
- **引用**: Liu et al., PRL 132, 030601 (2024)
- **DOI**: 10.1103/PhysRevLett.132.030601
- **arXiv**: 2304.09587
- **子领域**: RCS 张量网络经典模拟
- **关键方法**: Multi-amplitude Tensor Contraction
- **已用于反查的目标**: T4, T5, T6
- **关联审查意见 ID**: --
- **一句话要点**: 多振幅同时收缩可将 RCS 经典模拟提速数量级——T4/T5/T6 的 classical runtime 估计若未考虑此方法则自动过时。

### Oh et al. 2024
- **引用**: Oh, Lim, Fefferman, Jiang, Nat. Phys. 20, 1647 (2024)
- **DOI**: 10.1038/s41567-024-02535-8
- **arXiv**: 2306.03709
- **子领域**: GBS 经典模拟
- **关键方法**: Boson Sampling 损耗利用
- **已用于反查的目标**: T7, T8
- **关联审查意见 ID**: --
- **一句话要点**: 利用光子损耗构造 MPS 经典欺骗算法，已打破九章 2.0——九章 3.0/4.0 的损耗率若未显著改善则面临同样攻击。

### Bulmer et al. 2022
- **引用**: Bulmer et al., SA 8, eabl9236 (2022)
- **DOI**: 10.1126/sciadv.abl9236
- **arXiv**: 2109.11525
- **子领域**: GBS 经典模拟
- **关键方法**: Boson Sampling 损耗利用 (phase-space)
- **已用于反查的目标**: T7, T8
- **关联审查意见 ID**: --
- **一句话要点**: 九章 1.0 的 Gaussian 态在有损情况下可被 phase-space 采样器经典复现——建立了 GBS 经典反击的方法论模板。

### Morvan et al. 2024
- **引用**: Morvan et al., Nature 634, 328 (2024)
- **DOI**: 10.1038/s41586-024-07998-6
- **arXiv**: 2403.05457
- **子领域**: RCS phase transition
- **关键方法**: RCS 相变分析
- **已用于反查的目标**: T4, T5, T6
- **关联审查意见 ID**: --
- **一句话要点**: RCS 存在噪声驱动的"easy-hard"相变——任何 RCS 声明需证明其参数在 hard phase 内，而非仅报告名义 qubit 数和 depth。

### Begusic, Gray, Chan 2024
- **引用**: Begusic, Gray, Chan, SA 10, eadk4321 (2024)
- **DOI**: 10.1126/sciadv.adk4321
- **arXiv**: 2306.05400
- **子领域**: NISQ utility 经典模拟
- **关键方法**: Sparse Pauli Dynamics (SPD)
- **已用于反查的目标**: T1, T2, T9
- **关联审查意见 ID**: --
- **一句话要点**: SPD 在 IBM Eagle 127-qubit utility 实验上实现经典匹配——任何基于 observable estimation 的量子声明需排除 SPD 基线。

### Tindall et al. 2024
- **引用**: Tindall et al., PRX Quantum 5, 010308 (2024)
- **DOI**: 10.1103/PRXQuantum.5.010308
- **arXiv**: 2306.17839
- **子领域**: 张量网络经典模拟
- **关键方法**: Tensor Network + Belief Propagation
- **已用于反查的目标**: T3, T9
- **关联审查意见 ID**: --
- **一句话要点**: 在 heavy-hex 几何上，TN+BP 可以以多项式代价达到与 IBM Eagle utility 实验同量级精度——任何 heavy-hex / square lattice 的新量子声明都必须先排除这个基线。

### Wu et al. 2021 (Zuchongzhi 2.0 原始声明)
- **引用**: Wu et al., PRL 127, 180501 (2021)
- **DOI**: 10.1103/PhysRevLett.127.180501
- **arXiv**: 2106.14734
- **子领域**: RCS 量子优势声明
- **关键方法**: Random Circuit Sampling
- **已用于反查的目标**: T6
- **关联审查意见 ID**: --
- **一句话要点**: T6 攻击的原始靶标论文。声明 60 qubit / 24 cycle RCS 经典需 4.8x10^4 年。

### Gao et al. 2025 (Zuchongzhi 3.0 原始声明)
- **引用**: Gao et al., PRL 134, 090601 (2025)
- **DOI**: 10.1103/PhysRevLett.134.090601
- **子领域**: RCS 量子优势声明
- **关键方法**: Random Circuit Sampling
- **已用于反查的目标**: T4
- **关联审查意见 ID**: --
- **一句话要点**: T4 攻击的原始靶标论文。声明 83 qubit / 32 cycle RCS Frontier 需 6.4x10^9 年。

### Deng et al. 2025 (九章 3.0 原始声明)
- **引用**: Deng et al., PRL 134, 090604 (2025)
- **DOI**: 10.1103/PhysRevLett.134.090604
- **子领域**: GBS 量子优势声明
- **关键方法**: Gaussian Boson Sampling
- **已用于反查的目标**: T8
- **关联审查意见 ID**: --
- **一句话要点**: T8 攻击的原始靶标论文。声明 255 photon GBS exact 需 3.1x10^10 年。
