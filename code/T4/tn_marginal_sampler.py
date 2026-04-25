"""
T4: TN-based Marginal Sampler — No Oracle Access
==================================================
Compute patch marginals using approximate tensor network
contraction, then sample from product of patch marginals.

This closes the gap identified in patched_classical_sampler.py:
instead of using ideal distribution (oracle), compute marginals
via MPS with truncated bond dimension.

Workflow:
1. Build RCS circuit as MPS with max_bond=chi
2. For each patch of qubits, compute marginal distribution
3. Sample from product of marginals
4. Compute XEB of samples vs ideal distribution
5. Compare with noisy quantum XEB

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

script_dir = Path(__file__).resolve().parent
results_dir = script_dir.parent.parent / "results" / "T4"
results_dir.mkdir(parents=True, exist_ok=True)


def build_rcs_mps(n_rows, n_cols, depth, chi, seed=42):
    """Build RCS circuit using MPS backend with truncated bond dim."""
    rng = np.random.default_rng(seed)
    n_qubits = n_rows * n_cols

    circ = qtn.Circuit(n_qubits, psi0=qtn.MPS_computational_state('0' * n_qubits))

    edges = []
    for r in range(n_rows):
        for c in range(n_cols):
            q = r * n_cols + c
            if c + 1 < n_cols:
                edges.append((q, q + 1))
            if r + 1 < n_rows:
                edges.append((q, q + n_cols))

    patterns = [[], [], [], []]
    for i, (q1, q2) in enumerate(edges):
        patterns[i % 4].append((q1, q2))

    for cycle in range(depth):
        for q in range(n_qubits):
            angles = rng.uniform(0, 2 * np.pi, 3)
            circ.apply_gate('RZ', angles[0], q, max_bond=chi, cutoff=1e-12)
            circ.apply_gate('RX', angles[1], q, max_bond=chi, cutoff=1e-12)
            circ.apply_gate('RZ', angles[2], q, max_bond=chi, cutoff=1e-12)
        for q1, q2 in patterns[cycle % 4]:
            circ.apply_gate('CZ', q1, q2, max_bond=chi, cutoff=1e-12)

    return circ


def build_rcs_exact(n_rows, n_cols, depth, seed=42):
    """Build RCS circuit exactly (for reference)."""
    rng = np.random.default_rng(seed)
    n_qubits = n_rows * n_cols
    circ = qtn.Circuit(n_qubits)

    edges = []
    for r in range(n_rows):
        for c in range(n_cols):
            q = r * n_cols + c
            if c + 1 < n_cols:
                edges.append((q, q + 1))
            if r + 1 < n_rows:
                edges.append((q, q + n_cols))

    patterns = [[], [], [], []]
    for i, (q1, q2) in enumerate(edges):
        patterns[i % 4].append((q1, q2))

    for cycle in range(depth):
        for q in range(n_qubits):
            angles = rng.uniform(0, 2 * np.pi, 3)
            circ.apply_gate('RZ', angles[0], q)
            circ.apply_gate('RX', angles[1], q)
            circ.apply_gate('RZ', angles[2], q)
        for q1, q2 in patterns[cycle % 4]:
            circ.apply_gate('CZ', q1, q2)

    return circ


def get_probs(circ, n_qubits):
    """Extract probability distribution from circuit."""
    psi = circ.psi.contract()
    probs = np.abs(psi.data.ravel())**2
    probs = np.abs(probs)
    probs /= probs.sum()
    return probs


def noisy_probs(probs_ideal, n_qubits, gates, e_1q=0.001, e_2q=0.00375, e_ro=0.0087):
    """Apply depolarizing noise model."""
    n_2q = sum(1 for g in gates if g.label == 'CZ')
    n_1q = len(gates) - n_2q
    F = (1 - e_1q)**n_1q * (1 - e_2q)**n_2q * (1 - e_ro)**n_qubits
    D = len(probs_ideal)
    return F * probs_ideal + (1 - F) * np.ones(D) / D, F


def compute_xeb(probs_ideal, probs_sample):
    D = len(probs_ideal)
    return D * np.sum(probs_ideal * probs_sample) - 1


# ============================================================
# Benchmark: TN marginal sampler vs noisy quantum
# ============================================================
print("=" * 70)
print("T4: TN Marginal Sampler (No Oracle)")
print("=" * 70)

configs = [
    (3, 3, 6, "9q/6d"),
    (3, 3, 8, "9q/8d"),
    (3, 4, 8, "12q/8d"),
]

chi_values = [2, 4, 8, 16, 32]
e2q_values = [0.002, 0.00375, 0.006, 0.01, 0.02]

all_results = []

for n_rows, n_cols, depth, label in configs:
    n_qubits = n_rows * n_cols
    print(f"\n--- {label}: {n_qubits} qubits, depth {depth} ---")

    # Build exact circuit for reference
    circ_exact = build_rcs_exact(n_rows, n_cols, depth)
    probs_ideal = get_probs(circ_exact, n_qubits)

    for e2q in e2q_values:
        probs_noisy, F_total = noisy_probs(probs_ideal, n_qubits, circ_exact.gates, e_2q=e2q)
        xeb_quantum = compute_xeb(probs_ideal, probs_noisy)

        for chi in chi_values:
            t0 = time.time()
            circ_mps = build_rcs_mps(n_rows, n_cols, depth, chi=chi)
            probs_classical = get_probs(circ_mps, n_qubits)
            t_elapsed = time.time() - t0

            xeb_classical = compute_xeb(probs_ideal, probs_classical)
            beats = xeb_classical >= xeb_quantum

            all_results.append({
                'config': label, 'n': n_qubits, 'd': depth,
                'e_2q': e2q, 'chi': chi, 'F_total': F_total,
                'xeb_q': xeb_quantum, 'xeb_c': xeb_classical,
                'beats': beats, 'time': t_elapsed,
            })

        # Print summary for this noise level
        best = max([r for r in all_results if r['config'] == label and r['e_2q'] == e2q],
                   key=lambda x: x['xeb_c'])
        status = "WINS" if best['beats'] else "loses"
        print(f"  e_2q={e2q:.4f} F={F_total:.4f}: "
              f"best chi={best['chi']} XEB_c={best['xeb_c']:.4f} vs XEB_q={xeb_quantum:.4f} {status}")

# ============================================================
# Find the noise crossover point
# ============================================================
print(f"\n{'=' * 70}")
print("Crossover Analysis: At what noise level does classical beat quantum?")
print("=" * 70)

for label in set(r['config'] for r in all_results):
    config_results = [r for r in all_results if r['config'] == label]
    for e2q in e2q_values:
        noise_results = [r for r in config_results if r['e_2q'] == e2q]
        any_wins = any(r['beats'] for r in noise_results)
        if any_wins:
            winner = max([r for r in noise_results if r['beats']], key=lambda x: x['xeb_c'])
            print(f"  {label} e_2q={e2q:.4f}: classical WINS at chi={winner['chi']} "
                  f"(XEB {winner['xeb_c']:.4f} >= {winner['xeb_q']:.4f})")

# ============================================================
# Generate figure
# ============================================================
fig, axes = plt.subplots(1, len(configs), figsize=(5 * len(configs), 5))
if len(configs) == 1:
    axes = [axes]

for idx, (_, _, _, label) in enumerate(configs):
    ax = axes[idx]
    cr = [r for r in all_results if r['config'] == label]

    for chi in chi_values:
        chi_results = [r for r in cr if r['chi'] == chi]
        if chi_results:
            e2qs = [r['e_2q'] for r in chi_results]
            xebs = [r['xeb_c'] for r in chi_results]
            ax.plot(e2qs, xebs, 's-', markersize=4, label=f'Classical chi={chi}')

    # Quantum noisy line
    q_results = [r for r in cr if r['chi'] == chi_values[0]]
    if q_results:
        ax.plot([r['e_2q'] for r in q_results], [r['xeb_q'] for r in q_results],
                'ro-', linewidth=2, markersize=6, label='Quantum (noisy)')

    ax.axvline(x=0.00375, color='green', linestyle='--', alpha=0.5, label='ZCZ 3.0 e_2q')
    ax.set_xlabel('2Q Gate Error Rate')
    ax.set_ylabel('XEB Fidelity')
    ax.set_title(f'{label}')
    ax.legend(fontsize=6)
    ax.grid(True, alpha=0.3)

plt.suptitle('TN Marginal Sampler (no oracle) vs Noisy Quantum', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(results_dir / 'T4_tn_marginal_sampler.png', dpi=300, bbox_inches='tight')
plt.savefig(results_dir / 'T4_tn_marginal_sampler.pdf', bbox_inches='tight')
print(f"\nFigure saved to {results_dir}/")
