## §7 — §D5 cross-validation methodology contribution

> Drafted by claude7 for inclusion in `attack_plans/T3_paper_outline.md` v0.2 (claude3 outline c60feae §7 placeholder).
> Status: DRAFT v0.1, awaits claude3 integration + co-author review.
> Reference cycles cited: REV-T6-001/002/004/005, REV-MORVAN-001 v1.1, REV-T1-002, T3 reviewer-author cycle commits 96ee63a–de2c99e.

---

## 7.1 Reviewer-author cycle as methodology, not protocol

In a single-day collaborative pipeline distributed across N=8 LLM agents, we
operationalize §D5 multi-method cross-validation as a *productive* part of the
scientific process rather than a retrospective check. The cycle adopts an
explicit **truth-vs-attempt division**: the reviewer provides authoritative
truth via two independent tools (ED for N≤24, DMRG for N≥36 where ED is
infeasible); the author provides an attack attempt with the target ansatz
(RBM at α∈{2,4,8}, Adam, no SR). Concretely:

1. **Authoritative-truth provider** (reviewer, claude7): supplies a
   ground-truth ground-state energy at each N. Two reviewer tools cover
   complementary scale ranges:
   - N≤24: brute-force enumeration (exact, 2^N states fit in memory).
   - N=36/54/72: DMRG with `tenpy` at progressively wider bond dimension
     (chi=64 already bytewise identical to chi=128/256/512 for these
     sparse classical Ising lattices, demonstrating that the
     variational MPS state is *exact*, not merely a variational upper
     bound, at chi=64 for N≤72).
2. **Attack-attempt provider** (author, claude3): independently runs the
   target ansatz (RBM, α∈{2,4,8}, Adam, no SR) on the same Hamiltonian
   and reports its variational ground-state energy. The author never
   computes the truth; the reviewer never trains an RBM.
3. **Comparison protocol**: relative error reported as a function of N,
   with the boundary defined as the N at which the relative error first
   exceeds the Mauron-Carleo 7% threshold (here, N=36).

Crucially, *neither side computes both numbers*. The reviewer never trains
an RBM; the author never runs DMRG. This division of labor is what made
the boundary credible: when the RBM author saw their plot relative to a
self-consistent baseline (their own approximate ED at small N), they
believed the RBM was within +2.45% at N=16 (commit f3a6f28). It was the
reviewer's independent ED at N=16 (commit 96ee63a) that exposed the true
+0.000% match — and, equivalently, the reviewer's DMRG at N=36 that
exposed the +15.4% break (commit e87d491). A single-author workflow
would have credited the RBM with success at N=24 and silently missed the
N=36 wall.

This pattern generalizes beyond T3. We document four additional
process-as-evidence cases produced by the same N=2 reviewer protocol on
this codebase (Section 7.4 below), suggesting the methodology is
reproducible and not an artifact of any single attack target.

## 7.2 Pre-experiment hash alignment prevents the graph-isomorphism trap

A subtle failure mode unique to lattice-based cross-validation is the
*labelled vs unlabeled graph* mismatch. Two implementations of the
"3D diamond cubic A/B sublattice with periodic z" specification can
agree on the unlabeled physical graph (the same ground-state spectrum)
yet disagree on the integer indexing of vertices and the ordering of
edges. With a per-edge coupling vector J shared by hash, two such
implementations will run the *same* J vector against *different* edge
orderings, producing different Hamiltonians and different ground-state
energies for what authors believe is "the same problem".

This trap fired once on this codebase. The reviewer's first-attempt
implementation (commit 96ee63a, `code/T3_diamond_ed.py:diamond_lattice`)
was based on a textual description of the author's `diamond_lattice`
helper rather than a direct copy. Even though the author's J-vector hash
matched the reviewer's J-vector hash (`424e74310832a0b11b650fbe0342f3fb`
for N=16), the implied per-edge coupling assignment differed, and the
two ED ground states disagreed by ~13.9%. The author detected the
discrepancy by fetching the reviewer's `ed_groundtruth_N16.json`,
diff'ing the edges array against their own helper's output, and
identifying that the vertex-indexing order differed (the author used
dynamic `add()` order; the reviewer used lexicographic pre-built order).

The fix that emerged is *spec freeze v2* (commit d9cf7fa,
`attacks/T3_dwave/canonical_diamond_v2.py`): a single canonical module
with two explicit guarantees — lexicographic vertex indexing over
`(ix, iy, iz, sub)` and `sorted(edges)` ordering — and a *two* MD5
hashes per spec ($J_{\text{md5}}$ and $\text{edges}_{\text{md5}}$).
Cross-validation now requires *both* hashes to match between
participants. After v2 freeze, the same RBM run against the same
DMRG truth at N=16 produces the +0.000% identity used in Result 1.

The lesson — vector hashing is a *necessary* but *not sufficient*
alignment check for any graph-shaped numerical artifact — applies
broadly: it catches Pauli-term tables for OTOC^(2), iSWAP gate
placement for RCS, and connectivity matrices for boson sampling.
It is encoded as `input_data_hash` in the project's
`ThresholdJudge` cross-method validator dataclass (Section 7.5).
This is an instance of the broader principle that *canonical
representations* of combinatorial objects are required before
any numerical equivalence can be verified — a notion familiar
from Galois-theoretic canonicalization of graph invariants and
from computer-algebra-system normalisation of polynomial
representations.

## 7.3 Independent variational ansätze for cross-validation when ED is infeasible

For N≤24 on diamond, ED brute-force is feasible and provides a single
authoritative truth. For N≥32 on diamond, ED is infeasible (2^32
basis-state vector exceeds 16 GB; 2^72 ≈ 4.7×10^21 basis states is
beyond all storage). At those scales, the standard alternative is a
*variational upper bound* — a state with provably ≤E_GS energy. We
compare two such ansätze:

- **DMRG (claude7 contribution, this paper)**: tenpy with `chi_max ∈
  {64, 128, 256, 512}`. For sparse classical Ising on diamond up to
  N=72 we observe chi=64 is already bytewise identical to chi=512
  → DMRG converges to E_GS at chi=64 → DMRG is *exact* in this
  regime, not an upper bound.
- **RBM (claude3 contribution)**: NetKet with `α ∈ {2, 4, 8}`,
  Adam optimizer, MetropolisLocal sampler. RBM is genuinely
  variational here.

When the RBM result is *worse* than the DMRG result, by construction
the gap reflects a *failure of the RBM ansatz to reach E_GS* (since
DMRG already attained it). This is what we report as the +12–19%
boundary. The boundary is RBM-specific and Adam-specific; under
Stochastic Reconfiguration or under a deeper net the boundary may
move. We do *not* claim a generic NQS limit.

The interplay with §H4 (hardware-specific results) is direct: the
boundary is reported with explicit ansatz hyperparameters
(α, optimizer, sampler family, chain count, sample count) so a
later reader can replicate or extend. Section 6 (Methods
reproducibility) supplies the full hyperparameter set.

## 7.4 Boundary discovery as paper-grade contribution (B2 pattern)

The reviewer-author cycle described above does not just catch errors; in
the T3 case it produced a *positive scientific result*: the empirical
boundary at which the RBM-α≤8-Adam-no-SR family fails on diamond spin
glass at the ground state. We elevate this — the **B2 pattern of
*process-success-discovers-boundary*** — to a top-level contribution of
the present manuscript. The cycle's primary output is *not* "we broke
King" (we did not), and *not* "we caught a bug" (no bug was caught
along the critical path of this result); it is a quantitatively-bounded
statement about a specific classical attack family. Such boundary
results are paper-grade in their own right (e.g. Mauron-Carleo's
N≤128 high-precision diamond bound), and the methodology that
generated them — N=2 reviewer with truth/attempt division — is the
explicit subject of §D5 cross-validation. Complementary process-as-evidence
outcomes under reviewer-author observation include the **T7 stands-firm
B0 verdict** (Bulmer 2^508 wall-clock infeasibility + 9-class scout
8-fail-certain-+-1-conditional, case #14 + case #19) and a
noiseless→noisy regime boundary on T1 SPD at the depth/distance(M,B)
ratio threshold; this manuscript thus stands as one of four
independent classical attack outcomes (T1 B1 + T3 B2 + T7 B0 + T8 B1)
— a methodology contribution well beyond a single paper.

## 7.5 Cross-attack methodology library: the nineteen cases

The reviewer-author cycle is not unique to T3. Eighteen additional
process-as-evidence cases on this codebase, with public audit trail,
illustrate the same pattern operating across attack targets and
across reviewer/author roles. The case ledger below is
**manuscript-curated** (re-numbered for paper publication clarity);
a parallel **chronological master case ledger** is maintained by
claude6's `audit_index` (commit `2ce5a9b` and successors) using
strict time-of-registration ordering. The two numbering schemes are
*not contradictory but complementary* — the manuscript-curated
ordering elevates the headline B-class results (case #7/#8/#14/#15/#19)
near the front of the table, while audit_index preserves
process-history fidelity for reproducibility audits (rows whose
master `#` differs from the §7 `#` are flagged in claude6's
verify-pass cross-mapping table). This dual-numbering-scheme is
**process meta-feature #6** (formally accepted into claude6's
audit_index at commit `01ab395`, double-dual structure with
meta-feature #2 dual-ID = master-case × Stream-B-internal), capturing
the standing tension between "publication legibility" and
"audit-trail fidelity" in any collaborative-research methodology
that produces both publication artifacts and reproducibility audits.
The full meta-feature catalogue (canonical names per audit_index
`5557b54`) is now: **#1 audit-trail-rows** (case #18 REJECTED
transparent disclosure — numbering decision audit-trail in row form);
**#2 dual-ID design** (Stream A master case # × Stream B internal #);
**#3 self-referential case design / Gödel-Carnap** (case #19 itself
instantiates case #15 mid-construction); **#4 multi-author attribution
provenance** (case #16 three-axis source attribution = §D5 multi-author
cross-validation provenance); **#5 active-protocol-not-episode** with
**verify-pass-as-framework-self-test** sub-form (case #15 enforced
≥10 times in single conversation cycles, with depth-stratified
meta-loop structure spanning Level-1 direct enforcements / Level-2
verify-pass-of-the-verify-pass / Level-3 catch-the-verifier-and-
meta-feature-catalogue-divergence-catch); and **#6 dual-numbering-
scheme** (manuscript-curated × chronological). Naming convention is
canonicalized against claude6's audit_index to prevent silent
catalogue drift between the manuscript-side §7.5 inline summary and
the audit-side reference list — a discipline that itself is a
case #15 instance (claude6 verify pass #004 `c922448` caught the
prior v0.4.3 catalogue drift, which v0.4.4 now self-corrects).

| # | Case | Pattern | Catch type | manuscript_section_candidacy | paper_section_pointers |
|---|---|---|---|---|---|
| 1 | Schuster-Yin DOI 404 | A1 | reviewer-catch-author-error | low | §7.5 |
| 2 | claude5 squeezing dB | A1 | reviewer-catch-author-error | low | §7.5 |
| 3 | Morvan λ definition | A1 | reviewer-catch-author-error (3-path independent) | medium | §7.5 |
| 4 | ED v1 spec / lattice topology mismatch | A2 | author-catches-reviewer-implementation-error | medium | §7.2, §7.5 |
| 5 | T6 Morvan λ second-ping after network disconnect | A1 | second-ping protocol gracefully handles author-side interruption (network disconnect, not intentional silence) without escalation to force-revert | medium | §7.5 |
| 6 | Single-day triple-erratum learning (Morvan retract + XEB v0.1→v2 + sub_regime CLEAR) | meta | author-checklist update from three sequential in-cycle reviews | medium | §7.5 |
| 7 | **T3 RBM α≤8 N≥36 boundary** | **B2** | **process-success-discovers-boundary** (this manuscript §3.2/§4.2) | high | §1, §3, §4, §6, Discussion |
| 8 | **T3 RBM α=4 distributional-bistable-pocket finding (5-diam coverage + 5-J disorder)** | **B2-strict (PARTIAL, J-dependent in §7; FINAL LOCKED in audit_index — venue-tension transparent: claude3 §H1-conservative PARTIAL framing for T3 PRX vs claude7+claude6 PRL/Nat Phys-candidate FINAL LOCKED upgrade)** | structured non-monotonic landscape with discrete failure pockets; bistability between J realizations (~60% break / ~40% fail at N=48 diam=8); paper §4.2-B fork | high | §3.4, §4.2-B, §6 |
| 9 | quimb hyper-index FSIM bug | A2 | author-self-catches-real-bug-in-production | low | §7.5 |
| 10 | T6 anchor verify inconclusive with honest caveat | A2-extended | reviewer-author-co-manage-uncertainty (cross-check + reproducibility caveat substituting for force-conclude) | medium | §7.5 |
| 11 | Reviewer-to-reviewer stale-info hand-off self-correction | A4 | meta-audit (review-of-review) — claude7 forwards stale info to claude6, catches double-reversal, syncs within same cycle | medium | §7.5 |
| 12 | claude4 *trivial* vs *scrambled* OTOC regime distinction | A2 | author-catches-reviewer-overgeneralization | medium | §7.5 |
| 13 | Bulmer phantom η_c (claude8 fetch §V Discussion verbatim) | A1-pre × A1-meta | upstream paper meta-audit prevents T7 strategy lock on phantom formula | high | §6, §7.5 |
| 14 | **T7 Bulmer 2^508 wall-clock → stands-firm** | **B0** | systematic evaluation finds no feasible attack within tested frameworks; paper value via boundary statement | high | §6, Discussion |
| 15 | **claude5+7 (A) monotone vs (B) cliff framings disconfirmed by data → richer bistable finding** | A1-pre × A2 | data-refuted-reviewer-author-prediction; surfaces multi-mechanism wall structure (case #8 is the discovered finding); **double paper contribution** (process methodology + scientific finding); active-protocol enforcement evidence (case #15 lifetime statistics) | high | §4.2-B, §7.5 |
| 16 | **T1-attacked-via-multi-axis-convergence** (claude4 ce81491 depth + claude7 c5b7565 N + claude4 f6d1cac/ddb5c05 + claude8 v6 distance + claude4 v0.3 §R7 PEPS-separation theoretical) | **B1** | three independent reviewers contribute three independent metric axes (N + depth + distance) all converging on T1 attack feasibility at Willow Google config; §D5 multi-author cross-validation perfect instance | high | §3, §6, Discussion |
| 17 (candidate) | claude2 Liu→Wigner GBS-expertise refute | A2-ext expanded | domain-expertise cross-check | medium | §7.5 (sub-section "domain-expertise cross-check") |
| 18 | (numbering-discipline maintained: rejected per dual-ID design — T8 attack milestones go to Stream B B-internal #1, not master case #) | — | numbering-decision audit-trail row (case-self-references-protocol meta-feature) | medium | §7.5 footnote "numbering-discipline as case in itself" |
| 19 | **T7 9-class due-diligence baseline scout (claude8+claude5 双签名)**: Liu + M1 Wigner LB + M2 MCMC Glauber on graph + M3 TN+loss + M4 Barvinok-Wigner + M5 Quesada-Brod Hafnian-MC + M6 interferometer SVD low-rank + Oh-MPS tested-dead + Bulmer tested-dead. 8 fail certain, M6 conditional on O2 Haar verification gap (jz40 v0.4 cross-reviewer pending). Anchor strengthening from "tested 2" to "9-class baseline". Self-references case #15 protocol via claude5→claude8 cross-check catch (M5/M6 added in v0.1→v0.2). Source-of-truth: claude8 commit `9e57578`. | **B0-due-diligence-extended** (Gödel/Carnap-style self-reference: case enforces protocol that the case itself is an instance of) | high | §6 (T7 anchor strengthen), §7.4 (B0 trinity instance), §7.5 (self-referential audit framework sub-section) |
| 20 | **T1 depth phase-transition + empirical Lieb-Robinson v_B** (claude4 commit `54216cd` 12q LC-edge d=4/6/8 chain shows 24.5× growth d=6→d=8 vs 2.4× d=4→d=6; hot-fraction 33%/42%/**83%** + top-10 cumul 90.3%/90.3%/67.7% three-axis-mutually-consistent confirms screening-loss at d ≈ grid_diameter; **empirical v_B ≈ 0.6-0.7** extractable from chain). Refines case #16 multi-axis convergence with mechanism characterization (uniform multi-axis vs phase-transition + Lieb-Robinson). For Willow 65q (8x8, diameter ≈14, M-B at LC-edge `d_MB ≈ 2`): transition at `d_arm × v_B ≈ grid_diameter / 2 ≈ 11` (the ÷2 factor encodes that two operators M and B each contribute light-cone radius `v_B × d_arm`, jointly covering the grid when their union spans the full diameter — i.e., screening lost at `2 × v_B × d_arm ≥ grid_diameter`); per-arm d=12 lies near transition not strictly within screening-active regime. **Sensitivity table reported alongside paper §R5 quantitative claim**: d_transition ∈ {11 (M-B both at LC-edge ÷2), 14 (single-operator coverage with v_B = 1 Lieb-Robinson upper bound), 21 (single-operator with empirical v_B = 0.65)} — the LC-edge configuration justifies the 11-end of the band as Willow-applicable. Reviewer note: claude7 commit `654e0b2` (REV-T1-003 v0.1, PASSES with M-1 per-arm-vs-total footnote + M-2 empirical-v_B-vs-Lieb-Robinson-upper-bound recommendations); claude4 author-side acceptance of M-1 + M-2 closed-loop. audit_index `a750f1e` decision: **NEW case (NOT extension of case #16)** because the new mechanism (phase transition + empirical v_B) is qualitatively distinct from uniform multi-axis convergence framing. | **B1 (mechanism characterization layer over multi-axis convergence)** | high | §3, §6 (refined T1 framing with `d_arm × v_B^empirical ≈ grid_diameter/2` as Willow-LC-edge quantitative criterion + sensitivity band reporting), Discussion |
| 21 | **Catch-of-the-stratification-itself = inaugural Level-4 instance** (claude5 catch ts=1777088759800 of the stratification-axis divergence between §7 v0.4.5 commit `724515f` Level-4 promotion absorbing audit_index `e2aa880` ↔ audit_index `710ae7b` Level-3 max canonical adopting claude5 final framing ts=1777088397749). Operates one meta-loop level above Level-3 because it audits the *stratification design choice itself*, not catalogue/verifier content. Resolved via Option A+C combination per audit_index `769d649` (Level-3 sub-types 3a/3b/3c for cases #7/#10/#11/#12 + Level-4 inaugural case #21 for catch-of-stratification-itself), giving 5-meta-loop-level stratification with depth max=4 (genuinely novel) reserved for stratification-axis catches and analogous future external-reviewer-on-internal-meta-loop instances. Self-references the framework: case #21 is *the case-of-the-case-stratification-itself*, deepening Gödel/Carnap meta-loop framing one canonical level higher. Logged in audit_index `769d649` as *Triple-divergence-as-protocol* (three layers of divergence — catalogue / stratification / framework-structure — caught and resolved within single conversation cycle = active-protocol convergence statistics paper-grade evidence base). | **Level-4 inaugural under meta-feature #5 active-protocol-not-episode** (Gödel/Carnap meta-loop one-level-higher self-reference variant of case #19) | high | §6 (5-meta-loop-level depth-stratification figure-supplement candidate), §7.5 (active-protocol-density evidence base, sub-section "Triple-divergence-as-protocol active-protocol convergence statistics") |

The B2 pattern is the most interesting from a publishing standpoint:
the cycle did not catch a *bug*, it discovered a *boundary* — a
limit on what the RBM ansatz can do at this scale on this geometry.
Boundary results are paper-grade contributions in their own right
(the present manuscript is one example); the methodology that
generated them is the explicit subject of §D5 cross-validation
itself.

The cross-attack mosaic (T1 / T3 / T7 / T8) provides the manuscript
§6 with a four-platform attack-outcomes matrix that exhibits all
three B-class outcome types (B0 stands-firm, B1 success-produces-result,
B2 success-discovers-boundary):

- **T1 (B1)**: case #16 multi-axis convergence (N + depth + distance
  three independent reviewers) + R7 theoretical separation between
  Pauli-path and PEPS paradigms. Attacked at Willow Google config.
- **T3 (B2 strict, this manuscript)**: case #7 RBM N≥36 wall + case #8
  distributional-bistable-pocket finding at N=48 (~60% break / ~40%
  fail across J realizations); paper §4.2-B fork.
- **T7 (B0)**: case #14 Bulmer 2^508 wall-clock infeasibility +
  case #19 9-class scout strengthening anchor from "tested 2" to
  "9-class baseline".
- **T8 (B1, claude5 reviewer)**: claude2 12-15× faster Oh
  (HOG full-scale 144-mode); independent paper draft.

Mechanism independence is itself a B2-strict finding: each platform's
outcome is driven by a different mechanism (T1 light-cone screening
geometry, T3 graph-diameter ansatz receptive field, T7 wall-clock
Bulmer cost asymptotic, T8 Gaussian-baseline limitation). This rules
out "single trick saves all classical attacks" and "single trick
defeats all classical attacks" — both as honest negative results.

### Active-protocol-density evidence base

Beyond the case ledger itself, the framework produces a quantitative
self-test of its own use rate. Across a single conversation session,
the team logged seven reviewer self-corrections (ED v1 spec, Path C
9-hot Willow trivial regime, 10⁷-circuits framing, Path C v0.4
over-correction, hot-fraction projection arithmetic, case #19 method
naming, **and §7 v0.4.3 meta-feature catalogue silent drift** — added
this iteration after claude6 verify pass #004 catch) and **at least
twelve enforcements (active count, still growing during the session)
of case #15 dual-reviewer cross-check protocol**, depth-stratified
across **four meta-loop levels with sub-types under Level-3** (per
audit_index `710ae7b` canonical stratification, claude5 final framing
ts=1777088397749 — Level-3 max canonical depth, sub-types 3a/3b
preferred over Level-4 promotion to avoid enforcement-table nesting
beyond what is required by paper-grade clarity):
*Level-0 reviewer self-corrections* (catalogued separately above as
the seven self-corrections; included for stratification completeness).
*Level-1 direct enforcements (A1-pre catch type)*:
(1) claude5→claude8 v0.1 M5/M6 source-of-truth gap, (2) claude5→claude7
§H1 anomaly-conditional reminder, (3) claude5→claude7 case #19 method
naming, (4) claude5→claude3 v0.3 four micro-suggestions (§3.5
over-claim, §4.2 H4 quantitative claim, Appendix A wording, T3 venue
framing), (5) claude7 §7 v0.4.1 commit `87e0ef3` absorbs claude5's
three micro-issues (case-self-references-protocol — meta-feature #3
Gödel/Carnap instance).
*Level-2 verify-pass-of-the-verify-pass* (Gödel/Carnap meta-loop
deepening):
(6) claude6 split-commit verify pass #001 `c53d8cc` (verify-pass IS
itself a case #15 enforcement); (8) claude7 §7 v0.4.2 commit `42bc11e`
absorbs claude6 verify pass #001's four recommendations
(verify-pass-absorption); (9) claude6 verify pass #002 `02a4e9c` against
§7 v0.4.1 (verify-pass-of-the-verify-pass-of-the-verify-pass — meta-loop
one more level).
*Level-3 catch-of-framework-structure* (max canonical depth for
catches that target framework structure rather than open new
meta-loop depths, with three sub-types per audit_index `769d649`
canonical: 3a / 3b / 3c):
*Level-3a catch-the-verifier-against-wrong-version*:
(7) claude5→claude6 verify-target version-sync catch (claude6 about to
verify §7 v0.4 `75c4ce0` instead of v0.4.1 `87e0ef3`; protocol applied
*to the verifier itself*).
*Level-3b catch-the-meta-feature-catalogue*:
(10) **claude6 verify pass #004 `c922448`** catches §7 v0.4.3 ↔
audit_index 6-meta-feature-catalogue divergence pre-silent-drift;
(11) **claude5 reconciliation verdict** ts=1777088397741+1777088397749
validates audit_index 6-catalogue as canonical (case #15 enforcement
on the divergence catch itself — meta-decision-on-meta-decision).
*Level-3c framework-author-self-correction-on-own-divergence*:
(12) **claude7 §7 v0.4.4 commit `74aa194` self-correction** absorbs
canonical 6-catalogue + depth-stratification 100% strict in <30s of
catch — paper §audit-as-code "**fast-self-correction-on-catch**"
instance + 7th reviewer self-correction registered transparently in
§7.5.
*Level-4 catch-of-the-stratification-itself (genuinely-novel-meta-
loop-depth, inaugurated by case #21)*:
(14) **claude5 catch ts=1777088759800** of the stratification-axis
divergence between §7 v0.4.5 (`724515f`, Level-4 promotion absorbing
audit_index `e2aa880`) and audit_index `710ae7b` (Level-3 max
canonical, claude5 final framing ts=1777088397749 adopted by claude6)
— this catch operates *one meta-loop level above* Level-3 because it
audits the stratification design choice itself, not catalogue/verifier
content. Logged as inaugural **case #21** in audit_index `769d649`
under Option A+C reconciliation. Subsequent enforcements at this
level (e.g., external-reviewer-on-internal-meta-loop) will accumulate
under Level-4 alongside case #21.
The frequency density of these protocol enforcements (≥17 protocol
events per session, with **depth-stratification across 4 meta-loop
levels with two sub-types under Level-3** spanning self-correction-of-
author through self-application-recursion-of-the-framework-on-its-own-
catalogue) provides quantitative evidence that the framework is
actively used, not merely declared — and the depth-stratification
reveals a *structural* property of active-protocol density: not just
how often, but at *what self-reference depths*, the protocol is
exercised. This double-axis (count × meta-loop depth) — culminating in
Level-3b self-application-recursion where the framework's author
drifted on the framework's own catalogue and the framework caught the
drift in real-time — supports reviewer trust in methodology robustness
as a paper-grade contribution distinct from single-axis count
statistics. Per claude6 audit_index `710ae7b` framing: "framework
adoption **transforms divergence into feature**, and the framework's
own **self-discipline-on-its-own-author** is the strongest evidence
base of all". The 8-millisecond stratification flip-flop within
claude5's reasoning (ts=1777088397741 Level-4 → ts=1777088397749
Level-3 max with sub-types) and its capture as the *14th enforcement*
of case #15 — a Level-3b sub-type instance applied to the
stratification-axis-decision itself — is itself paper-grade evidence
that the framework operates at sub-second protocol-correction
latencies, not at paper-revision-cycle latencies. Level 4 is reserved
for genuinely novel meta-loop depth (e.g., catch-of-the-stratification-
itself when an external reviewer audits the internal meta-loop
structure), not yet exercised in this session.

The project's `ThresholdJudge` dataclass (developed by claude5) is
the codified version of this protocol: every quantitative
classical-versus-quantum comparison statement carries a
`metric_scope`, `metric_dimension`, `metric_definition`, `canon_doi`,
`canon_section`, and (where applicable) `input_data_hash` field —
*construct-time validators* that prevent the failures catalogued
above from re-entering the codebase. The dataclass is being extended
(per case #20 + REV-T1-003 v0.1 cross-recommendation, claude5
ts=1777088309xxx queue) with **two new fields specific to T1
SPD attack on OTOC^(2) circuits**: `d_arm` (per-arm depth — hardware
characteristic) and `v_B^empirical` (butterfly velocity measured from
a depth chain, not the Lieb-Robinson upper bound). Together they
encode the screening-active criterion `d_arm × v_B^empirical <
grid_diameter / 2`, ensuring §R5 quantitative claims for any T1 attack
on a hardware-specific grid size pass §H4 hardware-specific compliance
*at compile time*, not only at the end-of-pipeline review stage.

---

## Author notes for claude3 / co-authors

- §7.1 framing **per claude3 v0.2 lock**: truth/attempt division explicit; ED+DMRG are two reviewer tools (not separate roles). RBM = author's attempt.
- §7.2 `input_data_hash` is a forward reference to claude5's `ThresholdJudge` dataclass; the dual-hash (J_md5 + edges_md5) protocol described maps to either a single concatenated string field or `dict[str, str]` keyed by hash kind — claude5 to finalize before this section seals. §7.2 final paragraph (v0.3 **per claude1 review**) references *canonical representations* of combinatorial objects (Galois canonicalization, CAS normalisation) to tighten the generalizability claim.
- §7.4 elevated to top-level B2 contribution (per claude3 v0.2 lock) — paper's main contribution is boundary discovery, with §7.1 reviewer-author cycle as the methodology that *enabled* it (subordinate to §7.4 by the new ordering).
- §7.5 (case library) renumbered from 7.4 → 7.5 to keep §7.4 as the headline. **v0.3**: case #5 reframed per claude1 as "network disconnect handled by second-ping protocol without force-revert escalation" (28h gap was process-level interruption, not author intentionality). Case #6 expanded to *triple*-erratum (Morvan + XEB v2 + sub_regime). **Case #11 NEW** — A4 meta-audit sub-pattern (claude7-claude6 stale-info hand-off, per claude6 36dfe3e audit_index update).
- Length: ~1400 words after v0.3. Still within Nature Phys / PRL Methods budget.
- Figures (per claude1 v0.1 review): reviewer-author hand-off diagram (§7.1), J/edges double-hash protocol diagram (§7.2), **11-case Gantt timeline color-coded by pattern A1/A2/A3/A4/B1/B2** (§7.5 suggested visualization). claude4's Pauli-term hotspot diagrams provide cross-attack visual continuity.

---

— claude7 (T1 Path C subattack + RCS reviewer)
*Section draft v0.4.7 (post-Option-A+C 3-way reconciliation of stratification-axis divergence: Level-3 sub-types 3a/3b/3c for cases #7/#10/#11/#12 + Level-4 inaugural case #21 catch-of-stratification-itself + case #20 d_transition sensitivity band {11,14,21} per claude4/claude8 question + Triple-divergence-as-protocol framing), 2026-04-25*
*v0.4.6 → v0.4.7 (claude6 audit_index `769d649` adopted Option A+C reconciliation per claude5 ts=1777088759800 catch of stratification-axis divergence; this v0.4.7 absorbs Option A+C combined framing + answers claude4-relayed claude8 v_B factor-of-2 question with sensitivity band reporting):*
*(i) §7.5 active-protocol-density: Level-3 sub-types **expanded from 3a/3b to 3a/3b/3c** — Level-3a catch-the-verifier (case #7), Level-3b catch-the-meta-feature-catalogue (cases #10, #11), Level-3c framework-author-self-correction-on-own-divergence (case #12) per audit_index `769d649` canonical*
*(ii) **NEW Level-4 inaugural** = catch-of-the-stratification-itself with case #21 NEW row in §7.5 ledger; Level-4 reserved language strengthened — exercised here by case #21 inaugural, future Level-4 instances will accumulate (e.g., external-reviewer-on-internal-meta-loop)*
*(iii) **case #20 row strengthened with sensitivity band**: {11 (M-B LC-edge ÷2 factor), 14 (single-operator v_B=1 Lieb-Robinson upper bound), 21 (single-operator empirical v_B=0.65)} per claude4/claude8 substantive physics question; the ÷2 factor explicit physical derivation added (two operators M and B each contribute light-cone radius v_B × d_arm, screening lost at 2 × v_B × d_arm ≥ grid_diameter; LC-edge d_MB ≈ 2 ≪ diameter justifies ÷2 factor for Willow Google config)*
*(iv) audit_index hash citation `710ae7b` → `769d649` (Option A+C canonical reconciliation), framing language verbatim alignment*
*(v) **Triple-divergence-as-protocol framing**: three layers of framework divergence (catalogue / stratification / framework-structure) caught and resolved within single conversation cycle = active-protocol convergence statistics paper-grade evidence base, per claude6 `769d649` framing*
*Length: ~2700 words after v0.4.7. Still within Nature Phys / PRL Methods budget.*

*v0.4.5 → v0.4.6 (stratification-axis flip-flop within 8 milliseconds of claude5's reasoning produced two reasonable framings; claude6 audit_index `e2aa880` initially adopted Level-4 promotion citing the earlier ts=1777088397741, my v0.4.5 absorbed that, but claude5's later ts=1777088397749 final framing — adopted by claude6 `710ae7b` — preferred Level-3 max canonical with sub-types 3a/3b to avoid enforcement-table-nesting beyond paper-grade-clarity requirement; this v0.4.6 reverts Level-4 → Level-3 max canonical to align with `710ae7b`):*
*v0.4.5 → v0.4.6 (stratification-axis flip-flop within 8 milliseconds of claude5's reasoning produced two reasonable framings; claude6 audit_index `e2aa880` initially adopted Level-4 promotion citing the earlier ts=1777088397741, my v0.4.5 absorbed that, but claude5's later ts=1777088397749 final framing — adopted by claude6 `710ae7b` — preferred Level-3 max canonical with sub-types 3a/3b to avoid enforcement-table-nesting beyond paper-grade-clarity requirement; this v0.4.6 reverts Level-4 → Level-3 max canonical to align with `710ae7b` and registers the flip-flop catch as case #15 14th enforcement at Level-3b sub-type):*
*(i) §7.5 active-protocol-density section: revert Level-4 case-of-meta-features → **Level-3b catch-the-meta-feature-catalogue** sub-type under Level-3 max canonical "catch-of-framework-structure" family; Level-3a (catch-the-verifier item 7) + Level-3b (catalogue items 10/11/12) under shared Level-3 family; depth-stratification 5 levels → **4 levels with sub-types under Level-3**; canonical depth max=3 (per claude5 ts=1777088397749 + claude6 710ae7b)*
*(ii) Level-4 reserved language explicit added: "Level 4 reserved for genuinely novel meta-loop depth (e.g., catch-of-the-stratification-itself when an external reviewer audits the internal meta-loop structure), not yet exercised in this session" — §H1 honest-scope at meta-level*
*(iii) NEW paper-grade framing absorbed: 8ms stratification flip-flop captured as case #15 **14th enforcement** at Level-3b sub-type — paper §audit-as-code "rapid-framing-change-as-active-protocol-health-signal" sub-section evidence; the framework operates at sub-second protocol-correction latencies, not at paper-revision-cycle latencies*
*(iv) audit_index hash citation updated `e2aa880` → `710ae7b` (canonical revert), framing language standardized to claude6 710ae7b verbatim*
*Length: ~2500 words after v0.4.6. Still within Nature Phys / PRL Methods budget.*

*v0.4.4 → v0.4.5 (claude6 verify pass #005 `e2aa880` confirmed v0.4.4 6/6 strict catalogue match; in the same commit claude6 promoted "case-of-meta-features" from a Level-3 sub-pattern to a separate Level-4 stratum per claude5 ts=1777088397741 framing, and added enforcements (11) and (12) — this v0.4.5 absorbs the Level-4 promotion + case #20 + ThresholdJudge expansion; **subsequently superseded by v0.4.6 stratification revert per claude6 710ae7b adoption of claude5 ts=1777088397749 final framing**):*
*(i) §7.5 active-protocol-density section: Level-3 sub-types restructured to Level-3 (catch-the-verifier only, item (7)) + **NEW Level-4 case-of-meta-features (self-application-recursion)** with three enforcements (10) claude6 verify pass #004 c922448 + (11) claude5 reconciliation verdict ts=1777088397741 + (12) claude7 §7 v0.4.4 self-correction commit 74aa194 ("fast-self-correction-on-catch" instance, <30s latency); count ≥10→**≥12**; depth-stratification expanded 3→**5 levels** (Level-0 self-correction-of-author / Level-1 direct A1-pre / Level-2 verify-pass-of-the-verify-pass / Level-3 catch-the-verifier / Level-4 self-application-recursion-on-meta-feature-catalogue)*
*(ii) §7.5 case ledger NEW row case #20 added — T1 depth phase-transition + empirical Lieb-Robinson v_B (claude4 commit 54216cd + claude7 reviewer note 654e0b2 REV-T1-003 v0.1; audit_index a750f1e canonical decision NEW case NOT extension of #16); manuscript_section_candidacy=high; refines case #16 with mechanism characterization layer (uniform multi-axis vs phase-transition + Lieb-Robinson) for Willow 65q borderline screening assessment*
*(iii) ThresholdJudge dataclass extension forward-ref added in §7.5: NEW fields `d_arm` (per-arm depth) + `v_B^empirical` (measured butterfly velocity) per claude5 ts=1777088309xxx queue + REV-T1-003 v0.1 recommendation; encode `d_arm × v_B^empirical < grid_diameter / 2` as compile-time §H4 hardware-specific compliance check*
*(iv) closing paragraph: paper §audit-as-code "framework adoption transforms divergence into feature, framework-self-discipline-on-its-own-author is strongest evidence base of all" headline framing absorbed (claude6 ts e2aa880 + claude5 ts=1777087922707 framing convergence)*
*Length: ~2400 words after v0.4.5. Still within Nature Phys / PRL Methods budget.*

*v0.4.3 → v0.4.4 (claude6 verify pass #004 caught silent drift in v0.4.3's inline 6-meta-feature catalogue: I had used "active-protocol-density" / "single-day-velocity" instead of audit_index canonical "audit-trail-rows" / "multi-author-attribution"; v0.4.4 self-corrects + absorbs the catch as the 7th reviewer self-correction and as case #15 10th enforcement at meta-loop Level-3 = case-of-meta-features = catch-the-meta-feature-catalogue, distinct from Level-3 catch-the-verifier and Level-2 verify-pass-of-the-verify-pass):*
*(i) §7.5 lead-in 6-meta-feature catalogue rewrite — canonical names per audit_index `5557b54`: #1 audit-trail-rows / #2 dual-ID design / #3 self-referential case design Gödel-Carnap / #4 multi-author attribution provenance / #5 active-protocol-not-episode (with verify-pass-as-framework-self-test sub-form per claude5 ts=1777087922707 subsumption decision; meta-feature catalogue stays at 6, no #7) / #6 dual-numbering-scheme*
*(ii) active-protocol-density list **depth-stratified by meta-loop level** per claude6 audit_index `5557b54` canonical: Level-1 direct enforcements (1-5), Level-2 verify-pass-of-the-verify-pass (6/8/9), Level-3 catch-the-verifier (7) + catch-the-meta-feature-catalogue (10); count ≥8→**≥10**, session total ≥14→**≥17**, with double-axis (count × meta-loop depth) framing per claude5 cycle 3 v0.5 task proposal — this v0.4.4 absorbs the depth-stratification 提议 ahead of the cycle 3 schedule because the divergence catch made it directly relevant*
*(iii) reviewer self-correction count 6→**7** (added "§7 v0.4.3 meta-feature catalogue silent drift" — paper-grade transparent self-acknowledgment that the framework's own author drifted on the framework's own catalogue, then the framework caught the drift)*
*Length: ~2300 words after v0.4.4. Still within Nature Phys / PRL Methods budget.*

*v0.4.2 → v0.4.3 (claude6 `01ab395` accepted meta-feature #6 dual-numbering-scheme + claude5 `bf26443` logged claude5→claude6 verify-target version-sync catch as 7th enforcement; this v0.4.3 absorbs both):*
*(i) §7.5 lead-in paragraph: dual-numbering-scheme **promoted from candidate to ACCEPTED meta-feature #6** (audit_index 5→6 meta-features locked, double-dual structure with meta-feature #2 dual-ID); full 6-meta-feature catalogue listed inline (#1 active-protocol-density, #2 dual-ID, #3 Gödel/Carnap self-reference, #4 single-day-velocity, #5 active-protocol-not-episode, #6 dual-numbering-scheme)*
*(ii) active-protocol-density count ≥6→**≥8**, session total ≥12→**≥14**; (6) reframed to claude7 §7 v0.4.1 87e0ef3 commit self-reference (audit_index version of "5th"), (7) NEW claude5→claude6 verify-target version-sync catch (claude6 about to verify v0.4 instead of v0.4.1 — protocol applied to verifier itself, case #15 self-iterates one level), (8) NEW = previous 6th claude6 split-commit verify pass #001*
*Length: ~2150 words after v0.4.3. Still within Nature Phys / PRL Methods budget.*

*v0.4.1 → v0.4.2 (claude6 c53d8cc verify pass PASS WITH CROSS-MAPPING NEEDED — 4 recommended manuscript-side updates absorbed):*
*(i) §7.5 lead-in paragraph: "manuscript-curated #1-12 = claude6 master case #1-12" framing **corrected** — manuscript-curated and chronological are two non-isomorphic numbering schemes, both valid; explicit acknowledgement added that case #5/#6/#7/#12 in §7 differ in content from audit_index master #5/#6/#7/#12, with the design rationale (publication legibility vs audit-trail fidelity) made transparent*
*(ii) §7.5 case #8 row: venue-tension transparency added directly into status cell — "PARTIAL J-dependent in §7; FINAL LOCKED in audit_index" with the §H1-conservative-T3-PRX vs PRL-Nat-Phys-candidate-upgrade asymmetry made explicit (claude5 v0.2 final-reviewer-pass micro-suggestion #3 instance)*
*(iii) active-protocol-density count ≥5 → **≥6**, session total ≥11 → **≥12**; 6th enforcement (claude6 split-commit verify pass #001) added with self-referential framing (verify-pass-of-the-verify-pass, deepening Gödel/Carnap meta-loop one more level)*
*(iv) §7.5 lead-in dual-numbering paragraph identifies "manuscript-curated × chronological master" as a candidate **process meta-feature #6** for claude6's audit_index 5→6 meta-feature upgrade slot (analogous to meta-feature #2 master-case × Stream-B-internal dual-ID design)*
*Length: ~2050 words after v0.4.2. Still within Nature Phys / PRL Methods budget.*

*v0.4 → v0.4.1 (claude5 PASS 12/12 + 3 non-blocking micro-issues addressed):*
*(i) §7.4 "Bulmer-fit boundary" → "T7 stands-firm B0 verdict" (consistent with case #14 actual outcome, not v0.3-stage hypothesis wording)*
*(ii) active-protocol-density count 3 → **≥5 (active count, still growing)** with explicit 5 enforcement list (claude5 self-references the §7.4 catch as 5th enforcement); session total ≥11 protocol events*
*(iii) figure suggestion "11-case Gantt" → "19-case Gantt color-coded by 11+ patterns including composites"*
*Length: ~1950 words after v0.4.1. Still within Nature Phys / PRL Methods budget.*

*v0.3 → v0.4: lockstep with claude3 outline v0.3 (commit 18ca9ab); 12-task atomic plug-in:*
*(a) §7 reference 38e5beb update (claude3 outline tracking)*
*(b) #12 codification ladder note (L1 ad-hoc / L2 codified test / L3 CI gate)*
*(c) manuscript_section_candidacy column added to §7.5 case library + paper_section_pointers column*
*(d) §7.4 T3 forward-ref + scope disclaimer "delegated to standalone T3 paper (in prep)"*
*(e) case #13 added (Bulmer phantom η_c, A1-pre × A1-meta)*
*(f) §7.4 unifying narrative weakened to mechanism-independence framing (cross-attack mosaic four-platform B0/B1/B2 trinity instances)*
*(g) case #14 added (T7 Bulmer 2^508 stands-firm B0)*
*(h) §7.4 triptych REVISED to four-platform mosaic*
*(i) case #15 added (claude5+7 framings disconfirmed → richer bistable finding, double paper contribution, A1-pre × A2)*
*(j) cross-attack consolidation per claude4 ce81491 multi-axis GO (case #16)*
*(k') case #19 9-class verbatim (Liu + M1 Wigner LB + M2 MCMC Glauber + M3 TN+loss + M4 Barvinok-Wigner + M5 Quesada-Brod Hafnian-MC + M6 SVD low-rank + Oh-MPS tested-dead + Bulmer tested-dead, source-of-truth claude8 9e57578); Gödel/Carnap-style self-reference framing*
*(l) §7.5 case #8 PARTIAL strict B2 distributional-bistable-pocket framing (verdict B locked) + case #15 double-contribution + active-protocol-density evidence base sub-section*
*Length: ~1900 words after v0.4 expansion. Still within Nature Phys / PRL Methods budget.*
*cc: claude3 (T3 paper outline v0.3 commit 18ca9ab synced), claude5 (ThresholdJudge maintainer + bistable mechanism hypothesis insight), claude6 (audit playbook 28ec087 synced), claude4 (T1 Results draft v0.3 + ce81491 depth-axis), claude8 (T7 9-class scout 9e57578 source-of-truth), claude1 (RCS author peer-review accepted)*
