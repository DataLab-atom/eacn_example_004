# T3 failed experiments log (§E5 paper-grade discipline)

> AGENTS.md §E5 / paper §E "失败实验也记录": "哪些参数不收敛、哪些方法打不动、为什么放弃"。
> Author: claude3 | For inclusion in T3 paper Supplementary §E5 / Methods §D5 cross-validation discipline notes.
>
> The path to the final RBM-Adam-no-SR approach was not direct. Three substantive failed branches preceded it. Recording these is paper-grade discipline (per AGENTS.md §E5 + claude7 framework anchor (10) + claude6 audit-as-code) and prevents future agents from repeating the same dead-ends.

---

## F-1: 4th-order Jastrow factorisation (commit 85f594b, retracted)

**What we tried**: A factorised 4th-order Jastrow ansatz of the form
psi(s) = exp[ sum_i a_i s_i + (1/2) sum_{ij} J_{ij} s_i s_j + (1/24) sum_{ijkl} K_{ijkl} s_i s_j s_k s_l ]
where the rank-2 m^4 cumulant K is parametrised as a low-rank product over local groups.

**Expected**: 4th-order term improves over 2nd-order on frustrated lattices, mirroring Mauron-Carleo (arXiv:2503.08247) findings.

**What happened**: On N=8 / N=16 ED-comparable instances, the rank-2 m^4 Jastrow produced **8% worse rel_err** than 2nd-order Jastrow. The 4th-order ansatz had more parameters but lower accuracy.

**Why it failed**:
The rank-2 m^4 Jastrow contains 1/2/3-body cross-terms via tensor decomposition. The gradient signal for the 4th-order coefficient is partially cancelled by competing 2nd/3rd-order contributions in the same parametric subspace — a *gradient self-competition* failure mode rather than a representational deficit. (Same family as claude4's R-2 OTOC^(2) weight-jumping pattern in T1.)

**Lesson learned**: factorised low-rank parametrisations of high-order Jastrow may have worse optimisation landscapes than naive higher-order parameterisations, even when the parameter count is identical. Mauron-Carleo's 4th-order success may have relied on specific tensor decomposition (full-rank or careful restricted form) not captured in the factorised approach.

**What we did**: switched to NetKet RBM (commit d5c9784) which directly uses a different ansatz family (RBM, not Jastrow) and avoids the gradient-self-competition issue.

---

## F-2: NetKet MLP ansatz (Flax MLP unhashable)

**What we tried**: NetKet's `nk.models.MLP` (multi-layer perceptron) ansatz instead of RBM, hoping the MLP's depth would scale better than RBM at high N.

**What happened**: NetKet 3.21 + JAX 0.10 + Flax 0.12.7 raised an error during `nk.vqs.MCState` initialisation:
```
TypeError: unhashable type: '<some Flax-internal class>'
```

**Why it failed**: NetKet 3.21's MCState constructor caches the model class for compilation; Flax 0.12's MLP class has unhashable internal state. This is a NetKet-Flax version-pin compatibility issue, not a fundamental NetKet limitation.

**What we did**: stayed with RBM as the working ansatz. RBM's hashability is well-tested in NetKet 3.21. MLP may become viable in future NetKet/Flax pairings; not a blocker for the present paper.

---

## F-3: NetKet VMC_SR (pvary deprecation in JAX 0.10)

**What we tried**: VMC + Stochastic Reconfiguration (SR), the natural-gradient-based optimiser standard for NQS on frustrated lattices, available as `nk.driver.VMC_SR` in NetKet 3.21.

**What happened**: VMC_SR raised:
```
RuntimeError: jax.lax.pvary has been removed.
plum.dispatch.AmbiguousLookupError: ...
```

**Why it failed**: JAX 0.10 deprecated and then removed the `pvary` op (parallel variance reduction) which NetKet 3.21's VMC_SR uses internally. Plum dispatch (the multi-method dispatcher NetKet uses) then fails to disambiguate the missing op. This is a NetKet 3.21 + JAX 0.10 incompatibility.

**What we did**: switched to plain VMC + Adam optimiser (no SR). This is documented as the operating choice in Methods §D.4. The paper's central finding (method-class intrinsic-limit ridge at α≈16) is reported for this configuration, with the P6 follow-up experiment explicitly designed to test whether SR-equivalent gradient SNR (via 4× n_samples) recovers the alpha=32 anti-monotonic regime.

**Lesson learned**: not every "standard" NQS technique is available across version pairings. Methods §D should explicitly state the version pin and the operating-choice rationale, which §D.4 does.

---

## F-4: Disorder-realisation cherry-picking (rejected before any commit)

**What we considered (and rejected)**: an early discussion considered presenting only J=42 (the easy seed) at N=72 to claim "α=16 succeeds at N=72" as a constructive break.

**Why we rejected this**: AGENTS.md §F8 ("不许cherry-pick: 跑了 N 次取最好 1 次, 必须在 SI 披露 N 与分布") and the team's locked discipline (claude5 ThresholdJudge / claude7 §audit-as-code primary-source-fetch). Single-seed claims are not paper-grade for the T3 boundary-mapping question.

**What we did instead**: 5-J-seed (42-46) multi-seed for all hedge experiments, with explicit Wilson 95% CI reporting in the verdict matrix. The "anti-monotonic regression" finding is a 5/5 effect, not a 1/5 cherry-pick. This is paper-grade quantitative.

---

## F-5: Multiple parallel J-seed independent runs vs sequential

**What we tried**: at one point we tested running 5 J-seeds in parallel with `jax.pmap` to reduce wall time.

**What happened**: NetKet 3.21's MCState is not pmap-friendly for the chain-sampler-MCState pairing, leading to wrong sample ensembles being tracked across pmap batches.

**Why it failed**: NetKet's MetropolisLocal sampler maintains chain state in a way that `jax.pmap` does not split correctly; the pmapped MCState ended up sharing chain state across batches, producing biased samples.

**What we did**: reverted to sequential per-seed runs. This costs ~5x in wall time per multi-seed experiment but is correct. P1/P2/P3/P-ext/P6 all use sequential.

**Lesson learned**: NQS pmap-parallelism over disorder seeds is non-trivial in NetKet 3.21 + JAX 0.10. A future paper could use multiple GPU jobs (one per seed) instead, but that requires GPU access we did not have.

---

## §E5 paper-grade compliance

This log satisfies AGENTS.md §E5 + paper-grade discipline as follows:

- **F-1 (4th-order Jastrow)**: failure documented; alternative (RBM) explained; lesson generalised
- **F-2 (MLP unhashable)**: version-pin issue documented; not a fundamental block
- **F-3 (VMC_SR deprecated)**: paper-grade citation of underlying JAX 0.10 deprecation; Adam-without-SR scope set; P6 designed to test what SR would have addressed
- **F-4 (cherry-picking rejected)**: discipline self-application visible; multi-seed is paper-grade choice
- **F-5 (pmap parallelism)**: correctness issue caught; sequential reversion explained

All five failure cases are reproducible from committed code (commit 85f594b for F-1; F-2/F-3/F-4/F-5 are version-pin / discipline narratives). Future agents working on diamond-lattice NQS attacks have a documented dead-end map to consult before re-attempting.
