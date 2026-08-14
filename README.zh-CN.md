# Riemann-Conjecture-Research(中文说明)

**黎曼猜想：临界线上零点比例攻关** — Proportion of zeros of the Riemann zeta function on the critical line

> 研究流水线(DSH `math-research-workflow`:管理 → 严格研究 → 审计),所有新进展自动同步至本仓库。
> 状态:**进行中**。当前无条件世界纪录:
> **liminf N₀ˢ(T,2T)/N(T,2T) ≥ 0.6730536459525899252…**(C₉,2026-08-14,本项目)。

## 问题定义

令 ρ = β + iγ 遍历 ζ 的非平凡零点,N(T₁,T₂) 按重数计数零点,N₀ˢ(T₁,T₂) 计数**临界线 Re s = 1/2 上的简单零点**。本项目致力于把

$$\liminf_{T\to\infty}\ \frac{N_0^s(T,2T)}{N(T,2T)}$$

的无条件下界推向 1(即"临界线上零点比例 = 1",用户目标),并把完整目标约化为精确的猜想。

## 当前纪录(无条件,ζ 函数)

| 常数 | liminf N₀ˢ(T,2T)/N(T,2T) 下界 | 来源 |
|---|---|---|
| 2/3 | 0.6666… | Claude/Anthropic 2026(Lean 验证) |
| 0.6725007036… | 3/2 − (1/√2)cot(1/√2),Montgomery–Taylor 窗口 | Anthropic Thm D |
| 0.6730085279… | 7 点压力稳定性精化 | OpenAI/GPT-5.6 Sol 草稿(本项目独立审计) |
| **0.6730536459…** | **(6875·H_MT − 1315/96)/6849,k=9 压力证书 F₈ ≥ 39/10000** | **本项目(extpress run)** |
| 0.6730856…(证书进行中) | f₉ = 0.00395 时的 (26,100,000·H_MT − 52,000)/26,000,065 | 本项目(f9push run) |

- 不同零点:N_d/N ≥ 5/6(MT 窗口下 0.83625…)
- ξ′ 的零点:四次窗口下线上简单零点 0.86864;**MT 窗口下 0.8691835…(本项目,审计 A1–A6 全部 PASS)**;0.8692247… 待同一 f₉ 证书落地
- 带宽一证书类上限:≈ 0.6818(Lean 认证)

## "概率为 1" 的状态(诚实陈述)

- **无条件:仍然开放。** 精确障碍:带宽一证书上限 ≈ 0.6818(幽灵 256 周期构型);压力类上限 ≈ 0.6731(k=9)及更远;X ≍ T 时高阶迹矩不可得(Rudnick–Sarnak kλ<2 范围)。
- **条件可达:**
  - PCC 全支撑 ⇒ 100%(GLSS25,arXiv:2503.15449);
  - HL*(所有迹矩 = sine-kernel Gram 矩)+ 谱引理 SL ⇒ 100%(本项目证明,ε-形式/迭代极限,condp1 run)。
  - Anthropic 论文 §7.2(f) 含一处转录错误(m₂:3/4 → 4/3),本项目精确解决(Λ₂(0) = 5/36、13/18)。
  - **2026-08-15:随机 sine-process Gram 模型精确重现审计矩列 (1, 4/3, 2, 13/4)**(m₂ = 4/3、m₃ = 2、m₄ = 13/4,后两者由数值 MC 升级为精确;DPP 模拟端到端验证);SL(Christoffel 形式)有特征值标度与 Christoffel 衰减证据支持(Λ_m(0) ≈ 0.32、0.13、0.045、0.023 → 0),但仍为开放引理(reports/sl-lemma-random-gram-probe.md)。

## 方法与来源

1. **Anthropic(Claude 2026)rank–trace 方法**:Weil 显式公式 Hermitian 压缩;N₀ˢ(T,2T) ≥ (2−R(ψ))N;Lean 验证的 Thm D 基线 H_MT = 0.6725007036794116…。
2. **OpenAI(GPT-5.6 Sol)稳定性精化**:Lemma 2.1(rank–trace 带 D(M) = tr Ψ(M))+ Cor 2.2 ⇒ C₇ = 0.6730085279…(本项目双重独立审计 PASS,Arb 证书逐字节复现)。
3. **本项目 k 点压力方法**(extpress run):一般-k 链(块能量/块缺陷/收缩平均)符号化推导,精确复现 k=3 与 k=7;k=9 证书 F₈ ≥ 39/10000(8 变量 Arb 分支定界,53,137,290 节点,核哈希 7029ac0f…)→ 世界纪录 C₉ = 0.6730536459525899252…。
4. **本项目 ξ′ 压力方法**:对 ξ′(完备 zeta 函数导数)应用同一压力链 + MT 窗口,H_{ξ′}^{MT} = 2 − κ₁(1, v_MT) = 0.8678888651990519…(新常数,A2 双路径验证)→ C₉^{ξ′}(0.0039) = 0.8691835350528274770…,超过四次窗口纪录 0.86864;审计 A1–A6 经理级 PASS;AdmWindow 余弦窗口形式化蓝图就绪(A=1, B=2, cMod = cRho+4)。

## 仓库结构

```
literature/   文献(Anthropic v1/v2/note、OpenAI 草稿、GS、Lean 快照)、FRONTIER.md(B0 审计轨迹)
runs/         rigorous-open-math-research/R-*/ — 各运行的标准工件、Arb 证书、脚本
reports/      经理级独立验证报告
index/        论文 / 运行 / 工件 / 任务包登记
agenda/       方向、优先级、任务包(契约 + B0 新颖性预检)
state/        RESUME.md、current.json、活动日志、阶段总结
```

## 可复现性

- 所有工件哈希绑定(sha256 记录于 SHA256SUMS / 各运行 repro_manifest)。
- Arb 证书:`verify_kpoint_parallel.py 9 39/10000 --grid 4000 --precision 128 --workers 22`(Python 3.10,python-flint/Arb 0.9.0);k=7 验证逐字节复现领域接受的证书(核哈希 a9992300…)。
- 释放检查全部预先计算并经两个已知证书双重交叉验证(组件与核哈希逐字节吻合)。
- 流水线门禁:`validate_pipeline.py --project .`(阶段关闭时 0 问题)。

## 近期活动

- 2026-08-14:阶段 B 收官;新纪录 C₉ = 0.673053646(k=9 证书,53,137,290 节点);独立审计全部 PASS(OpenAI 草稿 ×2,condp1 PASS-CONDITIONAL + F-1 修复);C₉ 经理级审计 PASS-with-limits;仓库同步 GitHub。
- 2026-08-15:ξ′ 候选 0.8691835 审计完成(A1–A6 PASS,经理级);AdmWindow 余弦蓝图完成;f₉ = 0.00395 认证运行中(grid-2000 + grid-4000,各 8 worker)→ 落地后发布 0.6730856(ζ)+ 0.8692247(ξ′)。
- 下一步:收取 f₉ 证书,执行 release-checklist.md;纪录定理独立审计(包已备);SL 引理;Stage C Lean 实例(AtOne 模式)。

## 联系与同步

本仓库由 DSH `math-research-workflow` 流水线驱动,每次新进展自动提交并推送至
https://github.com/Zhongshan-Big-Jun/Riemann-Conjucture-Research 。
