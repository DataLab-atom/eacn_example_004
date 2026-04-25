# Abstract + Introduction Draft (for Nature/Science manuscript)

> **Status**: Draft v0.1
> **Author**: claude4

---

## Abstract

We present a systematic classical simulation attack on Google's
Quantum Echoes experiment — the first verifiable quantum advantage
claim based on second-order out-of-time-order correlators (OTOC^(2))
measured on the 105-qubit Willow processor. Using Sparse Pauli
Dynamics (SPD) in the Heisenberg picture, we demonstrate that the
experimentally relevant lightcone-edge configuration requires <=255
Pauli terms at depth 4 on 24-qubit wide grids, with term count
*decreasing* as grid width increases (4007 at 8q -> 3884 at 12q ->
255 at 24q). The Pauli coefficient tail exhibits a regime-dependent
transition: exponential decay (slope -0.5) in the screening regime
(circuit depth below a critical threshold d_crit ~ 11 for Willow
65q), recovering power-law scaling (alpha = 1.705, DELTA_AIC = +1158)
in the post-transition regime. Google's choice of M-operator placement
at the physical lightcone edge — made to maximize quantum signal —
simultaneously minimizes the classical simulation cost. Three
independent classical paths (fixed-weight SPD, Schuster-Yin
Pauli-path, adaptive top-K) converge on these findings. The attack
is provisionally feasible for Willow's estimated per-arm depth of
~12 cycles, which lies at the screening-to-transition boundary.
We contextualize this result within a broader systematic evaluation
of 2025 quantum advantage claims, finding mixed outcomes: substantive
classical attacks succeed on some targets while others stand firm,
revealing four distinct boundary types that characterize the
classical-quantum frontier.

---

## 1. Introduction

### 1.1 Context

The year 2025 marks a proliferation of quantum advantage claims
across multiple hardware platforms: superconducting qubits (Google
Willow, USTC Zuchongzhi 3.0), photonic systems (USTC Jiuzhang 4.0),
and quantum annealers (D-Wave Advantage2). Each claim invokes a
different computational task — random circuit sampling (RCS),
Gaussian boson sampling (GBS), quantum annealing dynamics, or
out-of-time-order correlators (OTOCs) — yet all share a common
structure: the quantum device produces output that is claimed to
be intractable for classical computers.

The history of quantum advantage is one of iterative challenge and
response. Google's 2019 Sycamore claim (10,000 years) was reduced
to feasible classical computation within three years (Pan & Zhang,
PRL 129, 2022). IBM's 2023 Eagle utility experiment was classically
matched within weeks (Begusic, Gray, Chan, Science Advances 10,
2024; Tindall et al., PRX Quantum 5, 2024). Each cycle refines the
boundary between classical and quantum computational regimes.

### 1.2 The Quantum Echoes experiment

Google's Quantum Echoes experiment (Nature, 2025) represents a
qualitative shift: rather than sampling from a random circuit output
distribution, it measures a physical observable — the second-order
OTOC — that quantifies information scrambling in a quantum system.
The claim is that 65-qubit OTOC^(2) measurements on Willow are
13,000x faster than the best classical tensor network simulation.

Bermejo et al. (arXiv:2604.15427, 2026) subsequently proved that
tensor networks with belief propagation (TNBP) cannot feasibly
simulate the Quantum Echoes experiment, due to the incompressibility
of OTOC circuits in the Schrodinger picture. This closes the
PEPS-based attack class but leaves open the question: can
Heisenberg-picture methods — which operate in operator space rather
than state space — succeed where Schrodinger-picture methods fail?

### 1.3 This work

We address this question using Sparse Pauli Dynamics (SPD), a
Heisenberg-picture method that tracks the operator as a sparse sum
of Pauli strings. Our key contributions are:

1. **First systematic SPD evaluation of OTOC^(2)**: we implement and
   validate SPD for second-order OTOCs on 2D grid circuits with
   iSWAP-like gates, achieving machine precision at max weight = n.

2. **Regime-dependent tail discovery**: Pauli coefficient tails are
   exponential in the screening regime (d < d_crit) but transition
   to power-law (alpha = 1.705) at d >= d_crit, reconciling our
   OTOC-specific findings with the general Schuster et al. framework.

3. **Grid topology dominance**: wide grids (NxN) require dramatically
   fewer Pauli terms than narrow grids (2xN), with term count
   *decreasing* from 4007 (8q) to 255 (24q) on scrambled circuits.

4. **Google's configuration is easiest**: the lightcone-edge M-B
   placement chosen by Google for maximum signal has 5x fewer terms
   and steeper tail decay than alternative configurations.

5. **PEPS/Pauli-path separation**: Pauli-path term count decreases
   with system size while PEPS bond dimension increases exponentially,
   suggesting a separation between the two classical attack paradigms.

6. **Broader attack portfolio**: we contextualize T1 within a
   systematic evaluation of 9 quantum advantage claims, revealing
   four distinct boundary types (regime-transition, ansatz-capacity,
   hardware-bounded, transparency-vacuum) — the non-uniformity of
   outcomes is itself a methodology contribution.

---

*Draft v0.1, 2026-04-26.*
