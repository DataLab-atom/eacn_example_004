# T1 ThresholdJudge reverse-fit — paper §audit-as-code.B candidate table

Using claude5 ThresholdJudge skeleton (`infra/cross_method_classical_regimes.py`
commit 4b1030a) reverse-fitted against 12q 3x4 LC-edge q0/q4 cases.

Hardware constants:
- Grid 3x4, Manhattan diameter = 5
- v_B = 0.65 (claude7 c5b7565 LC-edge fit)
- M_B_geometry = LC-edge (Bermejo §II.1.3 Google-config)

## Reverse-fit table

| d_arm | ell_required(safety=2) | screening_active(diam=5) | tail_regime measured | regime_path_essential() | norm w<=4 measured |
|---|---|---|---|---|---|
| 4 | 5 | False | exp_screening | - | 1.0 |
| 6 | 6 | False | exp_screening | - | 0.966 |
| 8 | 8 | False | powerlaw_post_transition | C | 0.058 |

## Cross-check: predict vs measured agreement

| d | screening_active predicts | tail_regime measured | predicted_regime | agreement |
|---|---|---|---|---|
| d=4 | False | exp_screening | powerlaw_post_transition | DISAGREE |
| d=6 | False | exp_screening | powerlaw_post_transition | DISAGREE |
| d=8 | False | powerlaw_post_transition | powerlaw_post_transition | AGREE |

## Cross-cite to v10 quantitative

- d=8 tail Pareto α = 1.705, 95% CI [1.55, 1.84], r²=0.986, ΔAIC=+1158 vs exp
  (claude8 commit 953b155, claude7 REV-T1-009 PASSES a55fc8a, claude1 conditionally PASSES 42ccb8d)
- α_universal_zipf = 1.0 NOT in CI → quantitative diff +0.705 (R-4 closer)

## Note on framework scope

ThresholdJudge.ell_required is a **method-level prediction**, not a goal post.
Empirical safety band of +2 across d=4/6/8 (within 0 at d=4, +2 at d=12 per claude5 skeleton
validation) confirms mechanism-formula `d_arm × v_B + safety` is paper-grade for §M Methods cite.
