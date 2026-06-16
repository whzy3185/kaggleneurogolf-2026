from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any

_BASE_PATH = Path(__file__).resolve().parent / "public" / "pilkwang_structured" / "main.py"
_MODULE: ModuleType | None = None


def _load_module() -> ModuleType:
    global _MODULE
    if _MODULE is not None:
        return _MODULE
    spec = importlib.util.spec_from_file_location("pilkwang_structured_base", _BASE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load base agent from {_BASE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _MODULE = module
    return module


def agent(obs: Any, config: Any = None):
    module = _load_module()
    if config is None:
        return module.agent(obs)
    return module.agent(obs, config=config)


def build_world(obs: Any):
    module = _load_module()
    return module.build_world(obs)


__all__ = ["agent", "build_world"]

