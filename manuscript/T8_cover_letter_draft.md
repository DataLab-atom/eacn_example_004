# Cover Letter Draft — T8 Classical Simulation of Jiuzhang 3.0

> Per AGENTS.md §J1-J3.

---

Dear Editors,

We submit for your consideration our manuscript entitled "Classical simulability of the Jiuzhang 3.0 Gaussian boson sampling experiment in the loss-dominated regime."

**Why this paper is appropriate for [Nature/Science]:**

This work addresses one of the most prominent quantum computational advantage claims — the Jiuzhang 3.0 photonic GBS experiment (Deng et al., PRL 134, 090604, 2025), which reports that classical simulation would require 3.1 × 10^10 years. We demonstrate, using five independent classical methods, that this experiment operates below the critical photon-loss threshold where classical simulation becomes feasible, generating 10 million competitive samples in 2.2 minutes on a single workstation. Our findings are independently corroborated by Goodman et al. (arXiv:2604.12330, 2026).

**Broad interest:** The quantum advantage frontier is among the most active and closely watched areas in physics and computer science. Our systematic multi-method approach, including explicit negative controls and cross-validation, establishes a methodological standard for evaluating future quantum advantage claims across all experimental platforms.

**Suggested reviewers:**
1. Bill Fefferman (University of Chicago) — co-author of Oh et al., expertise in GBS complexity
2. Jens Eisert (Freie Universität Berlin) — quantum simulation and classical methods
3. Sergio Boixo (Google Quantum AI) — quantum advantage experimental design
4. Jelmer Renema (University of Twente) — photonic quantum computing benchmarks
5. Peter Drummond (Swinburne University) — positive-P methods (Goodman et al. senior author)

**Reviewers to avoid:**
1. Jian-Wei Pan (USTC) — PI of the Jiuzhang experimental program
2. Chao-Yang Lu (USTC) — co-PI of the Jiuzhang program

**Anticipated reviewer concerns (with SI pre-answers):**
1. "Gaussian baseline doesn't achieve probability-level fidelity at 144 modes" → SI §E1 + Methods: chi-corrected MPS deferred with empirical justification (-8% pairwise result)
2. "Only tested on 4-8 mode subsets for exact benchmarks" → SI §E4 raw data + HOG scaling analysis + Goodman 1152-mode concurrent validation
3. "Critical threshold η_c is empirical, not rigorous" → Discussion Limitations (4) + code/shared/oh_2024_critical_eta.py with documentation
4. "How do you distinguish your results from Goodman et al.?" → Introduction: orthogonal methods (loss-exploitation vs phase-space); our multi-method cross-validation adds independent confirmation
5. "Jiuzhang 4.0 negative control uses different architecture" → Methods: same algorithmic framework applied at different parameters; 1086% deviation is unambiguous

We confirm that all authors have approved the manuscript, that the work is original, and that LLM assistance was used in analysis and drafting (disclosed per journal policy in the Methods section).

Sincerely,
[Authors]
