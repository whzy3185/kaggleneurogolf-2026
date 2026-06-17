# Vkhydras Last Single-File Audit

Date: 2026-06-17

Candidate:

```text
agents/public/vkhydras_last_heuristic/main.py
```

No Kaggle submit command was run.

## Summary

```yaml
single_file_ready: yes
entrypoint: agent(obs, config=None)
local_smoke: pass
```

## Imports

Static import scan:

```python
import math
import os
import json
import time
from collections import defaultdict, namedtuple
```

The candidate does not import project `src/`, `external/`, Kaggle tokens,
network libraries, or third-party packages.

## Entrypoint

The file defines:

```python
def agent(obs, config=None):
    ...
```

The file also exports:

```python
__all__ = ["agent", "Planet", "Fleet"]
```

## Local Smoke

Compile check:

```powershell
python -m py_compile agents\public\vkhydras_last_heuristic\main.py
```

Result: pass.

Smoke command:

```powershell
python scripts\smoke_single_file_agent.py agents\public\vkhydras_last_heuristic\main.py --seed 11 --json
```

Result:

```json
{
  "has_agent": true,
  "sample_actions_ok": true,
  "env_status": "ok",
  "rewards": [1, -1],
  "turns": 86,
  "duration_s": 0.7435,
  "seed": 11,
  "passed": true
}
```

The smoke uses Kaggle's local `orbit_wars` environment against the built-in
`random` opponent. This is not an official leaderboard score.

## Static Risk Checks

No matches were found for:

```text
requests
urllib
socket
subprocess
print(
__file__
kaggle.json
token
cookie
password
secret
```

Known static findings:

- The file imports `os` and reads environment variables for feature toggles.
- `ORBIT_TRACE` can trigger local trace writes through `open(...)`.
- In normal Kaggle execution, `ORBIT_TRACE` is not expected to be set, so this
  path should not run. It remains a packaging/audit risk to keep visible.

## Timeout Risk

The agent uses a soft deadline derived from `config.actTimeout`:

```text
soft_budget = max(0.5, actTimeout * SOFT_DEADLINE_FRACTION)
```

The Phase 1 smoke completed in under one second. Larger local tournament
matches can take tens of seconds wall-clock because they run the full local env
and opponent code, but previous screens recorded no timeout status for this
candidate.

## License / Attribution Risk

License is not resolved in this phase. Existing metadata says:

```text
source: vkhydras/orbit-wars-heuristic-bots
license: unknown_no_license_file
```

Phase 4 must document whether competition submission use and public
redistribution are allowed, unclear, or blocked.
