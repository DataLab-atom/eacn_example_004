"""
T8: HOG Score Benchmark — Classical vs Quantum
================================================
Heavy Output Generation (HOG) score is the primary benchmark
used by GBS experiments to demonstrate quantum advantage.

HOG = fraction of samples in the "heavy" (high-probability) outputs.
- Random/uniform sampler: HOG ≈ 0.5
- Ideal quantum sampler: HOG > 0.5 (biased toward heavy outputs)
- Classical sampler: HOG between 0.5 and ideal

key assumption (verified):
- HOG is the standard benchmark for GBS, used by USTC in all
  Jiuzhang papers (Zhong et al., Science 2020, 2021; Deng 2025)
- Oh et al. arXiv:2306.03709 showed their classical sampler
  OUTPERFORMS quantum device on HOG for JZ 2.0

Author: claude2
Date: 2026-04-25
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import time

script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(script_dir))
results_dir = script_dir.parent.parent / "results" / "T8"

from oh_lossy_gbs_sampler import (
    squeezed_vacuum_cov, apply_loss, random_interferometer,
    apply_interferometer, mean_photon_number
)


def compute_hog_score(samples_total_photons, ideal_total_photons, n_samples_ideal=100000):
    """Compute HOG score.

    HOG = fraction of samples whose total photon count falls in the
    "heavy" region (above median of the ideal distribution).

    For exact HOG we'd need the full output probability distribution,
    but for photon-number-based HOG (used in GBS experiments), we
    compare total photon count distributions.
    """
    # Median of ideal distribution
    median_ideal = np.median(ideal_total_photons)

    # HOG = fraction of samples above median
    hog = np.mean(samples_total_photons >= median_ideal)
    return hog, median_ideal


def generate_samples(r, eta, n_modes, n_samples, seed=42):
    """Generate classical samples from lossy GBS Gaussian baseline."""
    cov = squeezed_vacuum_cov(r, n_modes)
    S = random_interferometer(n_modes, seed=seed)
    cov = apply_interferometer(cov, S)
    cov = apply_loss(cov, eta)

    rng = np.random.default_rng(seed)

    # Batched sampling
    batch_size = min(10000, n_samples)
    all_totals = []
    all_clicks = []

    for start in range(0, n_samples, batch_size):
        bs = min(batch_size, n_samples - start)
        q = rng.multivariate_normal(np.zeros(2 * n_modes), cov, size=bs)
        ph = np.maximum(0, np.round((q[:, 0::2]**2 + q[:, 1::2]**2 - 1) / 2)).astype(int)
        all_totals.extend(np.sum(ph, axis=1))
        all_clicks.extend(np.sum(ph > 0, axis=1))

    return np.array(all_totals), np.array(all_clicks)


# ============================================================
# HOG benchmark for JZ 3.0
# ============================================================
print("=" * 70)
print("T8: HOG Score Benchmark")
print("=" * 70)

N_MODES = 144
N_SAMPLES = 50000

configs = [
    ('JZ 3.0 classical (r=1.5, eta=0.424)', 1.5, 0.424, 42),
    ('JZ 3.0 classical (r=1.2, eta=0.424)', 1.2, 0.424, 42),
    ('JZ 3.0 classical (r=1.6, eta=0.424)', 1.6, 0.424, 42),
    ('JZ 3.0 classical (diff seed)', 1.5, 0.424, 99),
]

# Generate "ideal" reference (high eta, same r)
print("\nGenerating ideal reference (r=1.5, eta=0.95)...")
ideal_totals, ideal_clicks = generate_samples(1.5, 0.95, N_MODES, N_SAMPLES, seed=42)
median_ideal = np.median(ideal_totals)
print(f"  Ideal mean photons: {np.mean(ideal_totals):.1f}")
print(f"  Ideal median: {median_ideal:.0f}")

# Uniform baseline
rng_unif = np.random.default_rng(42)
n_bar_est = np.mean(ideal_totals) / N_MODES
uniform_totals = rng_unif.poisson(n_bar_est, size=N_SAMPLES) * N_MODES // N_MODES
# Actually for uniform, each mode independently Poisson
uniform_totals2 = np.sum(rng_unif.poisson(n_bar_est, size=(N_SAMPLES, N_MODES)), axis=1)
hog_uniform, _ = compute_hog_score(uniform_totals2, ideal_totals)

print(f"\n  Uniform baseline HOG: {hog_uniform:.4f} (expected ~0.5)")

results = []
print(f"\n{'Config':<45} {'HOG':>8} {'Mean_n':>8} {'Median':>8}")
print("-" * 75)

for name, r, eta, seed in configs:
    t0 = time.time()
    totals, clicks = generate_samples(r, eta, N_MODES, N_SAMPLES, seed=seed)
    t_elapsed = time.time() - t0

    hog, med = compute_hog_score(totals, ideal_totals)

    print(f"{name:<45} {hog:>8.4f} {np.mean(totals):>8.1f} {np.median(totals):>8.0f}")

    results.append({
        'name': name, 'r': r, 'eta': eta, 'seed': seed,
        'hog': float(hog), 'mean_photons': float(np.mean(totals)),
        'median_photons': float(np.median(totals)),
        'time_s': t_elapsed,
    })

print(f"\n{'Uniform baseline':<45} {hog_uniform:>8.4f}")
print(f"{'Ideal (eta=0.95)':<45} {'0.5000':>8}")

# ============================================================
# Analysis
# ============================================================
print(f"\n{'=' * 70}")
print("HOG Score Analysis")
print("=" * 70)

best = max(results, key=lambda x: x['hog'])
print(f"""
Best classical HOG: {best['hog']:.4f} ({best['name']})
Uniform baseline:   {hog_uniform:.4f}
Ideal quantum:      0.5000 (by definition of median)

Interpretation:
- HOG > 0.5 means sampler is biased toward heavy outputs (good)
- HOG = 0.5 means random/uniform (no quantum signal)
- Classical HOG {best['hog']:.4f} {'>' if best['hog'] > 0.5 else '<='} 0.5

Note: This is photon-number-based HOG (total photon count),
not the full output-probability-based HOG used in the actual
experiments. The full HOG requires computing Hafnians, which
is the computationally expensive part that Oh et al.'s MPS
method addresses.

For the paper, the key comparison will be:
1. Oh et al. MPS classical HOG vs JZ 3.0 quantum HOG
2. Our Gaussian baseline serves as a LOWER BOUND on classical HOG
3. With MPS chi correction, classical HOG should improve
""")

# ============================================================
# Figure
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# (a) Photon number distributions
ax = axes[0]
bins = np.arange(150, 450, 5)
for res in results[:2]:  # Show r=1.5 and r=1.2
    totals, _ = generate_samples(res['r'], res['eta'], N_MODES, 20000, seed=res['seed'])
    ax.hist(totals, bins=bins, alpha=0.5, density=True, label=f"Classical r={res['r']}")
ax.hist(ideal_totals, bins=bins, alpha=0.3, density=True, label='Ideal (eta=0.95)', color='green')
ax.axvline(x=median_ideal, color='red', linestyle='--', label=f'Ideal median={median_ideal:.0f}')
ax.set_xlabel('Total Photon Number')
ax.set_ylabel('Probability Density')
ax.set_title('(a) Photon Number Distributions')
ax.legend(fontsize=7)

# (b) HOG scores comparison
ax = axes[1]
names_short = ['r=1.2', 'r=1.5', 'r=1.6', 'Uniform']
hogs = [r['hog'] for r in results[:3]] + [hog_uniform]
colors = ['blue', 'blue', 'blue', 'gray']
bars = ax.bar(names_short, hogs, color=colors, alpha=0.7)
ax.axhline(y=0.5, color='red', linestyle='--', label='Random baseline')
ax.set_ylabel('HOG Score')
ax.set_title('(b) HOG Scores: Classical Sampler')
ax.legend()
for bar, val in zip(bars, hogs):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.005, f'{val:.3f}', ha='center', fontsize=9)

plt.suptitle('T8: HOG Score Benchmark — JZ 3.0 Classical Sampling', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(results_dir / 'T8_hog_benchmark.png', dpi=300, bbox_inches='tight')
plt.savefig(results_dir / 'T8_hog_benchmark.pdf', bbox_inches='tight')
print(f"Figure saved to {results_dir}/")

import json
with open(results_dir / 'T8_hog_benchmark.json', 'w') as f:
    json.dump({'results': results, 'hog_uniform': hog_uniform, 'median_ideal': float(median_ideal)}, f, indent=2)
print(f"JSON saved to {results_dir}/")
