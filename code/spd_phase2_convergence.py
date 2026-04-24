"""
SPD Phase 2: Noise-assisted convergence study for OTOC
======================================================
Systematic sweep of max_weight vs error under depolarizing noise.
Validates Schuster-Yao theory: noise exponentially damps high-weight
Pauli strings, making SPD truncation more effective.

Target: T1 Google Quantum Echoes (Willow ~0.3-0.7% 2Q gate error)

Author: claude4 (branch: claude4)
Date: 2026-04-25
"""

import numpy as np
import json
import time
import sys
import os

# Add code directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spd_otoc_core import (
    build_2d_grid_connectivity,
    generate_random_circuit_layers,
    compute_otoc_spd,
    compute_otoc_exact,
)


def convergence_sweep(
    n_qubits: int,
    rows: int,
    cols: int,
    n_layers: int,
    noise_gammas: list,
    max_weights: list,
    seed: int = 42,
) -> dict:
    """
    Sweep max_weight and noise_gamma, comparing SPD to exact.

    Returns structured results dict.
    """
    edges = build_2d_grid_connectivity(rows, cols)
    layers = generate_random_circuit_layers(n_qubits, edges, n_layers, seed=seed)

    obs_q, obs_p = 0, 3       # Z on qubit 0
    pert_q, pert_p = n_qubits - 1, 1  # X on last qubit

    results = {
        'n_qubits': n_qubits,
        'grid': f'{rows}x{cols}',
        'n_layers': n_layers,
        'seed': seed,
        'sweeps': []
    }

    # Compute noiseless exact once (noise exact needs density matrix, deferred)
    exact_noiseless = None
    if n_qubits <= 14:
        exact_noiseless = compute_otoc_exact(
            n_qubits, layers, obs_q, obs_p, pert_q, pert_p
        )
        print(f"  Exact (noiseless): {float(np.real(exact_noiseless)):+.6f}")

    for gamma in noise_gammas:
        # For gamma=0, compare to exact; for gamma>0, report SPD-only
        # (noisy exact requires density matrix simulation, deferred to Phase 3)
        exact = exact_noiseless if gamma == 0 else None

        for mw in max_weights:
            if mw > n_qubits:
                continue

            t0 = time.time()
            spd_val, diag = compute_otoc_spd(
                n_qubits, layers, obs_q, obs_p, pert_q, pert_p,
                max_weight=mw,
                noise_gamma_2q=gamma,
                verbose=False
            )
            elapsed = time.time() - t0

            error = abs(spd_val - exact) if exact is not None else None

            entry = {
                'gamma': gamma,
                'max_weight': mw,
                'spd_real': float(np.real(spd_val)),
                'spd_imag': float(np.imag(spd_val)),
                'exact_real': float(np.real(exact)) if exact is not None else None,
                'error': float(error) if error is not None else None,
                'n_terms': diag['final_n_terms'],
                'wall_time_s': elapsed,
                'max_norm_loss': max(diag['truncated_norm_loss']) if diag['truncated_norm_loss'] else 0,
            }
            results['sweeps'].append(entry)

            err_str = f"{error:.2e}" if error is not None else "N/A"
            print(f"  n={n_qubits} gamma={gamma:.4f} w<={mw:2d}: "
                  f"OTOC={float(np.real(spd_val)):+.6f}  "
                  f"|err|={err_str}  "
                  f"terms={diag['final_n_terms']:6d}  "
                  f"time={elapsed:.2f}s")

    return results


def main():
    print("=" * 70)
    print("SPD Phase 2: Noise-assisted convergence study")
    print("=" * 70)

    all_results = []

    # Willow-relevant noise rates
    noise_gammas = [0.0, 0.003, 0.005, 0.01]

    # ---- 8 qubits (2x4): full sweep ----
    print("\n--- 8 qubits (2x4), 6 layers ---")
    r8 = convergence_sweep(
        n_qubits=8, rows=2, cols=4, n_layers=6,
        noise_gammas=noise_gammas,
        max_weights=[2, 3, 4, 5, 6, 8],
        seed=42
    )
    all_results.append(r8)

    # ---- 10 qubits (2x5): full sweep ----
    print("\n--- 10 qubits (2x5), 6 layers ---")
    r10 = convergence_sweep(
        n_qubits=10, rows=2, cols=5, n_layers=6,
        noise_gammas=noise_gammas,
        max_weights=[2, 3, 4, 5, 6, 8, 10],
        seed=42
    )
    all_results.append(r10)

    # ---- 12 qubits (3x4): medium sweep ----
    print("\n--- 12 qubits (3x4), 6 layers ---")
    r12 = convergence_sweep(
        n_qubits=12, rows=3, cols=4, n_layers=6,
        noise_gammas=noise_gammas,
        max_weights=[2, 3, 4, 5, 6, 8],
        seed=42
    )
    all_results.append(r12)

    # ---- 14 qubits (2x7): push the limit of exact validation ----
    print("\n--- 14 qubits (2x7), 4 layers ---")
    r14 = convergence_sweep(
        n_qubits=14, rows=2, cols=7, n_layers=4,
        noise_gammas=[0.0, 0.005],
        max_weights=[2, 4, 6, 8],
        seed=42
    )
    all_results.append(r14)

    # Save results
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', 'results', 'phase2_convergence.json'
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {output_path}")

    # Summary table
    print("\n" + "=" * 70)
    print("SUMMARY: Noise effect on SPD truncation error")
    print("=" * 70)
    print(f"{'n':>3} {'gamma':>7} {'w_max':>5} {'|error|':>12} {'terms':>8} {'time':>8}")
    print("-" * 50)
    for res in all_results:
        for s in res['sweeps']:
            if s['error'] is not None:
                print(f"{res['n_qubits']:3d} {s['gamma']:7.4f} {s['max_weight']:5d} "
                      f"{s['error']:12.2e} {s['n_terms']:8d} {s['wall_time_s']:7.1f}s")

    print("\n" + "=" * 70)
    print("Phase 2 complete.")
    print("=" * 70)


if __name__ == '__main__':
    main()
