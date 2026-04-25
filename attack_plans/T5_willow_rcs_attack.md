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

## Data from TN Review (arXiv:2603.18825, Kshetrimayum 2026.03)

- 103 qubits, 2D square lattice
- Gate errors: 1Q 0.05%, 2Q 0.15% (better than Sycamore/ZCZ)
- 40q circuits: classical SNR 5.3 (diag) vs quantum 5.4 — CLOSE
- 40q off-diagonal: classical SNR only 1.1 — GAP
- 65q: Frontier 3.2 years vs quantum 2.1 hours — LARGE GAP
- TN contraction = most efficient classical method for OTOC
- No gPEPS results reported on Willow specifically

## Assessment

T5 is HARD. Willow has better gate fidelities than Sycamore/ZCZ,
and the 65q OTOC gap is still orders of magnitude. The "moving
boundary" framing from the TN review suggests incremental classical
progress but no breakthrough path currently visible.

Best hope: SPD on off-diagonal OTOC (claude4's T1 work directly
relevant — LC-edge configurations may be the soft spot).

## First Steps
1. Monitor claude4 T1 SPD progress — if LC-edge works at 65q, T5 benefits
2. Check if Willow RCS (non-OTOC) part has different parameters
3. Estimate Pan-Zhang TN cost for Willow RCS configuration
