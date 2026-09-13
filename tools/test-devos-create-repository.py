#!/usr/bin/env python3
import importlib.util
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools/devos-create-repository.py"
spec = importlib.util.spec_from_file_location("devos_create_repo", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    ready = mod.plan("@me", "test-project", False)
    assert ready["status"] == "READY"
    assert ready["capability"] == "repository.create"
    assert ready["execution"] == "NONE"
    assert ready["authorization"] == "UNCHANGED"

    bad = mod.plan("", "test-project", False)
    assert bad["status"] == "BLOCKED"

    script = Path(__file__).with_name("devos-create-repository.py")
    # Plan mode must not require credentials or make network calls.
    result = __import__("subprocess").run(
        ["python", str(script), "--owner", "@me", "--name", "plan-only"],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "Status: READY" in result.stdout

    # Apply requires explicit authorization and the local safety switch.
    result = __import__("subprocess").run(
        ["python", str(script), "--owner", "@me", "--name", "no-auth", "--apply"],
        capture_output=True, text=True, check=False,
        env={k: v for k, v in __import__("os").environ.items() if k != "DEVOS_ALLOW_REPO_CREATE"},
    )
    assert result.returncode != 0
    assert "NEEDS_APPROVAL" in result.stdout

    with patch.object(mod.urllib.request, "urlopen") as opener:
        class Response:
            status = 201
            def read(self):
                return b'{"full_name":"zzpsah/test-created","html_url":"https://github.com/zzpsah/test-created","default_branch":null}'
            def __enter__(self): return self
            def __exit__(self, *args): pass
        opener.return_value = Response()
        result = mod.github_create("@me", "test-created", False, "test", "fake-token")
        assert result["status"] == "ATTEMPTED"
        assert result["repository"] == "zzpsah/test-created"
        assert opener.call_count == 1

    with patch.object(mod.urllib.request, "urlopen", side_effect=TimeoutError()):
        result = mod.github_create("@me", "timeout-test", False, "test", "fake-token")
        assert result["status"] == "UNCERTAIN"

    with patch.object(mod.urllib.request, "urlopen") as opener:
        class Response:
            status = 201
            def read(self): return b'{"full_name":"zzpsah/no-secret-leak"}'
            def __enter__(self): return self
            def __exit__(self, *args): pass
        opener.return_value = Response()
        result = mod.github_create("@me", "no-secret-leak", False, "test", "SUPERSECRET")
        assert "SUPERSECRET" not in repr(result)

    print("PASS: repository creation capability regression corpus")

if __name__ == "__main__":
    main()
