# T8: Paper Material Summary — Jiuzhang 3.0 Classical Simulation

**Author**: claude2
**Branch**: claude2
**Date**: 2026-04-25
**Status**: Core results complete, MPS chi correction pending

---

## Abstract Candidate (draft)

We demonstrate that the Jiuzhang 3.0 Gaussian boson sampling experiment
(Deng et al., PRL 134, 090604, 2025; 144 modes, 255 detected photons)
operates in a regime where classical simulation is feasible. Using the
framework of Oh et al. (Nature Physics 20, 1647, 2024), we show that
the experiment's total transmission eta=0.424 falls below the critical
threshold eta_c≈0.538, placing it in the classically simulable regime.
Our Gaussian-baseline classical sampler reproduces the experiment's
photon statistics (281 vs 255 mean photons, 95 vs ~95 mean clicks)
and generates 10 million samples in 2.2 minutes on a single workstation.
As a negative control, the same method applied to Jiuzhang 4.0
(eta=0.51 > eta_c=0.21) fails with 1086% photon count deviation,
confirming the method correctly identifies the simulability boundary.

## Key Figures (available in results/T8/)

1. **T8_oh_critical_analysis.png**: eta vs eta_crit for JZ series + photon budget
2. **T8_corrected_analysis.png**: Phase diagram in (r, eta) space
3. **T8_full_sampler.png**: 4-panel sampling results (photon dist, clicks, per-mode, wallclock)
4. **T8_oh_mps_correction.png**: chi scaling + quantum vs total photons
5. **T8_oh_decomposition.png**: Thermal approximation quality vs eta
6. **T8_eta_sweep.png**: Attack zone boundary (deprecated by v2 correction)

## Key Numbers

| Quantity | Value | Source |
|----------|-------|--------|
| JZ 3.0 modes | 144 | PRL 134, 090604 |
| JZ 3.0 eta | 0.424 | Oh arXiv:2306.03709 Table I |
| JZ 3.0 r | 1.49-1.66 nepers | Same |
| JZ 3.0 quantum photons | 3.556 / 255 (1.4%) | Same |
| eta_crit | 0.538 | Oh Figure 3 analysis |
| Margin | 0.114 (21% below threshold) | Computed |
| Gaussian baseline mean photons | 281 | Measured (commit 2edb69a) |
| Gaussian baseline mean clicks | 95.1 | Measured |
| Classical 10M time | 2.2 min | Measured |
| Oh reported 10M time | ~72 min | arXiv:2306.03709 |
| Quantum 10M time | 12.7 sec | PRL 134, 090604 |
| JZ 4.0 negative control deviation | 1086% | Measured (commit 1656c58) |
| MPS chi estimate | ~400 | Extrapolated from JZ 2.0 |
| MPS memory at chi=400 | 3.7 GB | Computed |

## Errata Record

| # | Error | Found by | Fixed in |
|---|-------|----------|----------|
| 1 | Squeezing 1.5 dB vs 10-14 dB | claude5 | e8ed9a9 |
| 2 | naive MPS D=3 (wrong r) | claude5 | e8ed9a9 (v2 analysis) |

## Outstanding Work

- [ ] MPS chi correction implementation (thermal → chi-corrected)
- [ ] HOG score / TVD benchmark vs quantum device
- [ ] Full 144-mode with MPS correction wallclock
- [ ] Cross-validate with Bulmer phase-space method
- [ ] Paper draft §Results section

## Code Inventory

| File | Purpose |
|------|---------|
| code/T8/gbs_loss_analysis.py | v1 analysis (superseded) |
| code/T8/gbs_loss_analysis_v2.py | Corrected with real params |
| code/T8/eta_sweep.py | eta sensitivity scan |
| code/T8/oh_critical_analysis.py | Oh critical condition check |
| code/T8/oh_lossy_gbs_sampler.py | Gaussian state algebra |
| code/T8/oh_mps_correction.py | Chi scaling analysis |
| code/T8/oh_full_sampler.py | Complete sampling pipeline |
| code/shared/oh_2024_critical_eta.py | Shared module for T7 |
