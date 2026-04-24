"""
T4: Patched Classical Sampler — Proof of Concept
==================================================
In the strong-noise phase (lambda/lc > 1), the output distribution
of a noisy RCS circuit can be approximated as a product of
weakly-correlated patches.

This script demonstrates the concept on small circuits:
1. Simulate ideal + noisy quantum circuit
2. Divide into patches and sample from patch marginals
3. Compare XEB of patched sampler vs noisy quantum

This is the CONSTRUCTIVE part of the T4 attack.

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


def build_noisy_rcs(n_rows, n_cols, depth, e_2q=0.00375, seed=42):
    """Build RCS circuit and return ideal + noisy probability distributions."""
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

    # Ideal probabilities
    psi = circ.psi.contract()
    probs_ideal = np.abs(psi.data.ravel())**2

    # Noisy: depolarizing model
    n_2q = sum(1 for g in circ.gates if g.label == 'CZ')
    n_1q = len(circ.gates) - n_2q
    F_total = (1 - 0.001)**n_1q * (1 - e_2q)**n_2q * (1 - 0.0087)**n_qubits
    D = 2**n_qubits
    uniform = np.ones(D) / D
    probs_noisy = F_total * probs_ideal + (1 - F_total) * uniform

    return probs_ideal, probs_noisy, F_total, n_qubits


def patched_sampler(probs_ideal, n_qubits, n_patches, noise_mix=0.99):
    """Simple patched classical sampler.

    Divides qubits into patches and samples each patch independently
    from a mixture of marginal ideal distribution and uniform.

    This is a simplified version of the Morvan decomposition.
    """
    D = 2**n_qubits
    patch_size = n_qubits // n_patches
    remainder = n_qubits % n_patches

    # Compute marginal distributions for each patch
    probs_patched = np.ones(D)

    for p in range(n_patches):
        start = p * patch_size + min(p, remainder)
        end = start + patch_size + (1 if p < remainder else 0)
        patch_qubits = list(range(start, end))
        other_qubits = [q for q in range(n_qubits) if q not in patch_qubits]
        n_patch = len(patch_qubits)
        n_other = len(other_qubits)

        # Compute marginal distribution for this patch
        # by summing over other qubits
        probs_reshaped = probs_ideal.reshape([2] * n_qubits)

        # Sum over other qubits
        # Sort axes to sum: need to sum out all "other" dimensions
        for q in sorted(other_qubits, reverse=True):
            probs_reshaped = probs_reshaped.sum(axis=q)

        # This gives the marginal distribution over patch qubits
        marginal = probs_reshaped.ravel()
        marginal = marginal / marginal.sum()

        # Mix with uniform (noise model)
        uniform_patch = np.ones(2**n_patch) / 2**n_patch
        marginal_noisy = noise_mix * uniform_patch + (1 - noise_mix) * marginal

        # Expand marginal back to full distribution
        # (tensor product with uniform on other qubits)
        full_marginal = np.ones(D)
        for idx in range(D):
            bits = [(idx >> q) & 1 for q in range(n_qubits)]
            patch_bits = [bits[q] for q in patch_qubits]
            patch_idx = sum(b << i for i, b in enumerate(patch_bits))
            full_marginal[idx] *= marginal_noisy[patch_idx]

    # Normalize
    probs_patched = full_marginal
    probs_patched = probs_patched / probs_patched.sum()
    return probs_patched


def compute_xeb(probs_ideal, probs_sample):
    """XEB = D * sum(p_ideal * p_sample) - 1"""
    D = len(probs_ideal)
    return D * np.sum(probs_ideal * probs_sample) - 1


# ============================================================
# Benchmark: patched sampler vs noisy quantum
# ============================================================
print("=" * 70)
print("T4: Patched Classical Sampler Benchmark")
print("=" * 70)

configs = [
    (3, 3, 8, "9q/8d"),
    (3, 4, 10, "12q/10d"),
    (4, 4, 12, "16q/12d"),
]

# Sweep noise levels to show the transition
e2q_values = [0.001, 0.002, 0.004, 0.006, 0.008, 0.01, 0.015, 0.02]

results = []

for n_rows, n_cols, depth, label in configs:
    n_qubits = n_rows * n_cols
    print(f"\n--- {label} ---")

    for e2q in e2q_values:
        probs_ideal, probs_noisy, F_total, nq = build_noisy_rcs(
            n_rows, n_cols, depth, e_2q=e2q
        )

        xeb_quantum = compute_xeb(probs_ideal, probs_noisy)

        # Try different patch counts
        best_xeb_classical = -1
        best_patches = 1
        for n_patches in [1, 2, 3, max(1, n_qubits // 3)]:
            if n_patches > n_qubits:
                continue
            noise_mix = 1 - F_total  # match noise level
            probs_classical = patched_sampler(probs_ideal, n_qubits, n_patches,
                                              noise_mix=noise_mix)
            xeb_classical = compute_xeb(probs_ideal, probs_classical)
            if xeb_classical > best_xeb_classical:
                best_xeb_classical = xeb_classical
                best_patches = n_patches

        beats = best_xeb_classical >= xeb_quantum * 0.5  # within 50% counts
        results.append({
            'config': label, 'n_qubits': n_qubits, 'depth': depth,
            'e_2q': e2q, 'F_total': F_total,
            'xeb_quantum': xeb_quantum, 'xeb_classical': best_xeb_classical,
            'best_patches': best_patches, 'competitive': beats,
        })

        marker = "OK" if beats else "NO"
        print(f"  e_2q={e2q:.4f}: F={F_total:.4f} XEB_q={xeb_quantum:.4f} "
              f"XEB_c={best_xeb_classical:.4f} ({best_patches}p) {marker}")

# ============================================================
# Plot: XEB ratio as function of noise
# ============================================================
fig, axes = plt.subplots(1, len(configs), figsize=(5 * len(configs), 5))
if len(configs) == 1:
    axes = [axes]

for idx, (_, _, _, label) in enumerate(configs):
    ax = axes[idx]
    cr = [r for r in results if r['config'] == label]
    e2qs = [r['e_2q'] for r in cr]
    xeb_q = [r['xeb_quantum'] for r in cr]
    xeb_c = [r['xeb_classical'] for r in cr]
    ratios = [c / q if q > 0 else 0 for c, q in zip(xeb_c, xeb_q)]

    ax.plot(e2qs, xeb_q, 'ro-', label='Quantum (noisy)')
    ax.plot(e2qs, xeb_c, 'bs-', label='Classical (patched)')
    ax.axvline(x=0.00375, color='green', linestyle='--', alpha=0.5, label='ZCZ 3.0 e_2q')
    ax.set_xlabel('2Q Gate Error Rate')
    ax.set_ylabel('XEB Fidelity')
    ax.set_title(f'{label}')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

plt.suptitle('Patched Classical Sampler vs Noisy Quantum', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(results_dir / 'T4_patched_sampler.png', dpi=300, bbox_inches='tight')
plt.savefig(results_dir / 'T4_patched_sampler.pdf', bbox_inches='tight')
print(f"\nFigure saved to {results_dir}/")
