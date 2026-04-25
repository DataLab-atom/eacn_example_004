"""
T3 §D5 cross-validate support: ED ground truth on diamond lattice
=================================================================

Provides exact ground state energy + correlators for claude3's
fast t-VMC fidelity calibration. Pure classical Ising H = -sum J_ij sz_i sz_j
(transverse field Gamma=0), so brute-force state enumeration suffices.

Usage:
    python code/T3_diamond_ed.py --N 8 --L 2 --Lv 1 --seed 42

Output: results/T3/ed_groundtruth_N{N}.json with schema:
    {N, L_perp, L_vert, n_edges, edges, J_md5_hash, J,
     E_GS_total, E_per_edge, GS_state_bitstring,
     correlators_NN, correlators_long_range,
     runtime_s, code_commit_hash}
"""

import numpy as np
import hashlib
import json
import time
import argparse
import subprocess
from pathlib import Path


def diamond_lattice(L_perp, L_vert):
    """Spec v2 (canonical, claude3+claude7 §D5 freeze, commit d9cf7fa).

    Site indexing: lexicographic over (ix, iy, iz, sub) — purely
    deterministic, no dependency on edge-loop ordering.
    Edge ordering: sorted ascending.

    Replaces the v1 dynamic add() implementation that produced a
    different site->idx mapping than claude3's reference.
    """
    site_index = {}
    for ix in range(L_perp):
        for iy in range(L_perp):
            for iz in range(L_vert):
                for sub in [0, 1]:
                    site_index[(ix, iy, iz, sub)] = len(site_index)

    offsets = [(0, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]
    edges = set()
    for ix in range(L_perp):
        for iy in range(L_perp):
            for iz in range(L_vert):
                a = site_index[(ix, iy, iz, 0)]
                for dx, dy, dz in offsets:
                    nx, ny = ix + dx, iy + dy
                    nz = (iz + dz) % L_vert
                    if 0 <= nx < L_perp and 0 <= ny < L_perp:
                        b = site_index[(nx, ny, nz, 1)]
                        edges.add((min(a, b), max(a, b)))

    edges_sorted = sorted(edges)
    return len(site_index), edges_sorted


def edges_md5(edges):
    return hashlib.md5(str(edges).encode()).hexdigest()


def gen_J(seed, n_edges):
    rng = np.random.RandomState(seed)
    return rng.uniform(-1, 1, size=n_edges)


def md5_J(J):
    return hashlib.md5(np.array_str(J).encode()).hexdigest()


def enumerate_ising_groundstate(N, edges, J):
    """Brute-force ground state for H = -sum_e J_e sz_i sz_j, sz in {+1,-1}.

    Vectorized over all 2^N states using numpy bit ops. Memory: O(2^N * 4 bytes).
    Feasible for N<=24 in 8GB; N=32 needs batching (not done here).
    """
    assert N <= 28, f"N={N} too large for in-memory enumeration; use batched version"
    n_states = 1 << N
    states = np.arange(n_states, dtype=np.int64)

    # spin[i] = 2 * bit_i - 1 in {+1, -1}
    spins = np.zeros((n_states, N), dtype=np.int8)
    for i in range(N):
        spins[:, i] = 2 * ((states >> i) & 1) - 1

    energies = np.zeros(n_states, dtype=np.float64)
    for (i, j), Jij in zip(edges, J):
        energies -= Jij * spins[:, i].astype(np.float64) * spins[:, j].astype(np.float64)

    gs_idx = int(np.argmin(energies))
    E_GS = float(energies[gs_idx])
    gs_spins = spins[gs_idx].astype(int).tolist()
    gs_bitstring = "".join("1" if s == 1 else "0" for s in gs_spins)

    correlators = {}
    for (i, j) in edges:
        correlators[f"({i},{j})"] = float(spins[gs_idx, i] * spins[gs_idx, j])

    long_range = []
    if N >= 4:
        for (i, j) in [(0, N // 2), (0, N - 1)]:
            if i < N and j < N:
                long_range.append({
                    "pair": [i, j],
                    "value": float(spins[gs_idx, i] * spins[gs_idx, j]),
                })

    return {
        "E_GS_total": E_GS,
        "GS_bitstring": gs_bitstring,
        "GS_spins": gs_spins,
        "correlators_NN": correlators,
        "correlators_long_range": long_range,
    }


def get_git_commit():
    try:
        out = subprocess.check_output(
            ["git", "-C", str(Path(__file__).resolve().parent.parent),
             "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        )
        return out.decode().strip()
    except Exception:
        return "unknown"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=8, help="expected n_sites (for sanity check)")
    ap.add_argument("--L", type=int, default=2, help="L_perp")
    ap.add_argument("--Lv", type=int, default=1, help="L_vert")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    n, edges = diamond_lattice(args.L, args.Lv)
    assert n == args.N, f"diamond_lattice({args.L},{args.Lv}) gave N={n}, expected {args.N}"
    J = gen_J(args.seed, len(edges))
    h = md5_J(J)

    t0 = time.time()
    result = enumerate_ising_groundstate(n, edges, J)
    runtime = time.time() - t0

    e_md5 = edges_md5(edges)
    out = {
        "N": n,
        "L_perp": args.L,
        "L_vert": args.Lv,
        "n_edges": len(edges),
        "edges": [list(e) for e in edges],
        "J": J.tolist(),
        "J_md5_hash": h,
        "edges_md5_hash": e_md5,
        "spec_version": "v2 (canonical_diamond_v2 by claude3 d9cf7fa)",
        "E_GS_total": result["E_GS_total"],
        "E_per_edge": result["E_GS_total"] / len(edges),
        "GS_bitstring": result["GS_bitstring"],
        "GS_spins": result["GS_spins"],
        "correlators_NN": result["correlators_NN"],
        "correlators_long_range": result["correlators_long_range"],
        "runtime_s": runtime,
        "code_commit_hash": get_git_commit(),
        "method": "brute_force_enumeration",
        "Hamiltonian": "H = -sum_(i,j) J_ij sz_i sz_j  (pure classical Ising, Gamma=0)",
    }

    out_path = Path(__file__).resolve().parent.parent / "results" / "T3" / f"ed_groundtruth_N{n}_v2.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)

    print(f"N={n}, edges={len(edges)}, J_md5={h}")
    print(f"  E_GS = {result['E_GS_total']:.6f}")
    print(f"  E_per_edge = {result['E_GS_total']/len(edges):.6f}")
    print(f"  GS = {result['GS_bitstring']}")
    print(f"  runtime = {runtime:.3f}s")
    print(f"  -> {out_path}")


if __name__ == "__main__":
    main()
