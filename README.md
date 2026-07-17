# Kaggle NeuroGolf 2026 Archive

This repository was migrated from the complete
`whzy3185/kaggleorbit:retrospective/neurogolf-2026` branch on 2026-07-17.
The source commit and the initial target `main` commit are both
`007060e275a9ef0f3ca1965a9c78eb04bcea8dee`; the source branch was retained.

The NeuroGolf material is under
[`retrospectives/neurogolf-2026`](retrospectives/neurogolf-2026/README.md).
The consolidated public Code/Discussion review is in
[`KAGGLE_CODE_DISCUSSION_LESSONS.md`](retrospectives/neurogolf-2026/KAGGLE_CODE_DISCUSSION_LESSONS.md).

The remaining files are preserved because the requested migration covered the
entire source branch, including its inherited Orbit Wars workspace and history.

# Orbit Wars Adaptive Agent

This project is the Orbit Wars workspace for a first official submission
baseline and then targeted agent development.

Current rule:

- Keep this project outside the Nemotron repository.
- Keep official data, downloaded zips, logs, replays, and packaged submissions out of git.
- First submit the official starter as a connectivity baseline.
- After official feedback exists, build targeted content around a stronger baseline:
  physics-aware world model, opponent tendency profiler, and confidence-gated
  counter-policy modifiers.

Competition:

- Slug: `orbit-wars`
- Environment: `orbit_wars`
- Entry file: `main.py`
- Required function: `agent(obs)`
- Action format: `[[from_planet_id, direction_angle, num_ships], ...]`

Current official best in this workspace:

- Agent: `vkhydras_last_heuristic` single-file candidate
- Submission: `53772607`
- Public score: `810.6`
- Package: `dist/main.py`
- SHA256: `73679EC04C1521E2538FCF61013034B32729ED18CD0A5658C68090B65EC20049`

Previous completed best was `pilkwang_structured` submission `53767789`, latest
observed public score `678.9`.
