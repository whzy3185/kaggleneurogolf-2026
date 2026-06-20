# Alyce V7 Continuous Recovery Wrapper

Entry point:

```python
def agent(obs):
    ...
```

Runtime notes:

- self-contained multi-file candidate;
- imports bundled `orbit_lite`;
- imports `torch`;
- starts from `alyce_v6_prod_gap_mode`;
- enables V7 selected-action filter only in the 4P preset;
- adds a 4P turn 35-190 continuous recovery mode when our production is already
  behind or rank 2+;
- writes selected-action trace only when `ORBIT_V7_TRACE_PATH` is set;
- does not use network access;
- does not read secrets or external data.

Verification commands:

```text
python -m py_compile agents/variants/alyce_v7_continuous_recovery/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v7_continuous_recovery
```

Current status:

```text
local research candidate
not submitted
```

