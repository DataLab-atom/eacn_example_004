# Tail analysis v8 — d=8 phase transition impact (summary-derived; no JSON)

> **Status**: v8 = qualitative analysis from claude4 commit `54216cd` summary
> markdown (`12q_depth_chain_LCedge_complete.md`); JSON-level Pauli term data
> NOT exported by claude4 due to 46,665 terms × ~100 bytes/entry > 4 MB
> repo-bloat concern. Quantitative tail-decay slope fit pending JSON.

---

## 12q LC-edge d=4/6/8 chain (summary numbers from claude4 ce81491 + 54216cd)

| Depth | Terms (w<=4) | Hot %  | Top-10 cum | Growth from prev | Phase regime           |
|------:|-------------:|-------:|-----------:|-----------------:|------------------------|
| 4     | 780          | 33%    | 98.7%      | —                | screening active       |
| 6     | 1,908        | 42%    | 90.3%      | 2.4×             | screening active       |
| **8** | **46,665**   | **83%**| **67.7%**  | **24.5×**        | **phase transition**   |

**Phase transition at d ≈ grid_diameter** (12q 3x4 diameter ~5):
- d < diameter: light-cone fits in grid → screening active → terms grow slowly (2.4× per 2-step)
- d ≥ diameter: light-cone fills grid → screening lost → terms grow rapidly (24.5×, comparable to narrow-grid 241×)

---

## ℓ region revision: [4, 8] → [6, 10] for d ≥ 8

claude4's specific question: does v7 lock ℓ ∈ [4, 8] need stretch to [6, 10]
to absorb d=8 phase transition?

**Quantitative analysis** (norm-based, w=4 truncation residual):

|       | d=4    | d=6    | d=8 (predicted from 24.5× growth) |
|------:|-------:|-------:|----------------------------------:|
| terms | 780    | 1,908  | 46,665                            |
| norm  | 1.000  | 0.966  | ~0.5–0.7 (estimated; needs JSON)  |
| top-10 cum | 98.7% | 90.3% | 67.7%                            |

**Norm extrapolation logic**: Top-10 cumulative dropped 99% → 90% → 68%
across d=4/6/8. The fraction outside top-100 grew correspondingly. If
the Pauli-norm distribution at d=8 follows the same exponential family
with shallower slope, the 3.4% missing-norm at d=6 likely grows to
30%+ at d=8 under the same w=4 cap.

**Implication for ℓ region**:
- **d=4**: ℓ=4 sufficient (norm 1.000) ✓
- **d=6**: ℓ=4 insufficient (norm 0.966 → 3.4% miss); ℓ=6 baseline holds
- **d=8** (phase transition): ℓ=6 likely insufficient (top-10=67.7% means
  much more weight is in tail strings beyond w=4 truncation); **need ℓ=8 minimum**
- **d=10–12**: in 12q grid, beyond grid diameter → phase-transition regime
  fully active; **need ℓ=10+** if grid-diameter-bound applies

**Revised ℓ region for paper §R5 / §A5** (claude8 proposal, claude4 ack
pending):
- **ℓ_baseline = 6**: covers d=4–6 (screening regime, norm ≥ 0.96)
- **ℓ_stretch = 10**: covers d=6–8 (transition zone, norm needs >0.95)
- **ℓ_extreme = 12+**: would be needed for full coverage of d ≥ grid_diameter

**Conditional verdict for Willow 65q (8x8, diameter ~14)**:
- IF per-arm depth d ≤ 12 (Bermejo "12 iSWAP per bond" inference, NOT
  paper-verbatim per F2 audit): **screening still active on 65q** because
  d=12 < diameter=14 → ℓ ∈ [6, 8] should still work even though 12q d=8
  showed phase transition (12q diameter ~5 << 65q diameter ~14)
- IF per-arm depth d ≥ 14: phase-transition regime → ℓ=14+ needed →
  cost O(65^14) ≈ 10^25 → Path B INFEASIBLE → must pivot to Path C
  (claude7 adaptive top-K) or accept §A5 conditional

**Combined per-arm-depth × grid-diameter conditional** (revised paper §A5
framing, joint with claude4):
"Path B fixed weight ℓ ∈ [6, 10] is feasible at Willow 65q ONLY if
per-arm depth < grid diameter. For Willow with diameter ≈ 14 and
estimated per-arm depth ≈ 12 (Bermejo §II.1.3 PEPS bond inference,
unverified at exact value), this condition is plausibly but not
certainly satisfied."

---

## What's needed to upgrade v8 from qualitative to quantitative

1. **12q LC-edge d=8 Pauli term JSON** (claude4 export 46,665 terms × pauli_string/weight/coeff_sq/sites schema) → enables direct measurement of:
   - Norm-residual at ℓ=4, 6, 8 (vs the v7 oracle 0.966 at d=6)
   - Tail decay slope (does it stay exponential or transition to power-law at d=8?)
   - Site-count distribution histogram (does the 83% hot fraction localize on grid edge or center?)
2. **24q LC-edge d=8** (likely OOM, optional) → would test diameter scaling
3. **Independent grid-diameter audit**: actual Willow grid diameter for 65q
   active subgrid — depends on whether 65q is 8x8 (diameter 14) vs 5x13
   (diameter 17) or other shape (Bermejo paper does not give specific
   subgrid layout)

---

## Cross-link to 9-class T7 / Option B framework

The phase-transition discovery shows T1 has same "X-conditional-on-Y"
structure as T7:
- **T7**: 8 classical methods fail certain + 1 (M6 SVD) conditional on O2 Haar verification gap
- **T1**: 8 dimensions vindicated + per-arm depth × grid-diameter conditional

Both targets reveal **honest scope discipline** wins over force-universality
narratives. Paper §6 unified framing: "T1, T3, T7 each reveal a different
boundary type, with each conditional on a specific experimental parameter
the relevant paper does not explicitly verify." This is the §H1 standard.

---

## File status

- **Status**: v8 qualitative analysis based on summary; JSON-level analysis
  pending claude4 export
- **Last update**: 2026-04-25 (commit `<this commit>`)
- **Cross-references**: claude4 ce81491 (depth resolved markdown),
  54216cd (depth chain complete with d=8 phase transition),
  claude8 30fa5df (v7 quantitative d=4 vs d=6),
  claude8 627afb7 (v6 distance × size matrix)
