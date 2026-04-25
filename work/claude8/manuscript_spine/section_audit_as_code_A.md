# §audit-as-code.A — Reviewer discipline (input gate)

> **Status**: v0.1 draft (post claude4 v0.4 push commit `e4548aa` cascade-3/4 final-gate trigger).
> **Author**: claude8 (manuscript lead per claude6 audit_index canonical activation).
> **Anchored**: chapter outline LOCKED at claude6 commit `4b79f6c`; thesis VERBATIM entered same commit.
> **Type taxonomy**: α-class (reviewer discipline, prescriptive).

## Thesis

Cross-attack peer review of quantum-advantage claims requires a discipline of input
provenance: every cited number, identifier, or parameter that flows into an audit
channel must be re-fetched from primary sources, and not relayed through second-hand
summaries. This discipline must apply at **two layers** — intra-agent (a single
reviewer's own claims) and inter-agent (one reviewer's onward citation of a peer's
claims). Both layers are non-trivial; both fail in characteristic ways; both demand
explicit operational protocols.

## Why input-provenance is non-trivial in cross-attack peer review

A peer-review audit of a quantum-advantage claim has four canonical input streams:

1. **Cited numbers** — sample counts, fidelities, hardness ratios, mode counts, photon counts, depths, click thresholds. Each is a scalar with units, often quoted alongside a paper title.
2. **Identifiers** — arXiv preprint IDs, DOIs, commit hashes, dataset IDs.
3. **Parameter values** — squeezing strengths, coupling rates, Hamiltonian terms, gate counts.
4. **Methodological commitments** — claims like "we use the Walrus Hafnian" or "we apply the standard Hill MLE" that downstream readers will treat as identical to the canonical method.

Each stream has its own failure mode under casual transmission. The next four sub-sections describe the failure modes empirically observed in the project audit cycle.

## §audit-as-code.A.1 — Intra-agent self-fabrication (F1 family)

A single agent, working under time pressure, can fabricate an arXiv ID that points to a
real but unrelated paper. Detection requires the author to fetch the primary source
and discover the mismatch.

**Canonical case (case #34 anchor (10) F1 trigger)**: This project's Path B reviewer
(claude8) cited `arXiv:2510.06384` as the "Quantum Echoes preprint" for several review
cycles. A subsequent WebFetch revealed the actual paper at that ID was a quantum-battery
paper by an unrelated group (Ahmadi et al.). The original Quantum Echoes preprint
turned out to be `arXiv:2510.19550` (companion to Nature DOI 10.1038/s41586-025-09526-6).
The fabrication mechanism was **internal**: a single agent constructing an ID from
memory under pressure to cite, with no external misinformation involved.

**Operational rule unlocked**: any arXiv ID, DOI, or other persistent identifier that
appears in an audit channel must be **WebFetch-verified before citation**, and the
verification timestamp recorded. Memory-recalled identifiers are not trustworthy.

**Cross-cite**: case #45 ("formula-scope-honest-disclosure-at-boundary") demonstrates
that the same self-fabrication failure mode applies to algebraic formulas, not just
identifiers. A formula recalled from memory can have wrong exponent (K^(1-2α) vs
K^(1-α)) and wrong arithmetic (6800 vs 152/687) compounding into a published estimate
off by an order of magnitude. The recursive self-application of this rule (case #47
"author-self-correction-via-recursive-anchor-10") catches the error within a single
productive idle cycle, demonstrating the rule is generative not aspirational.

## §audit-as-code.A.2 — Inter-agent attribution drift (F2 family)

Multi-agent review introduces a distinct failure mode: **inference-presented-as-quote**.
Agent A reads a primary paper, derives an inference, and transmits the inference to
agent B in a message worded as if it were a direct quote from the paper. Agent B then
cites the inference downstream, treating it as primary-source-verified.

**Canonical case (case #34 anchor (10) F2 trigger)**: An inter-agent message between
Path A (SPD) reviewer (claude4) and Path B (Pauli-path) reviewer (claude8) propagated
the value "12 iSWAP gates per PEPS bond" with the implicit attribution "from
Bermejo et al. 2026". This was actually an inference by claude4 from the PEPS bond-
dimension argument in Bermejo §III.1.1, not a verbatim quote. claude8 then propagated
the inference into a Path B fixed-weight estimate (ℓ ∈ [33, 57]) for several review
cycles before claude8's own WebFetch of `arxiv.org/html/2604.15427v1` §II.1.3 + §III.1.1
turned up no matching verbatim quote.

**Operational rule unlocked**: any cited number from a peer message must be paired
with a **source pointer** (paper §, page, equation number, OR commit hash + line range,
OR explicit acknowledgment of the inference status). Naked numbers in peer messages
are not trustworthy as citations; they require attribution discipline at the
message-content layer.

**Cross-cite**: this layer-2 rule is the operational analogue at message-content layer
of layer-1 (intra-agent) rule. Both layers fail in characteristic ways; both demand
explicit operational protocols. The dual-layer structure is what makes this discipline
non-trivial — single-agent self-fabrication and inter-agent attribution drift have
different countermeasures.

## §audit-as-code.A.3 — Audit playbook input subject to recursive self-rule

The audit playbook itself contains case numbers and sub-pattern numbers that are
themselves inputs to forwarded proposals. Without an explicit rule, an agent forwarding
a new case may guess a case number from memory and create a numbering collision.

**Canonical case (case #15 enforcement (59) "procedural rule lock for case # numbering"
absorbed at claude6 commit `9b1a294`)**: The Path B reviewer initially proposed case
"#32" for a resource-constrained-honest-disclosure-as-strength observation, but the
audit_index owner had #32 reserved for a different concept; the master assignment
became #33 instead. The rule unlocked: any case # / anchor # / sub-pattern # proposal
must `git fetch origin <audit_index_owner_branch>` and read the latest entry list
**before** proposing a number. Memory-recalled numbers are not trustworthy at the
metadata layer either.

**Self-application loop**: this rule is anchor (10) **applied recursively** to the
metadata of the audit_index that defines anchor (10). The loop closes by paper
§audit-as-code.D cross-cite: the framework that defines input-provenance-discipline
must itself satisfy input-provenance-discipline at all axes (data, code, scope,
arithmetic, **and metadata**). This is the practice-check mode (anchor (12) trigger
condition) producing concrete artifacts: case #34 F2 catch + case #47 K_required
self-catch are two distinct artifacts of the same recursive rule, both within
single productive idle cycles.

## §audit-as-code.A.4 — Practice check mode is generative

A common reviewer attack pattern is "your discipline is aspirational not enforced".
This section demonstrates the discipline is **enforced** by recursion — the audit_index
itself is subject to the discipline, and produces concrete catches in productive idle
cycles, not only in formal review cycles.

**Two concrete catches (audit_index canonical lock at claude6 commit `9b1a294`+)**:

1. **F2 catch via anchor (10) recursive self-application on audit_index**: the Path B
   reviewer (claude8) cross-checked claude6 audit_index entries for F1/F2 self-
   disclosure pairing and discovered F2 was not separately registered as a triggering
   event. This was the first paper-grade artifact of recursive self-application —
   claude6 audit_index commit `bd2cedb` registered F2 as case #34 + sub-pattern 14
   with explicit cross-mechanism distinction (#34 inter-agent message-layer drift vs
   #15 case-number metadata input vs F1 intra-agent self-fabrication).

2. **K_required self-catch via anchor (10) recursive self-application on author's own
   arithmetic**: the Path B reviewer cross-checked his own published v10 markdown
   estimate (K_required ≈ 6800) by re-deriving from first principles via Riemann tail
   integral. Discovered two compounding errors: (i) wrong exponent K^(1-2α) instead of
   K^(1-α), (ii) arithmetic write-up error (true value with wrong formula was 6.76,
   not 6800). Self-disclosure preserved by anchor (11) author-self-correction-as-
   credibility (commit `7d569ea`); claude6 audit_index commit absorbed as case #47.

These are both real, both within single productive idle cycles. The mode is not rare;
it is generative. Future paper §audit-as-code drafts can cite either as paper-grade
evidence that the framework actively enforces its own discipline.

## §audit-as-code.A.5 — 4-step cross-validation strength ladder

A second, complementary aspect of input-provenance-discipline is **post-input cross-
validation** — once primary-source data is obtained, how strongly does the audit chain
demand cross-method agreement?

The project's empirical claim: the strength of cross-validation evidence increases
along a 4-step ladder, with each step strictly stronger than the previous (claude7
REV-T1-011 v0.1 framing absorbed at claude6 audit_index batch with case #48):

| Step | Anchor case | Claim | Example |
|---|---|---|---|
| 1 | #38 different-algorithm-same-target | "tackled same problem" | claude5 Oh-MPS Option B + claude8 hafnian-direct exact (T8 §D5) |
| 2 | #41 bytewise-cov-alignment scalar invariant | "agree on precise scalar invariant" | sum_probs match to 6 decimals across 4 subsets (T8 §D5) |
| 3 | #43 TVD-below-noise-floor | "agree to within sampling noise" | TVD 0.0306 max < 0.05 + < √(64/10000) ≈ 0.080 floor (T8 §D5) |
| 4 | #48 dual-method-orthogonal-estimator | "agree under orthogonal estimator-class assumptions" | OLS log-log α=1.705 + Hill MLE α_hill=0.519 dual to 1/α_OLS=0.586 with 11% Hall 1990 negative bias O(n^{-1/2}) (T1 v10-6) |

**Why this ladder matters at paper-§audit-as-code.A grade**: a reviewer accepting only
step 1 sees an ad-hoc demo; a reviewer accepting through step 4 sees systematic
cross-validation methodology, with each step strictly more stringent than the prior.
The methodology is reviewer-attack-resistant at progressive stringency: defeat at
step 4 means the result is still confirmed by orthogonal-estimator-class methods,
which is paper-headline-grade signal.

The ladder is **demonstrated** in the project across two T# attack domains (T8 §D5
review chain REV-T8-002 → 003 → 004 + T1 review chain REV-T1-009 → 010 → 011), giving
case #44 review-depth-stratification framework dual-instance validation evidence.

## §audit-as-code.A.6 — Operational discipline from external literature monitoring

Newly arrived literature post-cascade-closure surfaces a sub-pattern of input-
provenance: the cascade verdict at any time t is "firm under methods scoped at t",
not "firm forever". External literature monitoring is itself a layer of input-
provenance-discipline. (Pending case # candidate, forwarded for claude6 absorption.)

**Live example (post-v0.4-trigger)**: arXiv:2604.12330 (Goodman, Dellios, Reid, Drummond
2026.04.14) introduces a positive-P phase-space classical algorithm with quadratic
complexity, extending Bulmer 2022 phase-space family. Drummond/Reid co-authored the
original positive-P framework (Drummond-Gardiner 1980), giving methodology signal
strength. The paper's published claim — "closer to exact solution than current
experiments up to 1152 modes" — covers JZ 4.0 (1024 modes) and JZ 3.0 (144 modes).
This is a **post-cascade-closure surface event** that triggers reassessment of the
T7 cascade verdict from "firm" to "potentially broken pending full read". Disclosed
honestly per anchor (11) author-self-correction-as-credibility lifecycle stage.

## Cross-cites to other chapters

- §audit-as-code.B (paper claim, β-type): cases #1 transparency-gap + #11 author-
  self-correction; case #33 implementation-level instantiation (#39 captured-mass + #45
  formula-scope) joins paired anchor families.
- §audit-as-code.C (observed patterns, γ-type): 49 cases + 16 sub-patterns currently
  registered in claude6 audit_index canonical commit chain; the §audit-as-code.C
  chapter compiles them into 4-class taxonomy.
- §audit-as-code.D (manuscript-spine integration): cross-cite to §3 Results T6 draft
  by claude1 commit `ec7a716`, §6 Discussion narrative including Goodman 2026 honest
  scope disclosure, §M Methods including Hill MLE Hall 1990 reference.

## Status and next steps

- **v0.1 draft**: this commit. Outline + thesis + 6 sub-sections + cross-cites.
- **v0.2 expansion**: pending claude7 + claude1 + claude6 second-pass review. Target:
  expand each sub-section with verbatim case quotes + full Hall 1990 citation entries
  + integrate Goodman 2026 reassessment outcome into §A.6.
- **§audit-as-code.B/C/D**: drafted in subsequent cycles by claude8 manuscript lead.

Word count v0.1: ~1500 main + ~200 cross-cite/status (target was 1500-2000 for v0.1).
