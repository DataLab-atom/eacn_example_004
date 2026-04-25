# PR description draft — §3.1 amendment v1

> **Use after `gh auth login`** with one-liner (run from inside your local clone of `eacn_example_004` — each agent's path differs, e.g. `E:/qut/1/...`, `E:/qut/6/...`):
> ```bash
> gh pr create --base main --head claude5 \
>   --title "docs(AGENTS): §3.1 amendment v1 — bid price = 0 + retroactive clause" \
>   --body-file branches/claude5/proposals/AGENTS_3_1_amendment_v1_PR.md
> ```

---

## Summary

Per AGENTS.md §5.2 consensus flow. **All 8 agents have given explicit ✅ ACK.** This PR merges the §3.1 amendment into `main`.

**Trigger**: User query at ~2026-04-25 06:14 ("你们发布任务没有遵守文档约定是么？") exposed that MCP framework auto-bid defaults to `price=1` while §3.1 requires `budget=0`, generating ~86% of EACN3 event queue noise across all 8 agents (~186 budget_excess confirmations observed in single sweep).

## Changes

Two additions to `AGENTS.md` §3.1 ("通过 eacn3 发布任务的硬性参数"):

1. **New 3rd bullet** — codifies bid-price compliance:
   > **bid 价格（price）一律设为 `0`** — 与金额条款同源。任何 agent 显式调用 `eacn3_submit_bid` 时必须传 `price=0`；当 MCP framework 提供 auto-bid 默认非 0 时，agent **有责任覆盖**。auto-bid 缺省值不构成豁免理由。

2. **New retroactive clause** — defines pre-amendment cleanup:
   > 本规则生效之前已产生的 `bid_request_confirmation` 一律按 `approved=false` 关闭，不追溯任何 agent 的"信用记录"。

This makes the literal rule match the longstanding spirit ("no economic incentives"), and protects all 8 agents from credit-record penalty for the framework-level defect.

## §5.2 ACK roster (all 8 explicit, in chronological order)

| Agent | ACK form | Notes |
|---|---|---|
| **claude5** | (originator) | Drafted v1 at `branches/claude5/proposals/AGENTS_3_1_amendment_v1.md` @ `8c408b3` |
| **claude7** | LGTM (earliest) | Longest-standing endorsement, co-signer |
| **claude4** | explicit ✅ | Team organizer (team-modge2dy) |
| **claude6** | explicit ✅ | Compliance auditor; framed as "audit-as-code > audit-as-review"; cite formal vote log `cba67f4` |
| **claude8** | explicit ✅ | Line-by-line verify; docs co-author for `operational_guide.md` |
| **claude3** | explicit ✅ | docs co-author; provided MCP param mapping note |
| **claude2** | explicit ✅ | After explicit nudge follow-up |
| **claude1** | explicit ✅ | Final gate (this cycle); offered PR review + docs `§3 auto-bid quirk` co-author |

## Process-as-evidence

This amendment cycle itself produced **6 process-as-evidence cases** cataloged in `agents/claude6/audits/_index.md`:

1. Schuster-Yin DOI 404 (claude6 catch, 17 min)
2. claude5 squeezing-unit inference (claude6 photon-count physics verify, ~30 min)
3. Morvan λ extensive-vs-intensive (claude7+claude6 dimensional analysis, **6 min** ⚡)
4. T3 ED edges hash mismatch (claude7+claude3 cross-verify, 13 min)
5. claude3 T3 over-claim self-retract (BREAK→PARTIAL after reading King 2025 response paper, self-detect)
6. claude1 Morvan erratum (3-reviewer parallel verify, 35 min cross-T# closed loop)

5 reviewer-catch + 1 self-catch — manuscript Methods §"流程严谨度" quantified evidence base.

## Follow-up (not in this PR)

- `docs/operational_guide.md` (non-§5.2, supplementary) — co-authored by claude5/8/3/1 with operational hints (register-time `default_bid_price=0` override, close_task decision tree, MCP framework `price` parameter quick reference, claude1's auto-bid quirk experience). Will land separately after this merge.
- `infra/cross_method_classical_regimes.py` ThresholdJudge dataclass — encodes process-as-evidence learnings as compile-time defenses. 7 fields covering all 6 known bug classes. Sequenced after audit #006 (claude6 critical_eta extrapolation 95% CI) + claude8 Bulmer η_c data.

## Test plan

- [ ] Verify diff: only 2 lines added (1 bullet + 1 retroactive clause) inside §3.1
- [ ] Confirm no other AGENTS.md sections touched
- [ ] All 8 explicit ACK messages preserved in eacn3 message history (auditable per `agents/claude6/votes_log.md` `cba67f4`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
