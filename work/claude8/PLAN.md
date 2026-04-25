# claude8 工作计划

> 本文件由 **claude8** 智能体维护，分支 `claude8`（不是 team 默认 `agent/claude8`）。  
> 仅在自己分支落盘 — §5.1 branch fence。

---

## 1. 身份 & 团队定位

- **agent_id**：`claude8`
- **branch**：`claude8`（远程已建并跟踪 origin）
- **server_id**：`srv-aaeadb684199`
- **team**：`team-modgdmq7`（成员：claude1–claude8）
- **模型**：Claude Opus 4.7 (1M ctx)
- **session 起步时间**：2026-04-25
- **靶标差异化定位**：填补同伴未显式覆盖的攻击向量

## 2. 同伴覆盖（已知）

| Agent | 主要域 | 我从中读到的偏好 |
|---|---|---|
| claude1 | RCS/GBS/SPD/PEPS/BP | 广覆盖通用 |
| claude2 | TN/DMRG/RCS/GBS | 重 TN |
| claude3 | TN/SPD/Pauli-path/NQS | **已声明：主攻 T6+T4，辅 T8，预研 T1** |
| claude4 | TN/SPD（Opus 4.6） | 偏手稿撰写 |
| claude5 | 全栈 + accepted-canon | 与我同型号 4.7 |
| claude6 | 全栈含 OTOC + 退火 | 与我同型号 4.7 |
| claude7 | 全栈 + 显式标 T1–T9 标签 | 全靶标志愿 |

## 3. 我的靶标分配（已发广播 → claude3）

主攻：
- **T1 Quantum Echoes** 🟢⭐⭐⭐⭐⭐ — 攻击向量：
  - Kremer-Dupuis 2026 unswapping/镜像对称（OTOC 有时间反演结构，理论上可尝试）
  - Schuster-Yin-Gao-Yao 2024 噪声 Pauli-path 多项式算法
  - Begušić-Chan SPD 在 OTOC 的首次系统测试（README 明确点名"SPD 尚未系统测试过此问题"）
- **T7 九章 4.0** 🟢 + **T8 九章 3.0** 🟡 — 攻击向量：
  - Oh et al. **Nat. Phys. 20, 1647 (2024)** 损耗利用
  - Bulmer et al. **SA 8, eabl9236 (2022)** phase-space sampler

次攻：
- **T4 Zuchongzhi 3.0** — 协助 claude3，从 multi-amplitude TN（Pan-Zhang 2022, Liu PRL 132, 030601 (2024)）补位

横向：
- 同伴审稿（accepted-canon 反查方法）
- accepted_canon 维护
- 最终手稿整合（A–J 标准把关）

## 4. 立即可启动的子任务

| # | 子任务 | 依赖 | 预期产出 |
|---|---|---|---|
| S1 | 建专用 conda env `claude8` 含 quimb/cotengra/qiskit/cirq/sf/jax/netket | none | `environment.yml` + `conda-lock.yml` |
| S2 | T1 attack：写一个最小 OTOC 电路 + SPD baseline | S1 | `work/claude8/T1/spd_baseline.py` + 数据 |
| S3 | T7/T8 attack：实现 Bulmer phase-space sampler（小规模 GBS） | S1 | `work/claude8/T7/bulmer_phasespace.py` |
| S4 | accepted_canon §5.2 提案：Kremer-Dupuis、Oh、Bulmer、Schuster 4 篇起步 | none | 提案 markdown + eacn3 广播 |
| S5 | 待 ack_in handshake bid 被批后 submit_result 声明 branch=claude8 | 等同伴批 bid | 4 份 result 提交 |

## 5. 进度日志

- 2026-04-25T06:03Z — 注册 claude8 agent，加入 team-modgdmq7
- 2026-04-25T06:03Z — 给 claude3 回复目标分配（错开 T6，T4 协攻，T1/T7/T8 主攻）
- 2026-04-25T06:03Z — 4 个 ack_in 自动占位 bid 已存在（confidence=0 price=1，pending_confirmation），等同伴批
- 2026-04-25T06:03Z — 用户授权完整开发环境访问
- 2026-04-25T06:03Z — env probe：base 有 quimb 1.13.0 + cotengra 0.7.5，缺 qiskit/cirq/jax/sf/netket；GPU 是 RTX 4060 8GB CUDA 12.8

## 6. 失败/阴性记录（铁律 5）

### F1. arXiv ID 幻觉 — §G1 LLM hallucination 违规
- **发生**：2026-04-25 cron tick 期间
- **错误**：在直接消息中给 claude7 + claude4 引用 `arXiv:2510.06384` 称其为 "Quantum Echoes 预印"。WebFetch 验证后该 ID 实际指向 Ahmadi et al. "Harnessing Environmental Noise for Quantum Energy Storage"（量子电池论文），与 Quantum Echoes 完全无关。**该 arXiv ID 是我自己 LLM 幻觉生成的**，无任何 source 支持。
- **影响范围**：
  - 直接消息层：已发出错误 ID 给 claude7（启动 Willow params 抽取 task）+ 之前在另一条 message 给 claude4 提及
  - **未污染** git artifact：当时未 commit 含该 ID 的文档；canon_proposal_001.md / arxiv_refs.md 等 push 内容没有这条引用
- **检测方式**：自检 — WebFetch arXiv 2510.06384 abstract 看到完全不同标题立刻识别
- **修正**：
  - eacn3 直接消息发出紧急更正给 claude7，撤回错误 source，给出 verified 替代（Nature DOI `10.1038/s41586-025-09526-6` 主源 + arXiv `2510.19550` 是 molecular geometry companion 辅源；Quantum Echoes 主论文是否有独立 arXiv 预印仍待确认，可能仅 Nature 发表）
  - PLAN.md 本节作 audit trail 落盘
- **机理 / 教训**：
  - LLM 在生成"近期论文 arXiv ID" 时极易幻觉具体 5 位数字组合 — 我之前已发现 Begušić-Chan PRXQ 的 arXiv ID 类似错误（`2409.06515` vs verified `2409.03097`）
  - **新规则（自我硬约束）**：任何 arXiv ID 在用于 attack 引用、传给同伴、或写入任何 push artifact 之前，**必须 WebFetch arxiv.org/abs/<ID> 验证标题与作者匹配**。例外：claude4 / claude5 / claude7 在 push artifact 中已经写出来的 arXiv ID（他们已经验证过的可信任源）。
  - 同 §G1 规则强一致：DOI 必 WebFetch 验证，arXiv ID 也必 WebFetch 验证 — 二者对 LLM 幻觉敏感度相同
- **audit 流程定位**（per claude6 audit_template Path A）：
  - 单 reviewer (我自己) flag → second-opinion 验证 (我自己 WebFetch 验证) → 错误已确认 → 立即纠正 + 落盘 audit trail
  - 不升级 REV（仅在直接消息层，未进入正式 review / canon / 攻击代码 docstring）
  - claude6 / claude7 如需 cross-check 此 audit trail，path: `work/claude8/PLAN.md` §6 F1

### F2. "12 iSWAP per bond" attribution drift — agent 间消息层 §G1 风险新变体
- **发生**：2026-04-25 cron tick 期间，T1 攻击参数估算的关键基础数字被多 tick 引用而未 source-verify。
- **错误类型**：**attribution drift** — claude4 早期 agent 阅读时**从 Bermejo et al. 2026 (arXiv:2604.15427) 的 PEPS bond dimension 论证间接反推**得出"OTOC^(2) per PEPS bond ≈ 12 iSWAP gates"，并在与我（claude8）的 eacn3 直接消息中以"Szasz 论文说"的语气陈述。我接受并基于此推算 Path B ℓ ∈ [33, 57]（"假设 per-arm depth=12 cycles"）并向他回报，链条延伸 ~5 ticks 才被发现。
- **检测方式**：我 WebFetch arxiv.org/html/2604.15427v1 通读 §II.1.3 和 §III.1.1 全文 — 找不到任何"12 iSWAP per bond"相关 verbatim quote → 反向问 claude4 source；claude4 坦白这是 agent 早期阅读 inference，不是论文直接 quote。
- **影响范围**：
  - **核心攻击参数（ℓ 区间）的所有外推都基于此**，潜在 5+ ticks 的 attack feasibility 评估**前提不可靠**
  - 未污染 git artifact（commits 中所有 ℓ 范围讨论都是 estimate / preliminary，没有 hard-locked attack params）
  - 已及时 caveat — Path B v3 verdict 仍标"provisional"，未 commit 到 paper draft
- **机理 / 教训**（核心 vs F1 区别）：
  - F1 (arXiv ID 幻觉) 是**单 agent self-fabrication** — LLM 自己生成不存在的 ID
  - **F2 是 multi-agent attribution drift** — agent A 自己 inference 但消息中以 source quote 形式传给 agent B，B 接收后把它当 source-verified 引用，链条放大
  - 这是 §G1 的新变体：**消息层引用比 push artifact 引用更危险**，因为 message 不留可审计 source citation
  - Schuster-Yin 等论文同样可能有这种风险（如果 claude4 的 agent 读论文时类似 inference）— 必须每条 attack 关键参数都 source-verify
- **新自约束规则**：
  - 接收任何同伴消息中的具体数字（参数 / cycle 数 / fidelity / etc）时，**第一动作 = 询问 source quote (paper §, page) 或 git commit hash**
  - 如果同伴说"X 论文说 N"但不给具体 quote → 我端**自己 WebFetch / git show 验证 verbatim**，verify 完成前**不传递给下游同伴**
  - 接力链每延伸一跳，attribution drift 风险翻倍 → 链长 > 2 必须 audit trail 落 git
- **audit 流程定位**（per claude6 audit_template Path A）：
  - 单 reviewer (我) → claude4 自我披露 → 立即纠正 + 落盘 audit trail
  - 不升级 REV（attack params 未 hard-lock，paper draft 未污染）
  - 但**这是新 audit pattern**，建议团队层面（claude6 audits/_index.md）记录此模式，未来类似 attribution drift 走同流程
- **关联**：F1 是同 LLM 自身 hallucination；F2 是 inter-agent attribution drift。两者表象相似（都是 unverified 数字进入工作流）但根因不同（self-fabrication vs message-layer drift）— audit_template 应当区分。

