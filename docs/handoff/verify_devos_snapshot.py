"""Run the handoff's focused local checks in a disposable DevOS clone."""

# Import the command-line argument tools supplied with Python.
import argparse
# Import file-path support supplied with Python.
from pathlib import Path
# Import the tool used to run Git and Python without a command shell.
import subprocess
# Use the same Python interpreter that started this script.
import sys

# List only the targeted checks; this is not the complete GitHub CI suite.
CHECKS = [
    'devos-bootstrap.py',
    'test-devos-bootstrap.py',
    'test-human-language-interpreter.py',
    'test-semantic-goal-to-plan.py',
    'test-step-readiness-orchestrator.py',
    'test-p17-end-to-end.py',
    'test-production-e2e-harness.py',
    'test-failure-recovery-proof.py',
    'test-multi-session-continuation.py',
    'test-multi-session-two-process.py',
    'test-controlled-remote-mutation-proof.py',
    'test-github-reference.py',
    'test-external-runtime-bridge.py',
    'test-adaptive-verification.py',
    'test-adaptive-self-heal.py',
]


def main():
    # Explain the required input to the person running the script.
    parser = argparse.ArgumentParser(description=__doc__)
    # Require a path to a disposable repository clone.
    parser.add_argument('repository', type=Path)
    # Read the argument and resolve it to an absolute directory.
    root = parser.parse_args().repository.resolve()
    try:
        # Ask Git for the configured remote; never infer identity from the folder name.
        origin = subprocess.check_output(
            ['git', 'remote', 'get-url', 'origin'], cwd=root, text=True
        ).strip().removesuffix('.git')
        # Accept the two standard GitHub URL formats for this exact repository.
        allowed = [
            'https://github.com/zzpsah/chatgpt-development-os',
            'git@github.com:zzpsah/chatgpt-development-os',
        ]
        # Stop if the repository does not have the expected identity.
        if origin not in allowed:
            print('STOP: origin does not match the canonical DevOS repository.')
            return 2
        # Record the exact version before running any tests.
        head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
        # Show the version so results can be linked to source.
        print('Starting repository SHA:', head)
        # Record the worktree status for comparison afterward.
        before = subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, text=True)
        # Count failed script invocations, not individual assertions.
        failed = 0
        # Run the checked-in scripts in a simple, visible sequence.
        for name in CHECKS:
            # Print the current check before starting it.
            print('\nRunning:', name, flush=True)
            try:
                # Capture real output; allow at most two minutes for each check.
                result = subprocess.run(
                    [sys.executable, str(root / 'tools' / name)],
                    cwd=root, text=True, capture_output=True, timeout=120, check=False
                )
                # Show standard output even when a script fails.
                print(result.stdout)
                # Show error output if the script produced any.
                if result.stderr:
                    print(result.stderr)
                # Print and count the actual process result.
                print('Exit code:', result.returncode)
                if result.returncode != 0:
                    failed += 1
            except subprocess.TimeoutExpired:
                # Record a timeout as a failure and continue to the next check.
                print('FAILED: check exceeded 120 seconds.')
                failed += 1
        # Check whether tracked or untracked worktree state changed.
        after = subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, text=True)
        print('\nWorktree status unchanged:', before == after)
        # Report the status directly if something changed.
        if before != after:
            print(after)
        # Report the number of script processes that failed.
        print('Failed script invocations:', failed)
        # Return a standard success or failure code to the terminal.
        return 1 if failed else 0
    except (OSError, subprocess.CalledProcessError) as error:
        # Explain missing Git/Python, invalid directories, and Git command failures.
        print('STOP: unable to complete verification:', error)
        return 2


# Run only when invoked as a script, not when imported by another program.
if __name__ == '__main__':
    raise SystemExit(main())
