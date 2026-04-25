"""
Generate paper figures per manuscript/figure_plan.md
====================================================
Fig 1: SPD scaling + hotspot + distance ladder
Fig 2: Depth phase transition + tail decay
Fig 3: (schematic — manual)
Fig 4: Path B+C cost comparison

Author: claude4
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

out = Path('manuscript/figures')
out.mkdir(parents=True, exist_ok=True)

# Colorblind-friendly palette (§B4)
C_BLUE = '#0077BB'
C_RED = '#CC3311'
C_GREEN = '#009988'
C_ORANGE = '#EE7733'

# ============================================================
# Fig 1: SPD scaling
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# (a) Term count vs qubit count
n_adj = [8, 12, 24]
terms_adj = [4007, 3884, 255]
terms_lce = [780, 780, 255]

ax = axes[0]
ax.plot(n_adj, terms_adj, 'o-', color=C_BLUE, label='Adjacent (d=1)', markersize=8)
ax.plot(n_adj, terms_lce, 's-', color=C_RED, label='LC-edge (d=2)', markersize=8)
ax.set_xlabel('Qubit count n', fontsize=11)
ax.set_ylabel('Pauli terms (w≤4)', fontsize=11)
ax.set_yscale('log')
ax.set_title('(a) Term count vs grid size', fontsize=12, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
for i, (n, t) in enumerate(zip(n_adj, terms_adj)):
    ax.annotate(f'{t}', (n, t), textcoords='offset points', xytext=(8, 5), fontsize=8)

# (b) Hot-site fraction
hot_adj = [87.5, 50.0, 21.0]
hot_lce = [75.0, 33.0, 21.0]

ax = axes[1]
ax.plot(n_adj, hot_adj, 'o-', color=C_BLUE, label='Adjacent', markersize=8)
ax.plot(n_adj, hot_lce, 's-', color=C_RED, label='LC-edge', markersize=8)
ax.set_xlabel('Qubit count n', fontsize=11)
ax.set_ylabel('Hot-site fraction (%)', fontsize=11)
ax.set_title('(b) Hotspot concentration', fontsize=12, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 100)

# (c) Distance ladder
dist = [1, 2, 3, 4]
terms_dist = [3884, 780, 778, 780]
labels_dist = ['adjacent', 'LC-edge\n(Google)', 'LC-outer', 'mid-grid']

ax = axes[2]
bars = ax.bar(dist, terms_dist, color=[C_BLUE, C_RED, C_ORANGE, C_GREEN], alpha=0.8)
ax.set_xlabel('M-B Manhattan distance', fontsize=11)
ax.set_ylabel('Pauli terms (w≤4)', fontsize=11)
ax.set_title('(c) Distance ladder (12q)', fontsize=12, fontweight='bold')
ax.set_xticks(dist)
ax.set_xticklabels(labels_dist, fontsize=8)
for bar, t in zip(bars, terms_dist):
    ax.text(bar.get_x() + bar.get_width()/2, t + 50, str(t), ha='center', fontsize=8)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(out / 'fig1_spd_scaling.pdf', bbox_inches='tight')
plt.savefig(out / 'fig1_spd_scaling.png', dpi=600, bbox_inches='tight')
print('Fig 1 saved.')

# ============================================================
# Fig 2: Phase transition
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# (a) Norm vs depth
depths = [4, 6, 8]
norms = [1.000, 0.966, 0.058]

ax = axes[0]
ax.plot(depths, norms, 'o-', color=C_RED, markersize=10, linewidth=2)
ax.axhline(y=0.95, color='gray', linestyle=':', alpha=0.5)
ax.annotate('paper-grade\nthreshold', xy=(7.5, 0.96), fontsize=8, color='gray')
ax.set_xlabel('Circuit depth (per arm)', fontsize=11)
ax.set_ylabel('Operator norm at w≤4', fontsize=11)
ax.set_title('(a) Phase transition in norm', fontsize=12, fontweight='bold')
ax.set_ylim(-0.05, 1.1)
ax.grid(True, alpha=0.3)
for d, n in zip(depths, norms):
    ax.annotate(f'{n:.3f}', (d, n), textcoords='offset points', xytext=(10, -5), fontsize=9)

# (b) Growth factor
growth = [2.4, 24.5]
depth_pairs = ['d4→d6', 'd6→d8']

ax = axes[1]
bars = ax.bar(depth_pairs, growth, color=[C_GREEN, C_RED], alpha=0.8)
ax.set_ylabel('Term growth factor', fontsize=11)
ax.set_title('(b) Growth acceleration', fontsize=12, fontweight='bold')
ax.set_yscale('log')
for bar, g in zip(bars, growth):
    ax.text(bar.get_x() + bar.get_width()/2, g * 1.2, f'{g}x', ha='center', fontsize=10, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

# (c) Path B vs Path C cost at Willow 65q
d_arms = [4, 8, 12, 14]
path_b = [5.6e7, 5.6e7, 2.06e9, 2.3e18]
path_c = [5.6e7, 5.6e7, 5.6e7, 5.6e7]

ax = axes[2]
x = np.arange(len(d_arms))
w = 0.35
ax.bar(x - w/2, path_b, w, label='Path B (fixed-w)', color=C_BLUE, alpha=0.8)
ax.bar(x + w/2, path_c, w, label='Path C (adaptive)', color=C_RED, alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels([f'd={d}' for d in d_arms])
ax.set_ylabel('Cost (operations)', fontsize=11)
ax.set_title('(c) Path B vs C at Willow 65q', fontsize=12, fontweight='bold')
ax.set_yscale('log')
ax.legend(fontsize=9)
ax.annotate('37x', xy=(2, 1e9), fontsize=10, fontweight='bold', color=C_RED)
ax.annotate('INFEASIBLE', xy=(3, 1e17), fontsize=8, color='gray', rotation=45)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(out / 'fig2_phase_transition.pdf', bbox_inches='tight')
plt.savefig(out / 'fig2_phase_transition.png', dpi=600, bbox_inches='tight')
print('Fig 2 saved.')

print(f'\nAll figures saved to {out}/')
