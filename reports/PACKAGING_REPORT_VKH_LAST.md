# Packaging Report: Vkhydras Last

Date: 2026-06-17

No Kaggle submit command was run.

## Candidate

```yaml
candidate: vkhydras_last_heuristic
source_path: agents/public/vkhydras_last_heuristic/main.py
output_path: dist/main.py
entrypoint: agent
```

## Packaging Command

```powershell
python scripts\package_single_file_agent.py --source agents\public\vkhydras_last_heuristic\main.py --output dist\main.py
```

Result:

```json
{
  "ok": true,
  "sha256": "73679ec04c1521e2538fcf61013034b32729ed18cd0a5658c68090b65ec20049",
  "bytes": 286646,
  "line_count": 6105,
  "entrypoint": "agent",
  "banned_findings": [],
  "stripped_orbit_trace_blocks": 1
}
```

## Packaging Sanitization

The source file contains an optional `ORBIT_TRACE` branch that writes local trace
logs with `open(...)` only when the environment variable is set.

Because this task lists `open(` as a banned packaging pattern, the package
script removes that optional trace block from `dist/main.py`. The source file is
not changed. This should not affect normal game behavior because `ORBIT_TRACE`
is not part of standard Kaggle execution.

## Output Metadata

```yaml
sha256: 73679EC04C1521E2538FCF61013034B32729ED18CD0A5658C68090B65EC20049
size_bytes: 286646
line_count_python_splitlines: 6105
```

## Checks

Compile:

```powershell
python -m py_compile dist\main.py
```

Result: pass.

Banned pattern scan:

```powershell
rg -n "kaggle\.json|open\(|requests|urllib|socket|external/|outputs/|data/" dist\main.py
```

Result: no matches.

Smoke:

```powershell
python scripts\smoke_single_file_agent.py dist\main.py --seed 12 --json
```

Result:

```json
{
  "has_agent": true,
  "sample_actions_ok": true,
  "env_status": "ok",
  "rewards": [1, -1],
  "turns": 95,
  "duration_s": 0.8152,
  "seed": 12,
  "passed": true
}
```

## Known Risks

- Local smoke is not an official Kaggle score.
- `dist/main.py` is sanitized relative to source by removing optional trace
  writes. Phase 3 must verify packaged behavior against source.
- License remains unresolved until Phase 4.
- Existing `dist/*.tar.gz` files are ignored and are not part of this
  single-file candidate.
