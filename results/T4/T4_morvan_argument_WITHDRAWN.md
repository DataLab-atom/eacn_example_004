# T4 Morvan Phase Argument — WITHDRAWN

**Date**: 2026-04-25
**Reason**: Incorrect noise parameter definition

## What was claimed (commit 27f2016)

ZCZ 3.0 operates at lambda/lc = 1.55, deep in the "classical phase"
of the Morvan phase transition framework (Nature 634, 328, 2024).

## Why it's wrong

Morvan et al. Figure 3g defines the critical parameter as:
**ε_c = 0.47 errors per cycle** (per-gate, intensive parameter)

We used:
**lambda = n × d × ε_2q** (total noise budget, extensive parameter)
with **lambda_c = 6.5** (source unknown — likely ad hoc)

ZCZ 3.0 per-cycle error: ε ≈ 0.005 << ε_c = 0.47
→ ZCZ 3.0 is in the **quantum advantage phase**, not classical

## What remains valid for T4

1. XEB = 0.026% — extremely low fidelity bar (confirmed by paper data)
2. Sycamore precedent — broken by Pan-Zhang despite similar per-gate errors
3. Total noise budget argument — even if Morvan's specific framework doesn't
   apply, the cumulative effect of noise over 83q×32c is real
4. TN contraction scaling — still valid independent of phase transition theory

## Lesson

Always verify that the specific definition of a parameter in a referenced
paper matches your usage. "Lambda" in different contexts means different
things. The per-gate vs total-budget distinction is fundamental.
