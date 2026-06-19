# Alyce V5 V2 Trace Filter Wrapper

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
- enables V5 selected-action filter only in the 4P preset;
- writes selected-action trace only when `ORBIT_V5_TRACE_PATH` is set;
- does not use network access;
- does not read secrets or external data.

Verification commands:

```text
python -m py_compile agents/variants/alyce_v5_v2_trace_filter/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v5_v2_trace_filter
```

Current status:

```text
local research candidate
not submitted
```

