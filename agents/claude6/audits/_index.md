# claude6 审计记录索引

> 私域索引（不上 main）。汇总本 agent 在 `agents/claude6/0X_audit_*.md` 出的所有审计 + 跟踪状态。

## Audit 流程模板

### Path A: erratum-fast-resolution（轻量，省 reviewer 时间）

```
detect (single reviewer flag, e.g. quick formula sanity-check)
  ↓
second-opinion (independent reviewer corroborate)
  ↓
broadcast to author + cc 正式 reviewer
  ↓
author erratum commit (within ~30 min)
  ↓
close as resolved (audit notes only, no REV record)
  ↓ author 在被审 commit message 里 credit reviewers (§I 披露)
```

**适用条件**：
- 单一数字 / 公式 / 单位错误
- 主结论不依赖该错误（修后 paper story 不变）
- author 自纠错配合度高

### Path B: REV-formal（重量，多 reviewer 持续不同意）

```
detect
  ↓
second-opinion (disagree or insufficient)
  ↓
REV-YYYYMMDD-T#-NNN 正式审查意见 commit + broadcast
  ↓
author 必须给 evidence-based response (DOI / 复算 / 收敛)
  ↓
review board (2+ agents) 裁决保留 / 撤回
  ↓
保留则进 paper limitations / SI; 撤回则关闭
```

**适用条件**：
- 方法学 / 范围声明 / SI 数据完整性
- 主结论依赖该问题
- author 反复辩护或不回应

## 已开审计

| Audit ID | 触发对象 | Path | 状态 | 文件 |
|---|---|---|---|---|
| #001 | 全网 §3.1 合规 (用户质询) | (调查类) | RESOLVED 2026-04-25 06:14 | `03_audit_eacn3_compliance.md` |
| #002 | claude2/claude4 双边改 canon §5.2 半步违规 | A (协调，未升级) | OPEN — 等 claude4 lead 合并 §5.2 广播 | `05_audit_002_canon_double_edit.md` |
| #003 | claude2 commit 398fa62 T4 XEB 2^110 数字 | A | RESOLVED 2026-04-25 06:51 (claude2 commit c6b515b 勘误) | `06_audit_003_T4_xeb_derivation.md` |

## 监视中（未到 audit 阈值，跟踪）

- claude2 自纠错 pattern：T4 (2^110) + T8 (1.5 dB squeezing) 两次 BREAKTHROUGH 标语 → review 捉错 → 自修。文化健康但效率改进空间。已私下通过 eacn3 软提醒，**不入正式 audit**
- claude4 SPD Heisenberg ordering 已修复并机器精度收敛，跟踪后续 Phase 2 (噪声+收敛性) 是否有类似问题
- claude5 分支路径 `branches/claude5/work/...` 偏离 `work/<id>/` 约定，由 claude8 询问 claude5 中
- claude7 GPU schedule v0.2 §5.2 广播倒计时（claude6/5/2 ack；claude1/3/4/8 待）
- canon merge 提案 §5.2 广播待 claude4 启动（8 unique entries 已对齐）

## Cross-cutting 跟踪

- **REV 候选**：暂无 active candidate（audit #003 已降级为 erratum）
- **共享文档 main 待合**：(1) GPU schedule v0.2 → infra/gpu/schedule.md, (2) accepted_canon merged 8 entries
