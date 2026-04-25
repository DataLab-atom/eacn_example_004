# T2 Phase 2 — Graph-theoretic structure analysis on heavy-hex L=3,6 v0.1

> **Author**: claude6 (T2 main attack lead)
> **Status**: Phase 2 v0.1 (continuous-advance mode per user directive 2026-04-26 04:40)
> **Trigger**: T2 Phase 1 due-diligence v0.1 complete (commit 29dd447)
> **Anchor (10) primary-source-fetch discipline**: heavy-hex topology + Floquet layer model verified directly from Algorithmiq paper §II + Fig. 3
> **Sub-pattern 18 + 17 disciplines applied**: company technical document, not peer-reviewed; multi-paper-attribution-collision watch active

## 1. Heavy-hex topology canonical reference

Algorithmiq §II.A + Fig. 3a verbatim:

> "(a) A **heavy-hex-lattice 2D material** compatible with the topology of IBM's quantum computers."

> "Translationally invariant periodic lattices of **inequivalent cells**. Paradigmatic examples for heterogeneous operator dynamics are attained with (a, b, c) **two sets of vertices** or (d) **two sets of edges** resulting in the fast (V₁,E₁) or slow (V₂,E₂) propagation of the effective operator support through them."

**Vertex classification on heavy-hex (Fig. 3a)**:
- 3 vertex classes labeled **A, B, C**
- A vertices = degree-2 (linear segments)
- B vertices = degree-3 (T-junctions)
- C vertices = degree-3 (Y-junctions / branch points)
- Edge sets E₁ and E₂ (and E₃ at higher Floquet layers per Fig. 4) partition the interaction pattern

**Heterogeneity mechanism**: A/B/C vertices have **inequivalent local interaction strengths** via the {h=π/8, b₁=3π/16, b=0.25} parameters per Eq. (8)-(9) (per §V Experimental design).

## 2. Floquet layer structure

Algorithmiq §II.B verbatim:

> "A **Floquet layer U_FL** as a part of the unitary dynamics U. Typically, U_FL = Π_{E⊂ℰ} (⊗_{(q₁,q₂)∈E} u_{q₁q₂}) (⊗_{q∈V} u_q) or U_FL = Π_{E⊂ℰ} (⊗_{(q₁,q₂)∈E} u_{q₁q₂} u_{q₁} u_{q₂})"

where u_{q₁q₂} = native two-qubit gate, u_q = single-qubit gate.

> "The difference between the **scrambling (U₁)** and **unscrambling (U†₂)** parts of the dynamics U† = U†₂ U₁ is in the presence of **scattering on some of the vertices or the edges in U†₂**. If U_FL is a Floquet layer in U₁, then its **scattered version U_FLS** in U₂ reads U_FLS = (⊗_{q∈V_S} v_q) U_FL (⊗_{q∈V_S} v†_q) or U_FLS = (⊗_{(q₁,q₂)∈E_S} v_{q₁q₂}) U_FL (⊗_{(q₁,q₂)∈E_S} v†_{q₁q₂})"

**KEY OBSERVATION (axis 2.1 attack opportunity)**: U₁ and U₂ are nearly identical Floquet layers with U₂ adding scattering operators v_q (or v_{q₁q₂}) at scattering sites V_S (or edges E_S). The OLE structure ⟨U₁ U†₂⟩ = nearly-identity-perturbed-by-scattering — this is **explicit time-reversal-with-perturbation** structure.

## 3. Algebraic structure of OLE = U₁ U†₂

If V_S = ∅ (no scattering), then U₁ = U₂ and OLE = ⟨U₁ U†₁⟩ = ⟨I⟩ = 1 (trivially).

If V_S ⊆ V (subset of vertices scatter), then:

```
OLE = ⟨U₁ U†₂⟩ = ⟨U₁ (⊗_{q∈V_S} v_q) U†_FL... U†_FL (⊗_{q∈V_S} v†_q)⟩
```

Per Algorithmiq Eq. (31), this relates to OTOC at infinite temperature ⟨[G, O₀(t)]† [G, O₀(t)]⟩_{ϱ_∞}.

**Attack-relevant algebraic property**: U†₂ inverts U₁ exactly except at scattering sites. The "effective" non-trivial dynamics is **localized at scattering sites V_S** propagated via the U₁/U†₂ chain. **Hidden structure attack hypothesis**: if V_S has **automorphism symmetry** with respect to the heavy-hex graph, OLE may factorize via group-representation decomposition into smaller invariant subspaces.

## 4. Graph automorphism analysis approach (axis 2.1 from kickoff)

### 4.1 Heavy-hex automorphism group basics

Heavy-hex lattice = heavy-hexagonal IBM topology. For a finite N-qubit heavy-hex patch:
- **Translation symmetries**: limited by boundary
- **Reflection symmetries**: vertical/horizontal mirror axes (depending on cut)
- **Rotation symmetries**: 60° rotations (full hex has C₆; heavy-hex has C₂ from connectivity additions)

**Full automorphism group of finite heavy-hex patch**: typically a small finite group (depending on boundary conditions); for periodic-boundary heavy-hex it's larger (translation × point-group).

**For Algorithmiq experiment** (per §V): L=3, 6 Floquet layers on heavy-hex; experiment runs on IBM Heron 133q. Specific patch boundary conditions = TBD (need to extract from Fig. 4 detailed inspection or supplementary materials if released).

### 4.2 Symmetry-breaking by scattering sites V_S

If scattering sites V_S = {single vertex} → C_v automorphism subgroup (vertex stabilizer)
If V_S = {set of vertices} → smaller subgroup
If V_S has C_n rotational symmetry within the heavy-hex automorphism group → OLE factorizes into n invariant subspaces

**Attack opportunity**: if Algorithmiq's V_S choice happens to be C_n-symmetric within heavy-hex automorphism group, classical methods can exploit n-fold reduction in effective dimension.

### 4.3 Time-reversal sub-symmetry

OLE = U₁ U†₂ has **explicit time-reversal-with-perturbation** structure. Per BlueQubit unswapping precedent (canon entry per README line 161), peaked circuits (specifically constructed time-reversal-rich circuits) were broken via reversal mapping. **Hypothesis for T2**:
- Algorithmiq's OLE circuit may admit **time-reversal mapping** that simplifies classical computation
- Specifically: the "unscrambling" U†₂ part is largely U₁ inverse → effective dynamics is **scattering-localized** at V_S, not full Floquet expansion

### 4.4 Mirror symmetry detection

For heavy-hex with periodic boundary conditions (Algorithmiq's likely setup per "translationally invariant"):
- A/B/C vertex labeling per Fig. 3a creates 3-coloring of vertices
- Each color class has its own invariant subspace under automorphism action
- 3-color symmetric scattering V_S = {1 of A + 1 of B + 1 of C} → 3-fold factorization

## 5. Pauli-weight bound argument (cross-cite axis 2.3 SPD)

Per Algorithmiq Table I (page 14):
- N_q = 70, L = 6, b = 0.25 → median Pauli weight w_m = 39, exact memory ~31 GB

**Pauli-weight scaling for heavy-hex**:
- Floquet expansion w(L) grows with L per gate fan-out
- For heavy-hex degree-3 vertices, single-step fan-out = 3-4 neighbors
- L=6 → potentially w_m = O(degree^L) = O(3^6) ≈ 729 if uniformly expanding, but Algorithmiq's empirical w_m = 39 suggests **substantial Pauli sparsity**
- This sparsity is the **structural opening** for SPD-class methods at N_q > 70 + b > 0.25

**Extrapolation hypothesis** for IBM Heron 133q:
- If w_m scales sub-linearly with N_q (per Algorithmiq table N_q=49 → w_m=19; N_q=70 → w_m=21 at L=3) → 133q L=3 may have w_m ≈ 25-30
- Memory cost scales C(N_q, w_m) × 4^w_m for exact Pauli enumeration → at N_q=133, w_m=30, this is **C(133,30) × 4^30 ≈ infeasible**
- BUT: if probabilistic Pauli sampling (Algorithmiq §VI.C) with N_P=1 limit (their empirical optimum) → memory dominated by single-string tracking → **feasible at 133q L=3**
- Cross-cite to claude4 T1 SPD infrastructure (be999f7) — same paradigm, same code-base extension

## 6. Belief-propagation TN axis (cross-cite axis 2.4)

Per Algorithmiq §VI.A:
> "[Belief-propagation] efficacy is essential for looped tensor networks, especially for **large loops** in which the exact tensor contraction often assumes prohibitive costs"

> "For tougher cases of **numerous tight loops, such as on a square lattice topology**, one can resort to the loop series expansion"

**Heavy-hex topology characteristics**:
- Loops in heavy-hex are **6-cycles minimum** (heavy-hexagons themselves)
- Smaller than square lattice loops (4-cycles)
- BUT: heavy-hex has fewer loop densities than square → potentially better BP regime

**Attack hypothesis**: **BP + loop series expansion may be more tractable on heavy-hex** than Algorithmiq estimates if (a) we restrict to single Floquet layer L=1 (known easy) + (b) verify loop correlation decay matches BP convergence criterion.

## 7. NQS axis (axis 2.2 NEW gap)

Algorithmiq's classical methods table (§VI) does NOT include NQS. **This is a methodological gap** in their analysis — Mauron-Carleo NQS is the strongest known classical method for D-Wave heterogeneous spin glasses (T3 cross-attack reference per case #36 P3-CONFIRMED-Sub-C track-record).

**Heterogeneous Floquet operator dynamics ↔ heterogeneous spin glass dynamics** structural similarity:
- Both have non-uniform local interaction strengths
- Both have **localized regions** (Anderson localization-style sub-domains)
- t-VMC + Jastrow-Feenberg NQS may be applicable

**Attack hypothesis**: NQS-on-heterogeneous-Floquet may achieve sub-exponential cost in V_S | + bounded entanglement region scaling.

## 8. 4-axis attack opportunity refinement (post Phase 2)

| Axis | Phase 2 finding | Concrete attack scaling | Cross-T# canon |
|------|----------------|-------------------------|----------------|
| 2.1 Hidden structure | OLE = U₁ U†₂ explicit time-reversal-with-perturbation; A/B/C vertex automorphism may give 3-fold factorization | C_n group decomposition × scattering-site-localized dynamics | BlueQubit unswapping precedent |
| 2.2 NQS localized regimes | NOT in Algorithmiq's classical methods; heterogeneous Floquet ≈ heterogeneous spin glass structural similarity | Mauron-Carleo t-VMC scaling (4 GPU 3 days for 128q) | Mauron-Carleo + Carleo-Cirac NQS canon |
| 2.3 SPD operator dynamics | Pauli-sparsity w_m sub-linear scaling; probabilistic Pauli sampling (Algorithmiq §VI.C N_P=1 optimum) extends to 133q | Memory-bounded by single-string tracking + N_q L iterations | Begušić-Gray-Chan SA 10 (2024) + claude4 T1 SPD code |
| 2.4 BP+PEPS | Heavy-hex loops 6-cycles (smaller than square 4-cycles), better BP regime; BP + loop series expansion | Bond-dim grows with L Floquet layer, but heavy-hex loop density favors convergence | Bermejo 2026 PEPS bond dim |

## 9. Status + next steps

- ✅ Phase 1 primary-source-fetch + due diligence COMPLETE (commit 29dd447)
- ✅ Phase 2 graph-theoretic structure analysis COMPLETE (this commit)
- 🔄 Phase 3: method-class deployment — start with axis 2.3 SPD extension to N_q=133 leveraging claude4 T1 SPD infrastructure (be999f7)
- 🔄 Phase 4: 4-step §D5 cross-validation strength ladder applied to T2

**Continuous-advance mode**: starting Phase 3 SPD extension next tick. Will need claude4 T1 SPD code-base familiarization + Bermejo 2026 PEPS bond-dim methodology cross-reference.

**Sub-pattern 18 reminder**: this paper is Algorithmiq company document Nov 2025, NOT peer-reviewed, NO arXiv ID — sub-pattern 18 v0.6 naming-correction discipline applies. Any onward citation requires "Algorithmiq company technical document Nov 2025, not peer-reviewed" annotation.

**Reviewer ping anticipation post-Phase 3**: claude4 (SPD cross-cite + T1 infra leverage), claude7 (Morvan-trap-checklist + framework-self-reference), claude5 (ground-truth verify if v0.3 cites Algorithmiq numbers).
