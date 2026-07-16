# 本机 Kaggle 提交手册

适用环境：Windows PowerShell、Python、Kaggle CLI。本文按本机已验证的 `Kaggle CLI 2.2.3` 编写，同时覆盖普通文件比赛和 Code Competition。

## 1. 安装与检查

优先在项目虚拟环境安装：

```powershell
python --version
python -m pip install -U kaggle
kaggle --version
```

建议每个比赛使用独立目录：

```text
competition-work/
├── data/
├── src/
├── notebooks/
├── submissions/
├── kaggle_kernel/
├── reports/
└── logs/
```

## 2. 配置 Kaggle token

实际 token 形如：

```text
KGAT_<YOUR_TOKEN>
```

禁止把真实 token 写进 Git、README、Notebook、submission message、命令日志或聊天记录。

### 方式 A：仅当前 PowerShell 会话有效

最简单的命令是：

```powershell
$env:KAGGLE_API_TOKEN = "KGAT_<YOUR_TOKEN>"
```

该写法会进入 PowerShell 历史。更安全的方式是交互输入：

```powershell
$secure = Read-Host "Kaggle API token" -AsSecureString
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
try {
    $env:KAGGLE_API_TOKEN = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
}
kaggle competitions list --page-size 3
```

关闭终端后环境变量消失。

### 方式 B：Kaggle CLI 的 access token 文件

Kaggle CLI 2.x 可以读取用户目录中的 token 文件。不要在项目目录中创建它。

```powershell
$token = Read-Host "Kaggle API token"
$kaggleDir = Join-Path $HOME ".kaggle"
New-Item -ItemType Directory -Force -Path $kaggleDir | Out-Null
Set-Content -LiteralPath (Join-Path $kaggleDir "access_token") -Value $token -NoNewline
Remove-Variable token
```

随后限制文件只允许当前用户访问：

```powershell
$tokenFile = Join-Path $HOME ".kaggle\access_token"
icacls $tokenFile /inheritance:r
icacls $tokenFile /grant:r "$env:USERNAME:(R,W)"
```

项目 `.gitignore` 仍应包含：

```gitignore
kaggle.json
access_token
.env
*.zip
```

## 3. 初始化比赛

设定比赛 slug：

```powershell
$competition = "your-competition-slug"
kaggle competitions files -c $competition
```

如果返回 403 或规则未接受：

1. 打开比赛网页。
2. 阅读并接受 Rules。
3. 确认账号满足电话、身份或团队要求。
4. 再运行 CLI，不要无限重试。

下载数据：

```powershell
New-Item -ItemType Directory -Force data\raw | Out-Null
kaggle competitions download -c $competition -p data\raw
```

记录原始文件哈希：

```powershell
Get-ChildItem data\raw -File | Get-FileHash -Algorithm SHA256
```

## 4. 提交前的硬门禁

任何提交至少满足：

```text
1. 使用真实 sample submission 或官方输出格式。
2. 列名、行数、ID 顺序完全一致。
3. 预测无 NaN、Inf 和非法标签。
4. 本地验证脚本成功退出。
5. 候选文件 SHA256 已记录。
6. 当前父提交、代码 commit、数据版本和随机种子可追踪。
7. 没有仍处于 PENDING 的同类提交。
8. 已检查当日额度。
```

示例：

```powershell
python src\validate_submission.py submissions\submission.csv
Get-FileHash submissions\submission.csv -Algorithm SHA256
kaggle competitions submissions -c $competition --format json --page-size 200
```

## 5. 普通文件比赛提交

CSV、ZIP 或其他官方允许文件可直接提交：

```powershell
$file = "submissions\submission.csv"
$message = "exp_012 lgbm time-cv seed42 commit abc1234"
kaggle competitions submit -c $competition -f $file -m $message
```

推荐 message 格式：

```text
<exp_id> <parent> <model_or_method> <local_cv> <git_sha>
```

不要在 message 中写 token、绝对路径、账号密码或未公开数据来源。

查询结果：

```powershell
kaggle competitions submissions -c $competition
kaggle competitions submissions -c $competition --format json --page-size 200
```

只在状态变成 `COMPLETE` 后记录分数。`PENDING`、`ERROR` 和上传成功不是同一件事。

## 6. Code Competition / Notebook output 提交

### 6.1 kernel 目录

```text
kaggle_kernel/
├── kernel-metadata.json
└── notebook.ipynb
```

最小 metadata：

```json
{
  "id": "<kaggle_owner>/<kernel_slug>",
  "title": "<kernel_slug>",
  "code_file": "notebook.ipynb",
  "language": "python",
  "kernel_type": "notebook",
  "is_private": true,
  "enable_gpu": false,
  "enable_tpu": false,
  "enable_internet": false,
  "competition_sources": ["your-competition-slug"],
  "dataset_sources": [],
  "model_sources": []
}
```

Notebook 输入必须来自 `/kaggle/input/...`，输出写入 `/kaggle/working/`。不要在 Notebook 中读取 token。

### 6.2 推送 kernel

```powershell
kaggle kernels push -p kaggle_kernel
kaggle kernels status <kaggle_owner>/<kernel_slug>
```

等待 kernel 完成后下载并检查输出：

```powershell
New-Item -ItemType Directory -Force kaggle_output | Out-Null
kaggle kernels output <kaggle_owner>/<kernel_slug> `
  -p kaggle_output `
  -o `
  --file-pattern "submission.*"
```

### 6.3 从 kernel output 提交比赛

```powershell
kaggle competitions submit $competition `
  -k <kaggle_owner>/<kernel_slug> `
  -v <kernel_version> `
  -f submission.zip `
  -m "exp_012 code competition candidate"
```

`-f` 是 kernel 输出中的文件名，不是本机绝对路径。

## 7. 本机 NeuroGolf 自动化流程参考

本机 `E:\kagglegolf` 已验证过以下任务链，但这些脚本包含 NeuroGolf 特定字段，下一场比赛应迁移思想而不是直接照搬：

```powershell
python scripts\13_single_task_override.py ... --validate --pack --build-notebook --record
python scripts\19_submit_queue.py --exp-id <exp_id> --poll-after-submit --poll-timeout 300
python scripts\20_poll_submission_results.py --exp-id <exp_id>
python scripts\09_query_submission_history.py
```

可复用的设计：

- `manifest.json` 记录 parent、代码、数据、候选 SHA。
- `submission_queue.csv` 管理状态。
- 本地验证通过后才能入队。
- kernel 输出存在后才能提交 Code Competition。
- 失败生成 `MANUAL_SUBMIT_<exp_id>.md`，不自动重复消耗额度。
- `COMPLETE` 后计算相对 parent 的真实增益。

不建议复用的设计：

- 在提交脚本中自动 `git add .`、commit 和 push。
- 对网络错误执行无限重试。
- 把重复 package hash 当作普通候选再次提交。
- 多个高风险变更一次性打包，导致无法归因。

## 8. 推荐的通用提交状态机

```text
experimental
→ local_valid
→ format_valid
→ package_valid
→ ready_to_submit
→ submitted
→ pending
→ complete | error | rejected
```

每次状态变化记录：

```text
exp_id
parent_submission
git_sha
data_sha
artifact_sha
local_metric
submission_ref
public_score
private_score
status
failure_reason
```

## 9. 轮询与额度管理

简单轮询：

```powershell
do {
    $rows = kaggle competitions submissions -c $competition --format json --page-size 20 | ConvertFrom-Json
    $latest = $rows | Select-Object -First 1
    $latest | Select-Object ref,status,publicScore,date,description
    if ($latest.status -match "COMPLETE|ERROR|FAILED") { break }
    Start-Sleep -Seconds 30
} while ($true)
```

提交策略：

1. 每次提交前刷新 history。
2. 保留至少 10% 日额度用于回滚和最终集成。
3. 高风险候选单独提交。
4. 低风险、已证明可加的候选可以累计提交。
5. 出现 `ERROR` 后先读错误，不自动重试相同 package。
6. 使用 artifact SHA 防止重复提交。

## 10. 常见故障

### 403 / Rules not accepted

去网页接受规则；确认 token 对应正确账号。

### CLI 能列比赛但不能下载数据

通常是比赛规则、团队资格或数据许可未完成，不要重新生成 token 作为第一反应。

### Kernel push 成功但没有输出

检查：

```powershell
kaggle kernels status <owner>/<slug>
kaggle kernels output <owner>/<slug> -p kaggle_output -o
```

重点查看 Notebook 是否把文件写到了 `/kaggle/working/`。

### SubmissionStatus.ERROR

区分：

- 文件格式错误。
- Notebook 输出不存在。
- 运行时依赖或算子不兼容。
- Code Competition 推理超时或内存超限。
- 文件名与规则要求不一致。

保存日志，修复后只提交新 SHA 的 package。

### 本地分提高但线上下降

不要立即叠加更多改动。执行：

1. 回到已知 COMPLETE 父包。
2. 每个高风险变更单独消融。
3. 检查 CV 泄漏、时间泄漏、组间泄漏和隐藏输入域。
4. 更新实验记录后再决定是否继续。

## 11. 下一场比赛启动检查表

```text
[ ] Kaggle CLI 可运行
[ ] token 只存在用户目录或当前进程
[ ] 规则已接受
[ ] 数据和 sample submission 已下载
[ ] 评价指标与方向已确认
[ ] 本地 validator 已完成
[ ] baseline 可复现
[ ] CV 与测试分布匹配
[ ] 每个候选有 exp_id、Git SHA、artifact SHA
[ ] 普通提交还是 Code Competition 已确认
[ ] 提交额度与截止时间已记录
[ ] 第一次提交只验证完整链路
```
