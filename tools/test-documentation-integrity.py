#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

MODULE = Path(__file__).with_name("verify-documentation-integrity.py")
spec = importlib.util.spec_from_file_location("verify_documentation_integrity", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def assert_ok(paths):
    result = mod.evaluate_paths(paths)
    assert result["ok"], result
    return result


def assert_fail(paths):
    result = mod.evaluate_paths(paths)
    assert not result["ok"], result
    return result


def main():
    # No material change -> no documentation requirement.
    assert_ok(["docs/README-NOTE.md"])

    # Material implementation without durable record must fail.
    assert_fail(["tools/example.py"])
    assert_fail(["core/example-contract.md"])
    assert_fail([".github/workflows/example.yml"])
    assert_fail(["config/example.json"])

    # Durable record in the same bounded change satisfies the syntactic guard.
    assert_ok(["tools/example.py", ".ai/CURRENT-STATE.md"])
    assert_ok(["core/example-contract.md", "docs/EXAMPLE.md"])
    assert_ok([".github/workflows/example.yml", "CHANGELOG.md"])
    assert_ok(["config/example.json", "README.md"])

    # Implementation authorities never self-document merely because they are Markdown.
    result = assert_fail(["core/actionable-hold-scoped-approval.md"])
    assert result["durable"] == []

    # Root operating docs are durable records, not implementation artifacts.
    result = assert_ok(["AGENTS.md"])
    assert result["material"] == []

    print("PASS: documentation-integrity deterministic regression corpus")


if __name__ == "__main__":
    main()
