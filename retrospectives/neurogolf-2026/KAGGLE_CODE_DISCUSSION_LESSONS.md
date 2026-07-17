# NeuroGolf 2026 Code 与 Discussion 复盘

采集时间：2026-07-17（比赛结束后两天）。  
范围：Kaggle `neurogolf-2026` 的公开 Code、Discussion、赛后 solution write-up；以 Kaggle API/CLI 返回内容为准。投票数和帖子状态会继续变化，本文保留采集时快照，不把社区争议当作已证实事实。

## 一页结论

NeuroGolf 的高排名方案并不是靠一个“万能 ONNX 技巧”取胜，而是把 400 个任务做成可持续优化的工程系统：

1. 每个任务都保存模型、可复现 builder、任务知识和失败记录。
2. 候选只能经过官方风格的正确性、成本、运行时和隐藏分布代理验证后晋升。
3. 纵向深挖单任务，用于发现新架构；横向扫描相似任务，用于迁移新技巧。
4. 用短期共享 memory 加长期 archive/cookbook，避免每个 agent 重复理解任务。
5. 把模型选择视为“每任务多候选 + 总运行时约束”的组合优化，而不是只保留一个最高本地分模型。
6. 在线分数是验证信号，不是替代本地证据的调参接口；异常必须用小批次或单任务差分提交隔离。

这和本仓库原有提交复盘的结论一致：真正稳定的增益来自 parent-bound、可复现、可回滚、可归因的精确变换，而不是覆盖率、报告数量或未经隔离的累积大包。

## Code 区观察

采集时高票 Code 的代表性条目如下（链接均为公开 Kaggle Notebook）：

| Code | 采集时票数 | 可复用价值 |
| --- | ---: | --- |
| [The 2026 NeuroGolf Championship](https://www.kaggle.com/code/mmoffitt/the-2026-neurogolf-championship) | 509 | 官方任务可视化、示例加载、候选网络验证入口；应作为环境和接口的基准。 |
| [Audited NeuroGolf ONNX Overrides](https://www.kaggle.com/code/kojimar/audited-neurogolf-onnx-overrides) | 336 | 按任务读取多个 bundle、只覆盖更优候选、重建 400 文件提交；体现 task-level attribution 和可审计合并。 |
| [2026 NeuroGolf Baseline](https://www.kaggle.com/code/yusuketogashi/2026-neurogolf-baseline) | 196 | 记录精确 lineage、变更任务、成本差、验证数量和提交回执；适合作为候选 manifest 模板。 |
| [NeuroGolf 2026: Graph Surgeon](https://www.kaggle.com/code/seddiktrk/neurogolf-2026-graph-surgeon) | 172 | 串联 `onnxoptimizer` 与 ONNX Script 优化器；适合先做通用无损清理，但不能替代语义级重写。 |
| [All Task Description Analysis](https://www.kaggle.com/code/karnakbaevarthur/all-task-description-analysis) | 164 | 将 400 个 ARC 任务结构化为变换类型、复杂度和尺寸变化，支持任务分群与技巧迁移。 |
| [NeuroGolf 2026: All Graph Surgeries](https://www.kaggle.com/code/seddiktrk/neurogolf-2026-all-graph-surgeries) | 153 | 从安全到高风险分层执行 cleanup、索引压缩、广播压缩、结构微改写、FP16，并逐任务验收。 |
| [Chimera Safe-Boost Caddies](https://www.kaggle.com/code/lucifer19/chimera-safe-boost-caddies) | 141 | 把 Constant 提升为 initializer、合并 Gather、缩窄索引、删死图；每个任务独立证据门控和原子回滚。 |
| [NeuroGolf 7266.48 / kaggloop](https://www.kaggle.com/code/ryosukeshiroshita/neurogolf-7266-48-github-com-qurore-kaggloop) | 140 | 公开可复现实验循环、官方 scorer 复核、严格 min-merge；同时展示终端算子、低秩 Einsum、GridSample、ConvInteger、画布裁剪等技巧族。 |

### Code 区最重要的工程经验

#### 1. 先锁死 scorer、接口和运行时

所有候选必须验证静态输入输出、ONNX checker、shape inference、目标 ONNX Runtime、公开样例、生成样例和文件限制。一个模型“能加载”不等于“能提交”，“公开样例正确”也不等于“隐藏分布正确”。

#### 2. 通用优化器是第一层，不是最后一层

死代码删除、常量折叠、CSE、Identity/no-op 删除通常安全，但高价值增益更多来自表示变化：直接让终端算子写入免费 output、以计算换存储、把全画布中间量变成标量/短向量/小 crop、用小因子重建大张量。

#### 3. 候选必须按任务审计

400 个模型的整包分数不能说明哪个任务有效。正确做法是维护 `task -> parent -> candidate -> cost -> validation -> online attribution`，只将严格成本更低且证据完整的候选覆盖到最新 parent。

#### 4. 生成器验证要覆盖真实状态空间

固定公开 shape 上的随机测试会产生“局部精确”的错觉。凡是依赖尺寸、padding、索引、量化、动态 Slice/Pad 或静态窗口的变换，都应从生成器/规则证明范围，或执行全 shape、全 palette、边界值测试。

#### 5. 每次提交都要可复现

记录 source notebook/version、父包 SHA、变更任务、模型 SHA、预期增益、验证命令、运行时与实际 Kaggle 回执。否则公开 bundle 的不断 fork 会快速丢失来源和因果关系。

## Discussion 与赛后方案观察

### 第一名：知识复用和两类搜索循环

来源：

- [1st Place - Introduction](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726654)
- [Pipeline overview](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726799)
- [Self Evolving Prompts](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726883)

第一名团队把 task notes、task facts、架构族、失败路径、builder、公共 ARC 解法和共享 cookbook 一起交给 worker。其公开统计称，架构重写平均单任务约 `+0.5`，在现有图上继续微调平均约 `+0.05`；因此 prompt 会给明确目标并要求在无法达到时重新考虑表示，而不是无期限剪枝。

工作流交替执行：

`单任务纵向探索 -> 分析轨迹并提炼新技巧 -> 相似任务横向迁移 -> 再探索`

运行时也被当作一等约束。团队保存每任务的多候选分数和速度，用 Multiple-Choice Knapsack Problem 在总运行时限制下选 400 个模型，并同时保留高分慢包与略低分快包。

“Self Evolving Prompts”的核心不是神秘措辞，而是让多个 agent 参加同目标、同时限的 mini-contest，保留成功上下文，人工复盘后把最好的经验晋升为 manager/cookbook。可复用部分是有指标的 prompt 实验与知识蒸馏，不是简单复制长 conversation。

### 第六名：双团队换区，打破局部最优

来源：[6th Place Solution - Claudex](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726691)

两个团队分别处理 200 个任务，一到两天后交换任务区间；Codex 与 Web ChatGPT 并行工作。不同 prompt、算子偏好和初始表示能让第二组在第一组认为“已经榨干”的任务上继续改进。其验证门包括目标运行时、精确公开样例和 1000 个新 ARC-GEN 样例；LB 0、超时和格式错误被写回任务警告，而不是被当作一次性事故。

### 第九名：短 memory + 长 archive

来源：[9th Place Gold - Pavel & CroDoc](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726782)

两位成员经常独立解决同一任务，再按验证分数和运行时合并。共享知识分成约 200 行的 `MEMORY.md` 和完整 `MEMORY_ARCHIVE.md`：前者每次加载，后者按需检索，定期去重和晋升技巧。这比把全部历史塞进每个 prompt 更稳定。

技术层面反复出现“recompute instead of store”和“让终端算子直接写 output”。该方案主集合中有 202/400 个单节点模型、273/400 个以 Einsum 结束；这不是说 Einsum 永远最优，而是说明免费 MAC 与收费中间内存的 metric 会系统性偏好代数程序式表示。

### 第十名：三文件任务单元与事务式 scheduler

来源：[10th Place Solution](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726653)

每个任务保持三个同步资产：

- `taskNNN.onnx`：实际执行物；
- `attack_tNNN.py`：可复现 builder 与测试；
- `task-NNN.md`：规则、假设、实验、成本历史和隐藏风险。

每个任务有独立持久 Codex session，scheduler 使用有界 worker pool。每轮执行 `backup -> experiment -> validate -> promote/restore`，失败不会破坏已接受状态。线上整包分数与本地预期不一致时，用差分分组/二分提交定位问题任务；只有线上确认的通用技巧才由串行 consolidation 步骤写入共享 `tricks.md`。

这一方案公开的五天低并发无人值守结果为本地验证分从 7516.01 到 7575.78（+59.77），271 个任务发生变化且没有保留成本回退，说明收益来自系统持续保留许多小中型改进，而不是一次性大技巧。

### 暂未完成的赛后 write-up

[4th Place Atlas](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726879) 已公开研究 Atlas，但采集时技术正文仍待补；[7th](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726660) 和 [8th](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726693) 仍是 draft。后续刷新时应单独更新，不能根据排名猜测未公开方法。

## 下一场比赛可直接复用的作业规范

### 仓库结构

```text
tasks/<id>/
  current_artifact
  builder
  notes.md
  candidates/
registries/
  task_state.csv
  candidate_manifest.csv
  evidence_registry.md
cookbook/
  concise.md
  archive.md
reports/
  online_attribution.md
```

### 候选状态机

`discovered -> locally_valid -> generator_valid -> runtime_valid -> package_valid -> online_confirmed -> promoted`

任何阶段失败都进入带原因的 terminal state；不删除负证据，也不让并行 worker 直接修改共享 cookbook。

### 验证阶梯

1. 静态格式与 schema。
2. 官方本地 checker/metric。
3. 全公开样例。
4. 生成器、全 shape、边界值和变形测试。
5. 目标运行时与整包预算。
6. 确定性打包和 SHA 审计。
7. 单任务或小批次线上归因。
8. 只有证据闭环后才合入 parent。

### 合规底线

比赛后期出现过公开模型 archive、分数真实性和最后数日合规性的争议。本文只记录这些讨论存在，不对参与者作事实判断。未来使用公共模型、数据集或代码前，应保存发布时间、版本、作者、许可证、规则条款和 host/staff 澄清；没有明确来源与许可时，只把它作为研究线索，不直接并入最终提交。

## 与本仓库复盘的合并判断

本仓库原复盘已经识别出 parent rebasing、SHA、deterministic ZIP、负证据、单任务隔离和全 shape 验证的重要性。赛后 Code/Discussion 进一步补足了四点：

1. 每任务必须长期保存 builder 和 notes，不能只保存二进制。
2. 知识库要分短 memory 与长 archive，并由串行步骤维护。
3. 新技巧要同时支持纵向发现和横向迁移。
4. 最终 400 模型选择应显式建模运行时预算和候选组合。

下一场类似的多任务竞赛，应该先搭建这些系统，再开始大规模 agent 优化。
