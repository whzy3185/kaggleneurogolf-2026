# Alyce V9 4P Mission Router Wrapper

Entry point:

```python
def agent(obs):
    ...
```

Runtime notes:

- self-contained multi-file candidate;
- imports bundled `orbit_lite`;
- imports `torch`;
- starts from official-best `alyce_v6_prod_gap_mode`;
- enables V9 mission router only in the 4P preset;
- leaves 2P and 3P configs unchanged;
- writes selected-action trace only when `ORBIT_V9_TRACE_PATH`,
  `ORBIT_V6_TRACE_PATH`, or `ORBIT_V5_TRACE_PATH` is set;
- does not use network access;
- does not read secrets or external data.

Verification commands:

```text
python -m py_compile agents/variants/alyce_v9_4p_mission_router/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v9_4p_mission_router
```

Current status:

```text
local research candidate
not submitted
```
