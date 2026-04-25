# T2: SPD on IBM Heron 133q Heavy-Hex — MEASURED

| Depth | w≤6 terms | Norm | Time | Status |
|-------|-----------|------|------|--------|
| 4 | 48 | 1.000 | 0.0s | **100% captured** |
| 8 | 12621 | 0.602 | 52.7s | 60% captured |
| 12 | OOM | — | — | Memory limit |
| 20 | — | — | — | Not attempted |

d=4 captures 100% of operator at w≤6 on 133q heavy-hex.
Algorithmiq claims operator dynamics — if depth ≤ 4, SPD breaks it.
IBM Eagle was broken by Begusic SPD at similar scale.

## Depth Sweep w≤4 (133q heavy-hex)

| Depth | Terms | Norm | Status |
|-------|-------|------|--------|
| 2 | 3 | 1.000 | ✅ trivial |
| 4 | 48 | 1.000 | ✅ 100% captured |
| 6 | 222 | 0.371 | ⚠️ 37% |
| 8 | 466 | 0.360 | ⚠️ 36% |
| 10 | 2051 | 0.147 | ❌ 15% |

Critical depth for SPD on heavy-hex: d_crit ≈ 5 (between d=4 full capture and d=6 collapse).
Algorithmiq experiment depth determines whether T2 is attackable.
IBM Eagle utility experiment used ~60 Trotter steps — but Begusic broke it with SPD.
Key: Begusic used different SPD variant (not weight-truncated but amplitude-truncated).
