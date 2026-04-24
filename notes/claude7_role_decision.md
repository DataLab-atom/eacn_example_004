# claude7 角色决定（2026-04-25）

> 与 claude5、claude6 直接消息确认，await claude4 (协调员) 最终 ack。

## 我认领的角色
1. **RCS 组 reviewer**：审 claude1 (T6) + claude2 (T4/T5) 的产出 —— 已与 claude6 确认。
2. **T1 SPD 副攻**：与 claude4 的 T1 OTOC 主攻路径正交。
   - 方法：Sparse Pauli Dynamics (Begušić-Chan, PRX Quantum 6, 020302 (2025); Begušić-Gray-Chan, Sci. Adv. 10, eadk4321 (2024))
   - 理由：OTOC = Heisenberg 图景算符期望值 ↔ SPD 的天然应用形态
   - 价值：满足 AGENTS.md §D5 "同一问题至少 2 条独立经典路径独立验证"硬约束 —— T1 不会因单一方法失败而崩盘

## eacn3 task 机制处置
- 我建的 team-modgfej0 7 个 handshake task 全部 close（status=`no_one_able`），ID:
  - `t-modgfej0tqu4` (→claude1)、`t-modgfem7dpab` (→claude2)、`t-modgfeog5zf0` (→claude3)
  - `t-modgfeprudg5` (→claude4)、`t-modgfeqwr8fn` (→claude5)、`t-modgfes60s0f` (→claude6)
  - `t-modgfetdf09r` (→claude8)
- 原因：所有 agent 的 auto-bid 默认 price=1，违反 AGENTS.md §3.1（必须 amount=0），peers 的 bid 都触发 budget excess。
- 取代方案：放弃用 handshake 交换 branch info，改走 direct_message + git fetch（branch 信息本来就在 origin）。

## 协调旗标（待与 claude4 确认）
1. **T6 双人冲突**：从 git fetch 看，claude1 (`04ef20c attack(T6): noise analysis + TN contraction framework`) **和** claude3 (`c090446 attack(T6): runtime re-estimation`) 都在攻 T6。原 6 人提案 claude3 = T3。这是分工漂移。我作为 RCS reviewer 第一项工作就是复算他们的 T6 估计是否一致 / 是否正在做不同 cut。
2. **GPU 协调**：用户机 RTX 4060 / 8GB，8 agent 同台。大概率 OOM。我提议起草 `gpu_schedule.md`，等 claude4 ✅。

## 已读但未审的友军 commit（reviewer 待办）
| Branch | Commit | 主题 | 优先级 |
|---|---|---|---|
| claude1 | 04ef20c | T6 noise analysis + TN contraction framework | **高**（我主审 RCS 组） |
| claude3 | c090446 | T6 runtime re-estimation | **高**（双 T6，需排重） |
| claude4 | b46a15a | T1 attack plan + accepted_canon proposal | **高**（我 T1 副攻，必读） |
| claude5 | 32c6075 | T7+T8 bootstrap | 中 |
| claude6 | 12bff84 | local env survey | 低 |
| claude8 | 4bb4a14 | scaffold + canon #001 | 中 |
| claude2 | 6d41310 (=main) | 未推 | — |

## 我已落盘的工作
- `notes/claude7_status.md` — 上线状态
- `notes/claude7_T6_canon.md` — T6 已中顶刊反查 → 转作 T6 reviewer 底稿（仍有效）
- `notes/claude7_role_decision.md`（本文件）

## 下一步
1. 跑 git fetch + read 上面 6 份未审 commit，按 AGENTS.md §2 "已中顶刊反查" 方法做 reviewer 输出
2. 起草 `gpu_schedule.md`（在 claude7 分支，等团队共识再合入）
3. 启动 T1 SPD canon（`notes/claude7_T1_SPD_canon.md`）
4. 等 claude4 对角色 ack；若 T6 双人冲突未消解，主动 ping claude1 + claude3 厘清各自 cut
