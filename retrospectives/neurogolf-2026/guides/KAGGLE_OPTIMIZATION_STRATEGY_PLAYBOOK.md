# Kaggle 提分策略与选题手册

本文用于下一场 Kaggle 比赛。目标不是堆实验数量，而是在有限算力、时间和提交额度下，持续产生可归因、可复现、能泛化的分数提升。

## 1. 开赛后先锁定真实规则

建模前从 Kaggle 页面、CLI/API 下载文件和官方说明确认以下内容，不凭经验猜测：

- 预测对象和任务类型；
- 评价指标、计算方式以及分数方向；
- `sample_submission` 的列名、行数、ID 顺序和数据类型；
- train/test 数据字段及隐藏测试集结构；
- 是否为 Code Competition 或 Notebook-only；
- internet、GPU、运行时间、磁盘和外部数据限制；
- 每日提交额度、最终提交数量和截止时间；
- 组队、预训练模型、外部数据和人工标注规则。

抓取不到的信息必须标记 `UNKNOWN`，不能用假设补齐。规则、数据文件和 `sample_submission` 应保留原始副本及 SHA256。

## 2. 建立可复现基线

第一版基线只承担四件事：

1. 数据从原始目录读入；
2. 本地训练和验证完整运行；
3. 推理输出通过格式校验；
4. Kaggle 能接受一次提交并返回分数。

基线必须固定：

- 代码 commit；
- Python 和依赖版本；
- 数据版本及 SHA256；
- 随机种子；
- 切分索引；
- 特征版本；
- 模型参数；
- OOF 预测；
- test 预测；
- submission SHA256。

没有 OOF 或等价离线验证证据的模型，不进入主线。

## 3. 先设计验证，再选择模型

验证方式应模拟隐藏测试集的生成方式，而不是追求更漂亮的本地分数。

| 数据结构 | 首选验证 | 主要泄漏风险 |
| --- | --- | --- |
| 独立同分布样本 | Stratified KFold / KFold | 同一实体重复出现 |
| 用户、设备、病人、商品 | GroupKFold | 同组样本跨 fold |
| 时间序列 | 时间前向切分 | 使用未来信息、全局统计 |
| 地理或站点数据 | 按区域或站点分组 | 邻近位置泄漏 |
| 排名、查询、会话 | 按 query/session 分组 | 同一查询跨 fold |
| 图数据 | 按连通分量或时间切分 | 邻居信息泄漏 |
| 合成任务或生成器 | 独立 seed、全状态空间或生成器验证 | 只覆盖公开样例形状 |
| Artifact/代码优化 | 官方样例 + 随机/生成器 + Runtime 审计 | 本地 Runtime 与评测端不一致 |

至少做一次 adversarial validation，检查 train/test 是否可被轻易区分。若 AUC 很高，优先处理分布漂移，而不是继续堆模型复杂度。

## 4. 用期望收益选题

不要使用“每题都到某门槛”“每个模型都必须优化”之类与总榜分无关的目标。统一按期望价值排序：

```text
priority =
    expected_score_gain
    * probability_local_valid
    * probability_hidden_generalizes
    / engineering_time
```

还应考虑：

- 与当前最优方案的相关性；
- 是否能迁移到多个任务或 fold；
- 提交是否能明确归因；
- 失败是否能产生可复用的负面证据；
- 计算成本和提交额度。

高成本但结构清晰的任务通常优先于低成本微调；小收益的通用方法可能优先于单题大工程，因为它能批量迁移。

## 5. 先计算上限和下限

开始一个实验前，先估算它的理论收益空间：

- 当前分数和误差来源；
- oracle blend 的上限；
- 特征或模型的理论下界；
- 样本噪声和标签不确定性；
- 计算和内存预算；
- 可接受的实现时间。

如果理论上限低于当前最小值得提交的收益，就停止该路线。这个步骤能过滤大量“能做但不值得做”的工作。

## 6. 三轨候选设计

每个高价值方向至少从三条不同路径尝试，而不是连续微调同一组参数。

### 候选 A：压缩或强化当前 winner

- 修复数据处理、泄漏和不稳定性；
- 搜索更可靠的参数区间；
- 删除无贡献特征；
- 调整正则化、采样和早停；
- 降低推理成本；
- 保持验证和部署风险最低。

### 候选 B：结构不同的方法

- 不同模型家族；
- 不同特征表示；
- 不同损失或采样策略；
- 不同尺度、窗口或上下文；
- 与主模型误差相关性更低的模型。

### 候选 C：从任务语义独立重建

- 重新解释目标生成过程；
- 从业务或赛题规则推导特征；
- 针对误差簇建立专用模型；
- 用规则、检索、排序、后处理或约束求解替代通用模型。

三个候选都应共享同一验证器和实验记录格式。

## 7. 按任务类型选择第一轮方法

### 表格

1. CatBoost/LightGBM 基线；
2. 缺失模式、频次、目标无关聚合；
3. Group-aware 或 time-aware CV；
4. 不同模型和 seed 的 OOF blend；
5. 检查类别编码和统计特征泄漏。

### 图像

1. 与图像尺寸匹配的预训练 backbone；
2. 按目标性质设计增强，避免改变标签语义；
3. 多尺度、TTA、不同架构 ensemble；
4. 逐类和逐场景误差分析；
5. 检查 train/test 设备、分辨率和压缩差异。

### 文本

1. 预训练 Transformer 或 embedding + 线性模型；
2. 长度、语言、来源和模板分组验证；
3. 清洗策略做 ablation；
4. 不同 max length、pooling、loss；
5. 防止同文本或近重复文本跨 fold。

### 时间序列

1. 严格时间切分；
2. lag、rolling、calendar 和实体统计；
3. 递归与直接多步预测对比；
4. 避免全数据归一化和未来聚合；
5. 针对 horizon 和 regime 做误差分析。

### 排名与推荐

1. 按 query/session/user 分组；
2. pointwise、pairwise、listwise 对比；
3. 候选召回与排序模型分别评估；
4. 负样本策略 ablation；
5. 关注 top-k 指标而非全局分类指标。

### 仿真、强化学习或生成任务

1. 先复现官方环境和 scorer；
2. 固定评估 seed，再使用独立 seed 验证；
3. 单独记录策略性能、方差和失败状态；
4. 避免只记最优单次结果；
5. 评估运行时间和评测端兼容性。

### Artifact 或代码优化

1. 绑定父 artifact SHA；
2. 找最大成本节点和中间量；
3. 只做精确等价或生成器证明过的重写；
4. 验证评测端算子、dtype、shape 和 Runtime；
5. 完整回归后才能叠加到父包。

## 8. 建立实验组合路线

推荐顺序：

1. **Baseline**：打通端到端和首次线上分；
2. **Validation**：修正切分，使 CV 与 LB 方向一致；
3. **Features/Data**：提高信息质量；
4. **Stronger model**：在稳定验证上升级模型；
5. **Diversity**：训练误差互补的模型；
6. **Ensemble**：仅使用 OOF 优化权重；
7. **Post-processing**：有指标或约束依据才加入；
8. **Ablation**：确认每项改动的独立贡献。

每轮只改变一个主要变量。多个改动一起上线后，无法知道真正有效的是哪一个。

## 9. 研究公开方案的正确方式

公开 notebook、dataset、discussion 和 GitHub 仓库主要用于：

- 核对数据理解；
- 发现验证陷阱；
- 学习特征和模型家族；
- 复现已知基线；
- 寻找评测端限制和失败案例。

每个来源记录：

```text
source_url
author
license
claimed_score
verified_score
data_version
method_family
reproduction_status
local_delta
provenance_notes
```

标题中的分数不等于可验证成绩。外部 artifact 不应直接混入主包；先还原方法、确认许可证和规则，再在自己的父版本上复现与验证。

## 10. 实验记录最小字段

```text
exp_id
datetime
git_commit
data_sha
parent_artifact_sha
fold_scheme
features
model
parameters
seed
cv_metric
fold_metrics
runtime
artifact_path
artifact_sha
submission_ref
public_lb
private_lb
status
notes
```

建议状态：

```text
idea
running
local_passed
candidate
submitted
online_positive
online_negative
blocked
rejected
```

只有 `local_passed` 以上状态才能构建 submission；线上负向候选不自动进入下一版累计包。

## 11. 提交额度分配

提交是实验资源，主要用于校准本地验证和隔离高风险改动。

### 推荐用途

1. 第一次提交：验证整个 pipeline 和格式；
2. 低风险累计包：确认 CV/LB 的总体一致性；
3. 高风险单变量：独立提交，便于归因；
4. 父包 rebase：只在父包身份和 SHA 明确时进行；
5. 最终组合：只包含线上正向或有强验证证据的候选。

### 额度规则

- 保留至少 10% 至 20% 用于截止日前应急；
- 有 `PENDING` 时不连续堆叠相关候选；
- 同一个 artifact SHA 不重复提交；
- 高风险变更单独提交，不和多个未知改动捆绑；
- 每次提交前刷新 history 和额度；
- 记录父分、预期增益和实际增益。

```text
expected_delta = candidate_local_metric - parent_local_metric
observed_delta = candidate_public_lb - parent_public_lb
```

若方向相反，立即隔离新增变量，检查分布、shape、Runtime、后处理和父包错配，不要用更多提交盲试。

## 12. Rebase 原则

任何累计候选都必须绑定一个确定父版本：

- parent submission ref；
- parent artifact SHA；
- parent code commit；
- parent CV 和线上分；
- 每个替换项的 old/new 指标。

当收到更高分父包时：

1. 解包并校验文件完整性；
2. 计算父包和每个 artifact SHA；
3. 重新测量候选相对新父包的增益；
4. 只保留严格优于新父包的候选；
5. 运行完整验证；
6. 生成新的 package SHA。

不要把相对旧父包有效的 diff 原样覆盖到新父包。

## 13. 上线前 Go/No-Go 门禁

只有全部为 `YES` 才提交：

```text
[ ] 规则和 submission 格式已从真实来源确认
[ ] CV 方案与隐藏测试生成方式匹配
[ ] 没有数据泄漏
[ ] 代码 commit 和数据 SHA 已记录
[ ] artifact 可从零复现
[ ] 本地指标严格优于当前 parent
[ ] 所有必要样例/fold/seed 已通过
[ ] 推理时间、内存和 Runtime 兼容
[ ] submission 文件通过 schema、行数、ID、NaN/Inf 校验
[ ] parent 和 submission SHA 已记录
[ ] 当前无冲突的 PENDING 提交
[ ] 剩余额度足够
```

## 14. 一周冲刺模板

### Day 1

- 锁定规则、指标、数据和提交格式；
- 建立最小 baseline；
- 完成一次 pipeline 提交。

### Day 2

- 设计可靠 CV；
- adversarial validation；
- 错误分桶和泄漏检查。

### Day 3

- 三类高价值特征或数据处理实验；
- 至少一次 ablation；
- 淘汰低上限路线。

### Day 4

- 两个不同模型家族；
- 多 seed 稳定性；
- 评估误差相关性。

### Day 5

- OOF ensemble；
- 约束驱动后处理；
- 单变量线上校准。

### Day 6

- 复现最有价值的公开方法；
- rebase 当前最佳父包；
- 运行完整回归。

### Day 7

- 清理高风险候选；
- 确定最终组合；
- 固化环境、SHA、日志和重现命令；
- 保留提交额度处理最后异常。

## 15. NeuroGolf 复盘中应迁移的经验

1. **总分增益优先。** 不要把所有子任务达到同一门槛当作目标。
2. **父版本感知。** 候选必须相对当前 winner 重新比较，不能沿用旧 diff。
3. **本地通过不等于隐藏集通过。** 已知 shape 上 exact 仍可能在未见 shape 失败。
4. **本地 Runtime 不等于 Kaggle Runtime。** dtype、算子、padding 和版本都要审计。
5. **中间成本可能比参数更重要。** 模型文件更小、节点更少不必然使官方指标更好。
6. **高风险改动必须隔离。** 一次叠加多个未知改动会浪费额度并破坏归因。
7. **方法迁移优于盲目复制 artifact。** 保留 provenance、许可证和构建脚本。
8. **覆盖率和文档不是分数。** 工具和记录只服务于更快地产生可信候选。

## 16. Token 与实验配置边界

提交认证由环境变量或 Kaggle CLI 凭据文件负责。文档和仓库中只能出现格式示例：

```text
KAGGLE_API_TOKEN=KGAT_<YOUR_TOKEN>
```

token 不能作为实验参数、dataset、notebook source、kernel metadata 或 Git 文件的一部分。实际配置方法见 `LOCAL_KAGGLE_SUBMISSION_PLAYBOOK.md`。

## 17. 最终原则

每个候选都要回答四个问题：

1. 它为什么应该提高官方指标？
2. 本地验证是否覆盖隐藏测试的关键变化？
3. 它相对哪个确定父版本有效？
4. 如果线上失败，能否用一次提交定位原因？

无法回答时，候选仍是实验，不是可提交版本。
