from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from orbitwars_agent.candidate_loader import load_candidate


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_load_single_file_candidate(tmp_path: Path) -> None:
    main_py = tmp_path / "main.py"
    _write(main_py, "def agent(obs):\n    return []\n")

    loaded = load_candidate(main_py)

    assert loaded.package_type == "single_file"
    assert loaded.main_py == main_py.resolve()
    assert loaded.agent({}) == []


def test_load_directory_candidate(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    _write(candidate / "main.py", "from helper import value\n\ndef agent(obs):\n    return value()\n")
    _write(candidate / "helper.py", "def value():\n    return []\n")

    loaded = load_candidate(candidate)

    assert loaded.package_type == "directory"
    assert loaded.agent({}) == []


def test_load_dataclass_candidate_registers_module(tmp_path: Path) -> None:
    main_py = tmp_path / "main.py"
    _write(
        main_py,
        "from dataclasses import dataclass\n"
        "@dataclass\n"
        "class Config:\n"
        "    value: int = 1\n"
        "def agent(obs):\n"
        "    Config()\n"
        "    return []\n",
    )

    loaded = load_candidate(main_py)

    assert loaded.agent({}) == []


def test_missing_main_py_fails_clearly(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="no main.py"):
        load_candidate(tmp_path / "missing")


def test_syspath_is_restored_after_directory_load(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    _write(candidate / "main.py", "def agent(obs):\n    return []\n")
    before = list(sys.path)

    load_candidate(candidate)

    assert sys.path == before
