# T1 Scaling Law Summary: OTOC^(2) SPD Feasibility

> Compiled from all Phase 1-3 experiments. All noiseless unless noted.

## w_min for <5% relative error on OTOC^(2) (noiseless)

| System | Topology | depth | w_min | w/n | terms | time | source |
|--------|----------|-------|-------|-----|-------|------|--------|
| 4q | 2x2 | 4 | 4 | 1.00 | 255 | 0.4s | Phase 1 |
| 6q | 2x3 | 4 | 4 | 0.67 | 63 | 0.01s | Phase 1 |
| 8q | 2x4 | 4 | 6 | 0.75 | 1023 | 0.7s | Phase 1 |
| 10q | 2x5 | 4 | 4 | 0.40 | 255 | 0.1s | Phase 3b |
| 10q | 2x5 | 6 | 8 | 0.80 | 61439 | 337s | Phase 3 |
| 12q | 3x4 | 4 | 6 | 0.50 | 3839 | 6s | Phase 3b |
| 12q | 3x4 | 6 | 6 | 0.50 | 3839 | 6s | SPD full |
| 14q | 2x7 | 4 | 6 | 0.43 | 4095 | 8s | Phase 3b |
| 16q | 4x4 | 4 | 4 | 0.25 | 233 | 0.3s | SPD full |

## Key Observations

### 1. Topology Effect (most important)
- **Square grids (NxN) are dramatically easier than narrow grids (2xN)**
- 16q 4x4 d=4: w/n = 0.25 (easiest)
- 10q 2x5 d=4: w/n = 0.40
- 8q 2x4 d=4: w/n = 0.75 (hardest)
- Pattern: wider grids have shorter OTOC propagation paths → lower w_min

### 2. Depth Effect
- depth 4→6 can increase w/n from 0.40 to 0.80 (10q 2x5)
- But 12q 3x4 is stable: w/n = 0.50 at both depth 4 and 6
- Wider grids are more robust to depth increase

### 3. Extrapolation to 65q Willow (~8x8 or ~10x10)

**Optimistic scenario** (if per-arm depth ≤ 16 cycles, M/B nearby):
- w/n ~ 0.25-0.35 → w_min ~ 16-23
- terms ~ O(10^5 - 10^7)
- wall-clock ~ minutes to hours on single GPU
- **ATTACK FEASIBLE**

**Pessimistic scenario** (if per-arm depth ≥ 24 cycles, M/B distant):
- w/n ~ 0.6-0.8 → w_min ~ 39-52
- terms ~ O(10^12+)
- wall-clock ~ years
- **ATTACK INFEASIBLE without adaptive truncation**

### 4. Critical Parameters to Extract from Google Paper
1. **Per-arm cycle count** of OTOC circuit → determines depth
2. **M, B qubit positions** → determines propagation distance
3. **Willow grid dimensions** → determines topology effect
4. **iSWAP-like gate parameters** → we use generic; need exact values

## Decision Matrix

| Per-arm depth | M-B distance | Verdict | Required method |
|--------------|-------------|---------|-----------------|
| ≤12 cycles | nearby (≤4 edges) | ✅ Feasible | SPD w≤15 |
| ≤16 cycles | nearby | ✅ Likely feasible | SPD w≤20 |
| ≤16 cycles | distant (>6 edges) | ⚠️ Uncertain | Adaptive SPD |
| ≥24 cycles | any | ❌ Likely infeasible | New method needed |

*claude8 is extracting these parameters from Google Nature 2025 (DOI:10.1038/s41586-025-09526-6)*

## 5. Depth Saturation (new finding from full Phase 3)

10q 2x5 data shows w_min saturates at depth >= 5:
- d=5: w_min=8 (w/n=0.80)
- d=6: w_min=8 (w/n=0.80)
- d=8: w_min=8 (w/n=0.80) — **same as d=6!**

This means depth effect has a CEILING on narrow grids.
For square grids, the ceiling is likely even lower.

Implication: even if Willow OTOC uses deep circuits (d=8+),
the required w_min may not grow beyond the d=5-6 level.
This is moderately good news for the attack.

---

*Compiled by claude4, 2026-04-25*
*Source data: commits 78b05aa, bc65324, 9a22484, 694d65d, 1f511ee on origin/claude4*
