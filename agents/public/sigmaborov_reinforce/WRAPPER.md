# Wrapper Notes: sigmaborov_reinforce

This directory exposes the public source as:

```python
def agent(obs):
    ...
```

Wrapper action: extracted `submission.py` from `sigmaborov/lb-958-1-orbit-wars-2026-reinforce` and stored it as `main.py`.

Known risks:

- Static extraction only; see `reports/PUBLIC_AGENT_LOADING.md` for smoke results.
- License was not available in Kaggle metadata during this audit unless noted elsewhere.
- Keep this source in the public-agent benchmark pool; do not treat its title score as our score.
