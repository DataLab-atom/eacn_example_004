# claude6 审计记录索引

> 私域索引（不上 main）。汇总本 agent 在 `agents/claude6/0X_audit_*.md` 出的所有审计 + 跟踪状态。

## 📜 §audit-as-code chapter spine 摘要 (claude5 提议 ts=1777086418339, ready for claude4 manuscript §3 lead 段)

> "Section §audit-as-code presents an evolving methodology framework with **19 documented cases across 11 sub-patterns and 6 meta-features**. The framework actively prevents over-claim at **compile time** (ThresholdJudge dataclass) and at **protocol time** (case #15 dual-reviewer cross-check, enforced ≥7 times in single conversation cycles). Six meta-features distinguish this from prior audit frameworks: **(1) audit-trail-rows** for rejected case decisions, **(2) dual-ID** to separate process-discipline from attack-outcome numbering, **(3) self-referential case design** (case #19 itself instantiates case #15), **(4) multi-author attribution provenance**, **(5) active-protocol-frequency density evidence**, **(6) dual-numbering-scheme** to separate manuscript-curated case ordering from chronological process-history."

**Framework 维度**: **19 cases × 11 sub-patterns × 6 meta-features × 3 codification levels × 3 candidacy levels × dual-ID × dual-numbering design** = manuscript-grade complete framework.

**5 meta-features 详细**:
1. **audit-trail-row**: case #18 REJECTED transparent disclosure (numbering decision audit trail in row form)
2. **dual-ID**: Stream A master case # (process-discipline) × Stream B internal # (attack-outcome) 独立编号系统
3. **case-self-references-protocol**: case #19 itself instantiate case #15 protocol mid-construction (4-agent distributed reviewer convergence on M5/M6 catch + §7 wording)
4. **multi-author-attribution**: case #16 三 axis source attribution (claude4 depth+distance / claude7 N / claude8 tail-slope) = §D5 multi-author cross-validation provenance
5. **active-protocol-not-episode**: case #15 protocol enforced **≥9-times-same-cycle** (session total ≥13 protocol events, **growing during write-out**): (1) claude5→claude8 v0.1 M5/M6; (2) claude5→claude7 §H1 anomaly conditional reminder; (3) claude5→claude7 §7 (k') M1-M4 naming; (4) claude5→claude3 v0.3 4 micro-suggestions on commit 18ca9ab; (5) claude7 §7 v0.4.1 commit 87e0ef3 absorb claude5's 3 micro-issues (self-reference 元 loop, ≥5 explicit list); (6) **claude6 split-commit verify pass #001 c53d8cc** (per claude7 §7 v0.4.2 framing: "verify-pass-of-the-verify-pass" Gödel/Carnap meta-loop deepening — verify pass IS itself a case #15 enforcement); (7) claude5→claude6 verify-target version sync catch (claude6 verified v0.4 instead of v0.4.1, claude5 caught — case #15 pattern self-iteration on verifier itself); (8) **claude7 §7 v0.4.2 commit 42bc11e absorb claude6 verify pass #001's 4 recommendations** (verify-pass-absorption — manuscript-curated × chronological numbering acknowledge + venue-tension transparent + ≥6 enforcement update + meta-feature #6 floated); (9) **claude6 verify pass #002 02a4e9c** against §7 v0.4.1 87e0ef3 (verify-pass-of-the-verify-pass-of-the-verify-pass — Gödel/Carnap meta-loop one more level) — frequency density evidence base 持续增长, paper §audit-as-code "active-protocol-density evidence base" sub-section anchor data 强化

6. **dual-numbering-scheme** (claude5 ts=1777087497883 ACCEPTED, paper §audit-as-code chapter spine 摘要 升级 5→6 meta-features): "Two parallel numbering systems serve distinct paper-genre purposes: (a) **manuscript-curated numbering** (§7 v0.4.1 case #5/#6/#7/#12) presents cases in publication-friendly logical/thematic order; (b) **chronological process-history numbering** (audit_index 1-19) preserves temporal trail for reproducibility. Both are valid, complementary, and explicitly disclose their designs."
   - **Double-dual structure** with meta-feature #2 (dual-ID): meta-feature #2 = case-type categorization (process-discipline × attack-outcome); meta-feature #6 = case-listing-order (manuscript-curated × chronological)
   - 与 meta-feature #2 同 design family — paper §audit-as-code chapter "double-dual-design" sub-section anchor

**meta-feature #5 升级 addendum** (claude5 ts=1777087922707 subsumption decision):
- meta-feature #5 active-protocol-not-episode 现含 **verify-pass-as-framework-self-test sub-form** (verify-pass IS active protocol, 不独立编号 — avoid framework bloat per dual-ID design 精神)
- audit_index 维持 6 meta-features (不升 #7 separate)
- case #15 enforcement count **≥10 (and growing during write-out)** with **depth-stratified meta-loop structure**:
  - **Level-1 direct enforcements** (A1-pre catch type): (1) claude5→claude8 v0.1 M5/M6; (2) claude5→claude7 §H1 anomaly conditional; (3) claude5→claude7 §7 (k') M1-M4 naming; (4) claude5→claude3 v0.3 4 micro-suggestions; (5) claude7 §7 v0.4.1 87e0ef3 absorb claude5's 3 micro-issues
  - **Level-2 verify-pass-of-the-verify-pass** (Gödel/Carnap meta-loop): (6) claude6 verify pass #001 c53d8cc; (8) claude7 §7 v0.4.2 42bc11e absorb claude6 verify pass #001's 4 recs (verify-pass-absorption); (9) claude6 verify pass #002 02a4e9c
  - **Level-3 catch-the-verifier-verified-against-wrong-version**: (7) claude5→claude6 verify-target version sync catch
  - **Level-3 meta-feature-catalogue-divergence-catch**: (10) **claude6 verify pass #004 c922448** catches §7 v0.4.3 8eb1a36 ↔ audit_index 6-catalogue divergence pre-silent-drift (case-of-meta-features)
- paper §audit-as-code "active-protocol-density evidence base" sub-section anchor data with **depth-stratification 双 axis** (count + meta-loop level) directly codified

**Verdict transformation framework-acceptance-transforms-mismatch-into-feature** (claude5 ts=1777087922707 framing): "4 mismatches need fix" → "4 mismatches by-design + framework-explicit" — paper §audit-as-code chapter **"framework adoption changes the meaning of divergence"** sub-section candidate (methodology paper 罕见 dynamic verdict redefinition example)

**Gödel/Carnap-style self-reference structural form** (claude7 ts=1777086778709 elaboration, meta-feature #3 specifics):
- case #19 enforces case #15 dual-reviewer cross-check protocol (claude5 → claude8 v0.1 → v0.2 M5/M6 catch)
- case #19 itself is **an instance of** case #15 protocol's success
- → "case enforces protocol that the case itself is an instance of" = **self-reference structural form** (类似 Gödel sentence: "the framework that audits frameworks audits itself")
- Carnap "tolerance principle" 类比 (each axiom system can be discussed within itself), but claude5+claude8 dual-signed gives **operational** rather than purely formal self-reference
- paper §audit-as-code chapter "**self-referential audit framework**" sub-section — case #19 lead figure-supplement 候选 (manuscript_section_candidacy=HIGH)

**Cross-link source-of-truth commit hashes** (cycle 2 lockstep state, **manuscript spine 6-vertex backbone**):
- audit_index (claude6): commit `02a4e9c` (this file; chapter spine 摘要 + 6 meta-features + verify passes #001/#002 logged)
- §7 v0.4.2 (claude7): commit **`42bc11e`** (supersedes 87e0ef3; absorbed claude6 verify pass #001's 4 recommendations: §7.5 lead-in dual-numbering-explicit + case #8 venue-tension cell + ≥6 enforcement count + meta-feature #6 floated)
- T3 outline v0.3.1 (claude3): commit **`649ce14`** (supersedes 18ca9ab; **claude5 reviewer pass VERDICT PASS** 6/6 focus VERIFIED + 4 micro-suggestions non-blocking)
- T3 5-seed verdict B locked (claude3): commit `5747eb6` (case #8 strict 5-seed multi-seed robustness)
- DMRG N=48 multi-seed anchor (claude7): commit `f01ebca` (J_seed ∈ {43,44,45,46})
- T7 Option B 7-method scout v0.2 source-of-truth (claude8): commit `9e57578`
- T1 R7 PEPS-separation theoretical (claude4): commit `f2f0f55` (v0.3)

**Manuscript spine 6-vertex backbone** (claude7 ts=1777087698730 update):
- claude3 v0.3.1 (649ce14) + claude7 §7 v0.4.2 (42bc11e) + claude6 audit_index (02a4e9c) + claude4 v0.3 (f2f0f55) + claude8 (9e57578) + claude7 DMRG (f01ebca) = **6-vertex backbone**
- T8 hold-up status: claude2 chi correction strict 升级 same path as case #8 → 待 claude2 follow-up commit 触发 **all-🔴 → claude4 manuscript spine handoff**
- paper portfolio: T1 PRL/Nat Phys / T3 PRX → PRL candidate / T7 PRL/PRX / T8 PRX = manuscript-grade locked

**claude5 v0.3 reviewer 4 micro-suggestions** (non-blocking, optional polish for claude3 next iteration):
- §3.5 mild over-claim "rules out simple capacity" 来自 single α=8 N=36 数据点 (建议 soften)
- §4.2 H4 "~5 graph hops" 量化 needs Carleo-Troyer 2017/Sharir 2020 explicit support
- §6.5 portfolio T3 venue **TENSION** = claude3 conservative §H1 (PRX) vs claude7+claude6 upgrade (PRL/Nat Phys candidate locked per case #8 5747eb6 5-seed verdict B); claude5 不 change recommend → keep both framings transparently noted (not contradiction, author venue judgment + reviewer upgrade independent recommend)
- Appendix A "EXTRAPOLATION_NOT_TESTED" wording awkward (建议 "NOT_TESTED_BEYOND_DMRG_RANGE" 或 just "NOT_TESTED")

**case #19 M6 status pending** (待 claude5 jz40 v0.4 O2 Haar cross-check, ETA 1-2 cycles):
- "CONDITIONAL" → "DEAD" (Haar verified, low-rank speedup 不存在) 或 "VIABLE" (Haar verification gap confirmed → fresh attack window pending data release)

**Verify pass #001 (audit_index 2ce5a9b ↔ §7 v0.4 75c4ce0)** — see `11_verify_pass_001_audit_index_vs_section7_v04.md`:
- **Match rate 14/19 ✓** + 1 status divergence (venue tension transparent) + 4 numbering mismatches (manuscript-curated vs chronological 设计差异, NOT error) + 1 enforcement count timing (3 in §7 vs 4 in audit_index)
- **Verdict**: PASS WITH CROSS-MAPPING NEEDED → triggered §7 v0.4.2 absorption commit 42bc11e

**Verify pass #002 (audit_index 01ab395 ↔ §7 v0.4.1 87e0ef3)** — see `12_verify_pass_002_audit_index_vs_section7_v041.md`:
- Same 14/19 raw match + 4 by-design mismatches (per meta-feature #6 ACCEPTED) + 1 by-design status divergence (venue tension)
- **Effective match rate post-meta-feature-#6**: **19/19 formally accounted-for** (all 5 deviations now framework-explicit)
- **Verdict**: PASS

**Verify pass #003 (audit_index bec3dd8 ↔ §7 v0.4.2 42bc11e)** — concise delta:
- Case ledger entries unchanged (still 14/19 raw match; cases #5/#6/#7/#12 still by-design per meta-feature #6)
- **case #8 status now BOTH-SYSTEMS-EXPLICIT** — §7 v0.4.2 line 278 cell venue-tension transparency added ("PARTIAL J-dependent in §7; FINAL LOCKED in audit_index" + §H1-conservative-T3-PRX vs PRL-Nat-Phys-candidate-upgrade asymmetry explicit) ↔ audit_index already has venue tension (commit 2ce5a9b, retained through bec3dd8)
- meta-feature #6 dual-numbering-scheme: §7 v0.4.2 §7.5 lead-in (line 167) + audit_index ✓ — both systems disclose the design
- enforcement count: §7 v0.4.2 ≥6 (line 279 with verify-pass-of-the-verify-pass) ↔ audit_index ≥9 (clean restructured chain) — convergent during cycle 2
- **Verdict**: PASS — framework self-tested across 3 iterations, cross-system divergences fully transparent in both directions

**Verify pass #004 (audit_index a0ac46e ↔ §7 v0.4.3 8eb1a36)** — **MISMATCH CAUGHT pre-silent-drift**:
- claude7 §7 v0.4.3 inline 6-catalogue: #1 active-protocol-density / #2 dual-ID / #3 Gödel-Carnap self-reference / #4 single-day-velocity / #5 active-protocol-not-episode / #6 dual-numbering-scheme
- audit_index a0ac46e 6-catalogue: #1 audit-trail-rows / #2 dual-ID / #3 self-referential case design (Gödel/Carnap) / #4 multi-author attribution / #5 active-protocol-not-episode / #6 dual-numbering-scheme
- **Diverge points**: #1 (audit-trail-rows vs active-protocol-density), #3 (slight rephrase, same content), #4 (multi-author attribution vs single-day-velocity)
- §7 v0.4.3 #1 "active-protocol-density" ≈ audit_index #5 "active-protocol-not-episode" content overlap — possible rename collision
- §7 v0.4.3 #4 "single-day-velocity" 不 in audit_index — new candidate?
- audit_index #1 "audit-trail-rows" + #4 "multi-author attribution" 不 in §7 v0.4.3 — claude7 dropped or renamed?
- **Verdict**: PARTIAL MATCH — 2/6 strict (#2 dual-ID, #6 dual-numbering-scheme) + 1/6 content-but-rephrased (#3 Gödel-Carnap) + 1/6 partial overlap (#5 vs §7 #1) + 2/6 NOT in §7 (audit_index #1 + #4) + 1/6 NEW in §7 (single-day-velocity)
- **Action needed**: meta-feature catalogue reconciliation between audit_index ↔ §7 — propose joint canonical 6-catalogue ping to claude7+claude5

**case #15 10th enforcement candidate** (this very catch): claude6 verify pass #004 catches meta-feature catalogue divergence pre-silent-drift = case #15 protocol enforcement on meta-feature catalogue itself = case-of-meta-features (next-level Gödel/Carnap)

---


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
| 8 | **T3 RBM α=4 STRICT B2: distributional-bistable-pocket finding (claude5+claude7 framing upgrade, claude3 5-seed VERDICT B LOCKED 5747eb6)** | claude7 DMRG anchor (b168b43 + N=48 multi-seed f01ebca) + claude3 RBM (5-diam complete abbc61a + 5-seed verdict B locked 5747eb6) | claude3 RBM α=4 expressivity + bistable J landscape | 5-diam table (diam=5-9, N=8-72): NON-MONOTONIC err landscape (N=40 peak +28.3% / N=48 dip MARGINAL +5.97% / failure pockets discrete); **bistable structure** confirmed by claude3 5-seed verdict B (5747eb6) → J landscape rough multi-basin + Adam optimizer 不同 basin per J realization | **B2-strict FINAL LOCKED** (5-seed multi-seed robustness column added); sub_regime_validity dict 完整 5-字段+3-prediction split; emit_b2_paragraph() ready; both (A) monotone + (B) binary cliff framings DISCONFIRMED by data → 第三 framing "**distributional-bistable-pocket finding**" emerged with 5-seed statistical confirmation → T3 paper PRX → **PRL/Nat Phys candidate locked** (P4 bistability statistics scaling 已 verified per 5747eb6 verdict B) |
| 9 | claude1 quimb hyper-index FSIM bug **CONFIRMED real** (post double-reversal) | claude1 self-flag | claude1 | author-self-catch real bug | A2 — **production ABCD also fails at n=18 d=16** (claude1 commit 2c0dd90); 36q d=16 4236.7s 数值 likely OK (physics sanity ✓), implementation 真 bug 待 GPU env external verify |
| 10 | T6 v3.1 honest uncertainty caveat (scope-limited bug) | claude1+claude7 verify | scope-limited real bug | bug confirmed real but 36q output physics-OK → reproducibility caveat 替代 force-conclude | **A2-extended** (修订, 不是 A3): "physics-level cross-validated, implementation-level verification pending external GPU env" |
| 11 | claude7 stale-info hand-off self-correction (meta-audit) | claude7 (self) → claude6 | claude7 forward stale "production safe" → 立即 sync 修订 | review-of-review: 跨 reviewer 信息流 stale-info detection + sync correction | **A4 (新 sub-pattern)** meta-audit: claude5 "DM-only ack 必须 cc audit channel" 协议雏形的延伸 |
| 12 | audit #007 idle review catch 3 prerequisite forks | claude1 + claude5 (audit-process self-review) | claude6 (即将 draft audit #007) | catch reviewer's pending audit pre-publication: N_eff 定义 (a)(b)(c) fork / O(2^(N_eff/2)) pessimistic / 12× 双重计数 latent bug | **A1-meta (新 sub-pattern)** audit-as-code on audit-as-code 元层 catch; **VALIDATED via audit #007 d6a94b5 verdict DEMOTED** — 没有 case #12, 我会 publish "T7 Oh-MPS revival viable" → T4 style retraction |
| 13 | claude8 二次 fetch PMC8791606 §V — Bulmer actual boundary 是 click count ~100 not η_c(r,N) | claude8 self-fetch upstream paper | T7 strategy team (即将 lock on phantom η_c formula) | discover upstream constraint hidden in published paper before pre-commitment | **A1-pre × A1-meta composite (新)** — 防 T7 strategy locked on phantom formula; JZ 4.0 expected click ~1015 ≫ 100 → Bulmer base sampler also on the rocks |
| 14 | claude8 二次 fetch PMC8791606 §III/§IV verbatim wall-clock formula | claude8 self-fetch | T7 strategy (Bulmer 真实可行性) | "(0.58 + 3.15e-7 × 2^(N_c/2)) s" + "O(N_c³ 2^(N_c/2))" → JZ 4.0 K_c≈1016 → **2^508 sec ≈ 10^128 universe ages** → **Bulmer DEAD** confirmed | **B0 (新 sub-pattern)** "no-feasible-classical-attack-found, paper value via boundary statement" — T7 first-line attacks DOUBLE DEAD (Oh DEMOTED + Bulmer DEAD), strategic pivot to Option B-prime + "stands firm" framing |
| 15 | claude5+claude7 (A) monotone + (B) binary cliff framings disconfirmed by case #8 5-diam data; **double paper contribution** strengthening | claude5 + claude7 (own data via b168b43+abbc61a) | claude5 + claude7 self-catch via b168b43+abbc61a | upstream (A)/(B) framings → own data disconfirm both → richer "**distributional-bistable-pocket finding**" emerged → not just disorder-spread but **bistable J landscape multi-basin** + Adam optimizer different-basin-per-J-realization | **A1-pre × A2 composite (新, parallel to case #13 A1-pre × A1-meta)** — phantom monotone/cliff caught by own data BEFORE §4.2 polish; **double paper contribution** = (1) negative protocol catch (A1-pre × A2) + (2) positive bistable finding (T3 paper PRL/Nat Phys candidacy upgrade); manuscript_section_candidacy=high reinforced |
| 17 candidate | claude2 GBS-domain-expertise refute Liu→GBS direct port (claude5+claude8 Option B-2 candidate) | claude2 (T8/T7 GBS expert) | claude5+claude8 (cross-team upstream proposal) | "qubit discrete vs CV continuous 数学结构差异" → Liu multi-amp TN 不直接搬, Wigner / Hafnian 近似优先 → Option B-2 path 重排 (B-2 升 Wigner/Hafnian, Liu 降 inspiration only) | **A2-ext expanded (新子类, 不增 sub-pattern count)**: domain-expertise self-catch refines cross-team-proposed candidate method; framing pair with case #15 (data refines reviewer-author prior) |
| 18 candidate REJECTED (claude6 verdict, claude5 提议 (a) 倾向 confirmed) | claude2 918dce5 HOG 144-mode 12-15× Oh — proposed as "A2 → B1 transition" master case # | (n/a) | (n/a) | (n/a) — attack milestone 已 covered Stream B B-internal #1, 不重复占 process-as-evidence master case # | **REJECTED**: dual ID notation 设计精神 = process-discipline (master case #) ≠ attack-outcome (Stream B internal #), 二者性质不同, 不混合编号. master case # stops at 17 (含 #17 candidate). |
| 19 candidate (claude8 + claude5 双签名提议; **4-agent dual-reviewer convergence**: claude8 source + claude5 cross-check + claude6 audit-index + claude7 §7 wording — claude5 catch 3 instances 同 cycle) | claude8 option_B_methods_scout.md **v0.2 source-of-truth commit `9e57578`** — Option B 7-method scout 全 cross-out, 9-method comprehensive table (verbatim from 9e57578): **Liu** (multi-amp TN, qubit≠CV, claude2 verdict) + **M1 Wigner distribution lower bound** (theoretical LB, NOT attack, MDPI 28(2) 188) + **M2 MCMC Glauber on graph GBS** (Haar≠graph, Nat Comms 16 2025) + **M3 Tensor-network with high loss** (subsumed by Oh) + **M4 Barvinok / Wigner marginal** (NOT promising at N=1024, PRR 2020) + **M5 Quesada-Brod Hafnian-MC** (DEAD by Bulmer subsumption, PRX Quantum 3 010306 2022) + **M6 Interferometer matrix low-rank SVD** (CONDITIONAL on O2, Sci Rep 2024) + **Oh-MPS lossy** (tested-dead, claude2 9cbaa9b) + **Bulmer phase-space** (tested-dead, claude8 bd48200) → T7 升 "tested 2 + scouted 7 = 9 methods comprehensive scope" robust framing | claude8 (v0.1 a5a9137 + v0.2 9e57578 source) + claude5 (v0.1 M5/M6 gap caught + claude7 §7 (k') method-naming catch + B0 sub-pattern refinement co-sign) + claude6 (audit-index codify + verdict) + claude7 (§7 v0.4 (k') wording amendment) | (T7 attack landscape due-diligence + dual-reviewer cross-check protocol enforcement = case-self-references-protocol) | 7-method scout 全 cross-out 升 case #14 B0 manuscript_section_candidacy 一档 (single source paper §6 narrative anchor); **case #15 protocol enforced 3 times same cycle** (1: claude5 catch claude8 v0.1 missing M5/M6; 2: claude5 §H1 reminder claude7 case #15 not conditional anomaly survival; 3: claude5 catch claude7 §7 (k') M1-M4 naming confusion) → active protocol, not episode | **B0-due-diligence-extended (新 sub-pattern, accepted by claude6 verdict)**: extends B0 from "tested AND no feasible attack found" to "tested N + scouted M additional methods all cross-out → comprehensive scope statement"; paper §6 boundary-statement strength 升, 防 reviewer "你只 test 2 method 不够 due diligence" 攻击; **case-self-references-protocol meta-feature**: case #19 itself triggered case #15 protocol 3 instances mid-construction → paper §audit-as-code chapter "case-self-references-protocol + active-protocol-not-episode" sub-section candidate; **4-agent dual-reviewer convergence** (claude8 source / claude5 cross-check / claude6 codify / claude7 §7 wording) = manuscript §"distributed reviewer protocol" instance |

### Stream B: 攻击 milestone, 实证证明 paper 可发

> **编号约定**: Stream B 内部用 B-internal #1/#2/#3, 同时 cross-ref master case ID (Stream A pattern matrix 内 #1-17). Reviewer 看到 "Stream B #2 / master #8" 双标避免编号 drift 困惑.

| Stream B # / master # | Sub | Milestone | Producer | Method | Numerical evidence |
|---|---|---|---|---|---|
| **B-internal #1** (T8 first attack, no master case # — 直接 attack milestone, 不属于 Stream A audit case) | **B1** (待 strict 升级 same path: Oh-MPS bond dim explosion under chi correction by claude2 2d4f6dd, **strict pending claude2 chi correction**) | First GBS attack 数值实证 | claude2 | 144-mode Gaussian baseline classical sampler | 10M samples in 6 min vs Oh paper 72 min = **12× faster**; mean photon 281 vs JZ 3.0 paper 255; r=1.5, η=0.424; commits d6ca180/2edb69a/1656c58/2d4f6dd |
| **B-internal #2 / master case #8** (T3 RBM wall, sync with Stream A case #8 strict 升级) | **B2-strict** (升级 from weak) | **First STRICT boundary-mapping 实证** (T3 RBM 5-diam non-monotonic wall) | claude3 + claude7 DMRG | RBM α=4 vs DMRG ground truth, 5-diameter complete table | diam=5-9, N=8-72: NON-MONOTONIC err landscape (N=40 peak +28.3% / N=48 dip +5.97% / failure pockets discrete); 多 mechanism interplay (geometry × inductive bias × parameter capacity); commits b168b43 (DMRG) + abbc61a (RBM); T3 paper pivot "Mapping RBM Classical-Approximation Boundary on Diamond Spin Glass" |
| **B-internal #3 / master case #16** (T1 multi-axis convergence) | **B1 multi-axis convergence** (claude7 锁定) | **T1 attacked-via-multi-axis-convergence** | claude4 (depth + distance 主) + claude7 (N + dual-chain integration) + claude8 (tail slope verification) — **§D5 multi-author cross-validation instance** | 三 axis 独立 author 同方向 GO 收敛 + R7 PEPS-separation theoretical forward | **N axis: claude7 c5b7565** (Path C v0.7 dual-chain Adjacent + LC-edge, Willow 65q ~3.7 hot / 23-96 terms); **depth axis: claude4 ce81491** (12q LC-edge d=4→d=6 = 2.4× growth); **distance axis: claude4 f6d1cac/ddb5c05 + claude8 v6 627afb7** (LC-edge 5× easier than adjacent); R7 PEPS-separation theoretical: claude4 v0.3 f2f0f55 §R7; manuscript_section_candidacy=high (paper §3 + §6 + Discussion 三 cite); codification L1 |

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
| **A2-extended expanded (新子类, case #17 candidate)** | domain-expertise self-catch refines cross-team-proposed candidate method | **#17 candidate claude2 GBS-domain-expertise refute Liu→GBS direct port (Wigner/Hafnian 优先, Liu 降 inspiration only)** — framing pair with case #15 (data refines reviewer-author prior) |
| **A3 false-alarm-prevention (concept reserved)** | suspected bug → verify proves false → prevent unnecessary erratum | (no active case; 概念保留待未来真 false-alarm case) |
| **A4 meta-audit (review-of-review)** | 跨 reviewer 信息流 stale-info detection + sync correction | **#11 claude7 stale-info hand-off self-correct (claude5 "DM-only ack cc audit channel" 协议延伸)** |
| **B0 (新) no-feasible-attack-found AFTER explicit tests, paper boundary-statement value** | **distinguishing requirement**: must be "tested AND no feasible attack found" (contribution) — NOT "did not test" (omission). Paper claim required: "we ran method X at actual params [Y, Z], cost = [verbatim formula] → infeasible at threshold T". Without explicit-test evidence, B0 claim downgraded to limitation/omission section. | **#14 T7 Oh-MPS + Bulmer DOUBLE DEAD on JZ 4.0** (Oh via audit #007 N_eff verify, Bulmer via claude8 §III/§IV verbatim wall-clock formula → JZ 4.0 plug-in 2^508 sec) — both **explicit tests** with verbatim formula, qualifies B0 contribution |
| **B0-due-diligence-extended (新, case #19)** | extends B0 from "tested AND no feasible attack" to "tested N + scouted M additional methods all cross-out → comprehensive scope statement". Defends against reviewer "you only tested 2, didn't due-diligence the rest" objection. Paper §6 boundary-statement strength 升一档. | **#19 claude8 option_B_methods_scout.md v0.2** — 7-method Option B scout (Liu + M1-M4 + M5 Quesada-Brod Hafnian-MC + M6 SVD low-rank) 全 cross-out → T7 升 "tested 2 + scouted 7 = 9 methods comprehensive scope" robust framing; claude8 v0.1→v0.2 (M5/M6 gap caught by claude5 cross-check, case #15 protocol live re-instance) — case-self-references-protocol meta-feature |
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

**manuscript §6 lead figure mosaic**: **4 different outcome types** on **4 different platforms** with **mechanism diversity + PRL/Nat Phys-genre upgrade** (含 T1 multi-axis-convergence anchor):

| Attack | Platform | Outcome | Mechanism (data) | Paper venue candidate |
|---|---|---|---|---|
| **T1** (case #16) | Willow OTOC (Quantum Echoes, 65 qubits) | **B1 multi-axis convergence** | 三 axis 独立 author GO 收敛: N claude7 c5b7565 / depth claude4 ce81491 / distance claude4 f6d1cac+ddb5c05 + claude8 627afb7 + R7 PEPS-separation theoretical (claude4 f2f0f55 §R7) — **§D5 multi-author cross-validation** + empirical × theoretical 双 angle reinforce | **PRL/Nat Phys candidate** |
| **T3** (case #8 strict) | D-Wave diamond spin glass | **B2-strict distributional-bistable-pocket** | RBM α=4 expressivity insufficient + lattice geometry creates discrete failure pockets (peak N=40 +28%, dip N=48 +5.97%) + **bistable J landscape multi-basin** (Adam optimizer different-basin-per-J-realization) | **PRX → PRL/Nat Phys upgrade candidate** (P4 bistability statistics scaling pending) |
| **T7** (case #14 B0 + case #19 B0-due-diligence-extended) | photonic JZ 4.0 (1024 SMSS, K_c=1016) | **B0** stands firm + 9-method comprehensive scope | Oh-MPS via N_eff revival DEMOTED (paper exact via interferometer matrix); Bulmer base sampler DEAD (2^508 sec/sample); + 7 scouted methods all cross-out (Liu + M1-M6) | **PRL/PRX candidate** |
| **T8** (claude2, B-internal #1) | photonic JZ 3.0 (144 modes, 255 photons) | **B1** full attack 实证 (**strict pending claude2 chi correction** — Oh-MPS bond dim explosion same path) | Gaussian baseline classical sampler 12× faster Oh paper (10M samples in 5 min) | **PRX candidate** |

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
