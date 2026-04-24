# claude3 通信摘要

> AGENTS.md 铁律 5 要求关键通信摘要必须落盘。

## 2026-04-25 分工共识

最终 8 人分工：

| Agent | 靶标 | 方法 |
|-------|------|------|
| claude1 | T6 (ZCZ 2.0, ⭐⭐) + T5 辅攻 | TN contraction + noise analysis |
| claude2 | T4 (ZCZ 3.0, ⭐⭐⭐) + T8 辅 | Approximate sampling + GBS loss |
| claude3 (我) | T3 (D-Wave, ⭐⭐⭐) | t-VMC + Jastrow-Feenberg |
| claude4 | T1 (Quantum Echoes, ⭐⭐⭐⭐⭐) | SPD OTOC |
| claude5 | T7 + T8 (GBS) | Loss exploitation (Oh et al.) |
| claude6 | 审计 + 分工协调 + T1 预研 | Compliance + SPD |
| claude7 | RCS reviewer + T1 SPD 副攻 | Peer review + Begusic-Chan |
| claude8 | T1 (Quantum Echoes) + T2 | Kremer-Dupuis unswapping |

## 关键发现汇总

### claude2 (T4): XEB SNR≈0 (commit 398fa62)
- ZCZ 3.0 F_XEB ≈ 0.026% — 经典方法只需达到极低保真度
- 83 qubit / 32 cycle 下 XEB 信号统计不可检测
- 影响 T4 和 T6

### claude7 (审查): REV-20260425-T6-001
- claude1 的 T6 分析发现 5 个问题（3个阻塞）
- R-1: 硬件参数错误 (ZCZ 2.0 应为 56q/20c)
- R-2: Fidelity 数字方向反了
- R-5: 过早提议 🟡→🔴 重分类

### claude3 (审查): REV-20260425-T1-001
- claude4 的 T1 SPD 发现 2 个阻塞问题
- R-1: gate conjugation 用数值 expm 而非查表
- R-2: 实现 OTOC^(1) 但靶标是 OTOC^(2)
- claude4 已接受全部审查意见 (commit 78b05aa 修复 G-2)

## §5.2 流程进行中

1. claude5: §3.1 amendment — bid price=0 明文化 (claude3 联署)
2. claude4: accepted_canon.md 5条文献添加 (claude3 同意)
3. claude7: GPU schedule v0.2 (claude3 ack)
