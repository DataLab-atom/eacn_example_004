# Cover Letter Draft (§J)

> **Status**: Draft v0.1
> **Target**: Nature / Science

---

Dear Editors,

We submit for your consideration our manuscript "Classical simulation
of quantum advantage experiments: a systematic evaluation revealing
regime-dependent boundaries."

**Why this paper matters for your readership:**

This work addresses the central open question in quantum computing:
which quantum advantage claims survive rigorous classical scrutiny?
We provide the first systematic, multi-target evaluation using
state-of-the-art classical methods at the actual experimental
parameters reported by hardware teams — not toy models or simplified
benchmarks.

**Key findings of broad interest:**

1. Google's Quantum Echoes experiment (Willow, Nature 2025) — the
   most recent verifiable quantum advantage claim — is classically
   attackable via Sparse Pauli Dynamics, with the experimentally
   chosen configuration (lightcone-edge M-B placement) being
   paradoxically the easiest for classical simulation.

2. Classical attack feasibility exhibits a sharp phase transition
   at a critical circuit depth determined by the butterfly velocity
   and grid geometry, with Pauli coefficient tails transitioning
   from exponential to power-law (alpha = 1.705, decisively measured).

3. Not all claims fall: Jiuzhang 4.0 stands firm against all 10
   surveyed classical methods, with a transparency audit revealing
   6 undisclosed experimental axes that prevent definitive classical
   assessment.

4. Four distinct boundary types emerge across the attack portfolio,
   demonstrating that quantum advantage is not a monolithic property
   but a regime-dependent phenomenon.

**Why Nature/Science specifically:**

The quantum advantage debate is followed by the broad scientific
community, not just quantum computing specialists. Our mixed-outcome
finding — some claims broken, some standing firm, all with quantified
boundaries — provides the honest, nuanced assessment that this debate
requires. The methodology contribution (systematic evaluation +
transparency audit) sets a template for future quantum advantage
adjudication.

**Suggested reviewers:**

1. Garnet Kin-Lic Chan (Caltech) — SPD method developer, can assess
   our Pauli-path methodology rigorously
2. Frank Pollmann (TU Munich) — tensor network expert, can evaluate
   our PEPS/Pauli-path separation claim
3. Bill Fefferman (U. Chicago) — computational complexity theorist,
   can assess our regime-dependent hardness claims
4. Jian-Wei Pan (USTC) — experimental quantum advantage lead, can
   verify we correctly characterize the Jiuzhang experiments
5. Sergio Boixo (Google) — Quantum Echoes experiment lead

**Reviewer avoidance:**

1. Aaron Szasz (Google) — co-author of Bermejo et al. which our
   work directly builds upon/challenges
2. Guifre Vidal (Google) — same group

**Declarations:**

- No conflicts of interest
- LLM-assisted: all manuscript sections co-authored with Claude
  (Anthropic), with human verification of all numerical results
  and citations. Full LLM usage disclosure per journal requirements.
- Data and code: GitHub repository with DOI (to be archived on Zenodo)
- All authors contributed per CRediT taxonomy (to be detailed)

Sincerely,
[Corresponding author]

---

## Anticipated reviewer concerns (§J2, internal only)

**Q1: "You only tested up to 24 qubits — how do you know 65q works?"**
A: Three-point scaling chain (8/12/24q) with dual-chain fit (adjacent
+ LC-edge) both project <100 terms at 65q d=4. Power-law fit R^2=0.87.
Acknowledged as formal scaling fit with wide CI (§A5 Limitation 2).

**Q2: "Per-arm depth ~12 is at the transition boundary — isn't that
just barely feasible?"**
A: Explicitly conditional claim (§A5 Limitation 5). d=12 lies at
d_crit ~ 11 +/- 1. Path C adaptive provides the worst-case rescue.
Combined Path B + C = paper-grade defensible scope.

**Q3: "Depolarizing noise model is too simple for Willow."**
A: Acknowledged (§A5 Limitation 4). Noise does NOT help OTOC^(2)
truncation — our attack relies on circuit structure, not noise.
This is actually a strength: results hold regardless of noise model.

**Q4: "Why should we trust power-law alpha=1.705 from 500 terms?"**
A: DELTA_AIC = +1158 (10^251 odds ratio). Bootstrap CI [1.55, 1.84].
Top-K convergence trend non-saturated (1.42 -> 1.71 at K=100-500).

**Q5: "Jiuzhang 4.0 'stands firm' — isn't that just admitting failure?"**
A: No — the transparency audit (6 undisclosed axes) is itself a
paper-grade contribution. "Effects beyond losses cause classical
simulability" (Goodman 2026) aligns with our finding.

---

*Draft v0.1, 2026-04-26.*
