# NGC-work 本地清单

盘点时间：2026-07-17。

## 路径与仓库

| 项目 | 结果 |
| --- | --- |
| 原本地路径 | `E:\kongming\NGC-work` |
| 新本地路径 | `E:\kongming\kaggle` |
| 重命名状态 | 已完成；旧目录名不再存在 |
| Git 远端 | `git@github.com:lljjcc426/NGC-work.git` |
| 当前分支 | `codex/full400-hardening-round1` |
| 当前提交 | `63b208c` — Add exact ONNX contraction optimizations and closeout results |
| 工作树 | 重命名前后均无 Git 内容改动 |

顶层内容包括：

- `.github/`
- `assignments/`
- `neurogolf_400_tasks/`
- `workplace A/` 至 `workplace F/`
- `README.md`
- `requirements-dev.txt`

本地还发现两个相关 Git 工作区：

- `E:\kagglegolf` -> `git@github.com:whzy3185/kagglegolf.git`，包含大量赛末未提交实验状态；本次未改写或提交。
- `E:\orbitwars_adaptive_agent` -> `git@github.com:whzy3185/kaggleorbit.git`，其 `retrospective/neurogolf-2026` 分支已完整迁移到 `whzy3185/kaggleneurogolf-2026`。

## 旧绝对路径引用审计

重命名后仍有文本记录引用旧路径 `E:\kongming\NGC-work`：

| 仓库 | 文件数 | 主要类型 |
| --- | ---: | --- |
| `E:\kongming\kaggle` | 92 | 64 CSV、28 Markdown |
| `E:\kagglegolf` | 49 | 48 CSV、1 Markdown |

这些引用主要位于实验 ledger、candidate manifest、cost diff 和复盘报告，记录的是当时真实的 artifact 来源路径。为保持证据链与提交复盘的历史真实性，本次没有批量改写这些记录。后续若恢复旧实验，应将路径解析逻辑改为仓库相对路径或显式 workspace root，而不是继续写新的机器绝对路径。

## 后续约定

新脚本和新文档使用：

1. 仓库相对路径；或
2. 环境变量定义的 workspace root；或
3. manifest 中同时记录相对路径和 artifact SHA。

不再新增 `E:\kongming\NGC-work` 绝对路径。
