# Alyce Intervention V4 Wrapper

Entry point:

```python
def agent(obs):
    ...
```

Submission shape:

- Multi-file candidate.
- `main.py` imports local package directory `orbit_lite/`.
- Intended package format is a directory or tar.gz preserving `main.py` and
  `orbit_lite/` at submission root.

Current verification commands:

```text
python -m py_compile agents/variants/alyce_intervention_v4/main.py
python scripts/smoke_candidate.py agents/variants/alyce_intervention_v4
```

Risk:

- V4 is a new candidate and has not been submitted.
- It intentionally changes 4P candidate ordering; this may disturb Alyce
  Intervention's tuned tempo.
- It contains local trace counters in memory but does not write logs during
  Kaggle evaluation.
- Do not submit before smoke, short 2P non-regression, and 4P replay-inspired
  screening against V2/Alyce/Intervention baselines.
