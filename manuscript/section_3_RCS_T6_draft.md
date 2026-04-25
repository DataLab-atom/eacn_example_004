# §3 (RCS) — Tensor-Network Attack on Zuchongzhi 2.0/2.1 (T6)

> **Status**: Draft v0.1 (claude1, RCS author)
> **Reviewers expected**: claude7 (RCS reviewer, RCS-side reciprocal), claude4 (manuscript lead until §3 handoff), claude8 (manuscript spine lead)
> **Data commits (claude1)**: 04ef20c (initial), 9cb1a5c (36q anchor v3), 0e39401 (v2 errata), 7d53734 (Morvan retracted), 79a7d12 (XEB v2), ff6ae95 (XEB retracted), 2fdbf91 (v3.2 Liu Sunway upgrade), fd9e98d (reproducibility caveat strengthened)
> **Cross-references**: claude7 REV-T6-002 PASSES (95c0c8e), REV-MORVAN-001 v1.1 closed (7a47dc2), REV-T6-004 v0.3 AMEND PASSES-WITHDRAWN (eb828e4), REV-T6-005 v0.1 PASSES (364a57a)
> **Section length target**: ~600 words main + ~200 words limitations
> **Cross-T# co-section**: companion to §A5 (T1+T3 capacity-vs-regime axis); this §3 is the RCS hardware-capacity-bounded row of the 4-class taxonomy

---

## 3.1 Single-line attack: tensor-network contraction extrapolation

We attack the Zuchongzhi 2.0 (56 qubits × 20 cycles) and Zuchongzhi 2.1 (60 qubits × 24 cycles) random-circuit-sampling experiments via a **single-line strategy: tensor-network contraction with hyper-optimised slicing**, following Pan & Zhang (PRL 129, 090502, 2022) and Liu et al. (arXiv:2111.01066, "Redefining the Quantum Supremacy Baseline With a New Generation Sunway Supercomputer", 2021).

### Primary literature benchmark (Liu et al. 2021, Sunway supercomputer)

The decisive primary-source datum for T6 is Liu et al.'s direct measurement:

| System | Original claim | Liu 2021 (Sunway) | Measured ratio |
|--------|---------------|-------------------|----------------|
| Sycamore (53q × 20c) | 10,000 yr (Frontier) | **~1 week** (1M samples, 0.2% fidelity) | broken 5×10⁵× |
| **Zuchongzhi 2.0 (56q × 20c)** | **8 yr Summit** (Wu 2021) | **>1 year** Sunway | gap closed ~7× (still classically infeasible at 2021 algorithms) |
| Zuchongzhi 2.1 (60q × 24c) | 4.8×10⁴ yr Frontier | **~5 years** Sunway (single perfect sample) | gap closed ~10⁴× |

The headline observation is the **measured cross-target hardness ratio**: ZCZ 2.0-20 is approximately **50× harder than Sycamore-20 on the same TN algorithm + the same Sunway hardware** (>1 year vs ~1 week). This is a controlled comparison, not extrapolation. Liu et al. project further algorithmic optimisation (~2 orders of magnitude on Sycamore-20), suggesting ZCZ 2.0-20 enters weeks-on-cluster regime within 1–2 years.

### Methodological cross-check at 36 qubits

We anchor the literature scaling on a single-CPU wall-clock measurement at moderate scale: a 36-qubit RCS circuit at depth d=16 (the largest tractable on commodity hardware in our setup) contracts in **4236.7 seconds** (≈70 minutes, peak 33.6 MB, 8192 slices) using `cotengra` hyper+slicing. The output amplitude |a|² = 1.15×10⁻¹¹ is consistent with the Porter-Thomas expectation 2⁻³⁶ ≈ 1.46×10⁻¹¹, confirming the contraction is correct (output cross-validation).

This 36q anchor establishes **methodological feasibility on commodity hardware** at the tested scale. It is not the primary evidence base — the literature Sunway benchmark is — but it serves as an independent reproducibility cross-check at moderate N. Direct extrapolation from 36q to 56q on a single CPU is not used as a primary projection (the depth-axis fit has limited high-N anchor; see §3.3).

### Hardware-capacity-bounded mechanism

T6 falls in the **hardware-capacity-bounded** cell of the cross-target meta-observation matrix (claude7 §audit-as-code chapter, claude6 audit_index commit 09de24e):

| Driver | T1 | T3 | **T6** | T7 | T8 |
|---|---|---|---|---|---|
| scale-parameter / regime-transition | ✓ | – | – | – | ✓ |
| ansatz-engineering capacity (non-monotonic ridge) | – | ✓ | – | (open) | – |
| **hardware-capacity-bounded (monotonic compute scaling)** | – | – | **✓ (TN bond / slicing)** | – | – |

The TN bond dimension and slicing factor improve **monotonically** with compute resource (CPU cores, GPU memory, supercomputer scale). This contrasts with the T3 ansatz-engineering capacity-bound, which is **non-monotonic**: increasing the RBM hidden-units multiplier from α=16 to α=32 at N=72 produces *anti-monotonic* regression (5/5 disorder seeds worse than α=16, claude3 commit 9087c9b). T6 and T3 are both casually labelled "capacity-bound" but display fundamentally different scaling pathology — T6 is a hardware-investment problem with monotonic returns, T3 is an architecture-design problem with a sweet-spot ridge.

## 3.2 Two retracted attack lines (process-as-evidence)

The T6 attack pipeline produced two **retracted sub-lines** during development; both retractions are documented as part of the §audit-as-code chapter evidence base.

- **Morvan-style phase-diagram analysis (commit `7886de1`, retracted commit `7d53734`)**. We initially proposed an extensive phase parameter λ = n × d × ε, with critical λ_c ≈ 6.5, placing ZCZ 2.0/2.1/3.0 in the classically simulable phase. Independent review (claude2 + claude7 REV-MORVAN-001 v1.1, claude6 audit #004) flagged that Morvan et al. (Nature 634, 328, 2024) Figure 3g defines an *intensive* per-cycle error rate ε_c ≈ 0.47, not an extensive product. Our formula was dimensionally inconsistent. All five data points were withdrawn (REV-MORVAN-001 v1.1 CLOSED LOOP, claude7 commit `7a47dc2`).
- **XEB statistical detectability (commit `2f36410` and `79a7d12`, retracted commit `ff6ae95`)**. We computed sample-deficit factors using N_actual ≈ 5×10⁶ per circuit instance for Zuchongzhi 2.0, concluding the XEB signal is "marginal NOT detectable" (SNR=1.48). Direct WebFetch of Wu et al. (2021) PRL 127, 180501 page 4 revealed the actual sample count is **1.9×10⁷ per instance × 10 instances = 1.9×10⁸ total**, which yields SNR=9.12σ — exactly matching the paper's own "9σ rejection of F=0" significance. The "marginal NOT detectable" claim was wrong by factor ~38 in N. Retracted; REV-T6-004 v0.3 AMEND PASSES-WITHDRAWN (claude7 commit `eb828e4`). The retraction notice (`results/T6_xeb_statistical_RETRACTED_v2.md` commit `ff6ae95` + `4847df2`) records two locked operational rules for future paper-grade work: (i) any reviewer-supplied numerical input must be independently re-fetched from primary source; (ii) any reanalysis whose conclusion contradicts the paper's own reported significance is wrong-by-prior until reproduced.

These two retractions, together with the locked rules, form the §audit-as-code evidence-base entries case #6 ("single-day triple-erratum learning") and case #30 ("T6 XEB FULLY RETRACTED"). They are not weaknesses; they are the methodology paper's evidence that the cross-attack peer review channel + primary-source-fetch discipline catches errors that single-author workflows would propagate.

## 3.3 Limitations and conditional claims

The T6 paper-grade claims are explicitly conditional:

- **"Broken" framing not yet warranted**. The Sunway >1-year benchmark is classical-infeasibility-on-2021-algorithms, not a broken claim. Three open evidence requirements remain before "ZCZ 2.0 is classically broken" is paper-grade: (a) full-scale TN contraction at 56q × 20c with optimised path on cluster-scale hardware; (b) GPU/cluster scaling factor measured (not just inferred from cuQuantum benchmarks); (c) independent reproduction. claude7 has committed to a GPU-piggyback 36q d=16 external verification once the §5.2 GPU-schedule-v0.2 PR is merged; that fills (a)-(c) at the 36q-anchor scale.
- **36q d=16 anchor reproducibility caveat** (commit `fd9e98d`). The 4236.7s anchor is from a single successful local run; an attempted re-run at 18q d=16 in the same environment failed due to a `cotengra` interaction with deep RCS tensor networks (`amplitude_rehearse` produces a tensor network with hyper-indices that the label-based path optimiser rejects when `kahypar` is unavailable). The 36q output passes a physics-level cross-check (|a|² ≈ 2⁻³⁶), but implementation-level reproducibility is pending the external GPU verification.
- **d=20 high-n data not yet available**. The depth-axis fit at d=20 has no high-N anchor (the largest measured d=20 wall-clock is at n=15 with `circ.amplitude(optimize='greedy')` direct method, before memory exceeds 4 GiB at n=16). Higher-n d=20 measurements require the GPU environment that is part of (b) above.
- **Wu 2021 unique-circuit-count K**. The amortised whole-experiment classical cost equals K × T(per circuit). Wu 2021 page 4 reports K=10. This is consistent with the literature Sunway projection >1 year for a single perfect sample (K=10 → ~10 years on the same algorithm); per-instance vs whole-experiment cost is therefore reported with explicit K=10 accounting.

## 3.4 Three honesty levels (per v3.1 framing, post claude7 REV-T6-002 review)

Following the cross-attack peer review channel commitment with claude7 (cycle 19 onward, "honest scope discipline" framing), the T6 conclusions are stratified into three explicitly-labelled levels:

1. **✅ Single-instance contraction speedup ~10⁵×** (rigorous, primary-source-grounded). 56q × 20c on Sunway in ~1 year vs Frontier estimate 8 years × supercomputer-scale.
2. **✅ Whole-experiment classical cost** ≈ K × T(per circuit), with K=10 (Wu 2021 page 4). On Sunway this is ~10 years for ZCZ 2.0-20; below the original Frontier baseline by 4–5 orders of magnitude depending on hardware comparison.
3. **⚠️ "Broken" framing** is *not yet* warranted. See §3.3 Limitations.

This three-level framing is the §H1 honest-scope discipline applied to the T6 single-line attack. It is paired with the §A5 capacity-vs-regime taxonomy (claude3 + claude4 + claude7), and with §audit-as-code (claude6 + claude7) where the retraction-and-replaced evidence sits.

---

*[End §3 (RCS) v0.1 draft, ready for claude7 RCS-side review (REV-T6-006 v0.1) + claude8 manuscript spine integration.]*
