"""
T6 Attack: Classical Simulation of Zuchongzhi 2.0/2.1 RCS
==========================================================
Target: Wu et al., PRL 127, 180501 (2021) - 60 qubit, 24 cycles
         Zhu et al., Sci. Bull. 67, 240 (2022) - 66 qubit

Method: Tensor network contraction via quimb + cotengra
        Following Pan & Zhang, PRL 129, 090502 (2022)

Agent: claude1 | Branch: claude1
"""

import numpy as np
import quimb.tensor as qtn
import time
import json
import os
from dataclasses import dataclass, asdict

# ── Circuit topology ─────────────────────────────────────────────

def sycamore_like_couplers(nrows, ncols):
    """Generate 2D grid couplers, grouped into ABCD patterns."""
    couplers = []
    for r in range(nrows):
        for c in range(ncols):
            idx = r * ncols + c
            # horizontal
            if c + 1 < ncols:
                couplers.append((idx, idx + 1, 'h', (r + c) % 2))
            # vertical
            if r + 1 < nrows:
                couplers.append((idx, idx + ncols, 'v', (r + c) % 2))
    # Group into 4 patterns: h-even, h-odd, v-even, v-odd
    groups = {i: [] for i in range(4)}
    for q1, q2, direction, parity in couplers:
        if direction == 'h':
            groups[parity].append((q1, q2))
        else:
            groups[2 + parity].append((q1, q2))
    return groups


# ── Build RCS circuit with quimb native API ──────────────────────

def build_rcs_circuit(nrows, ncols, depth, seed=42):
    """
    Build Random Circuit Sampling circuit using quimb's native gates.

    Uses fSim(theta=pi/2, phi=pi/6) as the 2-qubit gate
    and random U3 as single-qubit gates, matching Zuchongzhi design.
    """
    n_qubits = nrows * ncols
    rng = np.random.default_rng(seed)
    circ = qtn.Circuit(n_qubits)
    coupler_groups = sycamore_like_couplers(nrows, ncols)

    for cycle in range(depth):
        # Single-qubit layer: random U3 on every qubit
        for q in range(n_qubits):
            theta = rng.uniform(0, np.pi)
            phi = rng.uniform(0, 2 * np.pi)
            lam = rng.uniform(0, 2 * np.pi)
            circ.u3(theta, phi, lam, q)

        # Two-qubit layer: fSim in ABCD pattern
        pattern = coupler_groups[cycle % 4]
        for q1, q2 in pattern:
            circ.fsim(np.pi / 2, np.pi / 6, q1, q2)

    return circ


# ── Benchmarking ─────────────────────────────────────────────────

@dataclass
class BenchResult:
    n_qubits: int
    nrows: int
    ncols: int
    depth: int
    seed: int
    build_time_s: float
    contract_time_s: float
    amplitude_abs2: float
    expected_uniform: float
    n_tensors: int
    n_indices: int
    notes: str


def benchmark_amplitude(nrows, ncols, depth, seed=42, optimize='greedy'):
    """Benchmark single-amplitude tensor network contraction."""
    n_qubits = nrows * ncols
    print(f"  Building {nrows}x{ncols}={n_qubits}q, d={depth} ...", end=' ')

    t0 = time.time()
    circ = build_rcs_circuit(nrows, ncols, depth, seed)
    t_build = time.time() - t0

    target = '0' * n_qubits

    t1 = time.time()
    amp = circ.amplitude(target, optimize=optimize)
    t_contract = time.time() - t1

    prob = abs(complex(amp)) ** 2
    expected = 2.0 ** (-n_qubits)

    tn = circ.amplitude_tn(target)

    print(f"done in {t_contract:.3f}s  |a|²={prob:.2e}  (uniform={expected:.2e})")

    return BenchResult(
        n_qubits=n_qubits, nrows=nrows, ncols=ncols, depth=depth, seed=seed,
        build_time_s=round(t_build, 4),
        contract_time_s=round(t_contract, 4),
        amplitude_abs2=prob,
        expected_uniform=expected,
        n_tensors=tn.num_tensors,
        n_indices=tn.num_indices,
        notes=f"optimize={optimize}"
    )


def run_scaling_study(max_qubits=36, depths=None):
    """
    Scaling study: measure contraction time vs qubit count and depth.
    Establishes the classical cost curve to challenge ZCZ 2.0.
    """
    if depths is None:
        depths = [8, 12, 16, 20, 24]

    configs = [
        (2, 3),   # 6
        (2, 4),   # 8
        (2, 5),   # 10
        (3, 4),   # 12
        (3, 5),   # 15
        (4, 4),   # 16
        (4, 5),   # 20
        (5, 5),   # 25
        (5, 6),   # 30
        (6, 6),   # 36
        (6, 7),   # 42
        (7, 7),   # 49
        (7, 8),   # 56
        (10, 6),  # 60
    ]

    results = []
    for nrows, ncols in configs:
        n = nrows * ncols
        if n > max_qubits:
            break
        for d in depths:
            print(f"\n--- {nrows}x{ncols}={n}q, depth={d} ---")
            try:
                r = benchmark_amplitude(nrows, ncols, d)
                results.append(asdict(r))
            except Exception as e:
                print(f"  FAILED: {e}")
                results.append({'n_qubits': n, 'depth': d, 'error': str(e)})

    outfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'T6_scaling_results.json')
    with open(outfile, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {outfile}")
    return results


# ── XEB fidelity ─────────────────────────────────────────────────

def compute_xeb(nrows, ncols, depth, n_samples=500, seed=42):
    """
    Compute XEB fidelity for a random circuit.
    F_XEB = 2^n * <p(x)> - 1, averaged over random bitstrings.
    """
    n_qubits = nrows * ncols
    circ = build_rcs_circuit(nrows, ncols, depth, seed)
    rng = np.random.default_rng(seed + 1000)

    probs = []
    for _ in range(n_samples):
        bs = format(rng.integers(0, 2**n_qubits), f'0{n_qubits}b')
        amp = circ.amplitude(bs)
        probs.append(abs(complex(amp))**2)

    fxeb = (2**n_qubits) * np.mean(probs) - 1
    fxeb_std = (2**n_qubits) * np.std(probs) / np.sqrt(n_samples)
    print(f"XEB({nrows}x{ncols}, d={depth}): F_XEB = {fxeb:.4f} +/- {fxeb_std:.4f}")
    return fxeb, fxeb_std


# ── Noise analysis ───────────────────────────────────────────────

def noise_analysis(n_qubits, depth,
                   error_1q=0.0014, error_2q=0.0059, error_ro=0.0226,
                   label=""):
    """
    Analyze whether noise makes ZCZ classically simulable.
    Based on Schuster et al., arXiv:2407.12768 (2024).
    """
    n_1q = n_qubits * depth
    n_2q = (n_qubits * depth) // 2  # approx

    F_1q = (1 - error_1q) ** n_1q
    F_2q = (1 - error_2q) ** n_2q
    F_ro = (1 - error_ro) ** n_qubits
    F_total = F_1q * F_2q * F_ro

    # Sycamore comparison
    F_syc = ((1 - 0.0016)**(53*20) *
             (1 - 0.0062)**(53*10) *
             (1 - 0.038)**53)

    info = {
        'label': label,
        'n_qubits': n_qubits, 'depth': depth,
        'n_1q_gates': n_1q, 'n_2q_gates': n_2q,
        'error_1q': error_1q, 'error_2q': error_2q, 'error_readout': error_ro,
        'F_total': F_total,
        'log2_inv_F': -np.log2(max(F_total, 1e-300)),
        'F_sycamore': F_syc,
        'ratio_vs_sycamore': F_total / F_syc,
    }

    print(f"=== {label or 'Noise Analysis'} ===")
    print(f"  {n_qubits}q x {depth}cyc | 1Q={error_1q:.4f} 2Q={error_2q:.4f} RO={error_ro:.4f}")
    print(f"  F_total = {F_total:.4e}  (log2(1/F) = {info['log2_inv_F']:.1f})")
    print(f"  Sycamore F = {F_syc:.4e}  (ratio = {info['ratio_vs_sycamore']:.3f})")
    print()
    return info


# ── Contraction cost extrapolation ───────────────────────────────

def extrapolate_cost(results):
    """
    Fit exponential scaling T ~ a * 2^(b*n) to estimate
    contraction time for 60 qubits from smaller benchmarks.
    """
    from scipy.optimize import curve_fit

    # Filter valid results at depth=24
    data = [(r['n_qubits'], r['contract_time_s'])
            for r in results
            if isinstance(r.get('contract_time_s'), (int, float))
            and r.get('depth') == 24]

    if len(data) < 3:
        # Fall back to max depth available
        data = [(r['n_qubits'], r['contract_time_s'])
                for r in results
                if isinstance(r.get('contract_time_s'), (int, float))]

    if len(data) < 3:
        print("Not enough data for extrapolation")
        return None

    ns, ts = zip(*data)
    ns, ts = np.array(ns), np.array(ts)

    def model(n, a, b):
        return a * np.exp(b * n)

    try:
        popt, pcov = curve_fit(model, ns, ts, p0=[1e-6, 0.5], maxfev=10000)
        a, b = popt

        t_60 = model(60, a, b)
        t_66 = model(66, a, b)

        print(f"\n=== Extrapolation (T = a * exp(b*n)) ===")
        print(f"  a = {a:.4e}, b = {b:.4f}")
        print(f"  Estimated T(60q): {t_60:.2e} seconds")
        print(f"  Estimated T(66q): {t_66:.2e} seconds")
        print(f"  T(60q) in hours: {t_60/3600:.2e}")
        print(f"  T(60q) in years: {t_60/3600/24/365:.2e}")
        print(f"  Original claim: 4.8e4 years")
        print(f"  Improvement factor: {4.8e4*365*24*3600 / max(t_60, 1e-30):.2e}x")

        return {'a': a, 'b': b, 't_60q': t_60, 't_66q': t_66}
    except Exception as e:
        print(f"Extrapolation failed: {e}")
        return None


# ── Main ─────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='T6 RCS Classical Simulation')
    parser.add_argument('--mode', choices=['bench', 'scale', 'noise', 'xeb', 'all'],
                        default='all')
    parser.add_argument('--max-qubits', type=int, default=25)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()

    outdir = os.path.dirname(os.path.abspath(__file__))

    if args.mode in ('noise', 'all'):
        print("\n" + "="*60)
        print("PHASE 1: Noise Analysis")
        print("="*60)
        n1 = noise_analysis(60, 24, label="Zuchongzhi 2.0")
        n2 = noise_analysis(66, 24, 0.0010, 0.0041, 0.0087, "Zuchongzhi 2.1")
        n3 = noise_analysis(53, 20, 0.0016, 0.0062, 0.038, "Sycamore (broken)")
        with open(os.path.join(outdir, 'T6_noise_analysis.json'), 'w') as f:
            json.dump({'zcz20': n1, 'zcz21': n2, 'sycamore': n3}, f, indent=2)

    if args.mode in ('scale', 'all'):
        print("\n" + "="*60)
        print("PHASE 2: Scaling Study")
        print("="*60)
        results = run_scaling_study(max_qubits=args.max_qubits)

        print("\n" + "="*60)
        print("PHASE 3: Extrapolation")
        print("="*60)
        extrapolate_cost(results)

    if args.mode in ('xeb', 'all'):
        print("\n" + "="*60)
        print("PHASE 4: XEB Fidelity Check")
        print("="*60)
        # Small scale XEB to validate circuit
        compute_xeb(2, 3, 8, n_samples=100)
        compute_xeb(3, 4, 8, n_samples=100)

    if args.mode == 'bench':
        benchmark_amplitude(3, 4, 12, seed=args.seed)
