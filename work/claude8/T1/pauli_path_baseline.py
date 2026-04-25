"""
Schuster-Yin-Gao-Yao Pauli-path baseline (Path B for T1 Quantum Echoes attack).

Path B of the T1 three-path classical attack (per claude6 revised plan, claude4
+ claude7 + claude8 differentiation):
  - Path A (claude4): SPD core (Begušić-Gray-Chan SA 2024 + 2D extension Begušić-
    Chan PRX Quantum 6, 020302 2025) — heavy-truncation operator-evolution heuristic
  - **Path B (claude8, this file)**: Schuster-Yin-Gao-Yao arXiv:2407.12768 (2024)
    Pauli-path with **fixed weight bound ℓ** + strict polynomial cost argument
  - Path C (claude7): adaptive top-K Pauli weight + trace-form OTOC^(2)

Strategy
--------
- Different observable form: amplitude OTOC vs trace OTOC (vs claude4 amplitude;
  same observable form as claude4 — but algorithm is fixed weight, not heavy-trunc)
- ℓ region (per claude8 tail v7 measurement of d=4→d=6 norm 1.000→0.966):
  ℓ_baseline = 6, ℓ_stretch = 8 — covers d=4-12 sensitivity matrix
- §D5 cross-validation: target = reproduce claude4's 233 items at 4x4 grid d=4
  ℓ=4 LC-edge case verbatim (independent implementation, no code copy from
  claude4's spd_otoc_core.py)

Status: **SKELETON v0.1 — pure stubs, smoke test only**

Implementation plan (pending Phase 0b activation; not auto-triggered):
1. `build_iswap_brickwall_circuit`: 2D grid + brickwall + fSim=iSWAP·CPHASE
   per Bermejo §II.1.3 verbatim quote (claude8 commit 30fa5df audit trail)
2. `pauli_string_init`: M=Z on q0 + B=X on q_lightcone-edge
3. `heisenberg_evolve_pauli_path`: Heisenberg-picture conjugation U†OU layer-by-layer
   with FIXED weight bound truncation (drop strings of weight > ℓ)
4. `compute_otoc2`: OTOC^(2) = Tr(O(t) · O†(0) · O(t) · O†(0))
5. `compute_metrics`: BaselineResult-shaped tail / hot / cumulative metrics

References (full bibliography in work/claude8/arxiv_refs.md):
  [SchusterYin2024] Schuster, Yin, Gao, Yao, arXiv:2407.12768 (2024) — fixed-weight
                    Pauli-path strict polynomial cost; arXiv-only, not in canon
  [Bermejo2026]     Bermejo, Villalonga, Ware, Vidal, Szasz, arXiv:2604.15427
                    (2026) — Quantum Echoes circuit structure (brickwall, fSim);
                    also confirms M at lightcone edge (§II.1.3 quote)
  [BegusicGrayChan2024] Sci. Adv. 10, eadk4321 (2024) — SPD baseline for cross-check

Author: claude8 (branch claude8)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Result schema — same BaselineResult pattern as bulmer_baseline.py.
# Reuse the common dataclass once `infra/gbs/baseline_result.py` (claude5 9950ebd)
# is merged to main; until then, keep a local stub mirror for compile-time.
# ---------------------------------------------------------------------------

try:
    # Currently lives on origin/claude5; will become available to all branches
    # after the GBS shared-infra merge. Same try-import pattern as
    # bulmer_baseline.py — drop the fallback once §5.2 lands.
    from infra.gbs.baseline_result import BaselineResult  # type: ignore[import-not-found]
except ImportError:
    @dataclass
    class BaselineResult:
        # ---- shared sampler-agnostic ----
        click_marginal: np.ndarray
        total_click_distribution: np.ndarray
        tvd: float
        cross_entropy: float
        g2: np.ndarray
        wall_clock_s: float
        peak_vram_mb: float
        n_samples: int
        sample_seed: int
        truncation_error: float
        sampler_method: Literal[
            "oh_mps", "bulmer_phasespace", "thewalrus_check",
            "schuster_pauli_path",  # this file
        ] = "schuster_pauli_path"

        # ---- Path A SPD optional ----
        bond_dim: Optional[int] = None

        # ---- Path B (Bulmer phase-space) optional ----
        williamson_rank: Optional[int] = None
        bipartite_schmidt_rank: Optional[int] = None
        hafnian_calls: Optional[int] = None

        # ---- Path B (Schuster Pauli-path) optional ----
        pauli_weight_bound_l: Optional[int] = None
        n_pauli_strings_kept: Optional[int] = None
        residual_norm_outside_l: Optional[float] = None

        # ---- shared metadata ----
        circuit_meta: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Algorithmic stubs — all 5 raise NotImplementedError until Phase 0b coding.
# Order of implementation: 1 → 2 → 3 → 4 → 5.
# ---------------------------------------------------------------------------

def build_iswap_brickwall_circuit(grid_shape: Tuple[int, int], depth: int, seed: int):
    """
    Step 1. Construct 2D grid iSWAP-brickwall circuit per Bermejo §II.1.3.

    Layers alternate (a) entangling 2-qubit fSim=iSWAP·CPHASE on a brickwall
    bond-pattern (H-even / H-odd / V-even / V-odd, four sub-layers per "cycle")
    and (b) random single-qubit gates per Google Quantum Echoes specification.

    Returns
    -------
    circuit_spec : dict
      {
        "grid_shape": (rows, cols),
        "n_qubits": rows*cols,
        "depth": depth,
        "seed": seed,
        "cycles": List[cycle_dict],  # depth cycles
      }
    where each cycle_dict has:
      {
        "single_qubit_layer": List[(qubit_idx, axis_label)],  # axis_label in {"X^1/2","Y^1/2","W^1/2"} per Google
        "two_qubit_sublayers": [
          {"sublayer_type": "H-even"|"H-odd"|"V-even"|"V-odd",
           "pairs": List[(q1, q2)]},
          ...4 sublayers
        ]
      }
    """
    import numpy as np
    rng = np.random.default_rng(seed)
    rows, cols = grid_shape
    n_qubits = rows * cols

    def qid(r: int, c: int) -> int:
        return r * cols + c

    # Build the four brickwall sublayer pair sets.
    h_even, h_odd = [], []  # horizontal bonds (within-row, columns c--c+1)
    for r in range(rows):
        for c in range(cols - 1):
            pair = (qid(r, c), qid(r, c + 1))
            (h_even if c % 2 == 0 else h_odd).append(pair)

    v_even, v_odd = [], []  # vertical bonds (across-row, rows r--r+1)
    for c in range(cols):
        for r in range(rows - 1):
            pair = (qid(r, c), qid(r + 1, c))
            (v_even if r % 2 == 0 else v_odd).append(pair)

    sublayers_template = [
        ("H-even", h_even),
        ("H-odd", h_odd),
        ("V-even", v_even),
        ("V-odd", v_odd),
    ]

    AXES = ("X^1/2", "Y^1/2", "W^1/2")

    cycles: List[dict] = []
    for d in range(depth):
        sq_layer = [(q, AXES[rng.integers(0, 3)]) for q in range(n_qubits)]
        tq_sublayers = [{"sublayer_type": name, "pairs": list(pairs)}
                        for name, pairs in sublayers_template]
        cycles.append({
            "single_qubit_layer": sq_layer,
            "two_qubit_sublayers": tq_sublayers,
        })

    return {
        "grid_shape": (rows, cols),
        "n_qubits": n_qubits,
        "depth": depth,
        "seed": seed,
        "cycles": cycles,
    }


def pauli_string_init(
    grid_shape: Tuple[int, int],
    M_qubit: int,
    B_qubit: int,
    M_pauli: str = "Z",
    B_pauli: str = "X",
):
    """
    Step 2. Initial Pauli operator(s) for OTOC^(2) computation.

    For OTOC^(2): we need M and B operators evolving in opposite directions in
    the Heisenberg picture. Returns a dict {"M": pauli_op, "B": pauli_op}.

    Default Bermejo §II.1.3 setup: M=Z on a corner qubit, B=X on a qubit at the
    lightcone edge of B's spread (per claude4 d=2 LC-edge config = 12q 3x4 q0/q4).

    Pauli string representation:
        Tuple of length n_qubits with entries from {0, 1, 2, 3}:
            0 = I, 1 = X, 2 = Y, 3 = Z
        Each operator is a dict {pauli_string_tuple: coefficient}.

    A single weight-1 Pauli operator on qubit q with letter P is the dict
        {tuple_with_P_at_q_else_0: 1.0+0j}.
    """
    rows, cols = grid_shape
    n_qubits = rows * cols
    if not (0 <= M_qubit < n_qubits):
        raise ValueError(f"M_qubit {M_qubit} out of range for {n_qubits} qubits")
    if not (0 <= B_qubit < n_qubits):
        raise ValueError(f"B_qubit {B_qubit} out of range for {n_qubits} qubits")

    pauli_letter_to_int = {"I": 0, "X": 1, "Y": 2, "Z": 3}
    if M_pauli not in pauli_letter_to_int:
        raise ValueError(f"M_pauli {M_pauli!r} must be one of I/X/Y/Z")
    if B_pauli not in pauli_letter_to_int:
        raise ValueError(f"B_pauli {B_pauli!r} must be one of I/X/Y/Z")

    M_string = [0] * n_qubits
    M_string[M_qubit] = pauli_letter_to_int[M_pauli]
    B_string = [0] * n_qubits
    B_string[B_qubit] = pauli_letter_to_int[B_pauli]

    return {
        "M": {tuple(M_string): 1.0 + 0j},
        "B": {tuple(B_string): 1.0 + 0j},
    }


def pauli_weight(pauli_string: Tuple[int, ...]) -> int:
    """
    Number of non-identity Pauli factors in a Pauli string.

    Per Schuster-Yin-Gao-Yao 2024 §III: weight is the count of qubits where the
    Pauli is X/Y/Z (non-zero in our 0=I/1=X/2=Y/3=Z encoding).

    Used for ℓ-truncation: drop any string with weight > ℓ at every Heisenberg
    layer, giving classical cost O(n^ℓ · poly(depth)).

    >>> pauli_weight((0, 1, 0, 0))  # X on qubit 1
    1
    >>> pauli_weight((3, 0, 1, 2))  # Z, I, X, Y
    3
    >>> pauli_weight((0, 0, 0, 0))  # identity
    0
    """
    return sum(1 for p in pauli_string if p != 0)


def pauli_multiply_qubit(p1: int, p2: int) -> Tuple[complex, int]:
    """
    Multiply two single-qubit Paulis: returns (phase, result_pauli).

    Standard Pauli multiplication table per quantum mechanics:
        I*P = P*I = (1, P)
        X*X = Y*Y = Z*Z = (1, I)
        X*Y = (i, Z),  Y*X = (-i, Z)
        Y*Z = (i, X),  Z*Y = (-i, X)
        Z*X = (i, Y),  X*Z = (-i, Y)

    Encoding: 0=I, 1=X, 2=Y, 3=Z (consistent with pauli_string_init from Step 2).

    Used as the foundational primitive for Pauli conjugation rules under
    single-qubit Clifford (and beyond-Clifford) gates in Step 3.

    >>> pauli_multiply_qubit(0, 2)  # I*Y = Y
    ((1+0j), 2)
    >>> pauli_multiply_qubit(1, 1)  # X*X = I
    ((1+0j), 0)
    >>> pauli_multiply_qubit(1, 2)  # X*Y = i*Z
    (1j, 3)
    >>> pauli_multiply_qubit(3, 1)  # Z*X = i*Y
    (1j, 2)
    >>> pauli_multiply_qubit(2, 1)  # Y*X = -i*Z
    ((-0-1j), 3)
    """
    if p1 == 0:
        return (1.0 + 0j, p2)
    if p2 == 0:
        return (1.0 + 0j, p1)
    if p1 == p2:
        return (1.0 + 0j, 0)

    # Levi-Civita for cyclic XYZ → +i, anti-cyclic → -i
    # Cyclic order: (X, Y, Z) = (1, 2, 3) cyclic at indices 1→2→3→1
    cyclic_pairs = {(1, 2): 3, (2, 3): 1, (3, 1): 2}
    if (p1, p2) in cyclic_pairs:
        return (1j, cyclic_pairs[(p1, p2)])
    # Anti-cyclic: (Y,X)=Z, (Z,Y)=X, (X,Z)=Y with sign -i
    anti_cyclic = {(2, 1): 3, (3, 2): 1, (1, 3): 2}
    return (-1j, anti_cyclic[(p1, p2)])


def multiply_pauli_strings(
    s1: Tuple[int, ...],
    s2: Tuple[int, ...],
) -> Tuple[complex, Tuple[int, ...]]:
    """
    Multiply two full Pauli strings: P_s1 · P_s2 = phase * P_result.

    Composes pauli_multiply_qubit on each qubit independently. The total phase
    is the product of all per-qubit phases.

    Used as Step 4 prep primitive for compute_otoc2 (which needs Pauli operator
    dict multiplication: A · B = sum over (s1, s2) of a_s1 * b_s2 * phase(s1,s2)
    * P_{s1 * s2}).

    >>> multiply_pauli_strings((1, 0, 0), (0, 1, 0))  # X⊗I⊗I · I⊗X⊗I = X⊗X⊗I
    ((1+0j), (1, 1, 0))
    >>> multiply_pauli_strings((1, 1, 0), (1, 1, 0))  # XX · XX = II (each qubit X*X=I)
    ((1+0j), (0, 0, 0))
    >>> multiply_pauli_strings((1, 0, 0), (2, 0, 0))  # X · Y = i*Z on qubit 0
    (1j, (3, 0, 0))
    >>> multiply_pauli_strings((1, 2, 0), (2, 1, 0))  # XY · YX = (i*Z)(-i*Z) = II on q0+q1
    ((1+0j), (3, 3, 0))
    """
    if len(s1) != len(s2):
        raise ValueError(
            f"Pauli string length mismatch: {len(s1)} vs {len(s2)}"
        )
    total_phase = 1.0 + 0j
    result_string: List[int] = []
    for p1, p2 in zip(s1, s2):
        phase, p_result = pauli_multiply_qubit(p1, p2)
        total_phase *= phase
        result_string.append(p_result)
    return (total_phase, tuple(result_string))


def multiply_pauli_ops(
    op_a: Dict[Tuple[int, ...], complex],
    op_b: Dict[Tuple[int, ...], complex],
) -> Dict[Tuple[int, ...], complex]:
    """
    Multiply two Pauli operator dicts: A · B = sum over (s_a, s_b) of
    a_{s_a} * b_{s_b} * phase(s_a, s_b) * P_{s_a · s_b}.

    Composes multiply_pauli_strings on the cross-product of input strings.
    Coefficients are summed when distinct (s_a, s_b) pairs produce the same
    result Pauli string (collision summing).

    Used as Step 4 prep #2 for compute_otoc2 trace evaluation:
        OTOC^(2) = Tr(M(t) · B · M(t) · B) / 2^n
                 = identity_coefficient(M·B·M·B)
    where identity_coefficient extracts the (0,...,0)-Pauli coefficient.

    >>> # X · X = I (single-string each side)
    >>> multiply_pauli_ops({(1, 0): 1+0j}, {(1, 0): 1+0j})
    {(0, 0): (1+0j)}
    >>> # (X + Y) · X = X·X + Y·X = I + (-i Z) = I - i Z
    >>> result = multiply_pauli_ops({(1,): 1+0j, (2,): 1+0j}, {(1,): 1+0j})
    >>> result[(0,)]  # I coefficient
    (1+0j)
    >>> result[(3,)]  # Z coefficient = -i (from Y·X)
    -1j
    """
    if not op_a or not op_b:
        return {}
    result: Dict[Tuple[int, ...], complex] = {}
    for s_a, c_a in op_a.items():
        for s_b, c_b in op_b.items():
            phase, s_result = multiply_pauli_strings(s_a, s_b)
            new_coeff = c_a * c_b * phase
            if s_result in result:
                result[s_result] = result[s_result] + new_coeff
            else:
                result[s_result] = new_coeff
    return {k: v for k, v in result.items() if abs(v) > 1e-15}


def identity_coefficient(
    pauli_op: Dict[Tuple[int, ...], complex],
    n_qubits: int,
) -> complex:
    """
    Extract the coefficient of the identity Pauli string (0,...,0) from a
    Pauli operator dict.

    For a Pauli operator A = sum_s a_s P_s, this returns a_{identity}.
    Used in compute_otoc2 since Tr(P_s) = 0 for non-I Paulis and Tr(I) = 2^n,
    so Tr(A)/2^n = a_{identity}.

    >>> identity_coefficient({(0, 0, 0): 1.5+0.5j, (1, 0, 0): 2+0j}, 3)
    (1.5+0.5j)
    >>> identity_coefficient({(1, 0, 0): 2+0j}, 3)  # No identity component
    0j
    """
    return pauli_op.get(tuple([0] * n_qubits), 0.0 + 0j)


def conjugate_pauli_sqrt_w(pauli_at_qubit: int) -> Dict[int, complex]:
    """
    Conjugation rule for W^(1/2) gate where W = (X + Y) / sqrt(2).

    W^(1/2) is NON-Clifford, so each input Pauli expands into a SUM of Paulis:
        W^(1/2)† I W^(1/2) = +1 * I
        W^(1/2)† X W^(1/2) = (1/2) X + (1/2) Y + (1/sqrt(2)) Z
        W^(1/2)† Y W^(1/2) = (1/2) X + (1/2) Y - (1/sqrt(2)) Z
        W^(1/2)† Z W^(1/2) = -(1/sqrt(2)) X + (1/sqrt(2)) Y

    Verified numerically by direct matrix product of W^(1/2) = cos(pi/4)*I -
    i*sin(pi/4)*W. All coefficients are real (no imaginary parts).

    Encoding: 0=I, 1=X, 2=Y, 3=Z.
    Returns dict {result_pauli: coefficient}, may have multiple entries (unlike
    Clifford primitives which return single (phase, result_pauli) tuple).

    >>> sorted(conjugate_pauli_sqrt_w(0).items())  # I -> +I
    [(0, (1+0j))]
    >>> result = conjugate_pauli_sqrt_w(3)  # Z -> -(1/sqrt(2)) X + (1/sqrt(2)) Y
    >>> abs(result[1] + 0.7071067811865476) < 1e-10  # -1/sqrt(2) on X
    True
    >>> abs(result[2] - 0.7071067811865476) < 1e-10  # +1/sqrt(2) on Y
    True
    >>> 3 not in result  # No Z component on Z input
    True
    """
    import math
    half = 0.5 + 0j
    inv_sqrt2 = (1.0 / math.sqrt(2.0)) + 0j
    table = {
        0: {0: 1.0 + 0j},                              # I -> I
        1: {1: half, 2: half, 3: inv_sqrt2},           # X -> X/2 + Y/2 + Z/sqrt(2)
        2: {1: half, 2: half, 3: -inv_sqrt2},          # Y -> X/2 + Y/2 - Z/sqrt(2)
        3: {1: -inv_sqrt2, 2: inv_sqrt2},              # Z -> -X/sqrt(2) + Y/sqrt(2)
    }
    if pauli_at_qubit not in table:
        raise ValueError(f"pauli_at_qubit must be in {{0,1,2,3}}, got {pauli_at_qubit}")
    return dict(table[pauli_at_qubit])  # copy to avoid caller mutation


def conjugate_pauli_iswap(p_qubit1: int, p_qubit2: int) -> Tuple[complex, int, int]:
    """
    Conjugation rule for iSWAP gate on two qubits.

    iSWAP is Clifford, so each (P_a, P_b) pair maps to exactly one (P_c, P_d)
    pair with phase ±1.

    Table verified numerically by direct matrix computation:
        iSWAP† (P_a ⊗ P_b) iSWAP = phase * P_c ⊗ P_d

    Encoding: 0=I, 1=X, 2=Y, 3=Z.
    Returns (phase, result_p_qubit1, result_p_qubit2).

    >>> conjugate_pauli_iswap(0, 0)  # II -> II
    ((1+0j), 0, 0)
    >>> conjugate_pauli_iswap(0, 1)  # IX -> -YZ
    ((-1+0j), 2, 3)
    >>> conjugate_pauli_iswap(1, 1)  # XX -> XX
    ((1+0j), 1, 1)
    >>> conjugate_pauli_iswap(3, 0)  # ZI -> IZ (swaps as expected)
    ((1+0j), 0, 3)
    >>> conjugate_pauli_iswap(0, 3)  # IZ -> ZI (swaps as expected)
    ((1+0j), 3, 0)
    >>> conjugate_pauli_iswap(3, 3)  # ZZ -> ZZ
    ((1+0j), 3, 3)
    """
    # Full 16-entry table (verified numerically — see commit message).
    # Encoded as {(p_in_1, p_in_2): (phase, p_out_1, p_out_2)}.
    table = {
        (0, 0): (+1.0 + 0j, 0, 0),  # II -> +II
        (0, 1): (-1.0 + 0j, 2, 3),  # IX -> -YZ
        (0, 2): (+1.0 + 0j, 1, 3),  # IY -> +XZ
        (0, 3): (+1.0 + 0j, 3, 0),  # IZ -> +ZI
        (1, 0): (-1.0 + 0j, 3, 2),  # XI -> -ZY
        (1, 1): (+1.0 + 0j, 1, 1),  # XX -> +XX
        (1, 2): (+1.0 + 0j, 2, 1),  # XY -> +YX
        (1, 3): (-1.0 + 0j, 0, 2),  # XZ -> -IY
        (2, 0): (+1.0 + 0j, 3, 1),  # YI -> +ZX
        (2, 1): (+1.0 + 0j, 1, 2),  # YX -> +XY
        (2, 2): (+1.0 + 0j, 2, 2),  # YY -> +YY
        (2, 3): (+1.0 + 0j, 0, 1),  # YZ -> +IX
        (3, 0): (+1.0 + 0j, 0, 3),  # ZI -> +IZ
        (3, 1): (-1.0 + 0j, 2, 0),  # ZX -> -YI
        (3, 2): (+1.0 + 0j, 1, 0),  # ZY -> +XI
        (3, 3): (+1.0 + 0j, 3, 3),  # ZZ -> +ZZ
    }
    if (p_qubit1, p_qubit2) not in table:
        raise ValueError(
            f"(p_qubit1, p_qubit2) must each be in {{0,1,2,3}}, "
            f"got ({p_qubit1}, {p_qubit2})"
        )
    return table[(p_qubit1, p_qubit2)]


def apply_sqrt_w_to_op(
    pauli_op: Dict[Tuple[int, ...], complex],
    qubit: int,
) -> Dict[Tuple[int, ...], complex]:
    """
    Apply W^(1/2) non-Clifford gate conjugation on `qubit` to each Pauli string
    in `pauli_op` and return the resulting operator dict.

    UNLIKE Clifford composers, W^(1/2) maps each Pauli to a SUM of Paulis
    (multi-entry expansion), so a single input string with coefficient c
    produces multiple output strings each with coefficient c * c_i (where
    c_i are the W^(1/2) expansion coefficients). The output dict typically
    has MORE entries than input, and entries from different input strings
    can collide on the same output string — coefficients are summed.

    >>> # I@q0 -> I@q0 (single entry preserved)
    >>> apply_sqrt_w_to_op({(0, 0): 1.0+0j}, 0)
    {(0, 0): (1+0j)}
    >>> # X@q0 expands to X/2 + Y/2 + Z/sqrt(2) on q0
    >>> result = apply_sqrt_w_to_op({(1, 0): 1.0+0j}, 0)
    >>> sorted(result.keys())  # 3 entries
    [(1, 0), (2, 0), (3, 0)]
    >>> abs(result[(1, 0)] - 0.5) < 1e-10  # X coefficient
    True
    >>> abs(result[(3, 0)] - 0.7071067811865476) < 1e-10  # Z coefficient
    True
    """
    result: Dict[Tuple[int, ...], complex] = {}
    for pauli_string, coeff in pauli_op.items():
        n = len(pauli_string)
        if not (0 <= qubit < n):
            raise ValueError(f"qubit {qubit} out of range for {n}-qubit string")
        expansion = conjugate_pauli_sqrt_w(pauli_string[qubit])
        for new_pauli_at_qubit, expansion_coeff in expansion.items():
            new_string = list(pauli_string)
            new_string[qubit] = new_pauli_at_qubit
            new_key = tuple(new_string)
            new_coeff = coeff * expansion_coeff
            if new_key in result:
                result[new_key] = result[new_key] + new_coeff
            else:
                result[new_key] = new_coeff
    # Drop zero coefficients
    return {k: v for k, v in result.items() if abs(v) > 1e-15}


def apply_iswap_to_op(
    pauli_op: Dict[Tuple[int, ...], complex],
    qubit_a: int,
    qubit_b: int,
) -> Dict[Tuple[int, ...], complex]:
    """
    Apply iSWAP gate conjugation on (qubit_a, qubit_b) to each Pauli string in
    `pauli_op` and return the resulting operator dict.

    iSWAP is Clifford (each (P_a, P_b) pair maps to single (P_c, P_d) pair),
    so the output dict has the same number of keys as input — no expansion.

    >>> # IX on (0, 1) two qubits applies iSWAP on (0, 1): IX -> -YZ
    >>> op = {(0, 1, 0): 1.0+0j}
    >>> apply_iswap_to_op(op, 0, 1)
    {(2, 3, 0): (-1+0j)}
    >>> # ZI on (0, 1) applies iSWAP: ZI -> IZ
    >>> op = {(3, 0, 0): 1.0+0j}
    >>> apply_iswap_to_op(op, 0, 1)
    {(0, 3, 0): (1+0j)}
    >>> # XX on (0, 1) applies iSWAP: XX -> XX
    >>> op = {(1, 1, 0): 1.0+0j}
    >>> apply_iswap_to_op(op, 0, 1)
    {(1, 1, 0): (1+0j)}
    """
    if qubit_a == qubit_b:
        raise ValueError(f"qubit_a and qubit_b must be distinct, got {qubit_a} and {qubit_b}")

    result: Dict[Tuple[int, ...], complex] = {}
    for pauli_string, coeff in pauli_op.items():
        n = len(pauli_string)
        if not (0 <= qubit_a < n and 0 <= qubit_b < n):
            raise ValueError(
                f"qubit_a={qubit_a}, qubit_b={qubit_b} out of range for "
                f"{n}-qubit string"
            )
        phase, new_pa, new_pb = conjugate_pauli_iswap(
            pauli_string[qubit_a],
            pauli_string[qubit_b],
        )
        new_string = list(pauli_string)
        new_string[qubit_a] = new_pa
        new_string[qubit_b] = new_pb
        new_key = tuple(new_string)
        new_coeff = coeff * phase
        if new_key in result:
            result[new_key] = result[new_key] + new_coeff
        else:
            result[new_key] = new_coeff
    return {k: v for k, v in result.items() if abs(v) > 1e-15}


def apply_single_qubit_clifford_to_op(
    pauli_op: Dict[Tuple[int, ...], complex],
    qubit: int,
    gate: Literal["sqrt_X", "sqrt_Y"],
) -> Dict[Tuple[int, ...], complex]:
    """
    Apply single-qubit Clifford gate conjugation (`gate`) on `qubit` to each
    Pauli string in `pauli_op` and return the resulting operator dict.

    For Clifford gates each Pauli maps to exactly ONE Pauli (with phase),
    so the output dict has the same number of keys as input — no expansion.

    Phase handling: each input string with coefficient c maps to one output
    string with coefficient c * phase. If the result Pauli string is
    identical for two distinct inputs (impossible for Clifford on single
    qubit since the gate is a bijection on Paulis), coefficients would be
    summed; here we simply re-insert.

    >>> # Single-qubit op X on qubit 0 of 3-qubit system, apply sqrt_X on qubit 0
    >>> op = {(1, 0, 0): 1.0+0j}
    >>> apply_single_qubit_clifford_to_op(op, 0, 'sqrt_X')
    {(1, 0, 0): (1+0j)}
    >>> # Y on qubit 1, apply sqrt_X on qubit 1: Y -> -Z
    >>> op = {(0, 2, 0): 1.0+0j}
    >>> apply_single_qubit_clifford_to_op(op, 1, 'sqrt_X')
    {(0, 3, 0): (-1+0j)}
    >>> # Z on qubit 2, apply sqrt_Y on qubit 2: Z -> -X
    >>> op = {(0, 0, 3): 1.0+0j}
    >>> apply_single_qubit_clifford_to_op(op, 2, 'sqrt_Y')
    {(0, 0, 1): (-1+0j)}
    """
    if gate == "sqrt_X":
        conjugate_fn = conjugate_pauli_clifford_sqrt_x
    elif gate == "sqrt_Y":
        conjugate_fn = conjugate_pauli_clifford_sqrt_y
    else:
        raise ValueError(f"gate must be 'sqrt_X' or 'sqrt_Y', got {gate!r}")

    result: Dict[Tuple[int, ...], complex] = {}
    for pauli_string, coeff in pauli_op.items():
        if not (0 <= qubit < len(pauli_string)):
            raise ValueError(
                f"qubit {qubit} out of range for {len(pauli_string)}-qubit string"
            )
        phase, new_pauli_at_qubit = conjugate_fn(pauli_string[qubit])
        new_string = list(pauli_string)
        new_string[qubit] = new_pauli_at_qubit
        new_key = tuple(new_string)
        new_coeff = coeff * phase
        # Sum coefficients in case of collision (shouldn't happen for
        # single-qubit Clifford bijection but handle gracefully).
        if new_key in result:
            result[new_key] = result[new_key] + new_coeff
        else:
            result[new_key] = new_coeff
    # Drop zero coefficients
    return {k: v for k, v in result.items() if abs(v) > 1e-15}


def conjugate_pauli_clifford_sqrt_x(pauli_at_qubit: int) -> Tuple[complex, int]:
    """
    Conjugation rule for √X (X^(1/2)) gate on a single qubit.

    √X is Clifford, so each Pauli maps to a single Pauli (with possible phase):
        √X† I √X = I
        √X† X √X = X        (X commutes with √X, since √X = exp(-i π/4 X))
        √X† Y √X = -Z       (Y → -Z under √X conjugation)
        √X† Z √X = Y        (Z → Y under √X conjugation)

    Encoding: 0=I, 1=X, 2=Y, 3=Z.
    Returns (phase, result_pauli).

    >>> conjugate_pauli_clifford_sqrt_x(0)  # I → I
    ((1+0j), 0)
    >>> conjugate_pauli_clifford_sqrt_x(1)  # X → X
    ((1+0j), 1)
    >>> conjugate_pauli_clifford_sqrt_x(2)  # Y → -Z
    ((-1+0j), 3)
    >>> conjugate_pauli_clifford_sqrt_x(3)  # Z → Y
    ((1+0j), 2)
    """
    table = {
        0: (1.0 + 0j, 0),    # I → I
        1: (1.0 + 0j, 1),    # X → X
        2: (-1.0 + 0j, 3),   # Y → -Z
        3: (1.0 + 0j, 2),    # Z → Y
    }
    if pauli_at_qubit not in table:
        raise ValueError(f"pauli_at_qubit must be in {{0,1,2,3}}, got {pauli_at_qubit}")
    return table[pauli_at_qubit]


def conjugate_pauli_clifford_sqrt_y(pauli_at_qubit: int) -> Tuple[complex, int]:
    """
    Conjugation rule for √Y (Y^(1/2)) gate on a single qubit.

    √Y is Clifford, so each Pauli maps to a single Pauli (with possible phase):
        √Y† I √Y = I
        √Y† X √Y = Z        (X → Z under √Y conjugation)
        √Y† Y √Y = Y        (Y commutes with √Y)
        √Y† Z √Y = -X       (Z → -X under √Y conjugation)

    Encoding: 0=I, 1=X, 2=Y, 3=Z.
    Returns (phase, result_pauli).

    >>> conjugate_pauli_clifford_sqrt_y(0)  # I → I
    ((1+0j), 0)
    >>> conjugate_pauli_clifford_sqrt_y(1)  # X → Z
    ((1+0j), 3)
    >>> conjugate_pauli_clifford_sqrt_y(2)  # Y → Y
    ((1+0j), 2)
    >>> conjugate_pauli_clifford_sqrt_y(3)  # Z → -X
    ((-1+0j), 1)
    """
    table = {
        0: (1.0 + 0j, 0),    # I → I
        1: (1.0 + 0j, 3),    # X → Z
        2: (1.0 + 0j, 2),    # Y → Y
        3: (-1.0 + 0j, 1),   # Z → -X
    }
    if pauli_at_qubit not in table:
        raise ValueError(f"pauli_at_qubit must be in {{0,1,2,3}}, got {pauli_at_qubit}")
    return table[pauli_at_qubit]


def truncate_pauli_op_by_weight(
    pauli_op: Dict[Tuple[int, ...], complex],
    weight_bound_l: int,
) -> Dict[Tuple[int, ...], complex]:
    """
    Drop Pauli strings whose weight exceeds ℓ from a Pauli operator dict.

    This is the core ℓ-truncation operation in Schuster-Yin-Gao-Yao 2024 §III,
    applied at EVERY Heisenberg layer to keep the operator support polynomial.

    Returns a NEW dict (does not mutate input) keeping only entries with
    pauli_weight(string) <= weight_bound_l.

    >>> op = {(1,1,1,0): 1.0+0j, (1,0,0,0): 0.5+0j}  # weight 3 + weight 1
    >>> truncate_pauli_op_by_weight(op, weight_bound_l=2)
    {(1, 0, 0, 0): (0.5+0j)}
    """
    if weight_bound_l < 0:
        raise ValueError(f"weight_bound_l must be >= 0, got {weight_bound_l}")
    return {
        s: c for s, c in pauli_op.items()
        if pauli_weight(s) <= weight_bound_l
    }


def heisenberg_evolve_pauli_path(
    pauli_op: Dict[Tuple[int, ...], complex],
    circuit_spec: dict,
    weight_bound_l: int,
    direction: Literal["forward", "backward"] = "forward",
) -> Dict[Tuple[int, ...], complex]:
    """
    Step 3. Heisenberg-picture evolution of a Pauli operator under a brickwall
    circuit, with FIXED weight bound ℓ truncation.

    Per Schuster-Yin-Gao-Yao 2024 §III: drop any Pauli string whose weight
    exceeds ℓ AFTER EACH CYCLE. Cost is O(n^ℓ · poly(depth)) given the
    truncation is hard.

    Direction:
      "forward":  applies U†·O·U where U = U_depth ... U_2 U_1 is the full
                  circuit unitary (so cycles are applied in FORWARD order via
                  conjugation primitives, building U_1†...U_d† O U_d...U_1).
      "backward": applies U·O·U† (currently NOT IMPLEMENTED — needed for OTOC
                  in Step 4 but can use forward with reversed circuit_spec).

    Composes the 10 Step 3 primitives:
      - apply_single_qubit_clifford_to_op (X^(1/2), Y^(1/2))
      - apply_sqrt_w_to_op (W^(1/2), non-Clifford multi-Pauli expansion)
      - apply_iswap_to_op (iSWAP 2-qubit)
      - truncate_pauli_op_by_weight (after each cycle)

    Iterates over circuit_spec["cycles"]: each cycle has
      single_qubit_layer: List[(qubit_idx, axis_label)]
      two_qubit_sublayers: 4 sublayers H-even/H-odd/V-even/V-odd
    """
    if direction != "forward":
        raise NotImplementedError(
            "Step 3 backward direction pending; use forward with reversed "
            "circuit_spec for backward Heisenberg evolution."
        )

    if weight_bound_l < 0:
        raise ValueError(f"weight_bound_l must be >= 0, got {weight_bound_l}")

    cycles = circuit_spec.get("cycles", [])
    if not isinstance(cycles, list):
        raise ValueError(f"circuit_spec['cycles'] must be a list")

    # Start with input operator (do not mutate caller's dict).
    current = dict(pauli_op)

    for cycle_idx, cycle in enumerate(cycles):
        # 1. Apply single-qubit layer.
        sq_layer = cycle.get("single_qubit_layer", [])
        for qubit_idx, axis_label in sq_layer:
            if axis_label == "X^1/2":
                current = apply_single_qubit_clifford_to_op(current, qubit_idx, "sqrt_X")
            elif axis_label == "Y^1/2":
                current = apply_single_qubit_clifford_to_op(current, qubit_idx, "sqrt_Y")
            elif axis_label == "W^1/2":
                current = apply_sqrt_w_to_op(current, qubit_idx)
            else:
                raise ValueError(
                    f"Unknown single-qubit axis_label {axis_label!r} at "
                    f"cycle {cycle_idx}, qubit {qubit_idx}"
                )

        # 2. Apply 4 two-qubit sublayers (H-even/H-odd/V-even/V-odd).
        for sublayer in cycle.get("two_qubit_sublayers", []):
            for qa, qb in sublayer.get("pairs", []):
                current = apply_iswap_to_op(current, qa, qb)

        # 3. Truncate by weight after each cycle (per Schuster-Yin §III).
        current = truncate_pauli_op_by_weight(current, weight_bound_l)

    return current


def compute_otoc2(
    M_evolved_forward: Dict[Tuple[int, ...], complex],
    B_evolved_backward: Dict[Tuple[int, ...], complex],
    grid_shape: Tuple[int, int],
) -> complex:
    """
    Step 4. Compute OTOC^(2) = Tr(O_M(t) · O_B · O_M(t) · O_B) / 2^n

    For Pauli operators O_M(t) = Σ_s m_s P_s and O_B = Σ_t b_t P_t:
    Tr(O_M · O_B · O_M · O_B) = 2^n · (identity coefficient of O_M · O_B · O_M · O_B)
    since Tr(P_s) = 0 for non-identity P_s and Tr(I) = 2^n.

    Therefore OTOC^(2) = identity_coefficient(O_M · O_B · O_M · O_B).

    Parameters
    ----------
    M_evolved_forward : Pauli operator dict
        M(t) = U†·M·U after Heisenberg forward evolution under circuit.
    B_evolved_backward : Pauli operator dict
        For the simplified OTOC^(2)(t) = Tr(M(t) B M(t) B)/2^n we use the
        ORIGINAL B operator (no time evolution); name reflects the more
        general OTOC^(4) variant where B may also be evolved.
    grid_shape : (rows, cols)
        Used to determine n_qubits = rows*cols for identity_coefficient.

    Returns
    -------
    otoc2_value : complex
        Should be real for Hermitian M, B (since Tr of self-adjoint product).

    Composes Step 4 prep primitives:
      multiply_pauli_ops × 3 (M·B, then ·M, then ·B) +
      identity_coefficient (extract (0,...,0) entry)
    """
    rows, cols = grid_shape
    n_qubits = rows * cols
    if not M_evolved_forward or not B_evolved_backward:
        return 0.0 + 0j
    # M · B
    mb = multiply_pauli_ops(M_evolved_forward, B_evolved_backward)
    # (M · B) · M
    mbm = multiply_pauli_ops(mb, M_evolved_forward)
    # (M · B · M) · B
    mbmb = multiply_pauli_ops(mbm, B_evolved_backward)
    # Tr(MBMB)/2^n = identity coefficient of MBMB
    return identity_coefficient(mbmb, n_qubits)


def compute_metrics(
    pauli_strings: List[Tuple[Tuple[int, ...], complex]],
    weight_bound_l: int,
    grid_shape: Tuple[int, int],
) -> dict:
    """
    Step 5. Compute BaselineResult-shaped metrics from a list of (string, c) pairs.

    Parameters
    ----------
    pauli_strings : List[(pauli_string_tuple, complex_coefficient)]
        Output of Step 3 heisenberg_evolve_pauli_path converted to list-of-tuples
        (or equivalent .items() of operator dict).
    weight_bound_l : int
        The truncation bound used during Step 3 evolution.
    grid_shape : (rows, cols)
        Used to determine n_qubits.

    Returns
    -------
    metrics : dict with keys:
        - pauli_weight_bound_l: int (input echo)
        - n_pauli_strings_kept: int (count of non-zero entries)
        - frobenius_norm_sq: float (sum |c|^2)
        - max_weight_observed: int (max pauli_weight over kept strings)
        - mean_weight_observed: float (mean weight, 0 if empty)
        - n_qubits: int (rows * cols)
        - identity_fraction: float (|c_identity|^2 / total Frobenius norm^2,
          captures the "diagonal" component fraction; useful as a sanity check
          for OTOC^(2) computation since OTOC = identity_coefficient(MBMB) is
          related)

    >>> metrics = compute_metrics(
    ...     [((1, 0, 0), 1.0+0j), ((0, 1, 0), 0.5+0j)],
    ...     weight_bound_l=2,
    ...     grid_shape=(1, 3),
    ... )
    >>> metrics['n_pauli_strings_kept']
    2
    >>> metrics['n_qubits']
    3
    >>> metrics['max_weight_observed']
    1
    >>> abs(metrics['frobenius_norm_sq'] - 1.25) < 1e-10  # 1^2 + 0.5^2
    True
    """
    rows, cols = grid_shape
    n_qubits = rows * cols
    n_kept = len(pauli_strings)
    if n_kept == 0:
        return {
            "pauli_weight_bound_l": weight_bound_l,
            "n_pauli_strings_kept": 0,
            "frobenius_norm_sq": 0.0,
            "max_weight_observed": 0,
            "mean_weight_observed": 0.0,
            "n_qubits": n_qubits,
            "identity_fraction": 0.0,
        }

    weights = [pauli_weight(s) for s, _ in pauli_strings]
    coeff_norms_sq = [abs(c) ** 2 for _, c in pauli_strings]
    frobenius_sq = sum(coeff_norms_sq)
    identity_string = tuple([0] * n_qubits)
    identity_coeff = next(
        (c for s, c in pauli_strings if s == identity_string),
        0.0 + 0j,
    )
    identity_fraction = (
        (abs(identity_coeff) ** 2) / frobenius_sq if frobenius_sq > 0 else 0.0
    )

    return {
        "pauli_weight_bound_l": weight_bound_l,
        "n_pauli_strings_kept": n_kept,
        "frobenius_norm_sq": frobenius_sq,
        "max_weight_observed": max(weights),
        "mean_weight_observed": sum(weights) / n_kept,
        "n_qubits": n_qubits,
        "identity_fraction": identity_fraction,
    }


# ---------------------------------------------------------------------------
# Top-level driver — equivalent in shape to claude5's run_oh_mps_attack and
# claude8's run_bulmer_attack. NOT YET WIRED.
# ---------------------------------------------------------------------------

def run_schuster_pauli_path_attack(
    grid_shape: Tuple[int, int],
    depth: int,
    M_qubit: int,
    B_qubit: int,
    weight_bound_l: int,
    seed: int = 42,
) -> BaselineResult:
    """
    End-to-end Schuster-Yin-Gao-Yao fixed-weight Pauli-path attack on OTOC^(2).

    Argument parity:
      - `weight_bound_l` ∈ [4, 8] per claude8 v7 measurement (`30fa5df`)
      - `grid_shape` 2D rectangular per Bermejo §II.1.3 brickwall
      - `M_qubit, B_qubit` per OTOC^(2) operator placement (default LC-edge)
      - `seed` for circuit randomness reproducibility

    Skeleton: raises NotImplementedError in Step 1; smoke test exercises driver
    parameter validation only.
    """
    if depth <= 0:
        raise ValueError("depth must be positive")
    if weight_bound_l <= 0 or weight_bound_l > grid_shape[0] * grid_shape[1]:
        raise ValueError("weight_bound_l must be in (0, n_qubits]")

    # n_qubits = grid_shape[0] * grid_shape[1]
    # circuit = build_iswap_brickwall_circuit(grid_shape, depth, seed)
    # init = pauli_string_init(grid_shape, M_qubit, B_qubit)
    # M_fwd  = heisenberg_evolve_pauli_path(init["M"], circuit, weight_bound_l, "forward")
    # B_bwd  = heisenberg_evolve_pauli_path(init["B"], circuit, weight_bound_l, "backward")
    # otoc2  = compute_otoc2(M_fwd, B_bwd, grid_shape)
    # metrics = compute_metrics(list(M_fwd.items()) + list(B_bwd.items()),
    #                           weight_bound_l, grid_shape)
    # return BaselineResult(..., **metrics)

    raise NotImplementedError(
        "run_schuster_pauli_path_attack: pipeline not yet wired (Phase 0b TODO)"
    )


# ---------------------------------------------------------------------------
# Smoke test — runs without `infra/gbs/baseline_result.py` available.
# Exercises BaselineResult dataclass + driver argument validation only.
# ---------------------------------------------------------------------------

def _smoke():
    fake = BaselineResult(
        click_marginal=np.zeros(4),
        total_click_distribution=np.zeros(5),
        tvd=0.0,
        cross_entropy=0.0,
        g2=np.zeros((4, 4)),
        wall_clock_s=0.0,
        peak_vram_mb=0.0,
        n_samples=0,
        sample_seed=42,
        truncation_error=0.0,
        pauli_weight_bound_l=6,
        n_pauli_strings_kept=233,
        residual_norm_outside_l=0.034,
    )
    assert fake.sampler_method == "schuster_pauli_path"
    assert fake.pauli_weight_bound_l == 6
    assert fake.bond_dim is None  # Path A field unused

    try:
        run_schuster_pauli_path_attack(
            grid_shape=(4, 4),
            depth=4,
            M_qubit=0,
            B_qubit=15,
            weight_bound_l=-1,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for weight_bound_l=-1")

    try:
        run_schuster_pauli_path_attack(
            grid_shape=(4, 4),
            depth=4,
            M_qubit=0,
            B_qubit=15,
            weight_bound_l=6,
        )
    except NotImplementedError:
        pass
    else:
        raise AssertionError("expected NotImplementedError once validation passes")

    print("pauli_path_baseline.py smoke test OK — schema + driver validation pass")


if __name__ == "__main__":
    _smoke()
