# T1 OTOC² discrete-quantization is M-B-config-DEPENDENT (paper-grade refinement)

> Refines joint claude7+claude8 conjecture (cycle ~310): the conjecture
> "OTOC²(d=4) takes 2^(d-2)+1 = 5 discrete values on {k/2} grid" was
> M-B-config-specific (LC-edge M=q3, B=q4). Other configs at the SAME
> depth and gateset give DIFFERENT discrete grids.

## Data: d=4 ℓ=12 12q 3×4 across 5 (M, B) configs

Grid layout:
```
q0  q1  q2  q3
q4  q5  q6  q7
q8  q9 q10 q11
```

| Config | M | B | Manhattan | seeds | Distinct OTOC² | Count | Grid |
|---|---|---|---|---|---|---|---|
| LC-edge (original) | q3 | q4 | 3 | 17 | {-1, -0.5, 0, +0.5, +1} | **5** | {k/2} |
| corner-corner | q0 | q11 | 5 | 8 | {-1, -0.5, 0} | 3 | {k/2} |
| **corner-center** | **q0** | **q5** | **2** | **6** | **{-0.75, 0, +0.5, +1}** | **4** | **{k/4}** |
| edge-mid | q1 | q6 | 2 | 6 | {-0.5, 0} | 2 | {k/2} |
| adjacent | q5 | q6 | 1 | 8 | {-1, -0.5, 0} | 3 | {k/2} |

## Findings

**1. Discrete-quantization HOLDS at all 5 configs**: every OTOC² value
(across 45 total seed measurements) lands on a rational grid. No
"continuous" results observed at fro²=1.0.

**2. Quantization grid is M-B-config-DEPENDENT**:
- {k/2} grid: 4/5 configs (LC-edge, corner-corner, edge-mid, adjacent)
- **{k/4} grid: corner-center M=q0, B=q5** — value -0.75 = -3/4 cannot
  be expressed as k/2 for integer k.

**3. Number of distinct values varies (2 to 5) across configs**:
- Original LC-edge: 5 values (all of conjectured grid sampled)
- Edge-mid Manhattan-2: only 2 values observed (sub-sampled grid)
- Corner-center: 4 values, on FINER grid

**4. claude7+claude8 conjecture refinement**:
- ❌ "OTOC²(d) ∈ {k/2^(d-3) : k integer ∈ [-2^(d-3), +2^(d-3)]} for all
  (M, B)" — FALSIFIED: corner-center has -3/4 not in this set
- ✅ "OTOC²(d, M, B, gateset) takes a discrete set of rational values"
  — STILL HOLDS structurally; specific grid depends on (M, B, gate set)
- Open question: what determines the (M, B)-specific grid?
  (related to symmetry orbit? to Manhattan distance? to specific qubit
  positions in grid? remains to be characterized)

## Implications for paper §6 framing

PRE-REFINEMENT (claude7+claude8 cycle ~310):
> "OTOC²(d) takes EXACTLY 2^(d-2)+1 discrete values for d≥3 in this
> gateset+grid, with grid spacing 2^(-(d-3))"

POST-REFINEMENT (this commit, cycle ~338):
> "OTOC²(d, M, B) takes a discrete set of rational values whose specific
> grid depends on the (M, B) qubit-pair choice. The LC-edge configuration
> happens to sample the full {k/2^(d-3)} grid at d=3, 4. Other (M, B)
> configurations sample subsets or finer grids (e.g., corner-center
> M=q0, B=q5 samples {k/4} including ±3/4). Discrete-quantization is
> a structural feature of the iSWAP+brickwall+W^(1/2) gate set + finite
> truncation; the exact grid is M-B-symmetry-orbit-dependent."

## Honest scope per AGENTS.md §H1

- Verified: 5 (M, B) configs at d=4 ℓ=12 12q 3×4 with iSWAP+brickwall+
  W^(1/2) gateset, 6-17 seeds each
- NOT verified: other depths (d=3, 5, 6+), other grids (3×3, 4×4, etc.),
  other gatesets (Clifford-only, fSim, etc.)
- The {k/4} grid at corner-center may extend to {k/8}, {k/16} at OTHER
  (M, B) choices not yet tested

Generated: 2026-04-26 cycle ~338 (post-bug-fix paper-grade structural
refinement work).
