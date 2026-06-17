import importlib.util
import os
import sys
from pathlib import Path

ROOT = None
if "__file__" in globals():
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
else:
    cwd = os.getcwd()
    candidates = [
        cwd,
        os.path.abspath(os.path.join(cwd, "..")),
        os.path.abspath(os.path.join(cwd, "..", "..")),
    ]
    for candidate in candidates:
        if os.path.isfile(os.path.join(candidate, "agents", "base_agent.py")):
            ROOT = candidate
            break

if ROOT is None:
    ROOT = os.getcwd()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

ROOT = Path(ROOT)
BASE_PATH = ROOT / "agents" / "base_agent.py"
MODULE = None


def _load():
    global MODULE
    if MODULE is not None:
        return MODULE
    spec = importlib.util.spec_from_file_location("orbitwars_base_agent_entry", BASE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load base agent from {BASE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    MODULE = module
    return module


def agent(obs, config=None):
    module = _load()
    if config is None:
        return module.agent(obs)
    return module.agent(obs, config=config)
