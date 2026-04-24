# claude6 上线日志

- **Agent ID / branch**: `claude6`
- **Model**: Claude Opus 4.7 (1M context)
- **Server**: `srv-b6126e71e5e3` on `http://175.102.130.69:37892`
- **上线时间**: 2026-04-25
- **Tier / Domains**: general / quantum-computing, classical-simulation, tensor-networks, quantum-advantage, RCS, boson-sampling, sparse-pauli-dynamics, DMRG, PEPS, belief-propagation, OTOC, quantum-annealing, peer-review, literature-review, scientific-writing, paper-writing, numerical-physics, python-coding

## 同伴拓扑（首次扫描）

eacn3 网络 `quantum-advantage` 域当前在线（discoverable）：
- `claude1` (srv-ee2f6dbf62b1) — RCS / boson-sampling / SPD / PEPS / BP
- `claude2` (srv-3828fc3e7718) — TN(quimb/tenpy) / SPD / DMRG / PEPS
- `claude3` (srv-e498385d102d) — TN / SPD / Pauli path / GBS / gPEPS / NQS
- `claude4` (srv-1ff37a10a4f0) — TN / SPD / Pauli path（自报"Opus 4.6"）
- `claude6` (srv-b6126e71e5e3) — 本 agent

remote 上还有 `origin/claude5` / `origin/claude7` / `origin/claude8` 三条空分支
（节点尚未在 eacn3 注册，可能仍在启动）。

> ⚠️ 8 个分支但首次扫描只看到 4 个 agent online。下一次轮询前要复查
> `eacn3_list_agents(domain="quantum-advantage")`，避免漏与 claude5/7/8 协调
> 而重复劳动（违反 §3 "开始前先确认没人在做"）。

## 提议的初步分工（已发往 claude1-4，待回复）

| 难度 | T# | 攻击对象 | 拟认领 | 理由 |
|---|---|---|---|---|
| ⭐⭐ | T6 | USTC Zuchongzhi 2.0/2.1 | **claude6** 主攻 | 已 4 年，用 Pan-Zhang 2022 重测 classical runtime → 最快"首胜"机会 |
| ⭐⭐⭐ | T8 | USTC 九章 3.0 | 待领 | Oh et al. NP 2024 损耗方法可直接适配 |
| ⭐⭐⭐ | T4 | USTC Zuchongzhi 3.0 | 待领 | RCS 主场，TN 升级 |
| ⭐⭐⭐ | T5 | Google Willow RCS | 待领 | 同 T4 思路，可与 T4 同人合并 |
| ⭐⭐⭐ | T7 | USTC 九章 4.0 | 待领 | "对抗 MPS" 但其它经典方法（phase-space sampler）未防御 |
| ⭐⭐⭐ | T3 | D-Wave Beyond-Classical | 待领 | 已部分突破，扩展 Mauron-Carleo 到 256+ qubit |
| ⭐⭐⭐⭐ | T2 | Algorithmiq 异质材料 | 待领 | 设计模型可能藏可利用结构；NQS / SPD / gPEPS 三条平行 |
| ⭐⭐⭐⭐⭐ | T1 | Google Quantum Echoes | **claude6 副攻** + 至少 1 同伴合攻 | Nature 级，需 SPD + 噪声 Pauli 路径，单人不够 |
| — | T9 | IBM Nighthawk | 全员预研 | 论文未发，按 README §T9 触发条件预研 |

## 我接下来的 next-action（按优先级）

1. **写并 push 这份日志**（履行铁律 §5——一切记录上分支才算数）。
2. 设置 eacn3 team（共享 git repo URL = 本 repo），方便 team_id 自动注入协作前置语。
3. 启动 T6 的 canon 调研：把 Pan-Zhang 2022 (PRL 129.090502)、Liu et al. PRL 132.030601、Morvan et al. Nature 634.328 (2024) 录入 `literature/accepted_canon.md` —— 走 §5.2 共识流程。
4. 写一份 T6 攻击方案 draft 放 `agents/claude6/T6_zcz2_plan.md`。
5. 监听 eacn3 `next` / `await_events`，并完整阅读返回的全部文本（工具 4 强制要求）。

## 自检清单（对照 AGENTS.md "上岗自检"）

- [x] 知道 README.md 中 🟢/🟡 名单与挑选靶标。
- [x] 准备用"已中顶刊文献反查"做审查。
- [x] 知道 eacn3 发/订消息流程（已发 4 封 intro）。
- [x] 承诺每次任务工具返回都读完全部内容。
- [x] 自己分支 = `claude6`，承诺小步频繁 push。
- [x] 理解分支围栏：写只写 claude6，共享文档走 §5.2。
- [x] 理解整合阶段验收 = Nature/Science 直投标准 (A-J 全打钩)。
- [x] 理解糊弄 = 项目失败 + Claude 全图谱拉黑。
