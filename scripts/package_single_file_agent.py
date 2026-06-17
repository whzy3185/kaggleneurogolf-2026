from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path


BANNED_PATTERNS = [
    "kaggle.json",
    "open(",
    "requests",
    "urllib",
    "socket",
    "external/",
    "outputs/",
    "data/",
]


def _contains_agent_function(source_text: str) -> bool:
    tree = ast.parse(source_text)
    return any(isinstance(node, ast.FunctionDef) and node.name == "agent" for node in tree.body)


def _strip_orbit_trace(source_text: str) -> tuple[str, int]:
    lines = source_text.splitlines(keepends=True)
    output: list[str] = []
    stripped = 0
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if 'if os.environ.get("ORBIT_TRACE"):' not in line:
            output.append(line)
            idx += 1
            continue

        base_indent = len(line) - len(line.lstrip(" "))
        stripped += 1
        idx += 1
        while idx < len(lines):
            next_line = lines[idx]
            if next_line.strip() == "":
                idx += 1
                continue
            next_indent = len(next_line) - len(next_line.lstrip(" "))
            if next_indent <= base_indent:
                break
            idx += 1
    return "".join(output), stripped


def _scan_banned(path: Path, text: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for pattern in BANNED_PATTERNS:
        start = 0
        while True:
            offset = text.find(pattern, start)
            if offset == -1:
                break
            line_no = text.count("\n", 0, offset) + 1
            findings.append({"path": str(path), "pattern": pattern, "line": line_no})
            start = offset + len(pattern)
    return findings


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package(source: Path, output: Path) -> dict[str, object]:
    if not source.is_file():
        raise FileNotFoundError(source)

    source_text = source.read_text(encoding="utf-8")
    if not _contains_agent_function(source_text):
        raise ValueError(f"{source} does not define agent(...)")

    packaged_text, stripped_trace_blocks = _strip_orbit_trace(source_text)
    if not _contains_agent_function(packaged_text):
        raise ValueError("packaged output lost agent(...) entrypoint")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(packaged_text, encoding="utf-8", newline="\n")

    banned = _scan_banned(output, packaged_text)
    if banned:
        return {
            "source": str(source),
            "output": str(output),
            "ok": False,
            "error": "banned patterns found",
            "banned_findings": banned,
            "stripped_orbit_trace_blocks": stripped_trace_blocks,
        }

    return {
        "source": str(source),
        "output": str(output),
        "ok": True,
        "sha256": _sha256(output),
        "bytes": output.stat().st_size,
        "line_count": packaged_text.count("\n") + (0 if packaged_text.endswith("\n") else 1),
        "entrypoint": "agent",
        "banned_findings": [],
        "stripped_orbit_trace_blocks": stripped_trace_blocks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = package(Path(args.source), Path(args.output))
    print(json.dumps(result, indent=2))
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
