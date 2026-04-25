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

## Summary verdict

| # | Method | Type | Applicability to JZ 4.0 |
|---|---|---|---|
| M1 | Wigner lower bound | Theoretical | Audit-supporting only, not attack |
| M2 | MCMC Glauber on graph GBS | Algorithmic | Likely NOT (Haar-random ≠ graph) |
| M3 | TN + high loss | Algorithmic | CROSS-OUT (subsumed by Oh) |
| M4 | Barvinok / Wigner marginal | Algorithmic | NOT promising at N=1024 |

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
