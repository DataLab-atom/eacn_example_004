"""
T6 Attack: Classical Runtime Re-estimation for Zuchongzhi 2.0/2.1 RCS

Target: Wu et al., PRL 127, 180501 (2021)
  - 60 qubits, 24 cycles, claimed classical runtime: 4.8 x 10^4 years

Attack strategy:
  Use post-2021 advances in tensor network contraction to re-estimate
  the classical simulation cost. Key improvements since original claim:
  1. Pan & Zhang PRL 2022: slicing + contraction order optimization
  2. Liu et al. PRL 2024: multi-amplitude contraction
  3. GPU hardware improvements (A100 -> H100 -> B200)
  4. Morvan et al. Nature 2024: phase transition analysis

This script:
  (a) Models the tensor network for a 2D grid RCS circuit
  (b) Estimates contraction cost using cotengra optimizer
  (c) Compares with original claim
  (d) Performs small-scale validation

Author: claude3 agent
Date: 2026-04-25
"""

import numpy as np
import time
import json
from pathlib import Path

# ============================================================
# Part 1: Circuit and Tensor Network Parameters
# ============================================================

# Zuchongzhi 2.0 parameters (from Wu et al. PRL 127, 180501)
N_QUBITS = 60          # number of qubits
N_CYCLES = 24          # circuit depth (cycles)
GATE_SET = {
    "single": ["sqrt_X", "sqrt_Y", "sqrt_W"],  # random single-qubit gates
    "two": "fSim(theta=pi/6, phi=pi/6)"        # two-qubit gate
}
# fSim gate bond dimension when decomposed as MPO
FSIM_BOND_DIM = 4      # 4x4 unitary -> bond dim 4

# Grid topology: ~6x10 grid with some qubits removed
GRID_ROWS = 6
GRID_COLS = 10
# Actual qubit count after removing some: 60

# Key fidelity parameters from original paper
FIDELITY_1Q = 0.9990   # single-qubit gate fidelity
FIDELITY_2Q = 0.9938   # two-qubit gate fidelity
FIDELITY_RO = 0.9909   # readout fidelity

# ============================================================
# Part 2: Classical Simulation Cost Model
# ============================================================

def estimate_tn_contraction_cost(n_qubits, n_cycles, grid_rows, grid_cols,
                                  bond_dim=4, method="pan_zhang_2022"):
    """
    Estimate the computational cost of tensor network contraction
    for RCS on a 2D grid.

    The contraction cost is dominated by:
    - Treewidth of the line graph of the tensor network
    - Number of sliced indices (reduces treewidth at cost of more contractions)
    - Bond dimension of each tensor

    Returns estimated FLOP count and wall-clock time on various hardware.
    """

    # Number of two-qubit gates per cycle (approximately half the edges)
    n_edges = (grid_rows - 1) * grid_cols + grid_rows * (grid_cols - 1)
    gates_per_cycle = n_edges // 2  # alternating ABCD pattern
    total_2q_gates = gates_per_cycle * n_cycles

    # Total number of tensors in the network
    n_tensors = n_qubits + total_2q_gates + n_qubits  # init + gates + final

    # Treewidth estimation for 2D grid circuit
    # For a m x n grid with depth d, treewidth ~ min(m, n) * d / 2
    # After slicing, effective treewidth is reduced
    treewidth_raw = min(grid_rows, grid_cols) * n_cycles // 2

    if method == "original_2021":
        # Original estimate: no slicing optimization, basic contraction
        n_slices = 0
        treewidth_eff = treewidth_raw
        flops_per_amplitude = bond_dim ** treewidth_eff
        n_amplitudes = 1e6  # ~10^6 samples for XEB
        total_flops = flops_per_amplitude * n_amplitudes

    elif method == "pan_zhang_2022":
        # Pan-Zhang improvement: optimal slicing + contraction order
        # Key insight: slice O(k) indices to reduce treewidth by k
        # Cost: multiply by 2^k (number of slice configurations)
        # Optimal k minimizes: 2^k * bond_dim^(treewidth - k)

        # Optimal number of slices
        k_opt = int(treewidth_raw - np.log2(treewidth_raw) / np.log2(bond_dim))
        k_opt = min(k_opt, treewidth_raw - 5)  # don't slice too much
        k_opt = max(k_opt, 10)

        treewidth_eff = treewidth_raw - k_opt
        slice_overhead = 2 ** k_opt

        flops_per_amplitude = bond_dim ** treewidth_eff * slice_overhead
        # Multi-amplitude: can compute many amplitudes in one contraction
        n_amplitudes = 1e6
        # Amortization factor from shared contraction paths
        amortization = max(1, n_amplitudes / (2 ** 10))
        total_flops = flops_per_amplitude * n_amplitudes / amortization

    elif method == "liu_2024_multi_amplitude":
        # Liu et al. 2024: multi-amplitude tensor contraction
        # Further improvement: compute 2^s amplitudes simultaneously
        # by not summing over s output indices

        k_opt = int(treewidth_raw * 0.6)  # aggressive slicing
        s = min(10, n_qubits - treewidth_raw + k_opt)  # multi-amplitude parameter

        treewidth_eff = treewidth_raw - k_opt
        slice_overhead = 2 ** k_opt
        n_amplitudes_per_contraction = 2 ** s

        flops_per_batch = bond_dim ** treewidth_eff * slice_overhead
        n_batches = max(1, 1e6 / n_amplitudes_per_contraction)
        total_flops = flops_per_batch * n_batches

    else:
        raise ValueError(f"Unknown method: {method}")

    return {
        "method": method,
        "n_qubits": n_qubits,
        "n_cycles": n_cycles,
        "treewidth_raw": treewidth_raw,
        "treewidth_effective": treewidth_eff,
        "n_slices": k_opt if method != "original_2021" else 0,
        "total_flops": float(total_flops),
        "log10_flops": np.log10(float(total_flops)),
    }


def estimate_wall_time(total_flops, hardware="gpu_cluster"):
    """
    Convert FLOP count to estimated wall-clock time on various hardware.

    Hardware FLOPS rates (FP32, sustained):
    - Single A100:     ~19.5 TFLOPS = 1.95e13
    - Single H100:     ~51 TFLOPS  = 5.1e13 (tensor core mixed: ~990 TFLOPS)
    - Frontier (full): ~1.194 EFLOPS = 1.194e18 (FP64)
    - 512 H100 cluster: ~2.6e16
    - Single B200:     ~72 TFLOPS = 7.2e13 (FP32)
    """

    hardware_flops = {
        "single_a100": 1.95e13,
        "single_h100": 5.1e13,
        "single_b200": 7.2e13,
        "h100_cluster_512": 2.6e16,
        "frontier": 1.194e18,       # peak FP64
        "frontier_sustained": 5e17,  # ~40% efficiency
    }

    results = {}
    for name, flops_rate in hardware_flops.items():
        seconds = total_flops / flops_rate
        results[name] = {
            "seconds": seconds,
            "hours": seconds / 3600,
            "days": seconds / 86400,
            "years": seconds / (365.25 * 86400),
        }

    return results


# ============================================================
# Part 3: Small-scale Validation with quimb
# ============================================================

def small_scale_rcs_validation(n_qubits_small=12, n_cycles_small=8):
    """
    Validate our tensor network contraction approach on a small circuit.
    Uses quimb + cotengra for actual contraction.
    """
    try:
        import quimb.tensor as qtn
        import cotengra as ctg
    except ImportError:
        return {"error": "quimb/cotengra not installed"}

    print(f"\n=== Small-scale validation: {n_qubits_small} qubits, {n_cycles_small} cycles ===")

    # Create a random circuit on a small 2D grid
    rows = int(np.sqrt(n_qubits_small))
    cols = n_qubits_small // rows
    actual_qubits = rows * cols

    print(f"Grid: {rows} x {cols} = {actual_qubits} qubits")

    # Build random unitary circuit using quimb
    circ = qtn.Circuit(actual_qubits)

    np.random.seed(42)  # reproducibility

    for cycle in range(n_cycles_small):
        # Random single-qubit gates
        for q in range(actual_qubits):
            gate_type = np.random.choice(["RX", "RY", "RZ"])
            angle = np.random.uniform(0, 2 * np.pi)
            if gate_type == "RX":
                circ.rx(angle, q)
            elif gate_type == "RY":
                circ.ry(angle, q)
            else:
                circ.rz(angle, q)

        # Two-qubit gates (nearest-neighbor on grid)
        if cycle % 2 == 0:
            # Horizontal bonds
            for r in range(rows):
                for c in range(0, cols - 1, 2):
                    q1 = r * cols + c
                    q2 = r * cols + c + 1
                    circ.cx(q1, q2)
        else:
            # Vertical bonds
            for r in range(0, rows - 1, 2):
                for c in range(cols):
                    q1 = r * cols + c
                    q2 = (r + 1) * cols + c
                    circ.cx(q1, q2)

    # Method 1: Exact statevector simulation
    t0 = time.time()
    psi_exact = circ.psi.to_dense()
    t_exact = time.time() - t0

    # Sample a specific bitstring amplitude
    bitstring = "0" * actual_qubits
    amp_exact = psi_exact.ravel()[0]
    prob_exact = abs(amp_exact) ** 2

    # Method 2: Tensor network contraction
    t0 = time.time()
    tn = circ.psi

    # Use cotengra to find optimal contraction path
    opt = ctg.HyperOptimizer(
        max_repeats=32,
        max_time=30,
        progbar=False,
    )

    # Contract for the all-zero bitstring amplitude
    amp_tn_raw = tn.contract(optimize=opt)
    t_tn = time.time() - t0

    # Extract scalar from Tensor object if needed
    if hasattr(amp_tn_raw, 'data'):
        amp_tn = complex(amp_tn_raw.data.ravel()[0])
    elif hasattr(amp_tn_raw, '__complex__'):
        amp_tn = complex(amp_tn_raw)
    else:
        amp_tn = complex(np.array(amp_tn_raw).ravel()[0])

    # Contraction info
    tree = tn.contraction_tree(optimize=opt)

    results = {
        "n_qubits": actual_qubits,
        "n_cycles": n_cycles_small,
        "grid": f"{rows}x{cols}",
        "exact_amplitude_real": float(np.real(amp_exact)),
        "exact_amplitude_imag": float(np.imag(amp_exact)),
        "exact_probability": float(prob_exact),
        "tn_amplitude": amp_tn,
        "time_exact_s": t_exact,
        "time_tn_s": t_tn,
        "contraction_cost_log10": float(np.log10(tree.total_flops())),
        "contraction_width": int(tree.contraction_width()),
        "agreement": bool(np.allclose(amp_exact, amp_tn, atol=1e-10)),
    }

    print(f"Exact amplitude: {amp_exact:.6e}")
    print(f"TN amplitude:    {amp_tn:.6e}")
    print(f"Agreement: {results['agreement']}")
    print(f"Exact time: {t_exact:.3f}s, TN time: {t_tn:.3f}s")
    print(f"Contraction cost: 10^{results['contraction_cost_log10']:.1f} FLOPS")
    print(f"Contraction width: {results['contraction_width']}")

    return results


# ============================================================
# Part 4: Runtime Comparison Analysis
# ============================================================

def run_full_analysis():
    """
    Main analysis: compare classical runtime estimates across methods and hardware.
    """
    print("=" * 70)
    print("T6 ATTACK: Classical Runtime Re-estimation for Zuchongzhi 2.0/2.1")
    print("=" * 70)

    methods = ["original_2021", "pan_zhang_2022", "liu_2024_multi_amplitude"]

    all_results = {}

    for method in methods:
        print(f"\n--- Method: {method} ---")
        cost = estimate_tn_contraction_cost(
            N_QUBITS, N_CYCLES, GRID_ROWS, GRID_COLS,
            bond_dim=FSIM_BOND_DIM, method=method
        )
        wall_times = estimate_wall_time(cost["total_flops"])

        print(f"  Treewidth (raw):       {cost['treewidth_raw']}")
        print(f"  Treewidth (effective): {cost['treewidth_effective']}")
        print(f"  Sliced indices:        {cost['n_slices']}")
        print(f"  Total FLOPS:           10^{cost['log10_flops']:.1f}")
        print(f"  Wall time (Frontier):  {wall_times['frontier_sustained']['hours']:.2e} hours")
        print(f"  Wall time (512xH100):  {wall_times['h100_cluster_512']['hours']:.2e} hours")
        print(f"  Wall time (1xH100):    {wall_times['single_h100']['hours']:.2e} hours")

        all_results[method] = {
            "cost": cost,
            "wall_times": wall_times,
        }

    # Compare with original claim
    print("\n" + "=" * 70)
    print("COMPARISON WITH ORIGINAL CLAIM")
    print("=" * 70)
    original_years = 4.8e4
    print(f"Original claim: {original_years:.1e} years on classical supercomputer")

    for method in ["pan_zhang_2022", "liu_2024_multi_amplitude"]:
        frontier_years = all_results[method]["wall_times"]["frontier_sustained"]["years"]
        speedup = original_years / frontier_years if frontier_years > 0 else float('inf')
        print(f"\n{method}:")
        print(f"  Estimated Frontier time: {frontier_years:.2e} years")
        print(f"  Speedup vs original claim: {speedup:.2e}x")
        if frontier_years < 1:
            print(f"  >> FEASIBLE: {frontier_years * 365.25:.1f} days on Frontier")
            print(f"  >> This BREAKS the quantum advantage claim!")
        elif frontier_years < 10:
            print(f"  >> MARGINAL: could be feasible with more resources")
        else:
            print(f"  >> Still classically hard at this scale")

    # Also estimate for the Zuchongzhi 2.1 variant
    print("\n" + "=" * 70)
    print("ZUCHONGZHI 2.1 VARIANT (Zhu et al., Sci. Bull. 67, 240)")
    print("=" * 70)
    # ZCZ 2.1: 60 qubits, 24 cycles, slightly different circuit
    # Similar parameters, similar analysis applies
    print("Same qubit count and depth -> same cost analysis applies.")
    print("ZCZ 2.1 used verified (not just linear) XEB, but the")
    print("classical simulation cost is dominated by the same TN contraction.")

    return all_results


# ============================================================
# Part 5: Noise-Aware Analysis (Morvan Phase Transition)
# ============================================================

def noise_phase_analysis():
    """
    Apply Morvan et al. Nature 2024 phase transition framework
    to determine if ZCZ 2.0 parameters are in the 'hard' phase.

    Key insight: RCS has a noise-driven phase transition.
    Below a critical noise rate, classical simulation is easy.
    """
    print("\n" + "=" * 70)
    print("PHASE TRANSITION ANALYSIS (Morvan et al. 2024)")
    print("=" * 70)

    # Per-gate error rates
    e1 = 1 - FIDELITY_1Q  # single-qubit error: 0.001
    e2 = 1 - FIDELITY_2Q  # two-qubit error: 0.0062
    e_ro = 1 - FIDELITY_RO  # readout error: 0.0091

    # Total circuit error rate (approximate)
    # Number of gates
    n_1q_gates = N_QUBITS * N_CYCLES
    n_2q_gates_per_cycle = ((GRID_ROWS - 1) * GRID_COLS + GRID_ROWS * (GRID_COLS - 1)) // 2
    n_2q_gates = n_2q_gates_per_cycle * N_CYCLES

    # Total fidelity (multiplicative noise model)
    log_fidelity = (n_1q_gates * np.log(FIDELITY_1Q) +
                    n_2q_gates * np.log(FIDELITY_2Q) +
                    N_QUBITS * np.log(FIDELITY_RO))
    total_fidelity = np.exp(log_fidelity)

    # XEB fidelity (linear cross-entropy benchmark)
    # F_XEB ~ total_fidelity for depolarizing noise
    f_xeb = total_fidelity

    # Critical XEB for phase transition
    # From Morvan et al.: transition occurs around F_XEB ~ 1/2^n for n qubits
    # More precisely: the easy phase is when noise is high enough that
    # the output distribution is close to uniform
    f_xeb_critical = 2 ** (-N_QUBITS)  # trivial lower bound

    # Effective noise parameter: epsilon = 1 - F_XEB^(1/(n*d))
    if f_xeb > 0:
        eps_eff = 1 - f_xeb ** (1 / (N_QUBITS * N_CYCLES))
    else:
        eps_eff = 1.0

    print(f"Circuit parameters:")
    print(f"  Single-qubit gates: {n_1q_gates}")
    print(f"  Two-qubit gates:    {n_2q_gates}")
    print(f"  Total fidelity:     {total_fidelity:.6e}")
    print(f"  XEB fidelity:       {f_xeb:.6e}")
    print(f"  Effective noise/gate: {eps_eff:.4f}")
    print(f"")
    print(f"Phase transition analysis:")
    print(f"  F_XEB trivial bound: {f_xeb_critical:.2e}")
    print(f"  F_XEB / trivial:     {f_xeb / f_xeb_critical:.2e}")

    if f_xeb < 1e-3:
        print(f"  >> LOW FIDELITY regime: noise may push into classically easy phase")
        print(f"  >> Pauli path methods (Schuster et al. 2024) may be polynomial")
    else:
        print(f"  >> Moderate fidelity: noise analysis inconclusive")

    return {
        "n_1q_gates": n_1q_gates,
        "n_2q_gates": n_2q_gates,
        "total_fidelity": float(total_fidelity),
        "f_xeb": float(f_xeb),
        "eps_effective": float(eps_eff),
        "phase": "low_fidelity" if f_xeb < 1e-3 else "moderate",
    }


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    # 1. Full cost analysis
    results = run_full_analysis()

    # 2. Noise/phase analysis
    noise_results = noise_phase_analysis()

    # 3. Small-scale validation
    validation = small_scale_rcs_validation(n_qubits_small=12, n_cycles_small=8)

    # 4. Save all results
    output = {
        "target": "T6: Zuchongzhi 2.0/2.1",
        "paper": "Wu et al., PRL 127, 180501 (2021)",
        "original_claim_years": 4.8e4,
        "analysis_date": "2026-04-25",
        "agent": "claude3",
        "cost_analysis": {k: v["cost"] for k, v in results.items()},
        "wall_times": {k: v["wall_times"] for k, v in results.items()},
        "noise_analysis": noise_results,
        "small_scale_validation": {
            k: v for k, v in validation.items()
            if k != "tn_amplitude"  # complex not JSON serializable
        } if "error" not in validation else validation,
    }

    output_path = Path(__file__).parent.parent.parent / "results" / "T6_runtime_analysis.json"
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\nResults saved to {output_path}")
