"""
T3 Attack: Classical simulation of D-Wave "Beyond-Classical" quantum annealing
via time-dependent Variational Monte Carlo (t-VMC) + Jastrow-Feenberg ansatz.

Target: King et al., Science 388, 199 (2025)
  - 2D, 3D, infinite-dimensional spin glass quench dynamics
  - D-Wave Advantage2 prototype, up to ~3200 qubits
  - Claimed: MPS, PEPS, NQS all fail to match in reasonable time

Attack strategy (extending Mauron & Carleo, EPFL 2025, arXiv:2503.08247):
  - t-VMC + Jastrow-Feenberg wavefunctions on 3D diamond lattice
  - Mauron-Carleo achieved: 4 GPU, 3 days, 128 qubit, error <7%
  - Our goal: extend to 256+ qubits, reduce error, cover more topologies

Key physics:
  - Transverse-field Ising model (TFIM) quench dynamics
  - H(t) = -sum_ij J_ij sigma_z^i sigma_z^j - Gamma(t) sum_i sigma_x^i
  - Gamma(t): annealing schedule from large Gamma to 0
  - Observable: <sigma_z^i sigma_z^j> at end of anneal

Methods implemented here:
  1. Jastrow-Feenberg variational wavefunction
  2. Time-dependent VMC (TDVP / McLachlan variational principle)
  3. Spin glass disorder averaging
  4. Scaling analysis from small to large systems

Author: claude3 agent
Date: 2026-04-25
"""

import numpy as np
from scipy.linalg import expm
from scipy.sparse import csr_matrix, kron, eye
import time
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

# ============================================================
# Part 1: Lattice Geometry
# ============================================================

@dataclass
class Lattice:
    """Defines a lattice geometry for spin glass simulation."""
    name: str
    n_sites: int
    edges: List[Tuple[int, int]]
    dimension: int
    coordination: float  # average coordination number

    @staticmethod
    def cubic_3d(L: int) -> "Lattice":
        """3D cubic lattice with periodic boundary conditions."""
        n = L ** 3
        edges = []
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    i = x * L * L + y * L + z
                    # +x neighbor
                    j = ((x + 1) % L) * L * L + y * L + z
                    edges.append((i, j))
                    # +y neighbor
                    j = x * L * L + ((y + 1) % L) * L + z
                    edges.append((i, j))
                    # +z neighbor
                    j = x * L * L + y * L + ((z + 1) % L)
                    edges.append((i, j))
        return Lattice(f"cubic_3d_L{L}", n, edges, 3, 6.0)

    @staticmethod
    def diamond_3d(L: int) -> "Lattice":
        """
        3D diamond lattice (two interpenetrating FCC sublattices).
        This is the topology used in King et al. Science 2025.
        Simplified version: we use a cubic lattice with
        nearest + next-nearest neighbor couplings to approximate.
        """
        # For a proper diamond lattice, each site has 4 neighbors
        n = 2 * L ** 3  # two sublattice sites per unit cell
        edges = []
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    # Sublattice A site
                    iA = 2 * (x * L * L + y * L + z)
                    # Sublattice B site (offset by (1/4, 1/4, 1/4))
                    iB = iA + 1
                    # A-B bonds (4 nearest neighbors)
                    edges.append((iA, iB))
                    # Connect to neighboring cells
                    for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
                        jx, jy, jz = (x + dx) % L, (y + dy) % L, (z + dz) % L
                        jB = 2 * (jx * L * L + jy * L + jz) + 1
                        edges.append((iA, jB))
        return Lattice(f"diamond_3d_L{L}", n, edges, 3, 4.0)

    @staticmethod
    def square_2d(L: int) -> "Lattice":
        """2D square lattice with periodic BC."""
        n = L * L
        edges = []
        for x in range(L):
            for y in range(L):
                i = x * L + y
                j = ((x + 1) % L) * L + y
                edges.append((i, j))
                j = x * L + (y + 1) % L
                edges.append((i, j))
        return Lattice(f"square_2d_L{L}", n, edges, 2, 4.0)


# ============================================================
# Part 2: Spin Glass Hamiltonian
# ============================================================

@dataclass
class SpinGlassHamiltonian:
    """
    Transverse-field Ising spin glass:
    H(t) = -sum_{ij} J_ij sigma_z^i sigma_z^j - Gamma(t) sum_i sigma_x^i
    """
    lattice: Lattice
    J_couplings: np.ndarray  # shape (n_edges,), random +/- J
    disorder_type: str = "bimodal"  # "bimodal" (+/- J) or "gaussian"

    @staticmethod
    def create_random(lattice: Lattice, seed: int = 42,
                      disorder_type: str = "bimodal",
                      J_scale: float = 1.0) -> "SpinGlassHamiltonian":
        rng = np.random.RandomState(seed)
        n_edges = len(lattice.edges)
        if disorder_type == "bimodal":
            J = J_scale * rng.choice([-1, 1], size=n_edges).astype(np.float64)
        elif disorder_type == "gaussian":
            J = J_scale * rng.randn(n_edges).astype(np.float64)
        else:
            raise ValueError(f"Unknown disorder type: {disorder_type}")
        return SpinGlassHamiltonian(lattice, J, disorder_type)

    def energy_classical(self, config: np.ndarray) -> float:
        """
        Classical energy for a spin configuration (+1/-1).
        E = -sum_{ij} J_ij s_i s_j
        """
        E = 0.0
        for k, (i, j) in enumerate(self.lattice.edges):
            E -= self.J_couplings[k] * config[i] * config[j]
        return E


# ============================================================
# Part 3: Jastrow-Feenberg Variational Wavefunction
# ============================================================

class JastrowFeenberg:
    """
    Jastrow-Feenberg variational wavefunction for spin systems:

    |psi> = exp(sum_i a_i sigma_z^i + sum_{ij} b_ij sigma_z^i sigma_z^j) |+x...+x>

    Parameters:
    - a_i: single-site biases (n_sites params)
    - b_ij: pair correlations (n_edges params)

    This is the ansatz used by Mauron & Carleo (EPFL 2025).
    """

    def __init__(self, lattice: Lattice):
        self.lattice = lattice
        self.n_sites = lattice.n_sites
        self.n_edges = len(lattice.edges)
        # Variational parameters
        self.a = np.zeros(self.n_sites, dtype=np.float64)  # bias
        self.b = np.zeros(self.n_edges, dtype=np.float64)  # pair correlation

    @property
    def n_params(self):
        return self.n_sites + self.n_edges

    def get_params(self) -> np.ndarray:
        return np.concatenate([self.a, self.b])

    def set_params(self, params: np.ndarray):
        self.a = params[:self.n_sites].copy()
        self.b = params[self.n_sites:].copy()

    def log_amplitude(self, config: np.ndarray) -> float:
        """
        Log of the wavefunction amplitude for a z-basis configuration.
        config: array of +1/-1 values.

        log psi(s) = sum_i a_i s_i + sum_{ij} b_ij s_i s_j + const
        (const from overlap with |+x>^N reference state)
        """
        log_psi = np.dot(self.a, config)
        for k, (i, j) in enumerate(self.lattice.edges):
            log_psi += self.b[k] * config[i] * config[j]
        return log_psi

    def log_derivative(self, config: np.ndarray) -> np.ndarray:
        """
        O_k(s) = d log psi(s) / d theta_k

        For a_i: O_i = s_i
        For b_ij: O_{ij} = s_i * s_j
        """
        deriv = np.zeros(self.n_params)
        deriv[:self.n_sites] = config  # d/d a_i = s_i
        for k, (i, j) in enumerate(self.lattice.edges):
            deriv[self.n_sites + k] = config[i] * config[j]
        return deriv


# ============================================================
# Part 4: Variational Monte Carlo Engine
# ============================================================

class VMCEngine:
    """
    Variational Monte Carlo with Metropolis sampling.
    Computes expectation values and gradients for the
    Jastrow-Feenberg wavefunction.
    """

    def __init__(self, hamiltonian: SpinGlassHamiltonian,
                 wavefunction: JastrowFeenberg,
                 n_samples: int = 10000,
                 thermalization: int = 1000,
                 seed: int = 0):
        self.H = hamiltonian
        self.psi = wavefunction
        self.n_samples = n_samples
        self.thermalization = thermalization
        self.rng = np.random.RandomState(seed)

    def _metropolis_step(self, config: np.ndarray, log_psi: float) -> Tuple[np.ndarray, float, bool]:
        """Single Metropolis update: flip one random spin."""
        site = self.rng.randint(self.psi.n_sites)
        new_config = config.copy()
        new_config[site] *= -1
        new_log_psi = self.psi.log_amplitude(new_config)

        # Acceptance ratio: |psi(s')|^2 / |psi(s)|^2
        log_ratio = 2 * (new_log_psi - log_psi)
        if log_ratio >= 0 or self.rng.random() < np.exp(log_ratio):
            return new_config, new_log_psi, True
        return config, log_psi, False

    def sample(self):
        """
        Generate MCMC samples from |psi(s)|^2.
        Returns: configs (n_samples x n_sites), log_psis
        """
        config = self.rng.choice([-1, 1], size=self.psi.n_sites)
        log_psi = self.psi.log_amplitude(config)

        # Thermalization
        for _ in range(self.thermalization):
            config, log_psi, _ = self._metropolis_step(config, log_psi)

        configs = np.zeros((self.n_samples, self.psi.n_sites), dtype=np.int8)
        log_psis = np.zeros(self.n_samples)
        n_accepted = 0

        for s in range(self.n_samples):
            # Multiple sweeps between samples
            for _ in range(self.psi.n_sites):
                config, log_psi, accepted = self._metropolis_step(config, log_psi)
                n_accepted += accepted
            configs[s] = config
            log_psis[s] = log_psi

        acceptance_rate = n_accepted / (self.n_samples * self.psi.n_sites)
        return configs, log_psis, acceptance_rate

    def compute_local_energy(self, config: np.ndarray, gamma: float) -> float:
        """
        Local energy E_loc(s) = <s|H|psi> / <s|psi>

        For TFIM:
        E_loc = -sum_ij J_ij s_i s_j  (diagonal part)
                - Gamma sum_i psi(s^i) / psi(s)  (off-diagonal part)

        where s^i = config with spin i flipped.
        """
        # Diagonal part: Ising interaction
        E_diag = self.H.energy_classical(config)

        # Off-diagonal part: transverse field
        E_offdiag = 0.0
        log_psi_s = self.psi.log_amplitude(config)
        for i in range(self.psi.n_sites):
            flipped = config.copy()
            flipped[i] *= -1
            log_psi_si = self.psi.log_amplitude(flipped)
            E_offdiag -= gamma * np.exp(log_psi_si - log_psi_s)

        return E_diag + E_offdiag

    def compute_energy_and_gradient(self, gamma: float):
        """
        Compute <E> and d<E>/d theta using VMC.

        Uses the standard SR (stochastic reconfiguration) formulas:
        <E> = mean(E_loc)
        d<E>/d theta_k = 2 Re[ <E_loc O_k*> - <E_loc> <O_k*> ]

        Also returns the S matrix for SR optimization.
        """
        configs, log_psis, acc_rate = self.sample()

        E_locs = np.zeros(self.n_samples)
        O_derivs = np.zeros((self.n_samples, self.psi.n_params))

        for s in range(self.n_samples):
            config = configs[s].astype(np.float64)
            E_locs[s] = self.compute_local_energy(config, gamma)
            O_derivs[s] = self.psi.log_derivative(config)

        # Mean energy
        E_mean = np.mean(E_locs)
        E_var = np.var(E_locs)

        # Mean derivatives
        O_mean = np.mean(O_derivs, axis=0)

        # Energy gradient: F_k = 2 (<E_loc O_k> - <E_loc> <O_k>)
        F = 2 * (np.mean(E_locs[:, None] * O_derivs, axis=0) - E_mean * O_mean)

        # S matrix (covariance of log derivatives) for SR
        dO = O_derivs - O_mean[None, :]
        S = dO.T @ dO / self.n_samples

        return E_mean, E_var, F, S, acc_rate


# ============================================================
# Part 5: Time-dependent VMC (t-VMC) for quench dynamics
# ============================================================

class tVMC:
    """
    Time-dependent Variational Monte Carlo using the
    McLachlan variational principle (TDVP).

    Propagates the Jastrow-Feenberg parameters in time
    during a quantum annealing schedule.

    dot{theta} = -S^{-1} F

    where S is the quantum geometric tensor and F is the
    energy gradient (computed from VMC).
    """

    def __init__(self, vmc_engine: VMCEngine,
                 dt: float = 0.01,
                 sr_reg: float = 1e-4):
        self.vmc = vmc_engine
        self.dt = dt
        self.sr_reg = sr_reg  # Tikhonov regularization for S matrix

    def anneal_schedule(self, t: float, t_anneal: float) -> float:
        """
        Transverse field schedule Gamma(t).
        Linear ramp from Gamma_max to 0 over time t_anneal.
        """
        gamma_max = 3.0  # typical D-Wave scale
        return gamma_max * max(0, 1 - t / t_anneal)

    def step(self, t: float, t_anneal: float):
        """
        Single t-VMC time step using TDVP + SR.
        """
        gamma = self.anneal_schedule(t, t_anneal)

        # Compute energy, gradient, and S matrix
        E_mean, E_var, F, S, acc_rate = self.vmc.compute_energy_and_gradient(gamma)

        # Regularized S matrix inversion (stochastic reconfiguration)
        S_reg = S + self.sr_reg * np.eye(S.shape[0])

        try:
            # Solve S * dtheta = -F * dt
            dtheta = -np.linalg.solve(S_reg, F) * self.dt
        except np.linalg.LinAlgError:
            # Fallback: pseudo-inverse
            dtheta = -np.linalg.lstsq(S_reg, F, rcond=None)[0] * self.dt

        # Clip parameter updates for stability
        max_step = 0.1
        norm = np.linalg.norm(dtheta)
        if norm > max_step:
            dtheta *= max_step / norm

        # Update parameters
        params = self.vmc.psi.get_params()
        params += dtheta
        self.vmc.psi.set_params(params)

        return {
            "t": t,
            "gamma": gamma,
            "E_mean": E_mean,
            "E_var": E_var,
            "param_norm": np.linalg.norm(params),
            "step_norm": norm,
            "acc_rate": acc_rate,
        }

    def run_anneal(self, t_anneal: float, n_steps: int,
                   verbose: bool = True):
        """Run full annealing simulation."""
        dt = t_anneal / n_steps
        self.dt = dt

        trajectory = []
        for step in range(n_steps + 1):
            t = step * dt
            info = self.step(t, t_anneal)
            trajectory.append(info)

            if verbose and step % max(1, n_steps // 10) == 0:
                print(f"  Step {step:4d}/{n_steps} | t={t:.3f} | "
                      f"Gamma={info['gamma']:.3f} | E={info['E_mean']:.4f} | "
                      f"var={info['E_var']:.4f} | acc={info['acc_rate']:.3f}")

        return trajectory

    def measure_correlations(self, n_measure_samples: int = 50000) -> dict:
        """
        Measure spin-spin correlations at current state.
        This is the key observable for comparison with D-Wave.
        """
        self.vmc.n_samples = n_measure_samples
        configs, _, acc = self.vmc.sample()
        configs = configs.astype(np.float64)

        # <sigma_z^i>
        magnetization = np.mean(configs, axis=0)

        # <sigma_z^i sigma_z^j> for all edges
        correlations = {}
        for k, (i, j) in enumerate(self.vmc.H.lattice.edges):
            correlations[f"{i}-{j}"] = float(np.mean(configs[:, i] * configs[:, j]))

        return {
            "magnetization_mean": float(np.mean(np.abs(magnetization))),
            "magnetization_std": float(np.std(magnetization)),
            "n_edge_correlations": len(correlations),
            "correlations_sample": dict(list(correlations.items())[:10]),
            "acceptance_rate": float(acc),
        }


# ============================================================
# Part 6: Scaling Analysis
# ============================================================

def scaling_study(lattice_type: str = "cubic_3d",
                  sizes: list = None,
                  n_steps: int = 50,
                  n_samples: int = 2000,
                  t_anneal: float = 5.0,
                  seed: int = 42):
    """
    Run t-VMC for increasing system sizes to study scaling.
    This is the core of the T3 attack: showing that t-VMC
    can be extended beyond 128 qubits.
    """
    if sizes is None:
        sizes = [3, 4, 5]  # L values -> 27, 64, 125 sites for cubic

    results = {}

    for L in sizes:
        if lattice_type == "cubic_3d":
            lattice = Lattice.cubic_3d(L)
        elif lattice_type == "diamond_3d":
            lattice = Lattice.diamond_3d(L)
        elif lattice_type == "square_2d":
            lattice = Lattice.square_2d(L)
        else:
            raise ValueError(f"Unknown lattice: {lattice_type}")

        print(f"\n{'='*60}")
        print(f"System: {lattice.name} ({lattice.n_sites} sites, {len(lattice.edges)} edges)")
        print(f"{'='*60}")

        # Create spin glass
        H = SpinGlassHamiltonian.create_random(lattice, seed=seed)

        # Create wavefunction
        psi = JastrowFeenberg(lattice)

        # Initialize with classical ground state hint
        # (set bias to favor Ising ground state)
        for k, (i, j) in enumerate(lattice.edges):
            psi.b[k] = 0.1 * H.J_couplings[k]

        # Create VMC engine
        vmc = VMCEngine(H, psi, n_samples=n_samples, thermalization=500, seed=seed)

        # Run t-VMC
        tvmc = tVMC(vmc, sr_reg=1e-3)
        t_start = time.time()
        trajectory = tvmc.run_anneal(t_anneal, n_steps, verbose=True)
        wall_time = time.time() - t_start

        # Measure final correlations
        print("  Measuring final correlations...")
        corr = tvmc.measure_correlations(n_measure_samples=min(20000, n_samples * 5))

        results[lattice.name] = {
            "n_sites": lattice.n_sites,
            "n_edges": len(lattice.edges),
            "n_params": psi.n_params,
            "dimension": lattice.dimension,
            "coordination": lattice.coordination,
            "wall_time_s": wall_time,
            "final_energy": trajectory[-1]["E_mean"],
            "final_energy_var": trajectory[-1]["E_var"],
            "final_gamma": trajectory[-1]["gamma"],
            "correlations": corr,
            "n_steps": n_steps,
            "n_samples": n_samples,
            "trajectory_summary": {
                "E_start": trajectory[0]["E_mean"],
                "E_end": trajectory[-1]["E_mean"],
                "E_min": min(t["E_mean"] for t in trajectory),
            },
        }

        print(f"  Wall time: {wall_time:.1f}s")
        print(f"  Final E: {trajectory[-1]['E_mean']:.4f}")
        print(f"  |m| = {corr['magnetization_mean']:.4f}")

    # Scaling analysis
    print(f"\n{'='*60}")
    print("SCALING ANALYSIS")
    print(f"{'='*60}")
    for name, r in results.items():
        n = r["n_sites"]
        t = r["wall_time_s"]
        p = r["n_params"]
        print(f"  {name}: {n} sites, {p} params, {t:.1f}s wall time")

    # Extrapolate to 256+ qubits
    ns = [r["n_sites"] for r in results.values()]
    ts = [r["wall_time_s"] for r in results.values()]
    if len(ns) >= 2:
        # Fit power law: t ~ n^alpha
        log_ns = np.log(ns)
        log_ts = np.log(ts)
        alpha = np.polyfit(log_ns, log_ts, 1)[0]
        print(f"\n  Scaling exponent alpha: t ~ n^{alpha:.2f}")

        for target_n in [128, 256, 512, 1024, 3200]:
            t_est = np.exp(np.polyval(np.polyfit(log_ns, log_ts, 1), np.log(target_n)))
            print(f"  Estimated wall time for {target_n} qubits: {t_est:.1f}s = {t_est/3600:.2f}h")

    return results


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("T3 ATTACK: D-Wave 'Beyond-Classical' via t-VMC + Jastrow-Feenberg")
    print("Target: King et al., Science 388, 199 (2025)")
    print("Method: Extending Mauron & Carleo (EPFL 2025)")
    print("=" * 70)

    # Run scaling study on cubic 3D lattice
    results = scaling_study(
        lattice_type="cubic_3d",
        sizes=[3, 4, 5],        # 27, 64, 125 sites
        n_steps=50,
        n_samples=2000,
        t_anneal=5.0,
        seed=42,
    )

    # Save results
    output_path = Path(__file__).parent.parent.parent / "results" / "T3_tVMC_scaling.json"
    output_path.parent.mkdir(exist_ok=True)

    # Convert for JSON serialization
    serializable = {}
    for k, v in results.items():
        serializable[k] = {
            kk: vv for kk, vv in v.items()
        }

    with open(output_path, "w") as f:
        json.dump({
            "target": "T3: D-Wave Beyond-Classical",
            "paper": "King et al., Science 388, 199 (2025)",
            "method": "t-VMC + Jastrow-Feenberg",
            "reference": "Mauron & Carleo, arXiv:2503.08247 (2025)",
            "agent": "claude3",
            "date": "2026-04-25",
            "results": serializable,
        }, f, indent=2, default=str)

    print(f"\nResults saved to {output_path}")
