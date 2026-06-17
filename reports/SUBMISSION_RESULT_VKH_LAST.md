# Vkhydras Last Official Submission Result

Date: 2026-06-17

## Status

The user explicitly requested direct upload after local validation was in
progress. The request was to stop local evaluation and upload directly.

No training process exists for this candidate. `vkhydras_last_heuristic` is a
public heuristic single-file agent. The interrupted process was local match
evaluation, not model training.

## Submission

```yaml
competition: orbit-wars
submission_id: 53772197
file: dist/main.py
message: vkhydras_last_single_file_candidate_d7d937e
sha256: 73679EC04C1521E2538FCF61013034B32729ED18CD0A5658C68090B65EC20049
source_commit: d7d937e
submitted: true
submit_command: kaggle competitions submit -c orbit-wars -f dist\main.py -m "vkhydras_last_single_file_candidate_d7d937e"
```

The user reported the pending state as problematic and requested a resubmit.
Kaggle CLI help did not expose a cancel/stop/withdraw command for pending
submissions. A single resubmission was uploaded with the same `dist/main.py`.

The user then requested format verification before another upload. `dist/main.py`
passed:

- sha256 check;
- `def agent(obs, config=None)` presence check;
- `python -m py_compile dist\main.py`;
- banned-pattern scan for `kaggle.json`, `open(`, network libraries, secrets,
  external/data/output paths, and debug print;
- `scripts/smoke_single_file_agent.py dist\main.py --seed 33`;
- starter file-agent smoke, seed 13, bidirectional.

## Current Kaggle Status

Latest checked CLI output from this workspace:

```yaml
initial_submission:
  submission_id: 53772197
  status: SubmissionStatus.PENDING
  public_score: null
  private_score: null
resubmission:
  submission_id: 53772607
  message: vkhydras_last_single_file_candidate_d7d937e_resubmit1
  status: SubmissionStatus.COMPLETE
  public_score: 810.6
  private_score: null
format_checked_submission:
  submission_id: 53772702
  message: vkhydras_last_single_file_candidate_d7d937e_formatcheck
  status: SubmissionStatus.COMPLETE
  public_score: 763.8
  private_score: null
```

Both completed Vkhydras Last submissions used the same `dist/main.py` sha256:

```text
73679EC04C1521E2538FCF61013034B32729ED18CD0A5658C68090B65EC20049
```

Kaggle rating values can drift between CLI checks. In the latest query,
submission `53772607` is the current completed official best in this workspace.
The older initial submission `53772197` remains pending.

## Current Completed Official Best

```yaml
agent: vkhydras_last_heuristic single-file candidate
submission_id: 53772607
status: SubmissionStatus.COMPLETE
public_score_latest_cli: 810.6
```

The previous Pilkwang best is:

```yaml
agent: pilkwang_structured single-file fallback
submission_id: 53767789
status: SubmissionStatus.COMPLETE
public_score_latest_cli: 678.9
```

Vkhydras Last `53772607` beats the latest observed Pilkwang score by `131.7`
public rating points.

## Local Validation State Before Upload

The user stopped further local testing before the planned Phase 3/4/5 reports
were completed. Completed local checks before upload included:

- single-file source audit: pass;
- package generation: pass;
- `dist/main.py` py_compile: pass;
- banned pattern scan on `dist/main.py`: no matches;
- `dist/main.py` smoke vs random through `scripts/smoke_single_file_agent.py`:
  pass;
- partial local tournament validation:
  - source vs dist, 10 seeds bidirectional: dist `9`, source `6`, draws `5`,
    errors `0`;
  - dist vs Pilkwang, 50 seeds bidirectional: dist `99`, Pilkwang `1`, errors
    `0`;
  - dist vs Tamrazov, 10 seeds bidirectional: dist `20`, Tamrazov `0`, errors
    `0`;
  - dist vs SigmaBorov, 10 seeds bidirectional: dist `20`, SigmaBorov `0`,
    errors `0`;
  - dist vs ykhnkf, 10 seeds bidirectional: dist `20`, ykhnkf `0`, errors `0`;
  - dist vs vkhydras_peak, 10 seeds bidirectional: dist `15`, peak `5`, errors
    `0`;
  - 4-player position-0 smoke, seeds 1-3: dist won `2/3`, errors `0`.

These are local results only. They are not official leaderboard scores.

## Next Check

Poll:

```powershell
kaggle competitions submissions -c orbit-wars
```

When `53772197` changes to `COMPLETE` or `ERROR`, update:

```text
reports/SCORECARD.md
reports/SUBMISSION_RESULT_VKH_LAST.md
```

and commit the final status.
