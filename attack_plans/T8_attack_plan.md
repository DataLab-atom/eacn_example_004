# T8 Attack Plan: USTC Jiuzhang 3.0

**Attacker**: claude2
**Branch**: claude2
**Status**: Planned (after T4 initial results)
**Last updated**: 2026-04-25

---

## Target Summary

| Field | Value |
|---|---|
| **Paper** | Deng et al., PRL 134, 090604 (2025) |
| **Hardware** | Photonic, 255 photons |
| **Claim** | Frontier exact needs 3.1x10^10 years; sample in 1.27 us |
| **Status** | 🟡 Challenged (Oh et al. method advancing but incomplete) |

## Attack Strategy

### Primary: Oh et al. GBS Loss Exploitation

Oh, Lim, Fefferman, Jiang (Nature Physics 20, 1647, 2024) demonstrated that photon loss makes GBS classically simulable. The method directly targets the Jiuzhang series.

**Steps**:
1. Characterize Jiuzhang 3.0 loss rate from paper
2. Implement Oh et al. MPS-based classical sampler adapted for 255-photon scale
3. Show that at reported loss rates, classical simulation achieves comparable statistical distances
4. Benchmark against Jiuzhang 3.0's claimed sampling time

### Secondary: Bulmer Phase-Space Methods

Bulmer et al. (Science Advances 8, 2022) demonstrated loop hafnian-based classical sampling for GBS. Can be updated for 255-photon scale.

## Key Observation

Every previous Jiuzhang version has been classically broken:
- Jiuzhang 1.0: Bulmer et al. 2022
- Jiuzhang 2.0: Oh et al. 2024
- Jiuzhang 3.0: window is open, methods exist

The pattern strongly suggests 3.0 is also vulnerable.
