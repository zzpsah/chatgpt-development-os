#!/usr/bin/env python3
"""Synchronize durable Development OS context in the checked-out project."""
from __future__ import annotations

import fnmatch
import os
import subprocess
from pathlib import Path

ROOT = Path.cwd()
CONTEXT = ROOT / os.environ.get("DEVOS_CONTEXT_DIRECTORY", ".ai")
DEFAULT_PATTERNS = [
    "src/**", "app/**", "pages/**", "components/**", "api/**", "lib/**",
    "public/**", "supabase/**", "migrations/**", "prisma/**", "db/**",
    "database/**", "package.json", "package-lock.json", "pnpm-lock.yaml",
    "yarn.lock", "pyproject.toml", "requirements.txt", "poetry.lock",
    "Cargo.toml", "Cargo.lock", "go.mod", "go.sum", "composer.json",
    "pom.xml", "build.gradle", "Dockerfile", "*.csproj", "*.sln",
    ".github/workflows/**",
]


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=check)


def git(*args: str, check: bool = True) -> str:
    return run("git", *args, check=check).stdout.strip()


def changed_files() -> list[str]:
    before = os.environ.get("DEVOS_BEFORE_SHA", "")
    head = git("rev-parse", "HEAD")
    if before and run("git", "cat-file", "-e", f"{before}^{{commit}}", check=False).returncode == 0:
        raw = git("diff", "--name-only", before, head)
    else:
        raw = git("diff-tree", "--no-commit-id", "--name-only", "-r", head)
    return [line for line in raw.splitlines() if line and not line.startswith(".ai/")]


def meaningful(paths: list[str]) -> bool:
    supplied = os.environ.get("DEVOS_MEANINGFUL_PATTERNS", "")
    patterns = [p.strip() for p in supplied.split(",") if p.strip()] if supplied else DEFAULT_PATTERNS
    return any(any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns) for path in paths)


def ensure_file(path: Path, content: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def update_current_state(commit_sha: str, subject: str, date: str) -> None:
    state = CONTEXT / "CURRENT-STATE.md"
    ensure_file(state, "# Current State\n\nLast verified: never\n")
    text = state.read_text(encoding="utf-8")
    marker = "## Last automated change"
    if marker in text:
        text = text.split(marker, 1)[0].rstrip() + "\n\n"
    else:
        text = text.rstrip() + "\n\n"
    text += (
        f"{marker}\n"
        f"- Commit: {commit_sha}\n"
        f"- Change: {subject}\n"
        f"- Date: {date}\n"
        "- Durable context synchronization: completed\n"
    )
    state.write_text(text, encoding="utf-8")


def update_changelog(commit_sha: str, subject: str, author: str, date: str, paths: list[str], is_meaningful: bool) -> None:
    changelog = CONTEXT / "CHANGELOG.md"
    ensure_file(changelog, "# Project Change Log\n\nAutomatically maintained by Development OS.\n")
    old = changelog.read_text(encoding="utf-8")
    files = "\n".join(f"- `{p}`" for p in paths) if paths else "- (no application files detected)"
    entry = (
        f"## {date} — {subject}\n"
        f"- Commit: {commit_sha}\n"
        f"- Author: {author}\n"
        f"- Classification: {'meaningful' if is_meaningful else 'routine'}\n"
        f"- Changed files:\n{files}\n\n"
    )
    changelog.write_text(entry + old, encoding="utf-8")


def update_index(commit_sha: str, subject: str, author: str, date: str, branch: str, is_meaningful: bool) -> None:
    index = CONTEXT / "STATE-INDEX.md"
    required = ["AGENTS.md", "manifest.yaml", "PROJECT.md", "CURRENT-STATE.md", "TASKS.md"]
    health = "healthy" if all((ROOT / name).exists() if name == "AGENTS.md" else (CONTEXT / name).exists() for name in required) else "incomplete"
    sessions = CONTEXT / "SESSIONS"
    latest = sorted(p.name for p in sessions.glob("*.md"))[-1] if sessions.exists() and list(sessions.glob("*.md")) else "none"
    index.write_text(
        "# Project State Index\n\n"
        "Generated automatically by Development OS.\n\n"
        "> Deterministic repository/context evidence only; inspect project state, source, and Git before semantic conclusions.\n\n"
        "## Repository\n"
        f"- Branch: {branch}\n- HEAD: {commit_sha}\n- Last commit: {subject}\n- Last commit date: {date}\n- Last commit author: {author}\n\n"
        "## Context health\n"
        f"- Overall: {health}\n"
        + "".join(f"- `{name}`: {'present' if ((ROOT / name) if name == 'AGENTS.md' else (CONTEXT / name)).exists() else 'missing'}\n" for name in required)
        + f"- `CHANGELOG.md`: {'present' if (CONTEXT / 'CHANGELOG.md').exists() else 'missing'}\n"
        + f"- `SESSIONS/`: {'present' if sessions.exists() else 'missing'}\n\n"
        f"## Recent activity\n- Latest session: {latest}\n- Meaningful change detected: {str(is_meaningful).lower()}\n\n"
        "## Recovery\n"
        "1. Read `AGENTS.md` and `.ai/manifest.yaml`.\n"
        "2. Read `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and relevant decisions/architecture.\n"
        "3. Inspect source code and Git history.\n"
        "4. Treat this index as evidence, not semantic authority.\n",
        encoding="utf-8",
    )


def main() -> None:
    CONTEXT.mkdir(parents=True, exist_ok=True)
    sha = git("rev-parse", "HEAD")
    subject = git("log", "-1", "--pretty=%s")
    author = git("log", "-1", "--pretty=%an")
    date = git("log", "-1", "--date=short", "--pretty=%ad")
    branch = os.environ.get("GITHUB_REF_NAME", git("branch", "--show-current"))
    paths = changed_files()
    is_meaningful = meaningful(paths)

    update_changelog(sha, subject, author, date, paths, is_meaningful)
    if is_meaningful:
        update_current_state(sha, subject, date)
    update_index(sha, subject, author, date, branch, is_meaningful)

    subprocess.run(["git", "config", "user.name", "development-os[bot]"], cwd=ROOT, check=True)
    subprocess.run(["git", "config", "user.email", "development-os[bot]@users.noreply.github.com"], cwd=ROOT, check=True)
    subprocess.run(["git", "add", str(CONTEXT / "CHANGELOG.md"), str(CONTEXT / "STATE-INDEX.md")] + ([str(CONTEXT / "CURRENT-STATE.md")] if (CONTEXT / "CURRENT-STATE.md").exists() else []), cwd=ROOT, check=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if diff.returncode == 0:
        print("OK: no durable context changes needed")
        return
    subprocess.run(["git", "commit", "-m", "chore: sync project AI context [devos-context-sync]"], cwd=ROOT, check=True)
    subprocess.run(["git", "push"], cwd=ROOT, check=True)
    print("OK: durable project context synchronized")


if __name__ == "__main__":
    main()
