"""
Sparse Pauli Dynamics (SPD) for OTOC Classical Simulation
=========================================================
Target: T1 — Google Quantum Echoes (OTOC on Willow 105 qubit)

This module implements the core SPD algorithm in the Heisenberg picture
for computing Out-of-Time-Order Correlators (OTOCs).

OTOC^(2) = Tr(rho * M * U^dag * B * U * M * U^dag * B * U)

where U is a random circuit on Willow's 2D grid, B and M are Pauli operators.

Method: Evolve the observable backward through the circuit in the Pauli basis,
truncating high-weight Pauli strings at each layer.

References:
  - Begusic, Gray, Chan, Science Advances 10, eadk4321 (2024)
  - Begusic & Chan, PRX Quantum 6, 020302 (2025)
  - Schuster, Yin, Gao, Yao, arXiv:2407.12768 (2024)

Author: claude4 (branch: claude4)
Date: 2026-04-25
"""

import numpy as np
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import time


# ============================================================
# Pauli algebra primitives
# ============================================================

# Pauli labels: 0=I, 1=X, 2=Y, 3=Z
# Multiplication table: P_a * P_b = phase * P_c
# Using the convention: XY = iZ, YZ = iX, ZX = iY (cyclic)

# Product of two single-qubit Paulis: (a, b) -> (phase, c)
# phase encoded as power of i: 0,1,2,3 for 1,i,-1,-i
PAULI_MULT_TABLE = np.zeros((4, 4, 2), dtype=np.int8)

def _init_pauli_mult():
    """Initialize Pauli multiplication table."""
    # I*P = P*I = P
    for p in range(4):
        PAULI_MULT_TABLE[0, p] = [0, p]
        PAULI_MULT_TABLE[p, 0] = [0, p]
    # P*P = I
    for p in range(1, 4):
        PAULI_MULT_TABLE[p, p] = [0, 0]
    # XY = iZ
    PAULI_MULT_TABLE[1, 2] = [1, 3]
    PAULI_MULT_TABLE[2, 1] = [3, 3]  # YX = -iZ
    # YZ = iX
    PAULI_MULT_TABLE[2, 3] = [1, 1]
    PAULI_MULT_TABLE[3, 2] = [3, 1]  # ZY = -iX
    # ZX = iY
    PAULI_MULT_TABLE[3, 1] = [1, 2]
    PAULI_MULT_TABLE[1, 3] = [3, 2]  # XZ = -iY

_init_pauli_mult()


@dataclass
class PauliString:
    """
    A Pauli string on n qubits: coefficient * (P_0 x P_1 x ... x P_{n-1})

    Stored as:
      - paulis: tuple of ints (0=I, 1=X, 2=Y, 3=Z), length n
      - coeff: complex coefficient
    """
    paulis: tuple  # (p0, p1, ..., p_{n-1}) where pi in {0,1,2,3}
    coeff: complex

    @property
    def weight(self) -> int:
        """Number of non-identity Pauli factors."""
        return sum(1 for p in self.paulis if p != 0)

    def __hash__(self):
        return hash(self.paulis)

    def __eq__(self, other):
        return self.paulis == other.paulis


class PauliOperator:
    """
    A sparse linear combination of Pauli strings: O = sum_j c_j P_j

    This is the central data structure for SPD: we track the operator
    as a dictionary {pauli_tuple: complex_coefficient}.
    """

    def __init__(self, n_qubits: int):
        self.n = n_qubits
        self.terms: Dict[tuple, complex] = {}

    @classmethod
    def single_pauli(cls, n_qubits: int, qubit: int, pauli: int, coeff: complex = 1.0):
        """Create a single Pauli operator on one qubit (rest = I)."""
        op = cls(n_qubits)
        paulis = [0] * n_qubits
        paulis[qubit] = pauli
        op.terms[tuple(paulis)] = coeff
        return op

    @classmethod
    def identity(cls, n_qubits: int):
        """Create the identity operator."""
        op = cls(n_qubits)
        op.terms[tuple([0] * n_qubits)] = 1.0
        return op

    def weight_distribution(self) -> Dict[int, float]:
        """Return {weight: sum of |coeff|^2} for diagnostics."""
        dist = defaultdict(float)
        for paulis, coeff in self.terms.items():
            w = sum(1 for p in paulis if p != 0)
            dist[w] += abs(coeff) ** 2
        return dict(sorted(dist.items()))

    def truncate(self, max_weight: int) -> 'PauliOperator':
        """Truncate: discard all terms with Pauli weight > max_weight."""
        new_op = PauliOperator(self.n)
        for paulis, coeff in self.terms.items():
            w = sum(1 for p in paulis if p != 0)
            if w <= max_weight:
                new_op.terms[paulis] = coeff
        return new_op

    def truncate_by_magnitude(self, eps: float) -> 'PauliOperator':
        """Truncate: discard all terms with |coeff| < eps."""
        new_op = PauliOperator(self.n)
        for paulis, coeff in self.terms.items():
            if abs(coeff) >= eps:
                new_op.terms[paulis] = coeff
        return new_op

    @property
    def num_terms(self) -> int:
        return len(self.terms)

    @property
    def norm_sq(self) -> float:
        """Squared Frobenius norm (sum |c_j|^2)."""
        return sum(abs(c) ** 2 for c in self.terms.values())

    def trace_with(self, other: 'PauliOperator') -> complex:
        """Compute Tr(self^dag * other) / 2^n using Pauli orthogonality."""
        result = 0.0
        for paulis, coeff in self.terms.items():
            if paulis in other.terms:
                result += np.conj(coeff) * other.terms[paulis]
        return result


# ============================================================
# Gate implementations in Heisenberg picture
# ============================================================

def _apply_single_qubit_rotation_heisenberg(
    op: PauliOperator, qubit: int, axis: int, angle: float
) -> PauliOperator:
    """
    Apply exp(-i * angle/2 * P_axis) on qubit in Heisenberg picture.

    U^dag O U where U = exp(-i angle/2 P_axis).
    For a Pauli P_j on the target qubit:
      - If P_j commutes with P_axis: P_j unchanged
      - If P_j anticommutes with P_axis: P_j -> cos(angle)*P_j + sin(angle)*[P_axis, P_j]/(2i)

    Args:
        op: PauliOperator to transform
        qubit: target qubit index
        axis: Pauli axis (1=X, 2=Y, 3=Z)
        angle: rotation angle
    """
    c = np.cos(angle)
    s = np.sin(angle)
    new_op = PauliOperator(op.n)

    for paulis, coeff in op.terms.items():
        p = paulis[qubit]

        if p == 0 or p == axis:
            # Commutes: unchanged
            new_op.terms[paulis] = new_op.terms.get(paulis, 0) + coeff
        else:
            # Anticommutes: P_j -> cos(angle)*P_j + i*sin(angle)*P_axis*P_j
            # P_axis * P_j = i^phase * P_product
            phase_power, product = PAULI_MULT_TABLE[axis, p]
            phase = 1j ** int(phase_power)

            # cos term: same paulis
            new_op.terms[paulis] = new_op.terms.get(paulis, 0) + c * coeff

            # sin term: replace qubit's pauli with product
            new_paulis = list(paulis)
            new_paulis[qubit] = product
            new_paulis = tuple(new_paulis)
            # Factor: i * sin(angle) * phase (from Pauli product)
            # But in Heisenberg: U^dag P U, so the sign depends on commutation
            # For anticommuting P_j and P_axis:
            # e^{+i angle/2 P_axis} P_j e^{-i angle/2 P_axis}
            #   = cos(angle) P_j + sin(angle) * (i * P_axis * P_j)
            new_op.terms[new_paulis] = new_op.terms.get(new_paulis, 0) + s * (1j * phase) * coeff

    # Clean up near-zero terms
    new_op.terms = {k: v for k, v in new_op.terms.items() if abs(v) > 1e-15}
    return new_op


def apply_iswap_like_heisenberg(
    op: PauliOperator, q0: int, q1: int, theta: float = np.pi / 2, phi: float = 0.0
) -> PauliOperator:
    """
    Apply iSWAP-like gate in Heisenberg picture.

    The Willow iSWAP-like gate is:
      iSWAP(theta, phi) = exp(-i * (theta/2) * (XX + YY) - i * phi * (ZZ))

    For the standard iSWAP: theta = pi/2, phi = 0.
    Google's Sycamore/Willow uses a parameterized version.

    In the Heisenberg picture, we conjugate the observable:
      O -> U^dag O U

    For each Pauli string, we only need to update the two qubits
    involved in the gate. The transformation on the 2-qubit subspace
    is computed exactly.

    Args:
        op: PauliOperator to transform
        q0, q1: qubit indices
        theta: XX+YY coupling angle (pi/2 for standard iSWAP)
        phi: ZZ coupling angle
    """
    # Use precomputed lookup table for this (theta, phi)
    table = precompute_iswap_table(theta, phi)

    new_op = PauliOperator(op.n)

    for paulis, coeff in op.terms.items():
        p0, p1 = paulis[q0], paulis[q1]

        # Lookup precomputed conjugation result
        transformed = table[p0 * 4 + p1]

        for (new_p0, new_p1, phase) in transformed:
            new_paulis = list(paulis)
            new_paulis[q0] = new_p0
            new_paulis[q1] = new_p1
            key = tuple(new_paulis)
            new_op.terms[key] = new_op.terms.get(key, 0) + coeff * phase

    # Clean up
    new_op.terms = {k: v for k, v in new_op.terms.items() if abs(v) > 1e-15}
    return new_op


def _iswap_like_conjugate_2q(
    p0: int, p1: int, theta: float, phi: float
) -> list:
    """
    Compute U^dag (P0 x P1) U for iSWAP-like gate on 2 qubits.

    Returns list of (new_p0, new_p1, complex_phase) tuples.

    The iSWAP-like unitary is:
      U = exp(-i theta/2 (XX + YY)) * exp(-i phi ZZ)

    We decompose into ZZ rotation followed by XX+YY rotation.
    """
    results = []
    c = np.cos(theta)
    s = np.sin(theta)

    # First apply ZZ rotation: exp(-i phi ZZ)
    # ZZ commutes with II, IZ, ZI, ZZ (eigenvalue +1 or -1)
    # ZZ anticommutes with XI, IX, XZ, ZX, YI, IY, YZ, ZY, XY, YX, XX, YY

    # For ZZ rotation on (p0, p1):
    # Commutation: ZZ commutes with P0xP1 iff both P0,P1 commute or both anticommute with Z
    # Z commutes with I,Z; anticommutes with X,Y

    zz_terms = _zz_rotation_conjugate(p0, p1, phi)

    # Then apply XX+YY rotation to each resulting term
    for (pp0, pp1, zz_phase) in zz_terms:
        xxyy_terms = _xxyy_rotation_conjugate(pp0, pp1, theta)
        for (rp0, rp1, xxyy_phase) in xxyy_terms:
            results.append((rp0, rp1, zz_phase * xxyy_phase))

    # Merge duplicate Pauli pairs
    merged = {}
    for (rp0, rp1, phase) in results:
        key = (rp0, rp1)
        merged[key] = merged.get(key, 0) + phase

    return [(k[0], k[1], v) for k, v in merged.items() if abs(v) > 1e-15]


def _commutes_with_z(p: int) -> bool:
    """Does single-qubit Pauli p commute with Z?"""
    return p == 0 or p == 3  # I, Z commute; X, Y anticommute


def _zz_rotation_conjugate(p0: int, p1: int, phi: float) -> list:
    """Conjugate P0xP1 by exp(-i phi ZZ)."""
    # ZZ has eigenvalues +1 (for II, IZ, ZI, ZZ, XX, YY, XY, YX)
    # and -1 (for IX, XI, IY, YI, XZ, ZX, YZ, ZY) — wait, this isn't right.
    #
    # Actually: [ZZ, P0xP1] depends on commutation of each factor with Z.
    # If both P0 and P1 commute with Z, or both anticommute: P0xP1 commutes with ZZ.
    # If exactly one commutes and the other anticommutes: P0xP1 anticommutes with ZZ.

    c0 = _commutes_with_z(p0)
    c1 = _commutes_with_z(p1)

    if c0 == c1:
        # Commutes with ZZ: unchanged
        return [(p0, p1, 1.0)]
    else:
        # Anticommutes with ZZ
        # exp(i phi ZZ) (P0xP1) exp(-i phi ZZ) = cos(2phi)(P0xP1) + i sin(2phi) [ZZ, P0xP1]/(2i)
        # For anticommuting: e^{i phi ZZ} P e^{-i phi ZZ} = cos(2phi) P + i sin(2phi) ZZ*P
        c2p = np.cos(2 * phi)
        s2p = np.sin(2 * phi)

        # ZZ * (P0 x P1)
        ph0, r0 = PAULI_MULT_TABLE[3, p0]
        ph1, r1 = PAULI_MULT_TABLE[3, p1]
        total_phase = 1j ** int(ph0 + ph1)

        results = [(p0, p1, c2p)]
        if abs(s2p) > 1e-15:
            results.append((r0, r1, 1j * s2p * total_phase))
        return results


def _xxyy_rotation_conjugate(p0: int, p1: int, theta: float) -> list:
    """
    Conjugate P0xP1 by exp(-i theta/2 (XX + YY)).
    Uses precomputed lookup table for the given theta.
    """
    return _get_xxyy_table(theta)[p0 * 4 + p1]


# 4x4 Pauli matrices for 2-qubit system
_I = np.eye(2, dtype=complex)
_X = np.array([[0, 1], [1, 0]], dtype=complex)
_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_Z = np.array([[1, 0], [0, -1]], dtype=complex)
_PAULIS_1Q = [_I, _X, _Y, _Z]

# Cache for precomputed Pauli conjugation tables
_XXYY_TABLE_CACHE = {}
_ISWAP_TABLE_CACHE = {}


def _get_xxyy_table(theta: float) -> list:
    """
    Get or compute the 16-entry lookup table for XX+YY conjugation.
    Table maps (p0*4 + p1) -> list of (new_p0, new_p1, phase).
    """
    # Round theta to avoid floating point cache misses
    key = round(theta, 12)
    if key in _XXYY_TABLE_CACHE:
        return _XXYY_TABLE_CACHE[key]

    from scipy.linalg import expm

    # Build U = exp(-i theta (XX+YY)/2)
    XX = np.kron(_X, _X)
    YY = np.kron(_Y, _Y)
    H = (XX + YY) / 2.0
    U = expm(-1j * theta * H)
    Ud = U.conj().T

    # Precompute all 16 Pauli basis matrices
    pauli_basis = []
    for a in range(4):
        for b in range(4):
            pauli_basis.append(np.kron(_PAULIS_1Q[a], _PAULIS_1Q[b]))

    table = []
    for idx in range(16):
        P = pauli_basis[idx]
        result = Ud @ P @ U
        terms = []
        for out_idx in range(16):
            coeff = np.trace(pauli_basis[out_idx].conj().T @ result) / 4.0
            if abs(coeff) > 1e-12:
                terms.append((out_idx // 4, out_idx % 4, coeff))
        table.append(terms)

    _XXYY_TABLE_CACHE[key] = table
    return table


def precompute_iswap_table(theta: float, phi: float) -> list:
    """
    Precompute the full 16-entry lookup table for the iSWAP-like gate
    conjugation: U^dag (P0 x P1) U where U = exp(-i theta/2 (XX+YY)) exp(-i phi ZZ).

    Returns table[p0*4 + p1] -> list of (new_p0, new_p1, phase).
    """
    key = (round(theta, 12), round(phi, 12))
    if key in _ISWAP_TABLE_CACHE:
        return _ISWAP_TABLE_CACHE[key]

    table = []
    for p0 in range(4):
        for p1 in range(4):
            # Use the decomposed conjugation
            zz_terms = _zz_rotation_conjugate(p0, p1, phi)
            merged = {}
            for (pp0, pp1, zz_phase) in zz_terms:
                xxyy_terms = _xxyy_rotation_conjugate(pp0, pp1, theta)
                for (rp0, rp1, xxyy_phase) in xxyy_terms:
                    k = (rp0, rp1)
                    merged[k] = merged.get(k, 0) + zz_phase * xxyy_phase
            terms = [(k[0], k[1], v) for k, v in merged.items() if abs(v) > 1e-15]
            table.append(terms)

    _ISWAP_TABLE_CACHE[key] = table
    return table


# ============================================================
# Noise model
# ============================================================

def apply_depolarizing_noise(op: PauliOperator, gamma: float) -> PauliOperator:
    """
    Apply single-qubit depolarizing noise to all qubits.

    Under depolarizing noise with rate gamma, each Pauli string
    of weight w is damped by factor (1-gamma)^w.

    This is the key insight from Schuster et al.: noise exponentially
    suppresses high-weight Pauli strings, making truncation natural.

    Args:
        op: PauliOperator
        gamma: depolarizing rate per qubit (0 to 1)
    """
    damping = 1.0 - gamma
    new_op = PauliOperator(op.n)
    for paulis, coeff in op.terms.items():
        w = sum(1 for p in paulis if p != 0)
        new_op.terms[paulis] = coeff * (damping ** w)
    return new_op


def apply_gate_depolarizing_noise(
    op: PauliOperator, qubits: list, gamma_2q: float
) -> PauliOperator:
    """
    Apply 2-qubit depolarizing noise after a 2-qubit gate.

    Any Pauli string with non-identity support on the gate qubits
    is damped by (1 - gamma_2q).

    Args:
        op: PauliOperator
        qubits: list of 2 qubit indices involved in the gate
        gamma_2q: 2-qubit gate error rate
    """
    damping = 1.0 - gamma_2q
    new_op = PauliOperator(op.n)
    for paulis, coeff in op.terms.items():
        # Check if any of the gate qubits have non-identity Pauli
        has_support = any(paulis[q] != 0 for q in qubits)
        factor = damping if has_support else 1.0
        new_op.terms[paulis] = coeff * factor
    return new_op


# ============================================================
# Circuit construction (Willow-like)
# ============================================================

def build_2d_grid_connectivity(rows: int, cols: int) -> list:
    """
    Build the connectivity graph for a 2D grid (Willow-like).

    Returns list of (q0, q1) edges.
    """
    edges = []
    for r in range(rows):
        for c in range(cols):
            q = r * cols + c
            if c + 1 < cols:
                edges.append((q, q + 1))  # horizontal
            if r + 1 < rows:
                edges.append((q, (r + 1) * cols + c))  # vertical
    return edges


def generate_random_circuit_layers(
    n_qubits: int, edges: list, n_layers: int, seed: int = 42
) -> list:
    """
    Generate random circuit layers for OTOC simulation.

    Each layer consists of:
      1. Single-qubit random rotations on all qubits
      2. iSWAP-like gates on a subset of edges (alternating patterns)

    Returns list of layers, each layer is a list of gate dicts.
    """
    rng = np.random.RandomState(seed)
    layers = []

    for layer_idx in range(n_layers):
        gates = []

        # Single-qubit random rotations
        for q in range(n_qubits):
            axis = rng.choice([1, 2, 3])  # X, Y, or Z
            angle = rng.uniform(0, 2 * np.pi)
            gates.append({
                'type': 'single',
                'qubit': q,
                'axis': axis,
                'angle': angle
            })

        # Two-qubit iSWAP-like gates (alternating edge subsets)
        # Color edges into non-overlapping groups
        used_qubits = set()
        edge_subset = []
        shuffled_edges = list(edges)
        rng.shuffle(shuffled_edges)
        for (q0, q1) in shuffled_edges:
            if q0 not in used_qubits and q1 not in used_qubits:
                edge_subset.append((q0, q1))
                used_qubits.add(q0)
                used_qubits.add(q1)

        for (q0, q1) in edge_subset:
            theta = np.pi / 2 + rng.normal(0, 0.05)  # Near iSWAP
            phi = rng.uniform(0, 0.1)  # Small ZZ
            gates.append({
                'type': 'iswap_like',
                'qubits': (q0, q1),
                'theta': theta,
                'phi': phi
            })

        layers.append(gates)

    return layers


# ============================================================
# SPD OTOC computation
# ============================================================

def compute_otoc_spd(
    n_qubits: int,
    layers: list,
    observable_qubit: int,
    observable_pauli: int,
    perturbation_qubit: int,
    perturbation_pauli: int,
    max_weight: int,
    noise_gamma_2q: float = 0.0,
    noise_gamma_1q: float = 0.0,
    verbose: bool = False
) -> Tuple[complex, dict]:
    """
    Compute first-order OTOC using SPD.

    OTOC = <0| M U^dag B U |0> (simplified first-order correlator)

    More precisely, for the Quantum Echoes experiment:
    OTOC = Tr(|0><0| * M * U^dag * B * U) / 2^n

    In Heisenberg picture:
    1. Start with observable M (single Pauli)
    2. Evolve M backward through U^dag (= forward through U's inverse layers)
    3. Multiply by B
    4. Evolve forward through U
    5. Take expectation in |0><0>

    Equivalently:
    1. Start with B
    2. Evolve through U: B(t) = U^dag B U
    3. Compute <0| M B(t) |0>

    We use the second approach: evolve B through the circuit layers.

    Args:
        n_qubits: number of qubits
        layers: circuit layers (from generate_random_circuit_layers)
        observable_qubit: qubit index for M
        observable_pauli: Pauli type for M (1=X, 2=Y, 3=Z)
        perturbation_qubit: qubit index for B
        perturbation_pauli: Pauli type for B
        max_weight: SPD truncation threshold
        noise_gamma_2q: 2-qubit gate depolarizing rate
        noise_gamma_1q: 1-qubit gate depolarizing rate
        verbose: print diagnostics

    Returns:
        (otoc_value, diagnostics_dict)
    """
    t_start = time.time()

    # Initialize B as a single Pauli
    B_evolved = PauliOperator.single_pauli(
        n_qubits, perturbation_qubit, perturbation_pauli
    )

    diagnostics = {
        'n_terms_per_layer': [],
        'weight_distributions': [],
        'truncated_norm_loss': []
    }

    # Evolve B through each layer: B(t) = U^dag B U
    # In exact simulation, U = L_{n-1} ... L_1 L_0 (each layer built via U = U_gate @ U).
    # So U^dag B U = L_0^dag ... L_{n-1}^dag B L_{n-1} ... L_0.
    # Sequential conjugation: start from innermost pair (L_{n-1}), work outward.
    # => Process layers in REVERSE order, and within each layer, gates in REVERSE order.
    for layer_idx, layer in enumerate(reversed(layers)):
        for gate in reversed(layer):
            if gate['type'] == 'single':
                B_evolved = _apply_single_qubit_rotation_heisenberg(
                    B_evolved, gate['qubit'], gate['axis'], gate['angle']
                )
                if noise_gamma_1q > 0:
                    B_evolved = apply_gate_depolarizing_noise(
                        B_evolved, [gate['qubit']], noise_gamma_1q
                    )
            elif gate['type'] == 'iswap_like':
                q0, q1 = gate['qubits']
                B_evolved = apply_iswap_like_heisenberg(
                    B_evolved, q0, q1, gate['theta'], gate['phi']
                )
                if noise_gamma_2q > 0:
                    B_evolved = apply_gate_depolarizing_noise(
                        B_evolved, [q0, q1], noise_gamma_2q
                    )

        # Truncate by weight
        norm_before = B_evolved.norm_sq
        B_evolved = B_evolved.truncate(max_weight)
        norm_after = B_evolved.norm_sq

        diagnostics['n_terms_per_layer'].append(B_evolved.num_terms)
        diagnostics['weight_distributions'].append(B_evolved.weight_distribution())
        diagnostics['truncated_norm_loss'].append(
            (norm_before - norm_after) / max(norm_before, 1e-30)
        )

        if verbose and (layer_idx % max(1, len(layers) // 5) == 0):
            print(f"  Layer {layer_idx}/{len(layers)}: "
                  f"{B_evolved.num_terms} terms, "
                  f"max_weight={max(B_evolved.weight_distribution().keys()) if B_evolved.weight_distribution() else 0}, "
                  f"norm_loss={diagnostics['truncated_norm_loss'][-1]:.2e}")

    # Compute OTOC = Tr(M * B(t)) / 2^n for initial state |0><0>
    # For |0><0>, the expectation of a Pauli string P is:
    #   <0|P|0> = product over qubits of <0|P_i|0>
    #   = 1 if all P_i in {I, Z}, 0 otherwise
    #   with sign: <0|Z|0> = +1, <0|I|0> = +1

    # First multiply M * B(t) in Pauli basis
    M = PauliOperator.single_pauli(n_qubits, observable_qubit, observable_pauli)

    # <0| M B(t) |0> = sum_j c_j <0| M P_j |0>
    # M * P_j = phase * P_product
    otoc = 0.0
    for paulis_b, coeff_b in B_evolved.terms.items():
        # Multiply M (single Pauli on observable_qubit) with this term
        m_pauli = observable_pauli
        b_pauli_at_obs = paulis_b[observable_qubit]

        phase_power, product_pauli = PAULI_MULT_TABLE[m_pauli, b_pauli_at_obs]
        phase = 1j ** int(phase_power)

        # Build the resulting Pauli string
        result_paulis = list(paulis_b)
        result_paulis[observable_qubit] = product_pauli

        # Check if <0|result|0> is nonzero (all I or Z)
        expectation = 1.0
        for p in result_paulis:
            if p == 0 or p == 3:  # I or Z
                continue  # <0|I|0> = <0|Z|0> = 1
            else:
                expectation = 0.0
                break

        if expectation != 0:
            otoc += coeff_b * phase * expectation

    t_elapsed = time.time() - t_start
    diagnostics['wall_time_s'] = t_elapsed
    diagnostics['final_n_terms'] = B_evolved.num_terms

    return otoc, diagnostics


# ============================================================
# Exact simulation (for small systems, validation)
# ============================================================

def compute_otoc_exact(
    n_qubits: int,
    layers: list,
    observable_qubit: int,
    observable_pauli: int,
    perturbation_qubit: int,
    perturbation_pauli: int,
    noise_gamma_2q: float = 0.0
) -> complex:
    """
    Compute OTOC exactly using full state vector simulation.
    Only feasible for n <= ~16 qubits.

    OTOC = <0| M U^dag B U |0>
    """
    from scipy.linalg import expm

    N = 2 ** n_qubits

    # Build full unitary U from layers
    U = np.eye(N, dtype=complex)
    for layer in layers:
        for gate in layer:
            if gate['type'] == 'single':
                q = gate['qubit']
                axis_mat = _PAULIS_1Q[gate['axis']]
                u_1q = expm(-1j * gate['angle'] / 2 * axis_mat)
                # Embed in full space
                U_gate = _embed_1q_gate(u_1q, q, n_qubits)
                U = U_gate @ U
            elif gate['type'] == 'iswap_like':
                q0, q1 = gate['qubits']
                theta, phi = gate['theta'], gate['phi']
                XX = np.kron(_X, _X)
                YY = np.kron(_Y, _Y)
                ZZ = np.kron(_Z, _Z)
                H_2q = theta / 2 * (XX + YY) + phi * ZZ
                u_2q = expm(-1j * H_2q)
                U_gate = _embed_2q_gate(u_2q, q0, q1, n_qubits)
                U = U_gate @ U

    # Build M and B as full matrices
    M = _embed_1q_gate(_PAULIS_1Q[observable_pauli], observable_qubit, n_qubits)
    B = _embed_1q_gate(_PAULIS_1Q[perturbation_pauli], perturbation_qubit, n_qubits)

    # OTOC = <0| M U^dag B U |0>
    state_0 = np.zeros(N, dtype=complex)
    state_0[0] = 1.0

    # |psi1> = U |0>
    psi1 = U @ state_0
    # |psi2> = B |psi1>
    psi2 = B @ psi1
    # |psi3> = U^dag |psi2>
    psi3 = U.conj().T @ psi2
    # |psi4> = M |psi3>
    psi4 = M @ psi3
    # OTOC = <0|psi4>
    otoc = state_0.conj() @ psi4

    return otoc


def _embed_1q_gate(u: np.ndarray, qubit: int, n_qubits: int) -> np.ndarray:
    """Embed a 1-qubit gate into the full Hilbert space."""
    ops = [np.eye(2)] * n_qubits
    ops[qubit] = u
    result = ops[0]
    for op in ops[1:]:
        result = np.kron(result, op)
    return result


def _embed_2q_gate(u: np.ndarray, q0: int, q1: int, n_qubits: int) -> np.ndarray:
    """Embed a 2-qubit gate (on q0, q1) into the full Hilbert space."""
    # This is more complex if q0 and q1 are not adjacent
    # We use the permutation approach
    N = 2 ** n_qubits
    result = np.eye(N, dtype=complex)

    for i in range(N):
        for j in range(N):
            # Extract the 2-qubit state of (q0, q1)
            b_i_q0 = (i >> (n_qubits - 1 - q0)) & 1
            b_i_q1 = (i >> (n_qubits - 1 - q1)) & 1
            b_j_q0 = (j >> (n_qubits - 1 - q0)) & 1
            b_j_q1 = (j >> (n_qubits - 1 - q1)) & 1

            # Check that all other qubits match
            other_match = True
            for q in range(n_qubits):
                if q != q0 and q != q1:
                    if ((i >> (n_qubits - 1 - q)) & 1) != ((j >> (n_qubits - 1 - q)) & 1):
                        other_match = False
                        break

            if other_match:
                # 2-qubit indices
                idx_i = b_i_q0 * 2 + b_i_q1
                idx_j = b_j_q0 * 2 + b_j_q1
                result[i, j] = u[idx_i, idx_j]
            else:
                result[i, j] = 0.0

    return result


# ============================================================
# Main: validation test
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("SPD OTOC Validation: Small-scale test")
    print("=" * 60)

    for n_qubits in [4, 6, 8]:
        # Build circuit
        if n_qubits <= 6:
            rows, cols = 2, n_qubits // 2
        else:
            rows, cols = 2, 4
            n_qubits = rows * cols

        edges = build_2d_grid_connectivity(rows, cols)
        n_layers = 4
        layers = generate_random_circuit_layers(n_qubits, edges, n_layers, seed=42)

        # Observable M = Z on qubit 0, Perturbation B = X on last qubit
        obs_q, obs_p = 0, 3  # Z
        pert_q, pert_p = n_qubits - 1, 1  # X

        print(f"\n--- {n_qubits} qubits ({rows}x{cols}), {n_layers} layers ---")

        # Exact result
        if n_qubits <= 12:
            otoc_exact = compute_otoc_exact(
                n_qubits, layers, obs_q, obs_p, pert_q, pert_p
            )
            print(f"Exact OTOC:  {otoc_exact:.6f}")

        # SPD results at different truncation levels
        for max_w in [2, 4, 6, n_qubits]:
            otoc_spd, diag = compute_otoc_spd(
                n_qubits, layers, obs_q, obs_p, pert_q, pert_p,
                max_weight=max_w, verbose=False
            )
            error = abs(otoc_spd - otoc_exact) if n_qubits <= 12 else float('nan')
            print(f"SPD (w<={max_w:2d}): {otoc_spd:.6f}  "
                  f"|error|={error:.2e}  "
                  f"terms={diag['final_n_terms']:6d}  "
                  f"time={diag['wall_time_s']:.3f}s")

    print("\n" + "=" * 60)
    print("Validation complete.")
    print("=" * 60)
