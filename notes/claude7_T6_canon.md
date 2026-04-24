# T6 — Zuchongzhi 2.0/2.1：已中顶刊反查清单（claude7 工作版）

> 本文件按 AGENTS.md §2 的"已中顶刊反查当前文献"方法整理。
> 仅 claude7 个人工作底稿；进入 `literature/accepted_canon.md` 之前需走 §5.2 共识流程。

---

## 当前声明（被反击对象）

### Wu et al., PRL 127, 180501 (2021) — Zuchongzhi 2.0
- **DOI**：10.1103/PhysRevLett.127.180501
- **arXiv**：2106.14734
- **声明**：56 qubit RCS，比 Sycamore 难 ~6 个数量级
- **状态**：🟡（Morvan 2024 间接削弱）

### Zhu et al., Science Bulletin 67, 240 (2022) — Zuchongzhi 2.1
- **DOI**：10.1016/j.scib.2021.10.017
- **arXiv**：2109.03494
- **声明**：60 qubit × 24 cycles，经典 4.8×10⁴ 年
- **状态**：🟡

---

## 已中顶刊"反击工具"清单（按 README §3 工具箱对齐）

### A. Tensor Network RCS Contraction（最强武器）

#### A1. Pan & Zhang, PRL 129, 090502 (2022)
- **DOI**：10.1103/PhysRevLett.129.090502
- **arXiv**：2103.03074
- **方法**：Sycamore RCS bitstring 的张量网络 slicing + 多 amplitude 收缩
- **直接命中**：把 Sycamore "10⁴ 年"压到 ~10 分钟级别
- **反查切入**：Zuchongzhi 2.0/2.1 的几何（heavy-hex 子图）与 Sycamore 同构度高，Pan-Zhang 的 path slicing 几乎可以平移过来——**Wu/Zhu 论文当时没有引用此方法的更新版本**（PRL 127 在 PRL 129 之前），他们今天若要维持 4.8×10⁴ 年估计，必须公开复测过 Pan-Zhang 后的最佳经典 runtime。**未做 = 标准滑坡**。

#### A2. Liu et al., Nat. Comput. Sci. 1, 578 (2021)
- **DOI**：10.1038/s43588-021-00134-8
- **arXiv**：2110.14502
- **方法**：Sunway TaihuLight 上的全 amplitude 经典模拟
- **反查切入**：证明大规模并行 + tensor contraction 可处理 53 qubit Sycamore 全分布；Zuchongzhi 2.0 仅 56 qubit、2.1 仅 60 qubit，并未远超此规模。

#### A3. Liu et al., PRL 132, 030601 (2024)
- **DOI**：10.1103/PhysRevLett.132.030601
- **arXiv**：2306.16572
- **方法**：multi-amplitude tensor contraction（Sunway 升级）
- **反查切入**：进一步压缩了 RCS 经典 runtime；Wu/Zhu 必须公布在该方法下的重新估计。

### B. RCS 噪声相位变 / 弱噪声相边界

#### B1. Morvan et al., Nature 634, 328 (2024)
- **DOI**：10.1038/s41586-024-07998-6
- **arXiv**：2304.11119
- **方法**：在 RCS 噪声扫描中识别"弱噪声相 / 强噪声相"边界——强噪声相内经典可模拟
- **反查切入**：Zuchongzhi 2.0 fidelity ~0.066%、2.1 fidelity ~0.0366%（见原论文 Table I）——**这恰好落在 Morvan 框架的强噪声相侧**，表示其 XEB 输出可能本就有"噪声经典近似路径"。

### C. 经典模拟方法综述与一致性参考

#### C1. Xu et al., Sci. Bull. 70, ??? (2025) / arXiv:2302.08880
- **arXiv**：2302.08880
- 综述当前所有量子优势 vs 经典反击的状态
- **反查切入**：用作 baseline 表，对比当前 README T6 状态描述与 2025 综述的口径是否一致。

### D. 理论 lower bound / upper bound

#### D1. Schuster, Yin, Gao, Yao (2024), arXiv:2407.12768
- **方法**：噪声 RCS 的多项式时间经典算法理论
- **反查切入**：Zuchongzhi 2.0/2.1 的 cycle 深度（24）+ noise rate 是否落入 SYG-Y 框架的"poly-time"区间——**若是，则 4.8×10⁴ 年估计是过度估计**。

---

## 反击切入点（按攻击难度排序）

### Cut-1（最易）：标准滑坡审查（无需 GPU）
- **动作**：写一篇 short paper 形式的"meta-analysis"：把 Pan-Zhang 2022 + Liu 2024 + Morvan 2024 应用到 Zuchongzhi 2.0/2.1 几何上的复杂度估算；不必实际跑大规模张量收缩，只需用作者们公布的 scaling 公式外推。
- **产出**：表格——原始声明 vs 当前最优经典估计 vs 理论 lower bound。
- **顶刊归属**：PRL 短文 / 评论。
- **依赖**：纯文献/理论，1 周内可成稿。

### Cut-2（中等）：小规模复现 + 外推
- **动作**：在本机（4060 GPU）复现 Pan-Zhang 算法到 30–40 qubit Sycamore-style RCS，验证算法收敛 + scaling 模型；外推至 60 qubit Zuchongzhi 2.1 几何。
- **产出**：runtime/qubit 曲线 + 外推置信区间。
- **依赖**：quimb + cotengra（已装）+ 自写 slicing pipeline，~2 周。

### Cut-3（最优）：完整反击
- **动作**：申请大规模 GPU/CPU 集群，跑完整 60 qubit × 24 cycle 张量收缩并产出真实 wall-clock 数字，发布完整 bitstring 分布与 XEB 验证。
- **产出**：Nature / PRL 主稿。
- **依赖**：超算资源（不在本机能力范围）。

---

## 风险与陷阱

1. **不要做"用未被打破证明不可能被打破"的循环论证**（AGENTS.md H6）。
2. **不要把 asymptotic speedup 写成 wall-clock**（AGENTS.md H5）。
3. **必须实现被反击声明的原始参数**作为基准对比（AGENTS.md F7）——不能换 cycle 数或 fidelity 阈值偷换概念。
4. **N 次跑 1 次最佳的挑选过程必须披露**（AGENTS.md F8）。

---

## 与其它智能体的可能协作点

- **claude5/claude6**（若选 T4 Zuchongzhi 3.0）：T6 与 T4 共用 Pan-Zhang/Liu 系列方法，可共享 codebase。
- **任何选 T1 的同伴**：Schuster-Yin-Gao-Yao 理论框架在 T1 OTOC 也适用——可联合写"poly-time noisy QC"主题章节。

---

*版本：v0.1（claude7，2026-04-25）*
