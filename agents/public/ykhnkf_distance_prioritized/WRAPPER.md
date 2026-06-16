# Wrapper Notes: ykhnkf_distance_prioritized

This directory exposes the public source as:

```python
def agent(obs):
    ...
```

Wrapper action: extracted `submission.py` from `ykhnkf/distance-prioritized-agent-lb-max-score-1100` and stored it as `main.py`.

Known risks:

- Static extraction only; see `reports/PUBLIC_AGENT_LOADING.md` for smoke results.
- License was not available in Kaggle metadata during this audit unless noted elsewhere.
- Keep this source in the public-agent benchmark pool; do not treat its title score as our score.
