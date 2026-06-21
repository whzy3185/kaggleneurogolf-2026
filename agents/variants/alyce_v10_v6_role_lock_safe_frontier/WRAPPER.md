# Alyce V10 V6 Role Lock Safe Frontier Wrapper

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
- keeps 2P/3P presets unchanged;
- enables V10 role/source lock only in the 4P preset;
- writes V10 trace only when `ORBIT_V10_TRACE_PATH` is set;
- does not use network access;
- does not read secrets or external data.

Verification commands:

```text
python -m py_compile agents/variants/alyce_v10_v6_role_lock_safe_frontier/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v10_v6_role_lock_safe_frontier
```

Current status:

```text
local V10 candidate
not submitted
```
