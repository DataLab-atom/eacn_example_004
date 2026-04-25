"""
T3 §D5 DMRG variational anchor on diamond lattice (spec v2).

Uses tenpy DMRG to compute variational ground-state energy bounds
on diamond_lattice_v2 (canonical lex sites + sorted edges + RandomState(42)).

Acts as an independent variational ansatz to compare against:
  - claude7 ED (exact, only feasible for N≤24 with brute-force enum)
  - claude3 NetKet RBM α=4 (variational, alternative ansatz)

For N>24 where ED is infeasible, DMRG chi-sweep gives variational
upper bound on E_GS (for classical Ising H = -sum J_ij sz_i sz_j,
the variational bound is exact at large enough chi for finite N).

Usage:
    python code/T3_dmrg_diamond.py --L 3 --Lv 2 --chi 64 128 256
"""

import json
import time
import argparse
import hashlib
import sys
import numpy as np
from pathlib import Path

repo = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo))
sys.path.insert(0, str(repo / "attacks" / "T3_dwave"))
try:
    from canonical_diamond_v2 import diamond_lattice_v2
except ImportError:
    from canonical_diamond_v2 import diamond_lattice_v2 as diamond_lattice_v2

from tenpy.networks.mps import MPS
from tenpy.networks.site import SpinHalfSite
from tenpy.models.lattice import Chain
from tenpy.models.model import CouplingMPOModel
from tenpy.algorithms.dmrg import run as dmrg_run


class DiamondIsingModel(CouplingMPOModel):
    """Pure classical Ising on a sparse graph mapped onto a 1D MPS chain.

    The diamond geometry is mapped to a 1D MPS via index ordering;
    edges become long-range Ising couplings via add_coupling_term.
    Hamiltonian: H = -sum_(i,j) J_ij Sz_i Sz_j
    """

    def init_sites(self, model_params):
        return SpinHalfSite(conserve=None)

    def init_lattice(self, model_params):
        n_sites = model_params["n_sites"]
        site = self.init_sites(model_params)
        return Chain(L=n_sites, site=site, bc="open", bc_MPS="finite")

    def init_terms(self, model_params):
        edges = model_params["edges"]
        J = model_params["J"]
        for (i, j), Jij in zip(edges, J):
            self.add_coupling_term(-Jij * 4.0, i, j, "Sz", "Sz")


def md5_J(J):
    return hashlib.md5(np.array_str(J).encode()).hexdigest()


def edges_md5(edges):
    return hashlib.md5(str(edges).encode()).hexdigest()


def run_dmrg(L_perp, L_vert, chi_list, max_sweeps=20, J_seed=42):
    n_sites, edges = diamond_lattice_v2(L_perp, L_vert)
    rng = np.random.RandomState(J_seed)
    J = rng.uniform(-1, 1, size=len(edges))

    print(f"DMRG on diamond_lattice_v2 L={L_perp} Lv={L_vert}: N={n_sites}, edges={len(edges)}")
    print(f"  J_md5={md5_J(J)}")
    print(f"  edges_md5={edges_md5(edges)}")
    print()

    results = []
    for chi in chi_list:
        t0 = time.time()
        params = {"n_sites": n_sites, "edges": edges, "J": J}
        model = DiamondIsingModel(params)
        psi = MPS.from_lat_product_state(
            model.lat,
            [["up"]] if n_sites > 0 else [["up"]],
        )
        dmrg_params = {
            "trunc_params": {"chi_max": chi, "svd_min": 1e-10},
            "min_sweeps": 5,
            "max_sweeps": max_sweeps,
            "mixer": True,
        }
        info = dmrg_run(psi, model, dmrg_params)
        E = info["E"]
        runtime = time.time() - t0
        result = {
            "chi": chi,
            "E_DMRG": float(E),
            "E_per_edge": float(E) / len(edges),
            "runtime_s": runtime,
            "max_sweeps": max_sweeps,
            "n_sweeps_actual": info.get("sweep_statistics", {}).get("sweep", [None])[-1],
        }
        results.append(result)
        print(f"  chi={chi:4d}: E={E:.6f}, E/edge={E/len(edges):.6f}, runtime={runtime:.1f}s")

    out = {
        "N": n_sites,
        "L_perp": L_perp,
        "L_vert": L_vert,
        "n_edges": len(edges),
        "edges_md5": edges_md5(edges),
        "J_md5": md5_J(J),
        "spec_version": "v2 (canonical_diamond_v2 by claude3 d9cf7fa)",
        "method": "tenpy DMRG variational",
        "Hamiltonian": "H = -sum_(i,j) J_ij Sz_i Sz_j  (4*Sz factor for spin-1/2 Pauli convention)",
        "chi_sweep": results,
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--L", type=int, default=3)
    ap.add_argument("--Lv", type=int, default=2)
    ap.add_argument("--chi", type=int, nargs="+", default=[64, 128, 256])
    ap.add_argument("--max_sweeps", type=int, default=20)
    ap.add_argument("--seed", type=int, default=42, help="J seed (RandomState)")
    args = ap.parse_args()

    out = run_dmrg(args.L, args.Lv, args.chi, args.max_sweeps, J_seed=args.seed)
    suffix = f"_seed{args.seed}" if args.seed != 42 else ""
    out_path = repo / "results" / "T3" / f"dmrg_diamond_N{out['N']}_v2{suffix}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n-> {out_path}")


if __name__ == "__main__":
    main()
