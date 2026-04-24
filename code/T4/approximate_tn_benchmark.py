"""
T4: Approximate TN Contraction Benchmark at Small Scale
========================================================
Verify that approximate tensor network contraction with reduced
bond dimension chi can achieve fidelity exceeding ZCZ 3.0's
0.026% XEB on small-scale circuits, then extrapolate.

This is the CONSTRUCTIVE part of the T4 attack:
not just arguing quantum is weak, but SHOWING classical can match it.

Author: claude2
Date: 2026-04-25
"""

import numpy as np
import quimb.tensor as qtn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import time
import json

script_dir = Path(__file__).resolve().parent
results_dir = script_dir.parent.parent / "results" / "T4"
results_dir.mkdir(parents=True, exist_ok=True)


def build_rcs_circuit(n_rows, n_cols, depth, seed=42):
    """Build an RCS circuit on a 2D grid (same as tn_cost_estimation.py)."""
    rng = np.random.default_rng(seed)
    n_qubits = n_rows * n_cols
    circ = qtn.Circuit(n_qubits)

    edges = []
    for r in range(n_rows):
        for c in range(n_cols):
            q = r * n_cols + c
            if c + 1 < n_cols:
                edges.append((q, q + 1, 'H'))
            if r + 1 < n_rows:
                edges.append((q, q + n_cols, 'V'))

    patterns = [[], [], [], []]
    for q1, q2, direction in edges:
        r1, c1 = divmod(q1, n_cols)
        if direction == 'H':
            pattern_idx = (r1 % 2) * 2 + (c1 % 2)
        else:
            pattern_idx = (r1 % 2) * 2 + (c1 % 2)
        patterns[pattern_idx % 4].append((q1, q2))

    single_gate_set = ['RZ', 'RX', 'RZ']
    for cycle in range(depth):
        for q in range(n_qubits):
            angles = rng.uniform(0, 2 * np.pi, 3)
            for gate, angle in zip(single_gate_set, angles):
                circ.apply_gate(gate, angle, q)
        pattern = patterns[cycle % 4]
        for q1, q2 in pattern:
            if q1 < n_qubits and q2 < n_qubits:
                circ.apply_gate('CZ', q1, q2)

    return circ


def add_depolarizing_noise(circ, n_qubits, e_1q=0.001, e_2q=0.0038, e_ro=0.0087):
    """Apply depolarizing noise to the circuit state vector.

    Returns the noisy density matrix diagonal (probabilities).
    For small circuits, we can compute the ideal state vector,
    then apply noise analytically.
    """
    # Get ideal state vector
    psi = circ.psi.contract()
    probs_ideal = np.abs(psi.data.ravel())**2

    # Simple noise model: mix with uniform distribution
    # F_total = F_1q^N_1q * F_2q^N_2q * F_ro^N_ro
    # Noisy probs = F_total * ideal + (1 - F_total) * uniform
    # This is the leading-order depolarizing approximation

    # Count gates
    total_gates = len(circ.gates)
    n_2q = sum(1 for g in circ.gates if g.label == 'CZ')
    n_1q = total_gates - n_2q

    F_total = (1 - e_1q)**n_1q * (1 - e_2q)**n_2q * (1 - e_ro)**n_qubits
    uniform = np.ones_like(probs_ideal) / len(probs_ideal)
    probs_noisy = F_total * probs_ideal + (1 - F_total) * uniform

    return probs_ideal, probs_noisy, F_total


def compute_xeb(probs_ideal, samples_probs):
    """Compute linear XEB fidelity.

    XEB = D * <p_ideal(x)> - 1
    where the average is over samples x drawn from the sampling distribution.
    """
    D = len(probs_ideal)
    return D * np.mean(samples_probs) - 1


def approximate_contraction(circ, chi, n_qubits):
    """Contract the circuit TN approximately with max bond dimension chi.

    Uses quimb's MPS simulator with truncated bond dimension.
    Returns approximate probability distribution.
    """
    # Re-simulate with MPS backend at truncated bond dim
    circ_mps = qtn.Circuit(n_qubits, psi0=qtn.MPS_computational_state('0' * n_qubits))
    for gate in circ.gates:
        circ_mps.apply_gate(
            gate.label, *gate.params, *gate.qubits,
            max_bond=chi, cutoff=1e-12
        )
    psi_mps = circ_mps.psi
    # Contract to get full state vector for XEB comparison
    psi_full = psi_mps.contract()
    probs_approx = np.abs(psi_full.data.ravel())**2
    probs_approx = np.abs(probs_approx)
    total = probs_approx.sum()
    if total > 0:
        probs_approx /= total
    return probs_approx


# ============================================================
# Benchmark: fidelity vs bond dimension on small circuits
# ============================================================
print("=" * 70)
print("T4: Approximate TN Contraction Benchmark")
print("=" * 70)

# Test on multiple small circuits
test_configs = [
    (3, 3, 8, "9q/8d"),
    (3, 4, 10, "12q/10d"),
    (4, 4, 12, "16q/12d"),
]

chi_values = [2, 4, 8, 16, 32, 64]
all_results = []

for n_rows, n_cols, depth, label in test_configs:
    n_qubits = n_rows * n_cols
    print(f"\n--- {label}: {n_qubits} qubits, depth {depth} ---")

    circ = build_rcs_circuit(n_rows, n_cols, depth, seed=42)
    probs_ideal, probs_noisy, F_total = add_depolarizing_noise(circ, n_qubits)

    D = 2**n_qubits
    xeb_noisy = D * np.sum(probs_ideal * probs_noisy) - 1

    print(f"  F_total (noise model): {F_total:.6f}")
    print(f"  XEB of noisy quantum:  {xeb_noisy:.6f}")

    for chi in chi_values:
        if chi >= D:
            # Exact at this bond dim
            xeb_approx = 1.0
            t_elapsed = 0
        else:
            t0 = time.time()
            try:
                probs_approx = approximate_contraction(circ, chi, n_qubits)
                t_elapsed = time.time() - t0
                # XEB of approximate classical vs ideal
                xeb_approx = D * np.sum(probs_ideal * probs_approx) - 1
            except Exception as e:
                print(f"  chi={chi}: ERROR — {e}")
                xeb_approx = None
                t_elapsed = 0

        if xeb_approx is not None:
            beats_quantum = "WINS" if xeb_approx > xeb_noisy else "loses"
            print(f"  chi={chi:>3}: XEB_classical={xeb_approx:.6f} vs XEB_quantum={xeb_noisy:.6f} → {beats_quantum} ({t_elapsed:.2f}s)")

            all_results.append({
                'config': label,
                'n_qubits': n_qubits,
                'depth': depth,
                'chi': chi,
                'xeb_classical': float(xeb_approx),
                'xeb_quantum': float(xeb_noisy),
                'F_total': float(F_total),
                'time_s': t_elapsed,
                'beats_quantum': xeb_approx > xeb_noisy,
            })

# ============================================================
# Analysis and extrapolation
# ============================================================
print(f"\n{'=' * 70}")
print("Analysis: Minimum chi to beat quantum device")
print("=" * 70)

for config_label in set(r['config'] for r in all_results):
    config_results = [r for r in all_results if r['config'] == config_label]
    for r in config_results:
        if r['beats_quantum']:
            print(f"  {config_label}: chi={r['chi']} beats quantum (XEB {r['xeb_classical']:.4f} > {r['xeb_quantum']:.4f})")
            break
    else:
        print(f"  {config_label}: no chi tested beats quantum")

# ============================================================
# Generate figure
# ============================================================
fig, axes = plt.subplots(1, len(test_configs), figsize=(5 * len(test_configs), 5))
if len(test_configs) == 1:
    axes = [axes]

for idx, (n_rows, n_cols, depth, label) in enumerate(test_configs):
    ax = axes[idx]
    config_results = [r for r in all_results if r['config'] == label]
    if not config_results:
        continue

    chis = [r['chi'] for r in config_results]
    xebs_classical = [r['xeb_classical'] for r in config_results]
    xeb_quantum = config_results[0]['xeb_quantum']

    ax.semilogx(chis, xebs_classical, 'bo-', label='Classical (approx TN)')
    ax.axhline(y=xeb_quantum, color='red', linestyle='--', label=f'Quantum (noisy): {xeb_quantum:.4f}')
    ax.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
    ax.set_xlabel('Bond Dimension chi')
    ax.set_ylabel('XEB Fidelity')
    ax.set_title(f'{label}')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.suptitle('Approximate TN vs Noisy Quantum: XEB Fidelity', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(results_dir / 'T4_approx_tn_benchmark.png', dpi=300, bbox_inches='tight')
plt.savefig(results_dir / 'T4_approx_tn_benchmark.pdf', bbox_inches='tight')
print(f"\nFigure saved to {results_dir}/")

# Save results
json_path = results_dir / 'T4_approx_tn_benchmark.json'
with open(json_path, 'w') as f:
    json.dump(all_results, f, indent=2, default=str)
print(f"Results saved to {json_path}")
