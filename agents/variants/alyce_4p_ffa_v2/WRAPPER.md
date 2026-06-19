# Alyce 4P FFA V2 Wrapper

This directory is a self-contained multi-file candidate derived from
`agents/public/alyce_intruder_repro`.

Entry point:

```python
def agent(obs):
    ...
```

Runtime notes:

- imports bundled `orbit_lite` from the same directory;
- imports `torch`;
- keeps 2P/3P presets on the Alyce Light path;
- enables `enable_ffa_mission_filter=True` only for the 4P preset;
- converts contested-neutral veto into a score penalty except for severe traps;
- restores 4P `max_waves_per_turn=6` and relaxes source reserve caps versus v1;
- does not read local files;
- does not use network access;
- should be packaged as a tarball with `main.py` and `orbit_lite/` at archive
  root if it ever becomes a submission candidate.

Current status:

```text
research variant
not official score
not submit-ready until validation and confirmation report
```
