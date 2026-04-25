# T2 — Algorithmiq Heterogeneous Materials Attack Kickoff Plan v0.1

> **Author**: claude6 (T2 main attack lead per allocation v2)
> **Status**: kickoff plan v0.1 (continuous-advance mode per user directive 2026-04-26 04:40)
> **Target**: Algorithmiq heterogeneous quantum materials operator dynamics (IBM Quantum Developer Conference 2025.11 announcement; arXiv + Quantum Advantage Tracker 2025.11 submission)
> **Hardware**: IBM Heron 133-qubit
> **Independent verification**: Flatiron Institute (classical-difficulty validated)
> **README anchor**: T2 entry lines 32-43

## 1. Target characterization

**Physical system**: Heterogeneous quantum material operator dynamics with non-uniform regional locality, disorder + irregular connectivity dominating information flow.

**Algorithmiq's claim chain**:
1. Material has different regional local properties (heterogeneity)
2. Disorder + irregular connectivity → information flow patterns hard for classical methods
3. Flatiron independent verification: classical methods cannot match quantum simulation accuracy in reasonable time
4. Algorithmiq's IQM Quantum Echo / NQS-style method achieves the simulation

**Hardness assertion structure** (per README):
- 异质性（heterogeneity）→ standard uniform-method assumptions break
- 无序（disorder）→ standard ordered-lattice methods break
- 不规则连接性（irregular connectivity）→ standard regular-lattice methods break
- → claim: combinatorial of these features defeats classical methods

## 2. Attack target candidate axes (4 mechanisms per README)

### 2.1 Hidden exploitable structure in Algorithmiq's designed model

Pattern: BlueQubit "peaked circuits" were broken via unswapping reversal. Similar question: does Algorithmiq's designed model contain implicit symmetries / structures discoverable via:
- Mirror symmetry analysis of the operator dynamics
- Time-reversal pattern detection (similar to Quantum Echoes T1 OTOC sensitivity to time-reversal)
- Lattice-axis hidden permutations
- Connection-graph-symmetry decomposition

**Tools**: graph-theoretic analysis of the connectivity matrix; exhaustive sub-graph automorphism check.

### 2.2 NQS in localized regimes

Heterogeneity often produces localized regions (Anderson localization sub-domains). NQS may perform well in localized regimes with sufficient ansatz capacity. Path:
- Identify locality structure regions of Algorithmiq's heterogeneous lattice
- Apply Mauron-Carleo t-VMC + Jastrow-Feenberg NQS (per cross-attack canon entry)
- Test across parameter range to find regions where NQS error <ε threshold

**Cross-attack reference**: case #44 universal applicability + #65 Step-4-ladder cross-paper method-class extension — NQS is method-class diversity option.

### 2.3 SPD (Sparse Pauli Dynamics) for operator dynamics

Operator dynamics → observable estimation via SPD direct route. SPD has worked for T1 Quantum Echoes (claude4 main attack) — same paradigm applies to T2.

**Cross-attack reference**: SPD canon entry (Begušić, Gray, Chan SA 10 2024 + Begušić & Chan PRXQ 6 2025) explicitly listed as T2 + T9 candidate.

**Cross-cite to claude4 T1 work**: claude4's SPD scaffolding (be999f7 threshold_judge_wrapper) provides foundation; T2 attack can leverage same code-base infrastructure with T2-specific parameters.

### 2.4 PEPS + belief propagation untested on Algorithmiq's new model

Algorithmiq's model is newly designed → PEPS + belief propagation hasn't been tested on it. Direct application of:
- T1-style PEPS bond-dimension analysis (Bermejo 2026 framework)
- Cross-attack reference: case #38+#41+#43+#48 4-step §D5 cross-validation strength ladder applied to T2

## 3. Cross-T# leverage from existing canon

### 3.1 Direct method-class candidates

Per README cross-attack canon entries (lines 154-160):
- **SPD**: Begušić, Gray, Chan SA 10 (2024) + PRXQ 6 (2025) — T1 + T2 + T9
- **Pauli Path + 噪声稀疏性**: Schuster-Yin-Gao-Yao 2024 — T1 + T2
- **MPO Heisenberg Evolution**: Anand-Temme-Kandala-Zaletel 2023 — T2 + T9

### 3.2 Cross-T# meta-pattern leverage

Per audit_index canonical (commit 6feb785) 4-class cross-T# taxonomy (refined per claude7):
- **Class (1) scale-parameter-driven regime-transition** (T1+T8 #20+#24): NOT primary T2 framework axis
- **Class (2) ansatz-engineering capacity-bound** (T3 #26+#37): Mauron-Carleo NQS approach class fits
- **Class (3) primary-source-fetch hardware-capacity** (T6 #31): primary-source verify for IBM Heron 133q + Algorithmiq paper
- **Class (4) dual-impl-via-different-algorithm-same-target** (T8 #38+#41+#43+#48): apply 4-step §D5 cross-validation strength ladder to T2 (NQS × SPD × PEPS × MPO Heisenberg = 4 distinct methods)

## 4. Attack roadmap v0.1

**Phase 1 — primary-source-fetch + reproducibility-due-diligence** (anchor 10 baseline):
- WebFetch Algorithmiq arXiv submission + IBM Quantum Developer Conference 2025.11 talk slides if available
- Flatiron independent verification reference identification
- Hardware specifications: IBM Heron 133q + native gate set + connectivity graph
- All cited numbers verbatim quotes captured

**Phase 2 — graph-theoretic structure analysis** (axis 2.1):
- Connectivity graph construction from Algorithmiq specifications
- Automorphism analysis for hidden symmetries
- Time-reversal / mirror-symmetry detection
- If hidden structure found: structural BREAK candidate (similar to BlueQubit unswapping)

**Phase 3 — method-class deployment** (axes 2.2-2.4):
- NQS (Mauron-Carleo) on heterogeneous lattice subdomains
- SPD on operator dynamics (leverage claude4 T1 infrastructure)
- PEPS + belief propagation
- MPO Heisenberg evolution as cross-validation method

**Phase 4 — 4-step §D5 cross-validation strength ladder** (case #38+#41+#43+#48 paradigm):
- Step 1 different-algorithm-same-target: 4 method-classes above
- Step 2 bytewise-cov-alignment scalar invariant: physical observable cross-method match
- Step 3 TVD-below-noise-floor: distribution-level cross-method TVD
- Step 4 dual-method-orthogonal-estimator: orthogonal estimator-class within each method

**Phase 5 — paper §audit-as-code integration**:
- T2 attack §section anchored in §audit-as-code.D.2 cross-cite chain
- Honest-scope §H1 disclosure per 5-axis family
- 5-standard reviewer-discipline applied (3-layer + Morvan-trap + primary-source-fetch + paper-self-significance + commit-message-vs-file-content cross-check)

## 5. Reviewer protocol (anticipated)

Per project §audit-as-code framework + cross-T# review pattern:
- **Path A (informal verify)**: claude6 self-fetch + verify-text + verify-physics + broadcast (case #4 Morvan audit precedent)
- **Path B (REV-formal)**: cross-agent reviewer assignment via task broadcast
- **Path C (paper-extraction verify chain)**: integrate §audit-as-code chapter cross-cites

**Anticipated reviewers** (per allocation v2 + project pattern):
- claude4 (T1 SPD reviewer cross-cite, since SPD shared T1+T2 method-class)
- claude7 (general framework + Morvan-trap-checklist)
- claude5 (ground-truth via primary-source if needed)
- claude1 (content-completeness axis if §3 RCS T6 framing applies)

## 6. Status + next steps

- **v0.1**: kickoff plan (this commit, claude6 main attack lead)
- **v0.2**: Phase 1 primary-source-fetch + reproducibility due diligence
- **v0.3**: Phase 2 graph-theoretic structure analysis
- **v0.4+**: Phase 3-5 method-class deployment + ladder + paper integration

**Continuous-advance mode**: starting Phase 1 immediately (primary-source-fetch via WebFetch arXiv ID once located).

**Open question**: arXiv ID for Algorithmiq submission not directly cited in README. Need WebFetch on Algorithmiq company website / IBM Quantum announcement to locate. claude5 ground-truth ping may be needed if README pre-dated publication.
