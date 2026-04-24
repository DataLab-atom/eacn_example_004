# §5.2 共享文档修改提案 #001

> 提案对象：`literature/accepted_canon.md`  
> 提案者：claude8  
> 状态：**草案，未广播，等内容复核后通过 eacn3 走 §5.2**  
> 时间：2026-04-25

## 提案要点

`literature/accepted_canon.md` 当前为模板，无任何条目。我提案添加 4 篇**已被顶刊正式接收**的论文作为反查 T1/T7/T8 的起步弹药。所有引用均可点开 DOI 验证（不引 arXiv-only）。

⚠️ **重要：第 4 条 Kremer-Dupuis 与第 1 条 Schuster 当前可能都仍在 arXiv 预印本阶段；我会在广播前再确认其期刊接收状态，未确认则只列入 `work/claude8/` 私域笔记，不进入 canon。**

---

## 拟新增条目（待事实复核后才走 §5.2）

### 1. Begušić, Gray, Chan 2024 — SPD 打破 IBM Eagle
- **引用**：Begušić, Gray, Chan, *Sci. Adv.* **10**, eadk4321 (2024)
- **DOI**：10.1126/sciadv.adk4321
- **arXiv**：2308.05077
- **子领域**：NISQ utility / SPD
- **关键方法**：Sparse Pauli Dynamics (SPD)
- **已用于反查的目标**：T1 (Quantum Echoes), T2 (Algorithmiq), T9 (IBM Nighthawk)
- **关联审查意见 ID**：（待开）
- **一句话要点**：SPD 把 Heisenberg-picture 算符演化稀疏化到 Pauli weight 截断，已在 IBM Eagle utility 实验上以 wall-clock 几百秒完成；T1 Quantum Echoes 是 second-order OTOC（同样 Heisenberg 图景算符期望值），SPD 是当前最直接、却**尚未系统测试过**的攻击向量。

### 2. Tindall, Fishman, Stoudenmire, Sels 2024 — TN+BP 打破 IBM Eagle
- **引用**：Tindall et al., *PRX Quantum* **5**, 010308 (2024)
- **DOI**：10.1103/PRXQuantum.5.010308
- **arXiv**：2306.17839
- **子领域**：张量网络 + 信念传播
- **关键方法**：Tensor Network + Belief Propagation（heavy-hex 几何）
- **已用于反查的目标**：T3 (D-Wave), T9 (IBM Nighthawk)
- **关联审查意见 ID**：（待开）
- **一句话要点**：在 heavy-hex 几何上 TN+BP 以多项式代价达到 IBM Eagle utility 同量级精度；任何在该几何或类似稀疏图（含部分 D-Wave 拓扑）的新声明必须先排除这个基线。

### 3. Oh, Lim, Fefferman, Jiang 2024 — GBS 损耗经典欺骗
- **引用**：Oh, Lim, Fefferman, Jiang, *Nat. Phys.* **20**, 1647 (2024)
- **DOI**：10.1038/s41567-024-02535-8
- **arXiv**：2306.03709
- **子领域**：玻色采样 / GBS
- **关键方法**：基于损耗的经典模拟（lossy MPS）
- **已用于反查的目标**：T7 (Jiuzhang 4.0), T8 (Jiuzhang 3.0)
- **关联审查意见 ID**：（待开）
- **一句话要点**：实验级 GBS 损耗水平下 MPS 可经典生成与硬件分布在统计指标上不可区分的样本；任何 GBS 量子优势声明必须公布逐 mode 损耗 + 与 lossy MPS baseline 的距离指标，未公布即审查意见。

### 4. Pan & Zhang 2022 — TN 收缩打破 Sycamore
- **引用**：Pan & Zhang, *Phys. Rev. Lett.* **129**, 090502 (2022)
- **DOI**：10.1103/PhysRevLett.129.090502
- **arXiv**：2111.03011
- **子领域**：RCS 经典模拟
- **关键方法**：张量网络收缩（big-batch amplitude）
- **已用于反查的目标**：T4 (Zuchongzhi 3.0), T5 (Willow RCS), T6 (Zuchongzhi 2.x)
- **关联审查意见 ID**：（待开）
- **一句话要点**：把 Sycamore "10000 年" 的 RCS 任务在 GPU 集群上数小时跑完；同样配方（53 q × 20 cycle 模板放大到 60–105 q × 20–32 cycle）至今仍是攻击 Zuchongzhi/Willow RCS 部分的主线，但在新硬件上需重新做 bond dimension 收敛性扫描。

---

## §5.2 流程预设

1. ✅ **本提案落 claude8 分支**（即本文件） — done at commit time
2. ⏳ **eacn3 广播给所有 7 同伴**（amount=0, invitee=至少 1）— 待我对 4 条 DOI 都人工 spot-check 后再发
3. ⏳ **等待 6/7 名同伴显式 ack/nack**（沉默不算同意）
4. ⏳ **达成共识后由我（提案发起者）合入 main**

注：在事实复核未完成前，本文件仅生效于 claude8 分支，不发广播 — 避免引入未验证 DOI。
