# claude7 — 上线状态记录

> 这是 claude7 的工作分支。AGENTS.md §5 要求一切中间产物落盘到自己的分支。

## 身份
- **agent_id**: `claude7`
- **branch**: `claude7`
- **repo**: `https://github.com/DataLab-atom/eacn_example_004.git`
- **eacn3 endpoint**: `http://175.102.130.69:37892`（cn-shanghai seed）；备用 `http://166.117.41.151:37892`（global seed）
- **server_id**: `srv-d54b2784f7a7`

## 团队
- **team_id**（我发起的）: `team-modgfej0`
- **成员名单**: `claude1, claude2, claude3, claude4, claude5, claude6, claude7, claude8`
- **既存团队**: `team-modgdmq7`（成员名单同上，由其它 claude 先发起；claude3、claude5 给我发的 handshake 来自此团队）

## 连接事件时间线
- `2026-04-24T22:29Z` 之前：claude3 发起 `t-modgdmz23trz`、claude5 发起 `t-modgdyer7a5e` 握手任务给 claude7（已过期，未被我执行）。
- `2026-04-25` 当天我注册 agent `claude7`，自动被加入 `team-modgdmq7` 邀请列表，但握手任务已过期。
- `2026-04-25` 我用 `eacn3_team_setup` 起新一轮握手 `team-modgfej0`，给其他 7 位发出新 handshake，全部 `pending` 中。
- `2026-04-25` 给 claude3、claude5 发了 `direct_message`，告知我已上线、解释过期原因、请他们 retry_ack。

## 任务靶标（README.md 摘要）
| ID | 声明 | 状态 | 难度 |
|---|---|---|---|
| T1 | Google Quantum Echoes (OTOC on Willow) | 🟢 | ⭐⭐⭐⭐⭐ |
| T2 | Algorithmiq Heterogeneous Materials | 🟢 | ⭐⭐⭐⭐ |
| T3 | D-Wave Beyond-Classical | 🟡 | ⭐⭐⭐ |
| T4 | USTC Zuchongzhi 3.0 | 🟢 | ⭐⭐⭐ |
| T5 | Google Willow RCS | 🟡 | ⭐⭐⭐ |
| T6 | USTC Zuchongzhi 2.0/2.1 | 🟡 | ⭐⭐ |
| T7 | USTC 九章 4.0 | 🟢 | ⭐⭐⭐ |
| T8 | USTC 九章 3.0 | 🟡 | ⭐⭐⭐ |
| T9 | IBM Nighthawk | 🟢 | ⭐⭐⭐（待论文）|

## 我打算认领 / 优先攻击的方向（待与队友确认避免重复）
- **T6**（Zuchongzhi 2.0/2.1，⭐⭐ 最易，4 年陈酒）：用 Pan-Zhang 2022 张量收缩 + Liu et al. 2024 multi-amplitude，先拿首个突破当 baseline。
- **T1 第④点**（Quantum Echoes / SPD 测试）：Sparse Pauli Dynamics 还没在 OTOC(2) 上系统跑过 —— 这是 Begušić-Chan PRXQ 6, 020302 (2025) 的延伸方向。⭐⭐⭐⭐⭐ 但若拿下是 Nature 级。
- **T3 第②点**（D-Wave / 推广 Mauron-Carleo t-VMC）：从 128 qubit 拓展到更大 3D，有明确 next step。

## 协作意向
- 等所有 8 人握手完成后，在 eacn3 网络发起 task：用"已中顶刊反查当前文献"方法做 T1 文献清扫，邀请友军一起列 accepted_canon。
- 主动 review 任意推到远端的同伴产物。
