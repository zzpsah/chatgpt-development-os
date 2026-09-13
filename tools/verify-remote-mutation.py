#!/usr/bin/env python3
"""Contract checks for Remote Mutation Controls v1."""
from pathlib import Path
import importlib.util
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def require(text, needles, source):
    for needle in needles:
        assert needle in text, f"missing {needle!r} in {source}"

contract = read("core/remote-mutation-controls.md")
bridge_contract = read("core/runtime-adapter-bridge.md")
profile = read("adapters/github-integration.md")
reference = read("adapters/github-reference.py")
bridge = read("tools/runtime-adapter-bridge.py")
controlled = read("core/controlled-remote-mutation-proof.md")

require(contract, [
    "explicit authorization",
    "ALREADY_GRANTED",
    "Security Gate",
    "expected current state",
    "optimistic concurrency",
    "must not be retried automatically",
    "UNVERIFIED",
    "actual provider evidence",
    "fresh remote readback",
    "MUTATION_REPLAY_FORBIDDEN",
    "never stored in `.ai`",
], "core/remote-mutation-controls.md")
require(bridge_contract, [
    "github.inspect.file",
    "github.mutate.file",
    "ALREADY_GRANTED",
    "security_gate: PASS",
    "expected current file SHA",
    "without automatic retry",
    "fresh `github.inspect.file` readback",
    "UNVERIFIED",
], "core/runtime-adapter-bridge.md")
require(profile, [
    "github.inspect.file",
    "github.mutate.file",
    "expected current file SHA",
    "authorization: ALREADY_GRANTED",
    "security_gate: PASS",
    "does not automatically retry",
    "post-mutation readback verification",
], "adapters/github-integration.md")
require(reference, [
    "READ_CAPABILITIES",
    "github.inspect.file",
    "MUTATION_CAPABILITIES",
    "github.mutate.file",
    "def inspect_file",
    "def mutate_file",
    "ALREADY_GRANTED",
    "expected_sha",
    "UNVERIFIED",
], "adapters/github-reference.py")
require(bridge, [
    "github.inspect.file",
    "github.mutate.file",
    "ALREADY_GRANTED",
    'request.get("security_gate") != "PASS"',
    "expected_sha",
], "tools/runtime-adapter-bridge.py")
require(controlled, [
    "DEVOS-CONTROLLED-MUTATION-v1",
    "one mutation attempt",
    "fresh provider readback",
    "MUTATION_REPLAY_FORBIDDEN",
    "VERIFIED",
    "HOLD",
], "core/controlled-remote-mutation-proof.md")

spec = importlib.util.spec_from_file_location("github_reference", ROOT / "adapters" / "github-reference.py")
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class FakeClient:
    def get_file(self, repository, path):
        return {"path": path, "sha": "old-sha", "content": "before\n"}

    def update_file(self, repository, path, content, message, expected_sha):
        return {"commit": {"sha": "new-commit"}, "content": {"path": path, "sha": "new-sha"}}

client = FakeClient()
file_read = module.inspect_file(client, "zzpsah/chatgpt-development-os", "docs/example.md")
assert file_read["status"] == "SUCCESS"
assert file_read["response"]["sha"] == "old-sha"

result = module.mutate_file(client, "zzpsah/chatgpt-development-os", "docs/example.md", "x", "test", "old-sha", "ALREADY_GRANTED")
assert result["status"] == "SUCCESS"
assert result["attempt"] == 1

blocked = module.mutate_file(client, "zzpsah/chatgpt-development-os", "docs/example.md", "x", "test", "old-sha", "NOT_REQUIRED")
assert blocked["status"] == "BLOCKED"

bridge_test = subprocess.run(
    [sys.executable, str(ROOT / "tools" / "test-external-runtime-bridge.py")],
    text=True,
    capture_output=True,
    check=False,
)
assert bridge_test.returncode == 0, bridge_test.stdout + bridge_test.stderr

reference_test = subprocess.run(
    [sys.executable, str(ROOT / "tools" / "test-github-reference.py")],
    text=True,
    capture_output=True,
    check=False,
)
assert reference_test.returncode == 0, reference_test.stdout + reference_test.stderr

controlled_test = subprocess.run(
    [sys.executable, str(ROOT / "tools" / "test-controlled-remote-mutation-proof.py")],
    text=True,
    capture_output=True,
    check=False,
)
assert controlled_test.returncode == 0, controlled_test.stdout + controlled_test.stderr

print("Remote Mutation Controls v1 checks passed.")
