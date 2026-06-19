# Alyce V4 Simulation Cause Analysis - 2026-06-19

## 结论

V4 当前不应该继续作为提交候选。

重新检查模拟结果、V2/V3/V4 代码路径和补跑 trace 后，原因不是单一参数太大或太小，而是三层问题叠加：

1. **V4 的基底选错了。**
   V4 是从 `alyce_intervention_v3` 继续改，不是从当前官方 best `alyce_4p_ffa_v2` 继续改。V2 已经有一套更有效的 FFA mission filter，而 V4 没有继承这套逻辑。

2. **V4 仍然只是候选目标的软评分层。**
   它不改 fleet size，不改 reserve floor，不强制 regroup，也不验证“被降权目标是否有更好替代”。所以它最多能改变少量 top candidate，不能修复复盘里反复出现的 4P early/mid production collapse。

3. **本地小样本模拟存在 seed 复跑不稳定。**
   同一 seed/同一座位补跑 trace 时，部分局的胜者和原始模拟不同。因此这组本地模拟可以判断“不足以证明 V4 更强”，但不能把单局当成精确可复盘录像。

最终判断：

```text
V2 仍是当前实际基准。
V4 当前结果说明：不要提交，不要继续在 V3 分支上堆复杂 scorer。
下一步应基于 V2 做 V4b/V5，并先补齐 selected-action trace 和 determinism audit。
```

## 复查材料

本次复查参考：

```text
reports/ALYCE_V4_LOCAL_V123_SIM_20260619.md
reports/ALYCE_INTERVENTION_V4_IMPLEMENTATION_20260619.md
reports/V2_LATEST_REPLAY_AND_V3_SUBMISSION_SYNTHESIS_20260619.md
reports/V3_OFFICIAL_REPLAY_EFFECTIVENESS_REVIEW_20260619.md
reports/ALYCE_52_REPLAY_REVIEW_20260618.md
agents/variants/alyce_4p_ffa_v2/main.py
agents/variants/alyce_intervention_v3/main.py
agents/variants/alyce_intervention_v4/main.py
outputs/v4_vs_v123_pair_s1_3/
outputs/v4_vs_v123_4p_s1_3/
```

补跑 trace 输出保留在：

```text
outputs/v4_reason_trace_20260619/
```

这些 `outputs/` 文件不提交 Git。

## 模拟结果复核

### 1v1

每组 3 seeds，双向，共 6 局。

| Matchup | V4 wins | Opponent wins | Draws | V4 winrate | 解释 |
|---|---:|---:|---:|---:|---|
| V4 vs V1 | 2 | 4 | 0 | 33.3% | V4 分支本身不稳，连旧 V1 都不能压住。 |
| V4 vs V2 | 3 | 3 | 0 | 50.0% | 对当前官方 best 家族没有优势。 |
| V4 vs V3 | 3 | 2 | 1 | 50.0% / 非 draw 60.0% | 小样本略优于 V3，但不构成提交依据。 |

重要解释：

```text
V4 scorer 在 2P 下被 player_count gate 关闭。
所以 1v1 结果主要不是 V4 context scorer 的效果，而是 V4 parent branch、位置/seed 和本地 runner 稳定性的综合表现。
```

### 4P family test

V1/V2/V3/V4 四者同场，V4 轮换 4 个座位，每个座位 3 seeds，共 12 局。

| Agent | Wins | Winrate | Avg rank | Avg final ships | 解释 |
|---|---:|---:|---:|---:|---|
| V2 | 5/12 | 41.7% | 1.6667 | 1246.25 | 当前仍是最强 practical baseline。 |
| V1 | 3/12 | 25.0% | 1.6667 | 1278.58 | 旧分支仍能赢过 V4。 |
| V3 | 2/12 | 16.7% | 2.0833 | 1488.83 | V3 较弱但仍多赢于 V4。 |
| V4 | 1/12 | 8.3% | 2.0833 | 811.00 | 不适合提交。 |

V4 by seat:

| V4 position | Games | Wins | Winrate |
|---:|---:|---:|---:|
| 0 | 3 | 0 | 0.0% |
| 1 | 3 | 0 | 0.0% |
| 2 | 3 | 1 | 33.3% |
| 3 | 3 | 0 | 0.0% |

这一组的核心信号不是 “V4 小样本输了一点”，而是：

```text
V4 在同族 4P 内战里最低胜率；
avg final ships 也最低；
没有稳定 seat robustness。
```

## 补跑 Trace 发现

为了分析 V4 scorer 是否真的改变了决策，补跑了 4 个代表局并打开：

```text
ORBIT_V4_TRACE_PATH=outputs/v4_reason_trace_20260619/<case>/trace.jsonl
```

### 重要限制：同 seed 复跑不完全一致

补跑 trace 时，部分原本的 seed/座位组合产生了不同 winner。例如：

| Case label | 原始模拟 winner | trace 补跑 winner | 说明 |
|---|---|---|---|
| pos0 seed1 | V3 | V4 | 同 seed 同座位胜者改变。 |
| pos1 seed3 | V1 | V2 | 同 seed 同座位胜者改变。 |
| pos2 seed3 | V4 | V1 | 同 seed 同座位胜者改变。 |
| pos3 seed2 | V2 | V2 | 这一局方向一致。 |

代码搜索没有发现 V2/V3/V4 主文件里显式使用 `random` / `torch.rand` / `np.random`。更可能的原因包括：

1. Kaggle environment 的 `randomSeed` 不足以覆盖 Orbit Wars 所有内部随机或数值路径。
2. agent 是 stateful runtime，虽然 loader 每局重新加载模块，但 callable / module / bundled package 状态仍需专门做 determinism audit。
3. PyTorch/环境中的 tie-break 或候选同分排序可能在细节上不稳定。
4. trace 写文件本身不应改变 score，但它改变运行路径和时序，不适合当作逐 turn 精确复盘证据。

因此：

```text
当前本地胜率只能作为 screen，不应当作为精确 Elo 或精确单局复盘。
后续必须先做 same-seed repeated-run determinism audit。
```

### Trace 汇总

| Case | Trace rows | top_changed | top_changed rate | trap_neutral | safe_neutral_bonus | source_protect | far_low_nonleader_enemy | leader_low_value_weak | trailing_bad_attack |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pos0 seed1 rerun, V4 win | 154 | 24 | 15.6% | 270 | 229 | 554 | 28 | 0 | 0 |
| pos1 seed3 rerun, V2 win | 97 | 4 | 4.1% | 94 | 0 | 0 | 0 | 8 | 15 |
| pos2 seed3 rerun, V1 win | 115 | 3 | 2.6% | 41 | 11 | 21 | 0 | 0 | 0 |
| pos3 seed2 rerun, V2 win | 183 | 15 | 8.2% | 400 | 594 | 81 | 0 | 95 | 3 |

Trace 说明：

1. V4 的 label 计数很多，但 `top_changed` 很低。
   - 这说明大量被标记的候选并不是原本会被选中的 top move。
   - 只统计 label 数量会高估策略影响。

2. `source_protect` 仍然可能在某些地图上很高。
   - V4 implementation report 中调参后某个 smoke seed 的 `source_protect` 只有 32。
   - 本次 pos0 trace rerun 达到 554。
   - 说明 source protection 仍强烈依赖地图/局势，不能认为已经稳定收窄。

3. `far_low_nonleader_enemy` 很少触发。
   - V4 设计重点之一是处理 far-low nonleader enemy，但补跑 trace 只有一局有 28，其余为 0。
   - 这说明 V4 当前失败并不主要由该 label 覆盖。

4. `leader_low_value_weak` 在 pos3 loss 里很多，但 V2 仍赢。
   - 这类 label 即使出现，也没有足够改变最终局势。
   - 原因可能是它只调 target score，没有解决 source reserve、holdability、regroup timing 和 fleet size。

## 代码层原因

### 1. V4 不是 V2 的增强版

V4 来源：

```text
agents/variants/alyce_intervention_v4/SOURCE.md
Immediate implementation parent: agents/variants/alyce_intervention_v3
```

V3 的核心改动是 `_apply_ffa_v3_safety_penalty`：

```text
agents/variants/alyce_intervention_v3/main.py:315
```

它只做：

```text
far low-value non-leader enemy penalty
far low-value neutral penalty
```

V4 替换为 `_apply_ffa_v4_context_score`：

```text
agents/variants/alyce_intervention_v4/main.py:343
```

但它仍然是：

```text
score = score + bonus - penalty
```

也就是说，V4 本质是 V3 分支上的更复杂 scorer。

而 V2 的 4P 逻辑不同。V2 有 `enable_ffa_mission_filter`：

```text
agents/variants/alyce_4p_ffa_v2/main.py:81
agents/variants/alyce_4p_ffa_v2/main.py:721
```

V2 里包括：

```text
severe trap hard veto
soft contested neutral penalty
safe neutral bonus
source depletion penalty
```

对应代码：

```text
agents/variants/alyce_4p_ffa_v2/main.py:359
agents/variants/alyce_4p_ffa_v2/main.py:370
agents/variants/alyce_4p_ffa_v2/main.py:377
agents/variants/alyce_4p_ffa_v2/main.py:380
agents/variants/alyce_4p_ffa_v2/main.py:385
```

所以当前 V4 的失败首先是路线问题：

```text
我们在低于 V2 的 V3 分支上继续修，而不是在 V2 official-best 分支上低风险增强。
```

### 2. V4 没有解决复盘指出的主因

V2/V3 official replay 复盘都指向同一个主因：

```text
4P losses are decided by early/mid production conversion.
step50/step100 production gap 扩大后，后续攻击很难恢复。
```

V2 最新复盘里：

```text
4P losses step100 avg production gap: -24.50
4P mid/late losses enemy_rate high, regroup/mine low
```

V3 复盘里：

```text
V3 4P losses step100 avg production gap: -28.5
far-low penalty does not create enough regroup/consolidation behavior
```

V4 的 scorer 尝试识别：

```text
reaction_bad
trap_neutral
safe_neutral
source_protect
trailing_bad_attack
leader_low_value_weak
```

对应代码：

```text
agents/variants/alyce_intervention_v4/main.py:421
agents/variants/alyce_intervention_v4/main.py:450
agents/variants/alyce_intervention_v4/main.py:451
agents/variants/alyce_intervention_v4/main.py:462
agents/variants/alyce_intervention_v4/main.py:470
agents/variants/alyce_intervention_v4/main.py:484
```

但它没有：

```text
1. 改 send size。
2. 改 source reserve floor。
3. 强制保留高产 source 的最低防守。
4. 在落后时主动切换到 production recovery / regroup mission。
5. 输出 selected source/target/send trace 来证明改动命中了关键动作。
```

所以它只能调整候选排序，不能保证生产恢复。

### 3. V4 的 trace 指标过粗

当前 trace 只记录：

```text
top_changed
label counts
prod_rank
prod_gap
```

问题是：

```text
label count != selected action changed
top_changed != changed move is better
```

例如 pos3 loss：

```text
trap_neutral: 400
safe_neutral_bonus: 594
leader_low_value_weak: 95
top_changed: 15 / 183
```

候选层面标签很多，但最后只 8.2% turn 改变 top candidate。更关键的是，报告没有记录：

```text
before_target
after_target
before_send
after_send
target owner/prod/ships
source ships/prod
whether changed move improved step50/100 production
```

没有这些字段，就不能确认 V4 是“避开坏动作”，还是“把一个坏动作换成另一个坏动作”。

## 为什么 V4 的 4P 胜率差

综合模拟、trace 和代码，最合理解释是：

### 原因 A：V4 丢掉了 V2 的有效 FFA filter

V2 在 4P 中已经有：

```text
trap hard veto
contested neutral soft penalty
safe neutral bonus
source depletion penalty
```

V4 不是从 V2 开始，因此它并不是对当前 official-best 的小修，而是在 V3 分支上重新做一套 context score。V4 输给 V2，首先说明 V2 的已有 mission filter 更有用。

### 原因 B：V4 对关键局势的 top action 影响不足

trace 里 top_changed 只有：

```text
2.6% - 15.6%
```

如果 losing 4P 的关键失误发生在少数早期高杠杆 turn，V4 需要准确改掉那些 turn。当前 trace 没证明这一点。

### 原因 C：V4 的 penalty/bonus 可能制造噪声

V4 同时加入：

```text
trap penalty
safe neutral bonus
source protect penalty
leader weak hold penalty
trailing bad attack penalty
lead bleed penalty
```

这些信号可能同时出现，但没有 mission priority。结果可能是：

```text
候选分数被多种小规则扰动，
但没有形成明确的 opening expansion / consolidation / leader pressure 模式。
```

### 原因 D：没有替代动作检查

V4 降权一个目标时，没有判断“替代 top target 是否真的更好”。在 4P 中，这很危险：

```text
坏目标 A 被降权，
但替代目标 B 可能更远、更慢、无法 hold，
最终 tempo 仍然丢失。
```

这解释了为什么 V4 经常 rank2/rank3，而不是转化成 win。

### 原因 E：小样本和非确定性让单局解释不可靠

同 seed 复跑胜者会变，说明：

```text
不能用某一局说“V4 在 turn X 一定因为 Y 输”。
```

当前能可靠使用的是聚合结论：

```text
V4 没有在当前本地筛选中显示优势；
V4 的 trace 也没有证明它稳定命中关键动作。
```

## 接下来怎么做

### 立即停止

不要提交当前 V4。

不要继续在 V3 分支上增加更多 scorer。

### 下一版方向：V4b/V5 应基于 V2

正确路线：

```text
base = agents/variants/alyce_4p_ffa_v2
not agents/variants/alyce_intervention_v3
```

只允许低风险增强：

1. 保留 V2 的 severe trap hard veto。
2. 保留 V2 的 contested neutral penalty。
3. 保留 V2 的 safe neutral bonus。
4. 保留 V2 的 source depletion penalty。
5. 在 V2 之后追加 very narrow selected-action safety check。

### 先补工具，不先改策略

下一步应先做：

```text
scripts/run_determinism_audit.py
scripts/run_selected_action_trace.py
```

必须记录：

```text
same seed repeated 3-5 times
winner stability
rank stability
score stability
selected source/target/send before and after filter
step20/50/100 production gap
```

没有这些，不应该再根据单局体感改代码。

### V2-based narrow filter 候选

只有 trace 证明有效时，再考虑：

```text
if 4P and selected target is low-prod far neutral/enemy:
    only replace if alternative target has:
      higher production,
      better reaction gap,
      lower source depletion,
      and no worse ETA
```

不要再做全候选小惩罚堆叠。

## Final Decision

```text
V4 result: reject.
Root cause: wrong parent branch + soft scorer cannot repair 4P production conversion.
Current best baseline: keep V2.
Next action: determinism audit + selected-action trace + V2-based narrow filter.
Kaggle submit: No.
```

