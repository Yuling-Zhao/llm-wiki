from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent
PACKAGED_TEMPLATE = PACKAGE_ROOT / "templates" / "default"
REPO_TEMPLATE = REPO_ROOT / "templates" / "default"
DEFAULT_TEMPLATE = PACKAGED_TEMPLATE if PACKAGED_TEMPLATE.exists() else REPO_TEMPLATE
REQUIRED_PATHS = (
    "AGENTS.md",
    "raw",
    "wiki",
    "wiki/index.md",
    "wiki/log.md",
    "wiki/overview.md",
)
LOG_HEADING_RE = re.compile(
    r"^## \[(?P<date>\d{4}-\d{2}-\d{2})\] (?P<kind>[^|]+) \| (?P<title>.+)$"
)
INDEX_ENTRY_RE = re.compile(
    r"^- \[(?P<title>[^\]]+)\]\((?P<path>[^)]+)\) - (?P<summary>.+)$"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="llm-wiki",
        description="Create and inspect local LLM-maintained wiki workspaces.",
    )
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Create a new wiki workspace.")
    init_parser.add_argument("path", help="Target directory for the workspace.")

    doctor_parser = subparsers.add_parser("doctor", help="Check workspace structure.")
    doctor_parser.add_argument("path", help="Workspace directory to check.")

    log_parser = subparsers.add_parser("log", help="Print recent wiki log entries.")
    log_parser.add_argument("path", help="Workspace directory.")
    log_parser.add_argument(
        "--limit", type=int, default=5, help="Number of recent entries to print."
    )

    index_parser = subparsers.add_parser("index", help="Print wiki index entries.")
    index_parser.add_argument("path", help="Workspace directory.")

    return parser


def init_workspace(path: Path) -> None:
    if path.exists() and any(path.iterdir()):
        raise ValueError(f"refusing to initialize non-empty directory: {path}")
    path.mkdir(parents=True, exist_ok=True)
    shutil.copytree(DEFAULT_TEMPLATE, path, dirs_exist_ok=True)


def missing_required_paths(path: Path) -> list[str]:
    return [relative for relative in REQUIRED_PATHS if not (path / relative).exists()]


def raw_contains_pdfs(path: Path) -> bool:
    raw_path = path / "raw"
    if not raw_path.is_dir():
        return False
    return any(
        file.is_file() and file.suffix.lower() == ".pdf"
        for file in raw_path.rglob("*")
    )


def parse_log_entries(log_path: Path) -> list[str]:
    entries: list[str] = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        match = LOG_HEADING_RE.match(line)
        if match:
            entries.append(
                f"{match.group('date')} {match.group('kind').strip()} | "
                f"{match.group('title').strip()}"
            )
    return entries


def parse_index_entries(index_path: Path) -> list[str]:
    entries: list[str] = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = INDEX_ENTRY_RE.match(line)
        if match:
            entries.append(
                f"{match.group('title').strip()} | "
                f"{match.group('path').strip()} | "
                f"{match.group('summary').strip()}"
            )
    return entries


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        if exc.code == 0:
            return 0
        raise

    try:
        if args.command == "init":
            init_workspace(Path(args.path))
            return 0
        if args.command == "doctor":
            missing = missing_required_paths(Path(args.path))
            if missing:
                for relative in missing:
                    print(f"missing: {relative}", file=sys.stderr)
                return 1
            if (
                raw_contains_pdfs(Path(args.path))
                and shutil.which("pdftotext") is None
            ):
                print(
                    "warning: raw/ contains PDF files but pdftotext was not found. "
                    "Install Poppler (macOS: brew install poppler; "
                    "Debian/Ubuntu: apt install poppler-utils), then convert "
                    "PDFs outside raw/ with pdftotext -layout before ingestion.",
                    file=sys.stderr,
                )
            print("workspace ok")
            return 0
        if args.command == "log":
            entries = parse_log_entries(Path(args.path) / "wiki" / "log.md")
            for entry in entries[-args.limit :]:
                print(entry)
            return 0
        if args.command == "index":
            entries = parse_index_entries(Path(args.path) / "wiki" / "index.md")
            for entry in entries:
                print(entry)
            return 0
        parser.print_help()
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
