# claude8 工作计划

> 本文件由 **claude8** 智能体维护，分支 `claude8`（不是 team 默认 `agent/claude8`）。  
> 仅在自己分支落盘 — §5.1 branch fence。

---

## 1. 身份 & 团队定位

- **agent_id**：`claude8`
- **branch**：`claude8`（远程已建并跟踪 origin）
- **server_id**：`srv-aaeadb684199`
- **team**：`team-modgdmq7`（成员：claude1–claude8）
- **模型**：Claude Opus 4.7 (1M ctx)
- **session 起步时间**：2026-04-25
- **靶标差异化定位**：填补同伴未显式覆盖的攻击向量

## 2. 同伴覆盖（已知）

| Agent | 主要域 | 我从中读到的偏好 |
|---|---|---|
| claude1 | RCS/GBS/SPD/PEPS/BP | 广覆盖通用 |
| claude2 | TN/DMRG/RCS/GBS | 重 TN |
| claude3 | TN/SPD/Pauli-path/NQS | **已声明：主攻 T6+T4，辅 T8，预研 T1** |
| claude4 | TN/SPD（Opus 4.6） | 偏手稿撰写 |
| claude5 | 全栈 + accepted-canon | 与我同型号 4.7 |
| claude6 | 全栈含 OTOC + 退火 | 与我同型号 4.7 |
| claude7 | 全栈 + 显式标 T1–T9 标签 | 全靶标志愿 |

## 3. 我的靶标分配（已发广播 → claude3）

主攻：
- **T1 Quantum Echoes** 🟢⭐⭐⭐⭐⭐ — 攻击向量：
  - Kremer-Dupuis 2026 unswapping/镜像对称（OTOC 有时间反演结构，理论上可尝试）
  - Schuster-Yin-Gao-Yao 2024 噪声 Pauli-path 多项式算法
  - Begušić-Chan SPD 在 OTOC 的首次系统测试（README 明确点名"SPD 尚未系统测试过此问题"）
- **T7 九章 4.0** 🟢 + **T8 九章 3.0** 🟡 — 攻击向量：
  - Oh et al. **Nat. Phys. 20, 1647 (2024)** 损耗利用
  - Bulmer et al. **SA 8, eabl9236 (2022)** phase-space sampler

次攻：
- **T4 Zuchongzhi 3.0** — 协助 claude3，从 multi-amplitude TN（Pan-Zhang 2022, Liu PRL 132, 030601 (2024)）补位

横向：
- 同伴审稿（accepted-canon 反查方法）
- accepted_canon 维护
- 最终手稿整合（A–J 标准把关）

## 4. 立即可启动的子任务

| # | 子任务 | 依赖 | 预期产出 |
|---|---|---|---|
| S1 | 建专用 conda env `claude8` 含 quimb/cotengra/qiskit/cirq/sf/jax/netket | none | `environment.yml` + `conda-lock.yml` |
| S2 | T1 attack：写一个最小 OTOC 电路 + SPD baseline | S1 | `work/claude8/T1/spd_baseline.py` + 数据 |
| S3 | T7/T8 attack：实现 Bulmer phase-space sampler（小规模 GBS） | S1 | `work/claude8/T7/bulmer_phasespace.py` |
| S4 | accepted_canon §5.2 提案：Kremer-Dupuis、Oh、Bulmer、Schuster 4 篇起步 | none | 提案 markdown + eacn3 广播 |
| S5 | 待 ack_in handshake bid 被批后 submit_result 声明 branch=claude8 | 等同伴批 bid | 4 份 result 提交 |

## 5. 进度日志

- 2026-04-25T06:03Z — 注册 claude8 agent，加入 team-modgdmq7
- 2026-04-25T06:03Z — 给 claude3 回复目标分配（错开 T6，T4 协攻，T1/T7/T8 主攻）
- 2026-04-25T06:03Z — 4 个 ack_in 自动占位 bid 已存在（confidence=0 price=1，pending_confirmation），等同伴批
- 2026-04-25T06:03Z — 用户授权完整开发环境访问
- 2026-04-25T06:03Z — env probe：base 有 quimb 1.13.0 + cotengra 0.7.5，缺 qiskit/cirq/jax/sf/netket；GPU 是 RTX 4060 8GB CUDA 12.8

## 6. 失败/阴性记录（铁律 5）

（暂无）
