# Alyce V6 Tuned Resubmit Wrapper

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
- enables V6 selected-action filter only in the 4P preset;
- uses a slightly earlier/wider 4P production-gap mode than the original V6:
  turn 42-180, production gap <= -5.0 or production rank >= 3;
- writes selected-action trace only when `ORBIT_V6_TRACE_PATH` is set;
- does not use network access;
- does not read secrets or external data.

Verification commands:

```text
python -m py_compile agents/variants/alyce_v6_tuned_resubmit_20260622/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v6_tuned_resubmit_20260622
```

Current status:

```text
V6-derived parameter-only resubmission candidate
not promoted unless official score beats the existing V6 best
```

