# T2 Phase 3 — SPD Extension to N_q=133 IBM Heron v0.1

> **Author**: claude6 (T2 main attack lead)
> **Status**: Phase 3 v0.1 (continuous-advance mode per user directive 2026-04-26 04:40)
> **Trigger**: Phase 2 graph-theoretic structure analysis COMPLETE (commit 9c0c240) identified axis 2.3 SPD extension as primary attack opportunity
> **Cross-cite**: claude4 SPD core + claude8 streaming wrapper (work/claude8/T1/spd_streaming_wrapper.py + threshold_judge_wrapper.py + pauli_path_baseline.py)

## 1. claude4 + claude8 T1 SPD infrastructure inventory (per anchor (10) primary-source-fetch)

Located at `work/claude8/T1/`:
- **`spd_streaming_wrapper.py`** — `SpilledTermsDict` LRU RAM + sqlite disk-spill MutableMapping for >8GB Pauli term dicts (claude8 instrumentation of claude4's `spd_otoc_core.py` via `PauliOperator.terms` injection)
- **`threshold_judge_wrapper.py`** — claude8 reverse-fit wrapper (be999f7) implementing claude5 ThresholdJudge dataclass on Bermejo §II.1.3 12q 3×4 LC-edge q0/q4 with d=4/6/8 verification
- **`pauli_path_baseline.py`** — Pauli-path Step 1 build_iswap_brickwall_circuit (44f7b6c step-stratification baseline)
- **`threshold_judge_reverse_fit.md`** — claude8 reverse-fit documentation

**Key infrastructure capability**: SpilledTermsDict allows SPD evolution at >8GB Pauli term capacity via disk-spill with LRU RAM. Spill threshold |c|² < 1e-12. This is **directly extensible to T2 N_q=133 SPD**.

## 2. T2 SPD adaptation requirements

### 2.1 Hamiltonian / circuit specification differences from T1

| Aspect | T1 (Quantum Echoes) | T2 (Algorithmiq Loschmidt echo) |
|--------|---------------------|--------------------------------|
| Topology | 12q 3×4 LC-edge (Bermejo §II.1.3) | IBM Heron 133q heavy-hex |
| Native gate | iSWAP brickwall | R_ZZ-like / Mølmer-Sørensen-like / CZ-like / R_XX+YY / iSWAP-like (Algorithmiq §II.B.1-3 — multiple gate models supported) |
| Circuit depth | d=4/6/8 (claude8 reverse-fit) | L=3, 6 Floquet layers |
| Heterogeneity | uniform | A/B/C vertex classes with {h=π/8, b₁=3π/16, b=0.25} |
| Target observable | OTOC / threshold_judge | OLE = U₁ U†₂ (Algorithmiq Eqs. 30-31) |

### 2.2 Required adaptations to claude4 SPD core

Per Algorithmiq Eq. (32) Pauli propagation transformation rule:
```
R†_Q(θ) P R_Q(θ) = { P,                          if [P,Q] = 0
                   { cos(θ)P + i·sin(θ)P',        if {P,Q} = 0 }
where P' = i[P,Q]/2
```

claude4's `spd_otoc_core.py` already implements this exact rule for OTOC (per audit_index case #47 K_required arithmetic context). T2 adaptation requires:
1. **OLE observable** instead of OTOC: `OLE = ⟨U₁ U†₂⟩` requires tracking 2 Pauli evolutions and combining
2. **Heavy-hex connectivity** instead of LC-edge: graph adjacency input
3. **Heterogeneous Floquet layer** instead of uniform: per-vertex/edge parameter dispatch

### 2.3 Memory feasibility analysis at N_q=133

Per Algorithmiq Table I (Phase 1 finding):
- N_q=70, L=6, b=0.25 → exact Pauli enumeration ~31 GB (median Pauli weight w_m=39)

For N_q=133 (IBM Heron):
- **Exact enumeration**: C(133, 39) × 4^39 ≈ infeasible
- **Probabilistic Pauli sampling** (Algorithmiq §VI.C, N_P=1 optimum): single-string tracking memory ~constant per evolution step
- **claude8 SpilledTermsDict** with disk-spill |c|² < 1e-12 threshold: **feasible at 133q L=3** by spilling sub-threshold terms to disk

**Estimated runtime** (rough): O(N_q × L × N_gates_per_layer × N_strings_tracked) per Monte Carlo realization × S realizations
- For N_q=133, L=3: N_gates_per_layer ≈ 200 (heavy-hex), N_strings ~ 10⁵-10⁶ with spill-threshold pruning
- Per-realization: minutes; S=1000 realizations: hours on laptop GPU/CPU

## 3. Phase 3 implementation roadmap

### 3.1 Sub-phase 3a: code adaptation (estimated 2-4 active work cycles)

1. Fork `work/claude8/T1/spd_streaming_wrapper.py` as `agents/claude6/scripts/t2_spd_streaming.py`
2. Implement `OLE` observable computation (vs OTOC):
   - Track two Pauli evolutions (U₁ and U†₂)
   - Compute ⟨U₁ U†₂⟩ via Pauli-string overlap with maximally mixed state
3. Add heavy-hex connectivity graph builder (133q topology)
4. Add heterogeneous Floquet layer with A/B/C vertex parameter dispatch
5. Verify smoke-test reproduces Algorithmiq's Table I N_q=49, L=3 exact enumeration baseline

### 3.2 Sub-phase 3b: extrapolation runs (estimated 4-8 active work cycles)

1. Run sub-phase 3a code at N_q=49, L=3 (matches Algorithmiq Table I) — verify ~10-14 GB exact memory baseline
2. Extend to N_q=70, L=6 — match Algorithmiq's ~31 GB benchmark
3. **Critical extension**: N_q=133, L=3 with SpilledTermsDict disk-spill — first attack run beyond Algorithmiq's analyzed regime
4. Cross-validate against Algorithmiq's published OLE values (if available in §V case circuits)

### 3.3 Sub-phase 3c: Path B Pauli sampling (estimated 2-4 active work cycles)

Per Algorithmiq §VI.C N_P=1 empirical optimum:
1. Implement Monte Carlo Pauli sampling with single-string tracking
2. S=1000-10000 realizations on full N_q=133 L=3-6
3. Compare estimator variance vs runtime trade-off
4. Cross-attack canon: matches probabilistic-Pauli-sampling-with-N_P=1-limit identification from Algorithmiq's own analysis

## 4. 4-step §D5 cross-validation strength ladder applied to T2 (per case #38+#41+#43+#48 paradigm)

If sub-phases 3a-3c produce results, apply 4-step §D5 ladder to T2:

| Step | Cross-validation level | T2 application |
|------|----------------------|----------------|
| 1 | different-algorithm-same-target (case #38) | claude6 SPD vs Algorithmiq Pauli propagation = 2 method-classes on same OLE target |
| 2 | bytewise-cov-alignment scalar invariant (case #41) | OLE numerical match to ~6 decimals on small-N regime |
| 3 | TVD-below-noise-floor (case #43) | OLE distribution-level TVD against Monte Carlo sampling |
| 4 | dual-method-orthogonal-estimator (case #48) | Hill MLE on OLE distribution + OLS log-log = orthogonal estimator-class |

## 5. Sub-pattern 18 + 17 disciplines reminder

- Algorithmiq Loschmidt echo paper Nov 2025 = company technical document, NOT peer-reviewed, NO arXiv ID
- Sub-pattern 17 preprint-vs-accepted-disclosure annotation required for any onward citation
- Quantitative anchor cross-validation discipline (per claude3 framing absorbed at batch-19 anchor (10) extension): primary-source-fetch on LOCKED content with target-specific quantitative anchor cross-validation

## 6. Cross-attack reviewer anticipation

Per cross-attack boundary mapping series (commit cbb68be):
- **claude4 (SPD cross-cite + T1 infra leverage)**: best-positioned reviewer — same SPD code-base, same Pauli-path paradigm
- **claude7 (Morvan-trap-checklist + framework-self-reference)**: heavy-hex topology + heterogeneous parameters Morvan-trap risk check
- **claude5 (ground-truth-axis)**: if v0.4+ cites Algorithmiq numbers, ground-truth WebFetch verification
- **claude1 (content-completeness + 5-standard discipline)**: file-content vs commit-message cross-check + RCS-attacker lens (since heavy-hex topology = T6 family)

## 7. Status + next steps

- ✅ Phase 1 primary-source-fetch + due diligence (commit 29dd447)
- ✅ Phase 2 graph-theoretic structure analysis (commit 9c0c240)
- ✅ Phase 3 SPD extension PLAN v0.1 (this commit)
- 🔄 Phase 3 sub-phase 3a: code adaptation start when active work cycles available

**Continuous-advance mode**: Phase 3 plan ready; actual code adaptation requires extended development cycles; deferred to next active session OR delegated to claude4 (T1 SPD owner with deepest infrastructure familiarity) if dispatch routes.

**Forward signals**:
- claude4 (T1 SPD primary author) for code-base familiarization + potential T2 extension dispatch
- claude7 for graph-theoretic + Morvan-trap pre-flight on heavy-hex L=3,6 + heterogeneous parameters
- claude5 for ground-truth verification if Algorithmiq §V case circuit values get cross-referenced

**Deferred to next session OR dispatch**: actual SPD adaptation code (sub-phase 3a) requires ~2-4 active work cycles.

**Continuous-advance contribution this tick**: Phase 3 SPD extension plan v0.1 LOCKED at paper-section-grade; cross-attack boundary mapping consolidated; Phase 1+2+3 plan complete; ready for Phase 3 implementation.
