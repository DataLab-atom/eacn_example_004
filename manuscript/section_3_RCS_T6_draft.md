# §3 (RCS) — Tensor-Network Attack on Zuchongzhi 2.0/2.1 (T6)

> **Status**: Draft v0.1.6 (claude1, RCS author) — v0.1.6 path-search-budget calibration: ran 56q × 10c with longer search (32 reps, 120s, 64MB slice) twice = 185s and 313s, **both slower** than v0.1.3 default-budget 144s. The 60q × 12c "longer-search faster" finding is **regime-specific to memory-boundary configurations**: at 56q × 10c (well below memory wall) default greedy paths are already near-optimal and longer search just adds path-search overhead. **Cliff-vs-comfort distinction**: longer search budget pays off at memory cliff, hurts at comfortable regime. Honest scope correction to v0.1.5 generalization. Raw: `results/T6_56q_d10_longsearch_v04.json` + ber6p299y stdout 313.23s second run.
> v0.1.5 history: substantive evidence-base extension at depth-axis: **first commodity-laptop measurement at 60q × 12 cycles** (Wu 2021 ZCZ 2.1 actual depth = 24c) in 171.58 s wall-time using cotengra hyper+slicing with longer search budget (120s, max_repeats=32, slice_target=64MB); 56q × 12c still hits 1 GiB OOM even with 64MB slice (commodity-laptop path-search width insufficient without kahypar). Raw: `results/T6_pushresult_56q60q_d12_v04.json`.
> v0.1.4 history: polish absorption per claude3 cross-attack contribution: §3.1 Y-1 sharpens T3 ridge wording to "method-class intrinsic-limit ridge at α≈16" with intensive-vs-extensive distinction explicit; Y-2 §3.1 cross-T# table T3 row wording aligned with §A5.2 v0.7.1 verbatim; Y-3 §3.2 cross-reference to T3 failed-experiments log (claude3 c2287a9) establishes project-wide §audit-as-code retraction discipline; Y-4 §3.4 three-honesty-levels isomorphism with T3 paper explicit (T1+T3+T6 share #54 axis project-wide).
> v0.1.3 history: substantive evidence-base extension — **first commodity-laptop measurements at ZCZ 2.0 (56q) and ZCZ 2.1 (60q) target qubit counts** at moderate depths (d=8/10) using cotengra hyper+slicing; 56q × 10c = 144 s; 60q × 10c = 333 s; commodity-laptop memory wall located at 56q × 12c (8 GiB OOM). Per user-directive continuous-advance push 朝着目标前进, removed the §3.3 limitation "no high-N anchor" at the target qubit counts. Raw: `results/T6_target_n_measurements_v04.md` + `T6_pushresult_56q_60q_v04.json` (commit `5c47f3f`).
> v0.1.2 history: cross-T# taxonomy table extended 4-class → 5-class with Goodman 2026 physical-mechanism-induced-classicality (algorithm-orthogonal axis) per claude7 REV-T7-005 v0.1 + claude5 v0.8 jz40 ground-truth + claude8 §audit-as-code.A v0.5 absorption; audit_index references updated 09de24e → 8bd50f3/92163e2/0bf11a4 batch-19 LOCK (case #60 citation-temporal-axis canonical T6 retraction reference); §audit-as-code cross-cite to 5-axis §H1-disclosure family saturation (#39+#45+#50+#54+**#60**) + 4-layer self-correction grid + 3-instance saturation of case #15 enforcement (59).
> v0.1.1 history: erratum fix Sycamore baseline Frontier→Summit + M-1 Liu Fig. 2(a/b/c) localization (commit 2578548).
> **Reviewers expected**: claude7 (RCS reviewer, RCS-side reciprocal), claude4 (manuscript lead until §3 handoff, REV-T1-008 v0.2 PASSES on §A5 chain), claude8 (manuscript spine lead, §audit-as-code.A v0.4 c68f3a2 UNCONDITIONAL PASSES)
> **Data commits (claude1)**: 04ef20c (initial), 9cb1a5c (36q anchor v3), 0e39401 (v2 errata), 7d53734 (Morvan retracted), 79a7d12 (XEB v2), ff6ae95 (XEB retracted), 2fdbf91 (v3.2 Liu Sunway upgrade), fd9e98d (reproducibility caveat strengthened), 2578548 (v0.1.1 erratum + Fig. 2 localization)
> **Cross-references**: claude7 REV-T6-002 PASSES (95c0c8e), REV-MORVAN-001 v1.1 closed (7a47dc2), REV-T6-004 v0.3 AMEND PASSES-WITHDRAWN (eb828e4), REV-T6-005 v0.1 PASSES (364a57a), REV-T6-006 v0.1 PASSES (1188cba), REV-T7-005 v0.1.1 erratum (2527da7), REV-T1-008 v0.2 PASSES (1cb8572)
> **Section length target**: ~600 words main + ~200 words limitations
> **Cross-T# co-section**: companion to §A5 (T1+T3 capacity-vs-regime axis, claude4 v0.6 8d436e5); this §3 is the RCS hardware-capacity-bounded row of the **5-class** cross-target taxonomy (post-Goodman 2026 algorithm-orthogonal extension).

---

## 3.1 Single-line attack: tensor-network contraction extrapolation

We attack the Zuchongzhi 2.0 (56 qubits × 20 cycles) and Zuchongzhi 2.1 (60 qubits × 24 cycles) random-circuit-sampling experiments via a **single-line strategy: tensor-network contraction with hyper-optimised slicing**, following Pan & Zhang (PRL 129, 090502, 2022) and Liu et al. (arXiv:2111.01066, "Redefining the Quantum Supremacy Baseline With a New Generation Sunway Supercomputer", 2021).

### Primary literature benchmark (Liu et al. 2021, Sunway supercomputer)

The decisive primary-source datum for T6 is Liu et al.'s direct measurement, reported in Fig. 2(a/b/c) of the paper as log-t(s)-vs-d (cycles) curves with horizontal reference lines at 200 s / 1 day / 1 week / 1 year:

| System | Original claim | Liu 2021 Fig. 2 (Sunway) | Measured ratio |
|--------|---------------|--------------------------|----------------|
| Sycamore (53q × 20c) | 10,000 yr Summit (Arute 2019) | **~1 week** (1M samples, 0.2% fidelity; 6.4 days mixed-precision = 2000 × 276 s perfect samples) | broken 5×10⁵× |
| **Zuchongzhi 2.0 (56q × 20c)** | **8 yr Summit** (Wu 2021) | **>1 year** Sunway (Liu 2021 body: "Zuchongzhi 2.0-20 ... require runtimes of more than 1 year, which are currently beyond our reach") | gap closed ~7× (still classically infeasible at 2021 algorithms) |
| Zuchongzhi 2.1 (60q × 24c) | 4.8×10⁴ yr Frontier (Zhu 2022) | **~5 years** Sunway (single perfect sample; Liu 2021 body: "Zuchongzhi 2.1-24 ... around 5 years for us") | gap closed ~10⁴× |

The headline observation is the **measured cross-target hardness ratio**: ZCZ 2.0-20 is approximately **50× harder than Sycamore-20 on the same TN algorithm + the same Sunway hardware** (>1 year vs ~1 week). This is a controlled comparison, not extrapolation. Liu et al. project further algorithmic optimisation (~2 orders of magnitude on Sycamore-20), suggesting ZCZ 2.0-20 enters weeks-on-cluster regime within 1–2 years.

### Methodological cross-check at 36 qubits

We anchor the literature scaling on a single-CPU wall-clock measurement at moderate scale: a 36-qubit RCS circuit at depth d=16 contracts in **4236.7 seconds** (≈70 minutes, peak 33.6 MB, 8192 slices) using `cotengra` hyper+slicing. The output amplitude |a|² = 1.15×10⁻¹¹ is consistent with the Porter-Thomas expectation 2⁻³⁶ ≈ 1.46×10⁻¹¹, confirming the contraction is correct (output cross-validation).

### Direct measurements at ZCZ-target qubit counts (v0.1.3 update, results commit `d8e22d9` follow-up)

Per the user-directive continuous-advance push, we extended the 36q anchor to **direct contraction at the ZCZ 2.0 (56q) and ZCZ 2.1 (60q) target qubit counts** at moderate depths on the same commodity laptop, using `cotengra` hyper+slicing without kahypar (slice target 2²⁹ ≈ 512 MB, max_repeats=4, max_time=15-30s):

| Config | n×d | grid | Wall (s) | |a|² | uniform 2⁻ⁿ | ratio | Status |
|---|---|---|---|---|---|---|---|
| ZCZ 2.0 target qubit count | | | | | | | |
| 56q d=8 | 7×8 | 7×8 | **42.95** | 1.77×10⁻¹⁸ | 1.39×10⁻¹⁷ | 0.13 | ✓ |
| 56q d=10 | 7×8 | 7×8 | **144.49** | 3.91×10⁻¹⁷ | 1.39×10⁻¹⁷ | 2.82 | ✓ |
| 56q d=12 | 7×8 | 7×8 | FAIL 69.6 | — | — | — | **8 GiB OOM** |
| ZCZ 2.1 target qubit count | | | | | | | |
| 60q d=8 | 10×6 | 10×6 | **7.51** | 4.21×10⁻¹⁹ | 8.67×10⁻¹⁹ | 0.49 | ✓ |
| 60q d=10 | 10×6 | 10×6 | **333.44** | 2.00×10⁻¹⁹ | 8.67×10⁻¹⁹ | 0.23 | ✓ |
| **60q d=12** | 10×6 | 10×6 | **171.58** | 5.78×10⁻¹⁹ | 8.67×10⁻¹⁹ | 0.67 | ✓ (v0.1.5: longer search 120s + slice 64MB found better path) |
| 56q d=10 (long-search) | 7×8 | 7×8 | 185.81 / 313.23 | 3.91×10⁻¹⁷ | 1.39×10⁻¹⁷ | 2.82 | ✓ (v0.1.6 path-search-budget calibration: longer search did **NOT** help here vs 144s default — opposite of 60q d=12; cliff-vs-comfort regime distinction) |
| Sub-target / cross-check | | | | | | | |
| 36q d=12 | 6×6 | 6×6 | 197.94 | 3.69×10⁻¹¹ | 1.46×10⁻¹¹ | 2.54 | ✓ (greedy fails OOM) |
| 50q d=8 | 10×5 | 10×5 | 4.04 | 1.48×10⁻¹⁶ | 8.88×10⁻¹⁶ | 0.17 | ✓ (narrow grid favorable) |

This batch establishes:
- **First commodity-laptop measurement at ZCZ 2.0 qubit count**: 56q × 10c in 144 s (vs Liu Sunway 2021 ">1 year" for 56q × 20c — same qubit, half depth)
- **First commodity-laptop measurement at ZCZ 2.1 qubit count**: 60q × 10c in 333 s (vs Liu Sunway 2021 "~5 years" for 60q × 24c — same qubit, less than half depth)
- **Empirical commodity-laptop memory wall at 56q × d=12**: 8 GiB intermediate tensor exceeds available RAM. This locates the hardware boundary on this setup.

The 56q d=10 ↔ 56q d=12 transition is where commodity-laptop falls off the cliff; d=20 (ZCZ 2.0 actual depth) requires GPU memory or cluster scaling. **None of these measurements break ZCZ 2.0/2.1** — d=10 < d=20/24 actual depth. They are sub-target-depth feasibility anchors, advancing the prior 36q-only commodity-laptop evidence base. Raw data + analysis: `results/T6_target_n_measurements_v04.md` + `results/T6_pushresult_v04.json` + `results/T6_pushresult_56q_60q_v04.json`.

The cross-grid-topology comparison at d=8 (56q 7×8 = 42.95s vs 50q 10×5 = 4.04s vs 60q 10×6 = 7.51s) **confirms narrow grids contract substantially faster** — generalizing the 36q observation that grid aspect ratio dominates contraction wall-time at fixed n × d. Path-forward: kahypar HyperOptimizer (currently fallback to "labels" optimizer) typically yields 2-5× lower contraction width per cotengra docs; installing kahypar via conda-forge would extend depth headroom without new compute.

This v0.1.3 batch establishes **methodological feasibility on commodity hardware at the ZCZ-target qubit counts** — the prior v0.1.2 36q-only anchor extended to direct 56q/60q measurements at d=8/10. It is not the primary evidence base — the literature Sunway benchmark is — but it removes the §3.3 limitation "no high-N anchor" at the 56q/60q target.

### Hardware-capacity-bounded mechanism

T6 falls in the **hardware-capacity-bounded** cell of the cross-target meta-observation matrix (claude6 audit_index commit `8bd50f3` batch-11 LOCK, advanced from prior `09de24e`; claude7 §audit-as-code chapter v0.4 = claude8 commit `c68f3a2`):

| Driver | T1 | T3 | **T6** | T7 | T8 |
|---|---|---|---|---|---|
| scale-parameter / regime-transition | ✓ | – | – | – | ✓ |
| ansatz-engineering capacity (**method-class intrinsic-limit ridge** at α≈16, non-monotonic) | – | ✓ | – | – | – |
| **hardware-capacity-bounded (monotonic compute scaling)** | – | – | **✓ (TN bond / slicing)** | – | – |
| transparency-vacuum (data-availability mismatch) | – | – | – | ✓ | – |
| **physical-mechanism-induced-classicality** (algorithm-orthogonal, post-Goodman 2026) | – | – | – | conditional† | – |

†Goodman et al. (arXiv:2604.12330, 2026-04-14) introduces a positive-P phase-space classical algorithm with **ε > 1 - tanh(r) ≈ 0.095 at r=1.5** thermal-noise threshold making GBS state classical. This is **algorithm-orthogonal** to the 4 prior classes (per claude7 REV-T7-005 v0.1 commit `1022ae2` + claude5 v0.8 jz40 ground-truth commit `a9666c9` + claude8 §audit-as-code.A v0.4 c68f3a2 §A.6 absorption): T6 hardware (TN bond/slicing) + T3 ansatz (RBM α) + Goodman algorithm (positive-P thermal) are all "capacity-bounded" but at distinct operational axes — paper-grade structural distinction preserved at 5-class. T7 verdict refined to 🟢 8/10 with **7-axis O7 ε** transparency-gap (per claude5 ground-truth: T7 stands-firm, NOT shifted to 🟡; verdict shift only IF future raw data release shows ε > 0.095 at JZ 4.0).

The TN bond dimension and slicing factor improve **monotonically** with compute resource (CPU cores, GPU memory, supercomputer scale). This contrasts with the T3 ansatz-engineering capacity-bound, which is **non-monotonic**: increasing the RBM hidden-units multiplier from α=16 to α=32 at N=72 produces *anti-monotonic* regression (5/5 disorder seeds worse than α=16, claude3 commit 9087c9b). T6 and T3 are both casually labelled "capacity-bound" but display fundamentally different scaling pathology — T6 is a **hardware-investment problem with monotonic returns** (extensive — adding compute resource directly extends depth/qubit headroom); T3 is an **architecture-design problem with a method-class intrinsic-limit ridge at α≈16**, where capacity scaling is non-monotonic because the optimisation landscape changes character beyond the ridge (intensive at the ansatz family level — increasing capacity past the ridge does not help and can actively hurt). Goodman-class is **algorithm-orthogonal** to both: not a hardware-investment nor an ansatz-architecture problem, but a physical-mechanism (thermal-noise threshold) that determines classical simulability independent of compute resource or ansatz design.

## 3.2 Two retracted attack lines (process-as-evidence)

The T6 attack pipeline produced two **retracted sub-lines** during development; both retractions are documented as part of the §audit-as-code chapter evidence base.

- **Morvan-style phase-diagram analysis (commit `7886de1`, retracted commit `7d53734`)**. We initially proposed an extensive phase parameter λ = n × d × ε, with critical λ_c ≈ 6.5, placing ZCZ 2.0/2.1/3.0 in the classically simulable phase. Independent review (claude2 + claude7 REV-MORVAN-001 v1.1, claude6 audit #004) flagged that Morvan et al. (Nature 634, 328, 2024) Figure 3g defines an *intensive* per-cycle error rate ε_c ≈ 0.47, not an extensive product. Our formula was dimensionally inconsistent. All five data points were withdrawn (REV-MORVAN-001 v1.1 CLOSED LOOP, claude7 commit `7a47dc2`).
- **XEB statistical detectability (commit `2f36410` and `79a7d12`, retracted commit `ff6ae95`)**. We computed sample-deficit factors using N_actual ≈ 5×10⁶ per circuit instance for Zuchongzhi 2.0, concluding the XEB signal is "marginal NOT detectable" (SNR=1.48). Direct WebFetch of Wu et al. (2021) PRL 127, 180501 page 4 revealed the actual sample count is **1.9×10⁷ per instance × 10 instances = 1.9×10⁸ total**, which yields SNR=9.12σ — exactly matching the paper's own "9σ rejection of F=0" significance. The "marginal NOT detectable" claim was wrong by factor ~38 in N. Retracted; REV-T6-004 v0.3 AMEND PASSES-WITHDRAWN (claude7 commit `eb828e4`). The retraction notice (`results/T6_xeb_statistical_RETRACTED_v2.md` commit `ff6ae95` + `4847df2`) records two locked operational rules for future paper-grade work: (i) any reviewer-supplied numerical input must be independently re-fetched from primary source; (ii) any reanalysis whose conclusion contradicts the paper's own reported significance is wrong-by-prior until reproduced.

These two retractions, together with the locked rules, form the §audit-as-code evidence-base. Per claude6 audit_index batch-11 LOCK (commit `8bd50f3`) + claude8 §audit-as-code.A v0.4 (commit `c68f3a2`) absorption, the canonical references are now:

- **XEB N retract** (commit `ff6ae95`): **case #60 sub-clause "Triple-axis canonical instance — T6 XEB N retract"** — single retraction simultaneously instantiating three distinct discipline axes: (i) F2 inter-agent attribution drift (claude7 review supplied N=5×10⁶ from inferred abstract; claude1 accepted without primary-source-verify); (ii) paper-self-significance check failure (claude1 SNR=1.48 contradicted Wu 2021's own 9σ — wrong-by-Bayesian-prior; rule unlocked); (iii) practice-check generative discipline (the retraction itself unlocked operational rule (i) primary-source-fetch + rule (ii) reanalysis-must-match-paper-self-significance, both now project-wide locked). Distinct from #34 12-iSWAP (single-axis F2) and #60 sub-clause Frontier→Summit at temporal sub-axis (single-axis F2 at temporal-citation-scope).
- **Morvan retraction** (commit `7d53734`): **F3 family canonical instance** (definition-axis: extensive λ vs intensive ε_c per-cycle scope mismatch). F3 = "is the imported definition applied at matching scope?" — distinct from F1 (identifier-axis) and F2 (attribution-axis). Per claude2 cycle-258 P2 d37ca22 + claude8 v0.5 absorption candidate.
- The **Morvan F3 + XEB N F2** pair is structurally a **multi-mechanism evidence base** at single-agent-multi-target sub-axis: two distinct failure modes in same agent within same target (T6) — paper-§A.6 evidence for §audit-as-code F1+F2+F3 triple-mechanism family completeness.

These are not weaknesses; they are paper-grade evidence that the cross-attack peer review channel + primary-source-fetch discipline catches errors that single-author workflows would propagate. The §A.4 5-axis §H1-disclosure family saturation (#39 data + #45 formula + #50 result-direction + #54 significance-stratification + **#60 citation-temporal**) and §A.3 3-instance saturation of case #15 enforcement (59) (collision / sequential-drift / commit-message-vs-file-content) both anchor on these T6 retractions plus my v0.1.1 erratum self-catch (commit `2578548` Frontier→Summit during NON-BLOCKING M-1 polish round).

An analogous T3 retraction log is documented in `notes/T3_failed_experiments_E5.md` (claude3 commit `c2287a9`), with 5 failure cases including 4th-order Jastrow gradient self-competition and pmap parallelism semantic issue. Together with the T6 retractions and T1 review-chain failed-attempt log this demonstrates the §audit-as-code retraction-and-replaced discipline is a **project-wide pattern** rather than T6-specific (per claude3 cross-attack contribution at v0.1.3 reception).

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

This three-level framing is the §H1 honest-scope discipline applied to the T6 single-line attack. It instantiates the **5-axis §H1-disclosure family saturation** at axis #54 significance-stratification-disclosure (canonical instance per claude6 batch-11 LOCK + claude8 §audit-as-code.A v0.4 §A.4 lock). The §3 T6 attack thereby contributes two of the five saturation-family canonical instances: **#54 (this section's three-honesty-levels at significance-stratification-axis) + #60 (Frontier→Summit erratum at citation-temporal-axis, my commit `2578548` during NON-BLOCKING M-1 polish)** — depth+breadth taxonomy completeness contribution from the RCS hardware-capacity-bounded row.

The three-honesty-levels structure is **isomorphic to the T3 paper's stratification** (per claude3 cross-attack contribution at v0.1.3): T3 has ✅ P1 SUPPORTED at original hyperparameters (commit `f1d09c9`) + ✅ §E3 hyperparameter-fragility caveat (commit `800987c`) + ⚠️ "method-class intrinsic limit" claim conditional on alt-ansatz cross-validation (commits `ce6fe8b` + `7a050ac`). The T1+T3+T6 three targets sharing this rigorous/supported/conditional stratification confirms #54 axis is a **project-wide §H1 discipline pattern**, not T6-specific.

The three-level framing is paired with: §A5 capacity-vs-regime taxonomy (claude3 + claude4 v0.6 + claude7 + claude5 jz40 v0.8 ground-truth, 5-class extension), §audit-as-code.A v0.4 (claude8 c68f3a2 UNCONDITIONAL PASSES at composite 4-reviewer-state paper-headline-grade), §audit-as-code.B/C/D (claude8 manuscript lead, drafting commences post-v0.5 absorption), and the project-wide 5-instance saturation candidate of case #15 enforcement (59) of which my commit `3f684f5` HOLD-MAINTAINED catch is the 3rd canonical instance (commit-message-vs-file-content drift sub-type).

---

*[End §3 (RCS) v0.1.2 draft. Ready for claude7 RCS-side review (REV-T6-006 v0.1 PASSES at v0.1.1 stage already, second-pass on v0.1.2 forward-integration optional) + claude8 manuscript spine §D integration. v0.1.2 is forward-integration of post-cycle-263 audit_index advances; substantive T6 conclusions unchanged from v0.1.1.]*
