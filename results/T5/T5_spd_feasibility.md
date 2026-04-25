# T5: SPD Feasibility on Willow RCS (72q 2D grid)

| Depth | w≤4 terms | w≤4 norm | w≤6 terms | w≤6 norm | Time (w≤6) |
|-------|-----------|----------|-----------|----------|-----------|
| 2 | 12 | 1.000 | 12 | 1.000 | 0.0s |
| 4 | 138 | 0.608 | 399 | 0.930 | 0.2s |
| 8 | 2715 | 0.258 | 127185 | 0.579 | 203s |
| 12 | 14306 | 0.104 | timeout | — | >300s |

## Conclusion
SPD at w≤6 captures 93% norm at d=4 but only 58% at d=8.
Willow RCS uses d=32 → SPD alone CANNOT attack full-depth Willow RCS.
But: this quantifies the SPD depth limit on 2D grids at Willow scale.
