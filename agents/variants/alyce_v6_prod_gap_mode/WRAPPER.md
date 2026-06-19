# Alyce V6 Production Gap Mode Wrapper

Entry point:

```python
def agent(obs):
    ...
```

Runtime notes:

- self-contained multi-file candidate;
- imports bundled `orbit_lite`;
- imports `torch`;
- starts from `alyce_4p_ffa_v2`;
- enables V6 selected-action filter only in the 4P preset;
- adds a 4P turn 45-170 production-gap mode when our production is already
  behind or rank 3/4;
- writes selected-action trace only when `ORBIT_V6_TRACE_PATH` is set;
- does not use network access;
- does not read secrets or external data.

Verification commands:

```text
python -m py_compile agents/variants/alyce_v6_prod_gap_mode/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v6_prod_gap_mode
```

Current status:

```text
local research candidate
not submitted
```

