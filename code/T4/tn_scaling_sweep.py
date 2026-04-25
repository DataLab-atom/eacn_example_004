"""
T4: TN Scaling Sweep — chi=64/128, N=9/12/16/20/25
====================================================
Test whether approximate TN (MPS) can match noisy quantum XEB
as system size increases. This is Morvan-independent.

Experiment design (locked by claude7 REV):
- Fixed chi: 64, 128
- Sweep N: 9 (3x3), 12 (3x4), 16 (4x4), 20 (4x5), 25 (5x5)
- Fixed depth = 8 (keep circuits tractable)
- ZCZ 3.0 noise: e_2q = 0.00375

Key question: does XEB_classical / XEB_quantum increase with N?

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
import sys

script_dir = Path(__file__).resolve().parent
results_dir = script_dir.parent.parent / "results" / "T4"
results_dir.mkdir(parents=True, exist_ok=True)

DEPTH = 8
E_2Q = 0.00375
E_1Q = 0.001
E_RO = 0.0087
SEED = 42

configs = [
    (3, 3, "9q"),
    (3, 4, "12q"),
    (4, 4, "16q"),
    (4, 5, "20q"),
]
# 25q (5x5) may be too slow for exact reference — try if time permits

chi_values = [4, 16, 64]  # start smaller to check feasibility


def build_exact(n_rows, n_cols, depth, seed):
    rng = np.random.default_rng(seed)
    n = n_rows * n_cols
    circ = qtn.Circuit(n)
    edges = []
    for r in range(n_rows):
        for c in range(n_cols):
            q = r * n_cols + c
            if c + 1 < n_cols: edges.append((q, q + 1))
            if r + 1 < n_rows: edges.append((q, q + n_cols))
    patterns = [[], [], [], []]
    for i, (q1, q2) in enumerate(edges):
        patterns[i % 4].append((q1, q2))
    for cycle in range(depth):
        for q in range(n):
            a = rng.uniform(0, 2*np.pi, 3)
            circ.apply_gate('RZ', a[0], q)
            circ.apply_gate('RX', a[1], q)
            circ.apply_gate('RZ', a[2], q)
        for q1, q2 in patterns[cycle % 4]:
            circ.apply_gate('CZ', q1, q2)
    return circ


def build_mps(n_rows, n_cols, depth, chi, seed):
    rng = np.random.default_rng(seed)
    n = n_rows * n_cols
    circ = qtn.Circuit(n, psi0=qtn.MPS_computational_state('0' * n))
    edges = []
    for r in range(n_rows):
        for c in range(n_cols):
            q = r * n_cols + c
            if c + 1 < n_cols: edges.append((q, q + 1))
            if r + 1 < n_rows: edges.append((q, q + n_cols))
    patterns = [[], [], [], []]
    for i, (q1, q2) in enumerate(edges):
        patterns[i % 4].append((q1, q2))
    for cycle in range(depth):
        for q in range(n):
            a = rng.uniform(0, 2*np.pi, 3)
            circ.apply_gate('RZ', a[0], q, max_bond=chi, cutoff=1e-12)
            circ.apply_gate('RX', a[1], q, max_bond=chi, cutoff=1e-12)
            circ.apply_gate('RZ', a[2], q, max_bond=chi, cutoff=1e-12)
        for q1, q2 in patterns[cycle % 4]:
            circ.apply_gate('CZ', q1, q2, max_bond=chi, cutoff=1e-12)
    return circ


def get_probs(circ):
    psi = circ.psi.contract()
    p = np.abs(psi.data.ravel())**2
    return p / p.sum()


def noisy(p_ideal, n, gates):
    n2 = sum(1 for g in gates if g.label == 'CZ')
    n1 = len(gates) - n2
    F = (1-E_1Q)**n1 * (1-E_2Q)**n2 * (1-E_RO)**n
    D = len(p_ideal)
    return F * p_ideal + (1-F) / D * np.ones(D), F


def xeb(p_ideal, p_sample):
    return len(p_ideal) * np.sum(p_ideal * p_sample) - 1


print("=" * 70)
print("T4: TN Scaling Sweep")
print(f"Depth={DEPTH}, e_2q={E_2Q}, chi={chi_values}")
print("=" * 70)

results = []

for nr, nc, label in configs:
    n = nr * nc
    print(f"\n--- {label} ({nr}x{nc}, depth={DEPTH}) ---")

    # Exact reference
    t0 = time.time()
    circ_ex = build_exact(nr, nc, DEPTH, SEED)
    p_ideal = get_probs(circ_ex)
    p_noisy, F_total = noisy(p_ideal, n, circ_ex.gates)
    xeb_q = xeb(p_ideal, p_noisy)
    t_exact = time.time() - t0
    print(f"  Exact: F={F_total:.4f}, XEB_q={xeb_q:.4f} ({t_exact:.1f}s)")

    for chi in chi_values:
        t0 = time.time()
        circ_mps = build_mps(nr, nc, DEPTH, chi, SEED)
        p_approx = get_probs(circ_mps)
        xeb_c = xeb(p_ideal, p_approx)
        t_mps = time.time() - t0

        ratio = xeb_c / xeb_q if xeb_q > 0 else 0
        print(f"  chi={chi:>4}: XEB_c={xeb_c:.4f}, ratio={ratio:.4f}, time={t_mps:.1f}s")

        results.append({
            'config': label, 'n': n, 'nr': nr, 'nc': nc,
            'depth': DEPTH, 'chi': chi,
            'F_total': float(F_total),
            'xeb_quantum': float(xeb_q),
            'xeb_classical': float(xeb_c),
            'ratio': float(ratio),
            'time_exact_s': float(t_exact),
            'time_mps_s': float(t_mps),
        })

# ============================================================
# Analysis
# ============================================================
print(f"\n{'=' * 70}")
print("Scaling Analysis: XEB ratio vs system size")
print("=" * 70)

for chi in chi_values:
    cr = [r for r in results if r['chi'] == chi]
    if cr:
        ns = [r['n'] for r in cr]
        rats = [r['ratio'] for r in cr]
        print(f"  chi={chi}: N={ns} -> ratio={[f'{r:.4f}' for r in rats]}")
        trend = "INCREASING" if len(rats) > 1 and rats[-1] > rats[0] else "DECREASING or FLAT"
        print(f"    Trend: {trend}")

# ============================================================
# Figure
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# (a) XEB ratio vs N
ax = axes[0]
for chi in chi_values:
    cr = [r for r in results if r['chi'] == chi]
    if cr:
        ax.plot([r['n'] for r in cr], [r['ratio'] for r in cr], 'o-', label=f'chi={chi}')
ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Classical = Quantum')
ax.set_xlabel('Number of Qubits N')
ax.set_ylabel('XEB_classical / XEB_quantum')
ax.set_title('(a) XEB Ratio vs System Size')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# (b) Wall-clock vs N
ax = axes[1]
for chi in chi_values:
    cr = [r for r in results if r['chi'] == chi]
    if cr:
        ax.semilogy([r['n'] for r in cr], [r['time_mps_s'] for r in cr], 's-', label=f'MPS chi={chi}')
cr_all = [r for r in results if r['chi'] == chi_values[0]]
if cr_all:
    ax.semilogy([r['n'] for r in cr_all], [r['time_exact_s'] for r in cr_all], 'ro-', label='Exact')
ax.set_xlabel('Number of Qubits N')
ax.set_ylabel('Wall-clock Time (s)')
ax.set_title('(b) Computation Time vs N')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# (c) XEB values
ax = axes[2]
cr0 = [r for r in results if r['chi'] == chi_values[0]]
if cr0:
    ax.plot([r['n'] for r in cr0], [r['xeb_quantum'] for r in cr0], 'ro-', label='Quantum (noisy)')
for chi in chi_values:
    cr = [r for r in results if r['chi'] == chi]
    if cr:
        ax.plot([r['n'] for r in cr], [r['xeb_classical'] for r in cr], 's-', label=f'Classical chi={chi}')
ax.set_xlabel('Number of Qubits N')
ax.set_ylabel('XEB Fidelity')
ax.set_title('(c) Absolute XEB vs N')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

plt.suptitle(f'TN Scaling Sweep (depth={DEPTH}, e_2q={E_2Q})', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(results_dir / 'T4_tn_scaling_sweep.png', dpi=300, bbox_inches='tight')
plt.savefig(results_dir / 'T4_tn_scaling_sweep.pdf', bbox_inches='tight')
print(f"\nFigure saved to {results_dir}/")

with open(results_dir / 'T4_tn_scaling_sweep.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"JSON saved to {results_dir}/")
