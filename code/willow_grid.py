"""
Willow Grid Generator
=====================
Constructs the qubit connectivity graph for Google's Willow processor
and generates OTOC circuit configurations matching the Quantum Echoes
experiment.

The Willow chip uses a 2D grid of ~105 transmon qubits with
nearest-neighbor coupling. OTOC experiments typically use a subset
(e.g., 65 or 95 qubits).

This module will be updated with exact parameters once claude7/claude8
extract them from the Google Nature 2025 paper.

Author: claude4 (branch: claude4)
Date: 2026-04-25
"""

import numpy as np
from spd_otoc_core import (
    build_2d_grid_connectivity,
    generate_random_circuit_layers,
    PauliOperator,
)


def build_willow_grid(rows: int = 10, cols: int = 10, active_qubits: int = None):
    """
    Build Willow-like 2D grid connectivity.

    Args:
        rows, cols: grid dimensions (default 10x10 ≈ Willow 105q)
        active_qubits: if set, use only first N qubits (for subgrid experiments)

    Returns:
        (n_qubits, edges, qubit_positions)
    """
    n_total = rows * cols
    n_qubits = active_qubits if active_qubits else n_total

    edges = build_2d_grid_connectivity(rows, cols)

    # Filter edges to active qubits
    if active_qubits and active_qubits < n_total:
        edges = [(q0, q1) for q0, q1 in edges if q0 < n_qubits and q1 < n_qubits]

    # Qubit positions for visualization
    positions = {}
    for q in range(n_qubits):
        r, c = divmod(q, cols)
        positions[q] = (c, -r)  # x=col, y=-row (top-left origin)

    return n_qubits, edges, positions


def manhattan_distance(q0: int, q1: int, cols: int) -> int:
    """Manhattan distance between two qubits on a grid."""
    r0, c0 = divmod(q0, cols)
    r1, c1 = divmod(q1, cols)
    return abs(r0 - r1) + abs(c0 - c1)


def generate_otoc_config(
    rows: int,
    cols: int,
    obs_qubit: int = None,
    pert_qubit: int = None,
    n_layers_per_arm: int = 8,
    seed: int = 42,
):
    """
    Generate a complete OTOC circuit configuration.

    If obs_qubit/pert_qubit not specified, places them at grid center
    with distance ~2-3 (nearby, for strong signal).

    Args:
        rows, cols: grid dimensions
        obs_qubit: M operator qubit (default: center)
        pert_qubit: B operator qubit (default: center+1)
        n_layers_per_arm: circuit depth per OTOC arm
        seed: random seed

    Returns:
        config dict with all parameters
    """
    n_qubits = rows * cols

    # Default: M and B on center qubits (nearby)
    center_r, center_c = rows // 2, cols // 2
    if obs_qubit is None:
        obs_qubit = center_r * cols + center_c
    if pert_qubit is None:
        pert_qubit = center_r * cols + (center_c + 1)  # adjacent

    edges = build_2d_grid_connectivity(rows, cols)
    dist = manhattan_distance(obs_qubit, pert_qubit, cols)

    layers = generate_random_circuit_layers(
        n_qubits, edges, n_layers_per_arm, seed=seed
    )

    return {
        'n_qubits': n_qubits,
        'rows': rows,
        'cols': cols,
        'edges': edges,
        'layers': layers,
        'obs_qubit': obs_qubit,
        'obs_pauli': 3,  # Z
        'pert_qubit': pert_qubit,
        'pert_pauli': 1,  # X
        'n_layers_per_arm': n_layers_per_arm,
        'mb_distance': dist,
        'seed': seed,
    }


def estimate_spd_cost(n_qubits: int, max_weight: int) -> dict:
    """
    Estimate SPD computational cost for given parameters.

    Returns dict with estimated term count and memory.
    """
    from math import comb

    # Upper bound on terms: sum_{w=0}^{max_weight} C(n, w) * 3^w
    max_terms = sum(comb(n_qubits, w) * (3 ** w) for w in range(max_weight + 1))

    # Memory per term: tuple of n ints (8 bytes) + complex (16 bytes)
    bytes_per_term = n_qubits * 1 + 16  # compact storage
    max_memory_gb = max_terms * bytes_per_term / 1e9

    # OTOC^(2) A^2 pairing cost: O(terms^2) worst case
    pairing_ops = max_terms ** 2

    return {
        'max_terms': max_terms,
        'max_memory_gb': max_memory_gb,
        'pairing_ops': pairing_ops,
        'feasible_single_gpu_8gb': max_memory_gb < 6.0,
    }


if __name__ == '__main__':
    print("Willow Grid SPD Cost Estimates")
    print("=" * 60)

    configs = [
        ("Phase 3 validated", 4, 4, 4),
        ("Willow subset", 6, 6, 10),
        ("Willow subset", 8, 8, 12),
        ("Willow OTOC^(2)", 8, 8, 15),
        ("Willow full", 10, 10, 15),
        ("Willow full", 10, 10, 20),
    ]

    print(f"{'Config':<20} {'n':>4} {'w_max':>6} {'max_terms':>12} {'mem_GB':>8} {'feasible':>8}")
    print("-" * 60)

    for name, r, c, w in configs:
        n = r * c
        est = estimate_spd_cost(n, w)
        print(f"{name:<20} {n:4d} {w:6d} {est['max_terms']:12,d} "
              f"{est['max_memory_gb']:8.2f} {'YES' if est['feasible_single_gpu_8gb'] else 'NO':>8}")

    print()
    print("Note: actual term count is much smaller than upper bound")
    print("(SPD truncation + circuit structure reduce terms significantly)")
    print()

    # Generate a sample Willow config
    config = generate_otoc_config(8, 8, n_layers_per_arm=6)
    print(f"Sample 8x8 OTOC config:")
    print(f"  M on qubit {config['obs_qubit']} (center)")
    print(f"  B on qubit {config['pert_qubit']} (adjacent)")
    print(f"  M-B distance: {config['mb_distance']}")
    print(f"  Layers per arm: {config['n_layers_per_arm']}")
    print(f"  Total edges: {len(config['edges'])}")
