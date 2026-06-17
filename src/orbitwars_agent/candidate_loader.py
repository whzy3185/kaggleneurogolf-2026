from __future__ import annotations

import importlib.util
import sys
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Callable, Iterator


@dataclass(frozen=True)
class LoadedCandidate:
    source_path: Path
    candidate_dir: Path
    main_py: Path
    package_type: str
    module_name: str
    module: ModuleType
    agent: Callable


def candidate_main(path: Path) -> tuple[Path, Path, str]:
    resolved = path.resolve()
    if resolved.is_dir():
        main_py = resolved / "main.py"
        package_type = "directory"
        candidate_dir = resolved
    else:
        main_py = resolved
        package_type = "single_file"
        candidate_dir = resolved.parent
    if not main_py.is_file():
        raise FileNotFoundError(f"Candidate has no main.py: {resolved}")
    return main_py, candidate_dir, package_type


@contextmanager
def _temporary_syspath(path: Path) -> Iterator[None]:
    path_s = str(path)
    old_path = list(sys.path)
    if path_s in sys.path:
        sys.path.remove(path_s)
    sys.path.insert(0, path_s)
    try:
        yield
    finally:
        sys.path[:] = old_path


def _clear_local_package_modules(candidate_dir: Path) -> None:
    """Avoid cross-candidate leakage for bundled packages such as orbit_lite."""
    package_names = []
    for child in candidate_dir.iterdir() if candidate_dir.is_dir() else []:
        if child.is_dir() and (child / "__init__.py").is_file():
            package_names.append(child.name)
    for name in list(sys.modules):
        root = name.split(".", 1)[0]
        if root in package_names:
            del sys.modules[name]


def load_candidate(path: Path) -> LoadedCandidate:
    main_py, candidate_dir, package_type = candidate_main(Path(path))
    _clear_local_package_modules(candidate_dir)
    module_name = f"orbitwars_candidate_{uuid.uuid4().hex}"
    spec = importlib.util.spec_from_file_location(module_name, main_py)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load candidate module from {main_py}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    with _temporary_syspath(candidate_dir):
        spec.loader.exec_module(module)
    agent_fn = getattr(module, "agent", None)
    if agent_fn is None or not callable(agent_fn):
        raise AttributeError(f"{main_py} does not expose callable agent(obs)")
    return LoadedCandidate(
        source_path=Path(path).resolve(),
        candidate_dir=candidate_dir,
        main_py=main_py,
        package_type=package_type,
        module_name=module_name,
        module=module,
        agent=agent_fn,
    )
