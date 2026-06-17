# Parameter Selection

Date: 2026-06-17

## Selected Parameters

Current final candidate:

```text
base_safe_fallback
```

Effective parameters:

```yaml
use_profiler: false
use_counter_policy: false
use_supplemental_moves: false
enabled_policies: []
```

Entrypoint:

```text
local/agents/base_agent_entry
```

## Reason

The current adaptive parameter space is not ready for tuning. Stage 3 and Stage 5 showed:

- adaptive_full loses 3-97 to base in local 50-seed bidirectional evaluation;
- adaptive_defense_only loses 0-2 to base in a seed-1 bidirectional smoke;
- adaptive_no_profiler loses 0-2 to base in a seed-1 bidirectional smoke;
- all tested variants completed without timeout/errors, so selection is based on strategy quality rather than runtime failure.

## Rejected Settings

| setting | status | reason |
| --- | --- | --- |
| `neutral_rusher` branch | disabled | likely turns normal strong expansion into unsafe counterattacks |
| `turtle` branch | disabled | can increase expansion/comet weighting without proof of value |
| `comet_greedy` branch | disabled | not materially useful in profile traces and unproven in tournament |
| `overcommitter` branch | disabled | can raise commit ratio and counterattack bonus, conflicting with base stability |
| unrestricted supplemental moves | disabled | no budget reservation and negative direct evidence |
| defense-only supplement | not selected | initial smoke still loses to base |

## Next Selection Gate

Adaptive parameters may be reconsidered only after a reworked integration passes all gates:

1. Direct base-vs-candidate local tournament is at least close to even before public-opponent testing.
2. No policy branch can increase max commit ratio by default.
3. Supplemental ship budget is capped and visible in logs.
4. Public-opponent screen does not regress against Pilkwang, Tamrazov, and SigmaBorov.
5. 4-player smoke completes without obvious collapse.

Until then, `configs/final_agent.yaml` intentionally selects base fallback.
