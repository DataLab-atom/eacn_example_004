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
    """3D diamond cubic lattice as in claude3 attacks/T3_dwave/fast_tVMC_benchmark.py.

    Unit cell: 2 sublattice (A, B) per (ix, iy, iz).
    A site (ix,iy,iz,0) connects to 4 B sites with offsets:
      (0,0,0), (-1,0,0), (0,-1,0), (0,0,-1).
    nz periodic (mod L_vert), nx/ny open.
    Returns (n_sites, edges) with edges as list of (i, j) with i<j.
    """
    sites = {}

    def add(ix, iy, iz, sub):
        key = (ix, iy, iz, sub)
        if key not in sites:
            sites[key] = len(sites)
        return sites[key]

    edges = set()
    offsets = [(0, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]

    for ix in range(L_perp):
        for iy in range(L_perp):
            for iz in range(L_vert):
                a = add(ix, iy, iz, 0)
                for (dx, dy, dz) in offsets:
                    nx, ny, nz = ix + dx, iy + dy, iz + dz
                    if 0 <= nx < L_perp and 0 <= ny < L_perp:
                        nz_p = nz % L_vert
                        b = add(nx, ny, nz_p, 1)
                        i, j = (a, b) if a < b else (b, a)
                        edges.add((i, j))

    n_sites = len(sites)
    edges_sorted = sorted(edges)
    return n_sites, edges_sorted


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

    out = {
        "N": n,
        "L_perp": args.L,
        "L_vert": args.Lv,
        "n_edges": len(edges),
        "edges": [list(e) for e in edges],
        "J": J.tolist(),
        "J_md5_hash": h,
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

    out_path = Path(__file__).resolve().parent.parent / "results" / "T3" / f"ed_groundtruth_N{n}.json"
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
