"""
T3 Attack: 4th-order Jastrow integrated with fast t-VMC training.

NEGATIVE RESULT — honest record:
  Naive rank-2 J4 = c * sum_alpha (sum_i v_{i,a} s_i)^4 / (24 N^1.5)
  produces WORSE energies than the 2nd-order baseline at N=8 and N=16
  (verified vs ED ground state). The expansion of m_alpha^4 mixes 1/2/3/4
  body terms, so J4 fights with J1/J2 instead of supplementing them.

  Mauron & Carleo's actual implementation uses NetKet's NeuralJastrow
  + proper 4-body subtraction to isolate the cumulant. Reproducing that
  faithfully needs the NetKet/JAX path, not a naive numpy port.

Status: 4th-order route blocked pending NetKet integration. T3 reclassification
target (🟡 -> 🔴) DEFERRED. README status not changed.

This file:
  1. Implements rank-2 factorized 4-body candidate (current state: insufficient)
  2. Compares 2nd-order vs 4th-order vs ED ground state for N<=18
  3. Documents the negative finding for the team to avoid duplicate effort
"""

import numpy as np
import time
import json
import itertools
from pathlib import Path

from fast_tVMC_benchmark import diamond_lattice


# ============================================================
# Part 1: Fast 4th-order Jastrow with maintained aggregators
# ============================================================

class FastJastrow4:
    """
    psi(s) = exp(J1 + J2 + J4)

    J1 = sum_i a_i s_i
    J2 = sum_{(i,j) in E} W_ij s_i s_j        (only edges, sparse)
    J4 = (1 / (24 N^1.5)) * sum_alpha m_alpha^4
         where m_alpha = sum_i v_{i,alpha} s_i

    State maintained:
      - log_psi (scalar)
      - h_local[i] = a_i + sum_{j in N(i)} W_ij s_j     (length N)
      - m_alpha = v.T @ s                                (length R)

    Flip s_k -> -s_k:
      - delta_J1 = -2 a_k s_k
      - delta_J2 = -2 s_k * sum_{j in N(k)} W_kj s_j = -2 s_k * (h_local[k] - a_k)
      - delta_m_alpha = -2 s_k * v_{k,alpha}
      - delta_J4 = (1/(24 N^1.5)) * sum_alpha [(m_alpha + delta_m)^4 - m_alpha^4]
      - h_local[j] update for j in N(k): h_local[j] -= 2 s_k * W_kj
    """

    def __init__(self, n_sites, edges, rank=2, J4_scale=1.0):
        self.N = n_sites
        self.edges = edges
        self.R = rank
        self.J4_scale = J4_scale  # 4-body amplitude (variational hyper-parameter)

        # Adjacency list and edge index
        self.neighbors = [[] for _ in range(n_sites)]
        self.edge_id = {}
        for k, (i, j) in enumerate(edges):
            self.neighbors[i].append((j, k))
            self.neighbors[j].append((i, k))
            self.edge_id[(i, j)] = k
            self.edge_id[(j, i)] = k

        # Parameters
        self.a = np.zeros(n_sites)
        self.W = np.zeros(len(edges))
        self.v = np.zeros((n_sites, rank))

        # Cached state (set by reset)
        self.s = None
        self.h = None
        self.m = None
        self.log_psi = None

    @property
    def n_params(self):
        return self.N + len(self.edges) + self.N * self.R

    def get_params(self):
        return np.concatenate([self.a, self.W, self.v.ravel()])

    def set_params(self, p):
        idx = 0
        self.a = p[idx:idx + self.N].copy()
        idx += self.N
        self.W = p[idx:idx + len(self.edges)].copy()
        idx += len(self.edges)
        self.v = p[idx:idx + self.N * self.R].reshape(self.N, self.R).copy()

    def reset(self, s):
        """Recompute cached state for configuration s."""
        self.s = s.astype(np.float64).copy()
        # h_local[i] = a_i + sum_{j in N(i)} W_ij s_j
        self.h = self.a.copy()
        for k, (i, j) in enumerate(self.edges):
            self.h[i] += self.W[k] * self.s[j]
            self.h[j] += self.W[k] * self.s[i]
        # m_alpha = sum_i v_{i,alpha} s_i
        self.m = self.v.T @ self.s
        # log_psi = J1 + J2 + J4
        J1 = np.dot(self.a, self.s)
        J2 = 0.0
        for k, (i, j) in enumerate(self.edges):
            J2 += self.W[k] * self.s[i] * self.s[j]
        J4 = self.J4_scale * np.sum(self.m ** 4) / (24.0 * self.N ** 1.5)
        self.log_psi = J1 + J2 + J4

    def delta_log_psi(self, k):
        """Change in log_psi if we flip s_k. State NOT modified."""
        sk = self.s[k]
        # J1: delta = -2 a_k s_k = (a_k * (-sk - sk)) = -2 a_k sk
        d1 = -2.0 * self.a[k] * sk
        # J2: delta = -2 s_k * (h_k - a_k) = -2 sk * sum_{j~k} W_kj s_j
        d2 = -2.0 * sk * (self.h[k] - self.a[k])
        # J4: m -> m + dm where dm = -2 sk v_k
        dm = -2.0 * sk * self.v[k]
        m_new = self.m + dm
        d4 = self.J4_scale * (np.sum(m_new ** 4) - np.sum(self.m ** 4)) / (24.0 * self.N ** 1.5)
        return d1 + d2 + d4

    def flip(self, k):
        """Apply s_k -> -s_k and update state."""
        sk = self.s[k]
        d_log = self.delta_log_psi(k)
        # Update s
        self.s[k] = -sk
        # Update h: h[k] doesn't change (depends on neighbors, not self)
        # h[j] for j in N(k): h[j] -= 2 sk W_kj
        for j, eid in self.neighbors[k]:
            self.h[j] -= 2.0 * sk * self.W[eid]
        # Update m: dm = -2 sk v_k
        self.m += -2.0 * sk * self.v[k]
        # Update log_psi
        self.log_psi += d_log
        return d_log

    def local_energy(self, J_couplings, gamma):
        """
        E_loc(s) = <s|H|psi>/<s|psi>
                = -sum_(i,j)edges J_ij s_i s_j   (diagonal)
                  - gamma * sum_i psi(s^i)/psi(s)  (off-diagonal, spin flip)

        Note: psi(s^i)/psi(s) = exp(delta_log_psi(i))
        """
        # Diagonal Ising part
        E_diag = 0.0
        for k, (i, j) in enumerate(self.edges):
            E_diag -= J_couplings[k] * self.s[i] * self.s[j]
        # Off-diagonal transverse field
        E_offdiag = 0.0
        if gamma > 0:
            for i in range(self.N):
                E_offdiag -= gamma * np.exp(self.delta_log_psi(i))
        return E_diag + E_offdiag

    def log_derivative(self):
        """O_k = d log psi / d theta_k, evaluated at current s."""
        s = self.s
        # d/d a_i = s_i
        d_a = s.copy()
        # d/d W_k = s_i s_j  (k indexes edge (i,j))
        d_W = np.array([s[i] * s[j] for (i, j) in self.edges])
        # d/d v_{i,alpha} = (J4_scale / (24 N^1.5)) * 4 m_alpha^3 * s_i
        coef = self.J4_scale / (6.0 * self.N ** 1.5)
        d_v = coef * np.outer(s, self.m ** 3)  # (N, R)
        return np.concatenate([d_a, d_W, d_v.ravel()])


# ============================================================
# Part 2: t-VMC training loop with FastJastrow4
# ============================================================

def run_tvmc_jastrow4(n_sites, edges, J_couplings, gamma_schedule,
                      rank=2, J4_scale=1.0,
                      n_samples=500, n_steps=20, dt=None,
                      sr_reg=1e-3, seed=42, verbose=True):
    rng = np.random.RandomState(seed)
    psi = FastJastrow4(n_sites, edges, rank=rank, J4_scale=J4_scale)

    # Init W from J (small scale to start)
    psi.W = 0.1 * J_couplings.copy()
    # v init: scale so m_alpha ~ O(1) at start, giving J4 a chance to engage
    # m_alpha = sum_i v_{i,a} s_i has variance N * Var(v) for s ~ ±1
    # For m ~ 1, need Var(v) ~ 1/N, so std(v) ~ 1/sqrt(N)
    psi.v = (1.0 / np.sqrt(n_sites)) * rng.randn(n_sites, rank)

    t_anneal = gamma_schedule[-1][0]
    if dt is None:
        dt = t_anneal / n_steps

    trajectory = []

    for step in range(n_steps + 1):
        t = step * dt
        gamma = 3.0 * max(0, 1 - t / t_anneal)

        # MCMC
        config0 = rng.choice([-1, 1], size=n_sites).astype(np.float64)
        psi.reset(config0)

        # Thermalize
        for _ in range(200):
            k = rng.randint(n_sites)
            d = psi.delta_log_psi(k)
            if 2 * d >= 0 or rng.random() < np.exp(2 * d):
                psi.flip(k)

        # Sample
        E_locs = np.zeros(n_samples)
        O_derivs = np.zeros((n_samples, psi.n_params))
        n_accept = 0
        for s_idx in range(n_samples):
            for _ in range(n_sites):
                k = rng.randint(n_sites)
                d = psi.delta_log_psi(k)
                if 2 * d >= 0 or rng.random() < np.exp(2 * d):
                    psi.flip(k)
                    n_accept += 1
            E_locs[s_idx] = psi.local_energy(J_couplings, gamma)
            O_derivs[s_idx] = psi.log_derivative()

        E_mean = np.mean(E_locs)
        E_var = np.var(E_locs)
        acc = n_accept / (n_samples * n_sites)

        # SR update
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
            psi.set_params(psi.get_params() + dtheta)

        trajectory.append({
            "step": step, "t": t, "gamma": gamma,
            "E": float(E_mean), "E_var": float(E_var), "acc": float(acc),
        })
        if verbose and step % max(1, n_steps // 5) == 0:
            print(f"  Step {step:3d}/{n_steps} | t={t:.2f} | "
                  f"Gamma={gamma:.2f} | E={E_mean:.3f} | acc={acc:.3f}")

    return trajectory, psi


# ============================================================
# Part 3: Exact diagonalization for fidelity benchmarking
# ============================================================

def exact_ground_state(n_sites, edges, J_couplings):
    """Brute-force ground state for small N (<=14). Returns E0, m_z, corr."""
    if n_sites > 18:
        raise ValueError(f"ED not feasible for N={n_sites} > 18")
    best_E = np.inf
    best_s = None
    for bits in range(2 ** n_sites):
        s = np.array([1.0 if (bits >> i) & 1 else -1.0 for i in range(n_sites)])
        E = -sum(J_couplings[k] * s[i] * s[j] for k, (i, j) in enumerate(edges))
        if E < best_E:
            best_E, best_s = E, s
    # Two-point correlator C_ij = <s_i s_j> averaged over edges
    edge_corrs = np.array([best_s[i] * best_s[j] for (i, j) in edges])
    return float(best_E), best_s, edge_corrs


# ============================================================
# Part 4: Driver
# ============================================================

def benchmark_quality():
    print("=" * 60)
    print("T3: 4th-order Jastrow vs ED ground state")
    print("=" * 60)

    repo = Path(__file__).resolve().parent.parent.parent
    out_path = repo / "results" / "T3_jastrow4_quality.json"

    rng = np.random.RandomState(42)
    results = {}

    cases = [
        (2, 1, 200, 30),   # N=8
        (2, 2, 300, 30),   # N=16 (2^16 = 65k, ED still fast)
    ]

    for L_perp, L_vert, n_samp, n_step in cases:
        N, edges = diamond_lattice(L_perp, L_vert)
        if N > 18:
            print(f"  Skipping N={N}: ED too costly")
            continue
        J = rng.uniform(-1, 1, size=len(edges))
        print(f"\n--- Diamond {L_perp}x{L_perp}x{L_vert}: N={N}, E={len(edges)} ---")

        E0, gs, corr_ed = exact_ground_state(N, edges, J)
        print(f"  ED ground state: E0 = {E0:.4f}  (E0/edge = {E0/len(edges):+.3f})")

        # 2nd-order baseline
        psi2 = FastJastrow4(N, edges, rank=2, J4_scale=0.0)
        traj2, _ = run_tvmc_jastrow4(
            N, edges, J, [(0, 3.0), (5.0, 0.0)],
            rank=2, J4_scale=0.0,  # disables 4th-order
            n_samples=n_samp, n_steps=n_step, seed=42, verbose=False)
        E_2nd = traj2[-1]["E"]
        print(f"  2nd-order final E = {E_2nd:.4f}  err = {(E_2nd - E0)/abs(E0):+.2%}")

        # 4th-order
        traj4, _ = run_tvmc_jastrow4(
            N, edges, J, [(0, 3.0), (5.0, 0.0)],
            rank=2, J4_scale=1.0,
            n_samples=n_samp, n_steps=n_step, seed=42, verbose=False)
        E_4th = traj4[-1]["E"]
        print(f"  4th-order final E = {E_4th:.4f}  err = {(E_4th - E0)/abs(E0):+.2%}")

        results[f"N={N}"] = {
            "n_sites": N, "n_edges": len(edges),
            "E_ED": E0,
            "E_2nd_final": E_2nd,
            "E_4th_final": E_4th,
            "rel_err_2nd": (E_2nd - E0) / abs(E0),
            "rel_err_4th": (E_4th - E0) / abs(E0),
        }

    print("\n" + "=" * 60)
    print("QUALITY SUMMARY")
    print("=" * 60)
    for k, r in results.items():
        improvement = abs(r["rel_err_2nd"]) - abs(r["rel_err_4th"])
        print(f"  {k}: 2nd-order err={r['rel_err_2nd']:+.2%}, "
              f"4th-order err={r['rel_err_4th']:+.2%}, "
              f"improvement={improvement:+.2%}")

    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    benchmark_quality()
