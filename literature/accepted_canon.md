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

*（本文件初始化时为空。第一个进入本仓库的反击/审查智能体应填入自己引用的第一条已中顶刊论文，并在 commit message 中写 `docs(canon): add <第一作者> <年份>`。）*
