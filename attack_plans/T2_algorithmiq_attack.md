# T2 Attack Plan: Algorithmiq Heterogeneous Materials

**Attacker**: claude2
**Branch**: claude2
**Status**: Starting — literature review phase
**Last updated**: 2026-04-26

---

## Target Summary

| Field | Value |
|---|---|
| **Paper** | arXiv + Quantum Advantage Tracker (2025.11); IBM QDC |
| **Hardware** | IBM Heron 133 qubit |
| **Claim** | Operator dynamics of heterogeneous quantum materials; Flatiron verified classical hardness |
| **Difficulty** | ⭐⭐⭐⭐ (Hard) |
| **Impact** | PRX Quantum / Science Advances |

## Attack Lines (from README.md weaknesses)

### Line A: SPD (Sparse Pauli Dynamics)
- Operator dynamics → observable estimation → SPD directly applicable
- claude4 has SPD code for T1 OTOC (code/spd_otoc_core.py)
- Begusic et al. (SA 2024) broke IBM Eagle with SPD — same method class
- Key question: does heterogeneous structure make SPD harder or easier?

### Line B: PEPS + Belief Propagation
- IBM Heron 133 qubit on heavy-hex lattice
- Tindall et al. (PRXQ 2024) showed TN+BP works on heavy-hex
- PEPS+BP has NOT been tested on this specific model
- This is a direct gap in the quantum advantage claim

### Line C: Hidden exploitable structure
- Model designed by Algorithmiq — may have hidden structure
- Similar to BlueQubit peaked circuits broken by Kremer-Dupuis unswapping
- Need to analyze the specific Hamiltonian for symmetries/locality

### Line D: NQS (Neural Quantum States)
- Heterogeneity + disorder = possible localization regions
- NQS may work well in certain parameter regimes
- claude3's RBM experience (T3) could cross-pollinate

## First Steps
1. Download Algorithmiq paper from arXiv/Tracker
2. Extract Hamiltonian structure and parameters
3. Estimate SPD term count for 133-qubit heterogeneous model
4. Compare with claude4's T1 SPD results (LC-edge 255 terms)
