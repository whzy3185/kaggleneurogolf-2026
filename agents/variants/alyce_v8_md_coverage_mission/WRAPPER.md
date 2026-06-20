# Alyce V8 MD Coverage Mission Wrapper

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
- only changes 4P preset behavior;
- exposes 4P multi-size send candidates;
- enables replay-risk selected-action replacement;
- writes top-candidate labels only when `ORBIT_V8_TRACE_PATH` is set;
- does not use network access;
- does not read secrets or external data.

Verification commands:

```text
python -m py_compile agents/variants/alyce_v8_md_coverage_mission/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v8_md_coverage_mission
```

Current status:

```text
local research candidate
not submitted
```
