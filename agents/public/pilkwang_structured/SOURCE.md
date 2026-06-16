# Pilkwang Structured Baseline Source

Date imported: 2026-06-16

```yaml
source_id: pilkwang_structured
name: Pilkwang Structured Baseline v11
author: Pilkwang Kim
kernel_slug: pilkwang/orbit-wars-structured-baseline
kernel_version: 45
license: Apache 2.0
source_path: external/orbit-wars-lab/agents/external/pilkwang-structured/main.py
tracked_path: agents/public/pilkwang_structured/main.py
sha256: 0F297612110D28A5A15F4564A1C36F87FDB5C895D557DE10876AF6F64D5E4B4C
```

Reason for import:

- Best local smoke round-robin result among P0/P1 candidates: 8 wins, 0 losses,
  0 errors over 8 games.
- Clear architecture: Physics + WorldModel + Strategy.
- Exposes `agent(obs, config=None)` and `build_world(obs)`.
- Apache 2.0 in `orbit-wars-lab` metadata.

Do not treat the author claimed LB score as our score.

