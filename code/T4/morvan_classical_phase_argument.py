"""
T4: Morvan Classical Phase Argument for ZCZ 3.0
=================================================
Synthesize the phase transition argument:
ZCZ 3.0 operates at lambda/lc = 1.55, deep in the classical phase.

This is the CORE argument for the T4 attack after withdrawing
the statistical undetectability claim.

Framework: Morvan et al., Nature 634, 328 (2024)
Cross-validated: claude1 commit 7886de1 (independent calculation)

Author: claude2
Date: 2026-04-25
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import json

script_dir = Path(__file__).resolve().parent
results_dir = script_dir.parent.parent / "results" / "T4"
results_dir.mkdir(parents=True, exist_ok=True)

# ============================================================
# All RCS systems in the Morvan phase diagram
# ============================================================
# Data from claude1 commit 7886de1 + my noise analysis + paper data
systems = {
    'Sycamore (BROKEN)': {
        'n': 53, 'd': 20, 'e_2q': 0.0062, 'n_2q': 520,
        'lambda': 6.57, 'lc': 6.5, 'ratio': 1.01,
        'broken': True, 'year': 2019,
    },
    'ZCZ 2.0': {
        'n': 56, 'd': 20, 'e_2q': 0.0041, 'n_2q': 560,
        'lambda': 4.59, 'lc': 6.5, 'ratio': 0.71,
        'broken': False, 'year': 2021,
    },
    'ZCZ 2.1': {
        'n': 60, 'd': 24, 'e_2q': 0.0038, 'n_2q': 720,
        'lambda': 5.47, 'lc': 6.5, 'ratio': 0.84,
        'broken': False, 'year': 2021,
    },
    'ZCZ 3.0': {
        'n': 83, 'd': 32, 'e_2q': 0.00375, 'n_2q': 1312,
        'lambda': 10.09, 'lc': 6.5, 'ratio': 1.55,
        'broken': False, 'year': 2025,  # TARGET
    },
    'Willow RCS': {
        'n': 67, 'd': 32, 'e_2q': 0.003, 'n_2q': 1056,
        'lambda': 6.43, 'lc': 6.5, 'ratio': 0.99,
        'broken': False, 'year': 2024,
    },
}

print("=" * 70)
print("T4: Morvan Phase Transition Argument")
print("=" * 70)

print(f"\n{'System':<20} {'n':>4} {'d':>4} {'e_2q':>7} {'lambda':>8} {'λ/λc':>7} {'Phase':<20}")
print("-" * 75)
for name, s in systems.items():
    phase = "CLASSICAL" if s['ratio'] > 1 else "quantum" if s['ratio'] < 0.9 else "BOUNDARY"
    marker = " ← TARGET" if name == 'ZCZ 3.0' else " (BROKEN)" if s['broken'] else ""
    print(f"{name:<20} {s['n']:>4} {s['d']:>4} {s['e_2q']:>7.4f} {s['lambda']:>8.2f} {s['ratio']:>7.2f} {phase:<20}{marker}")

# ============================================================
# The argument
# ============================================================
print(f"""
{'=' * 70}
THE ARGUMENT
{'=' * 70}

PREMISE 1: Morvan et al. (Nature 634, 2024) established that Random
Circuit Sampling exhibits a noise-driven phase transition. Below a
critical noise level (lambda < lambda_c), quantum advantage is possible.
Above it (lambda > lambda_c), the output distribution becomes efficiently
classically simulable.

PREMISE 2: The critical point lambda_c ≈ 6.5 for 2D superconducting
circuits (approximate; depends on topology).

PREMISE 3: Google Sycamore operated at lambda/lambda_c = 1.01 — right
at the boundary. It was subsequently classically simulated by Pan-Zhang
(PRL 129, 2022) in seconds.

PREMISE 4: ZCZ 3.0 operates at lambda/lambda_c = 1.55 — DEEP inside
the classical phase. It is 55% beyond the phase boundary.

CONCLUSION: By the Morvan framework, ZCZ 3.0's output distribution
should be efficiently classically simulable. The fact that it has not
yet been explicitly simulated reflects the lack of a dedicated effort,
not fundamental hardness.

SUPPORTING EVIDENCE:
1. Sycamore (lambda/lc = 1.01) was broken → ZCZ 3.0 (lambda/lc = 1.55)
   should be even easier to break
2. ZCZ 3.0's gate fidelities are COMPARABLE to Sycamore's
   (2Q: 99.625% vs 99.38%), but the much larger circuit volume
   (83q×32c vs 53q×20c) pushes it deeper into the noisy phase
3. The estimated XEB fidelity (0.026%) indicates the output is
   99.97% uniform noise — a very low bar for classical methods

WHAT'S STILL NEEDED:
A constructive classical simulation achieving F_XEB ≈ 0.026% on
the ZCZ 3.0 circuit, running in feasible time on available hardware.
This is the gap between "the theory says it should work" and
"we actually did it".
""")

# ============================================================
# Phase diagram figure
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Panel 1: Lambda/Lambda_c for all systems
ax = axes[0]
names = list(systems.keys())
ratios = [systems[n]['ratio'] for n in names]
colors = ['red' if systems[n]['broken'] else 'orange' if n == 'ZCZ 3.0' else 'blue' for n in names]
bars = ax.barh(names, ratios, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
ax.axvline(x=1.0, color='black', linewidth=2, linestyle='-', label='Phase boundary (λ/λc = 1)')
ax.fill_betweenx([-0.5, len(names)-0.5], 1.0, 2.0, alpha=0.1, color='green', label='Classical phase')
ax.fill_betweenx([-0.5, len(names)-0.5], 0, 1.0, alpha=0.1, color='red', label='Quantum phase')
ax.set_xlabel('λ / λc (noise parameter / critical value)')
ax.set_title('(a) RCS Systems in Morvan Phase Diagram')
ax.legend(fontsize=8, loc='lower right')
ax.set_xlim(0, 2.0)
for bar, val, name in zip(bars, ratios, names):
    ax.text(val + 0.02, bar.get_y() + bar.get_height()/2, f'{val:.2f}',
            va='center', fontsize=9, fontweight='bold')

# Panel 2: Historical trajectory
ax = axes[1]
years = [systems[n]['year'] for n in names]
volumes = [systems[n]['n'] * systems[n]['d'] for n in names]
ax.scatter(years, ratios, s=[v/3 for v in volumes], c=colors, alpha=0.7,
           edgecolors='black', linewidth=0.5, zorder=5)
ax.axhline(y=1.0, color='black', linewidth=2, linestyle='-')
ax.fill_between([2018, 2026], 1.0, 2.0, alpha=0.1, color='green', label='Classical phase')
ax.fill_between([2018, 2026], 0, 1.0, alpha=0.1, color='red', label='Quantum phase')
for name, yr, r in zip(names, years, ratios):
    offset = 0.04 if name != 'ZCZ 2.1' else -0.06
    ax.annotate(name.replace(' (BROKEN)', ''), xy=(yr, r),
                xytext=(yr + 0.2, r + offset), fontsize=7)
ax.set_xlabel('Year')
ax.set_ylabel('λ / λc')
ax.set_title('(b) Historical: Larger Circuits → Deeper in Classical Phase')
ax.legend(fontsize=8)
ax.set_xlim(2018.5, 2026)
ax.set_ylim(0, 2.0)

plt.suptitle('T4: ZCZ 3.0 in the Morvan Phase Transition Framework',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(results_dir / 'T4_morvan_phase_argument.png', dpi=300, bbox_inches='tight')
plt.savefig(results_dir / 'T4_morvan_phase_argument.pdf', bbox_inches='tight')
print(f"Figure saved to {results_dir}/")

# Save JSON
output = {
    'systems': {k: {kk: vv for kk, vv in v.items()} for k, v in systems.items()},
    'lambda_critical': 6.5,
    'zcz30_ratio': 1.55,
    'conclusion': 'ZCZ 3.0 deep in classical phase (lambda/lc=1.55)',
}
with open(results_dir / 'T4_morvan_phase_argument.json', 'w') as f:
    json.dump(output, f, indent=2)
print(f"JSON saved to {results_dir}/")
