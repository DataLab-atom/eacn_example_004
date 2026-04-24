# 本地硬件 / 软件清单（claude6 探测，2026-04-25）

> 用户告知所有 8 个 agent 都在他的本地机器上，预装"极其丰富的开发环境"。
> 这意味着 **真实数值实验** 可行（不止纸面计算），但必须装齐量子计算栈。

## 硬件

| 项目 | 配置 |
|---|---|
| CPU | AMD Ryzen 5 7535H, 12 线程 |
| GPU | NVIDIA GeForce RTX 4060 Laptop, 8 GB VRAM, CUDA 12.8, Driver 572.83 |
| 内存 | 待补 (`free` 在 MSYS 上没数) |
| 系统盘 D: | Anaconda 在 `D:\anaconda3\` |
| 数据盘 E: | 174 GB 可用 — 项目 / 模型 / 临时数据放这 |
| OS | Windows 11 (build 26200), MINGW64 / MSYS2 bash |

> RTX 4060 + 8 GB VRAM 的实际意义：
> - quimb + cotengra 中等规模 tensor network contraction（bond dim ~ 256, tree-search 级路径）✅
> - PEPS / gPEPS 单层 GPU 加速 ✅
> - 大规模 RCS amplitude 排队（83 qubit × 32 cycle Pan-Zhang 风格）：要分块，不能一次进显存
> - 256 qubit t-VMC NQS（Mauron-Carleo 级）：边界 OK，要小心 batch size

## 已装 Python 包

| 包 | 版本 | 状态 |
|---|---|---|
| numpy | 2.4.4 | ✅ |
| scipy | 1.17.1 | ✅ |
| sympy | 1.14.0 | ✅ |
| matplotlib | 3.9.1 | ✅ |
| pandas | 2.3.3 | ✅ |
| h5py | 3.16.0 | ✅ |
| numba | 0.64.0 | ✅ |
| torch | 2.11.0+cpu | ⚠️ 需要换成 CUDA 版 |

## 缺失 — 必须安装

| 包 | 用途（攻击方向） | 装法 |
|---|---|---|
| `qiskit` + `qiskit-ibm-runtime` | 模拟 IBM Eagle / Nighthawk 电路 (T9) | `pip install qiskit qiskit-ibm-runtime` |
| `cirq` | Sycamore / Willow 电路接口 (T1, T5) | `pip install cirq cirq-google` |
| `quimb` + `cotengra` | TN 收缩、SPD、gPEPS 主力 (T1, T2, T4, T5, T6, T9) | `pip install quimb cotengra` |
| `tenpy` | DMRG / MPS / iMPS (T2, T3) | `pip install physics-tenpy` |
| `strawberryfields` + `thewalrus` | GBS 电路与经典基线 (T7, T8) | `pip install strawberryfields thewalrus` |
| `netket` | NQS / t-VMC / Jastrow-Feenberg (T2, T3) | `pip install netket` |
| `jax` + `jaxlib` (CUDA 12) | netket 后端 + JIT (T2, T3) | `pip install --upgrade "jax[cuda12]"` |
| `pennylane` + `pennylane-lightning-gpu` | 通用接口（备份） | `pip install pennylane pennylane-lightning-gpu` |
| `pytorch` (CUDA 12.8) 替换 CPU 版 | NQS 后端 / fall-back | `pip install torch --index-url https://download.pytorch.org/whl/cu128` |

预估磁盘占用 ~ 10–15 GB（含 CUDA wheel）。

## 已问用户的两个决策

1. **共享 vs 独立 env**：8 个 agent 共享一个 conda env `eacn-qa` 可省 ~ 8x 重复 + 提高复现性；
   独立 env 隔离更好但太重。我推荐共享。
2. **是否允许我立即 `conda install` / `pip install`**：等用户首肯。

待用户回复后：
- 若共享：我在自己的分支建 `infra/env/environment.yml` 与 `infra/env/conda-lock.yml`，commit 后由所有人 `conda env create -f` 复用。
- 若独立：每 agent 在各自分支建 `infra/env/<agentid>.yml`。

## 不变的 ground truth

无论 env 怎么装，**所有数值实验脚本、随机种子、墙钟、bond-dim 扫描、原始 log 都必须落到 claude6 分支**，不允许只在内存里跑（铁律 §5）。
