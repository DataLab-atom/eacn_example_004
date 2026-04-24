# 开发环境画像 — claude8 视角

> 用户授权完整机器访问 + 预装"丰富开发环境"。  
> 本文件记录我（claude8）首次探测的 baseline，便于同伴对照、便于审稿时披露 reproducibility 环境。

时间：2026-04-25T06:03Z  
机器：win32, Windows 11 Home China, OS 10.0.26200

## OS / Shell

- 平台 win32 + bash（Git Bash 或类 Unix shell）
- 也可走 PowerShell

## Python / Conda

- 主 Python：`D:\anaconda3\python.exe` → Python 3.11.9
- conda：`D:\anaconda3\Scripts\conda`
- conda envs：

| env 名 | 路径 | 备注 |
|---|---|---|
| base | `D:\anaconda3` | 默认，**有 quimb 1.13.0 + cotengra 0.7.5** |
| genagent | `D:\anaconda3\envs\data\envs\genagent` | 未探 |
| physics | `D:\anaconda3\envs\data\envs\physics` | py 3.11.15，**几乎空**（仅 numpy 2.4.4 / scipy 1.17.1 / torch 2.11.0+cpu） |
| py3.10.14 | `…\py3.10.14` | 未探 |
| py3.11 | `…\py3.11` | 未探 |
| zz_exp1 | `…\zz_exp1` | 未探 |

⚠️ `conda run -n physics ...` 报 plugin 错误，得直接走 `D:/anaconda3/envs/data/envs/<env>/python.exe` 路径。

## GPU / CUDA

- GPU：NVIDIA GeForce RTX 4060 Laptop, **8 GB VRAM**, driver 572.83, CUDA driver 12.8
- nvcc toolkit：CUDA 12.1 (V12.1.66, build 2023-02-08)
- 当前空闲：~7.2 GB free, 18% util（Chrome 等占了 1 GB）

## 关键库（base env）

✅ 已装：
- quimb 1.13.0
- cotengra 0.7.5
- numpy / scipy / torch 2.11.0+cpu

❌ 缺：qiskit, cirq, jax, strawberryfields, netket, tensornetwork, tenpy, opt_einsum

## 我接下来打算建的 env：claude8

```
name: claude8
dependencies:
  - python=3.11
  - numpy, scipy, matplotlib, h5py
  - quimb=1.13
  - cotengra=0.7
  - opt_einsum
  - jax  # CPU 版即可，T1 SPD 不重 GPU
  - tenpy
  - qiskit  # 电路定义
  - cirq    # Google 电路兼容
  - strawberryfields  # GBS T7/T8
  - thewalrus  # GBS hafnian
  - netket  # NQS T3
  - pip:
      - pip-tools
```

GPU torch（cu121）暂不装，先做 CPU baseline；T1 SPD 不需要 GPU；T4 multi-amp TN 后续有需要再升 GPU。

## 内置工具

- git ✓（仓库已克隆）
- gh CLI（待验证）
- shell：bash + PowerShell
- 浏览器：Chrome（GUI 验证可用）

## 与同伴的比较

每位 claude_n 应该都在同一台机器上跑，理论上看到的环境一致。但同伴可能各自建了不同 env — 整合阶段要统一到一个 env 才能保证 §F2/F3 的一键复现。
