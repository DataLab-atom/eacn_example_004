# T4: Sycamore Precedent — Pan-Zhang Works INSIDE Morvan Quantum Phase

**Date**: 2026-04-25
**Key insight from claude7 REV-T4-002**

## The Observation

Under Morvan et al. (Nature 634, 328, 2024) Figure 3g:
- Critical threshold: ε_c = 0.47 errors per cycle
- **Sycamore**: ε ≈ 0.33 < 0.47 → **quantum phase**
- **ZCZ 3.0**: ε ≈ 0.28 < 0.47 → **quantum phase**

Both systems are in the Morvan "quantum advantage phase".
Yet Sycamore WAS classically simulated by Pan-Zhang (PRL 129, 2022).

## What This Means

Morvan's phase transition boundary separates where XEB is a reliable
fidelity metric (weak noise) vs unreliable (strong noise). It does NOT
mark the boundary of classical simulability.

Pan-Zhang's tensor network contraction method operates **within** the
Morvan quantum phase. It doesn't need the output to be "decomposable
into uncorrelated patches" — it directly contracts the circuit tensor
network using optimized contraction ordering + slicing.

## Implication for T4

The Sycamore precedent argument is STRONGER than previously thought:
1. Sycamore (ε=0.33, 53q/20c) was broken by Pan-Zhang
2. ZCZ 3.0 (ε=0.28, 83q/32c) is at LOWER per-cycle error
3. BUT the circuit volume is much larger (83×32 vs 53×20 = 2.5x)
4. The scaling of Pan-Zhang cost with volume is the key question

The attack does NOT require Morvan classical phase.
It requires: Pan-Zhang-style TN contraction scaling favorably to 83q/32c.

## Remaining Gap

Pan-Zhang broke Sycamore (volume=1060) with ~2^43 FLOPS.
ZCZ 3.0 has volume=2656 (2.5x larger).
The cost scaling determines feasibility:
- If polynomial in volume: feasible on modern GPU clusters
- If exponential in volume: needs supercomputer

This is an empirical question that cannot be answered without
implementing Pan-Zhang at the ZCZ 3.0 scale.
