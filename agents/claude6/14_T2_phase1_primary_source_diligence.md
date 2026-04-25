# T2 Phase 1 — Primary-source-fetch + reproducibility-due-diligence v0.1

> **Author**: claude6 (T2 main attack lead)
> **Status**: Phase 1 due-diligence note v0.1 (continuous-advance mode per user directive 2026-04-26 04:40)
> **Trigger**: T2 kickoff plan v0.1 (commit 0163318 13_T2_algorithmiq_attack_kickoff_v0.1.md)
> **Anchor (10) primary-source-fetch discipline applied**: WebSearch + WebFetch + curl + pypdf extraction direct from algorithmiq.fi
> **Sub-pattern 17 discipline**: this is **company website PDF, NOT peer-reviewed** — accepted_canon entry must annotate "company technical document, not peer-reviewed"

## 1. Primary source identification

- **Title**: "**Loschmidt echo for probing operator hydrodynamics in heterogeneous structures**"
- **Author**: Algorithmiq
- **URL** (canonical primary source): `https://algorithmiq.fi/files/model-information-flow-complex-material-document.pdf`
- **Pages**: 15
- **File size**: 1.4 MB (1469628 bytes)
- **Local copy**: `agents/claude6/scripts/algorithmiq_loschmidt_2025.pdf` (downloaded 2026-04-26 ~04:37)
- **WebSearch result chain**: query "Algorithmiq heterogeneous quantum materials operator dynamics IBM Heron 133 qubit 2025 arXiv" → Algorithmiq company website PDF (top hit)
- **arXiv ID**: NOT FOUND via WebSearch (paper appears to be company technical document, not arXiv preprint at present)
- **DOI**: NOT FOUND (no journal publication identified)
- **Publication date**: November 2025 per URL path `/wp-content/uploads/2025/11/`

**Sub-pattern 17 flag**: company technical document, not peer-reviewed, no arXiv preprint. Per accepted_canon header rule + sub-pattern 18 family discipline, any onward citation must annotate "Algorithmiq company technical document Nov 2025, not peer-reviewed, no arXiv ID."

## 2. Paper structure (verbatim Table of Contents)

```
I. Introduction
II. Dynamics in the structured heterogeneous circuits
   A. Graph representation
   B. Gate-based models
      1. Models with the continuously parameterized R_ZZ-like and Mølmer-Sørensen-like native entangling gates
      2. Models with the CZ-like native entangling gates
      3. Models with the R_XX+YY and iSWAP-like native entangling gates
   C. Probing operator spreading with local and global OTOCs
III. Hydrodynamics of the operator-support density
IV. Loschmidt echo
   A. Loschmidt echo for states
   B. Operator Loschmidt echo (OLE)
   C. Measurement of OLE
      1. OLE estimation protocol
      2. Multiple-OLE estimation protocol
   D. OLE and OTOC
V. Experimental design and the case circuits
VI. Classical simulations
   A. Belief-propagation tensor-network simulations
   B. Pauli propagation method
   C. Monte Carlo Methods
   D. Statistical approach: Full-scrambling assumption
References
```

## 3. Hardware + model spec (verbatim from §V Experimental design)

- **Hardware**: IBM Heron, **heavy-hex topology**
- **Experiment runner**: "The experiment is run by IBM's team" (verbatim §V)
- **Heterogeneous structure parameters** (Eqs. 8-9 + §V):
  - h = π/8
  - b₁ = 3π/16
  - b = 0.25
  - L = 3, 6 (number of Floquet layers)
- **Noise mitigation**: "Global rescaling with respect to δ=0 used as the simplest noise-agnostic mitigation method. The noise-aware methods such as the tensor-network error mitigation (TEM) [28-30] relying on the learnt structure of the noise are being tested on complex 2D topologies" (verbatim §V)

## 4. Observable definition (verbatim from §IV.D)

**Operator Loschmidt Echo (OLE)** related to OTOC via:

```
OLE(δ²) = 1 - (δ²/2) × OTOC

OTOC = ⟨[G, O₀(t)]† [G, O₀(t)]⟩_{ϱ_∞}
```

where ϱ_∞ = (½𝟙)⊗N is the maximally mixed (infinite temperature) state.

"The OTOC can also be seen as an ensemble average over the Loschmidt echos for states. However, the OLE provides a more practical way to estimate the OTOC in the presence of noise." (verbatim §IV.D)

## 5. Classical methods spec (verbatim from §VI)

### 5.A Belief-propagation tensor-network simulations
- Self-consistent algorithm for tensor network contraction
- Originally on closed tensor networks with no open legs
- Update rule: each message i→j defined as contraction of tensor i with all messages directed to i
- Loop correlation analysis for quality check (loop series expansion for tight loops)
- Recently applied to provide Vidal-gauge of tensor-network-state (per ref [33])

### 5.B Pauli propagation method (**directly relevant to claude6 SPD attack axis 2.3**)
- Sequential gate application tracking Pauli strings + coefficients
- Transformation rule:
  ```
  R†_Q(θ) P R_Q(θ) = { P,                          if [P,Q] = 0
                     { cos(θ)P + i·sin(θ)P',        if {P,Q} = 0 }
  ```
  where P' = i[P,Q]/2

### 5.C Monte Carlo Methods (sampling Pauli strings)
- N_P max Pauli strings retained in memory
- Probabilistic sampling when limit reached: cos²(θ) and sin²(θ) selection probabilities
- "**Empirically, optimal performance is achieved when restricting the evolution to a single Pauli string (N_P = 1).** However, as the number of simultaneously tracked Pauli strings increases beyond unity, the estimated OTOC value systematically decreases toward zero, indicating the accumulation of sampling errors in the Monte Carlo approximation."

### 5.D Statistical approach: Full-scrambling assumption
- (Section content not yet extracted — page 14+)

### Memory requirements Table I (Pauli propagation, exact)

| N_q | L | b | b_p+b_c | w_m | Memory (GB) |
|-----|---|---|---------|-----|-------------|
| 49  | 3 | 0.25 | 192 | 19 | 10-14 |
| 49  | 6 | 0.25 | 192 | 34 | 10-20 |
| 70  | 3 | 0.25 | 320 | 21 | 10-19 |
| 70  | 6 | 0.25 | 320 | 39 | 10-31 |

**Critical observation**: at N_q=70, L=6 (highest in their table), Pauli propagation requires ~31 GB exact memory. **133-qubit IBM Heron full-scale memory cost not provided in their table** — this is the attack regime gap.

## 6. Algorithmiq's hardness assertion structure (verbatim §I + §II + Fig. 1)

> "Given the noise constraints that restrict the problem size, the many-body and spin dynamics far from equilibrium is considered to be the most prominent candidate for leveraging the power of quantum computation"

> "a very narrow niche is left for a physical model to combine (i) practical relevance, (ii) high classical simulation complexity, [and (iii) technological feasibility]" (Fig. 1 caption shows triangle with these three corners; the niche is at intersection)

> "The previously reported experiments that were either classically hard (•, e.g., Refs. [11, 12]) or practically-oriented (■, e.g., Refs. [13, 14]) paved the way to the emergent research area with the both properties."

> "the observation of semiscrambling dynamics are present in the heterogeneous structures, where the interaction forms and strengths are distributed non-uniformly yet periodically akin to metamaterials [15] and Kitaev materials [16]."

> "The process of operator scrambling in heterogeneous structures is generally rather involved, with no direct evidence of what role particular sites and connections play in the operator spreading."

> "The resulting time evolution of the operator contains scrambling (U₁) and unscrambling (U₂†) stages—manifesting in the destructive interference effects—that are hard to capture with the classical methods."

## 7. Attack opportunity refinement (post-Phase 1 due diligence)

### 7.1 Algorithmiq pre-empted SPD axis (axis 2.3 reframe)

Algorithmiq explicitly listed Pauli propagation method (their §VI.B, identical to SPD paradigm) as a classical-method candidate they tested. **Their Table I shows Pauli propagation memory for N_q=49 L=3 = 10-14 GB up to N_q=70 L=6 = ~31 GB.** Two implications:
- Their analysis stops at N_q=70 — **133-qubit IBM Heron Pauli propagation memory NOT explicitly addressed**
- Memory growth pattern is sub-exponential (not 4^N) due to Pauli weight sparsity — leaves room for SPD attack on full 133-qubit at large b₁ + bounded weight
- **Cross-cite to claude4 T1 SPD work** (be999f7 threshold_judge_wrapper): same Pauli propagation paradigm, T1 already has §audit-as-code-grade infrastructure that can be extended to T2 specifications

### 7.2 Belief-propagation TN axis (axis 2.4 strengthened)

Their §VI.A documents BP tensor-network method but explicitly limits it to "looped tensor networks, especially for large loops". Heavy-hex topology has small loops + structured graph. **BP + loop series expansion may be more tractable than Algorithmiq estimates** if applied with claude7's GPU schedule infrastructure.

### 7.3 NQS axis (axis 2.2 — NEW gap)

**Algorithmiq's classical methods do NOT include NQS** in §VI table of contents. NQS-on-heterogeneous-Floquet may be unexplored territory. Direct attack opportunity per Mauron-Carleo + Bermejo cross-attack canon.

### 7.4 Hidden-structure axis (axis 2.1 — graph automorphism)

Heavy-hex topology with the parameters {h=π/8, b₁=3π/16, b=0.25} for L=3,6 may have hidden symmetry / structure. Specifically:
- L=3 (3 Floquet layers) with periodic structure → time-reversal sub-symmetry
- The OLE definition includes both U₁ scrambling + U₂† unscrambling stages → **explicit time-reversal structure** (similar to Quantum Echoes T1 sensitivity to time-reversal)
- BlueQubit "peaked circuits" precedent: structured circuits broken via unswapping reveal of symmetry

## 8. Cross-T# leverage refined

| Attack axis | Algorithmiq's coverage | claude6 T2 attack opportunity | Cross-T# canon leverage |
|-------------|------------------------|-------------------------------|------------------------|
| 2.1 Hidden structure | NOT addressed | Strong (OLE = U₁U₂† structure ≈ time-reversal) | BlueQubit unswapping precedent |
| 2.2 NQS localized regimes | NOT addressed | Strong (heterogeneous → localization possible) | Mauron-Carleo NQS canon |
| 2.3 SPD operator dynamics | Pre-empted (their §VI.B) but limited to N_q ≤ 70 | Medium (extend to N_q=133 + claude4 SPD infra) | Begušić-Gray-Chan SA 10 (2024) + claude4 T1 SPD code |
| 2.4 PEPS + belief propagation | Partial (their §VI.A, but limited large-loop applicability) | Strong (heavy-hex small-loop, BP + loop series may dominate) | Bermejo 2026 PEPS bond dim (claude4 T1 reference) |

## 9. Status + next steps

- ✅ Phase 1 primary-source-fetch + due diligence COMPLETE per anchor (10) discipline
- ✅ Anchor (10) sub-pattern 17 (preprint-vs-accepted-disclosure) discipline applied: company doc, not peer-reviewed
- 🔄 Phase 2: graph-theoretic structure analysis on heavy-hex + L=3,6 heterogeneous structure
- 🔄 Phase 3: method-class deployment (NQS axis 2.2 + extended SPD axis 2.3 + BP axis 2.4)
- 🔄 Phase 4: 4-step §D5 cross-validation strength ladder applied to T2

**Continuous-advance mode**: starting Phase 2 graph-theoretic structure analysis next tick. Will need claude4 T1 SPD code-base familiarization + Bermejo 2026 PEPS bond-dim methodology cross-reference.

**Open question for ground-truth ping**: Is there a follow-up arXiv preprint of Algorithmiq's paper? (claude5 ground-truth axis if needed.) Current canonical reference is company website PDF only.

**Reviewer ping anticipation**: claude4 (SPD cross-cite + T1 infra leverage), claude7 (Morvan-trap-checklist + framework-self-reference), claude5 (ground-truth verify if v0.2 cites Algorithmiq numbers).
