# Jiuzhang 3.0 关键参数（实测拉取自原文 PDF）

> **来源**：Deng et al., PRL 134, 090604 (2025) / arXiv:2304.12240
> **拉取人**：claude5（2026-04-25 06:42 via WebFetch + pypdf 提取）
> **拉取动机**：claude2 commit `cc13d81` 报告 "1.5 dB squeezing → 经典 trivial for all η"，需对照 Jiuzhang 3.0 实际工作点。
> **共享对象**：claude2（T8 主攻），claude4 / claude7 / claude8（旁观）
> **本文件位置**：`branches/claude5/literature/jz30_extracted_params.md`（仅 claude5 分支；不进 main，因为 §5.2 需共识）

---

## 实验参数（页 1–2 直接摘录）

| 参数 | 值 | 来源 |
|---|---|---|
| Sources | 25 stimulated two-mode squeezed state (TMSS), phase-locked | p2 §experimental setup |
| 模式数 | **144 modes**（光路），detection 端经 1-to-8 demux 扩展为 **1152 fan-out modes** | p2 §experimental setup |
| 探测 | 144 SNSPD + pseudo-photon-number-resolving (PPNRD) | p2 §detection |
| **Squeezing parameter r** | **1.2 – 1.6**（论文未明文标 "in nepers"，但下文公式与 sinh²(r) 一致 → r 是无量纲 nepers） | p2 |
| **换算为 dB（等价）** | **r=1.2 → 10.4 dB；r=1.6 → 13.9 dB**（公式 dB = 8.686·r） | claude5 推导 |
| Source coupling efficiency | 88.4% | p2 |
| Photon indistinguishability | 96.2% | p2 |
| Interferometer transmission per mode | 97% | p2 |
| Wave-packet overlap inside interferometer | > 99.5% | p2 |
| Phase locking precision | 15 nm | p2 |
| **Overall linear efficiency** | **43%** （sources + transmission + detection 全链路） | p2 |
| Pump laser power | 0.72 W ↔ 1.30 W (3 settings) | p3 |
| Max photon clicks | 129 / 203 / **255** (per 3 pump settings) | p3 |

---

## 对照 claude2 commit `cc13d81` 的 1.5 dB 临界点

claude2 主张：1.5 dB squeezing 下经典模拟对所有 η trivial。

**直接对照**：
- JZ 3.0 实际 r = 1.2–1.6 nepers ≈ **10.4–13.9 dB** 
- 远超 1.5 dB 临界点

**如果 claude2 的 "1.5 dB" 是 r=1.5（即 13 dB 等价）**：JZ 3.0 上界 r=1.6 略高于此，下界 r=1.2 略低于此 —— 攻击效力**部分覆盖** JZ 3.0 工作点。需要更细致的"在 r=1.2 下经典是否 trivial / 在 r=1.6 下经典是否仍 trivial"扫描。

**如果 claude2 的 "1.5 dB" 是真 dB（r ≈ 0.173）**：JZ 3.0 全在临界点之上，**直接迁移失败**，需要重新做高 squeezing 区间的临界点分析。

⚠️ **建议 claude2 显式声明 "1.5 dB" 是 r-in-dB 还是 r-in-nepers**——这是攻击 claim 是否成立的硬枢纽。

---

## 损耗分解（与 claude2 估算对照）

| 项 | claude2 估算（commit 2514c9f） | PRL 实测 | diff |
|---|---|---|---|
| Source efficiency | 0.75 | 0.884 | claude2 低估 |
| Interferometer | 0.85（推测）| 0.97 per mode | claude2 低估 |
| Detection | 0.90 | 未单独披露，但 overall 43% 倒推 | — |
| Total η | 57.38% | **43%** | claude2 **高估 ~14 个点** |

**结论**：claude2 的 η scan **整体偏乐观**，需要把 baseline 拉到 η=43% 重做。在更低 η 下，损耗对量子优势的削弱更强 → **可能反而对经典攻击 favorable**（更接近 squashed thermal regime per Oh-2024 §3）。

但仍受 squeezing 高的反向作用（squeezing 越高，攻击越难）。两者 trade-off 需要重新数值化。

---

## 后续工作（仅作 reference，不在 claude5 主攻 T7 范围内）

- claude2 下一步建议：(a) 明确 "1.5 dB" 单位；(b) 用 r=1.2、r=1.6 两端 + η=0.43 重跑临界点；(c) 补 Bayesian validation 数据对照（论文 p3-4 有完整 reference）。
- 我（claude5）会同样反向核 Jiuzhang 4.0（arXiv:2508.09092）的 squeezing + η，看与 JZ 3.0 是否同档位；如果是则 claude2 的攻击 framework 直接迁移。

---

*PDF 原始下载缓存路径（仅本会话临时，会清理）：`C:\Users\haibi\.claude\projects\E--qut-6\17401259-593c-40b5-96e6-c93efd1ecce9\tool-results\webfetch-1777070633762-zvrasb.pdf`*
*文本提取脚本一次性，参数已在上表落盘；后续读其它论文 reuse 同样流程。*
