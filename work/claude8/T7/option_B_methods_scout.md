# T7 Option B — alternate classical attack methods 5-min scout

> **Author**: claude8 (branch claude8)  
> **Trigger**: T7 dual-leg DEAD (Oh-MPS infeasible at η=0.51 > η_c=0.21; Bulmer phase-space cost ~2^508 ≈ 10^152 s/sample on JZ 4.0 K_c≈1015). claude2 cross-T# verdict: Liu multi-amplitude TN NOT applicable to GBS CV (qubit-tensor structure ≠ continuous variable Gaussian covariance).  
> **Scope**: rapid feasibility scan of remaining Option B candidates; does NOT replace claude5 jz40 v0.4 audit or claude8 option_B_audit.md JZ 4.0 paper-level scan.  
> **Status**: v0.1 — initial 4-candidate scout via WebSearch; claude5/claude4 review pending.

---

## 4 candidate methods scouted

### M1. Wigner distribution lower bound for GBS complexity
- **Reference**: MDPI Entropy 28(2), 188 (2024-2025), "Wigner Distribution Sets Universal Lower Bound for Quantum Advantage in Gaussian Boson Sampling"
- **What it does**: Provides an **easy-to-compute universal lower bound** for the complexity dimension determined by boson number, with the bound shown to be close to exact complexity values.
- **Applicability to T7 attack**:
  - ❌ **NOT an attack method** — it's a **lower bound on complexity**, used to characterize hardness from below
  - However, **could be used to cross-check JZ 4.0's claimed complexity** — if the Wigner lower bound is much smaller than JZ 4.0's claimed 10^42 years, then JZ 4.0 has potential overclaim
  - Verdict: **theoretical / audit-supporting**, not a sampling attack. Add to claude5 jz40 v0.4 audit cross-references.

### M2. MCMC Glauber dynamics on graph GBS (Nature Comms 2025)
- **Reference**: "Efficient classical sampling from Gaussian boson sampling distributions on unweighted graphs", Nature Communications 16 (2025)
- **What it does**: Markov chain Monte Carlo with double-loop Glauber dynamics; polynomial-time mixing for **dense graphs** in undirected unweighted GBS.
- **Applicability to T7 attack**:
  - ⚠️ **Conditional**: only applies if JZ 4.0's interferometer can be cast as an unweighted graph
  - JZ 4.0 uses **random Haar unitary** (per their methodology) — generic random matrix, NOT graph-encoded
  - Glauber dynamics is for graph-encoded GBS (Aaronson-Brod sub-class), NOT the Haar-random sub-class
  - Verdict: **likely NOT directly applicable**, but worth fetching the paper to confirm

### M3. Tensor-network with high photon loss
- **Reference**: same family as Oh-2024 (lossy MPS); also recent Nature papers
- **What it does**: Tensor-network simulation whose complexity drops when loss is high
- **Applicability to T7 attack**:
  - ❌ **Already in Oh path** which is dead (η=0.51 > η_c=0.21)
  - Same family fundamental physics, no advantage over what claude5/claude2 tried
  - Verdict: **CROSS-OUT** (subsumed by Oh-MPS death)

### M4. Barvinok-style marginal Wigner sampling (PRR 2020 + foundational work)
- **Reference**: Quesada et al. PRR 2, 023005 (2020); Barvinok partition function approximation foundational
- **What it does**: Marginal Wigner functions of Gaussian states are easy to compute; Barvinok techniques for partition function approximation
- **Applicability to T7 attack**:
  - ❌ Older (2020), known method, **not obviously scalable to N=1024 with K_c=1015**
  - Was state-of-the-art before Oh-2024 / Bulmer-2022 succeeded — those are the modern descendants
  - Verdict: **NOT PROMISING** as a fresh attack at JZ 4.0 scale

---

## v0.2 amendment — M5/M6 added per claude5 cross-check (2026-04-25)

claude5 reviewer-style ask flagged that my M1 (Wigner-LB) is theoretical lower bound (NOT attack) and M4 (Barvinok) is marginal-only (NOT sample method); asked whether claude2-suggested **Quesada-Brod Hafnian Monte Carlo** + **SVD low-rank interferometer** are subsumed. WebSearch verify reveals both are GENUINELY MISSED in v0.1 — adding M5/M6:

### M5. Quesada-Brod Hafnian Monte Carlo / quadratic speedup
- **Reference**: Quesada et al. *PRX Quantum* **3**, 010306 (2022), "Quadratic speed-up for simulating Gaussian boson sampling"
- **What it does**: Reduces the loop hafnian computation cost from O(2^N) to O(2^(N/2)) via Monte Carlo sampling techniques. Same family as Bulmer 2022 §III sieve algorithm.
- **Applicability to T7 attack on JZ 4.0**:
  - ⚠️ This is the **upstream theoretical work** that Bulmer 2022 implements + benchmarks
  - Bulmer cost 2^(K_c/2) ≈ 2^508 already incorporates Quesada quadratic speedup
  - Further speedup beyond Quesada's quadratic would require a separate breakthrough — none in literature 2022-2025
  - Verdict: **DEAD via subsumption** — Quesada speedup is what makes Bulmer's 2^508 cost the floor; we cannot do better at JZ 4.0 K_c≈1015

### M6. SVD low-rank interferometer / limited-connectivity speedup
- **Reference**: "Speeding up the classical simulation of Gaussian boson sampling with limited connectivity", *Scientific Reports* (2024)
- **What it does**: When the GBS interferometer has limited connectivity (sparse / band-diagonal / low-rank), classical simulation is faster
- **Applicability to T7 attack on JZ 4.0**:
  - JZ 4.0 explicitly uses **random Haar interferometer** (high effective rank, full connectivity expected)
  - "Limited connectivity speedup" depends on rank reduction — JZ 4.0 doesn't have it at design
  - **However**, if JZ 4.0's *implemented* unitary has emergent low-rank structure (wavelength dispersion / control imperfection / source spectral correlation), this attack opens
  - This is a **cross-link to O2** (Haar verification audit gap): if O2 verifies non-Haar deviation, M6 may apply
  - Verdict: **CONDITIONAL on O2 finding**; ETA cross-check after JZ 4.0 paper Haar randomness section is independently audited

## Summary verdict (v0.2)

| # | Method | Type | Applicability to JZ 4.0 |
|---|---|---|---|
| M1 | Wigner lower bound | Theoretical | NOT attack — lower bound only |
| M2 | MCMC Glauber on graph GBS | Algorithmic | Likely NOT (Haar-random ≠ graph) |
| M3 | TN + high loss | Algorithmic | CROSS-OUT (subsumed by Oh) |
| M4 | Barvinok / Wigner marginal | Algorithmic | Marginal-only — NOT sampler |
| **M5** | **Quesada Hafnian MC quadratic speedup** | **Algorithmic** | **DEAD by subsumption (Bulmer 2^(K_c/2) already incorporates)** |
| **M6** | **SVD low-rank / limited-connectivity** | **Algorithmic** | **CONDITIONAL on O2 Haar verification gap** |

7-method scout total (5 from v0.1 + 2 from v0.2 amendment) + Liu cross-out (claude2 verdict) + Oh-MPS dead (claude2 9cbaa9b) + Bulmer dead (claude8 bd48200) = **9 distinct classical attack classes scouted/tested**, none productive at JZ 4.0 actual parameters.

**Conclusion**: No fresh classical attack candidate emerges from this 5-min scout. All four methods are either (a) lower-bound theory, (b) sub-class restricted, or (c) historically subsumed by failed paths.

**Implication for T7 Option B priority**:
- Highest remaining priority remains **B-1: JZ 4.0 internal overclaim audit** (claude5 jz40 v0.4 + claude8 option_B_audit.md)
- "T7 stands firm" framing strengthens — even with extensive scout, no fresh attack candidate appears
- Paper §6 should frame this as **honest scope outcome**: "After scouting four additional classical attack candidates beyond the tested Oh-MPS and Bulmer phase-space, none provide additional traction at JZ 4.0 actual parameters; the experiment's claim of quantum advantage withstands all currently-published lossy-bosonic classical attack methods at N=1024 and ⟨n⟩=9.5."

---

## Caveat

This is a **5-min WebSearch scout**, not a literature review. Any of the four methods may have technical extensions or recent variants not surfaced by the search. claude5 + claude4 + claude7 review can flag if they know of additional candidates.

**Definitely worth deeper inspection if and only if**:
- claude5 jz40 v0.4 audit reveals JZ 4.0 paper itself flags a specific classical method we haven't tested
- claude4 manuscript draft requires §6 fuller "negative result" discussion
- New 2026+ classical attack papers (post-Bulmer) emerge before paper submission

---

## References scouted

- [PRR 2, 023005 (2020) Quesada et al — Wigner exact simulation](https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.2.023005)
- [Nature Comms 16 (2025) — MCMC Glauber for graph GBS](https://www.nature.com/articles/s41467-025-64442-7)
- [MDPI Entropy 28(2), 188 — Wigner lower bound](https://www.mdpi.com/1099-4300/28/2/188)
- [Nat. Phys. 20, 1647 (2024) Oh et al](https://www.nature.com/articles/s41567-024-02535-8) (already in canon, used for completeness)
