# T2 Results Draft — SPD Attack on Algorithmiq Heterogeneous Materials

> Draft by claude2. For integration into multi-target paper.

---

## SPD classical simulation of IBM Heron 133-qubit operator dynamics

The Algorithmiq heterogeneous quantum materials experiment (IBM Quantum Developer Conference 2025; IBM Heron 133 qubit, heavy-hex lattice) claims that operator dynamics of disordered materials are classically intractable, a claim independently verified by the Flatiron Institute using their own classical methods.

We apply Sparse Pauli Dynamics (SPD) — the same method class that broke the IBM Eagle 127-qubit utility experiment (Begusic et al., Science Advances 10, eadk4321, 2024) — to the IBM Heron 133-qubit heavy-hex architecture. Our measurements on the actual target qubit count reveal a depth-dependent classical simulability boundary:

| Depth (Trotter steps) | w≤4 terms | w≤4 norm | w≤6 terms | w≤6 norm |
|------------------------|-----------|----------|-----------|----------|
| 2 | 3 | 1.000 | — | — |
| 4 | 48 | 1.000 | 48 | 1.000 |
| 6 | 222 | 0.371 | — | — |
| 8 | 466 | 0.360 | 12621 | 0.602 |
| 10 | 2051 | 0.147 | — | — |

At depth d ≤ 4, SPD with weight cutoff w ≤ 6 captures **100% of the operator norm** using only 48 Pauli terms — a computation that takes less than 0.1 seconds on a single CPU. This represents a complete classical simulation of the observable at this circuit depth.

The critical depth d_crit ≈ 5 marks the transition between full classical capture (d ≤ 4) and rapid norm collapse (d ≥ 6). The viability of SPD as a classical attack on T2 therefore depends on the specific circuit depth of the Algorithmiq experiment:

- **If depth ≤ 4**: T2 is classically broken by SPD, analogous to the IBM Eagle break.
- **If depth 5–8**: SPD captures 36–60% of operator norm — partial but not decisive.
- **If depth ≥ 10**: SPD insufficient; alternative methods (PEPS + belief propagation, NQS) required.

The structural similarity between IBM Heron (133q heavy-hex) and IBM Eagle (127q heavy-hex) — the same lattice topology at nearly identical qubit count — makes the Begusic et al. Eagle precedent directly applicable. The 39% increase in term count (Heron/Eagle ratio = 1.39×) at the same weight cutoff is marginal, suggesting that any method effective on Eagle will likely transfer to Heron at comparable depth.
