"""
T8 Attack: Jiuzhang 3.0 GBS Analysis v2 — with REAL parameters
================================================================
CORRECTED with actual parameters from PRL 134, 090604 (extracted
by claude5, commit a6a926d on branch claude5).

Key corrections:
- Squeezing: r = 1.2–1.6 nepers (10.4–13.9 dB), NOT 1.5 dB
- Total eta: 43% (measured), NOT 57% (estimated)
- Source efficiency: 88.4% (NOT 75%)
- Interferometer: 97% per mode (NOT 85%)

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
n_cut = N_MODES // 2  # max entanglement cut

# REAL parameters from PRL 134, 090604
ETA_TOTAL_REAL = 0.43
R_LOW = 1.2   # nepers (lower bound)
R_HIGH = 1.6  # nepers (upper bound)
R_MID = 1.4   # midpoint estimate

# For comparison: my previous WRONG assumption
R_WRONG = 0.173  # = 1.5 dB in nepers (was the error)

print("=" * 70)
print("T8 v2: Jiuzhang 3.0 — CORRECTED with real parameters")
print("=" * 70)

print(f"\nPrevious (WRONG) parameters:")
print(f"  r = 0.173 nepers (= 1.5 dB)")
print(f"  eta = 57.38%")
print(f"  xi = {np.tanh(R_WRONG)**2 * 0.5738:.6f}")
print(f"  D_required ~ {np.exp(n_cut * np.tanh(R_WRONG)**2 * 0.5738):.1f}")

print(f"\nCORRECTED parameters (from PRL 134, 090604):")
print(f"  r = {R_LOW}–{R_HIGH} nepers (= {R_LOW*8.686:.1f}–{R_HIGH*8.686:.1f} dB)")
print(f"  eta = {ETA_TOTAL_REAL:.0%}")

# Compute for all three r values
for r_val, label in [(R_LOW, "r=1.2 (low)"), (R_MID, "r=1.4 (mid)"), (R_HIGH, "r=1.6 (high)")]:
    xi = np.tanh(r_val)**2 * ETA_TOTAL_REAL
    S_max = n_cut * xi
    D_req = np.exp(S_max)
    mem_gb = N_MODES * D_req**2 * 10 * 16 / 1e9

    print(f"\n  --- {label}, eta={ETA_TOTAL_REAL:.0%} ---")
    print(f"  tanh(r)^2 = {np.tanh(r_val)**2:.6f}")
    print(f"  xi = tanh(r)^2 * eta = {xi:.6f}")
    print(f"  n*xi = {N_MODES * xi:.2f}")
    print(f"  S_max = n_cut * xi = {S_max:.2f}")
    print(f"  D_required = exp(S_max) = {D_req:.2e}")
    print(f"  log2(D) = {np.log2(D_req):.1f}")
    print(f"  Memory = {mem_gb:.2e} GB")

    if D_req < 1e3:
        print(f"  >>> CLASSICALLY EASY (laptop)")
    elif D_req < 1e6:
        print(f"  >>> CLASSICALLY FEASIBLE (single GPU)")
    elif D_req < 1e12:
        print(f"  >>> HARD but possible (GPU cluster)")
    else:
        print(f"  >>> CLASSICALLY INFEASIBLE at this scale")

# ============================================================
# Full r-eta phase diagram
# ============================================================
print(f"\n{'=' * 70}")
print("Phase Diagram: Classical Simulability in (r, eta) space")
print("=" * 70)

r_range = np.linspace(0.1, 2.0, 200)
eta_range_2d = np.linspace(0.1, 1.0, 200)
R_grid, E_grid = np.meshgrid(r_range, eta_range_2d)

xi_grid = np.tanh(R_grid)**2 * E_grid
D_grid = np.exp(n_cut * xi_grid)
log2_D_grid = np.log2(D_grid)

# Find contours
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Panel 1: Phase diagram
ax = axes[0]
levels = [0, 5, 10, 15, 20, 30, 50, 100]
cs = ax.contourf(r_range, eta_range_2d, log2_D_grid, levels=levels,
                  cmap='RdYlGn_r', extend='max')
plt.colorbar(cs, ax=ax, label='log2(D_required)')
ax.contour(r_range, eta_range_2d, log2_D_grid, levels=[10, 20],
           colors='black', linewidths=1, linestyles='--')
# Mark JZ 3.0 operating region
ax.fill_between([R_LOW, R_HIGH], ETA_TOTAL_REAL - 0.05, ETA_TOTAL_REAL + 0.05,
                alpha=0.3, color='blue', label='JZ 3.0 region')
ax.scatter([R_MID], [ETA_TOTAL_REAL], c='blue', s=100, marker='*', zorder=10)
ax.annotate('JZ 3.0', xy=(R_MID + 0.05, ETA_TOTAL_REAL + 0.02), fontsize=10, color='blue')
# Mark wrong assumption
ax.scatter([R_WRONG], [0.5738], c='red', s=80, marker='x', zorder=10)
ax.annotate('v1 (WRONG)', xy=(R_WRONG + 0.02, 0.59), fontsize=8, color='red')
ax.set_xlabel('Squeezing r (nepers)')
ax.set_ylabel('Total Transmission eta')
ax.set_title('(a) Classical Simulability Phase Diagram\nlog2(MPS bond dimension)')
ax.legend(fontsize=8, loc='lower left')

# Panel 2: D vs r at eta=0.43
ax = axes[1]
r_scan = np.linspace(0.1, 2.0, 200)
D_at_043 = np.exp(n_cut * np.tanh(r_scan)**2 * 0.43)
ax.semilogy(r_scan, D_at_043, 'b-', linewidth=2)
ax.axhline(y=256, color='green', linestyle='--', alpha=0.7, label='D=256 (laptop)')
ax.axhline(y=4096, color='orange', linestyle='--', alpha=0.7, label='D=4096 (GPU)')
ax.axhline(y=1e6, color='red', linestyle='--', alpha=0.7, label='D=10^6 (cluster)')
ax.axvspan(R_LOW, R_HIGH, alpha=0.15, color='blue', label='JZ 3.0 r range')
ax.set_xlabel('Squeezing r (nepers)')
ax.set_ylabel('Required MPS Bond Dimension D')
ax.set_title(f'(b) D vs r at eta={ETA_TOTAL_REAL:.0%}')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)
ax.set_ylim(1, 1e30)

# Panel 3: Comparison old vs new
ax = axes[2]
scenarios = ['v1 (WRONG)\nr=0.17, η=57%', 'v2: r=1.2\nη=43%', 'v2: r=1.4\nη=43%', 'v2: r=1.6\nη=43%']
d_values = []
for r_val, eta_val in [(R_WRONG, 0.5738), (R_LOW, 0.43), (R_MID, 0.43), (R_HIGH, 0.43)]:
    xi = np.tanh(r_val)**2 * eta_val
    d_values.append(np.log2(np.exp(n_cut * xi)))

colors = ['red', 'blue', 'blue', 'blue']
bars = ax.bar(scenarios, d_values, color=colors, alpha=0.7)
ax.axhline(y=10, color='green', linestyle='--', alpha=0.7, label='GPU feasible')
ax.axhline(y=20, color='orange', linestyle='--', alpha=0.7, label='Cluster feasible')
ax.set_ylabel('log2(D_required)')
ax.set_title('(c) Bond Dimension: Wrong vs Corrected')
ax.legend(fontsize=8)
for bar, val in zip(bars, d_values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.5, f'{val:.1f}', ha='center', fontsize=9)

plt.suptitle('T8 v2: Jiuzhang 3.0 with REAL parameters from PRL', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(results_dir / 'T8_corrected_analysis.png', dpi=300, bbox_inches='tight')
plt.savefig(results_dir / 'T8_corrected_analysis.pdf', bbox_inches='tight')
print(f"\nFigure saved to {results_dir}/")

# ============================================================
# Summary
# ============================================================
xi_low = np.tanh(R_LOW)**2 * ETA_TOTAL_REAL
xi_high = np.tanh(R_HIGH)**2 * ETA_TOTAL_REAL
D_low = np.exp(n_cut * xi_low)
D_high = np.exp(n_cut * xi_high)

print(f"\n{'=' * 70}")
print("SUMMARY: T8 Corrected Assessment")
print("=" * 70)
print(f"""
ERRATUM: v1 analysis used r=0.173 nepers (1.5 dB). Actual JZ 3.0
uses r=1.2–1.6 nepers (10.4–13.9 dB). This is a 7–9x difference
in the squeezing parameter that FUNDAMENTALLY changes the analysis.

With REAL parameters (r=1.2–1.6, eta=43%):
  - xi = {xi_low:.4f} to {xi_high:.4f}
  - D_required = {D_low:.2e} to {D_high:.2e}
  - log2(D) = {np.log2(D_low):.1f} to {np.log2(D_high):.1f}

REVISED CONCLUSION:
  At r=1.2 (lower bound): log2(D)={np.log2(D_low):.1f}
    → {'Still GPU-feasible' if np.log2(D_low) < 12 else 'Requires cluster' if np.log2(D_low) < 20 else 'Very challenging' if np.log2(D_low) < 30 else 'INFEASIBLE with naive MPS'}

  At r=1.6 (upper bound): log2(D)={np.log2(D_high):.1f}
    → {'Still GPU-feasible' if np.log2(D_high) < 12 else 'Requires cluster' if np.log2(D_high) < 20 else 'Very challenging' if np.log2(D_high) < 30 else 'INFEASIBLE with naive MPS'}

The v1 conclusion ("trivially classical") was WRONG due to
squeezing unit confusion. The corrected analysis shows JZ 3.0
operates in a much harder regime for classical simulation.

HOWEVER: eta=43% (lower than estimated) partially compensates.
The loss is HIGHER than assumed, which helps the classical attack.

NEXT STEPS:
  a) Explore whether Oh et al. method works in high-squeezing regime
  b) Consider alternative classical methods beyond naive MPS
  c) Investigate whether the 43% efficiency creates enough loss
     to enable classical simulation despite high squeezing
""")

# Save CSV
csv_path = results_dir / 'T8_corrected_results.csv'
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['r_nepers', 'r_dB', 'eta', 'xi', 'n_xi', 'D_required', 'log2_D'])
    for r_val in [R_LOW, R_MID, R_HIGH]:
        xi = np.tanh(r_val)**2 * ETA_TOTAL_REAL
        D = np.exp(n_cut * xi)
        writer.writerow([f'{r_val:.2f}', f'{r_val*8.686:.1f}', f'{ETA_TOTAL_REAL:.2f}',
                        f'{xi:.6f}', f'{N_MODES*xi:.2f}', f'{D:.2e}', f'{np.log2(D):.1f}'])
print(f"CSV saved to {csv_path}")
