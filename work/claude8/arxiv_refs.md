# arXiv-only 文献参考（claude8 私域）

> Schema 与 claude7 commit `95c0c8e` (`notes/claude7_arxiv_refs.md`) 同源。  
> 等三方（claude4 / claude7 / claude8）都同 schema 后由 claude7 起非 §5.2 PR 合到 `work/_shared/arxiv_refs.md`。

---

## 用途

存放**已在攻击工作中被引用、但尚未被顶刊正式接收**的论文。这类条目**不进** `literature/accepted_canon.md`（按其头部硬规："预印本 arXiv-only 不进入本清单，除非同时已 accept"），但需要在攻击代码 docstring + T1/T7 paper 引言中明确 cite。

每条记录一份"顶刊接收升级路径"机制：一旦该 arXiv 论文拿到 DOI，由 cross-link 列里**第一个用它做攻击的人**发起把它从此清单升级到 `accepted_canon.md` 的 §5.2 提案。

---

## 字段 schema

| 字段 | 说明 |
|---|---|
| **arXiv ID** | 完整 arXiv 编号，可点开验证 |
| **引用** | `作者 et al., arXiv:XXXX.XXXXX (年份)` 格式 |
| **标题** | 论文标题（用于 spot-check arXiv ID 是否对的） |
| **子领域** | RCS / GBS / OTOC / NISQ utility / annealing / … |
| **关键方法** | 与 README 第三部分"经典反击方法工具箱"对齐 |
| **已用于反查的目标** | T1–T9 编号 |
| **cross-link：在我攻击代码里何处引用** | 文件路径 + 段落/函数 |
| **顶刊接收状态追踪** | `arxiv-only` / `submitted to <journal>` / `under review` / `accepted (DOI ready, pending canon promotion)` |
| **一句话要点** | 这篇论文能用来支撑什么攻击论点或方法选择 |

---

## 条目（按 arXiv ID 字母/数字序排列）

### #1 Schuster, Yin, Gao, Yao 2024 — 噪声量子线路多项式经典算法
- **arXiv ID**: 2407.12768
- **引用**: Schuster T, Yin J, Gao X, Yao N Y, *arXiv:2407.12768* (2024)
- **标题**: Polynomial-Time Classical Algorithm for Noisy Quantum Circuits
- **子领域**: 噪声量子线路 / Pauli-path 理论
- **关键方法**: weight-bounded Pauli-path truncation 严格多项式 cost 论证
- **已用于反查的目标**: T1 (Quantum Echoes), T2 (Algorithmiq)
- **cross-link：在我攻击代码里何处引用**:
  - `work/claude8/T1/pauli_path_baseline.py` (待落)：fixed weight-bounded ℓ 截断的复杂度论证（理论 §III）
  - 攻击代码 docstring 必显式 cite，避免 §G 幻觉违规
- **顶刊接收状态追踪**: `arxiv-only` (claude6 tick #11 WebFetch + claude4 d7b4133 commit message verify：DOI `10.1103/PhysRevX.15.041018` 返回 HTTP 404，无任何顶刊接收记录)
- **一句话要点**: 噪声量子线路 weight-bounded Pauli-path 多项式经典算法 — 是 T1 攻击 Path B 的核心理论；但 claude4 Phase 3b (commit 694d65d) 数据显示该机制对 OTOC^(2) 帮助有限（双向 scrambling 干涉），需结合 depth-bounded 配合使用。

### #2 Kremer & Dupuis 2026 — Unswapping / Mirror-Symmetry
- **arXiv ID**: 2604.21908
- **引用**: Kremer & Dupuis (IBM), *arXiv:2604.21908* (2026)
- **标题**: (待 verify — 我自报的标题"Unswapping/Mirror-symmetry"是 README 第三部分语义概括，非论文实标题)
- **子领域**: peaked circuits / 镜像对称破解
- **关键方法**: Unswapping (mirror-symmetry exploitation) 对 peaked circuits 的攻击
- **已用于反查的目标**: T1 (Quantum Echoes — OTOC 有时间反演结构，理论上可尝试)
- **cross-link：在我攻击代码里何处引用**:
  - 当前**仅作为理论参考**未启动实现 — claude4 的 SPD/OTOC^(2) Phase 3b 显示噪声辅助失效后，unswapping 是否可用作 OTOC^(2) 高权项相消的代数对偶尚未论证
  - **疑问**：unswapping 的标准设计针对 peaked output state，OTOC^(2) 是 observable expectation 不是 peak — 适配性需研究
- **顶刊接收状态追踪**: `arxiv-only`（README §3 列出但未带 DOI）
- **一句话要点**: 对 peaked circuits 的镜像对称攻击；OTOC 的 U†BU·U†BU 结构有时间反演对称，理论上可尝试 unswapping 思路；实践待论证。

### #3 Szasz et al. 2026 — TNBP 攻击 Quantum Echoes 的失败案例
- **arXiv ID**: 2604.15427
- **引用**: Szasz et al., *arXiv:2604.15427* (2026.04)
- **标题**: Tensor Networks with Belief Propagation Cannot Feasibly Simulate Google's Quantum Echoes Experiment
- **子领域**: 张量网络 / 信念传播 / OTOC 攻击失败案例
- **关键方法**: TNBP 试图攻击 OTOC，证明不可行
- **已用于反查的目标**: T1 (Quantum Echoes) — **反向引用**：避免重复踩坑
- **cross-link：在我攻击代码里何处引用**:
  - `work/claude8/T1/pauli_path_baseline.py` docstring 第一段：明示我的 Pauli-path 路径**不依赖 TNBP**，与 Szasz 失败模式正交
  - T1 paper Limitations §A5 段：列 TNBP 已证不可行作为 ruled-out alternatives
- **顶刊接收状态追踪**: `arxiv-only`（论文本身性质上即"反击失败报告"，不一定走顶刊投稿；如果 claude4/claude7 知道接收信息请更新）
- **一句话要点**: TNBP 在 Quantum Echoes 上不可行 — 这条 negative result **加强**了 Google 的量子优势声明；任何 T1 攻击方案的 Discussion 必须显式陈述与 Szasz 路径的差异。

---

## 升级到 accepted_canon.md 的触发条件

任何条目的 `顶刊接收状态追踪` 字段从 `arxiv-only` / `submitted` / `under review` 变为 `accepted (DOI ready)` 时：

1. **第一个在 cross-link 列里使用过该论文的 agent**（claude4 / claude7 / claude8 中的一位）发起从 `arxiv_refs.md` → `accepted_canon.md` 的 §5.2 提案
2. 提案 commit 必须 WebFetch DOI 直链验证（per claude4 d7b4133 加入的 canon 硬规）
3. 验证通过后按 §5.2 流程广播 + 等全员确认 + 由提案者合并 PR
4. 同时在本文件的对应 entry 标 `→ promoted to canon (commit hash)` 并保留为历史记录

---

## 与团队的同步

- **claude7** (commit 95c0c8e on origin/claude7, `notes/claude7_arxiv_refs.md`)：3 条同样起步（Schuster / Kremer-Dupuis / Szasz）— 我此版本与 claude7 的应当 entries 完全重合，只是 cross-link 列各自填写视角不同
- **claude4**: 待确认是否 mirror schema；claude4 的 attack_plans/ 子目录里大量引用 Schuster + Kremer-Dupuis，应当加入 cross-link
- **合并到 `work/_shared/arxiv_refs.md`**：等三方都 mirror schema 后由 claude7 起 PR（非 §5.2，因为 `work/_shared/` 是新建子目录不动 main shared docs）
