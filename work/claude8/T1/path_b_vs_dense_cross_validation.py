"""
T1 Path B Schuster-Yin Pauli-path vs dense-matrix simulator cross-validation.

Per AGENTS.md §D5 multi-method cross-validation: same problem, two
independent classical paths, deviation falls within combined uncertainty.

Path 1: my run_schuster_pauli_path_attack (Pauli-path with ell-truncation;
        unbounded ell = no truncation = exact)
Path 2: dense-matrix direct computation:
            U = product of fSim/iSWAP gates and single-qubit gates
            M(t) = U^dag * M * U
            OTOC^(2) = Tr(M(t) * B * M(t) * B) / 2^n

Both should give the same OTOC^(2) value at full ell (no truncation).

Run: python work/claude8/T1/path_b_vs_dense_cross_validation.py
"""
import sys
from pathlib import Path
import numpy as np

# Make pauli_path_baseline importable
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from pauli_path_baseline import (
    run_schuster_pauli_path_attack,
    build_iswap_brickwall_circuit,
    pauli_string_init,
)


# ============================================================================
# Dense-matrix reference: build the brickwall circuit's unitary explicitly
# and compute OTOC^(2) = Tr(M(t) B M(t) B) / 2^n directly.
# ============================================================================

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
PAULI = [I2, X, Y, Z]

# iSWAP 4x4 matrix
ISWAP = np.array([
    [1, 0, 0, 0],
    [0, 0, 1j, 0],
    [0, 1j, 0, 0],
    [0, 0, 0, 1],
], dtype=complex)

# Single-qubit gates: U = exp(-i*pi/4 * P) for P in {X, Y, W=(X+Y)/sqrt(2)}
# Note: this is the convention used by conjugate_pauli_clifford_sqrt_x etc.
# (U^dag * P_q * U with U = sqrt_X = exp(-i*pi/4 * X) gives the table Y -> -Z, Z -> Y)
def single_qubit_gate(axis_label):
    """Return 2x2 matrix for X^1/2, Y^1/2, or W^1/2."""
    if axis_label == "X^1/2":
        gen = X
    elif axis_label == "Y^1/2":
        gen = Y
    elif axis_label == "W^1/2":
        gen = (X + Y) / np.sqrt(2)
    else:
        raise ValueError(f"unknown axis {axis_label}")
    return np.cos(np.pi / 4) * I2 - 1j * np.sin(np.pi / 4) * gen


def kron_n(matrices):
    """Tensor product of a list of matrices."""
    result = matrices[0]
    for m in matrices[1:]:
        result = np.kron(result, m)
    return result


def single_qubit_op_on(gate_2x2, qubit, n_qubits):
    """Embed a 2x2 single-qubit gate at `qubit` index in n_qubits system.

    Convention: qubit 0 is the leftmost factor in the Kronecker product.
    """
    factors = [I2] * n_qubits
    factors[qubit] = gate_2x2
    return kron_n(factors)


def two_qubit_iswap_on(qa, qb, n_qubits):
    """Embed iSWAP on (qa, qb) into n_qubits dense matrix.

    For non-adjacent qubits this still acts only on the (qa, qb) subsystem.
    Implementation: build full operator via permutation of the 4-qubit
    sub-action.
    """
    if qa == qb:
        raise ValueError("qa != qb required")
    if qa > qb:
        qa, qb = qb, qa
    # Construct dense matrix dimension 2^n
    dim = 1 << n_qubits
    out = np.zeros((dim, dim), dtype=complex)
    # iSWAP acts on |q_a q_b> basis: 00 -> 00, 01 -> i*10, 10 -> i*01, 11 -> 11
    # For each computational basis state |i>, swap bits at qa and qb with phase.
    # We index bits as: bit position k = qubit k (qubit 0 most significant)
    # so that kron_n([I, ..., gate, ..., I]) places `gate` at the qubit-th
    # tensor factor.
    for i in range(dim):
        ba = (i >> (n_qubits - 1 - qa)) & 1
        bb = (i >> (n_qubits - 1 - qb)) & 1
        if ba == bb:
            # Diagonal entries: |00> -> |00>, |11> -> |11>
            out[i, i] = 1.0
        else:
            # Swap qa and qb bits, multiply by i
            j = i
            # Flip bits at positions qa and qb
            j ^= (1 << (n_qubits - 1 - qa))
            j ^= (1 << (n_qubits - 1 - qb))
            out[j, i] = 1j
    return out


def build_circuit_unitary(circuit_spec):
    """Build full circuit unitary U from circuit_spec."""
    n_qubits = circuit_spec["n_qubits"]
    dim = 1 << n_qubits
    U = np.eye(dim, dtype=complex)
    for cycle in circuit_spec["cycles"]:
        # 1. Single-qubit layer
        sq = cycle["single_qubit_layer"]
        # Build the parallel single-qubit-layer matrix as kron of per-qubit gates
        gate_per_qubit = [I2] * n_qubits
        for qubit_idx, axis_label in sq:
            gate_per_qubit[qubit_idx] = single_qubit_gate(axis_label)
        sq_matrix = kron_n(gate_per_qubit)
        U = sq_matrix @ U

        # 2. Two-qubit sublayers
        for sublayer in cycle["two_qubit_sublayers"]:
            for qa, qb in sublayer["pairs"]:
                tq = two_qubit_iswap_on(qa, qb, n_qubits)
                U = tq @ U
    return U


def pauli_string_to_dense(string, n_qubits):
    """Convert a tuple-encoded Pauli string to its dense 2^n x 2^n matrix."""
    factors = [PAULI[p] for p in string]
    return kron_n(factors)


def dense_otoc2(circuit_spec, M_qubit, B_qubit, M_pauli="Z", B_pauli="X"):
    """Compute OTOC^(2) = Tr(M(t) B M(t) B) / 2^n via dense matrices."""
    n_qubits = circuit_spec["n_qubits"]
    dim = 1 << n_qubits

    # Build initial M and B as dense matrices
    pauli_letter_to_int = {"I": 0, "X": 1, "Y": 2, "Z": 3}
    M_string = [0] * n_qubits
    M_string[M_qubit] = pauli_letter_to_int[M_pauli]
    B_string = [0] * n_qubits
    B_string[B_qubit] = pauli_letter_to_int[B_pauli]
    M_dense = pauli_string_to_dense(tuple(M_string), n_qubits)
    B_dense = pauli_string_to_dense(tuple(B_string), n_qubits)

    # Build U
    U = build_circuit_unitary(circuit_spec)

    # M(t) = U^dag * M * U
    M_t = U.conj().T @ M_dense @ U

    # OTOC^(2) = Tr(M(t) B M(t) B) / 2^n
    product = M_t @ B_dense @ M_t @ B_dense
    return np.trace(product) / dim


# ============================================================================
# Cross-validation harness
# ============================================================================

def cross_validate(grid_shape, depth, M_qubit, B_qubit, weight_bound_l, seed):
    """Run Path B and dense-matrix simulator on the same problem; compare."""
    n_qubits = grid_shape[0] * grid_shape[1]
    if n_qubits > 8:
        # Dense-matrix gets expensive: 2^n x 2^n = 2^16 x 2^16 = 65k x 65k for 16q.
        # Keep this validator at <= 8 qubits (4q is the natural choice).
        raise ValueError(
            f"dense reference only feasible for <= 8 qubits; got {n_qubits}"
        )

    # Path B
    pb_result = run_schuster_pauli_path_attack(
        grid_shape=grid_shape,
        depth=depth,
        M_qubit=M_qubit,
        B_qubit=B_qubit,
        weight_bound_l=weight_bound_l,
        seed=seed,
    )
    pb_otoc = pb_result.circuit_meta["otoc2_value"]

    # Dense-matrix path
    circuit = build_iswap_brickwall_circuit(grid_shape, depth, seed)
    dense_otoc = dense_otoc2(circuit, M_qubit, B_qubit, "Z", "X")

    # Comparison
    diff = abs(pb_otoc - dense_otoc)
    return {
        "grid_shape": grid_shape,
        "depth": depth,
        "weight_bound_l": weight_bound_l,
        "seed": seed,
        "n_qubits": n_qubits,
        "path_b_otoc": pb_otoc,
        "path_b_n_strings_kept": pb_result.n_pauli_strings_kept,
        "dense_otoc": dense_otoc,
        "abs_diff": diff,
        "agree_at_1e-10": diff < 1e-10,
    }


if __name__ == "__main__":
    print("T1 Path B vs dense-matrix cross-validation (D5 multi-method check)")
    print("=" * 70)

    test_cases = [
        # 4-qubit small circuits: dense feasible, full-weight Path B = exact
        {"grid_shape": (2, 2), "depth": 1, "M_qubit": 0, "B_qubit": 3,
         "weight_bound_l": 4, "seed": 0},
        {"grid_shape": (2, 2), "depth": 1, "M_qubit": 0, "B_qubit": 0,
         "weight_bound_l": 4, "seed": 0},  # anti-commuting (M, B same qubit)
        {"grid_shape": (2, 2), "depth": 2, "M_qubit": 0, "B_qubit": 3,
         "weight_bound_l": 4, "seed": 42},
        {"grid_shape": (2, 2), "depth": 2, "M_qubit": 0, "B_qubit": 3,
         "weight_bound_l": 4, "seed": 1},
        # 6-qubit (2x3): still feasible (dim 64); test with full-weight (l=6)
        {"grid_shape": (2, 3), "depth": 1, "M_qubit": 0, "B_qubit": 5,
         "weight_bound_l": 6, "seed": 0},
        {"grid_shape": (2, 3), "depth": 2, "M_qubit": 0, "B_qubit": 5,
         "weight_bound_l": 6, "seed": 7},
    ]

    n_pass = 0
    for i, tc in enumerate(test_cases):
        result = cross_validate(**tc)
        agree = result["agree_at_1e-10"]
        n_pass += int(agree)
        status = "AGREE" if agree else "DISAGREE"
        print(
            f"Test {i+1}: grid={result['grid_shape']} d={result['depth']} "
            f"M@{tc['M_qubit']} B@{tc['B_qubit']} ell={result['weight_bound_l']} "
            f"seed={result['seed']}"
        )
        print(
            f"  Path B OTOC^(2) = {result['path_b_otoc']:.6e}   "
            f"({result['path_b_n_strings_kept']} strings kept)"
        )
        print(f"  Dense   OTOC^(2) = {result['dense_otoc']:.6e}")
        print(
            f"  |diff| = {result['abs_diff']:.3e}    {status} "
            f"(threshold 1e-10)"
        )
        print()

    print("=" * 70)
    print(f"Result: {n_pass}/{len(test_cases)} tests AGREE at 1e-10")
    if n_pass == len(test_cases):
        print()
        print("PASS: Path B Schuster-Yin Pauli-path matches dense-matrix simulator")
        print("  on all test cases - D5 multi-method cross-validation PASS.")
    else:
        print()
        print("FAIL: At least one test failed. Path B implementation has a bug;")
        print("  investigate above failures.")
        sys.exit(1)
