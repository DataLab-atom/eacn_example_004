"""
T3 §D5 spec freeze v2: canonical diamond lattice for cross-validation.

Resolves the topology mismatch found between claude3's
fast_tVMC_benchmark.diamond_lattice and claude7's code/T3_diamond_ed.diamond_lattice.

Both legacy implementations describe the same physical lattice
(3D diamond cubic, A/B sublattice, periodic in z, open in x/y, coord=4)
but assigned different integer indices to the same physical sites,
producing different J -> edge mappings for the same J vector.

Spec v2 is the SINGLE authoritative source for both ED (claude7) and
t-VMC / NetKet (claude3) until §D5 work concludes.

Authoritative choices:
  1. Site indexing: lexicographic over (ix, iy, iz, sub)
     0 = (0,0,0,0)=A
     1 = (0,0,0,1)=B
     2 = (0,0,1,0)=A
     3 = (0,0,1,1)=B
     ...
     This is purely deterministic and depends only on (L_perp, L_vert).
  2. Edge generation: A->4xB offsets [(0,0,0),(-1,0,0),(0,-1,0),(0,0,-1)],
     periodic in z (mod L_vert), open in x/y.
  3. Edge canonical form: each edge stored as (min, max).
  4. Edge ordering: sorted ascending — sorted(edges).
  5. J vector: np.random.RandomState(42).uniform(-1, 1, size=len(edges))
     where len(edges) is from step (4).
  6. Hamiltonian: H = -sum_(i,j) in sorted_edges  J_idx s_i s_j

Returns hashes (edges_md5, J_md5) for cross-validation.
"""

import numpy as np
import hashlib


def diamond_lattice_v2(L_perp: int, L_vert: int):
    """Authoritative diamond lattice for §D5.

    Returns:
        n_sites: int
        edges: list[tuple[int,int]] — sorted, each (i,j) with i<j
    """
    # 1. Pre-build site indexing (lexicographic)
    site_index = {}
    for ix in range(L_perp):
        for iy in range(L_perp):
            for iz in range(L_vert):
                for sub in [0, 1]:
                    site_index[(ix, iy, iz, sub)] = len(site_index)

    # 2. Generate edges
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

    # 3. Canonical sorting
    edges_sorted = sorted(edges)
    return len(site_index), edges_sorted


def J_for(L_perp: int, L_vert: int, seed: int = 42):
    """Canonical J vector for the spec v2 lattice."""
    _, edges = diamond_lattice_v2(L_perp, L_vert)
    rng = np.random.RandomState(seed)
    return rng.uniform(-1, 1, size=len(edges))


def hashes(L_perp: int, L_vert: int, seed: int = 42):
    """Cross-validation hashes."""
    N, edges = diamond_lattice_v2(L_perp, L_vert)
    J = J_for(L_perp, L_vert, seed=seed)
    edges_md5 = hashlib.md5(str(edges).encode()).hexdigest()
    J_md5 = hashlib.md5(np.array_str(J).encode()).hexdigest()
    return {
        "N": N, "L_perp": L_perp, "L_vert": L_vert,
        "n_edges": len(edges), "edges_md5": edges_md5, "J_md5": J_md5,
    }


def main():
    print("Spec v2 hash table:")
    print("| N | L | Lv | edges | edges_md5 | J_md5 |")
    print("|---|---|----|-------|-----------|-------|")
    for L, Lv in [(2, 1), (2, 2), (3, 1), (2, 3), (3, 2), (2, 4), (3, 3), (3, 4), (4, 4)]:
        h = hashes(L, Lv)
        print(f"| {h['N']:>3} | {L} | {Lv} | {h['n_edges']:>3} | {h['edges_md5']} | {h['J_md5']} |")


if __name__ == "__main__":
    main()
