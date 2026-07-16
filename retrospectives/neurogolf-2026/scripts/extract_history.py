from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


FIELD_SEP = "\x1f"
RECORD_SEP = "\x1e"
KAGGLE_TOKEN_RE = re.compile(r"KGAT_[A-Za-z0-9_]+")


def run(command: list[str], *, cwd: Path, check: bool = True) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=check,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    return result.stdout


def commit_rows(repo: Path) -> list[dict[str, str]]:
    raw = run(
        [
            "git",
            "log",
            "--all",
            "--reverse",
            f"--pretty=format:%H{FIELD_SEP}%P{FIELD_SEP}%aI{FIELD_SEP}%an{FIELD_SEP}%ae{FIELD_SEP}%s{RECORD_SEP}",
        ],
        cwd=repo,
    )
    rows: list[dict[str, str]] = []
    for record in raw.split(RECORD_SEP):
        record = record.strip()
        if not record:
            continue
        values = record.split(FIELD_SEP)
        if len(values) != 6:
            raise RuntimeError(f"unexpected git record: {record!r}")
        sha, parents, date, author, email, subject = values
        rows.append(
            {
                "sha": sha,
                "short_sha": sha[:8],
                "parents": parents,
                "parent_count": str(len(parents.split()) if parents else 0),
                "date": date,
                "author": author,
                "email": email,
                "subject": subject,
            }
        )
    return rows


def classify(subject: str) -> str:
    lower = subject.lower()
    if lower.startswith("merge pull request"):
        return "merge"
    if any(word in lower for word in ("scaffold", "dashboard", "mirror", "document", "report")):
        return "documentation_and_setup"
    if any(word in lower for word in ("harden", "validate", "parameterize", "kernel")):
        return "validation_and_delivery"
    if any(word in lower for word in ("rebase", "submission", "verify", "online")):
        return "integration_and_online_verification"
    if any(word in lower for word in ("model", "task", "onnx", "optimization", "score", "gain", "scan")):
        return "modeling_and_optimization"
    return "other"


def commit_stats(repo: Path, sha: str) -> dict[str, object]:
    raw = run(
        ["git", "show", "--numstat", "--format=", "--find-renames", sha],
        cwd=repo,
    )
    files: list[str] = []
    insertions = 0
    deletions = 0
    for line in raw.splitlines():
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        added, removed, path = parts
        files.append(path)
        if added.isdigit():
            insertions += int(added)
        if removed.isdigit():
            deletions += int(removed)
    areas = Counter()
    for path in files:
        parts = Path(path).parts
        if not parts:
            continue
        if len(parts) >= 2 and parts[0].lower().startswith("workplace"):
            areas[f"{parts[0]}/{parts[1]}"] += 1
        else:
            areas[parts[0]] += 1
    return {
        "files_changed": len(files),
        "insertions": insertions,
        "deletions": deletions,
        "top_areas": ";".join(name for name, _ in areas.most_common(5)),
        "changed_paths": ";".join(files),
    }


def is_in_main(repo: Path, sha: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "origin/main"],
        cwd=repo,
        capture_output=True,
    )
    return result.returncode == 0


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0]) if rows else []
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def redact_submission_secrets(value: object) -> object:
    if isinstance(value, str):
        return KAGGLE_TOKEN_RE.sub("[REDACTED_KAGGLE_TOKEN]", value)
    if isinstance(value, list):
        return [redact_submission_secrets(item) for item in value]
    if isinstance(value, dict):
        return {key: redact_submission_secrets(item) for key, item in value.items()}
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract reproducible NeuroGolf commit and submission history.")
    parser.add_argument("--source-repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--personal-email", default="2402686765@qq.com")
    parser.add_argument("--competition", default="neurogolf-2026")
    args = parser.parse_args()

    repo = args.source_repo.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)

    rows = commit_rows(repo)
    write_csv(output / "all_commits.csv", rows)

    personal: list[dict[str, object]] = []
    for row in rows:
        if row["email"].lower() != args.personal_email.lower():
            continue
        enriched: dict[str, object] = dict(row)
        enriched.update(commit_stats(repo, row["sha"]))
        enriched["category"] = classify(row["subject"])
        enriched["in_origin_main"] = is_in_main(repo, row["sha"])
        personal.append(enriched)
    write_csv(output / "personal_commits.csv", personal)

    authors = Counter(f"{row['author']} <{row['email']}>" for row in rows)
    summary = {
        "source_repo": "lljjcc426/NGC-work",
        "source_head": run(["git", "rev-parse", "origin/main"], cwd=repo).strip(),
        "all_commit_count": len(rows),
        "personal_email": args.personal_email,
        "personal_commit_count": len(personal),
        "personal_commits_in_origin_main": sum(bool(row["in_origin_main"]) for row in personal),
        "personal_commits_not_in_origin_main": [row["sha"] for row in personal if not row["in_origin_main"]],
        "author_counts": dict(authors.most_common()),
    }
    (output / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    submissions_raw = run(
        [
            "kaggle",
            "competitions",
            "submissions",
            "-c",
            args.competition,
            "--format",
            "json",
            "--page-size",
            "200",
        ],
        cwd=repo,
    )
    submissions = redact_submission_secrets(json.loads(submissions_raw))
    (output / "kaggle_submissions.json").write_text(
        json.dumps(submissions, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({**summary, "submission_count": len(submissions)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
