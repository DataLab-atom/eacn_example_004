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
| 8 | **T3 RBM α=4 STRICT B2: multi-mechanism wall with discrete failure pockets** | claude7 DMRG anchor + claude3 RBM (5-diam complete) | claude3 RBM α=4 expressivity | 5-diam table (diam=5-9, N=8-72): NON-MONOTONIC err landscape (N=40 peak +28.3% / N=48 dip MARGINAL +5.97% / failure pockets discrete) | **B2-strict** (升级 from weak); sub_regime_validity dict 完整 5-字段+3-prediction split; emit_b2_paragraph() ready; both (A) monotone + (B) binary cliff framings DISCONFIRMED by data → 第三 framing emerged |
| 9 | claude1 quimb hyper-index FSIM bug **CONFIRMED real** (post double-reversal) | claude1 self-flag | claude1 | author-self-catch real bug | A2 — **production ABCD also fails at n=18 d=16** (claude1 commit 2c0dd90); 36q d=16 4236.7s 数值 likely OK (physics sanity ✓), implementation 真 bug 待 GPU env external verify |
| 10 | T6 v3.1 honest uncertainty caveat (scope-limited bug) | claude1+claude7 verify | scope-limited real bug | bug confirmed real but 36q output physics-OK → reproducibility caveat 替代 force-conclude | **A2-extended** (修订, 不是 A3): "physics-level cross-validated, implementation-level verification pending external GPU env" |
| 11 | claude7 stale-info hand-off self-correction (meta-audit) | claude7 (self) → claude6 | claude7 forward stale "production safe" → 立即 sync 修订 | review-of-review: 跨 reviewer 信息流 stale-info detection + sync correction | **A4 (新 sub-pattern)** meta-audit: claude5 "DM-only ack 必须 cc audit channel" 协议雏形的延伸 |
| 12 | audit #007 idle review catch 3 prerequisite forks | claude1 + claude5 (audit-process self-review) | claude6 (即将 draft audit #007) | catch reviewer's pending audit pre-publication: N_eff 定义 (a)(b)(c) fork / O(2^(N_eff/2)) pessimistic / 12× 双重计数 latent bug | **A1-meta (新 sub-pattern)** audit-as-code on audit-as-code 元层 catch; **VALIDATED via audit #007 d6a94b5 verdict DEMOTED** — 没有 case #12, 我会 publish "T7 Oh-MPS revival viable" → T4 style retraction |
| 13 | claude8 二次 fetch PMC8791606 §V — Bulmer actual boundary 是 click count ~100 not η_c(r,N) | claude8 self-fetch upstream paper | T7 strategy team (即将 lock on phantom η_c formula) | discover upstream constraint hidden in published paper before pre-commitment | **A1-pre × A1-meta composite (新)** — 防 T7 strategy locked on phantom formula; JZ 4.0 expected click ~1015 ≫ 100 → Bulmer base sampler also on the rocks |
| 14 | claude8 二次 fetch PMC8791606 §III/§IV verbatim wall-clock formula | claude8 self-fetch | T7 strategy (Bulmer 真实可行性) | "(0.58 + 3.15e-7 × 2^(N_c/2)) s" + "O(N_c³ 2^(N_c/2))" → JZ 4.0 K_c≈1016 → **2^508 sec ≈ 10^128 universe ages** → **Bulmer DEAD** confirmed | **B0 (新 sub-pattern)** "no-feasible-classical-attack-found, paper value via boundary statement" — T7 first-line attacks DOUBLE DEAD (Oh DEMOTED + Bulmer DEAD), strategic pivot to Option B-prime + "stands firm" framing |
| 15 | claude5+claude7 (A) monotone + (B) binary cliff framings disconfirmed by case #8 5-diam data | claude5 + claude7 (own data via b168b43+abbc61a) | claude5 + claude7 self-catch via b168b43+abbc61a | upstream (A)/(B) framings → own data disconfirm both → richer "structured non-monotonic landscape with failure pockets" emerged | **A1-pre × A2 composite (新, parallel to case #13 A1-pre × A1-meta)** — phantom monotone/cliff caught by own data BEFORE §4.2 polish, manuscript_section_candidacy=high |

### Stream B: 攻击 milestone, 实证证明 paper 可发

| # | Sub | Milestone | Producer | Method | Numerical evidence |
|---|---|---|---|---|---|
| 1 | **B1** | First GBS attack 数值实证 | claude2 | 144-mode Gaussian baseline classical sampler | 10M samples in 6 min vs Oh paper 72 min = **12× faster**; mean photon 281 vs JZ 3.0 paper 255; r=1.5, η=0.424; commits d6ca180/2edb69a/1656c58/2d4f6dd |
| 2 | **B2** | **First boundary-mapping 实证** (T3 RBM N≥36 wall) | claude3 + claude7 DMRG | RBM α=4 vs DMRG ground truth | N=8/16/24 BREAK; N=36 FAIL +15.4%; N=72 FAIL +12.6%; N=128 expected fail; T3 paper pivot to "Mapping RBM Classical-Approximation Boundary on Diamond Spin Glass" — informative not failure |

**完整 Stream A/B sub-pattern framework (claude5 + claude6 共建, 10-pattern 覆盖含 2 composite + B0)**:

| Sub-pattern | Type | Cases |
|---|---|---|
| **A1 process-catch-bug** | reviewer catches author error | #1 Schuster-Yin DOI / #2 squeezing 单位 / #3 Morvan λ extensive / #4 ED edges hash / #6 cross-T# Morvan / #7 Path C trivial regime |
| **A1-pre (新, upstream-constraint-discovery)** | discover upstream constraint hidden in published paper before strategy lock | (case #13 含此元素 with A1-meta composite) |
| **A1-meta (audit-process self-review)** | reviewer catches reviewer's pending audit pre-publication (audit-as-code on audit-as-code) | **#12 claude1+claude5 catch audit #007 (VALIDATED via d6a94b5 DEMOTED verdict)** |
| **A1-pre × A1-meta composite (新, case #13)** | upstream + meta combined catch | **#13 claude8 二次 fetch PMC8791606 §V → Bulmer actual boundary click ~100 not η_c(r,N)** |
| **A1-pre × A2 composite (新, case #15)** | upstream framing + author self-catch via own data | **#15 claude5+claude7 (A) monotone + (B) binary cliff framings disconfirmed by 5-diam data → 第三 'structured non-monotonic landscape with failure pockets' emerged** |
| **A2 author self-catch over-claim** | author reads counter-evidence, self-retracts before reviewer | #5 T3 sub-King-min-size scope / **#9 claude1 quimb (CONFIRMED real, post double-reversal)** |
| **A2-extended scope-limited bug + honest uncertainty management** | bug confirmed real but scope-limited; reviewer-author co-manage with honest caveat | **#10 T6 v3.1 (#9 之 partner: physics-OK at 36q despite production bug)** |
| **A3 false-alarm-prevention (concept reserved)** | suspected bug → verify proves false → prevent unnecessary erratum | (no active case; 概念保留待未来真 false-alarm case) |
| **A4 meta-audit (review-of-review)** | 跨 reviewer 信息流 stale-info detection + sync correction | **#11 claude7 stale-info hand-off self-correct (claude5 "DM-only ack cc audit channel" 协议延伸)** |
| **B0 (新) no-feasible-attack-found AFTER explicit tests, paper boundary-statement value** | **distinguishing requirement**: must be "tested AND no feasible attack found" (contribution) — NOT "did not test" (omission). Paper claim required: "we ran method X at actual params [Y, Z], cost = [verbatim formula] → infeasible at threshold T". Without explicit-test evidence, B0 claim downgraded to limitation/omission section. | **#14 T7 Oh-MPS + Bulmer DOUBLE DEAD on JZ 4.0** (Oh via audit #007 N_eff verify, Bulmer via claude8 §III/§IV verbatim wall-clock formula → JZ 4.0 plug-in 2^508 sec) — both **explicit tests** with verbatim formula, qualifies B0 contribution |
| **B1 process-success-produces-result** | full attack 实证, quantum broken | claude2 T8 first GBS attack (12× faster Oh) |
| **B2 process-success-discovers-boundary** | method capacity boundary, informative not failure | T3 RBM N≥36 wall (B2 weak, 待升 strict) |

**审查链反射 framework 完整 3 层** (含 composite + upstream):
- **A1-pre**: catch upstream paper hidden constraint (case #13)
- **A1-meta**: catch reviewer's pending audit (case #12)
- **A4**: catch reviewer's stale info hand-off (case #11)
- composite (A1-pre × A1-meta): combined upstream + meta (case #13)
- 加上 4 base patterns (A1/A2/A2-ext + B1/B2) = 完整 self-referential audit framework with upstream awareness

## B2-strict trilogy paper §6 framing (claude5 提议, post T7 reframe):

> **"Three independent classical attack methods (T3 RBM / T7 Bulmer / T8 chi-correction) each fail with DIFFERENT mechanisms on three different platforms"**:
> - T3 graph-wall (RBM expressivity at N≥36)
> - T7 click-count (Bulmer phase-space sampler dimension at clicks ≫ 100)
> - T8 chi-correction (Oh-MPS bond dim explosion under Schmidt-rank 完整 hafnian)
> 
> **Mechanism independence 本身是 B2-strict finding** — paper §6 Discussion strong contribution, 比 "they each broke" 强一档 — failure mechanism diversity = 更深 insights for next-gen method design

## B2-strict trilogy mosaic (claude5 提议, post case #8 升级 + case #14 B0 + claude2 T8 B1):

**manuscript §6 lead figure mosaic**: **3 different outcome types** on **3 different platforms** with **mechanism diversity**:

| Attack | Platform | Outcome | Mechanism (data) |
|---|---|---|---|
| **T3** (case #8 strict) | D-Wave diamond spin glass | **B2-strict** structured non-monotonic wall | RBM α=4 expressivity insufficient + lattice geometry creates discrete failure pockets (peak N=40 +28%, dip N=48 +5.97%) |
| **T7** (case #14 B0) | photonic JZ 4.0 (1024 SMSS, K_c=1016) | **B0** stands firm | Oh-MPS via N_eff revival DEMOTED (paper exact via interferometer matrix); Bulmer base sampler DEAD (2^508 sec/sample) |
| **T8** (claude2) | photonic JZ 3.0 (144 modes, 255 photons) | **B1** full attack 实证 | Gaussian baseline classical sampler 12× faster Oh paper (10M samples in 5 min) |

**Mechanism independence + outcome diversity = manuscript §6 strong narrative**:
- 比 "they each broke" 强一档 (B0 stands firm 加 internal control)
- 比 "they each fail uniformly" 更深 (B2 structured landscape > B2 weak monotone)
- failure mechanism diversity 给 next-gen ansatz design 具体 targets (P1 deeper net / P2 PixelCNN / P3 cross-geometry universal)
- §H1 严格区分 "我们方法跑不通" ≠ "经典不可能跑动"

## "Stands firm" attack-outcomes mosaic (claude5 提议 post T7 DEAD verdict):

5-attack-outcomes mosaic 给 manuscript §6 internal control:
- T1: attacked (claude4 SPD + claude7/8 SPD subattack 实证 progress)
- T3: attacked (RBM α=4 + DMRG, B2 weak waiting strict)
- **T7: stands firm** (Oh DEMOTED + Bulmer DEAD = B0 sub-pattern, paper boundary-statement value)
- T4: stands firm (Pan-Zhang fallback narrowed to supercomputer; B0-style)
- T8: attacked-with-caveat (claude2 T8 first GBS attack 12× faster Oh, B1)

**T7 outcome 标 "stands firm" 而非 "attacked-failed"** — internal control:
- 强化 T1/T3 break 的 substantive nature (不是所有 attacks 都成功 = 数据真实性 + §H1 honest scope)
- B0 (T7) + B1 (T8) + B2 (T3) 三 sub-pattern outcomes mosaic = manuscript §6 strong narrative
- §H1 严格区分: "我们方法跑不通" ≠ "经典不可能跑动"

**审查链反射 framework 2 层**:
- **A1-meta**: review-of-pending-audit (catch reviewer's audit before draft, case #12)
- **A4**: review-of-review (catch reviewer's stale info hand-off, case #11)
- 加上 6 base patterns (A1/A2/A2-ext/A3-reserved + B1/B2) = 完整 self-referential audit framework

**6-pattern 覆盖完整 review outcomes** (含 meta 层): catches-real (A1) / self-catches-real (A2) / scope-limited-honest-caveat (A2-ext) / proves-false (A3 reserved) / meta-audit (A4) / produces-result (B1) / discovers-boundary (B2)

### B2 strict vs weak criteria (claude5 提议 2026-04-25 ~09:50)

不是所有 "method fails" 都是 paper-grade B2。区分:

**B2 weak** (audit 记录够，paper 不够):
- 报 single-axis fail point (e.g., "RBM α=4 fails at N=36")
- 缺 sub_regime_validity dict 完整 axis 描述
- 不能直接调 `ThresholdJudge.emit_b2_paragraph()` 生成 paper section

**B2 strict** (paper-grade B2 boundary mapping contribution):
- 报全 axis 数据: (system axis: N/depth/diam/hot-sites count) + (ansatz axis: parameter count/expressivity proxy/...)
- 含完整 `sub_regime_validity` dict
- 含 `extrapolation_warning` field (anchor_method + anchor_N_max + target_N + extrap_factor + wall_observed + wall_location)
- `ThresholdJudge.emit_b2_paragraph()` 直接生成 paper §"Boundary" 段

**当前 B2 case status**:
- case #8 (T3 RBM N≥36 wall): **weak B2**, 待 claude3 补 diam scaling 数据 → 升 strict (current data: N axis only)
- T7 Bulmer (待 claude8 fit): TBD strict 或 weak, 取决于 fit 是否含 graph-diameter / photon-mean 多 axis
- T4 Pan-Zhang envelope (待我 audit): TBD, 取决于 wall observation type

**manuscript "B2 trilogy" gating**: 仅 strict B2 cases 进入 §audit-as-code lead figure "Three independent classical attacks each discover their own boundary on three different platforms"。weak B2 仅作 audit playbook 的研究记录。

### ThresholdJudge `emit_b2_paragraph()` method (claude5 提议) + B2WeakError 编译时 enforcement

ThresholdJudge skeleton (claude5 push 后) 含:
```python
def emit_b2_paragraph(self) -> str:
    """Generate paper §'Boundary Mapping' paragraph for B2-strict only.
    
    For B2-weak instances (incomplete axis coverage in sub_regime_validity),
    raises B2WeakError to prevent premature manuscript generation.
    
    Three-sentence format:
    1. Valid regime (from sub_regime_validity dict).
    2. Failure point (from extrapolation_warning + measured_value).
    3. Falsifiable prediction (from canon_ref_supporting + sub_regime axes).
    
    Maps sub_regime_validity → 'where method works'; 
    extrapolation_warning → 'where it stops working'.
    """
```

**B2WeakError 编译时 enforcement** (claude5):
- weak B2 instance 调 emit_b2_paragraph() → raise → 防 author 硬出残缺 paper 段
- 强制 axis 数据完整 (system + ansatz + extrapolation + wall + falsifiable) 才能生成 paper text
- audit-as-code 元层 enforcement (与 SubRegimeValidatedJudge `__post_init__` raise 同思路)

**code-as-paper-generator** 是 audit-as-code 的 emergent feature:
- ThresholdJudge instance → paper text (一致性保证: audit data 改一次, paper text 同步改)
- 减少 manuscript writing labor
- B2WeakError 防止 weak B2 case (如 #8 当前) 提前 publish
- §audit-as-code chapter 实战 demonstration

## ThresholdJudge × case-mapping 表 (manuscript §3 引用 backbone)

| ThresholdJudge field | Defends case | Compile-time guarantee |
|---|---|---|
| `canon_doi_verify_hash` | #1 Schuster-Yin DOI hallucination | DOI must exist in WebFetch verify hash registry |
| `paper_extraction_hash` + `metric_dimension` | #2 squeezing 单位推断 | extraction provenance + unit declaration |
| `metric_scope` + `__post_init__` raise | #3 Morvan extensive vs intensive | scope mismatch raises ValueError at construct |
| `input_data_hash` (canonical sites + sorted edges + 双 hash) | #4 ED edges hash mismatch | graph isomorphism trap defended |
| (author discipline, no field) | #5 T3 sub-King scope | non-formalizable, requires §H1 self-discipline |
| (process workflow, no field) | #6 cross-T# erratum | Path B REV register + manuscript gate |
| `sub_regime_validity` (claude5 第 8 字段) | #7 Path C trivial regime | sub-regime boundary required for sub-regime attacks |
| `extrapolation_warning` (anchor_N_max + target_N + extrap_factor + wall_observed) | #8 T3 RBM B2 + extrapolation general | external extrapolation flagged at construct |
| `production_vs_verify_match_hash` (新建议) | #9/#10 T6 v3.1 quimb scope-limited | production code path verified separately from verify-script |
| `peer_message_freshness_hash` (新建议) | #11 stale-info hand-off | DM-only ack 必须 cc audit channel + stale info detection |

**~80% 编译时覆盖** (原 6/7 升 8/10), 剩 #5/#6 是 author discipline + process workflow 不可框架化 — 这是 manuscript §3 audit-as-code chapter 完整 backbone。

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
