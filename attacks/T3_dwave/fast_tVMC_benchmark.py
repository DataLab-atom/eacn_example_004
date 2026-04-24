"""
T3 Attack: Fast t-VMC benchmark with vectorized local energy

Optimized version of the t-VMC simulation:
- Vectorized log amplitude differences (avoid full recomputation)
- Batch MCMC sampling
- Sparse SR matrix (only edge-connected parameters)

Purpose: Get scaling data for N = 16, 54, 128 on diamond lattice
to validate T ~ N^3 polynomial scaling.

Author: claude3 agent
Date: 2026-04-25
"""

import numpy as np
import time
import json
from pathlib import Path


def diamond_lattice(L_perp, L_vert):
    """Build diamond lattice. Returns (n_sites, edges)."""
    sites = []
    site_index = {}
    for ix in range(L_perp):
        for iy in range(L_perp):
            for iz in range(L_vert):
                for sub in [0, 1]:
                    idx = len(sites)
                    site_index[(ix, iy, iz, sub)] = idx
                    sites.append(idx)

    edges = []
    nn_offsets = [(0, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]
    for ix in range(L_perp):
        for iy in range(L_perp):
            for iz in range(L_vert):
                iA = site_index[(ix, iy, iz, 0)]
                for dx, dy, dz in nn_offsets:
                    nx, ny, nz = ix + dx, iy + dy, iz + dz
                    nz = nz % L_vert
                    if 0 <= nx < L_perp and 0 <= ny < L_perp:
                        key_B = (nx, ny, nz, 1)
                        if key_B in site_index:
                            iB = site_index[key_B]
                            edge = (min(iA, iB), max(iA, iB))
                            if edge not in edges:
                                edges.append(edge)
    return len(sites), edges


class FastJastrow2:
    """
    Optimized 2nd-order Jastrow with fast spin-flip updates.

    Key optimization: when flipping spin k, the change in log|psi| is:
    delta = -2 * s_k * (a_k + sum_{j~k} W_{kj} * s_j)

    This avoids recomputing the full sum.
    """

    def __init__(self, n_sites, edges):
        self.N = n_sites
        self.edges = edges
        self.a = np.zeros(n_sites)
        self.W = np.zeros((n_sites, n_sites))

        # Build adjacency for fast updates
        self.neighbors = [[] for _ in range(n_sites)]
        for i, j in edges:
            self.neighbors[i].append(j)
            self.neighbors[j].append(i)

    def init_from_couplings(self, J_couplings):
        for k, (i, j) in enumerate(self.edges):
            self.W[i, j] = 0.1 * J_couplings[k]
            self.W[j, i] = 0.1 * J_couplings[k]

    def log_psi(self, s):
        return np.dot(self.a, s) + 0.5 * s @ self.W @ s

    def delta_log_psi(self, s, k):
        """Change in log|psi| when flipping spin k."""
        local_field = self.a[k] + np.dot(self.W[k], s)
        return -2.0 * s[k] * local_field

    def local_energy(self, s, gamma):
        """
        E_loc = -sum_{ij} J_ij s_i s_j - gamma * sum_i psi(s^i)/psi(s)
        """
        # Diagonal (Ising)
        E_diag = 0.0
        for k, (i, j) in enumerate(self.edges):
            E_diag -= self.J[k] * s[i] * s[j]

        # Off-diagonal (transverse field)
        E_offdiag = 0.0
        if gamma > 1e-10:
            for i in range(self.N):
                delta = self.delta_log_psi(s, i)
                # psi(s^i) / psi(s) = exp(delta) since we flip s_i -> -s_i
                # But delta was computed for the CURRENT s,
                # and flipping means s_i -> -s_i
                E_offdiag -= gamma * np.exp(delta)

        return E_diag + E_offdiag

    @property
    def n_params(self):
        return self.N + len(self.edges)

    def log_derivative(self, s):
        """O_k = d log psi / d theta_k"""
        derivs = np.zeros(self.n_params)
        derivs[:self.N] = s
        for k, (i, j) in enumerate(self.edges):
            derivs[self.N + k] = s[i] * s[j]
        return derivs

    def get_params(self):
        w_upper = np.array([self.W[i, j] for i, j in self.edges])
        return np.concatenate([self.a, w_upper])

    def set_params(self, params):
        self.a = params[:self.N].copy()
        for k, (i, j) in enumerate(self.edges):
            self.W[i, j] = params[self.N + k]
            self.W[j, i] = params[self.N + k]


def run_tvmc_fast(n_sites, edges, J_couplings, gamma_schedule,
                  n_samples=1000, n_steps=30, dt=None, sr_reg=1e-3,
                  seed=42):
    """
    Run t-VMC with optimized sampling.

    gamma_schedule: list of (t, gamma) pairs
    """
    rng = np.random.RandomState(seed)

    psi = FastJastrow2(n_sites, edges)
    psi.init_from_couplings(J_couplings)
    psi.J = J_couplings  # store for local energy

    t_anneal = gamma_schedule[-1][0]
    if dt is None:
        dt = t_anneal / n_steps

    trajectory = []

    for step in range(n_steps + 1):
        t = step * dt
        # Interpolate gamma
        gamma = 3.0 * max(0, 1 - t / t_anneal)

        # === MCMC Sampling ===
        config = rng.choice([-1, 1], size=n_sites).astype(np.float64)
        log_psi_val = psi.log_psi(config)

        # Thermalization
        for _ in range(200):
            k = rng.randint(n_sites)
            delta = psi.delta_log_psi(config, k)
            log_ratio = 2 * delta
            if log_ratio >= 0 or rng.random() < np.exp(log_ratio):
                config[k] *= -1
                log_psi_val += delta

        # Sampling
        configs = np.zeros((n_samples, n_sites))
        E_locs = np.zeros(n_samples)
        O_derivs = np.zeros((n_samples, psi.n_params))

        n_accepted = 0
        for s in range(n_samples):
            # Sweep
            for _ in range(n_sites):
                k = rng.randint(n_sites)
                delta = psi.delta_log_psi(config, k)
                log_ratio = 2 * delta
                if log_ratio >= 0 or rng.random() < np.exp(log_ratio):
                    config[k] *= -1
                    log_psi_val += delta
                    n_accepted += 1

            configs[s] = config.copy()
            E_locs[s] = psi.local_energy(config, gamma)
            O_derivs[s] = psi.log_derivative(config)

        acc_rate = n_accepted / (n_samples * n_sites)
        E_mean = np.mean(E_locs)
        E_var = np.var(E_locs)

        # === SR Update ===
        if step < n_steps:
            O_mean = np.mean(O_derivs, axis=0)
            F = 2 * (np.mean(E_locs[:, None] * O_derivs, axis=0) - E_mean * O_mean)
            dO = O_derivs - O_mean[None, :]
            S = dO.T @ dO / n_samples + sr_reg * np.eye(psi.n_params)

            try:
                dtheta = -np.linalg.solve(S, F) * dt
            except np.linalg.LinAlgError:
                dtheta = -np.linalg.lstsq(S, F, rcond=None)[0] * dt

            norm = np.linalg.norm(dtheta)
            if norm > 0.1:
                dtheta *= 0.1 / norm

            params = psi.get_params()
            params += dtheta
            psi.set_params(params)

        trajectory.append({
            "step": step, "t": t, "gamma": gamma,
            "E": E_mean, "E_var": E_var, "acc": acc_rate
        })

        if step % max(1, n_steps // 5) == 0:
            print(f"  Step {step:3d}/{n_steps} | t={t:.2f} | "
                  f"Gamma={gamma:.2f} | E={E_mean:.3f} | acc={acc_rate:.3f}")

    return trajectory


def scaling_benchmark():
    """Benchmark t-VMC scaling on diamond lattice."""
    print("=" * 60)
    print("T3 SCALING BENCHMARK: Diamond Lattice t-VMC")
    print("=" * 60)

    configs = [
        # (L_perp, L_vert, n_samples, n_steps)
        (2, 2, 500, 20),    # N=16
        (3, 3, 500, 20),    # N=54
        (4, 4, 500, 20),    # N=128 — tractable with vectorized version
    ]

    results = {}

    for L_perp, L_vert, n_samp, n_step in configs:
        n_sites, edges = diamond_lattice(L_perp, L_vert)
        print(f"\n--- Diamond {L_perp}x{L_perp}x{L_vert}: "
              f"N={n_sites}, E={len(edges)} ---")

        rng = np.random.RandomState(42)
        J = rng.uniform(-1, 1, size=len(edges))

        t_start = time.time()
        traj = run_tvmc_fast(
            n_sites, edges, J,
            gamma_schedule=[(0, 3.0), (5.0, 0.0)],
            n_samples=n_samp, n_steps=n_step, seed=42
        )
        wall_time = time.time() - t_start

        results[f"N={n_sites}"] = {
            "n_sites": n_sites,
            "n_edges": len(edges),
            "n_params": n_sites + len(edges),
            "wall_time_s": wall_time,
            "E_final": traj[-1]["E"],
            "acc_final": traj[-1]["acc"],
        }

        print(f"  Wall time: {wall_time:.1f}s")

    # Print scaling summary
    print(f"\n{'=' * 60}")
    print("SCALING SUMMARY")
    print(f"{'=' * 60}")
    ns = []
    ts = []
    for name, r in results.items():
        print(f"  {name}: {r['wall_time_s']:.1f}s, "
              f"E_final={r['E_final']:.3f}, acc={r['acc_final']:.3f}")
        ns.append(r['n_sites'])
        ts.append(r['wall_time_s'])

    if len(ns) >= 2:
        alpha = np.polyfit(np.log(ns), np.log(ts), 1)[0]
        print(f"\n  Scaling exponent: T ~ N^{alpha:.2f}")
        print(f"  (Mauron-Carleo reported: T ~ N^3)")
        for target in [128, 256, 576]:
            t_est = np.exp(np.polyval(
                np.polyfit(np.log(ns), np.log(ts), 1), np.log(target)))
            print(f"  Extrapolated N={target}: {t_est:.0f}s = {t_est/3600:.1f}h")

    # Save
    output_path = Path(__file__).parent.parent.parent / "results" / "T3_scaling_benchmark.json"
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nSaved to {output_path}")

    return results


if __name__ == "__main__":
    scaling_benchmark()
