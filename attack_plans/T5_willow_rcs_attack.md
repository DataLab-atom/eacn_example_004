# T5 Attack Plan: Google Willow RCS

**Attacker**: claude2
**Branch**: claude2
**Status**: Starting
**Last updated**: 2026-04-26

---

## Target Summary

| Field | Value |
|---|---|
| **Paper** | Google Quantum AI, Nature 638, 920 (2025) |
| **Hardware** | Willow 105 qubit |
| **Claim** | 5 minutes completes task needing 10^25 classical years |
| **Status** | 🟡 Challenged (Multiverse/DIPC gPEPS partial) |

## Attack Lines (from README.md)

### Line A: Same as T4 RCS methods
- Pan-Zhang TN contraction
- Willow RCS part uses fewer qubits×cycles than ZCZ 3.0
- Per claude7 Morvan analysis: Willow epsilon=0.33 × n ≈ at boundary

### Line B: Willow RCS was NOT the paper's main point
- Willow's main claim is QEC (quantum error correction)
- RCS part may not be optimized to maximum difficulty
- Potential for classical attack on a "non-optimized" circuit

### Line C: gPEPS (already partially challenged)
- Multiverse/DIPC used gPEPS for partial challenge
- Can we extend their approach?

## Key Insight from T4 Work
- Sycamore precedent: Pan-Zhang works inside Morvan quantum phase
- Willow epsilon ≈ 0.33 (per claude7), very close to Sycamore 0.33
- If Pan-Zhang broke Sycamore at similar noise, Willow RCS may be vulnerable

## First Steps
1. Extract Willow RCS specific parameters from Nature 638, 920
2. Compare with Sycamore and ZCZ 3.0 parameters
3. Estimate Pan-Zhang TN cost for Willow RCS configuration
