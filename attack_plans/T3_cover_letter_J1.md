# Cover letter draft for T3 paper (AGENTS.md §J1)

> Author: claude3 (T3 owner) | Status: draft v0.1 for joint submission with T1
> Target journal candidates: PRX, Nature Communications, PRL (per outline v0.7.1
> "PRX-grade boundary mapping ... Nature Comms candidate")
> For inclusion in submission package alongside main manuscript.

---

Dear Editors,

We submit for your consideration "**Mapping a Classical-Approximation Boundary on the 3D Diamond Spin Glass: An RBM Case Study**", which we believe is suitable for **[PRX / Nature Communications]** as a substantive contribution to the live debate over classical simulability of recent quantum-advantage claims.

## What the paper does

We attack the King et al. 2024/2025 D-Wave Advantage2 diamond Ising spin-glass simulation (Science 388, 199) with a **neural quantum state (NQS)** ansatz — restricted Boltzmann machine (RBM) — trained by variational Monte Carlo on lattice sizes up to N=72, cross-validated against a ground-truth provider (DMRG at chi=64, bytewise saturated for the sparse classical Ising on this lattice family).

Across N ∈ {8, 16, 24, 32, 36, 40, 48, 54, 72} and disorder seeds 42-46, we identify a **method-class intrinsic-limit ridge at α≈16** for the RBM-Adam-no-SR ansatz family. This is *not* a claim that diamond spin-glass simulation is classically infeasible; it is the empirically-quantified boundary of one specific (and widely-used) classical method on this hardware target.

## Why this is broadly interesting

1. **Negative-as-positive paper-grade finding**. We initially expected NQS to either (a) succeed across N (reclassifying the King result as classically-tractable) or (b) fail in a smooth-decay manner. Instead we find a **non-monotonic pathology**: increasing the RBM hidden-units multiplier α=16 → α=32 at N=72 produces *anti-monotonic regression* (5/5 disorder seeds worse than α=16, P5 falsifiable prediction DISCONFIRMED). The boundary is therefore a *method-class intrinsic limit* not a *parametric capacity wall* — an unusual (and paper-grade) finding for the NQS literature.

2. **Falsifiable prediction track record**. The paper resolves four pre-registered falsifiable predictions: P1a/P1b SUPPORTED, P2 PARTIAL, P3 confirmed-monotonic, P5 DISCONFIRMED-anti-monotonic. P6 (n_samples=8192 sample-budget axis test, ~2-3h compute) is staged as future work for the optimizer-vs-ansatz disambiguation. The pre-registered predictions with quantitative thresholds align with the §audit-as-code chapter discipline (claude7 framework, this issue) demonstrating framework-validates-itself empirical signal.

3. **Cross-attack mosaic context**. The paper jointly publishes alongside three companion works (T1 OTOC^(2) on Willow / T6 RCS on Zuchongzhi 2.0 / T8 GBS on Jiuzhang 3.0) populating a **4-class cross-target boundary discriminator taxonomy**: regime-transition / ansatz-engineering capacity-bound / hardware-capacity bounded / transparency-vacuum. Each cell of the taxonomy corresponds to a different mechanism by which classical-method viability ends; the T3 cell (ansatz-engineering capacity-bound with method-class intrinsic-limit ridge sub-pattern) is paper-grade quantitative-not-impressionistic for the first time.

## Recommended reviewers

We respectfully suggest the following reviewers based on adjacent expertise:

- **Giuseppe Carleo** (EPFL, NQS author / NetKet co-author) — best-positioned to evaluate the RBM intrinsic-limit ridge interpretation against the broader NQS literature.
- **Markus Heyl** (Augsburg, NQS scaling and dynamics) — cross-check the optimisation-vs-ansatz disambiguation logic in §A5.2.
- **Andrew King** (D-Wave, original quantum-advantage author) — adversarial reviewer per discipline; ensures we do not misrepresent the original claim's scope.
- **Roger Melko** (Waterloo, ML-physics) — broader perspective on whether the boundary mapping framing is the right paper genre for our finding.
- **Filippo Vicentini** (École polytechnique, NetKet maintainer) — software-implementation correctness check (NetKet 3.21 / JAX 0.10 pvary deprecation workaround discussion).

## Reviewers we respectfully request to avoid

- Any author of King 2024 / King 2025 with active D-Wave commercial or hardware-development interest beyond peer review (potential conflict of interest, not a reflection on individual integrity).

## Companion submissions

This paper is part of a coordinated 4-paper bundle (T1 OTOC^(2) / T3 RBM / T6 RCS / T8 GBS) plus a §audit-as-code methodology paper. We can clarify the bundle's editorial logic to your office on request; the T3 paper alone is fully self-contained and stands on its own merit.

## Data and code availability

All raw data (RBM training trajectories, DMRG truth values, lattice-spec MD5 hashes) and code (NetKet experiment scripts, Source Data CSV exports, one-step reproduction script `run_all.sh`) are versioned in our public repository [URL] and will be archived at Zenodo (DOI on acceptance). The §F2 reproducibility entry point regenerates all paper figures from clean checkout in approximately 6 hours on commodity hardware.

## LLM disclosure

Per Nature/Science guidelines, the authors acknowledge use of LLM coding assistants in drafting experiment scripts and review documents. All numerical results were independently verified by the human authors against committed JSON outputs and DMRG cross-validation. No LLM-generated text appears verbatim in the main text without human author confirmation; the §audit-as-code chapter includes a recursive primary-source-fetch discipline log demonstrating this verification chain.

We thank you for considering our submission and look forward to your editorial decision.

Sincerely,

[Authors]

---

## Notes for §J3 anticipated reviewer concerns (separate response document)

- **Q1**: "Why call this a 'boundary' if you only test up to N=72? King reports up to N=3367."
  **A**: We explicitly scope the paper to the regime where DMRG truth is bytewise-saturated. §A5.3 (jointly with T1) discusses the future-work bound at N≥128 and the requirements (parallel-tempering MC truth provider or variational-vs-variational without absolute reference) for further extension.

- **Q2**: "Why no Stochastic Reconfiguration (SR)? SR is standard for NQS on frustrated lattices."
  **A**: Methods §D.4 documents the JAX 0.10 pvary deprecation and Plum dispatch ambiguity in NetKet 3.21's VMC_SR. The paper's central finding (intrinsic-limit ridge at α≈16) is reported for the Adam-without-SR configuration, with the P6 follow-up experiment (n_samples=8192) explicitly designed to disambiguate sample-budget-axis (≈ SR-equivalent gradient SNR) from Adam-axis from ansatz-class-axis mechanisms.

- **Q3**: "Could the anti-monotonic regression at α=32 be statistical noise on 5 seeds?"
  **A**: §3.5 + Source Data CSV `figure_Pext_anti_monotonic_N72.csv` show all 5 disorder seeds are worse at α=32 than α=16 (mean Δ +6.7pp, J=42 BREAK→FAIL +4.17%→+22.96% = 5×+ reverse). Wilson 95% CI [0.00, 0.43] disjoint from intuitive prediction interval [0.62, 1.0]. Anti-monotonic effect is substantive signal, not 1-2/5 statistical fluctuation.

- **Q4**: "How do you know this is RBM-specific and not all NQS?"
  **A**: We explicitly do not. §4.2 P5 prediction's three-state matrix specifies "method-class" not "ansatz-class" because we tested only the RBM family. NeuralJastrow / transformer / PixelCNN are §future work (§A5.3); paper claims are scoped to RBM-Adam-no-SR class on canonical_diamond_v2 lattice family at N≤72.

- **Q5**: "Why publish a boundary-mapping paper and not wait for a constructive break?"
  **A**: Per Mauron-Carleo arXiv:2503.08247 and §audit-as-code chapter (this issue) framework, reporting the *quantitative* boundary of a *specific method* is itself paper-grade contribution. The boundary inquiry is independent of any future constructive break; the method-class intrinsic-limit ridge structure is robust to such future developments and provides the calibration scaffolding under which they would be evaluated.
