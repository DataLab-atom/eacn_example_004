# T8: JZ 4.0 Negative Control — Gaussian Baseline Fails as Predicted

**Date**: 2026-04-25
**Purpose**: §E2 negative control for T8 attack framework

## Setup
- JZ 4.0 params: r=1.8, eta=0.51, 8176 modes, 1024 sources
- Same Gaussian baseline pipeline as T8 (JZ 3.0)
- Subset: 200 modes scaled to 8176

## Results

| System | Gaussian Prediction | Reported | Deviation |
|--------|-------------------|----------|-----------|
| JZ 3.0 (T8) | 281 photons | 255 | **10%** (matches) |
| JZ 4.0 (T7) | 36,181 photons | 3,050 | **1086%** (fails) |

## Interpretation

Oh critical eta for JZ 4.0: eta_crit = 0.21
JZ 4.0 eta = 0.51 >> 0.21 → OUTSIDE squashed thermal regime → HARD

The Gaussian baseline produces 10x too many photons for JZ 4.0,
confirming that the method correctly identifies the boundary
between classically simulable (JZ 3.0) and quantum-hard (JZ 4.0).

This is exactly what §E2 requires: "in regions where there should
be no advantage, the method should not spuriously claim one."

## Significance for Paper

This negative control STRENGTHENS the T8 positive result:
- JZ 3.0: method works (281 ≈ 255) → attack viable
- JZ 4.0: method fails (36K ≠ 3050) → method is honest, not overfitting
- The boundary is consistent with Oh et al.'s theoretical framework
