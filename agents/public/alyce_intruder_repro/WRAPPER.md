# Alyce Intruder Reproduction Wrapper

This directory is intentionally not a wrapper around another local source. It is
a direct reproduction of the public Kaggle output package:

```text
alycemiki/light-ver-1200-simple-orbit-intruder
```

Entry point:

```python
def agent(obs):
    ...
```

Runtime notes:

- multi-file submission package;
- imports bundled `orbit_lite` from the same directory;
- imports `torch`;
- no local file reads in the agent path;
- no network access in the agent path;
- should be packaged as a tarball with `main.py` and `orbit_lite/` at archive
  root.
