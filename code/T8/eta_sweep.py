"""
T8: Jiuzhang 3.0 — eta sweep to find "attack zone" boundary
=============================================================
Sweep total transmission eta from 0.30 to 0.90 and compute
required MPS bond dimension D(eta). Identifies the critical
eta above which classical simulation becomes hard.

Author: claude2
Date: 2026-04-25
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import csv

script_dir = Path(__file__).resolve().parent
results_dir = script_dir.parent.parent / "results" / "T8"
results_dir.mkdir(parents=True, exist_ok=True)

N_MODES = 144
SQUEEZING_DB = 1.5
SQUEEZING_R = SQUEEZING_DB / (20 * np.log10(np.e))
n_cut = N_MODES // 2

# Sweep eta
eta_range = np.linspace(0.30, 0.90, 200)
xi_vals = np.tanh(SQUEEZING_R)**2 * eta_range
S_vals = n_cut * xi_vals
D_vals = np.exp(S_vals)
log2_D_vals = np.log2(D_vals)
mem_gb_vals = N_MODES * D_vals**2 * 10 * 16 / 1e9  # d_local=10, complex128

# Practical thresholds
D_laptop = 256       # single laptop
D_gpu = 4096         # single GPU (A100, 80GB)
D_cluster = 1e6      # GPU cluster

# Find critical eta for each threshold
def find_critical_eta(D_threshold):
    S_thresh = np.log(D_threshold)
    xi_thresh = S_thresh / n_cut
    if xi_thresh <= 0:
        return 0.0
    eta_thresh = xi_thresh / np.tanh(SQUEEZING_R)**2
    return min(eta_thresh, 1.0)

eta_laptop = find_critical_eta(D_laptop)
eta_gpu = find_critical_eta(D_gpu)
eta_cluster = find_critical_eta(D_cluster)

print("=" * 60)
print("T8: Jiuzhang 3.0 — eta Sweep Results")
print("=" * 60)
print(f"\nSqueezing: {SQUEEZING_DB} dB (r = {SQUEEZING_R:.4f})")
print(f"Modes: {N_MODES}, cut size: {n_cut}")
print(f"\nCritical eta thresholds:")
print(f"  D < {D_laptop} (laptop):    eta < {eta_laptop:.3f}")
print(f"  D < {D_gpu} (single GPU): eta < {eta_gpu:.3f}")
print(f"  D < {D_cluster:.0e} (cluster):  eta < {eta_cluster:.3f}")
print(f"\nInterpretation:")
print(f"  If JZ 3.0 total eta < {eta_gpu:.2f}: classically simulable on single GPU")
print(f"  If JZ 3.0 total eta < {eta_cluster:.2f}: classically simulable on GPU cluster")
print(f"  If JZ 3.0 total eta > {eta_cluster:.2f}: classical simulation very hard")

# Also sweep squeezing
print(f"\n{'=' * 60}")
print("Sensitivity to squeezing level:")
print(f"{'=' * 60}")
print(f"  {'Squeezing (dB)':>15}  {'eta_crit (GPU)':>15}  {'eta_crit (cluster)':>18}")
for sdb in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]:
    sr = sdb / (20 * np.log10(np.e))
    xi_gpu = np.log(D_gpu) / n_cut
    eta_c = xi_gpu / np.tanh(sr)**2 if np.tanh(sr) > 0 else float('inf')
    xi_cl = np.log(D_cluster) / n_cut
    eta_cl = xi_cl / np.tanh(sr)**2 if np.tanh(sr) > 0 else float('inf')
    print(f"  {sdb:>15.1f}  {min(eta_c, 1.0):>15.3f}  {min(eta_cl, 1.0):>18.3f}")

# Generate figure
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Panel 1: D vs eta
ax = axes[0]
ax.semilogy(eta_range, D_vals, 'b-', linewidth=2)
ax.axhline(y=D_laptop, color='green', linestyle='--', alpha=0.7, label=f'Laptop (D={D_laptop})')
ax.axhline(y=D_gpu, color='orange', linestyle='--', alpha=0.7, label=f'GPU (D={D_gpu})')
ax.axhline(y=D_cluster, color='red', linestyle='--', alpha=0.7, label=f'Cluster (D={D_cluster:.0e})')
ax.axvspan(0.30, eta_gpu, alpha=0.1, color='green', label='Attack zone (GPU)')
ax.axvspan(eta_gpu, eta_cluster, alpha=0.1, color='orange')
ax.set_xlabel('Total Transmission eta')
ax.set_ylabel('Required MPS Bond Dimension D')
ax.set_title(f'(a) D vs eta\n({SQUEEZING_DB} dB squeezing, {N_MODES} modes)')
ax.legend(fontsize=7, loc='upper left')
ax.grid(True, alpha=0.3)
ax.set_ylim(1, 1e20)

# Panel 2: Memory vs eta
ax = axes[1]
ax.semilogy(eta_range, mem_gb_vals, 'r-', linewidth=2)
ax.axhline(y=80, color='orange', linestyle='--', alpha=0.7, label='A100 (80 GB)')
ax.axhline(y=1000, color='red', linestyle='--', alpha=0.7, label='8x A100 (640 GB)')
ax.set_xlabel('Total Transmission eta')
ax.set_ylabel('MPS Memory (GB)')
ax.set_title('(b) Memory Requirement vs eta')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_ylim(1e-6, 1e20)

# Panel 3: Critical eta vs squeezing
ax = axes[2]
sdb_range = np.linspace(0.5, 6.0, 100)
for D_thresh, label, color in [(D_laptop, 'Laptop', 'green'), (D_gpu, 'GPU', 'orange'), (D_cluster, 'Cluster', 'red')]:
    eta_crits = []
    for sdb in sdb_range:
        sr = sdb / (20 * np.log10(np.e))
        xi_t = np.log(D_thresh) / n_cut
        ec = xi_t / np.tanh(sr)**2 if np.tanh(sr) > 0 else 1.0
        eta_crits.append(min(ec, 1.0))
    ax.plot(sdb_range, eta_crits, color=color, linewidth=2, label=f'D={D_thresh:.0e}')
ax.fill_between(sdb_range, 0, [min(xi_t / np.tanh(s / (20*np.log10(np.e)))**2, 1.0)
                                for s in sdb_range
                                for xi_t in [np.log(D_gpu)/n_cut]][:len(sdb_range)],
                alpha=0.1, color='green')
ax.set_xlabel('Squeezing (dB)')
ax.set_ylabel('Critical eta (below = classically easy)')
ax.set_title('(c) Attack Zone Boundary')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 1)

plt.tight_layout()
plt.savefig(results_dir / 'T8_eta_sweep.png', dpi=300, bbox_inches='tight')
plt.savefig(results_dir / 'T8_eta_sweep.pdf', bbox_inches='tight')
print(f"\nFigure saved to {results_dir}/")

# Save CSV
csv_path = results_dir / 'T8_eta_sweep.csv'
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['eta', 'xi', 'S_max', 'D_required', 'log2_D', 'memory_GB'])
    for i in range(0, len(eta_range), 10):
        writer.writerow([f'{eta_range[i]:.3f}', f'{xi_vals[i]:.6f}',
                        f'{S_vals[i]:.4f}', f'{D_vals[i]:.2e}',
                        f'{log2_D_vals[i]:.2f}', f'{mem_gb_vals[i]:.2e}'])
print(f"CSV saved to {csv_path}")
