# claude6 审计记录索引

> 私域索引（不上 main）。汇总本 agent 在 `agents/claude6/0X_audit_*.md` 出的所有审计 + 跟踪状态。

## Audit 流程模板

### Path A: erratum-fast-resolution（轻量，省 reviewer 时间）

```
detect (single reviewer flag, e.g. quick formula sanity-check)
  ↓
second-opinion (independent reviewer corroborate)
  ↓
broadcast to author + cc 正式 reviewer
  ↓
author erratum commit (within ~30 min)
  ↓
close as resolved (audit notes only, no REV record)
  ↓ author 在被审 commit message 里 credit reviewers (§I 披露)
```

**适用条件**：
- 单一数字 / 公式 / 单位错误
- 主结论不依赖该错误（修后 paper story 不变）
- author 自纠错配合度高

**独立性硬要求（claude8 2026-04-25 补充）**：
- second-opinion 必须**独立推导**——只看被审 commit，**不读** detect 方的 audit 内容/数字/结论
- 如果 second-opinion 是"读了原 audit 后投 +1"，**不算独立 corroboration** → 必须升 Path B (REV)
- T4 audit #003 满足此条：claude6 commit 7cafcf8 推完前 claude8 无视任何 claude6 文本独立估算；claude8 推完前 claude6 无视任何 claude8 文本写出 §5。事实独立 ✓

### Path C: paper-extraction verify chain（claude5 提议 2026-04-25, 防 §G1 幻觉延伸到 paper body 提取）

```
[extract]        — extractor pypdf/MCP 抽 (paper, page, value)
[announce]       — extractor push branch + ping reviewer
[verify-text]    — reviewer 独立 WebFetch verbatim diff
[verify-physics] — reviewer 物理一致性 sanity check (formula reverse-derive)
[ack-or-fix]     — extractor ack OR errata commit
```

**适用条件**：
- 任何从 paper body / SI 提取的数值参数 (squeezing, η, fidelity, sample count, etc.)
- 尤其是**未显式标 unit / convention** 的数据（最易出错）
- 多 reviewer 同时依赖该数据做下游决策

**已用案例**：
- verify #001: claude5 JZ 3.0 r=1.2-1.6 nepers (2026-04-25 07:36, 5 步全过, claude6 c212250)

## process-as-evidence 全案例总览 (manuscript Methods §"流程严谨度" 引用基础)

### Stream A: process-catch-bug (防御 audit, 防止错误进 main)

| # | Case | Catcher | Catched | T_detect→close | Path |
|---|---|---|---|---|---|
| 1 | Schuster-Yin DOI 404 (canon hallucination) | claude6 | claude4 v2 canon | 17 min | A → 升 candidate → close |
| 2 | claude5 squeezing 单位推断 (jz30/jz40 extract) | claude6 (photon-count physics) | claude5 self-request | ~30 min | C (paper-extraction) |
| 3 | claude2/1 Morvan λ extensive 公式错 | claude2 self → claude7 量纲 → claude6 PDF | claude2 + claude1 | **6 min** ⚡ (record) | A → 3-reviewer consensus |
| 4 | claude3/7 ED edges hash mismatch (T3 spec v1) | claude7 self-correct + claude3 反 catch | claude7 + claude3 | 13 min (reviewer self-fix) | B-style (graph-isomorphism trap) |
| 5 | claude3 T3 sub-King-min-size scope self-retract | claude3 (self) | claude3 self-detected | self-detected | scope discipline |
| 6 | claude1 Morvan erratum (cross-T# closed loop) | claude7+claude2+claude6 (3-reviewer parallel) | claude1 + claude2 | 35 min cross-T# | A → REV-MORVAN-001 register |
| 7 | claude7 Path C "Willow 9 hot" 投射 trivial regime | claude7 self-correct (claude4 3bb7ed2 ground truth) | claude7 | reviewer self-correction #2 | A1 → Path C v0.4 重写 |
| 8 | RBM α=4 scaling break N≥36 (T3) | claude7 DMRG anchor catches RBM | claude3 | DMRG 第三独立 ansatz catches RBM scaling | B2 → T3 paper pivot to boundary mapping |
| 9 | claude1 quimb hyper-index FSIM bug **INITIAL flag → reversed** | claude1 self-flag | claude1 | INITIAL author-self-catch | A2 → **REVERSED**: bug 在 verify-script 不在 production; 36q d=16 4236.7s SAFE, REV-T6-002 PASSES 维持 |
| 10 | verify-stage self-correction prevents unnecessary erratum (T6 v3.1) | claude1+claude7 verify | claude1 (false alarm) | verify proves false → no erratum needed | **A3 (新 sub-pattern)** false-alarm-prevention; pairs with #9 (审查二阶严谨度证据) |

### Stream B: 攻击 milestone, 实证证明 paper 可发

| # | Sub | Milestone | Producer | Method | Numerical evidence |
|---|---|---|---|---|---|
| 1 | **B1** | First GBS attack 数值实证 | claude2 | 144-mode Gaussian baseline classical sampler | 10M samples in 6 min vs Oh paper 72 min = **12× faster**; mean photon 281 vs JZ 3.0 paper 255; r=1.5, η=0.424; commits d6ca180/2edb69a/1656c58/2d4f6dd |
| 2 | **B2** | **First boundary-mapping 实证** (T3 RBM N≥36 wall) | claude3 + claude7 DMRG | RBM α=4 vs DMRG ground truth | N=8/16/24 BREAK; N=36 FAIL +15.4%; N=72 FAIL +12.6%; N=128 expected fail; T3 paper pivot to "Mapping RBM Classical-Approximation Boundary on Diamond Spin Glass" — informative not failure |

**完整 Stream A/B sub-pattern framework (claude5 + claude6 共建, 5-pattern 覆盖)**:

| Sub-pattern | Type | Cases |
|---|---|---|
| **A1 process-catch-bug** | reviewer catches author error | #1 Schuster-Yin DOI / #2 squeezing 单位 / #3 Morvan λ extensive / #4 ED edges hash / #6 cross-T# Morvan / #7 Path C trivial regime |
| **A2 author self-catch over-claim** | author reads counter-evidence, self-retracts before reviewer | #5 T3 sub-King-min-size scope / #9 INITIAL claude1 quimb (后 reversed) |
| **A3 false-alarm-prevention (新)** | suspected bug → verify proves false → prevent unnecessary erratum | **#10 T6 v3.1 verify-script bug not production (claude1+claude7)** |
| **B1 process-success-produces-result** | full attack 实证, quantum broken | claude2 T8 first GBS attack (12× faster Oh) |
| **B2 process-success-discovers-boundary** | method capacity boundary, informative not failure | T3 RBM N≥36 wall |

**5-pattern 覆盖完整 review outcomes**: catches-real (A1) / self-catches-real (A2) / proves-false (A3) / produces-result (B1) / discovers-boundary (B2)

**manuscript Methods §"流程严谨度" 双 stream evidence**:
- Stream A (A1+A2): 7 cases, 防御 audit → 证流程能挡错
- Stream B (B1+B2): 2 cases, 攻击 milestone → 证流程能产果 OR 产 boundary
- B2 pattern 把 negative result 转成 paper contribution (与 §H1 严格区分一致)
- cross-attack boundary mapping (T3 + 可能的 T1/T7) → manuscript 新章节

共同模式：起草者自查可漏 → 独立 reviewer catch → reviewer 也可漏 → N=2 独立 reviewer 兜底。
manuscript 直接量化引用, 比 "我们 review 过" 软声明强一个量级。

## ThresholdJudge 编译时防御 (claude5 提议, audit-as-code)

```python
ThresholdJudge(
    target_id, metric_name, metric_scope, metric_definition,
    canon_doi, canon_section, measured_value, critical_value, comparator,
    input_data_hash  # 防 graph-isomorphism trap (case #4)
)
# __post_init__: 检查 scope/definition mismatch → 编译时 raise
# 防 case #3 类型错误 (Morvan extensive vs intensive 混淆) 永不进 commit
```

适用：T3/T4/T7/T8/T1 所有 threshold-judge 类攻击, 把 §G1/§H1/§H4 防御从 review-time 提前到 construct-time。

### Path B: REV-formal（重量，多 reviewer 持续不同意）

```
detect
  ↓
second-opinion (disagree or insufficient)
  ↓
REV-YYYYMMDD-T#-NNN 正式审查意见 commit + broadcast
  ↓
author 必须给 evidence-based response (DOI / 复算 / 收敛)
  ↓
review board (2+ agents) 裁决保留 / 撤回
  ↓
保留则进 paper limitations / SI; 撤回则关闭
```

**适用条件**：
- 方法学 / 范围声明 / SI 数据完整性
- 主结论依赖该问题
- author 反复辩护或不回应

## 已开审计

| Audit ID | 触发对象 | Path | 状态 | 文件 |
|---|---|---|---|---|
| #001 | 全网 §3.1 合规 (用户质询) | (调查类) | RESOLVED 2026-04-25 06:14 | `03_audit_eacn3_compliance.md` |
| #002 | claude2/claude4 双边改 canon §5.2 半步违规 | A (协调，未升级) | OPEN — 等 claude4 lead 合并 §5.2 广播 | `05_audit_002_canon_double_edit.md` |
| #003 | claude2 commit 398fa62 T4 XEB 2^110 数字 | A | RESOLVED 2026-04-25 06:51 (claude2 commit c6b515b 勘误) | `06_audit_003_T4_xeb_derivation.md` |

## 监视中（未到 audit 阈值，跟踪）

- claude2 自纠错 pattern：T4 (2^110) + T8 (1.5 dB squeezing) 两次 BREAKTHROUGH 标语 → review 捉错 → 自修。文化健康但效率改进空间。已私下通过 eacn3 软提醒，**不入正式 audit**
- claude4 SPD Heisenberg ordering 已修复并机器精度收敛，跟踪后续 Phase 2 (噪声+收敛性) 是否有类似问题
- claude5 分支路径 `branches/claude5/work/...` 偏离 `work/<id>/` 约定，由 claude8 询问 claude5 中
- claude7 GPU schedule v0.2 §5.2 广播倒计时（claude6/5/2 ack；claude1/3/4/8 待）
- canon merge 提案 §5.2 广播待 claude4 启动（8 unique entries 已对齐）

## Cross-cutting 跟踪

- **REV 候选**：暂无 active candidate（audit #003 已降级为 erratum）
- **共享文档 main 待合**：(1) GPU schedule v0.2 → infra/gpu/schedule.md, (2) accepted_canon merged 8 entries
