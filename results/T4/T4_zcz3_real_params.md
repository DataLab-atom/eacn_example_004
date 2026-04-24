# T4: ZCZ 3.0 Real Parameters (from arXiv 2412.11924)

## Extracted Data

| Parameter | Value | Source |
|---|---|---|
| Qubits (active) | 83 | p1 |
| Cycles | 32 | p1 |
| Gate pattern | ABCD-CDAB, iSWAP-like | p2 |
| 1Q gate error | 0.97‰ (F = 99.903%) | p2 |
| 2Q gate error | 3.75‰ (F = 99.625%) | p2 |
| Readout error | 8.67‰ (F = 99.133%) | p2 |
| Samples collected | **410 million** (91 hours) | p3 |
| Patch XEB fidelity | 0.70–0.79 | Fig. 3 region |
| Classical estimate | 6.4×10^9 years on Frontier | abstract |

## Impact on T4 Attack

### Statistical argument UPDATE
- Previous: N = 10^7 → SNR = 0.82 < 3 → "undetectable"
- **CORRECTED: N = 4.1×10^8 → SNR = 5.26 > 3 → DETECTABLE**
- The statistical undetectability argument DOES NOT HOLD
- ZCZ 3.0 collected 3.1x the minimum samples needed

### Noise analysis CONFIRMED
- Gate fidelities match my estimates within 0.01%
- F_XEB (estimated) = 0.026% from fidelity budget
- Patch XEB = 70-79% (much higher — these are for small sub-circuits)
- Full-circuit XEB: need to extract from Figure 3

### Attack strategy REVISED
- Statistical argument: WITHDRAWN (N is sufficient)
- Constructive attack: MUST demonstrate classical method achieving
  comparable XEB to quantum device
- Noise exploitation: remains primary approach (lambda/lc = 1.55)
- Morvan phase transition: ZCZ 3.0 IS in classical phase per claude1's analysis
